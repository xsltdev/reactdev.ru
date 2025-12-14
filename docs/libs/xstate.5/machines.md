---
title: 'Конечные автоматы'
---

[Конечный автомат](state-machines-and-statecharts.md) — это модель, описывающая поведение чего-либо, например [актора](actors.md). [Конечные автоматы](finite-states.md) описывают, как состояние актора переходит в другое состояние при наступлении [события](transitions.md).

!!!tip "Совет"

    Прочитайте наше [введение в конечные автоматы и диаграммы состояний](state-machines-and-statecharts.md), если вы ещё этого не сделали!

## Преимущества конечных автоматов

Конечные автоматы помогают создавать надёжное и устойчивое программное обеспечение. [Подробнее о преимуществах конечных автоматов](state-machines-and-statecharts.md#benefits-of-state-machines).

## Создание конечного автомата

В [XState](xstate.md) конечный автомат (называемый «машиной») создаётся с помощью функции `createMachine(config)`:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'question',
    states: {
        question: {
            on: {
                'feedback.good': {
                    target: 'thanks',
                },
            },
        },
        thanks: {
            // ...
        },
        // ...
    },
});
```

В этом примере автомат имеет два состояния: `question` и `thanks`. Состояние `question` имеет переход в состояние `thanks` при отправке события `feedback.good` автомату:

```ts
const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
    console.log(state.value);
});

feedbackActor.start();
// выводит 'question'

feedbackActor.send({ type: 'feedback.good' });
// выводит 'thanks'
```

## Создание акторов из автоматов

Автомат содержит логику актора. [Актор](actors.md) — это работающий экземпляр автомата; другими словами, это сущность, логика которой описывается автоматом. Из одного автомата можно создать несколько акторов, и каждый из этих акторов будет демонстрировать одинаковое поведение (реакцию на полученные события), но они будут независимы друг от друга и будут иметь собственные состояния.

Чтобы создать актора, используйте функцию `createActor(machine)`:

```ts
import { createActor } from 'xstate';

const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
    console.log(state.value);
});

feedbackActor.start();
// выводит 'question'
```

Вы также можете создать актора [из других типов логики](actors.md#actor-logic), таких как [функции](actors.md#fromtransition), [промисы](actors.md#frompromise) и [observables](actors.md#fromobservable).

## Предоставление реализаций

Реализации автомата — это код на конкретном языке программирования, который выполняется, но не связан напрямую с логикой конечного автомата (состояния и переходы). Это включает:

-   [Действия](actions.md), которые являются побочными эффектами типа «запустил и забыл».
-   [Акторы](actors.md), которые являются сущностями, способными взаимодействовать с актором автомата.
-   [Условия](guards.md), которые определяют, должен ли переход быть выполнен.
-   [Задержки](delayed-transitions.md), которые указывают время до выполнения отложенного перехода или отправки отложенного события.

Реализации по умолчанию можно предоставить в функции `setup({...})` при создании автомата, а затем ссылаться на эти реализации с помощью JSON-сериализуемых строк и/или объектов, таких как `{ type: 'doSomething' }`.

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    // Реализации по умолчанию
    actions: {
        doSomething: () => {
            console.log('Делаем что-то!');
        },
    },
    actors: {
        /* ... */
    },
    guards: {
        /* ... */
    },
    delays: {
        /* ... */
    },
}).createMachine({
    entry: { type: 'doSomething' },
    // ... остальная конфигурация автомата
});

const feedbackActor = createActor(feedbackMachine);

feedbackActor.start();
// выводит 'Делаем что-то!'
```

Вы можете переопределить реализации по умолчанию, _предоставив_ реализации через `machine.provide(...)`. Эта функция создаст новый автомат с той же конфигурацией, но с предоставленными реализациями:

```ts
const customFeedbackMachine = feedbackMachine.provide({
    actions: {
        doSomething: () => {
            console.log('Делаем что-то другое!');
        },
    },
});

const feedbackActor = createActor(customFeedbackMachine);

feedbackActor.start();
// выводит 'Делаем что-то другое!'
```

## Привязанные к типам помощники действий

_Начиная с XState версии 5.22.0_

Функция `setup()` предоставляет привязанные к типам помощники действий, которые полностью типизированы для context, events, actors, guards, delays и emitted типов setup. Эти помощники создают действия, привязанные к конкретному `setup()`, из которого они были созданы, и могут использоваться напрямую в автоматах, созданных этим setup.

### Создание пользовательских действий

Используйте `createAction(fn)` для создания типобезопасных пользовательских действий:

```ts
import { setup } from 'xstate';

const machineSetup = setup({
    types: {
        context: {} as { count: number; name: string },
        events: {} as
            | { type: 'increment'; value: number }
            | { type: 'reset' },
    },
});

// Создание пользовательского действия с полной типобезопасностью
// Может быть определено в любом файле, который импортирует machineSetup
// highlight-start
const logCount = machineSetup.createAction(
    ({ context, event }) => {
        // context и event полностью типизированы
        console.log(
            `Count: ${context.count}, Event: ${event.type}`
        );
    }
);
// highlight-end

const machine = machineSetup.createMachine({
    context: { count: 0, name: 'Counter' },
    initial: 'counting',
    states: {
        counting: {
            entry: logCount, // Полностью типизированное действие
            on: {
                increment: {
                    actions: logCount,
                },
            },
        },
    },
});
```

Setup предоставляет привязанные к типам версии всех основных встроенных действий:

-   `setup(…).assign(…)`
-   `setup(…).raise(…)`
-   `setup(…).emit(…)`
-   `setup(…).sendTo(…)`
-   `setup(…).log(…)`
-   `setup(…).cancel(…)`
-   `setup(…).spawnChild(…)`
-   `setup(…).stopChild(…)`
-   `setup(…).enqueueActions(…)`

Эти помощники полностью типизированы к типам вашего setup и не требуют объектов-обёрток:

```ts
import { setup } from 'xstate';

const machineSetup = setup({
    types: {
        context: {} as { count: number; items: string[] },
        events: {} as
            | { type: 'increment' }
            | { type: 'addItem'; item: string },
        emitted: {} as {
            type: 'COUNT_CHANGED';
            count: number;
        },
        // ...
    },
});

// highlight-start
// Привязанный к типу assign - context полностью типизирован
const incrementCount = machineSetup.assign({
    count: ({ context }) => context.count + 1,
});

const addItem = machineSetup.assign({
    items: ({ context, event }) => [
        ...context.items,
        event.item,
    ],
});

// Привязанный к типу raise - события полностью типизированы
const raiseIncrement = machineSetup.raise({
    type: 'increment',
});

// Привязанный к типу emit - emitted типы полностью типизированы
const emitCountChanged = machineSetup.emit(
    ({ context }) => ({
        type: 'COUNT_CHANGED',
        count: context.count,
    })
);

// Привязанный к типу sendTo - акторы полностью типизированы
const sendToLogger = machineSetup.sendTo(
    'logger',
    ({ context }) => ({
        type: 'LOG',
        message: `Count is ${context.count}`,
    })
);

// Привязанный к типу log - context и события полностью типизированы
const logContext = machineSetup.log(
    ({ context }) => `Context: ${JSON.stringify(context)}`
);

// Привязанный к типу cancel - акторы полностью типизированы
const cancelLogger = machineSetup.cancel('logger');

// Привязанный к типу stopChild - акторы полностью типизированы
const stopLogger = machineSetup.stopChild('logger');

// Привязанный к типу spawnChild - акторы полностью типизированы
const spawnLogger = machineSetup.spawnChild('logger', {
    input: ({ context }) => ({
        initialCount: context.count,
    }),
});

// Привязанный к типу enqueueActions - все помощники доступны с полной типизацией
const batchActions = machineSetup.enqueueActions(
    ({ enqueue, check }) => {
        enqueue(incrementCount);
        enqueue(logContext);

        if (check(() => true)) {
            enqueue(emitCountChanged);
        }
    }
);
// highlight-end

const machine = machineSetup.createMachine({
    context: { count: 0, items: [] },
    initial: 'active',
    states: {
        active: {
            entry: [
                incrementCount,
                logContext,
                emitCountChanged,
            ],
            on: {
                increment: {
                    actions: [incrementCount, batchActions],
                },
                addItem: {
                    actions: addItem,
                },
            },
        },
    },
});
```

## Переход состояния

_Начиная с XState версии 5.19.0_

Когда вы создаёте актор конечного автомата, следующее состояние определяется текущим состоянием автомата и событием, отправленным актору. Однако вы также можете определить следующее **состояние** и **действия** из текущего состояния и события, используя чистые функции `transition(machine, state, event)` и `initialTransition(machine)`:

```ts
// highlight-next-line
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
            entry: 'doSomething',
        },
    },
});

// highlight-next-line
const [initialState, initialActions] = initialTransition(
    machine
);

console.log(initialState.value);
// выводит 'pending'

console.log(initialActions);
// выводит []

// highlight-next-line
const [nextState, actions] = transition(
    machine,
    initialState,
    {
        type: 'start',
    }
);

console.log(nextState.value);
// выводит 'started'

console.log(actions);
// выводит [{ type: 'doSomething', … }]
```

## Определение следующего состояния

!!!warning "Внимание"

    Рекомендуется использовать функции `initialTransition(…)` и `transition(…)` вместо `getNextSnapshot(…)` и `getInitialSnapshot(…)`, которые будут объявлены устаревшими.

Когда вы создаёте актор конечного автомата, следующее состояние определяется текущим состоянием автомата и событием, отправленным актору. Если вы хотите определить следующее состояние вне актора, вы можете использовать функцию `getNextSnapshot(…)`:

```ts
import { getNextSnapshot } from 'xstate';
import { feedbackMachine } from './feedbackMachine';

const nextSnapshot = getNextSnapshot(
    feedbackMachine,
    feedbackMachine.resolveState({ value: 'question' }),
    { type: 'feedback.good' }
);

console.log(nextSnapshot.value);
// выводит 'thanks'
```

Вы также можете определить начальное состояние автомата, используя функцию `getInitialSnapshot(…)`:

```ts
import { getInitialSnapshot } from 'xstate';
import { feedbackMachine } from './feedbackMachine';

const initialSnapshot = getInitialSnapshot(
    feedbackMachine,
    // необязательные входные данные
    { defaultRating: 3 }
);

console.log(initialSnapshot.value);
// выводит 'question'
```

## Указание типов

Вы можете указать типы TypeScript внутри настройки автомата, используя свойство `.types`:

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as { feedback: string },
        events: {} as
            | { type: 'feedback.good' }
            | { type: 'feedback.bad' },
    },
    actions: {
        logTelemetry: () => {
            // TODO: реализовать
        },
    },
}).createMachine({
    // ...
});
```

Эти типы будут выводиться по всей конфигурации автомата и в созданном автомате и акторе, так что методы, такие как `machine.transition(...)` и `actor.send(...)`, будут типобезопасными.

## Модуляризация состояний

_Начиная с XState версии 5.21.0_

Вы можете использовать `.createStateConfig(...)` из setup API для создания модульных, переиспользуемых конфигураций состояний. Этот подход предоставляет несколько преимуществ, включая модульность, строгую типизацию и лучшую организацию.

### Базовое использование

```ts
import { setup } from 'xstate';

const lightMachineSetup = setup({
    // ...
});

// highlight-start
// Создание отдельных конфигураций состояний
const green = lightMachineSetup.createStateConfig({
    entry: { type: 'startTimer' },
    on: {
        TIMER: { target: 'yellow' },
        PEDESTRIAN: { target: 'yellow' },
        EMERGENCY: { target: 'red' },
    },
});

const yellow = lightMachineSetup.createStateConfig({
    entry: { type: 'startTimer' },
    on: {
        TIMER: { target: 'red' },
        EMERGENCY: { target: 'red' },
    },
});

const red = lightMachineSetup.createStateConfig({
    entry: { type: 'startTimer' },
    on: {
        TIMER: { target: 'green' },
        EMERGENCY: { target: 'green' },
    },
});
// highlight-end

// Компоновка автомата с использованием модульных конфигураций состояний
const trafficLightMachine = lightMachineSetup.createMachine(
    {
        initial: 'green',
        states: {
            green,
            yellow,
            red,
        },
    }
);
```

Все конфигурации состояний, созданные с помощью `.createStateConfig(...)`, имеют полные типы, указанные в конфигурации setup. Метод `.createStateConfig(...)` особенно полезен для очень больших, сложных конечных автоматов, где вы хотите разбить логику на управляемые части, сохраняя при этом строгую типизацию.

## Автоматы и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Лучший способ обеспечить строгую типизацию для вашего автомата — использовать функцию `setup(...)` и/или свойство `.types`.

```ts
import { setup, fromPromise } from 'xstate';

const someAction = () => {
    /* ... */
};

const someGuard = ({ context }) => context.count <= 10;

const someActor = fromPromise(async () => {
    // ...
    return 42;
});

const feedbackMachine = setup({
    types: {
        context: {} as { count: number },
        events: {} as
            | { type: 'increment' }
            | { type: 'decrement' },
    },
    actions: {
        someAction,
    },
    guards: {
        someGuard,
    },
    actors: {
        someActor,
    },
}).createMachine({
    initial: 'counting',
    states: {
        counting: {
            entry: { type: 'someAction' }, // строго типизировано
            invoke: {
                src: 'someActor', // строго типизировано
                onDone: {
                    actions: ({ event }) => {
                        event.output; // строго типизировано как number
                    },
                },
            },
            on: {
                increment: {
                    guard: { type: 'someGuard' }, // строго типизировано
                    actions: assign({
                        count: ({ context }) =>
                            context.count + 1,
                    }),
                },
            },
        },
    },
});
```

## Шпаргалка по автоматам

Используйте нашу шпаргалку по автоматам XState ниже для быстрого начала.

### Шпаргалка: создание автомата

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    initial: 'start',
    states: {
        start: {},
        // ...
    },
});
```

### Шпаргалка: настройка автомата с реализациями

```ts
import { setup } from 'xstate';

const machine = setup({
    actions: {
        someAction: () => {
            /* ... */
        },
    },
    guards: {
        someGuard: ({ context }) => context.count <= 10,
    },
    actors: {
        someActor: fromPromise(async () => {
            /* ... */
        }),
    },
    delays: {
        someDelay: () => 1000,
    },
}).createMachine({
    // ... Остальная конфигурация автомата
});
```

### Шпаргалка: привязанные к типам помощники действий

```ts
import { setup } from 'xstate';

const machineSetup = setup({
    types: {
        context: {} as { count: number },
        events: {} as
            | { type: 'increment' }
            | { type: 'reset' },
        emitted: {} as { type: 'COUNT_CHANGED' },
    },
});

// Пользовательское действие
const customAction = machineSetup.createAction(
    ({ context, event }) => {
        console.log(context.count, event.type);
    }
);

// Привязанные к типам встроенные действия
const increment = machineSetup.assign({
    count: ({ context }) => context.count + 1,
});
const raiseReset = machineSetup.raise({ type: 'reset' });
const emitEvent = machineSetup.emit({
    type: 'COUNT_CHANGED',
});
const logCount = machineSetup.log(
    ({ context }) => `Count: ${context.count}`
);

const machine = machineSetup.createMachine({
    context: { count: 0 },
    entry: [customAction, increment, emitEvent],
    on: {
        increment: { actions: increment },
        reset: { actions: raiseReset },
    },
});
```

### Шпаргалка: предоставление реализаций

```ts
import { createMachine } from 'xstate';
import { someMachine } from './someMachine';

const machineWithImpls = someMachine.provide({
    actions: {
        /* ... */
    },
    actors: {
        /* ... */
    },
    guards: {
        /* ... */
    },
    delays: {
        /* ... */
    },
});
```
