---
title: 'Входные данные'
---

Input (входные данные) — это данные, предоставляемые конечному автомату, которые влияют на его поведение. В [XState](xstate.md) вы предоставляете input при создании [актора](actors.md), используя второй аргумент функции `createActor(machine, { input })`:

```ts
import { createActor, setup } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as {
            userId: string;
            feedback: string;
            rating: number;
        },
        // highlight-start
        input: {} as {
            userId: string;
            defaultRating: number;
        },
        // highlight-end
    },
}).createMachine({
    // highlight-next-line
    context: ({ input }) => ({
        // highlight-next-line
        userId: input.userId,
        feedback: '',
        // highlight-next-line
        rating: input.defaultRating,
    }),
    // ...
});

const feedbackActor = createActor(feedbackMachine, {
    // highlight-start
    input: {
        userId: '123',
        defaultRating: 5,
    },
    // highlight-end
});
```

## Создание акторов с input

Вы можете передать `input` любому виду актора, прочитав эти входные данные из свойства `input` первого аргумента создателей логики актора, таких как `fromPromise()`, `fromTransition()`, `fromObservable()` и других.

**Input с `fromPromise()`:**

```ts
import { createActor, fromPromise } from 'xstate';

const userFetcher = fromPromise(
    ({ input }: { input: { userId: string } }) => {
        return fetch(`/users/${input.userId}`).then((res) =>
            res.json()
        );
    }
);

const userFetcherActor = createActor(userFetcher, {
    // highlight-start
    input: {
        userId: '123',
    },
    // highlight-end
}).start();

userFetcherActor.onDone((data) => {
    console.log(data);
    // выводит данные пользователя для userId 123
});
```

**Input с `fromTransition()`:**

```ts
import { createActor, fromTransition } from 'xstate';

const counter = fromTransition((state, event)) => {
  if (event.type === 'INCREMENT') {
    return { count: state.count + 1 };
  }
  return state;
}, ({ input }: { input: { startingCount?: number } }) => ({
  count: input.startingCount ?? 0,
});

const counterActor = createActor(counter, {
  // highlight-start
  input: {
    startingCount: 10,
  }
});
```

**Input с `fromObservable()`:**

```ts
import { createActor, fromObservable } from 'xstate';
import { interval } from 'rxjs';

const intervalLogic = fromObservable(
    ({ input }: { input: { interval: number } }) => {
        return interval(input.interval);
    }
);

const intervalActor = createActor(intervalLogic, {
    // highlight-start
    input: {
        interval: 1000,
    },
    // highlight-end
});

intervalActor.start();
```

## Input в начальном событии

Когда актор запускается, он автоматически отправляет себе специальное событие с именем `xstate.init`. Если `input` предоставлен в функцию `createActor(logic, { input })`, он будет включён в событие `xstate.init`:

```ts
import { createActor, createMachine } from 'xstate';

const feedbackMachine = createMachine({
    // highlight-start
    entry: ({ event }) => {
        console.log(event.input);
        // выводит { userId: '123', defaultRating: 5 }
    },
    // highlight-end
    // ...
});

const feedbackActor = createActor(feedbackMachine, {
    input: {
        userId: '123',
        defaultRating: 5,
    },
}).start();
```

## Вызов акторов с input

Вы можете предоставить input вызванным акторам через свойство `input` конфигурации `invoke`:

```ts
import { createActor, setup } from 'xstate';

const feedbackMachine = setup({
    actors: {
        liveFeedback: fromPromise(
            ({ input }: { input: { domain: string } }) => {
                return fetch(
                    `https://${input.domain}/feedback`
                ).then((res) => res.json());
            }
        ),
    },
}).createMachine({
    invoke: {
        src: 'liveFeedback',
        // highlight-start
        input: {
            domain: 'stately.ai',
        },
        // highlight-end
    },
});
```

Свойство `invoke.input` может быть статическим входным значением или функцией, возвращающей входное значение. Функция будет вызвана с объектом, содержащим текущий `context` и `event`:

```ts
import { createActor, setup } from 'xstate';

const feedbackMachine = setup({
    actors: {
        // highlight-start
        fetchUser: fromPromise(({ input }) => {
            return fetch(
                `/users/${input.userId}`
            ).then((res) => res.json());
        }),
        // highlight-end
    },
}).createMachine({
    context: {
        userId: '',
        feedback: '',
        rating: 0,
    },
    invoke: {
        src: 'fetchUser',
        // highlight-next-line
        input: ({ context }) => ({
            userId: context.userId,
        }),
    },
    // ...
});
```

## Порождение акторов с input

Вы можете предоставить input порождённым акторам через свойство `input` конфигурации `spawn`:

```ts
import { createActor, setup, type AnyActorRef } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as {
            userId: string;
            feedback: string;
            rating: number;
            emailRef: AnyActorRef;
        },
    },
    actors: {
        // highlight-start
        emailUser: fromPromise(({ input }: { input: { userId: string } }) => {
            return fetch(`/users/${input.userId}`, {
                method: 'POST',
                // ...
            });
        }),
        // highlight-end
    },
}).createMachine({
    context: {
        userId: '',
        feedback: '',
        rating: 0,
        emailRef: null,
    },
    // ...
    on: {
        'feedback.submit': {
            actions: assign({
                emailRef: ({ context, spawn }) => {
                    return spawn('emailUser', {
                        // highlight-next-line
                        input: { userId: context.userId },
                    });
                },
            }),
        },
    },
    // ...
});
```

## Варианты использования

Input полезен для создания переиспользуемых автоматов, которые могут быть настроены с различными входными значениями.

-   Заменяет старый способ написания фабричной функции для автоматов:

```ts
// Старый способ: использование фабричной функции
const createFeedbackMachine = (userId, defaultRating) => {
    return createMachine({
        context: {
            userId,
            feedback: '',
            rating: defaultRating,
        },
        // ...
    });
};

const feedbackMachine1 = createFeedbackMachine('123', 5);

const feedbackActor1 = createActor(
    feedbackMachine1
).start();

// Новый способ: использование input
const feedbackMachine = createMachine({
    context: ({ input }) => ({
        userId: input.userId,
        feedback: '',
        rating: input.defaultRating,
    }),
    // ...
});

const feedbackActor = createActor(feedbackMachine, {
    input: {
        userId: '123',
        defaultRating: 5,
    },
});
```

### Передача новых данных актору

Изменение input не приведёт к перезапуску актора. Вам нужно отправить событие актору, чтобы передать новые данные:

```tsx
const Component = (props) => {
    const feedbackActor = useActor(feedbackMachine, {
        input: {
            userId: props.userId,
            defaultRating: props.defaultRating,
        },
    });

    useEffect(() => {
        feedbackActor.send({
            type: 'userId.change',
            userId: props.userId,
        });
    }, [props.userId]);

    // ...
};
```

## Input и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `input` вашего автомата в свойстве `types.input` настройки автомата.

```ts
import { createActor, setup } from 'xstate';

const machine = setup({
    types: {
        // highlight-start
        input: {} as {
            userId: string;
            defaultRating: number;
        };
        // highlight-end
        context: {} as {
            userId: string;
            feedback: string;
            rating: number;
        };
    },
}).createMachine({
    context: ({ input }) => ({
        userId: input.userId,
        feedback: '',
        rating: input.defaultRating,
    }),
});

const actor = createActor(machine, {
    input: {
        userId: '123',
        defaultRating: 5,
    },
});
```

## Шпаргалка по input

Используйте нашу шпаргалку по input XState ниже для быстрого начала.

### Шпаргалка: предоставление input

```ts
const feedbackActor = createActor(feedbackMachine, {
    input: {
        userId: '123',
        defaultRating: 5,
    },
});
```

### Шпаргалка: предоставление input вызванным акторам

```ts
const feedbackMachine = createMachine({
    invoke: {
        src: 'liveFeedback',
        input: {
            domain: 'stately.ai',
        },
    },
});
```

### Шпаргалка: предоставление динамического input вызванным акторам

```ts
const feedbackMachine = createMachine({
    context: {
        userId: 'some-user-id',
    },
    invoke: {
        src: 'fetchUser',
        input: ({ context }) => ({
            userId: context.userId,
        }),
    },
});
```

### Шпаргалка: предоставление динамического input из свойств события вызванным акторам

```ts
const feedbackMachine = createMachine({
    types: {
        events:
            | { type: 'messageSent'; message: string }
            | { type: 'incremented'; count: number },
    },
    invoke: {
        src: 'fetchUser',
        input: ({ event }) => {
            // highlight-next-line
            assertEvent(event, 'messageSent');
            return {
                message: event.message,
            };
        },
    },
});
```

### Шпаргалка: предоставление input порождённым акторам

```ts
const feedbackMachine = createMachine({
    context: {
        userId: '',
    },
    // ...
    on: {
        'feedback.submit': {
            actions: assign({
                emailRef: ({ context, spawn }) => {
                    return spawn('emailUser', {
                        input: { userId: context.userId },
                    });
                },
            }),
        },
    },
    // ...
});
```
