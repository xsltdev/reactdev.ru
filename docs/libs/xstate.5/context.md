---
title: 'Context'
---

В XState `context` — это способ хранения данных в [акторе](actors.md) конечного автомата.

Свойство `context` доступно во всех состояниях и используется для хранения данных, относящихся к актору. Объект `context` неизменяем, поэтому вы не можете изменять его напрямую. Вместо этого для логики конечного автомата вы можете использовать действие `assign(...)` для обновления `context`.

Свойство `context` _необязательно_; если конечный автомат указывает только [конечные состояния](finite-states.md) без внешних контекстных данных, ему может не понадобиться `context`.

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    // Инициализация конечного автомата с context
    context: {
        feedback: 'Некоторый отзыв',
    },
});

const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
    console.log(state.context.feedback);
});

feedbackActor.start();
// выводит 'Некоторый отзыв'
```

!!!warning "Внимание"

    `context` должен быть объектом. Если вам нужно хранить список элементов, оберните его в объект, например: `context: { items: [] }`.

## Начальный context

Установите начальный context автомата в свойстве `context` конфигурации автомата:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    context: {
        feedback: 'Некоторый отзыв',
        rating: 5,
        // другие свойства
    },
});
```

Объект, который вы передаёте в `context`, будет начальным значением `context` для любого актора, созданного из этого автомата.

!!!warning "Внимание"

    Не изменяйте объект `context` напрямую. Вместо этого используйте действие `assign(...)` для иммутабельного обновления `context`. Если вы будете изменять объект `context` напрямую, вы можете получить неожиданное поведение, например, изменение `context` других акторов.

### Ленивый начальный context

Context может быть инициализирован лениво, передав функцию, которая возвращает начальное значение `context`:

```ts
const feedbackMachine = createMachine({
    context: () => ({
        feedback: 'Некоторый отзыв',
        createdAt: Date.now(),
    }),
});

const feedbackActor = createActor(feedbackMachine).start();

console.log(feedbackActor.getSnapshot().context.createdAt);
// выводит текущую метку времени
```

Ленивый начальный context вычисляется для каждого актора, поэтому у каждого актора будет свой собственный объект `context`.

### Input

Вы можете предоставить входные данные для начального `context` автомата, передав свойство `input` в функцию `createActor(machine, { input })` и используя свойство `input` из первого аргумента в функции `context`:

```ts
import { setup, createActor } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as {
            feedback: string;
            rating: number;
        },
        // highlight-start
        input: {} as {
            defaultRating: number;
        },
        // highlight-end
    },
}).createMachine({
    // highlight-next-line
    context: ({ input }) => ({
        feedback: '',
        // highlight-next-line
        rating: input.defaultRating,
    }),
});

const feedbackActor = createActor(feedbackMachine, {
    // highlight-start
    input: {
        defaultRating: 5,
    },
    // highlight-end
}).start();

console.log(feedbackActor.getSnapshot().context.rating);
// выводит 5
```

Узнайте больше о [input](input.md).

## Обновление context с помощью `assign(...)`

Используйте действие `assign(...)` в переходе для обновления context:

```ts
import { createMachine, assign, createActor } from 'xstate';

const feedbackMachine = createMachine({
    context: {
        feedback: 'Некоторый отзыв',
    },
    on: {
        'feedback.update': {
            actions: assign({
                feedback: ({ event }) => event.feedback,
            }),
        },
    },
});

const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
    console.log(state.context.feedback);
});

feedbackActor.start();

// выводит 'Некоторый отзыв'

feedbackActor.send({
    type: 'feedback.update',
    feedback: 'Другой отзыв',
});

// выводит 'Другой отзыв'
```

## Context и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `context` вашего автомата в свойстве `types.context` настройки актора.

```ts
import { setup } from 'xstate';

const machine = setup({
    types: {} as {
        // highlight-start
        context: {
            feedback: string;
            rating: number;
        };
        // highlight-end
    },
}).createMachine({
    // Начальный context
    context: {
        feedback: '',
        rating: 5,
    },
    entry: ({ context }) => {
        context.feedback; // string
        context.rating; // number
    },
});
```

## Шпаргалка по context

Используйте нашу шпаргалку по context XState ниже для быстрого начала.

### Шпаргалка: начальный context

```ts
const machine = createMachine({
    context: {
        feedback: '',
    },
});
```

### Шпаргалка: ленивый начальный context

```ts
const machine = createMachine({
    context: () => ({
        feedback: '',
        createdAt: Date.now(),
    }),
});
```

### Шпаргалка: обновление context с помощью `assign(...)`

```ts
const machine = createMachine({
    context: {
        feedback: '',
    },
    on: {
        'feedback.update': {
            actions: assign({
                feedback: ({ event }) => event.feedback,
            }),
        },
    },
});
```

### Шпаргалка: input

```ts
import { setup, createActor } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as {
            feedback: string;
            rating: number;
        },
        // highlight-start
        input: {} as {
            defaultRating: number;
        },
        // highlight-end
    },
}).createMachine({
    // highlight-next-line
    context: ({ input }) => ({
        feedback: '',
        // highlight-next-line
        rating: input.defaultRating,
    }),
});

const feedbackActor = createActor(feedbackMachine, {
    // highlight-start
    input: {
        defaultRating: 5,
    },
    // highlight-end
}).start();
```
