---
title: Отложенные (after) переходы
---

**Отложенные переходы** — это переходы, которые срабатывают после установленного промежутка времени. Отложенные переходы полезны для создания таймаутов и интервалов в логике вашего приложения. Если другое событие произойдёт до окончания таймера, переход не завершится.

Отложенные переходы определяются в свойстве `after` узла состояния, либо как число (измеряемое в миллисекундах), либо как строка, ссылающаяся на задержку, определённую в объекте `delays` настройки.

```ts
import { createMachine } from 'xstate';

const pushTheButtonGame = createMachine({
    initial: 'waitingForButtonPush',
    states: {
        waitingForButtonPush: {
            after: {
                5000: {
                    target: 'timedOut',
                    actions: 'logThatYouGotTimedOut',
                },
            },
            on: {
                PUSH_BUTTON: {
                    actions: 'logSuccess',
                    target: 'success',
                },
            },
        },
        success: {},
        timedOut: {},
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=78c59862-fc40-4b1e-8f9c-42f1b2ddc410" width="100%" height="400"></iframe>

!!!tip "Совет"

    Посмотрите наше видео ["Delayed (after) transitions" на YouTube](https://www.youtube.com/watch?v=5RE_eazRhrw&list=PLvWgkXBB3dd4I_l-djWVU2UGPyBgKfnTQ&index=12) (1m17s).

## Задержки

Вы можете определить задержки несколькими способами: [встроенные](#inlined-delays), [ссылочные](#referenced-delays) и как выражение.

## Встроенные задержки {#inlined-delays}

Вы можете определить встроенную задержку, указав время задержки (в миллисекундах) напрямую:

```ts
const machine = createMachine({
    initial: 'idle',
    states: {
        idle: {
            after: {
                1000: { target: 'nextState' },
            },
        },
        nextState: {},
    },
});
```

Это выполнит переход в состояние `nextState` через 1000мс.

## Ссылочные задержки {#referenced-delays}

Вы также можете определить ссылочные задержки, указав строковый ключ задержки и предоставив фактическое время задержки отдельно.

Например:

```ts
import { setup } from 'xstate';

const machine = setup({
    delays: {
        timeout: 1000,
    },
}).createMachine({
    initial: 'idle',
    states: {
        idle: {
            after: {
                timeout: { target: 'nextState' },
            },
        },
        nextState: {},
    },
});
```

## Динамические задержки

Задержки также могут быть динамически определены как функция, возвращающая время задержки в миллисекундах:

```ts
import { setup } from 'xstate';

const machine = setup({
    types: {
        context: {} as {
            attempts: number;
        },
    },
    delays: {
        timeout: ({ context }) => {
            return context.attempts * 1000;
        },
    },
}).createMachine({
    initial: 'attempting',
    states: {
        attempting: {
            after: {
                timeout: {
                    actions: assign({
                        attempts: ({ context }) =>
                            context.attempts + 1,
                    }),
                    target: 'attempting',
                },
            },
        },
        // ...
    },
});
```

## Жизненный цикл

Таймеры отложенных переходов отменяются при выходе из состояния.

## Тестирование

-   Симулированные часы

## Отложенные переходы и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `delays` вашей машины, настроив задержки в функции `setup()`:

```ts
import { setup } from 'xstate';

const machine = setup({
    delays: {
        shortTimeout: 1000,
        longTimeout: 5000,
        eventually: 10_000,
    },
}).createMachine({
    after: {
        shortTimeout: {
            /* ... */
        },
    },
});
```

## Шпаргалка по отложенным переходам

Используйте нашу шпаргалку по отложенным переходам XState ниже для быстрого старта.

```ts
createMachine({
    after: {
        DELAY: {
            /* ... */
        },
    },
}).provide({
    delays: {
        DELAY: 1000, // или выражение
    },
});
```
