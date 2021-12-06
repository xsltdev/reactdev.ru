# Контекст

Хотя _конечные_ состояния четко определены в конечных автоматах и ​​диаграммах состояний, состояние, которое представляет _количественные данные_ (например, произвольные строки, числа, объекты и т. д.), которые могут быть потенциально бесконечными, представлено как [расширенное состояние](https://en.wikipedia.org/wiki/UML_state_machine#Extended_states). Это делает диаграммы состояний более полезными для реальных приложений.

В XState расширенное состояние известно как **контекст** (_context_). Ниже приведен пример использования `context` для имитации наполнения стакана водой:

```js
import { createMachine, assign } from 'xstate';

// Action to increment the context amount
const addWater = assign({
  amount: (context, event) => context.amount + 1,
});

// Guard to check if the glass is full
function glassIsFull(context, event) {
  return context.amount >= 10;
}

const glassMachine = createMachine(
  {
    id: 'glass',
    // the initial context (extended state) of the statechart
    context: {
      amount: 0,
    },
    initial: 'empty',
    states: {
      empty: {
        on: {
          FILL: {
            target: 'filling',
            actions: 'addWater',
          },
        },
      },
      filling: {
        // Transient transition
        always: {
          target: 'full',
          cond: 'glassIsFull',
        },
        on: {
          FILL: {
            target: 'filling',
            actions: 'addWater',
          },
        },
      },
      full: {},
    },
  },
  {
    actions: { addWater },
    guards: { glassIsFull },
  }
);
```

Текущий контекст ссылается на `State` как `state.context`:

```js
const nextState = glassMachine.transition(
  glassMachine.initialState,
  {
    type: 'FILL',
  }
);

nextState.context;
// => { amount: 1 }
```

## Начальный контекст

Начальный контекст указывается в свойстве `context` автомата:

```js
const counterMachine = createMachine({
  id: 'counter',
  // initial context
  context: {
    count: 0,
    message: 'Currently empty',
    user: {
      name: 'David',
    },
    allowedToIncrement: true,
    // ... etc.
  },
  states: {
    // ...
  },
});
```

Для динамического контекста (то есть контекста, начальное значение которого задается извне) вы можете использовать фабричную функцию, которая создает автомат с предоставленными значениями контекста, например:

```js
const createCounterMachine = (count, time) => {
  return createMachine({
    id: 'counter',
    // values provided from function arguments
    context: {
      count,
      time,
    },
    // ...
  });
};

const counterMachine = createCounterMachine(42, Date.now());
```

Для существующих автоматов следует использовать `machine.withContext(...)`:

```js
const counterMachine = createMachine({
  /* ... */
});

// retrieved dynamically
const someContext = { count: 42, time: Date.now() };

const dynamicCounterMachine = counterMachine.withContext(
  someContext
);
```

Исходный контекст машины можно получить из ее начального состояния:

```js
dynamicCounterMachine.initialState.context;
// => { count: 42, time: 1543687816981 }
```

Этот способ предпочтительнее прямого доступа к `machine.context`, так как начальное состояние вычисляется с помощью начальных действий `assign(...)` и проходных переходов, если таковые имеются.

## Действие assign()

Действие `assign()` используется для обновления контекста автомата. Оно принимает контекст `assigner`, который указывает, как должны быть присвоены значения в текущем контексте.

| Параметр   | Тип                  | Описание                                                   |
| ---------- | -------------------- | ---------------------------------------------------------- |
| `assigner` | object<br />function | Объект или функция, которые присваивают значения контексту |

`assigner` может быть объектом (рекомендовано):

```js
import { createMachine, assign } from 'xstate';
// example: property assigner

// ...
  actions: assign({
    // increment the current count by the event value
    count: (context, event) => context.count + event.value,

    // assign static value to the message (no function needed)
    message: 'Count changed'
  }),
// ...
```

Или функция, которая возвращает обновленное состояние:

```js
// example: context assigner

// ...

  // return a partial (or full) updated context
  actions: assign((context, event) => {
    return {
      count: context.count + event.value,
      message: 'Count changed'
    }
  }),
// ...
```

Приведенная выше функция принимает три параметра: `context`, `event` и `meta`

| Параметр  | Тип         | Описание                                          |
| --------- | ----------- | ------------------------------------------------- |
| `context` | TContext    | Текущий контекст (расширенное состояние) автомата |
| `event`   | EventObject | Событие, вызвавшее действие `assign`              |
| `meta`    | AssignMeta  | объект с мета-данными, _начиная с версии 4.7+_    |

The `meta` object contains:

- `state` - the current state in a normal transition (`undefined` for the initial state transition)
- `action` - the assign action

::: warning
The `assign(...)` function is an **action creator**; it is a pure function that only returns an action object and does _not_ imperatively make assignments to the context.
:::

## Action Order

Custom actions are always executed with regard to the _next state_ in the transition. When a state transition has `assign(...)` actions, those actions are always batched and computed _first_, to determine the next state. This is because a state is a combination of the finite state and the extended state (context).

For example, in this counter machine, the custom actions will not work as expected:

```js
const counterMachine = createMachine({
  id: 'counter',
  context: { count: 0 },
  initial: 'active',
  states: {
    active: {
      on: {
        INC_TWICE: {
          actions: [
            (context) =>
              console.log(`Before: ${context.count}`),
            assign({
              count: (context) => context.count + 1,
            }), // count === 1
            assign({
              count: (context) => context.count + 1,
            }), // count === 2
            (context) =>
              console.log(`After: ${context.count}`),
          ],
        },
      },
    },
  },
});

interpret(counterMachine)
  .start()
  .send({ type: 'INC_TWICE' });
// => "Before: 2"
// => "After: 2"
```

This is because both `assign(...)` actions are batched in order and executed first (in the microstep), so the next state `context` is `{ count: 2 }`, which is passed to both custom actions. Another way of thinking about this transition is reading it like:

> When in the `active` state and the `INC_TWICE` event occurs, the next state is the `active` state with `context.count` updated, and _then_ these custom actions are executed on that state.

A good way to refactor this to get the desired result is modeling the `context` with explicit _previous_ values, if those are needed:

```js
const counterMachine = createMachine({
  id: 'counter',
  context: { count: 0, prevCount: undefined },
  initial: 'active',
  states: {
    active: {
      on: {
        INC_TWICE: {
          actions: [
            (context) =>
              console.log(`Before: ${context.prevCount}`),
            assign({
              count: (context) => context.count + 1,
              prevCount: (context) => context.count,
            }), // count === 1, prevCount === 0
            assign({
              count: (context) => context.count + 1,
            }), // count === 2
            (context) =>
              console.log(`After: ${context.count}`),
          ],
        },
      },
    },
  },
});

interpret(counterMachine)
  .start()
  .send({ type: 'INC_TWICE' });
// => "Before: 0"
// => "After: 2"
```

The benefits of this are:

1. The extended state (context) is modeled more explicitly
2. There are no implicit intermediate states, preventing hard-to-catch bugs
3. The action order is more independent (the "Before" log can even go after the "After" log!)
4. Facilitates testing and examining the state

## Notes

- 🚫 Never mutate the machine's `context` externally. Everything happens for a reason, and every context change should happen explicitly due to an event.
- Prefer the object syntax of `assign({ ... })`. This makes it possible for future analysis tools to predict _how_ certain properties can change declaratively.
- Assignments can be stacked, and will run sequentially:

```js
// ...
  actions: [
    assign({ count: 3 }), // context.count === 3
    assign({ count: context => context.count * 2 }) // context.count === 6
  ],
// ...
```

- Just like with `actions`, it's best to represent `assign()` actions as strings or functions, and then reference them in the machine options:

```js {5}
const countMachine = createMachine({
  initial: 'start',
  context: { count: 0 }
  states: {
    start: {
      entry: 'increment'
    }
  }
}, {
  actions: {
    increment: assign({ count: context => context.count + 1 }),
    decrement: assign({ count: context => context.count - 1 })
  }
});
```

Or as named functions (same result as above):

```js {9}
const increment = assign({ count: context => context.count + 1 });
const decrement = assign({ count: context => context.count - 1 });

const countMachine = createMachine({
  initial: 'start',
  context: { count: 0 }
  states: {
    start: {
      // Named function
      entry: increment
    }
  }
});
```

- Ideally, the `context` should be representable as a plain JavaScript object; i.e., it should be serializable as JSON.
- Since `assign()` actions are _raised_, the context is updated before other actions are executed. This means that other actions within the same step will get the _updated_ `context` rather than what it was before the `assign()` action was executed. You shouldn't rely on action order for your states, but keep this in mind. See [action order](#action-order) for more details.

## TypeScript

For proper type inference, add the context type as the first type parameter to `createMachine<TContext, ...>`:

```ts
interface CounterContext {
  count: number;
  user?: {
    name: string;
  };
}

const machine = createMachine<CounterContext>({
  // ...
  context: {
    count: 0,
    user: undefined,
  },
  // ...
});
```

When applicable, you can also use `typeof ...` as a shorthand:

```ts
const context = {
  count: 0,
  user: { name: '' },
};

const machine = createMachine<typeof context>({
  // ...
  context,
  // ...
});
```

In most cases, the types for `context` and `event` in `assign(...)` actions will be automatically inferred from the type parameters passed into `createMachine<TContext, TEvent>`:

```ts
interface CounterContext {
  count: number;
}

const machine = createMachine<CounterContext>({
  // ...
  context: {
    count: 0
  },
  // ...
  {
    on: {
      INCREMENT: {
        // Inferred automatically in most cases
        actions: assign({
          count: (context) => {
            // context: { count: number }
            return context.count + 1;
          }
        })
      }
    }
  }
});
```

However, TypeScript inference isn't perfect, so the responsible thing to do is to add the context and event as generics into `assign<Context, Event>(...)`:

```ts {3}
// ...
on: {
  INCREMENT: {
    // Generics guarantee proper inference
    actions: assign<CounterContext, CounterEvent>({
      count: (context) => {
        // context: { count: number }
        return context.count + 1;
      },
    });
  }
}
// ...
```

## Quick Reference

**Set initial context**

```js
const machine = createMachine({
  // ...
  context: {
    count: 0,
    user: undefined,
    // ...
  },
});
```

**Set dynamic initial context**

```js
const createSomeMachine = (count, user) => {
  return createMachine({
    // ...
    // Provided from arguments; your implementation may vary
    context: {
      count,
      user,
      // ...
    },
  });
};
```

**Set custom initial context**

```js
const machine = createMachine({
  // ...
  // Provided from arguments; your implementation may vary
  context: {
    count: 0,
    user: undefined,
    // ...
  },
});

const myMachine = machine.withContext({
  count: 10,
  user: {
    name: 'David',
  },
});
```

**Assign to context**

```js
const machine = createMachine({
  // ...
  context: {
    count: 0,
    user: undefined,
    // ...
  },
  // ...
  on: {
    INCREMENT: {
      actions: assign({
        count: (context, event) => context.count + 1,
      }),
    },
  },
});
```

**Assignment (static)**

```js
// ...
actions: assign({
  counter: 42
}),
// ...
```

**Assignment (property)**

```js
// ...
actions: assign({
  counter: (context, event) => {
    return context.count + event.value;
  }
}),
// ...
```

**Assignment (context)**

```js
// ...
actions: assign((context, event) => {
  return {
    counter: context.count + event.value,
    time: event.time,
    // ...
  }
}),
// ...
```

**Assignment (multiple)**

```js
// ...
// assume context.count === 1
actions: [
  // assigns context.count to 1 + 1 = 2
  assign({ count: (context) => context.count + 1 }),
  // assigns context.count to 2 * 3 = 6
  assign({ count: (context) => context.count * 3 })
],
// ...
```
