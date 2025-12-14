---
title: Акторы конечных автоматов
---

Акторы конечных автоматов — это акторы, логика которых представлена конечным автоматом или диаграммой состояний.

!!!xstate "XState"

    Эта страница является лишь обзором использования конечных автоматов для представления логики актора. Прочитайте документацию по [конечным автоматам](./machines.md), чтобы изучить их подробнее.

## Возможности акторов конечных автоматов

|     | Возможность        | Примечания                                                                                             |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------ |
| ✅  | Получение событий  | Акторы конечных автоматов могут получать события напрямую (`actor.send(event)`) или от других акторов. |
| ✅  | Отправка событий   | Акторы конечных автоматов могут отправлять события другим акторам, на которые у них есть ссылка.       |
| ✅  | Порождение акторов | Акторы конечных автоматов могут порождать/вызывать акторов и иметь дочерних акторов.                   |
| ✅  | Input              | Вы можете передавать `input` акторам конечных автоматов.                                               |
| ✅  | Output             | Акторы конечных автоматов могут производить `output`.                                                  |

## Логика актора конечного автомата

Вы можете определить логику актора конечного автомата с помощью создателя логики актора `createMachine(...)`, который принимает объект конфигурации конечного автомата или диаграммы состояний в качестве единственного аргумента.

```ts
import { createMachine, createActor } from 'xstate';

const toggleMachine = createMachine({
    initial: 'inactive',
    states: {
        inactive: {
            on: {
                toggle: {
                    target: 'active',
                },
            },
        },
        active: {
            on: {
                toggle: {
                    target: 'inactive',
                },
            },
        },
    },
});

const toggleActor = createActor(toggleMachine);
toggleActor.subscribe((snapshot) => {
    console.log(snapshot.value); // 'inactive' или 'active'
});
toggleActor.start();
// выводит 'inactive'

toggleActor.send({ type: 'toggle' });
// выводит 'active'

toggleActor.send({ type: 'toggle' });
// выводит 'inactive'
```

## Входные данные актора конечного автомата

Вы можете передать `input` актору конечного автомата, передав его в функцию `createActor(...)` как свойство `input` второго аргумента. В конечном автомате (`setup(...).createMachine(...)`) вы читаете свойство `input` первого аргумента, переданного в функцию `context`:

```ts
import { setup, createActor } from 'xstate';

const feedbackMachine = setup({
    // ...
}).createMachine({
    context: ({ input }) => ({
        rating: input.defaultRating,
    }),
    initial: 'question',
    states: {
        question: {
            /* ... */
        },
        // ...
    },
});

const feedbackActor = createActor(feedbackMachine, {
    // highlight-start
    input: {
        defaultRating: 3,
    },
    // highlight-end
});

feedbackActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});

feedbackActor.start();
// выводит { rating: 3 }
```

## Выходные данные актора конечного автомата

Прочитайте [выходные данные конечного автомата](./output.md) для получения дополнительной информации.
