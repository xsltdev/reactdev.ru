# Конечные автоматы

**Конечный автомат** (_state machine_) — это конечный набор состояний, которые могут детерминированно переходить друг в друга из-за событий.

## Конфигурация

И конечные автоматы, и диаграммы состояний определяются с помощью фабричной функции `createMachine()`:

```js
import { createMachine } from 'xstate';

const lightMachine = createMachine({
  // Machine identifier
  id: 'light',

  // Initial state
  initial: 'green',

  // Local context for entire machine
  context: {
    elapsed: 0,
    direction: 'east',
  },

  // State definitions
  states: {
    green: {
      /* ... */
    },
    yellow: {
      /* ... */
    },
    red: {
      /* ... */
    },
  },
});
```

Конфигурация машины такая же, как [конфигурация узла состояния](./statenodes.md), с добавлением свойства контекста:

- `context` — представляет локальное «расширенное состояние» для всех вложенных состояний машины. См. [контекст](./context.md) для получения более подробной информации.

## Параметры

Реализации для [действий](./actions.md), [активностей](./activities.md), [задержек](./delays.md), [защитных функций](./guards.md) и [служб](./communication.md) могут быть указаны в конфигурации машины в виде строки, а затем указаны как объект во втором аргументе `createMachine()`:

```js
const lightMachine = createMachine(
  {
    id: 'light',
    initial: 'green',
    states: {
      green: {
        // ссылка на действие в виде строки
        entry: 'alertGreen',
      },
    },
  },
  {
    actions: {
      // реализация действия
      alertGreen: (context, event) => {
        alert('Green!');
      },
    },
    activities: {
      /* ... */
    },
    delays: {
      /* ... */
    },
    guards: {
      /* ... */
    },
    services: {
      /* ... */
    },
  }
);
```

У этого объекта есть 5 необязательных свойств:

- `actions` — сопоставление действий с их реализацией
- `activities` — сопоставление активностей с их реализацией
- `delays` — сопоставление задержек с их реализацией
- `guards` — сопоставление охранников переходов с их реализацией
- `services` — сопоставление служб с их реализацией

## Расширение автомата

Существующие автоматы могут быть расширены с помощью метода `.withConfig()`, который принимает ту же структуру объекта, что и выше:

```js
const lightMachine = // (same as above example)

const noAlertLightMachine = lightMachine.withConfig({
  actions: {
    alertGreen: (context, event) => {
      console.log('green');
    }
  }
});
```

## Начальный контекст

Как показано в первом примере, контекст определяется непосредственно в самой конфигурации. Если вы хотите расширить существующую машину с другим начальным контекстом, вы можете использовать `.withContext()` и передать свой `context`:

```js
const lightMachine = // (same as first example)

const testLightMachine = lightMachine.withContext({
  elapsed: 1000,
  direction: 'north'
});
```

!!! warning "Внимание"

    Это не приведет к слиянию с исходным контекстом, а заменит исходный контекст контекстом, предоставленным для `.withContext(...)`. Вы все еще можете «объединить» контексты вручную, указав `machine.context`:

    ```js
    const testLightMachine = lightMachine.withContext({
      // merge with original context
      ...lightMachine.context,
      elapsed: 1000,
    });
    ```
