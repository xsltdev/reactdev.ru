# Использование TypeScript

Поскольку XState написан на [TypeScript](https://scriptdev.ru/ts/), строгая типизация диаграмм состояний полезна и приветствуется. Рассмотрим пример простого автомата:

```typescript
// The events that the machine handles
type LightEvent =
  | { type: 'TIMER' }
  | { type: 'POWER_OUTAGE' }
  | { type: 'PED_COUNTDOWN'; duration: number };

// The context (extended state) of the machine
interface LightContext {
  elapsed: number;
}

const lightMachine = createMachine<
  LightContext,
  LightEvent
>({
  key: 'light',
  initial: 'green',
  context: { elapsed: 0 },
  states: {
    green: {
      on: {
        TIMER: { target: 'yellow' },
        POWER_OUTAGE: { target: 'red' },
      },
    },
    yellow: {
      on: {
        TIMER: { target: 'red' },
        POWER_OUTAGE: { target: 'red' },
      },
    },
    red: {
      on: {
        TIMER: { target: 'green' },
        POWER_OUTAGE: { target: 'red' },
      },
      initial: 'walk',
      states: {
        walk: {
          on: {
            PED_COUNTDOWN: { target: 'wait' },
          },
        },
        wait: {
          on: {
            PED_COUNTDOWN: {
              target: 'stop',
              cond: (context, event) => {
                return (
                  event.duration === 0 &&
                  context.elapsed > 0
                );
              },
            },
          },
        },
        stop: {
          // Transient transition
          always: {
            target: '#light.green',
          },
        },
      },
    },
  },
});
```

Предоставление контекста и событий в качестве общих параметров для функции `createMachine()` дает множество преимуществ:

- Тип / интерфейс контекста (`TContext`) передается действиям, защитным функциям, службам и многому другому. Он также передается в глубоко вложенные состояния.
- Тип события (`TEvent`) гарантирует, что в конфигурациях перехода используются только указанные события (и встроенные, специфичные для XState). Предоставленные формы объекта события также передаются действиям, защитным функциям и службам.
- События, которые вы отправляете в автомат, будут строго типизированы, что даст вам гораздо больше уверенности в формах полезной нагрузки, которые вы будете получать.

## Объекты настроек

Общие типы для `MachineConfig<TContext, any, TEvent>` такие же, как и для `createMachine<TContext, TEvent>`. Это полезно, когда вы определяете объект конфигурации автомата _вне_ функции `createMachine(...)`, и помогает предотвратить [ошибки вывода типов](https://github.com/statelyai/xstate/issues/310):

```ts
import { MachineConfig } from 'xstate';

const myMachineConfig: MachineConfig<
  TContext,
  any,
  TEvent
> = {
  id: 'controller',
  initial: 'stopped',
  states: {
    stopped: {
      /* ... */
    },
    started: {
      /* ... */
    },
  },
  // ...
};
```

## Типизированные состояния

_Начиная с версии 4.7+_

**Типизированные состояния** (_Typestates_) — это концепция, сужающая форму общего контекста состояния `context` на основе значения состояния `value`. Это может быть полезно для предотвращения невозможных состояний и сужения контекста `context`, который должен быть в данном состоянии, без необходимости писать лишние утверждения.

`Typestate` — это интерфейс, состоящий из двух свойств:

- `value` — значение состояния typestate (на составные состояния следует ссылаться с использованием синтаксиса объекта; например, `{idle: 'error'}` вместо `idle.error`)
- `context` — суженный контекст состояния типа, когда состояние соответствует заданному `value`

Типизированные состояния автомата указываются как 3-й общий тип в `createMachine<TContext, TEvent, TTypestate>`.

**Пример:**

```ts
import { createMachine, interpret } from 'xstate';

interface User {
  name: string;
}

interface UserContext {
  user?: User;
  error?: string;
}

type UserEvent =
  | { type: 'FETCH'; id: string }
  | { type: 'RESOLVE'; user: User }
  | { type: 'REJECT'; error: string };

type UserTypestate =
  | {
      value: 'idle';
      context: UserContext & {
        user: undefined;
        error: undefined;
      };
    }
  | {
      value: 'loading';
      context: UserContext;
    }
  | {
      value: 'success';
      context: UserContext & {
        user: User;
        error: undefined;
      };
    }
  | {
      value: 'failure';
      context: UserContext & {
        user: undefined;
        error: string;
      };
    };

const userMachine = createMachine<
  UserContext,
  UserEvent,
  UserTypestate
>({
  id: 'user',
  initial: 'idle',
  states: {
    idle: {
      /* ... */
    },
    loading: {
      /* ... */
    },
    success: {
      /* ... */
    },
    failure: {
      /* ... */
    },
  },
});

const userService = interpret(userMachine);

userService.subscribe((state) => {
  if (state.matches('success')) {
    // from the UserState typestate, `user` will be defined
    state.context.user.name;
  }
});
```

!!!warning "Внимание"

    Для составных состояний все значения родительских состояний должны быть явно смоделированы, чтобы избежать ошибок типа при тестировании подсостояний.

    ```typescript
    type State =
    /* ... */
    | {
    	value: 'parent';
    	context: Context;
    	}
    | {
    	value: { parent: 'child' };
    	context: Context;
    	};
    /* ... */
    ```

    Если два состояния имеют одинаковые типы контекста, их объявления могут быть объединены с помощью объединения типов для значения.

    ```typescript
    type State =
    /* ... */
    {
    	value: 'parent' | { parent: 'child' };
    	context: Context;
    };
    /* ... */
    ```

## Исправление проблем

У XState и TypeScript есть некоторые известные ограничения. Нам нравится TypeScript, и мы _постоянно_ работаем над тем, чтобы сделать его лучше в XState.

Вот некоторые известные проблемы, которые можно обойти:

### События в опциях автомата

Когда вы используете `createMachine`, вы можете передавать реализации именованным действиям / службам / защитным функциям в вашем `config`. Например:

```ts
interface Context {}

type Event =
  | { type: 'EVENT_WITH_FLAG'; flag: boolean }
  | {
      type: 'EVENT_WITHOUT_FLAG';
    };

createMachine<Context, Event>(
  {
    on: {
      EVENT_WITH_FLAG: {
        actions: 'consoleLogData',
      },
    },
  },
  {
    actions: {
      consoleLogData: (context, event) => {
        // This will error at .flag
        console.log(event.flag);
      },
    },
  }
);
```

Причина этих ошибок в том, что внутри функции `consoleLogData` мы не знаем, какое событие вызвало ее срабатывание. Самый простой способ справиться с этим — самостоятельно подтвердить тип события.

```ts
createMachine<Context, Event>(machine, {
  actions: {
    consoleLogData: (context, event) => {
      if (event.type !== 'EVENT_WITH_FLAG') return
      // No more error at .flag!
      console.log(event.flag);
    };
  }
})
```

Также иногда возможно переместить реализацию внутрь.

```ts
createMachine<Context, Event>({
  on: {
    EVENT_WITH_FLAG: {
      actions: (context, event) => {
        // No more error, because we know which event
        // is responsible for calling this action
        console.log(event.flag);
      },
    },
  },
});
```

Этот подход работает не во всех случаях. Действие теряет свое название, поэтому на него становится менее приятно смотреть в визуализаторе. Это также означает, что если действие дублируется в нескольких местах, вам нужно скопировать и вставить его во все необходимые места.

### Типы событий в действиях входа

Типы событий во встроенных входных действиях в настоящее время не относятся к событию, которое к ним привело. Рассмотрим этот пример:

```ts
interface Context {}

type Event =
  | { type: 'EVENT_WITH_FLAG'; flag: boolean }
  | {
      type: 'EVENT_WITHOUT_FLAG';
    };

createMachine<Context, Event>({
  initial: 'state1',
  states: {
    state1: {
      on: {
        EVENT_WITH_FLAG: {
          target: 'state2',
        },
      },
    },
    state2: {
      entry: [
        (context, event) => {
          // This will error at .flag
          console.log(event.flag);
        },
      ],
    },
  },
});
```

Здесь мы не знаем, какое событие привело к действию `entry` в `state2`. Единственный способ исправить это — проделать аналогичный трюк, описанный выше:

```ts
entry: [
  (context, event) => {
    if (event.type !== 'EVENT_WITH_FLAG') return;
    // No more error at .flag!
    console.log(event.flag);
  },
];
```

### `onDone` и `onError` события в настройках автомата

Результат использования служб на основе промисов довольно сложно безопасно ввести в XState. Например, такой автомат:

```ts
interface Data {
  flag: boolean;
}

interface Context {}

type Event = {
  // Added here in order to bring out the TS errors
  type: 'UNUSED_EVENT';
};

createMachine<Context, Event>(
  {
    invoke: {
      src: async () => {
        const data: Data = {
          flag: true,
        };
        return data;
      },
      onDone: {
        actions: 'consoleLogData',
      },
      onError: {
        actions: 'consoleLogError',
      },
    },
  },
  {
    actions: {
      consoleLogData: (context, event) => {
        // Error on this line - data does not exist!
        console.log(event.data.flag);
      },
      consoleLogError: (context, event) => {
        // Error on this line - data does not exist!
        console.log(event.data);
      },
    },
  }
);
```

К сожалению, лучший способ исправить это — передать `event` в `any` и переназначить его в зависимости от того, что мы знаем о нем:

```ts
import { DoneInvokeEvent, ErrorPlatformEvent } from 'xstate'

actions: {
  consoleLogData: (context, _event: any) => {
    const event: DoneInvokeEvent<Data> = _event;
    console.log(event.data.flag);
  },
  consoleLogError: (context, _event: any) => {
    const event: ErrorPlatformEvent = _event;
    // Event.data is usually of type `Error`
    console.log(event.data.message);
  }
}
```

### Странное поведение действия assing

При запуске в режиме `strict: true` действия `assign` иногда могут вести себя очень странно.

```ts
interface Context {
  something: boolean;
}

createMachine<Context>({
  context: {
    something: true,
  },
  entry: [
    // Type 'AssignAction<{ something: false; }, AnyEventObject>'
    // is not assignable to type 'string'.
    assign(() => {
      return {
        something: false,
      };
    }),
    // Type 'AssignAction<{ something: false; }, AnyEventObject>'
    // is not assignable to type 'string'.
    assign({
      something: false,
    }),
    // Type 'AssignAction<{ something: false; }, AnyEventObject>'
    // is not assignable to type 'string'.
    assign({
      something: () => false,
    }),
  ],
});
```

Может показаться, что ничего из того, что вы пытаетесь сделать, не работает — все синтаксисы ошибочны. Исправление очень странное, но работает стабильно. Добавьте неиспользуемый аргумент контекста `context` к первому аргументу функции `assign`.

```ts
entry: [
  // No more error!
  assign((context) => {
    return {
      something: false,
    };
  }),
  // No more error!
  assign({
    something: (context) => false,
  }),
  // Unfortunately this technique doesn't work for this syntax
  // assign({
  //   something: false
  // }),
],
```

Это неприятная ошибка, которую нужно исправить, и она включает в себя перевод нашей кодовой базы в строгий режим, но мы планируем сделать это в V5.

### `keyofStringsOnly`

Если вы видите эту ошибку:

```
Type error: Type 'string | number' does not satisfy the constraint 'string'.
Type 'number' is not assignable to type 'string'. TS2344
```

Убедитесь, что ваш файл `tsconfig` не включает `"keyofStringsOnly": true,`.
