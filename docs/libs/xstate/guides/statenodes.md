# Узлы состояния

Конечный автомат содержит **узлы состояний** (_state nodes_), которые в совокупности описывают [общее состояние](./states.md) (_state_), в котором может находиться автомат. В автомате `fetchMachine`, описанном в следующем разделе, есть узлы состояний, такие как:

```js
// ...
{
  states: {
    // узел состояния
    idle: {
      on: {
        FETCH: {
          target: 'pending';
        }
      }
    }
  }
}
```

И общее **состояние** (_state_), которое является возвращаемым значением функции `machine.transition()` или значением обратного вызова `service.onTransition()`:

```js
const nextState = fetchMachine.transition('pending', {
  type: 'FULFILL',
});
// State {
//   value: { success: 'items' },
//   actions: [],
//   context: undefined,
//   ...
// }
```

## Что такое узлы состояния?

В XState **узел состояния** (_state node_) определяет конфигурацию состояния. Они определены в свойстве `state` автомата. Точно так же узлы подсостояния иерархически определены в свойстве `states` узла состояния.

Состояние, определенное из `machine.transition(state, event)`, представляет собой комбинацию узлов состояния. Например, в автомате ниже есть узел состояния `success` и узел подсостояния `items`. Значение состояния `{success: 'items'}` представляет комбинацию этих узлов состояния.

```js
const fetchMachine = createMachine({
  id: 'fetch',

  // Initial state
  initial: 'idle',

  // States
  states: {
    idle: {
      on: {
        FETCH: { target: 'pending' },
      },
    },
    pending: {
      on: {
        FULFILL: { target: 'success' },
        REJECT: { target: 'failure' },
      },
    },
    success: {
      // Initial child state
      initial: 'items',

      // Child states
      states: {
        items: {
          on: {
            'ITEM.CLICK': { target: 'item' },
          },
        },
        item: {
          on: {
            BACK: { target: 'items' },
          },
        },
      },
    },
    failure: {
      on: {
        RETRY: { target: 'pending' },
      },
    },
  },
});
```

---

<iframe src="https://stately.ai/viz/embed/?gist=932f6d193fa9d51afe31b236acf291c9" width="100%" height="360"></iframe>

## Типы узлов состояния

Есть пять различных типов узлов состояния:

- Узел **атомарного** (_atomic_) состояния не имеет дочерних состояний.
- Узел **составного** (_compound_) состояния содержит одно или несколько дочерних состояний и имеет начальное состояние, которое является ключом одного из этих дочерних состояний.
- Узел **параллельного** (_parallel_) состояния содержит два или более дочерних состояния и не имеет начального состояния, так как он представляет нахождение во всех своих дочерних состояниях одновременно.
- Узел **конечного** (_final_) состояния — это конечный узел, который представляет абстрактное «конечное» состояние.
- Узел состояния **истории** (_history_) — это абстрактный узел, который представляет преобразование в самое последнее мелкое или глубокое состояние истории своего родительского узла.

Тип узла состояния может быть явно определен на узле состояния:

```js
const machine = createMachine({
  id: 'fetch',
  initial: 'idle',
  states: {
    idle: {
      type: 'atomic',
      on: {
        FETCH: { target: 'pending' },
      },
    },
    pending: {
      type: 'parallel',
      states: {
        resource1: {
          type: 'compound',
          initial: 'pending',
          states: {
            pending: {
              on: {
                'FULFILL.resource1': { target: 'success' },
              },
            },
            success: {
              type: 'final',
            },
          },
        },
        resource2: {
          type: 'compound',
          initial: 'pending',
          states: {
            pending: {
              on: {
                'FULFILL.resource2': { target: 'success' },
              },
            },
            success: {
              type: 'final',
            },
          },
        },
      },
      onDone: 'success',
    },
    success: {
      type: 'compound',
      initial: 'items',
      states: {
        items: {
          on: {
            'ITEM.CLICK': { target: 'item' },
          },
        },
        item: {
          on: {
            BACK: { target: 'items' },
          },
        },
        hist: {
          type: 'history',
          history: 'shallow',
        },
      },
    },
  },
});
```

---

<iframe src="https://stately.ai/viz/embed/?gist=75cc77b35e98744e8d10902147feb313" width="100%" height="400"></iframe>

Явное указание `type` как `'atomic'`, `'compound'`, `'parallel'`, `'history'` или `'final'` полезно для анализа и проверки типов в TypeScript. Однако это требуется только для параллельного, исторического и конечного состояний.

## Узлы проходного состояния

**Узел проходного состояния** (_transient state node_) — это "проходной" узел состояния, который немедленно переходит к другому узлу состояния; то есть автомат не остается в проходном состоянии. Узлы проходного состояния полезны для определения того, в какое состояние автомат должен действительно перейти из предыдущего состояния на основе условий. Они больше всего похожи на [псевдосостояния выбора](https://www.uml-diagrams.org/state-machine-diagrams.html#choice-pseudostate) в UML.

Лучший способ определить узел проходного состояния — это бессобытийное состояние (eventless state) и постоянный переход `always`. Это переход, при котором немедленно выполняется первое условие, которое оценивается как истинное.

Например, начальное переходное состояние этого автомата преобразуется в `'morning'`, `'afternoon'` или `'evening'`, в зависимости от того, какое сейчас время (детали реализации скрыты):

```js hl_lines="10-16"
const timeOfDayMachine = createMachine(
  {
    id: 'timeOfDay',
    initial: 'unknown',
    context: {
      time: undefined,
    },
    states: {
      // Transient state
      unknown: {
        always: [
          { target: 'morning', cond: 'isBeforeNoon' },
          { target: 'afternoon', cond: 'isBeforeSix' },
          { target: 'evening' },
        ],
      },
      morning: {},
      afternoon: {},
      evening: {},
    },
  },
  {
    guards: {
      isBeforeNoon: {},
      isBeforeSix: {},
    },
  }
);

const timeOfDayService = interpret(
  timeOfDayMachine.withContext({ time: Date.now() })
)
  .onTransition((state) => console.log(state.value))
  .start();

// => 'morning' (assuming the time is before noon)
```

---

<iframe src="https://stately.ai/viz/embed/?gist=ca6a3f84f585c3e9cd6aadc3ae00b886" width="100%" height="360"></iframe>

## Метаданные узла состояния

Мета-данные, которые представляют собой статические данные, описывающие соответствующие свойства любого [узла состояния](./statenodes.md), могут быть указаны в свойстве `.meta` узла состояния:

```js hl_lines="19-21 24-26 32-34 37-39 42-44"
const fetchMachine = createMachine({
  id: 'fetch',
  initial: 'idle',
  states: {
    idle: {
      on: {
        FETCH: { target: 'loading' },
      },
    },
    loading: {
      after: {
        3000: { target: 'failure.timeout' },
      },
      on: {
        RESOLVE: { target: 'success' },
        REJECT: { target: 'failure' },
        TIMEOUT: { target: 'failure.timeout' }, // manual timeout
      },
      meta: {
        message: 'Loading...',
      },
    },
    success: {
      meta: {
        message: 'The request succeeded!',
      },
    },
    failure: {
      initial: 'rejection',
      states: {
        rejection: {
          meta: {
            message: 'The request failed.',
          },
        },
        timeout: {
          meta: {
            message: 'The request timed out.',
          },
        },
      },
      meta: {
        alert: 'Uh oh.',
      },
    },
  },
});
```

Текущее состояние машины собирает `.meta`-данные всех узлов состояния, представленных значением состояния, и помещает их в объект, где:

- Ключи — это [идентификаторы узлов состояния](./ids.md).
- Значения — это значения мета-узла состояния `.meta`.

## Теги

Узлы состояния могут иметь **теги** (_tags_), которые представляют собой строковые термины, помогающие описать узел состояния. Теги - это метаданные, которые могут быть полезны при классификации узлов различных состояний. Например, вы можете указать, какие узлы состояния представляют состояния, в которых данные загружаются, с помощью тега `"loading"` и определить, содержит ли состояние эти тегированные узлы состояния с помощью `state.hasTag(tag)`:

```js hl_lines="10 14"
const machine = createMachine({
  initial: 'idle',
  states: {
    idle: {
      on: {
        FETCH: 'loadingUser',
      },
    },
    loadingUser: {
      tags: ['loading'],
      // ...
    },
    loadingFriends: {
      tags: ['loading'],
      // ...
    },
    editing: {
      // ...
    },
  },
});

machine.initialState.hasTag('loading');
// => false

machine
  .transition(machine.initialState, 'FETCH')
  .hasTag('loading');
// => true
```
