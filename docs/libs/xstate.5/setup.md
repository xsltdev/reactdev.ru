---
title: 'Настройка'
---

В XState версии 5 вы можете использовать функцию `setup({ ... })` для настройки типов и источников для ваших автоматов. Это имеет много преимуществ:

-   Уменьшение шаблонного кода для строгой типизации и предоставления именованных источников
-   Более надёжная логика автомата, так как именованные источники гарантированно существуют
-   Лучший вывод типов для действий, акторов, условий, задержек, context, событий и т.д.
-   Строго типизированные события снимков и завершения для акторов
-   Строго типизированные значения состояний
-   Возможность повторного использования логики источников

Пример использования:

```ts
import { setup, assign } from 'xstate';

const machine = setup({
    types: {
        context: {} as { count: number },
        events: {} as { type: 'inc' } | { type: 'dec' },
    },
    actions: {
        increment: assign({
            count: ({ context }) => context.count + 1,
        }),
        decrement: assign({
            count: ({ context }) => context.count - 1,
        }),
    },
}).createMachine({
    context: { count: 0 },
    on: {
        inc: { actions: 'increment' },
        dec: { actions: 'decrement' },
    },
});
```

!!!warning "Внимание"

    Убедитесь, что вы используете последнюю версию TypeScript (версия 5.0 или выше). См. документацию по [использованию TypeScript с XState](./typescript.md) для получения дополнительной информации.

## Настройка типов

Типы автомата должны быть настроены в свойстве `types` функции `setup({ types })`. Здесь вы можете настроить типы для вашего автомата, включая:

-   Типы для `context`
-   Типы для `events`, включая полезную нагрузку событий
-   Типы для `input`
-   Типы для `actions`, включая `params` действий
-   Типы для `guards`, включая `params` условий
-   Типы для `actors`

## Миграция с `createMachine`

Миграция с простого `createMachine({ ... })` на `setup({ ... }).createMachine({ ... })` для создания автомата проста.

1.  Импортируйте `setup` вместо `createMachine` из `'xstate'`
2.  Переместите `types` из `createMachine(...)` в `setup(...)`
3.  Переместите источники действий, акторов, условий и т.д. из второго аргумента `createMachine(config, sources)` в `setup({ ... })`

```ts
import {
// createMachine
  setup
} from 'xstate';

const machine =
  setup({
    types: { ... },
    actions: { ... },
    guards: { ... }
  })
  .createMachine({
    // types: { ... }
  }, /* { actions, guards, ... } */);
```

## Расширение настроек

_Начиная с XState версии 5.24.0_

Метод `.extend()` позволяет постепенно наращивать вашу настройку, расширяя действия, условия и задержки. Это открывает возможности паттернов, которые ранее были невозможны с полной типобезопасностью.

### Зачем использовать `.extend()`?

До `.extend()` все действия, условия и задержки должны были быть определены в одном вызове `setup()`. С `.extend()` вы можете:

-   **Компоновать настройки из нескольких источников**: Создавать базовые настройки, которые могут быть расширены для различных доменов или модулей
-   **Ссылаться на базовые источники в расширенных источниках**: Использовать базовые действия, условия и задержки в расширенных с полной типобезопасностью
-   **Цеплять расширения**: Постепенно наращивать сложные настройки, сохраняя типобезопасность на протяжении всего процесса

### Базовое использование

Вы можете расширить любую настройку, вызвав `.extend()` с дополнительными действиями, условиями или задержками:

```ts
import { setup, enqueueActions } from 'xstate';

const baseSetup = setup({
    actions: {
        doSomething: () => {
            console.log('Делаем что-то');
        },
    },
    guards: {
        truthy: () => true,
    },
});

// highlight-start
const extendedSetup = baseSetup.extend({
    actions: {
        doSomethingElse: () => {
            console.log('Делаем что-то другое');
        },
    },
    guards: {
        falsy: () => false,
    },
});
// highlight-end

const machine = extendedSetup.createMachine({
    entry: [
        { type: 'doSomething' },
        { type: 'doSomethingElse' },
    ], // ✅ Оба действия доступны
    on: {
        EV: {
            guard: { type: 'truthy' }, // ✅ Базовое условие доступно
            actions: { type: 'doSomethingElse' },
        },
    },
});
```

### Ссылки на базовые источники в расширенных источниках

Одна из мощных возможностей `.extend()` — это возможность ссылаться на базовые действия, условия и задержки в расширенных, с полной типобезопасностью:

```ts
import {
    setup,
    enqueueActions,
    not,
    and,
    or,
    assign,
} from 'xstate';

const baseSetup = setup({
    types: {
        context: {} as { count: number },
    },
    actions: {
        increment: assign({
            count: ({ context }) => context.count + 1,
        }),
    },
    guards: {
        truthy: () => true,
        isPositive: ({ context }) => context.count > 0,
    },
});

const extendedSetup = baseSetup.extend({
    guards: {
        // ✅ Можно ссылаться на базовое условие с помощью not()
        falsy: not('truthy'),

        // ✅ Можно комбинировать базовые условия с помощью and()
        isPositiveAndTruthy: and(['isPositive', 'truthy']),

        // ❌ Ошибка TypeScript: 'nonexistent' не существует
        // nonexistent: not('nonexistent'),
    },
    actions: {
        // ✅ Можно ссылаться на базовые действия в enqueueActions
        incrementAndLog: enqueueActions(
            ({ enqueue, check }) => {
                enqueue('increment'); // ✅ Базовое действие доступно

                if (check('isPositive')) {
                    // ✅ Расширенное условие доступно
                    enqueue.raise({ type: 'POSITIVE' });
                }

                // ❌ Ошибка TypeScript: 'nonexistent' не существует
                // enqueue('nonexistent');
            }
        ),
    },
});

const machine = extendedSetup.createMachine({
    on: {
        EV: {
            guard: 'isPositiveAndTruthy', // ✅ Расширенное условие доступно
            actions: 'incrementAndLog',
        },
    },
});
```

Задержки также могут быть расширены и использованы в действиях:

```ts
import { setup, raise } from 'xstate';

const baseSetup = setup({
    delays: {
        short: 10,
    },
});

const extendedSetup = baseSetup.extend({
    delays: {
        medium: 100,
    },
});

const machine = extendedSetup.createMachine({
    initial: 'a',
    states: {
        a: {
            entry: [
                raise({ type: 'GO' }, { delay: 'short' }), // ✅ Базовая задержка
                raise({ type: 'GO' }, { delay: 'medium' }), // ✅ Расширенная задержка
                // ❌ Ошибка TypeScript: 'long' не существует
                // raise({ type: 'GO' }, { delay: 'long' }),
            ],
            on: {
                GO: 'b',
            },
        },
        b: {
            after: {
                medium: 'c', // ✅ Расширенная задержка доступна в after
            },
        },
        c: {},
    },
});
```
