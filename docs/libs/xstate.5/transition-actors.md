---
title: Transition-акторы
---

Transition-акторы — это акторы, логика которых представлена **функцией перехода состояний**, которая возвращает **следующее состояние** актора на основе:

-   **Текущего состояния** актора
-   **События**, которое вызвало переход

Это очень похоже на _функцию-редьюсер_ в библиотеках вроде Redux.

## Возможности Transition-акторов

|     | Возможность        | Примечания                                                                                                                                                          |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅  | Получение событий  | Transition-акторы получают события для изменения своего состояния.                                                                                                  |
| ✅  | Отправка событий   | Transition-акторы могут отправлять события другим акторам, на которые у них есть ссылка, например, предоставленным в `input`. Обратите внимание, что это _нечисто_. |
| ❌  | Порождение акторов | Transition-акторы в настоящее время не могут порождать новых акторов.                                                                                               |
| ✅  | Input              | Вы можете передавать `input` Transition-акторам.                                                                                                                    |
| ❌  | Output             | Transition-акторы в настоящее время не производят output — они активны бесконечно, пока не будут остановлены или не произойдёт ошибка.                              |

## Логика Transition-актора

Вы можете определить логику Transition-актора с помощью создателя логики актора `fromTransition(...)`, который принимает два аргумента:

-   **Функцию перехода состояний**, которая возвращает следующее состояние актора
-   **Начальное состояние** для актора

Создатель логики актора возвращает логику актора, которую можно использовать для создания Transition-акторов.

```ts
import { fromTransition, createActor } from 'xstate';

const countLogic = fromTransition(
    (state, event) => {
        switch (event.type) {
            case 'increment': {
                return { count: state.count + 1 };
            }
            case 'decrement': {
                return { count: state.count - 1 };
            }
            default: {
                return state;
            }
        }
    },
    { count: 0 }
); // Начальное состояние

const countActor = createActor(countLogic);
countActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});
countActor.start();
// выводит { count: 0 }

countActor.send({ type: 'increment' });
// выводит { count: 1 }

countActor.send({ type: 'decrement' });
// выводит { count: 0 }
```

## Входные данные Transition-актора

Вы можете передать `input` в Transition-актор, который будет передан в функцию, определяющую начальное состояние.

```ts
import { fromTransition, createActor } from 'xstate';

const countLogic = fromTransition(
    (state, event) => {
        // ...
        // highlight-start
    },
    ({ input }: { input: number }) => ({
        count: input, // Начальное состояние
    })
);
// highlight-end

const countActor = createActor(countLogic, {
    // highlight-next-line
    input: 42,
});

countActor.subscribe((snapshot) => {
    console.log(snapshot.context);
    // выводит { count: 42 }
});

countActor.start();
```
