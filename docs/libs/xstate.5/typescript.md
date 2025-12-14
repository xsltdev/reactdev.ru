---
title: TypeScript
---

XState v5 и связанные с ним библиотеки написаны на [TypeScript](https://www.typescriptlang.org) и используют сложные типы для обеспечения максимальной типобезопасности и вывода типов.

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте **последнюю версию TypeScript**.

Следуйте этим рекомендациям, чтобы убедиться, что ваш TypeScript-проект готов к использованию XState v5:

## Используйте последнюю версию TypeScript

Используйте последнюю версию TypeScript; требуется версия 5.0 или выше.

```bash
npm install typescript@latest --save-dev
```

## Настройте ваш файл `tsconfig.json`

-   Установите [`strictNullChecks`](https://www.typescriptlang.org/tsconfig#strictNullChecks) в `true` в вашем файле `tsconfig.json`. Это обеспечит корректную работу наших типов и поможет отлавливать ошибки в вашем коде. **(Настоятельно рекомендуется)**.
-   Установите [`skipLibCheck`](https://www.typescriptlang.org/tsconfig#skipLibCheck) в `true` в вашем файле `tsconfig.json`. (Рекомендуется).

```js
// tsconfig.json
{
    compilerOptions: {
        // ...
        strictNullChecks: true,
        // или установите `strict` в true, что включает `strictNullChecks`
        // "strict": true,

        skipLibCheck: true,
    },
}
```

## Указание типов

Рекомендуемый способ строгой типизации вашей машины — использовать функцию `setup(...)`:

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

Вы также можете указать типы TypeScript внутри [конфигурации машины](machines.md), используя свойство `.types`:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    types: {} as {
        context: { feedback: string };
        events:
            | { type: 'feedback.good' }
            | { type: 'feedback.bad' };
        actions: { type: 'logTelemetry' };
    },
});
```

Эти типы будут выводиться по всей конфигурации машины, а также в созданной машине и акторе, так что методы, такие как `machine.transition(...)` и `actor.send(...)`, будут типобезопасными.

## Динамические параметры

Рекомендуется использовать динамические параметры в [действиях](./actions.md) и [защитах](./guards.md), так как они позволяют создавать переиспользуемые функции, которые не привязаны к машине и строго типизированы.

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as {
            user: { name: string };
        },
    },
    actions: {
        greet: (_, params: { name: string }) => {
            console.log(`Hello, ${params.name}!`);
        },
    },
}).createMachine({
    context: {
        user: {
            name: 'David',
        },
    },
    // ...
    entry: {
        type: 'greet',
        params: ({ context }) => ({
            name: context.user.name,
        }),
    },
});
```

## Утверждение событий

### Действия и защиты

!!!info "Информация"

    Настоятельно рекомендуется использовать динамические параметры вместо прямого доступа к объекту события, когда это возможно, для улучшения типобезопасности и переиспользуемости.

Если использование динамических параметров невозможно и вы должны использовать событие в реализации действия или защиты, вы можете утвердить тип события с помощью вспомогательной функции `assertEvent(...)`:

```ts
import { createMachine, assertEvent } from 'xstate';

const machine = createMachine({
    types: {
        events: {} as
            | { type: 'greet'; message: string }
            | { type: 'log'; message: string }
            | { type: 'doSomethingElse' },
    },
    // ...
    states: {
        someState: {
            entry: ({ event }) => {
                // В действии входа сейчас невозможно узнать,
                // с каким событием это действие было вызвано.

                // Вызов `assertEvent` выбросит исключение, если
                // событие не ожидаемого типа.
                assertEvent(event, 'greet');

                // Теперь мы знаем, что событие — это `greet`,
                // и можем получить доступ к его свойству `message`.
                console.log(event.message.toUpperCase());
            },
            // ...
            exit: ({ event }) => {
                // Вы также можете утвердить несколько возможных типов событий.
                assertEvent(event, ['greet', 'log']);

                // Теперь мы знаем, что событие — это `greet` или `log`,
                // и можем получить доступ к его свойству `message`.
                console.log(event.message.toUpperCase());
            },
        },
    },
});
```

### Входные данные вызванного актора

Другой случай, когда полезно использовать `assertEvent` — при указании `input` для вызванного актора. Полученное `event` может быть любым из событий, полученных этим актором. Чтобы TypeScript распознал тип события и его свойства, вы можете использовать `assertEvent` для сужения типа события.

```ts
import { createMachine, assertEvent } from 'xstate';

const machine = createMachine({
    types: {
        events: {} as
            | { type: 'messageSent'; message: string }
            | { type: 'incremented'; count: number },
    },
    actors: {
        someActor: fromPromise<void, { message: string }>(
            ({ input }) => {
                // реализация актора
            }
        ),
    },
    // ...
    states: {
        someState: {
            invoke: {
                src: 'someActor',
                input: ({ event }) => {
                    assertEvent(event, 'messageSent');

                    return { message: event.message };
                },
            },
        },
    },
});
```

## Вспомогательные типы

XState предоставляет некоторые вспомогательные типы для упрощения работы с типами в TypeScript.

### `ActorRefFrom<T>`

Возвращает `ActorRef` из предоставленного параметра логики актора `T`, что полезно для создания строго типизированных акторов. Параметр `T` может быть любой `ActorLogic`, такой как возвращаемое значение `createMachine(…)`, или любой другой логикой актора, такой как `fromPromise(…)` или `fromObservable(…)`.

```ts
import { type ActorRefFrom } from 'xstate';
import { someMachine } from './someMachine';

type SomeActorRef = ActorRefFrom<typeof someMachine>;
```

### `SnapshotFrom<T>`

Возвращает `Snapshot` из предоставленного параметра `T`, что полезно для создания строго типизированных снимков. Параметр `T` может быть любой `ActorLogic` или `ActorRef`.

```ts
import { type SnapshotFrom } from 'xstate';
import { someMachine } from './someMachine';

type SomeSnapshot = SnapshotFrom<typeof someMachine>;
```

### `EventFromLogic<T>`

Возвращает объединение всех типов событий, определённых в предоставленном параметре логики актора `T`. Полезно для типобезопасной обработки событий.

```ts
import { type EventFromLogic } from 'xstate';
import { someMachine } from './someMachine';

// SomeEvent будет объединением всех типов событий,
// определённых в `someMachine`.
type SomeEvent = EventFromLogic<typeof someMachine>;
```
