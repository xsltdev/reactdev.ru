# Защищенные переходы

Часто вам нужно, чтобы переход между состояниями происходил только при соблюдении определенных условий состояния (конечных или расширенных) или события. Например, предположим, что вы создаете машину для формы поиска и хотите, чтобы поиск был разрешен только в том случае, если:

- пользователю разрешен поиск (`.canSearch` в этом примере)
- поисковый запрос `query` не пустой

Это хороший вариант использования для «защищенного перехода», который является переходом, который происходит только в том случае, если выполняется какое-то условие (`cond`). Переход с условием называется **защищенным переходом** (_guarded transition_).

## Защитные функции

**Защитная функция** (_condition function_) (также известная как **защитник** — _guard_), указанная в свойстве `.cond` перехода в виде строки или объекта условия со свойством `{type: '...'}` и принимает 3 параметра:

| Параметр   | Тип    | Описание                          |
| ---------- | ------ | --------------------------------- |
| `context`  | object | [Контекст](./context.md) автомата |
| `event`    | object | сработавшее событие               |
| `condMeta` | object | мета-данные                       |

Объект `condMeta` включает следующие свойства:

- `cond` — объект исходного состояния
- `state` — состояние машины до перехода
- `_event` — SCXML событие

**Возвращает**

`true` или `false`, что определяет, будет ли осуществлен переход.

```js hl_lines="19-20 35-39"
const searchValid = (context, event) => {
  return (
    context.canSearch &&
    event.query &&
    event.query.length > 0
  );
};

const searchMachine = createMachine(
  {
    id: 'search',
    initial: 'idle',
    context: {
      canSearch: true,
    },
    states: {
      idle: {
        on: {
          SEARCH: [
            {
              target: 'searching',
              // Only transition to 'searching'
              // if the guard (cond) evaluates to true
              cond: searchValid, // or { type: 'searchValid' }
            },
            { target: '.invalid' },
          ],
        },
        initial: 'normal',
        states: {
          normal: {},
          invalid: {},
        },
      },
      searching: {
        entry: 'executeSearch',
        // ...
      },
      searchError: {
        // ...
      },
    },
  },
  {
    guards: {
      searchValid, // optional, if the implementation doesn't change
    },
  }
);
```

Перейдите на вкладку _Events_ и отправьте событие типа `{"type": "SEARCH", "query": "something"}` в визуализаторе:

[https://stately.ai/viz?gist=09af23963bfa1767ce3900f2ae730029](https://stately.ai/viz?gist=09af23963bfa1767ce3900f2ae730029)

Если `cond` возвращает `false`, то переход не будет выбран, и переход не будет происходить из этого узла состояния. Если все переходы в дочернем состоянии имеют защитные функции, которые возвращают `false` и позволяют их выбрать, то событие будет передано в родительское состояние и обработано там.

Пример использования с контекстом `context`:

```js
import { interpret } from 'xstate';

const searchService = interpret(searchMachine)
  .onTransition((state) => console.log(state.value))
  .start();

searchService.send({ type: 'SEARCH', query: '' });
// => 'idle'

searchService.send({ type: 'SEARCH', query: 'something' });
// => 'searching'
```

!!!tip "Подсказка"

    Реализации защитных функций можно быстро прототипировать, задав свойство `cond` прямо в конфигурации автомата:

    ```js hl_lines="4"
    // ...
    SEARCH: {
      target: 'searching',
      cond: (context, event) => context.canSearch && event.query && event.query.length > 0
    }
    // ...
    ```

## Сериализация защитных функций

Защитные функции могут (и должны) быть сериализованы как строка или объект со свойством `{type: '...'}`. Детали реализации защитной функции указаны в свойстве `guards` параметров автомата, где `key` — это тип `type` защитной функции (указанный как строка или объект), а значение — это функция, которая принимает три параметра:

- `context` — текущий контекст автомата
- `event` — событие, которое вызвало потенциальный переход
- `guardMeta` — объект мета-данных о защитной функции и переходе:
  : - `cond` — исходный объект `cond`,
  : - `state` — состояние автомата то потенциального перехода

Рефакторинг приведенного выше примера:

```js hl_lines="9-11 19-27"
const searchMachine = createMachine(
  {
    // ...
    states: {
      idle: {
        on: {
          SEARCH: {
            target: 'searching',
            // The 'searchValid' guard implementation details are
            // specified in the machine config
            cond: 'searchValid', // or { type: 'searchValid' }
          },
        },
      },
      // ...
    },
  },
  {
    guards: {
      searchValid: (context, event) => {
        return (
          context.canSearch &&
          event.query &&
          event.query.length > 0
        );
      },
    },
  }
);
```

## Кастомизированные защитные функции

_Начиная с версии 4.4+_

Иногда, предпочтительнее сериализовать в JSON не только состояние переходов, но и логику защитных функций, определив её как объект с соответствующими данными:

```js hl_lines="9-13 21-30"
const searchMachine = createMachine(
  {
    // ...
    states: {
      idle: {
        on: {
          SEARCH: {
            target: 'searching',
            // Custom guard object
            cond: {
              type: 'searchValid',
              minQueryLength: 3,
            },
          },
        },
      },
      // ...
    },
  },
  {
    guards: {
      searchValid: (context, event, { cond }) => {
        // cond === { type: 'searchValid', minQueryLength: 3 }
        return (
          context.canSearch &&
          event.query &&
          event.query.length > cond.minQueryLength
        );
      },
    },
  }
);
```

## Несколько защитных функций

Если вы хотите, чтобы одно событие переходило в разные состояния в определенных ситуациях, вы можете предоставить массив условных переходов. Каждый переход будет проверяться по порядку, и будет выполнен первый переход, для которого защитная функция `cond` вернет `true`.

Например, вы можете смоделировать дверь, которая прослушивает событие `OPEN`, переходит в состояние `'opened'`, если вы администратор, или переходит в состояние `'closed.error'`, если значение `alert` истинно, или переходит в состояние `'closed.idle'` в противном случае.

```js hl_lines="30-32"
import {
  createMachine,
  actions,
  interpret,
  assign,
} from 'xstate';

const doorMachine = createMachine(
  {
    id: 'door',
    initial: 'closed',
    context: {
      level: 'user',
      alert: false, // alert when intrusions happen
    },
    states: {
      closed: {
        initial: 'idle',
        states: {
          idle: {},
          error: {},
        },
        on: {
          SET_ADMIN: {
            actions: assign({ level: 'admin' }),
          },
          SET_ALARM: {
            actions: assign({ alert: true }),
          },
          OPEN: [
            // Transitions are tested one at a time.
            // The first valid transition will be taken.
            { target: 'opened', cond: 'isAdmin' },
            { target: '.error', cond: 'shouldAlert' },
            { target: '.idle' },
          ],
        },
      },
      opened: {
        on: {
          CLOSE: { target: 'closed' },
        },
      },
    },
  },
  {
    guards: {
      isAdmin: (context) => context.level === 'admin',
      shouldAlert: (context) => context.alert === true,
    },
  }
);

const doorService = interpret(doorMachine)
  .onTransition((state) => console.log(state.value))
  .start();
// => { closed: 'idle' }

doorService.send({ type: 'OPEN' });
// => { closed: 'idle' }

doorService.send({ type: 'SET_ALARM' });
// => { closed: 'idle' }
// (state does not change, but context changes)

doorService.send({ type: 'OPEN' });
// => { closed: 'error' }

doorService.send({ type: 'SET_ADMIN' });
// => { closed: 'error' }
// (state does not change, but context changes)

doorService.send({ type: 'OPEN' });
// => 'opened'
// (since context.isAdmin === true)
```

---

<iframe src="https://stately.ai/viz/embed/?gist=8526f72c3041b38f7d7ba808c812df06" width="100%" height="400"></iframe>

!!!warning "Внимание"

    Функция `cond` всегда должна быть **чистой функцией**, которая ссылается только на параметры контекста `context` и события `event`.

!!!tip "Подсказка"

    Не злоупотребляйте защитными условиями. Если что-то может быть представлено дискретно как два или более отдельных события вместо нескольких `conds` для одного события, предпочтительнее избегать `cond` и вместо этого использовать несколько типов событий.

## Защитная функция `in`

Свойство `in` принимает идентификатор состояния в качестве аргумента и возвращает `true` тогда и только тогда, когда этот узел состояния активен в текущем состоянии. Например, мы можем добавить защитную функцию к светофору:

```js hl_lines="24"
const lightMachine = createMachine({
  id: 'light',
  initial: 'green',
  states: {
    green: {
      on: {
        TIMER: { target: 'yellow' },
      },
    },
    yellow: {
      on: {
        TIMER: { target: 'red' },
      },
    },
    red: {
      initial: 'walk',
      states: {
        walk: {
          /* ... */
        },
        wait: {
          /* ... */
        },
        stop: {
          /* ... */
        },
      },
      on: {
        TIMER: [
          {
            target: 'green',
            in: '#light.red.stop',
          },
        ],
      },
    },
  },
});
```

Когда защитная функция `in` присутствует с другими защитными функциями `cond` в том же переходе, все защитные функции должны вернуть `true`, чтобы переход был выполнен.

!!!tip "Подсказка"

    Использование защитных функций `in` обычно является признаком того, что автомат можно реорганизовать таким образом, чтобы в их использовании не было необходимости. По возможности избегайте защитных функций `in`.
