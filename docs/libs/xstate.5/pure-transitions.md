---
title: Чистые функции переходов
---

Чистые функции переходов позволяют вычислить следующее состояние и действия машины состояний без создания живого актора или выполнения каких-либо побочных эффектов. Это полезно для серверных приложений, тестирования и сценариев, где необходимо вычислять переходы состояний без побочных эффектов.

Есть две основные функции, которые вы можете использовать для вычисления переходов состояний:

-   `initialTransition(machine, input?)`: Возвращает кортеж `[initialState, initialActions]`, который представляет начальное состояние и любые действия входа для машины состояний.
-   `transition(machine, state, event)`: Возвращает кортеж `[nextState, actions]`, который представляет следующее состояние и любые действия, которые будут выполнены во время перехода.

```ts
import {
    createMachine,
    initialTransition,
    transition,
} from 'xstate';

const machine = createMachine({
    initial: 'pending',
    states: {
        pending: {
            on: {
                start: { target: 'started' },
            },
        },
        started: {
            entry: { type: 'doSomething' },
        },
    },
});

// Получение начального состояния и действий
const [initialState, initialActions] = initialTransition(
    machine
);

console.log(initialState.value); // 'pending'
console.log(initialActions); // [{ type: 'doSomething', ... }]

// Получение следующего состояния и действий
const [nextState, actions] = transition(
    machine,
    initialState,
    {
        type: 'start', // Событие для отправки
    }
);

console.log(nextState.value); // 'started'
console.log(actions); // [{ type: 'doSomething', ... }]
```

Этот чисто функциональный подход предлагает несколько преимуществ:

-   **Детерминированный**: Одинаковый вход всегда производит одинаковый выход
-   **Тестируемый**: Легко тестировать логику состояний без управления жизненным циклом акторов
-   **Подходит для сервера**: Идеален для серверных рабочих процессов и API-эндпоинтов
-   **Отлаживаемый**: Можно инспектировать изменения состояния и действия без побочных эффектов

## `initialTransition(machine, input?)`

Возвращает начальное состояние и любые действия входа для машины состояний. Если машина требует `input`, вы должны передать его как второй аргумент в `initialTransition`.

```ts
import {
    createMachine,
    initialTransition,
    transition,
} from 'xstate';

const machine = createMachine({
    initial: 'pending',
    context: ({ input }) => ({
        count: input.initialCount,
    }),
    states: {
        pending: {
            on: {
                start: { target: 'started' },
            },
        },
        started: {
            entry: { type: 'doSomething' },
        },
    },
});

// Получение начального состояния и действий
const [initialState, initialActions] = initialTransition(
    machine,
    {
        initialCount: 0,
    }
);

console.log(initialState.value); // 'pending'
console.log(initialState.context); // { count: 0 }
console.log(initialActions); // [{ type: 'doSomething', ... }]
```

### `transition(machine, state, event)`

Вычисляет следующее состояние и действия, учитывая текущее состояние и событие.

```ts
import {
    createMachine,
    initialTransition,
    transition,
} from 'xstate';

const machine = createMachine({
    initial: 'pending',
    states: {
        pending: {
            on: {
                start: { target: 'started' },
            },
        },
        started: {
            entry: { type: 'doSomething' },
        },
    },
});

// Получение начального состояния и действий
const [initialState, initialActions] = initialTransition(
    machine
);

// Получение следующего состояния и действий
const [nextState, actions] = transition(
    machine,
    initialState,
    {
        type: 'start', // Событие для отправки
    }
);

console.log(nextState.value); // 'started'
console.log(actions); // [{ type: 'doSomething', ... }]
```

## Действия

Действия представляют побочные эффекты, которые будут выполнены во время перехода. Чистые функции захватывают эти действия, но не выполняют их, давая вам полный контроль над тем, когда и как их обрабатывать.

Основное внимание следует уделить **пользовательским действиям** — действиям, которые вы определяете в своей машине состояний. Они захватываются как объекты действий с `type` и `params`:

```ts
import { createMachine, setup, transition } from 'xstate';

const machine = setup({
    actions: {
        sendEmail: (
            _,
            params: { to: string; subject: string }
        ) => {
            // Это не будет выполнено в чистых функциях
            console.log(
                `Sending email to ${params.to}: ${params.subject}`
            );
        },
        updateDatabase: (
            _,
            params: { userId: string; data: any }
        ) => {
            // Это не будет выполнено в чистых функциях
            console.log(
                `Updating user ${params.userId}`,
                params.data
            );
        },
    },
}).createMachine({
    initial: 'idle',
    states: {
        idle: {
            on: {
                processUser: {
                    target: 'processing',
                    actions: [
                        {
                            type: 'sendEmail',
                            params: ({ event }) => ({
                                to: event.email,
                                subject:
                                    'Processing started',
                            }),
                        },
                        {
                            type: 'updateDatabase',
                            params: ({ event }) => ({
                                userId: event.userId,
                                data: {
                                    status: 'processing',
                                },
                            }),
                        },
                    ],
                },
            },
        },
        processing: {},
    },
});

const [initialState] = initialTransition(machine);
const [nextState, actions] = transition(
    machine,
    initialState,
    {
        type: 'processUser',
        userId: '123',
        email: 'user@example.com',
    }
);

console.log(actions);
// [
//   {
//     type: 'sendEmail',
//     params: { to: 'user@example.com', subject: 'Processing started' }
//   },
//   {
//     type: 'updateDatabase',
//     params: { userId: '123', data: { status: 'processing' } }
//   }
// ]
```

## Восстановление сохранённого состояния

При работе с сохранённым состоянием используйте `machine.resolveState()` для восстановления снимков:

```ts
// Сохранение состояния
const stateToPersist = JSON.stringify(currentState);

// Позже, восстановление состояния
const restoredState = machine.resolveState(
    JSON.parse(stateToPersist)
);
const [nextState, actions] = transition(
    machine,
    restoredState,
    event
);
```
