---
title: Эмиттер событий
---

_Начиная с XState версии 5.9.0_

Машины состояний и другие типы логики акторов в XState имеют возможность эмитировать (излучать) события. Это позволяет внешним обработчикам событий получать уведомления о конкретных событиях.

В машинах состояний вы можете эмитировать события с помощью создателя действий `emit(event)`.

```ts
import { setup, emit } from 'xstate';

const machine = setup({
    actions: {
        emitEvent: emit({ type: 'notification' }),
    },
}).createMachine({
    // ...
    on: {
        someEvent: {
            actions: { type: 'emitEvent' },
        },
    },
});

const actor = createActor(machine);

actor.on('notification', (event) => {
    console.log('Notification received!', event);
});

actor.start();

actor.send({ type: 'someEvent' });
// Выводит:
// "Notification received!"
// { type: "notification" }
```

## Эмитирование событий из логики акторов

Для промис-акторов, transition-акторов, observable-акторов и callback-акторов вы можете использовать метод `emit` из аргументов для эмитирования событий.

**Промис-акторы**

```ts
import { fromPromise } from 'xstate';

const logic = fromPromise(async ({ emit }) => {
    // ...
    emit({
        type: 'emitted',
        msg: 'hello',
    });
    // ...
});
```

**Transition-акторы**

```ts
import { fromTransition } from 'xstate';

const logic = fromTransition((state, event, { emit }) => {
    // ...
    emit({
        type: 'emitted',
        msg: 'hello',
    });
    // ...
    return state;
}, {});
```

**Observable-акторы**

```ts
import { fromObservable } from 'xstate';

const logic = fromObservable(({ emit }) => {
    // ...
    emit({
        type: 'emitted',
        msg: 'hello',
    });
    // ...
});
```

**Callback-акторы**

```ts
import { fromCallback } from 'xstate';

const logic = fromCallback(({ emit }) => {
    // ...
    emit({
        type: 'emitted',
        msg: 'hello',
    });
    // ...
});
```

## Создатель действия emit

Действие emit — это специальное действие, которое _эмитирует_ событие внешним обработчикам событий из логики машины состояний. Эмитируемое событие может быть определено статически или динамически:

```ts
import { setup, emit } from 'xstate';

const machine = setup({
    actions: {
        // Эмитирование статически определённого события
        emitStaticEvent: emit({
            type: 'someStaticEvent',
            data: 42,
        }),

        // Эмитирование динамически определённого события на основе контекста
        emitDynamicEvent: emit(({ context }) => ({
            type: 'someDynamicEvent',
            data: context.someData,
        })),
    },
}).createMachine({
    // ...
    on: {
        someEvent: {
            actions: [
                { type: 'emitStaticEvent' },
                { type: 'emitDynamicEvent' },
            ],
        },
    },
});
```

## Обработчики событий

Вы можете прикрепить обработчики событий к актору для прослушивания эмитируемых событий с помощью `actor.on(event, handler)`:

```ts
const someActor = createActor(someMachine);

someActor.on('someEvent', (emittedEvent) => {
    // Обработка эмитируемого события
    console.log(emittedEvent);
});

someActor.start();
```

Метод `actor.on(…)` возвращает объект подписки. Вы можете вызвать `.unsubscribe()` на нём, чтобы удалить обработчик:

```ts
const someActor = createActor(someMachine);

const subscription = someActor.on(
    'someEvent',
    (emittedEvent) => {
        // Обработка эмитируемого события
        console.log(emittedEvent);
    }
);

someActor.start();

// ...

// Прекращение прослушивания событий
subscription.unsubscribe();
```

## Обработчики событий с подстановочными знаками

Вы можете прослушивать _любое_ эмитируемое событие, используя подстановочный знак `'*'`:

```ts
const someActor = createActor(someMachine);

actor.on('*', (emitted) => {
    console.log(emitted); // Любое эмитируемое событие
});
```

Тип `emitted` события будет определён как объединение всех возможных событий, которые могут быть эмитированы машиной.

## TypeScript

Вы можете строго типизировать эмитируемые события, определив типы эмитируемых событий в свойстве `types.emitted` функции `setup(…)`:

```ts
import { setup, emit, createActor } from 'xstate';

const machine = setup({
    types: {
        emitted: {} as
            | { type: 'notification'; message: string }
            | { type: 'error'; error: Error },
        // ...
    },
}).createMachine({
    // ...
    on: {
        someEvent: {
            actions: [
                // Строго типизированное эмитируемое событие
                emit({
                    type: 'notification',
                    message: 'Hello',
                }),
            ],
        },
    },
});

const actor = createActor(machine);

// Строго типизированный обработчик события
actor.on('notification', (event) => {
    console.log(event.message); // string
});
```
