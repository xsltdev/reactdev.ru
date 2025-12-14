---
title: Callback-акторы
---

Callback-акторы — это акторы, логика которых представлена функцией, которая может «вызывать обратно» родительский актор, отправляя события (через `sendBack(...)`). Они также могут получать (`receive(...)`) события от других акторов.

## Возможности Callback-акторов

|     | Возможность        | Примечания                                                                                                                                                       |
| --- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅  | Получение событий  | Callback-акторы могут получать события через функцию `receive(event => {...})`.                                                                                  |
| ✅  | Отправка событий   | Callback-акторы могут отправлять события родителю через `sendBack(event)` или другим акторам, на которые у них есть ссылка, например, предоставленным в `input`. |
| ❌  | Порождение акторов | Callback-акторы в настоящее время не могут порождать новых акторов.                                                                                              |
| ✅  | Input              | Вы можете передавать `input` Callback-акторам.                                                                                                                   |
| ❌  | Output             | Callback-акторы в настоящее время не производят output — они активны бесконечно, пока не будут остановлены или не произойдёт ошибка.                             |

## Логика Callback-актора

Вы можете определить логику Callback-актора с помощью создателя логики актора `fromCallback(...)`, который принимает функцию колбэка и возвращает логику актора, которую можно использовать для создания Callback-акторов.

```ts
import {
    createActor,
    createMachine,
    fromCallback,
    sendTo,
    setup,
} from 'xstate';

const resizeLogic = fromCallback(
    ({ sendBack, receive }) => {
        const resizeHandler = (event) => {
            sendBack(event);
        };

        window.addEventListener('resize', resizeHandler);

        const removeListener = () => {
            window.removeEventListener(
                'resize',
                resizeHandler
            );
        };

        receive((event) => {
            if (event.type === 'stopListening') {
                console.log('Прекращаем прослушивание');
                removeListener();
            }
        });

        // Функция очистки
        return () => {
            console.log('Очистка');
            removeListener();
        };
    }
);

const machine = setup({
    actors: {
        resizeLogic,
    },
}).createMachine({
    invoke: {
        id: 'resize',
        src: 'resizeLogic',
    },
    on: {
        stop: {
            actions: sendTo('resize', {
                type: 'stopListening',
            }),
        },
    },
});

const actor = createActor(machine);
actor.start();

actor.send({ type: 'stop' });
// выводит "Прекращаем прослушивание" из callback-актора

actor.stop();
// выводит "Очистка" из callback-актора
```

## Входные данные Callback-актора

Вы можете передать `input` при создании Callback-акторов, который передаётся в логику Callback-актора в свойстве `input` первого аргумента.

```ts
import { fromCallback, createActor, setup, type EventObject } from 'xstate';

const resizeLogic = fromCallback<EventObject, { defaultSize: number }>(
    ({
        sendBack,
        receive,
        input, // Типизирован как { defaultSize: number }
    }) => {
        input.defaultSize; // 100
        // ...
    }
);

const machine = setup({
    actors: {
        resizeLogic,
    },
}).createMachine({
    // ...
    invoke: {
        src: 'resizeLogic',
        input: {
            defaultSize: 100,
        },
    },
});
```
