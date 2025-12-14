---
title: Безсобытийные (always) переходы
---

**Безсобытийные переходы** — это переходы, которые происходят без явного события. Эти переходы _всегда_ выполняются, когда переход активен.

Безсобытийные переходы указываются в свойстве состояния `always` и часто называются переходами "always".

```ts
import { createMachine } from 'xstate';
const machine = createMachine({
    states: {
        form: {
            initial: 'valid',
            states: {
                valid: {},
                invalid: {},
            },
            always: {
                guard: 'isValid',
                target: 'valid',
            },
        },
    },
});
```

## Безсобытийные переходы и условия

Безсобытийные переходы выполняются сразу после обычных переходов. Они выполняются только если активны, например, если их [условия](guards.md) истинны. Это делает безсобытийные переходы полезными для выполнения действий при выполнении определённого условия.

## Избегайте бесконечных циклов

!!!warning "Внимание"

    Поскольку незащищённые переходы "always" всегда выполняются, вы должны быть осторожны, чтобы не создать бесконечный цикл. XState поможет защититься от большинства сценариев бесконечного цикла.

Безсобытийные переходы без `target` и `guard` вызовут бесконечный цикл. Переходы, использующие `guard` и `actions`, могут попасть в бесконечный цикл, если `guard` продолжает возвращать true.

Вы должны определять безсобытийные переходы с одним из следующих вариантов:

-   `target`
-   `guard` + `target`
-   `guard` + `actions`
-   `guard` + `target` + `actions`

Если объявлен `target`, значение должно отличаться от текущего узла состояния.

## Когда использовать

Безсобытийные переходы могут быть полезны, когда необходимо изменение состояния, но нет конкретного триггера для этого изменения.

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    id: 'kettle',
    initial: 'lukewarm',
    context: {
        temperature: 80,
    },
    states: {
        lukewarm: {
            on: {
                boil: { target: 'heating' },
            },
        },
        heating: {
            always: {
                guard: ({ context }) =>
                    context.temperature > 100,
                target: 'boiling',
            },
        },
        boiling: {
            entry: ['turnOffLight'],
            always: {
                guard: ({ context }) =>
                    context.temperature <= 100,
                target: 'heating',
            },
        },
    },
    on: {
        'temp.update': {
            actions: ['updateTemperature'],
        },
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=b2a299ef-efb8-4049-a242-2d197d27c931" width="100%" height="400"></iframe>

## Безсобытийные переходы и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Безсобытийные переходы потенциально могут быть активированы любым событием, поэтому тип `event` является объединением всех возможных событий.

```ts
const machine = createMachine({
    types: {} as {
        events:
            | { type: 'greet'; message: string }
            | { type: 'submit' };
    },
    // ...
    always: {
        actions: ({ event }) => {
            event.type; // 'greet' | 'submit'
        },
        guard: ({ event }) => {
            event.type; // 'greet' | 'submit'
            return true;
        },
    },
});
```

## Шпаргалка по безсобытийным переходам

### Шпаргалка: корневой безсобытийный (always) переход

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    always: {
        guard: 'isValid',
        actions: ['doSomething'],
    },
    // ...
});
```

### Шпаргалка: безсобытийный (always) переход в состоянии

```ts
const machine = createMachine({
    initial: 'start',
    states: {
        start: {
            always: {
                guard: 'isValid',
                target: 'otherState',
            },
        },
        otherState: {
            /* ... */
        },
    },
});
```
