---
title: Observable-акторы
---

Observable-акторы — это акторы, которые представляют наблюдаемый поток значений. Это упрощает взаимодействие с библиотеками наблюдаемых объектов, такими как RxJS.

!!!tip "Совет"

    Все акторы XState являются наблюдаемыми.

## Возможности Observable-акторов

|     | Возможность        | Примечания                                                                                                                                        |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌  | Получение событий  | Observable-акторы в настоящее время не получают события.                                                                                          |
| ✅  | Отправка событий   | Observable-акторы могут отправлять события другим акторам, на которые у них есть ссылка, например, предоставленным в `input`.                     |
| ❌  | Порождение акторов | Observable-акторы в настоящее время не могут порождать новых акторов.                                                                             |
| ✅  | Input              | Вы можете передавать `input` Observable-акторам.                                                                                                  |
| ❌  | Output             | Observable-акторы в настоящее время не производят output — они активны бесконечно, пока не будут остановлены, завершены или не произойдёт ошибка. |

## Логика Observable-актора

Вы можете определить логику Observable-актора с помощью создателя логики актора `fromObservable(...)`, который принимает функцию, возвращающую observable, и возвращает логику актора, которую можно использовать для создания Observable-акторов.

```ts
import { fromObservable, createActor } from 'xstate';
import { interval } from 'rxjs';

// highlight-next-line
const intervalLogic = fromObservable(() => interval(1000));

const intervalActor = createActor(intervalLogic);
intervalActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});

intervalActor.start();
// выводит 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...
// каждую секунду
```

## Входные данные Observable-актора

Вы можете передать `input` Observable-актору, передав его в функцию `createActor(...)` как свойство `input` второго аргумента. В логике observable (`fromObservable(observableFn)`) вы читаете свойство `input` первого аргумента, переданного в функцию observable:

```ts
import { fromObservable, createActor } from 'xstate';
import { interval } from 'rxjs';

// highlight-next-line
const intervalLogic = fromObservable(({ input }) =>
    interval(input.interval)
);

const intervalActor = createActor(intervalLogic, {
    // highlight-next-line
    input: { interval: 10_000 },
});
intervalActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});

intervalActor.start();
// выводит 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...
// каждые 10 секунд
```
