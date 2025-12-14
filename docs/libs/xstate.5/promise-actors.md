---
title: Promise-акторы
---

Promise-акторы — это акторы, которые представляют промис, выполняющий некоторую асинхронную задачу. Они могут разрешиться с некоторым выходным значением или отклониться с ошибкой.

## Возможности Promise-акторов

|     | Возможность        | Примечания                                                                                                                 |
| --- | ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| ❌  | Получение событий  | Promise-акторы в настоящее время не получают события.                                                                      |
| ✅  | Отправка событий   | Promise-акторы могут отправлять события другим акторам, на которые у них есть ссылка, например, предоставленным в `input`. |
| ❌  | Порождение акторов | Promise-акторы в настоящее время не могут порождать новых акторов.                                                         |
| ✅  | Input              | Вы можете передавать `input` Promise-акторам.                                                                              |
| ✅  | Output             | Promise-акторы могут производить `output`, который является разрешённым значением промиса.                                 |

## Логика Promise-актора

Вы можете определить логику Promise-актора с помощью создателя логики актора `fromPromise(...)`, который принимает функцию, возвращающую промис, и возвращает логику актора, которую можно использовать для создания Promise-акторов.

```ts
import { fromPromise, createActor } from 'xstate';

async function getUser(id: string) {
    // ...
    return { id /* другие данные пользователя */ };
}

// highlight-start
const promiseLogic = fromPromise(async () => {
    const user = await getUser('123');

    return user;
});
// highlight-end

const promiseActor = createActor(promiseLogic);

promiseActor.subscribe((snapshot) => {
    console.log(snapshot.status, snapshot.output);
});

promiseActor.start();

// выводит 'active', undefined
// ... (через некоторое время)
// выводит 'done', { id: '123', /* другие данные пользователя */ }
```

## Входные данные Promise-актора

Вы можете передать `input` Promise-актору, передав его в функцию `createActor(...)` как свойство `input` второго аргумента. В логике промиса (`fromPromise(promiseFn)`) вы читаете свойство `input` первого аргумента, переданного в функцию промиса:

```ts
import { fromPromise, createActor } from 'xstate';

const promiseLogic = fromPromise(async ({ input }) => {
    const user = await getUser(input.id);

    return user;
});

const promiseActor = createActor(promiseLogic, {
    // highlight-next-line
    input: { id: '123' },
});
```

Тип `input` выводится из типа первого аргумента функции промиса. Вы также можете указать явный тип `input` во втором параметре обобщения:

```ts
import { fromPromise } from 'xstate';

interface User {
    name: string;
    id: string;
}

const secondLogic = fromPromise(
    async ({ input }: { input: { id: string } }) => {
        const user = await getUser(input.id); // User выводится автоматически

        return user;
    }
);

const firstLogic = fromPromise<User, { id: string }>(
    async ({ input, self /* ... */ }) => {
        const user = await getUser(input.id);

        return user;
    }
);
```

## Выходные данные Promise-актора

Чтобы получить окончательное разрешённое значение `output` Promise-актора, вы можете подписаться на Promise-актор и проверить свойство `status` снимка. Если `status` равен `'done'`, вы можете получить доступ к свойству `output` снимка для получения разрешённого значения. В противном случае `output` будет `undefined`.

```ts
import { fromPromise } from 'xstate';

const promiseLogic = fromPromise(async () => {
    const user = await getUser('123');

    return user;
});

const promiseActor = createActor(promiseLogic);

promiseActor.subscribe((snapshot) => {
    if (snapshot.status === 'done') {
        console.log(snapshot.output);
        // выводит { id: '123', /* другие данные пользователя */ }
    }
});
```

Вы также можете использовать `toPromise(...)` для преобразования любого актора, включая Promise-акторы, в промис. Это полезно, если вы хотите использовать `await` для `output` актора:

```ts
import { toPromise, createActor } from 'xstate';
import { somePromiseLogic } from './somePromiseLogic';

const promiseActor = createActor(somePromiseLogic);
promiseActor.start();

// highlight-next-line
const output = await toPromise(promiseActor);

console.log(output);
// выводит разрешённый output Promise-актора
```

## Обработка ошибок Promise-актора

Если в логике промиса происходит ошибка, Promise-актор отклонится с ошибкой. Вы можете подписаться на Promise-актор и проверить свойство `status` снимка в **наблюдателе ошибок** (свойство `error` объекта-наблюдателя).

```ts
import { fromPromise } from 'xstate';

const promiseLogic = fromPromise(async () => {
    // ...
    throw new Error('Что-то пошло не так');
});

const promiseActor = createActor(promiseLogic);
promiseActor.subscribe({
    // highlight-start
    error: (error) => {
        console.error(error);
        // выводит 'Error: Что-то пошло не так'
    },
    // highlight-end
});

promiseActor.start();
```

## Остановка Promise-акторов

Вы можете остановить Promise-актор, созданный с помощью `createActor(promiseLogic)`, вызвав `.stop()` на экземпляре актора. Это отбросит разрешённое или отклонённое значение промиса и удалит все подписки на Promise-актор.

Вы также можете **прервать** Promise-актор, передав ему `signal`:

```ts
import { fromPromise, createActor } from 'xstate';

const promiseLogic = fromPromise(
    async ({
        input,
        // highlight-next-line
        signal,
    }) => {
        // highlight-start
        // Передаём signal для прерывания fetch при получении сигнала
        const data = await fetch('/some/url', { signal });
        // highlight-end

        return data;
    }
);

const promiseActor = createActor(promiseLogic);
promiseActor.start();

// ...

// highlight-start
// Прерываем Promise-актор
promiseActor.stop();
// highlight-end
```
