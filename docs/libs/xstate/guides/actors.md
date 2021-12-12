# Акторы

_Начиная с версии 4.6+_

[Модель актора](https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C_%D0%B0%D0%BA%D1%82%D0%BE%D1%80%D0%BE%D0%B2) — это математическая модель вычислений на основе сообщений, которая упрощает взаимодействие нескольких «сущностей» (или «акторов») друг с другом. Акторы общаются, отправляя друг другу сообщения (события). Локальное состояние актора является частным, если только он не хочет поделиться им с другим актором, отправив его как событие.

Когда актор получает событие, могут произойти три вещи:

- Конечное количество сообщений может быть **отправлено** другим участникам.
- Может быть создано (или **создано**) конечное количество новых участников.
- Локальное состояние актора может измениться (определяется его **поведением**)

Конечные автоматы и диаграммы состояний очень хорошо работают с моделью акторов, поскольку они являются основанными на событиях моделями поведения и логики. Помните: когда конечный автомат переходит из-за события, следующее состояние содержит:

- Следующее значение `value` и контекст `context` (локальное состояние актора)
- Следующие действия `actions`, которые должны быть выполнены (потенциально новые созданные акторы или сообщения, отправленные другим акторам)

Акторов можно _создавать_ или [_вызывать_](communication.md). Созданные акторы имеют два основных отличия от вызванных:

- Они могут быть _созданы_ в любое время (через `spawn(...)` внутри действия `assign(...)`)
- Их можно _остановить_ в любой момент (с помощью действия `stop(...)`)

## API акторов

Актор (как реализовано в XState) имеет интерфейс:

- Свойство `id`, которое однозначно идентифицирует актора в локальной системе
- Метод `.send(...)`, который используется для отправки событий этому актору
- Метод `.getSnapshot()`, который синхронно возвращает последнее _переданное значение_ актора.

У акторов могут быть дополнительные методы:

- Метод `.stop()`, который останавливает актора и выполняет всю необходимую очистку
- Метод `.subscribe(...)` для [наблюдаемых](https://github.com/tc39/proposal-observable) акторов.

Все существующие шаблоны вызываемых сервисов подходят под этот интерфейс:

- [Вызванные промисы](communication.md#invoking-promises) — это акторы, которые игнорируют любые полученные события и отправляют не более одного события обратно родительскому объекту.
- [Вызванные обратные вызовы](communication.md#invoking-callbacks) — это акторы, которые могут отправлять события родительскому объекту (первый аргумент `callback`), получать события (второй аргумент `onReceive`) и действовать в соответствии с ними.
- [Вызываемые наблюдаемые объекты](communication.md#invoking-observables) — это акторы, чьи передаваемые значения представляют собой события, которые должны быть отправлены обратно родительскому объекту.
- [Вызванные машины](communication.md#invoking-machines) — это акторы, которые могут отправлять события родительскому объекту (действие `sendParent(...)`) или другим субъектам, на которые он ссылается (действие `send(...)`), получать события, действовать на них (переходы между состояниями и действия), создавать новых акторов (функция `spawn(...)`) и останавливать их.

!!!tip "Что такое эмитированное значение?"

    **Эмитированное значение** (_emitted value_) актора — это значение, которое подписчики получают в методе актора `.subscribe(...)`.

    - Для служб передается текущее состояние.
    - Для промисов — разрешенное значение (или `undefined`, если не выполнено).
    - Для наблюдаемых объектов — последнее переданное значение.
    - Для обратных вызовов ничего не эмитируется.

## Создание акторов

Так же, как в языках, основанных на модели акторов, таких как [Akka](https://doc.akka.io/docs/akka/current/guide/introduction.html) или [Erlang](http://www.erlang.org/docs), акторы создаются и на них ссылаются в контексте `context` (в результате действия `assign(...)`).

1. Импортируйте функцию `spawn` из `xstate`
2. В действии `assign(...)` создайте новую ссылку на актора с помощью `spawn(...)`

Функция `spawn(...)` создает **ссылку на актора**, запрашивая 1 или 2 аргумента:

- `entity` — (реактивное) значение или автомат, который представляет поведение актора. Возможные типы `entity`:
  : - [Автомат](./communication.md#invoking-machines)
  : - [Промис](./communication.md#invoking-promises)
  : - [Функция обратного вызова](./communication.md#invoking-callbacks)
  : - [Наблюдаемый объект](./communication.md#invoking-observables)
- `name` (необязательно) — строка, однозначно определяющая актора. Она должна быть уникальной для всех созданных акторов и вызванных служб.

В качестве альтернативы `spawn` принимает объект параметров в качестве второго аргумента, который может содержать следующие свойства:

- `name` (необязательно) — строка, однозначно определяющая актора. Он должен быть уникальным для всех созданных акторов и вызванных служб.
- `autoForward` — (необязательно) `true`, если все события, отправленные на этот автомат, также должны быть отправлены (или _перенаправлены_) вызванному дочернему элементу (по умолчанию `false`)
- `sync` — (необязательно) `true`, если этот автомат должен автоматически подписываться на состояние порожденной дочерней машины, состояние будет сохранено как `.state` на дочерней машине `ref`.

```js hl_lines="13-14"
import { createMachine, spawn } from 'xstate';
import { todoMachine } from './todoMachine';

const todosMachine = createMachine({
  // ...
  on: {
    'NEW_TODO.ADD': {
      actions: assign({
        todos: (context, event) => [
          ...context.todos,
          {
            todo: event.todo,
            // add a new todoMachine actor with a unique name
            ref: spawn(todoMachine, `todo-${event.id}`),
          },
        ],
      }),
    },
    // ...
  },
});
```

Если вы не предоставите аргумент `name` для `spawn(...)`, уникальное имя будет автоматически сгенерировано. Это имя будет недетерминированным.

!!!tip "Подсказка"

    Рассматривайте `const actorRef = spawn(someMachine)` как обычное значение в `context`. Вы можете разместить этот `actorRef` где угодно в `context`, в зависимости от ваших логических требований. Пока он находится в функции присваивания в `assign(...)`, он будет привязан к службе, из которой он был создан.

!!!warning "Внимание"

    Не вызывайте `spawn(...)` вне функции присваивания. Это приведет к появлению осиротевшего актора (без родителя), который не будет иметь никакого эффекта.

    ```js
    // ❌ Never call spawn(...) externally
    const someActorRef = spawn(someMachine);

    // ❌ spawn(...) is not an action creator
    {
    	actions: spawn(someMachine);
    }

    // ❌ Do not assign spawn(...) outside of an assignment function
    {
    	actions: assign({
    		// remember: this is called immediately, before a service starts
    		someActorRef: spawn(someMachine),
    	});
    }

    // ✅ Assign spawn(...) inside an assignment function
    {
    	actions: assign({
    		someActorRef: () => spawn(someMachine),
    	});
    }
    ```

В качестве акторов могут быть созданы различные типы значений.

## Отправка событий акторам

С помощью действия `send()` события можно отправлять акторам через [целевое выражение](actions.md#send-targets):

```js hl_lines="13"
const machine = createMachine({
  // ...
  states: {
    active: {
      entry: assign({
        someRef: () => spawn(someMachine),
      }),
      on: {
        SOME_EVENT: {
          // Use a target expression to send an event
          // to the actor reference
          actions: send(
            { type: 'PING' },
            { to: (context) => context.someRef }
          ),
        },
      },
    },
  },
});
```

!!!tip "Подсказка"

    Если вы передаете аргумент с уникальным `name` для `spawn(...)`, вы можете ссылаться на него в целевом выражении:

    ```js
    const loginMachine = createMachine({
    	// ...
    	entry: assign({
    		formRef: () => spawn(formMachine, 'form'),
    	}),
    	states: {
    		idle: {
    			on: {
    				LOGIN: {
    					actions: send({ type: 'SUBMIT' }, { to: 'form' }),
    				},
    			},
    		},
    	},
    });
    ```

## Остановка акторов

Акторы могут быть остановлены с помощью создателя действия `stop(...)`:

```js
const someMachine = createMachine({
  // ...
  entry: [
    // Stopping an actor by reference
    stop((context) => context.someActorRef),
    // Stopping an actor by ID
    stop('some-actor'),
  ],
});
```

## Создание промисов

Как и при [вызове промисов](communication.md#invoking-promises), промисы могут создаваться как акторы. Событие, отправленное обратно на автомат, будет действием `done.invoke.<ID>` с промисом в качестве свойства `data` в полезной нагрузке:

```js hl_lines="11"
// Returns a promise
const fetchData = (query) => {
  return fetch(
    `http://example.com?query=${event.query}`
  ).then((data) => data.json());
};

// ...
{
  actions: assign({
    ref: (_, event) => spawn(fetchData(event.query)),
  });
}
// ...
```

!!!warning "Внимание"

    Создавать акторы промисов не рекомендуется, поскольку [вызов промисов](communication.md#invoking-promises) — лучший паттерн для этого, т. к. они зависят от состояния (самоотменяемы) и имеют более предсказуемое поведение.

## Создание функций обратного вызова

Как и при [вызове функций обратного вызова](communication.md#invoking-callbacks), обратные вызовы могут быть созданы как акторы. В этом примере моделируется субъект счетчика интервалов, который увеличивает свой счет каждую секунду, а также может реагировать на события `{type: 'INC'}`.

```js hl_lines="22"
const counterInterval = (callback, receive) => {
  let count = 0;

  const intervalId = setInterval(() => {
    callback({ type: 'COUNT.UPDATE', count });
    count++;
  }, 1000);

  receive(event => {
    if (event.type === 'INC') {
      count++;
    }
  });

  return () => { clearInterval(intervalId); }
}

const machine = createMachine({
  // ...
  {
    actions: assign({
      counterRef: () => spawn(counterInterval)
    })
  }
  // ...
});
```

Затем события могут быть отправлены актору:

```js hl_lines="5-7"
const machine = createMachine({
  // ...
  on: {
    'COUNTER.INC': {
      actions: send(
        { type: 'INC' },
        { to: (context) => context.counterRef }
      ),
    },
  },
  // ...
});
```

## Создание "наблюдаемых"

Как и при [вызове наблюдаемых объектов](communication.md#invoking-observables), наблюдаемые объекты могут быть созданы как акторы:

```js hl_lines="22"
import { interval } from 'rxjs';
import { map } from 'rxjs/operators';

const createCounterObservable = (ms) => interval(ms)
  .pipe(map(count => ({ type: 'COUNT.UPDATE', count })))

const machine = createMachine({
  context: { ms: 1000 },
  // ...
  {
    actions: assign({
      counterRef: ({ ms }) => spawn(createCounterObservable(ms))
    })
  }
  // ...
  on: {
    'COUNT.UPDATE': { /* ... */ }
  }
});
```

## Создание автоматов

Автоматы — это наиболее эффективный способ использования акторов, поскольку они предлагают наибольшие возможности. Создавать автоматы можно так же, как [вызывать автоматы](communication.md#invoking-machines), когда `machine` передается в `spawn(machine)`:

```js hl_lines="13 26 30-32"
const remoteMachine = createMachine({
  id: 'remote',
  initial: 'offline',
  states: {
    offline: {
      on: {
        WAKE: 'online',
      },
    },
    online: {
      after: {
        1000: {
          actions: sendParent('REMOTE.ONLINE'),
        },
      },
    },
  },
});

const parentMachine = createMachine({
  id: 'parent',
  initial: 'waiting',
  context: {
    localOne: null,
  },
  states: {
    waiting: {
      entry: assign({
        localOne: () => spawn(remoteMachine),
      }),
      on: {
        'LOCAL.WAKE': {
          actions: send(
            { type: 'WAKE' },
            { to: (context) => context.localOne }
          ),
        },
        'REMOTE.ONLINE': { target: 'connected' },
      },
    },
    connected: {},
  },
});

const parentService = interpret(parentMachine)
  .onTransition((state) => console.log(state.value))
  .start();

parentService.send({ type: 'LOCAL.WAKE' });
// => 'waiting'
// ... after 1000ms
// => 'connected'
```

## Синхронизация и считывание состояния

_Начиная с версии 4.6.1+_

Один из основных принципов модели актора заключается в том, что состояние актора является _приватным_ и _локальным_ — оно никогда не передается, если актор не решает поделиться им посредством передачи сообщений. Придерживаясь этой модели, актор может _уведомлять_ своего родителя всякий раз, когда его состояние изменяется, отправляя ему специальное событие «`update`» с его последним состоянием. Другими словами, родительские акторы могут подписаться на состояния своих дочерних акторов.

Для этого установите `{sync: true}` в качестве опции для `srawn(...)`:

```js hl_lines="4"
// ...
{
  actions: assign({
    // Actor will send update event to parent whenever its state changes
    someRef: () => spawn(todoMachine, { sync: true }),
  });
}
// ...
```

Это автоматически подпишет автомат на состояние порожденного дочернего автомата, которое постоянно обновляется и может быть доступно через `getSnapshot()`:

```js
someService.onTransition((state) => {
  const { someRef } = state.context;

  console.log(someRef.getSnapshot());
  // => State {
  //   value: ...,
  //   context: ...
  // }
});
```

```js
someService.onTransition((state) => {
  const { someRef } = state.context;

  console.log(someRef.state);
  // => State {
  //   value: ...,
  //   context: ...
  // }
});
```

!!!warning "Внимание"

    По умолчанию для `sync` установлено значение `false`. Никогда не читайте `.state` актора, когда `sync` отключена; в противном случае вы получите ссылку на устаревшее состояние.

## Отправка обновлений

_Начиная с версии 4.7+_

Для акторов, которые не синхронизированы с родительским, актор может отправить явное событие на свой родительский автомат через `sendUpdate()`:

```js
import { createMachine, sendUpdate } from 'xstate';

const childMachine = createMachine({
  // ...
  on: {
    SOME_EVENT: {
      actions: [
        // ...
        // Creates an action that sends an update event to parent
        sendUpdate(),
      ],
    },
  },
});
```

!!!tip "Подсказка"

    Предпочитайте явно отправлять события родительскому автомату (`sendUpdate()`), а не подписываться на каждое изменение состояния. Синхронизация с созданными машинами может привести к появлению «болтливых» журналов событий, поскольку каждое обновление от дочернего элемента приводит к новому событию `xstate.update`, отправляемому дочерним автоматом родительскому.

## Краткий справочник

**Импорт `spawn`** для вызова актора:

```js
import { spawn } from 'xstate';
```

**Вызов акторов** в создателе действия `assign`:

```js
// ...
{
  actions: assign({
    someRef: (context, event) => spawn(someMachine),
  });
}
// ...
```

**Вызов различных типов** акторов:

```js
// ...
{
  actions: assign({
    // From a promise
    promiseRef: (context, event) =>
      spawn(
        new Promise((resolve, reject) => {
          // ...
        }),
        'my-promise'
      ),

    // From a callback
    callbackRef: (context, event) =>
      spawn((callback, receive) => {
        // send to parent
        callback('SOME_EVENT');

        // receive from parent
        receive((event) => {
          // handle event
        });

        // disposal
        return () => {
          /* do cleanup here */
        };
      }),

    // From an observable
    observableRef: (context, event) => spawn(someEvent$),

    // From a machine
    machineRef: (context, event) =>
      spawn(
        createMachine({
          // ...
        })
      ),
  });
}
// ...
```

**Статус синхронизации** актора:

```js
// ...
{
  actions: assign({
    someRef: () => spawn(someMachine, { sync: true }),
  });
}
// ...
```

**Получение снапшота** актора (_4.20.0+_):

```js
service.onTransition((state) => {
  const { someRef } = state.context;

  someRef.getSnapshot();
  // => State { ... }
});
```

**Отправить событие актору** с помощью создателя действия `send`:

```js
// ...
{
  actions: send(
    { type: 'SOME_EVENT' },
    {
      to: (context) => context.someRef,
    }
  );
}
// ...
```

**Отправить событие с данными актору**, используя выражение `send`:

```js
// ...
{
  actions: send(
    (context, event) => ({ ...event, type: 'SOME_EVENT' }),
    {
      to: (context) => context.someRef,
    }
  );
}
// ...
```

**Отправить событие от актора** к родительскому автомату с создателем действия `sendParent`:

```js
// ...
{
  actions: sendParent({ type: 'ANOTHER_EVENT' });
}
// ...
```

**Отправить событие с данными от актора** к родительскому автомату с помощью выражения `sendParent`:

```js
// ...
{
  actions: sendParent((context, event) => ({
    ...context,
    type: 'ANOTHER_EVENT',
  }));
}
// ...
```

**Ссылка на акторов** из `context`:

```js
someService.onTransition((state) => {
  const { someRef } = state.context;

  console.log(someRef);
  // => { id: ..., send: ... }
});
```
