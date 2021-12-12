# Вызов служб

Выражение поведения всего приложения на одном автомате может быстро стать сложным и громоздким. Естественно (и поощряется!) использовать несколько автоматов, которые обмениваются данными друг с другом для реализации сложной логики. Это очень похоже на [модель актора](https://www.brianstorti.com/the-actor-model/), где каждый экземпляр автомата считается «актором», который может отправлять и получать события (сообщения) другим «акторам» (например, обещаниям или другим машинам) и реагировать на них.

Чтобы автоматы могли взаимодействовать друг с другом, родительский автомат **вызывает** дочерний и прослушивает события, отправленные с дочернего автомата через `sendParent(...)`, или ожидает, пока дочерний автомат достигнет своего [конечного состояния](final.md), что вызовет `onDone` переход.

Вы можете вызвать:

- [Промисы](#invoking-promises), которые будут выполнять переход `onDone` при разрешении `resolve` или переход `onError` при отклонении `reject`.
- [Функции обратного вызова](#invoking-callbacks), которые могут отправлять события и получать события от родительской машины
- [Наблюдаемые](#invoking-observables), которые могут отправлять события на родительский автомат, а также сигнализировать о его завершении
- [Автоматы](#invoking-machines), которые также могут отправлять и получать события, а также уведомлять родительский автомат, когда он достигает своего [конечного состояния](final.md).

## Свойство `invoke`

Вызов определяется в конфигурации узла состояния с помощью свойства `invoke`, значением которого является объект, содержащий:

- `src` — источник вызываемой службы, который может быть:
  : - автомат
  : - функция, которая возвращает `Promise`
  : - функция, которая возвращает "обработчик обратного вызова"
  : - функция, которая возвращает "наблюдаемого"
  : - строка, которая относится к любой из 4 перечисленных опций, определенных в `options.services` данного аппарата.
  : - вызываемый объект источника (_начиная с версии 4.12+_), который содержит исходную строку в `{type: src}`, а также любые другие метаданные.
- `id` — уникальный идентификатор вызванной службы
- `onDone` — (необязательно) переход, выполняемый, когда:
  : - дочерний автомат достигает своего конечного состояния, или
  : - вызванное обещание `Promise` разрешается, или
  : - вызываемый "наблюдаемый" завершается
- `onError` — (необязательно) переход, выполняемый, когда вызываемая служба обнаруживает ошибку выполнения.
- `autoForward` — (необязательно) `true`, если все события, отправленные на этот автомат, также должны быть отправлены (или перенаправлены) вызванному дочернему автомату (по умолчанию `false`)
  : - Избегайте установки `autoForward` в значение `true`, так как слепая пересылка всех событий может привести к неожиданному поведению или бесконечным циклам. Всегда предпочитайте явно отправлять события или использовать создателя действия `forward(...)` для прямой пересылки события вызываемому дочернему элементу (в настоящее время работает только для автомата).
- `data` — (необязательно, используется только при вызове автоматов) объект, который отображает свойства контекста дочернего автомата на функцию, которая возвращает соответствующее значение из контекста родительского автомата.

!!!warning "Внимание"

    Не путайте свойство `onDone` с состоянием `invoke.onDone` — они похожи на переходы, но относятся к разным вещам.

    - Свойство `onDone` на [узле состояния](statenodes.md) указывает на то, что узел составного состояния достигает [конечного состояния](final.md).
    - Свойство `invoke.onDone` относится к выполняемому вызову (`invoke.src`).

    ```js hl_lines="5 13"
    // ...
    loading: {
    	invoke: {
    		src: someSrc,
    		onDone: {/* ... */} // refers to `someSrc` being done
    	},
    	initial: 'loadFoo',
    	states: {
    		loadFoo: {/* ... */},
    		loadBar: {/* ... */},
    		loadingComplete: { type: 'final' }
    	},
    	onDone: 'loaded' // refers to 'loading.loadingComplete' being reached
    }
    // ...
    ```

## Вызов промисов

Поскольку каждый промис можно смоделировать как конечный автомат, XState может вызывать промисы "как есть". Промисы могут:

- `resolve()`, который примет переход `onDone`
- `reject()` (или выбросить ошибку), который примет переход `onError`

Если состояние, в котором активирован вызываемый промис, выходит до того, как промис разрешается, то результат промиса отбрасывается.

```js
// Function that returns a promise
// This promise might resolve with, e.g.,
// { name: 'David', location: 'Florida' }
const fetchUser = (userId) =>
  fetch(`url/to/user/${userId}`).then((response) =>
    response.json()
  );

const userMachine = createMachine({
  id: 'user',
  initial: 'idle',
  context: {
    userId: 42,
    user: undefined,
    error: undefined,
  },
  states: {
    idle: {
      on: {
        FETCH: { target: 'loading' },
      },
    },
    loading: {
      invoke: {
        id: 'getUser',
        src: (context, event) => fetchUser(context.userId),
        onDone: {
          target: 'success',
          actions: assign({
            user: (context, event) => event.data,
          }),
        },
        onError: {
          target: 'failure',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    success: {},
    failure: {
      on: {
        RETRY: { target: 'loading' },
      },
    },
  },
});
```

Разрешенные данные помещаются в событие `done.invoke.<id>` в свойстве `data`, например:

```js
{
  type: 'done.invoke.getUser',
  data: {
    name: 'David',
    location: 'Florida'
  }
}
```

### Отклонение промиса

Если промис отклоняется (reject), переход `onError` будет выполнен с событием `{type: 'error.platform'}`. Данные об ошибках доступны в свойстве `data` события:

```js
const search = (context, event) => new Promise((resolve, reject) => {
  if (!event.query.length) {
    return reject('No query specified');
    // or:
    // throw new Error('No query specified');
  }

  return resolve(getSearchResults(event.query));
});

// ...
const searchMachine = createMachine({
  id: 'search',
  initial: 'idle',
  context: {
    results: undefined,
    errorMessage: undefined,
  },
  states: {
    idle: {
      on: {
        SEARCH: { target: 'searching' }
      }
    },
    searching: {
      invoke: {
        id: 'search'
        src: search,
        onError: {
          target: 'failure',
          actions: assign({
            errorMessage: (context, event) => {
              // event is:
              // { type: 'error.platform', data: 'No query specified' }
              return event.data;
            }
          })
        },
        onDone: {
          target: 'success',
          actions: assign({ results: (_, event) => event.data })
        }
      }
    },
    success: {},
    failure: {}
  }
});
```

!!!warning "Внимание"

    Если переход `onError` отсутствует и промис отклонен, то ошибка будет проигнорирована, если не указан [строгий режим](machines.md#configuration) для автомата. В противном случае строгий режим остановит автомат и выдаст ошибку.

## Вызов функций обратного вызова

Потоки событий, отправляемых на родительский автомат, можно моделировать с помощью обработчика обратного вызова, который представляет собой функцию, которая принимает два аргумента:

- `callback` — вызывается с отправляемым событием
- `onReceive` — вызывается с помощью слушателя, который прослушивает события от родителя

Возвращаемое (необязательное) значение должно быть функцией, которая выполняет очистку (т. е. отмену подписки, предотвращение утечек памяти и т. д.) для вызванной службы при выходе из текущего состояния. Обратные вызовы **не могут** использовать синтаксис `async / await`, поскольку он автоматически помещает возвращаемое значение в `Promise`.

```js
// ...
counting: {
  invoke: {
    id: 'incInterval',
    src: (context, event) => (callback, onReceive) => {
      // This will send the 'INC' event to the parent every second
      const id = setInterval(() => callback('INC'), 1000);

      // Perform cleanup
      return () => clearInterval(id);
    }
  },
  on: {
    INC: { actions: assign({ counter: context => context.counter + 1 }) }
  }
}
// ...
```

### Прослушивание родительских событий

Вызванным обработчикам обратного вызова также предоставляется второй аргумент `onReceive`, который регистрирует прослушиватели для событий, отправляемых обработчику обратного вызова от родителя. Это обеспечивает связь между родительским и дочерним автоматами и вызванной службой обратного вызова.

Например, родительский автомат отправляет дочерней службе `ponger` событие `PING`. Дочерняя служба может прослушивать это событие с помощью `onReceive` (прослушиватель) и в ответ отправить событие `PONG` обратно родительскому автомату:

```js
const pingPongMachine = createMachine({
  id: 'pinger',
  initial: 'active',
  states: {
    active: {
      invoke: {
        id: 'ponger',
        src: (context, event) => (callback, onReceive) => {
          // Whenever parent sends 'PING',
          // send parent 'PONG' event
          onReceive((e) => {
            if (e.type === 'PING') {
              callback('PONG');
            }
          });
        },
      },
      entry: send({ type: 'PING' }, { to: 'ponger' }),
      on: {
        PONG: { target: 'done' },
      },
    },
    done: {
      type: 'final',
    },
  },
});

interpret(pingPongMachine)
  .onDone(() => done())
  .start();
```

## Вызов наблюдаемых объектов

_С версии 4.6+_

[Наблюдаемые объекты](https://github.com/tc39/proposal-observable) — это потоки значений, эмитированных с течением времени. Думайте о них как о массиве или коллекции, значения которой передаются асинхронно, а не все сразу. В JavaScript существует множество реализаций наблюдаемых объектов; самый популярный — [RxJS](https://angdev.ru/rxjs/observable/).

"Наблюдаемые" будут отправлять события (строки или объекты) на родительский автомат, но не получать события (однонаправленные). Наблюдаемый вызов — это функция, которая принимает контекст `context` и событие `event` в качестве аргументов и возвращает наблюдаемый поток событий. Подписка на наблюдаемый объект отменяется при выходе из состояния, в котором он был вызван.

```js
import { createMachine, interpret } from 'xstate';
import { interval } from 'rxjs';
import { map, take } from 'rxjs/operators';

const intervalMachine = createMachine({
  id: 'interval',
  initial: 'counting',
  context: { myInterval: 1000 },
  states: {
    counting: {
      invoke: {
        src: (context, event) =>
          interval(context.myInterval).pipe(
            map((value) => ({ type: 'COUNT', value })),
            take(5)
          ),
        onDone: 'finished',
      },
      on: {
        COUNT: { actions: 'notifyCount' },
        CANCEL: { target: 'finished' },
      },
    },
    finished: {
      type: 'final',
    },
  },
});
```

Вышеупомянутый `intervalMachine` будет получать события из `interval(...)`, сопоставленные с объектами событий, до тех пор, пока наблюдаемый объект не будет «завершен» (не завершится выдача значений). Если произойдет событие `CANCEL`, наблюдаемый будет удален (`.unsubscribe()` будет вызываться изнутри).

!!!tip "Подсказка"

    Наблюдаемые объекты необязательно создавать для каждого вызова. Вместо этого можно сослаться на «горячую наблюдаемую»:

    ```js
    import { fromEvent } from 'rxjs';

    const mouseMove$ = fromEvent(document.body, 'mousemove');

    const mouseMachine = createMachine({
    	id: 'mouse',
    	// ...
    	invoke: {
    		src: (context, event) => mouseMove$,
    	},
    	on: {
    		mousemove: {
    		/* ... */
    		},
    	},
    });
    ```

## Вызов автоматов

Автоматы обмениваются данными иерархически, а вызванные автоматы могут обмениваться данными:

- От родителя к потомку — через действие `send(EVENT, {to: 'someChildId'})`
- От потомка к родителю — через действие `sendParent(EVENT)`.

При выходе из состояния, в котором автомат был вызван — автомат останавливается.

```js
import {
  createMachine,
  interpret,
  send,
  sendParent,
} from 'xstate';

// Invoked child machine
const minuteMachine = createMachine({
  id: 'timer',
  initial: 'active',
  states: {
    active: {
      after: {
        60000: { target: 'finished' },
      },
    },
    finished: { type: 'final' },
  },
});

const parentMachine = createMachine({
  id: 'parent',
  initial: 'pending',
  states: {
    pending: {
      invoke: {
        src: minuteMachine,
        // The onDone transition will be taken when the
        // minuteMachine has reached its top-level final state.
        onDone: 'timesUp',
      },
    },
    timesUp: {
      type: 'final',
    },
  },
});

const service = interpret(parentMachine)
  .onTransition((state) => console.log(state.value))
  .start();
// => 'pending'
// ... after 1 minute
// => 'timesUp'
```

### Вызов с контекстом

Дочерние автоматы могут быть вызваны с контекстом `context`, который является производным от контекста родительского автомата `context` с помощью свойства `data`. Например, `parentMachine` ниже вызовет новую службу `timerMachine` с начальным контекстом `{duration: 3000}`:

```js
const timerMachine = createMachine({
  id: 'timer',
  context: {
    duration: 1000, // default duration
  },
  /* ... */
});

const parentMachine = createMachine({
  id: 'parent',
  initial: 'active',
  context: {
    customDuration: 3000,
  },
  states: {
    active: {
      invoke: {
        id: 'timer',
        src: timerMachine,
        // Deriving child context from parent context
        data: {
          duration: (context, event) =>
            context.customDuration,
        },
      },
    },
  },
});
```

Как и [`assign(...)`](context.md), дочерний контекст может быть отображен как объект (предпочтительно) или как функция:

```js
// Object (per-property):
data: {
  duration: (context, event) => context.customDuration,
  foo: (context, event) => event.value,
  bar: 'static value'
}

// Function (aggregate), equivalent to above:
data: (context, event) => ({
  duration: context.customDuration,
  foo: event.value,
  bar: 'static value'
})
```

!!!warning "Внимание"

    Данные `data` *заменяют* контекст по-умолчанию `context`, определенный в автомате — они не объединяются. Это поведение изменится в следующей мажорной версии.

### Конечные данные

Когда дочерний автомат достигает своего [конечного состояния](final.md), он может отправлять данные в событии `done` (например, `{type: 'done.invoke.someId', data: ...}`). Эти "конечные данные" указываются в свойстве `data` конечного состояния:

```js
const secretMachine = createMachine({
  id: 'secret',
  initial: 'wait',
  context: {
    secret: '42',
  },
  states: {
    wait: {
      after: {
        1000: { target: 'reveal' },
      },
    },
    reveal: {
      type: 'final',
      data: {
        secret: (context, event) => context.secret,
      },
    },
  },
});

const parentMachine = createMachine({
  id: 'parent',
  initial: 'pending',
  context: {
    revealedSecret: undefined,
  },
  states: {
    pending: {
      invoke: {
        id: 'secret',
        src: secretMachine,
        onDone: {
          target: 'success',
          actions: assign({
            revealedSecret: (context, event) => {
              // event is:
              // { type: 'done.invoke.secret', data: { secret: '42' } }
              return event.data.secret;
            },
          }),
        },
      },
    },
    success: {
      type: 'final',
    },
  },
});

const service = interpret(parentMachine)
  .onTransition((state) => console.log(state.context))
  .start();
// => { revealedSecret: undefined }
// ...
// => { revealedSecret: '42' }
```

### Отправка событий

- Чтобы отправить событие с дочернего автомата на родительский, используйте `sendParent(event)` (принимает те же аргументы, что и `send(...)`)
- Чтобы отправить событие с родительского автомата на дочерний, используйте `send(event, {to: <child ID>})`

!!!warning "Внимание"

    Создатели действий `send(...)` и `sendParent(...)` не обязательно отправляют события на машины. Это чистые функции, которые возвращают объект действия, описывающий, что нужно отправить, например `{type: 'xstate.send', event: ...}`. [Интерпретатор](interpretation.md) прочитает эти объекты, а затем отправит их.

    [Подробнее о `send`](actions.html#send-action)

Вот пример двух машин, `pingMachine` и `pongMachine`, которые обмениваются данными друг с другом:

```js
import {
  createMachine,
  interpret,
  send,
  sendParent,
} from 'xstate';

// Parent machine
const pingMachine = createMachine({
  id: 'ping',
  initial: 'active',
  states: {
    active: {
      invoke: {
        id: 'pong',
        src: pongMachine,
      },
      // Sends 'PING' event to child machine with ID 'pong'
      entry: send({ type: 'PING' }, { to: 'pong' }),
      on: {
        PONG: {
          actions: send(
            { type: 'PING' },
            { to: 'pong', delay: 1000 }
          ),
        },
      },
    },
  },
});

// Invoked child machine
const pongMachine = createMachine({
  id: 'pong',
  initial: 'active',
  states: {
    active: {
      on: {
        PING: {
          // Sends 'PONG' event to parent machine
          actions: sendParent('PONG', {
            delay: 1000,
          }),
        },
      },
    },
  },
});

const service = interpret(pingMachine).start();

// => 'ping'
// ...
// => 'pong'
// ..
// => 'ping'
// ...
// => 'pong'
// ...
```

## Отправка ответов

_Начиная с версии 4.7+_

Вызванная служба (или [порожденный актор](actors.md)) может _отвечать_ другой службе / субъекту; то есть она может отправлять событие _в ответ на_ событие, отправленное другой службой / актором. Это делается с помощью создателя действия `response(...)`.

Например, «клиентский» автомат `client` ниже отправляет событие `CODE` в вызванную службу `auth-server`, которая затем отвечает событием `TOKEN` через 1 секунду.

```js
import { createMachine, send, actions } from 'xstate';

const { respond } = actions;

const authServerMachine = createMachine({
  id: 'server',
  initial: 'waitingForCode',
  states: {
    waitingForCode: {
      on: {
        CODE: {
          actions: respond('TOKEN', { delay: 1000 }),
        },
      },
    },
  },
});

const authClientMachine = createMachine({
  id: 'client',
  initial: 'idle',
  states: {
    idle: {
      on: {
        AUTH: { target: 'authorizing' },
      },
    },
    authorizing: {
      invoke: {
        id: 'auth-server',
        src: authServerMachine,
      },
      entry: send({ type: 'CODE' }, { to: 'auth-server' }),
      on: {
        TOKEN: { target: 'authorized' },
      },
    },
    authorized: {
      type: 'final',
    },
  },
});
```

Этот конкретный пример может использовать `sendParent(...)` для того же эффекта; разница в том, что `response(...)` отправит событие обратно источнику полученного события, который не обязательно может быть родительским автоматом.

## Множественные службы

Вы можете вызвать несколько служб, указав каждую в массиве:

```js
// ...
invoke: [
  { id: 'service1', src: 'someService' },
  { id: 'service2', src: 'someService' },
  { id: 'logService', src: 'logService' }
],
// ...
```

Каждый вызов будет создавать _новый_ экземпляр этой службы, поэтому даже если `src` нескольких служб одинаковы (например, `someService` выше), будут вызываться несколько экземпляров `someService`.

## Настройка служб

Источники вызова (службы) могут быть настроены аналогично тому, как настраиваются действия, защитные функции и т. д. — путем указания `src` в виде строки и определения их в свойстве `services` в параметрах автомата:

```js
const fetchUser = // (same as the above example)

const userMachine = createMachine(
  {
    id: 'user',
    // ...
    states: {
      // ...
      loading: {
        invoke: {
          src: 'getUser',
          // ...
        }
      },
      // ...
    }
  },
  {
  services: {
    getUser: (context, event) => fetchUser(context.user.id)
  }
);
```

Вызов `src` также можно указать как объект (_начиная с версии 4.12+_), который описывает источник вызова с его типом `type` и другими связанными метаданными. Это можно прочитать в параметре `services` в аргументе `meta.src`:

```js
const machine = createMachine(
  {
    initial: 'searching',
    states: {
      searching: {
        invoke: {
          src: {
            type: 'search',
            endpoint: 'example.com',
          },
          // ...
        },
        // ...
      },
    },
  },
  {
    services: {
      search: (context, event, { src }) => {
        console.log(src);
        // => { endpoint: 'example.com' }
      },
    },
  }
);
```

## Тестирование

Указав службы в виде строк выше, "замоканные" службы можно выполнить, указав альтернативную реализацию с помощью `.withConfig()`:

```js
import { interpret } from 'xstate';
import { assert } from 'chai';
import { userMachine } from '../path/to/userMachine';

const mockFetchUser = async (userId) => {
  // Mock however you want, but ensure that the same
  // behavior and response format is used
  return { name: 'Test', location: 'Anywhere' };
};

const testUserMachine = userMachine.withConfig({
  services: {
    getUser: (context, event) => mockFetchUser(context.id),
  },
});

describe('userMachine', () => {
  it('should go to the "success" state when a user is found', (done) => {
    interpret(testUserMachine)
      .onTransition((state) => {
        if (state.matches('success')) {
          assert.deepEqual(state.context.user, {
            name: 'Test',
            location: 'Anywhere',
          });

          done();
        }
      })
      .start();
  });
});
```

## Ссылка на службы

_Начиная с версии 4.7+_

На службы (и [акторов](actors.md), которые являются порожденными службами) можно ссылаться непосредственно в [объекте состояния](states.md) из свойства `.children`. Объект `state.children` представляет собой сопоставление идентификаторов (ключей) службы с этими экземплярами (значениями) службы:

```js
const machine = createMachine({
  // ...
  invoke: [
    { id: 'notifier', src: createNotifier },
    { id: 'logger', src: createLogger },
  ],
  // ...
});

const service = interpret(machine)
  .onTransition((state) => {
    state.children.notifier; // service from createNotifier()
    state.children.logger; // service from createLogger()
  })
  .start();
```

При сериализации JSON объект `state.children` представляет собой сопоставление идентификаторов (ключей) службы с объектами, содержащими метаданные об этой службе.

## Краткий справочник

**Свойство `invoke`**

```js
const machine = createMachine({
  // ...
  states: {
    someState: {
      invoke: {
        // The `src` property can be:
        // - a string
        // - a machine
        // - a function that returns...
        src: (context, event) => {
          // - a promise
          // - a callback handler
          // - an observable
        },
        id: 'some-id',
        // (optional) forward machine events to invoked service
		// (currently for machines only!)
        autoForward: true,
        // (optional) the transition when the invoked
		// promise/observable/machine is done
        onDone: { target: /* ... */ },
        // (optional) the transition when an error
		// from the invoked service occurs
        onError: { target: /* ... */ }
      }
    }
  }
});
```

**Вызов промисов**

```js
// Function that returns a promise
const getDataFromAPI = () => fetch(/* ... */)
    .then(data => data.json());


// ...
{
  invoke: (context, event) => getDataFromAPI,
  // resolved promise
  onDone: {
    target: 'success',
    // resolved promise data is on event.data property
    actions: (context, event) => console.log(event.data)
  },
  // rejected promise
  onError: {
    target: 'failure',
    // rejected promise data is on event.data property
    actions: (context, event) => console.log(event.data)
  }
}
// ...
```

**Вызов функций обратного вызова**

```js
// ...
{
  invoke: (context, event) => (callback, onReceive) => {
    // Send event back to parent
    callback({ type: 'SOME_EVENT' });

    // Receive events from parent
    onReceive(event => {
      if (event.type === 'DO_SOMETHING') {
        // ...
      }
    });
  },
  // Error from callback
  onError: {
    target: 'failure',
    // Error data is on event.data property
    actions: (context, event) => console.log(event.data)
  }
},
on: {
  SOME_EVENT: { /* ... */ }
}
```

**Вызов "наблюдаемых"**

```js
import { map } from 'rxjs/operators';

// ...
{
  invoke: {
    src: (context, event) => createSomeObservable(/* ... */).pipe(
        map(value => ({ type: 'SOME_EVENT', value }))
      ),
    onDone: 'finished'
  }
},
on: {
  SOME_EVENT: /* ... */
}
// ...
```

**Вызов автоматов**

```js
const someMachine = createMachine({ /* ... */ });

// ...
{
  invoke: {
    src: someMachine,
    onDone: {
      target: 'finished',
      actions: (context, event) => {
        // Child machine's done data (.data property of its final state)
        console.log(event.data);
      }
    }
  }
}
// ...
```
