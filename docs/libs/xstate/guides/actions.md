# Действия

**Действия** (_actions_) — это [эффект](effects.md) запустил и забыл». Их можно объявить тремя способами:

- `entry` действия выполняются при входе в состояние
- `exit` действия выполняются при выходе из состояния
- действия перехода выполняются при переходе

## API

Действия могут быть добавлены так:

```js hl_lines="10-11 16-19 27-41"
const triggerMachine = createMachine(
  {
    id: 'trigger',
    initial: 'inactive',
    states: {
      inactive: {
        on: {
          TRIGGER: {
            target: 'active',
            // transition actions
            actions: ['activate', 'sendTelemetry'],
          },
        },
      },
      active: {
        // entry actions
        entry: ['notifyActive', 'sendTelemetry'],
        // exit actions
        exit: ['notifyInactive', 'sendTelemetry'],
        on: {
          STOP: { target: 'inactive' },
        },
      },
    },
  },
  {
    actions: {
      // action implementations
      activate: (context, event) => {
        console.log('activating...');
      },
      notifyActive: (context, event) => {
        console.log('active!');
      },
      notifyInactive: (context, event) => {
        console.log('inactive!');
      },
      sendTelemetry: (context, event) => {
        console.log('time:', Date.now());
      },
    },
  }
);
```

!!!note "Когда мне следует использовать переход (transition),<br />а когда - входные и выходные действия (action)?"

    Они означают разные вещи:

    Действие входа или выхода означает «выполнить это действие **при любом переходе, который входит или выходит из этого состояния**». Используйте действия входа или выхода, когда само действие зависит только от узла состояния, в котором оно находится, а не от узлов или событий предыдущего или следующего состояния.

    ```js
    // ...
    {
    	idle: {
    		on: {
    		LOAD: 'loading'
    		}
    	},
    	loading: {
    		// this action is executed whenever the 'loading' state is entered
    		entry: 'fetchData'
    	}
    }
    // ...
    ```

    Действие перехода означает «выполнить это действие **только на этом переходе**». Используйте действия перехода, когда действие зависит от события и узла состояния, в котором оно находится в данный момент.

    ```js
    // ...
    {
    	idle: {
    		on: {
    		LOAD: {
    			target: 'loading',
    			// this action is executed only on this transition
    			actions: 'fetchData'
    		}
    	},
    	loading: {
    		// ...
    	}
    }
    // ...
    ```

!!!tip "Подсказка"

    Реализации действий можно быстро прототипировать, указав функцию действия непосредственно в конфигурации автомата:

    ```js hl_lines="4"
    // ...
    TRIGGER: {
    	target: 'active',
    	actions: (context, event) => { console.log('activating...'); }
    }
    // ...
    ```

    Реорганизация встроенных реализаций действий в свойстве `actions` параметров автомата упрощает отладку, сериализацию, тестирование и точную визуализацию действий.

## Декларативные действия

Экземпляр `State`, возвращаемый из `machine.transition(...)`, имеет свойство `.actions`, которое представляет собой массив объектов действия для выполнения интерпретатором:

```js hl_lines="6-11"
const activeState = triggerMachine.transition('inactive', {
  type: 'TRIGGER',
});

console.log(activeState.actions);
// [
//   { type: 'activate', exec: ... },
//   { type: 'sendTelemetry', exec: ... },
//   { type: 'notifyActive', exec: ... },
//   { type: 'sendTelemetry', exec: ... }
// ]
```

Каждый объект действия имеет два свойства (и другие, которые вы можете указать):

- `type` — тип действия
- `exec` — реализация функции действия

Функция `exec` принимает три параметра:

| Параметр     | Тип          | Описание                                 |
| ------------ | ------------ | ---------------------------------------- |
| `context`    | TContext     | Текущий контекст автомата                |
| `event`      | event object | Событие, вызвавшее переход               |
| `actionMeta` | meta object  | Объект, содержащий метаданные о действии |

Объект `actionMeta` включает следующие свойства:

| Свойство | Тип           | Описание                                      |
| -------- | ------------- | --------------------------------------------- |
| `action` | action object | Исходный объект действия                      |
| `state`  | State         | Разрешенное состояние автомата после перехода |

Интерпретатор вызовет функцию `exec` с `currentState.context`, `event` и `state`, в которое перешел автомат. Вы можете настроить это поведение. Подробнее читайте в разделе «[Выполнение действий](interpretation.md#executing-actions)».

## Порядок действий

При интерпретации диаграмм состояний порядок действий не обязательно имеет значение (то есть они не должны зависеть друг от друга). Однако порядок действий в массиве `state.actions`:

1. `exit` — все действия выхода узла (ов) вышедшего состояния, от узла атомарного состояния вверх
2. `actions` — все действия перехода, определенные на выбранном переходе
3. `entry` — все действия входа узла (ов) введенного состояния, от родительского состояния вниз

!!!warning "Внимание"

    В XState версии 4.x назначенные действия `assign` имеют приоритет и выполняются перед любыми другими действиями. Это поведение будет исправлено в версии 5, так как действия назначения будут вызываться по порядку.

!!!danger "Осторожно"

    Все создатели действий, описанные здесь, возвращают **объекты действий**; это чистая функция, которая возвращает только объект действия и не обязательно отправляет событие. Не вызывайте создателей действий самостоятельно — они ничего не сделают!

    ```js
    // 🚫 Do not do this!
    entry: () => {
    // 🚫 This will do nothing; send() is not an imperative function!
    	send({ type: 'SOME_EVENT' });
    };

    console.log(send({ type: 'SOME_EVENT' }));
    // => { type: 'xstate.send', event: { type: 'SOME_EVENT' } }

    // ✅ Do this instead
    entry: send({ type: 'SOME_EVENT' });
    ```

## Действие send() {#send-action}

Создатель действия `send(action)` создает специальный объект действия `send`, который сообщает службе (т. е. [интерпретируемому автомату](interpretation.md)) отправить это событие самому себе. Он ставит событие в очередь работающей службы во внешней очереди событий, что означает, что событие отправляется на следующем «шаге» интерпретатора.

| Параметр   | Тип                                            | Описание                                                 |
| ---------- | ---------------------------------------------- | -------------------------------------------------------- |
| `event`    | string<br />event object<br />event expression | Событие для отправки в указанные `options.to` (или себе) |
| `options?` | send options                                   | Параметры отправки события                               |

Параметр отправки `options` — это объект, содержащий:

| Свойство | Тип    | Описание                                                                                          |
| -------- | ------ | ------------------------------------------------------------------------------------------------- |
| `id?`    | string | Идентификатор отправки (используется для отмены)                                                  |
| `to?`    | string | Цель события (по умолчанию `self`)                                                                |
| `delay?` | number | Тайм-аут (миллисекунды) перед отправкой события, если событие не отменено до истечения тайм-аута. |

!!!warning "Внимание"

    Функция `send(...)` является создателем действия; это чистая функция, которая возвращает только объект действия и не обязательно отправляет событие.

```js
import { createMachine, send } from 'xstate';

const lazyStubbornMachine = createMachine({
  id: 'stubborn',
  initial: 'inactive',
  states: {
    inactive: {
      on: {
        TOGGLE: {
          target: 'active',
          // send the TOGGLE event again to the service
          actions: send('TOGGLE'),
        },
      },
    },
    active: {
      on: {
        TOGGLE: { target: 'inactive' },
      },
    },
  },
});

const nextState = lazyStubbornMachine.transition(
  'inactive',
  {
    type: 'TOGGLE',
  }
);

nextState.value;
// => 'active'
nextState.actions;
// => [{ type: 'xstate.send', event: { type: 'TOGGLE' }}]

// The service will proceed to send itself the { type: 'TOGGLE' } event.
```

Аргумент события `event`, переданный в `send(event)`, может быть:

- Строковое событие, например `send('TOGGLE')`
- Объект события, например `send({type: 'TOGGLE', payload: ...})`
- Выражение события, которое представляет собой функцию, которая принимает текущий контекст `context` и событие `event`, вызвавшее действие `send()`, и возвращает объект события:

```js
import { send } from 'xstate';

// contrived example - reads from the `context` and sends
// the dynamically created event
const sendName = send((context, event) => ({
  type: 'NAME',
  name: context.user.name,
}));

const machine = createMachine({
  // ...
  on: {
    TOGGLE: {
      actions: sendName,
    },
  },
  //...
});
```

### Цели отправки {#send-targets}

Событие, отправленное создателем действия `send(...)`, может означать, что оно должно быть отправлено определенным целям, таким как [вызванные службы](communication.md) или [порожденные акторы](actors.md). Это делается путем указания свойства `{to: ...}` в действии `send (...)`:

```js
// ...
invoke: {
  id: 'some-service-id',
  src: 'someService',
  // ...
},
// ...
// Indicates to send { type: 'SOME_EVENT' } to the invoked service
actions: send({ type: 'SOME_EVENT' }, { to: 'some-service-id' })
```

Цель в свойстве `to` также может быть **целевым выражением** (_target expression_), которое представляет собой функцию, принимающую текущий контекст `context` и событие `event`, вызвавшее действие, и возвращает либо строковую цель, либо [ссылку на актора](actors.md#spawning-actors):

```js
entry: assign({
  someActor: () => {
    return spawn(someMachine, 'some-actor-name');
  },
}),
  // ...

  // Send { type: 'SOME_EVENT' } to the actor ref
  {
    actions: send(
      { type: 'SOME_EVENT' },
      {
        to: (context) => context.someActor,
      }
    ),
  };
```

!!!warning "Внимание"

    Опять же, функция `send(...)` является создателем действия и не обязательно отправляет событие. Вместо этого она возвращает объект действия, который описывает, куда будет отправлено событие:

    ```js
    console.log(send({ type: 'SOME_EVENT' }, { to: 'child' }));
    // logs:
    // {
    //   type: 'xstate.send',
    //   to: 'child',
    //   event: {
    //     type: 'SOME_EVENT'
    //   }
    // }
    ```

Чтобы отправить событие с дочернего автомата в родительский, используйте `sendParent(event)` (принимает те же аргументы, что и `send(...)`).

## Действие raise()

Создатель действия `raise()` ставит событие в очередь на диаграмму состояний во внутренней очереди событий. Это означает, что событие отправляется немедленно на текущем «шаге» интерпретатора.

| Параметр | Тип                      | Описание                        |
| -------- | ------------------------ | ------------------------------- |
| `event`  | string<br />event object | Событие, которое нужно поднять. |

```js
import { createMachine, actions } from 'xstate';
const { raise } = actions;

const raiseActionDemo = createMachine({
  id: 'raisedmo',
  initial: 'entry',
  states: {
    entry: {
      on: {
        STEP: {
          target: 'middle',
        },
        RAISE: {
          target: 'middle',
          // immediately invoke the NEXT event for 'middle'
          actions: raise('NEXT'),
        },
      },
    },
    middle: {
      on: {
        NEXT: { target: 'last' },
      },
    },
    last: {
      on: {
        RESET: { target: 'entry' },
      },
    },
  },
});
```

Кликните оба события `STEP` и `RAISE` в [визуализаторе](https://stately.ai/viz?gist=fd763ff2c161b172f719891e2544d428), чтобы увидеть разницу.

## Действие `respond()`

_Начиная с версии 4.7+_

`respond()` создает действие [`send()`](#send-action), которое отправляется в службу, отправившую событие.

При этом используются внутренние события SCXML, чтобы получить `origin` из события и установить `to` для действия `send()`.

| Параметр   | Тип                                           | Описание                                             |
| ---------- | --------------------------------------------- | ---------------------------------------------------- |
| `event`    | string<br />event object<br />send expression | Событие, которое нужно отправить обратно отправителю |
| `options?` | send options object                           | Параметры для передачи в событие `send()`            |

**Пример использования действия `respond()`**

Пример демонстрирует, как некоторая родительская служба (`authClientMachine`) отправляет событие `'CODE'` в вызываемую `authServerMachine`, а `authServerMachine` отвечает событием `'TOKEN'`.

```js
const authServerMachine = createMachine({
  initial: 'waitingForCode',
  states: {
    waitingForCode: {
      on: {
        CODE: {
          actions: respond(
            { type: 'TOKEN' },
            { delay: 10 }
          ),
        },
      },
    },
  },
});

const authClientMachine = createMachine({
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
      entry: send('CODE', { to: 'auth-server' }),
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

См. [📖 Отправка ответов](communication.md#sending-responses) для более подробной информации.

## Действие `forwardTo()`

_Начиная с версии 4.7+_

`forwardTo()` создает действие [`send()`](#send-action), которое перенаправляет самое последнее событие указанной службе через его идентификатор.

| Параметр | Тип                                     | Описание                                                           |
| -------- | --------------------------------------- | ------------------------------------------------------------------ |
| `target` | string or function that returns service | Целевая служба, в которую нужно отправить самое последнее событие. |

**Пример использования действия `forwardTo()`**

```js
import {
  createMachine,
  forwardTo,
  interpret,
} from 'xstate';

function alertService(_, receive) {
  receive((event) => {
    if (event.type === 'ALERT') {
      alert(event.message);
    }
  });
}

const parentMachine = createMachine({
  id: 'parent',
  invoke: {
    id: 'alerter',
    src: () => alertService,
  },
  on: {
    ALERT: { actions: forwardTo('alerter') },
  },
});

const parentService = interpret(parentMachine).start();

parentService.send({
  type: 'ALERT',
  message: 'hello world',
});
// => alerts "hello world"
```

## Действие escalate()

_Начиная с версии 4.7+_

`escalate()` эскалирует ошибку, отправляя ее в родительский автомат. Ошибка отправляется как специальное событие, которое распознается автоматом.

| Параметр    | Тип | Описание                                                         |
| ----------- | --- | ---------------------------------------------------------------- |
| `errorData` | any | Данные об ошибке для передачи (отправки) родительскому автомату. |

**Пример использования действия `escalate()`**

```js
import { createMachine, actions } from 'xstate';
const { escalate } = actions;

const childMachine = createMachine({
  // ...
  // This will be sent to the parent machine that invokes this child
  entry: escalate({ message: 'This is some error' }),
});

const parentMachine = createMachine({
  // ...
  invoke: {
    src: childMachine,
    onError: {
      actions: (context, event) => {
        console.log(event.data);
        //  {
        //    type: ...,
        //    data: {
        //      message: 'This is some error'
        //    }
        //  }
      },
    },
  },
});
```

## Действие log()

Создатель действия `log()` — это декларативный способ регистрации всего, что связано с текущим контекстом состояния `context` и / или событием `event`. Принимает два необязательных параметра:

| Параметр | Тип                  | Описание                                                                                                          |
| -------- | -------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `expr?`  | string<br />function | Строка или функция, которая принимает контекст `context` и событие `event` и возвращает значение для логирования. |
| `label?` | string               | Метка для обозначения залогированного сообщения message                                                           |

```js hl_lines="9 14-17 32-38"
import { createMachine, actions } from 'xstate';
const { log } = actions;

const loggingMachine = createMachine({
  id: 'logging',
  context: { count: 42 },
  initial: 'start',
  states: {
    start: {
      entry: log('started!'),
      on: {
        FINISH: {
          target: 'end',
          actions: log(
            (context, event) =>
              `count: ${context.count}, event: ${event.type}`,
            'Finish label'
          ),
        },
      },
    },
    end: {},
  },
});

const endState = loggingMachine.transition(
  'start',
  'FINISH'
);

endState.actions;
// [
//   {
//     type: 'xstate.log',
//     label: 'Finish label',
//     expr: (context, event) => ...
//   }
// ]

// The interpreter would log the action's evaluated expression
// based on the current state context and event.
```

Без параметров `log()` — это действие, которое регистрирует объект со свойствами `context` и `event`, содержащими текущий контекст и инициирующее событие.

## Действие choose()

`choose()` создает действие, которое указывает, какие действия должны быть выполнены на основе определенных условий.

| Параметр | Тип   | Описание                                                                                                       |
| -------- | ----- | -------------------------------------------------------------------------------------------------------------- |
| `conds`  | array | Массив объектов, содержащий действия `actions`, которые нужно выполнить, когда заданное условие `cond` истинно |

**Возвращает:**

Специальный объект действия `"xstate.choose"`, который внутренне оценивается, чтобы определить, какие объекты действия должны быть выполнены.

Каждый объект «условных действий» в `cond` имеет следующие свойства:

- `actions` — объекты действия для выполнения
- `cond?` — условие выполнения этих действий `actions`

!!!warning "Внимание"

    Не используйте `choose()` для выполнения действий, которые в иначе можно определить как безусловные действия, выполняемые в определенных состояниях или переходах в `entry`, `exit` или `actions`.

```js
import { actions } from 'xstate';

const { choose, log } = actions;

const maybeDoThese = choose([
  {
    cond: 'cond1',
    actions: [
      // selected when "cond1" is true
      log('cond1 chosen!'),
    ],
  },
  {
    cond: 'cond2',
    actions: [
      // selected when "cond1" is false and "cond2" is true
      log((context, event) => {
        /* ... */
      }),
      log('another action'),
    ],
  },
  {
    cond: (context, event) => {
      // some condition
      return false;
    },
    actions: [
      // selected when "cond1" and "cond2" are false
      // and the inline `cond` is true
      (context, event) => {
        // some other action
      },
    ],
  },
  {
    actions: [
      log('fall-through action'),
      // selected when "cond1", "cond2", and "cond3" are false
    ],
  },
]);
```

Это аналогично элементам SCXML `<if>`, `<elseif>` и `<else>`: [www.w3.org/TR/scxml/#if](https://www.w3.org/TR/scxml/#if)

## Действие pure()

Создатель действия `pure()` — это чистая функция (отсюда и название), которая возвращает объект(ы) действия, который должен быть выполнен, на основе контекста `context` текущего состояния и события `event`, вызвавшего действие. Это позволяет вам динамически определять, какие действия нужно выполнять.

| Параметр     | Тип      | Описание                                                                                              |
| ------------ | -------- | ----------------------------------------------------------------------------------------------------- |
| `getActions` | function | Функция, которая возвращает объект(ы) действия для выполнения на основе заданного `context` и `event` |

**Возвращает:**

Специальный объект действия «`xstate.pure`», который будет внутренне оценивать свойство `get` для определения объектов действия, которые нужно выполнить.

Параметры `getActions(context, event)`:

| Параметр  | Тип          | Описание                                 |
| --------- | ------------ | ---------------------------------------- |
| `context` | object       | Текущий `context` состояния              |
| `event`   | event object | Объект события, инициировавший действия. |

**Возвращает:**

Объект действия, массив объектов действия или `undefined`, если объектов действия нет.

```js
import { createMachine, actions } from 'xstate';

const { pure } = actions;

// Dynamically send an event to every invoked sample actor
const sendToAllSampleActors = pure((context, event) => {
  return context.sampleActors.map((sampleActor) => {
    return send('SOME_EVENT', { to: sampleActor });
  });
});
// => {
//   type: ActionTypes.Pure,
//   get: () => ... // evaluates to array of send() actions
// }

const machine = createMachine({
  // ...
  states: {
    active: {
      entry: sendToAllSampleActors,
    },
  },
});
```

## Действия в переходах без смены состояния {#actions-on-self-transitions}

[Переход без смены состояния](transitions.md#self-transitions) (_self-transition_) — это когда состояние переходит в само себя, из которого оно _может_ выйти, а затем снова войти в себя. Такие переходы могут быть **внутренними** или **внешними**:

Внутренний переход _не будет_ завершен и повторно начат, поэтому действия входа `entry` и выхода `exit` узла состояния не будут выполняться заново.

- Внутренние переходы обозначаются `{internal: true}` или `target` как `undefined`.
- Действия, определенные в свойстве `actions` перехода, будут выполнены.

Внешний переход завершится и повторно войдет в себя, поэтому действия входа `entry` и выхода `exit` узла состояния будут выполнены снова.

- По умолчанию все переходы внешние. Чтобы задать внешний переход явно, укажите `{internal: false}`.
- Действия, определенные в свойстве `actions` перехода, будут выполнены.

Например, эта счетная машина имеет одно состояние `'counting'` с внутренними и внешними переходами:

```js hl_lines="9-12"
const counterMachine = createMachine({
  id: 'counter',
  initial: 'counting',
  states: {
    counting: {
      entry: 'enterCounting',
      exit: 'exitCounting',
      on: {
        // self-transitions
        INC: { actions: 'increment' }, // internal (implicit)
        DEC: { target: 'counting', actions: 'decrement' }, // external
        DO_NOTHING: {
          internal: true,
          actions: 'logNothing',
        }, // internal (explicit)
      },
    },
  },
});

// External transition (exit + transition actions + entry)
const stateA = counterMachine.transition('counting', {
  type: 'DEC',
});
stateA.actions;
// ['exitCounting', 'decrement', 'enterCounting']

// Internal transition (transition actions)
const stateB = counterMachine.transition('counting', {
  type: 'DO_NOTHING',
});
stateB.actions;
// ['logNothing']

const stateC = counterMachine.transition('counting', {
  type: 'INC',
});
stateB.actions;
// ['increment']
```
