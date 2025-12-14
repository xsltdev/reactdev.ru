---
title: 'Порождение акторов'
description: 'Вы можете использовать spawn для запуска акторов. Акторы, созданные с помощью spawn, являются порождёнными акторами, а акторы, созданные с помощью invoke — вызванными акторами.'
---

Иногда вызов [акторов](actors.md) может быть недостаточно гибким для ваших нужд. Например, вы можете захотеть:

-   Вызвать дочерние автоматы, которые существуют в _нескольких_ состояниях
-   Вызвать _динамическое количество_ акторов

Вы можете сделать это путём **порождения** актора вместо вызова. Акторы, созданные путём порождения, являются **порождёнными акторами**, а акторы, созданные с помощью invoke — **вызванными акторами**.

!!!tip "Совет"

    [Узнайте о разнице между порождением и вызовом акторов](actors.md#invoking-and-spawning-actors).

Есть два способа порождения: создатель действия `spawnChild` или вспомогательная функция `spawn` для `assign`.

В большинстве случаев предпочтительнее использовать `spawnChild`, который заставляет актора быть порождённым и может принимать настраиваемый ID для последующей ссылки на актора:

```ts
createMachine({
    entry: spawnChild(childMachine, {
        id: 'child',
    }),
});
```

Вы можете использовать `spawnChild` для нескольких порождённых акторов:

```ts
createMachine({
    entry: [
        spawnChild(childMachine, { id: 'child-1' }),
        spawnChild(childMachine, { id: 'child-2' }),
        spawnChild(childMachine, { id: 'child-3' }),
    ],
});
```

Вы также можете использовать вспомогательную функцию `spawn`, предоставляемую создателем действия `assign`, которая позволяет хранить ссылку на порождённого актора (`ActorRef`) в `context` автомата:

```ts
const parentMachine = createMachine({
    entry: [
        assign({
            childMachineRef: ({ spawn }) =>
                spawn(childMachine, { id: 'child' }),
        }),
    ],
});
```

Однако, если вы используете `spawn`, **убедитесь, что вы удаляете ActorRef из `context` для предотвращения утечек памяти**, когда порождённый актор больше не нужен:

```ts
actions: [
    stopChild('child'),
    assign({ childMachineRef: undefined }),
];
```

Вы можете порождать (`spawn`) столько акторов, сколько вам нужно:

```ts
const childMachine = createMachine({
    /* ... */
});

const parentMachine = createMachine({
    entry: [
        assign({
            childMachineRefs: ({ spawn }) => [
                // highlight-start
                spawn(childMachine),
                spawn(childMachine),
                spawn(childMachine),
                // highlight-end
            ],
        }),
    ],
});
```

Если вам не нужно отслеживать ссылку на порождённого актора (например, для анонимных порождённых акторов), вы можете использовать создатель действия `spawnChild`. Он _не_ возвращает ссылку, но указывает интерпретатору XState, что должен быть порождён новый актор:

```ts
createMachine({
    entry: spawnChild('workflow', {
        id: 'workflow',
    }),
});
```

## API

```ts
actions: assign({
  ref: ({ spawn }) => spawn(fromPromise(...), {
    id: 'some-id',
  })
})
```

-   `spawn(actorBehavior, options?)`
    -   `actorBehavior` - Поведение порождаемого актора. Это может быть функция, промис, observable или колбэк.
    -   `options` - Опции для порождения актора.
        -   `id` (необязательно) - ID актора. Используется для ссылки на актора в конечном автомате.
        -   `input` (необязательно) - Входные данные для передачи актору.
        -   `systemId` (необязательно) - Строка, идентифицирующая актора, уникальная в масштабе всей системы.

## Источник

-   Встроенный: `spawn(fromPromise(...))`
-   По ссылке: `spawn('getUser')`
    -   `.provide({ actors })`

## Жизненный цикл

-   Создаётся и запускается при порождении
-   Останавливается при остановке автомата
-   Может быть остановлен вручную

## Остановка актора

Вы можете остановить дочернего актора с помощью действия «stop child». Это действие создаётся из создателя действия `stopChild(id)`.

```ts
import { setup, stopChild, fromPromise } from 'xstate';

const machine = setup({
    actors: {
        something: fromPromise(async () => {
            // Некоторая логика актора
            return 'Некоторый ответ';
        }),
    },
}).createMachine({
    context: ({ spawn }) => ({
        something: spawn('something', { id: 'thing' }),
    }),
    // ...
    on: {
        'thing.stop': {
            // highlight-next-line
            actions: stopChild('thing'),
        },
        'thing.stopFromContext': {
            // highlight-next-line
            actions: stopChild(
                ({ context }) => context.something
            ),
        },
    },
});
```

Остановка дочернего актора _не_ удаляет его из `context`. Чтобы удалить его из context, используйте [создатель действия `assign(...)`](./context.md):

```ts
import { setup, stopChild } from 'xstate';

const machine = setup({
    // ...
}).createMachine({
    context: ({ spawn }) => ({
        something: spawn('something', { id: 'thing' }),
    }),
    // ...
    on: {
        'thing.stop': {
            actions: [
                stopChild('thing'),
                assign({ something: undefined }),
            ],
        },
    },
});
```

## Spawn и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

_Скоро будет_

## Шпаргалка по spawn

### Базовое порождение

```ts
// Порождение дочернего автомата
createMachine({
    entry: spawnChild(childMachine, {
        id: 'child',
    }),
});

// Порождение нескольких дочерних автоматов
createMachine({
    entry: [
        spawnChild(childMachine, { id: 'child-1' }),
        spawnChild(childMachine, { id: 'child-2' }),
    ],
});
```

### Порождение с Context

```ts
// Хранение ссылки на актора в context
createMachine({
    entry: assign({
        childRef: ({ spawn }) =>
            spawn(childMachine, { id: 'child' }),
    }),
});

// Порождение нескольких акторов в context
createMachine({
    entry: assign({
        childRefs: ({ spawn }) => [
            spawn(childMachine),
            spawn(childMachine),
        ],
    }),
});
```

### Порождение разных типов акторов

```ts
// Порождение из промиса
spawnChild(
    fromPromise(() => Promise.resolve(42)),
    {
        id: 'promiseActor',
    }
);

// Порождение из observable
spawnChild(
    fromObservable(() => interval(1000)),
    {
        id: 'observableActor',
    }
);

// Порождение из именованного актора
setup({
    actors: {
        fetchData: fromPromise(({ input }) =>
            Promise.resolve(input)
        ),
    },
}).createMachine({
    entry: spawnChild('fetchData', {
        id: 'fetchActor',
        input: 42,
    }),
});
```

### Опции порождения

```ts
spawnChild(actor, {
    id: 'actorId', // Обязательно для ссылки
    input: { data: 42 }, // Необязательные входные данные
    systemId: 'systemId', // Необязательный уникальный ID в системе
});
```

### Остановка порождённых акторов

```ts
// Остановка по ID
actions: stopChild('actorId');

// Остановка по ссылке из context
actions: stopChild(({ context }) => context.actorRef);

// Остановка и очистка context
actions: [
    stopChild('actorId'),
    assign({ actorRef: undefined }),
];
```

### Динамическое порождение

```ts
// Динамический ID на основе context
spawnChild(childMachine, {
    id: ({ context }) => context.childId,
});

// Порождение с динамическими входными данными
spawnChild(childMachine, {
    id: 'child',
    input: ({ context }) => context.inputData,
});
```

### Лучшие практики

1.  Всегда указывайте `id`, когда вам нужно ссылаться на актора позже
2.  Очищайте ссылки на акторов из context при их остановке
3.  Используйте `spawnChild` для одноразовых акторов, которым не нужны ссылки в context
4.  Используйте `spawn` с `assign`, когда вам нужно отслеживать ссылки на акторов
5.  Рассмотрите использование `systemId` для акторов, которые должны быть глобально уникальными
