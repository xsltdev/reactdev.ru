---
title: Шпаргалка XState v5
---

Используйте эту шпаргалку, чтобы быстро найти синтаксис XState v5.

## Установка XState

=== "npm"

```bash
npm install xstate
```

=== "pnpm"

```bash
pnpm install xstate
```

=== "yarn"

```bash
yarn add xstate
```

[Подробнее об установке XState](xstate.md).

## Создание конечного автомата

```ts
import { setup, createActor, assign } from 'xstate';

const machine = setup({
    /* ... */
}).createMachine({
    id: 'toggle',
    initial: 'active',
    context: { count: 0 },
    states: {
        active: {
            entry: assign({
                count: ({ context }) => context.count + 1,
            }),
            on: {
                toggle: { target: 'inactive' },
            },
        },
        inactive: {
            on: {
                toggle: { target: 'active' },
            },
        },
    },
});

const actor = createActor(machine);
actor.subscribe((snapshot) => {
    console.log(snapshot.value);
});

actor.start();
// logs 'active' with context { count: 1 }

actor.send({ type: 'toggle' });
// logs 'inactive' with context { count: 1 }
actor.send({ type: 'toggle' });
// logs 'active' with context { count: 2 }
actor.send({ type: 'toggle' });
// logs 'inactive' with context { count: 2 }
```

[Подробнее о модели актера](actor-model.md).

## Создание логики обещаний

```ts
import { fromPromise, createActor } from 'xstate';

const promiseLogic = fromPromise(async () => {
    const response = await fetch(
        'https://dog.ceo/api/breeds/image/random'
    );
    const dog = await response.json();
    return dog;
});

const actor = createActor(promiseLogic);

actor.subscribe((snapshot) => {
    console.log(snapshot);
});

actor.start();
// logs: {
//   message: "https://images.dog.ceo/breeds/kuvasz/n02104029_110.jpg",
//   status: "success"
// }
```

[Подробнее о логике промиса](actors.md#frompromise).

## Создание логики перехода {#creating-transition-logic}

Функция перехода похожа на редуктор.

```ts
import { fromTransition, createActor } from 'xstate';

const transitionLogic = fromTransition(
    (state, event) => {
        switch (event.type) {
            case 'inc':
                return {
                    ...state,
                    count: state.count + 1,
                };
            default:
                return state;
        }
    },
    { count: 0 } // initial state
);

const actor = createActor(transitionLogic);

actor.subscribe((snapshot) => {
    console.log(snapshot);
});

actor.start();
// logs { count: 0 }

actor.send({ type: 'inc' });
// logs { count: 1 }
actor.send({ type: 'inc' });
// logs { count: 2 }
```

[Подробнее о transition-логике](actors.md#fromtransition).

## Создание наблюдаемой логики

```ts
import { fromObservable, createActor } from 'xstate';
import { interval } from 'rxjs';

const observableLogic = fromObservable(() =>
    interval(1000)
);

const actor = createActor(observableLogic);

actor.subscribe((snapshot) => {
    console.log(snapshot);
});

actor.start();
// logs 0, 1, 2, 3, 4, 5, ...
// every second
```

[Подробнее о наблюдаемых актерах](actors.md#fromobservable).

## Создание логики обратного вызова

```ts
import { fromCallback, createActor } from 'xstate';

const callbackLogic = fromCallback(
    ({ sendBack, receive }) => {
        const i = setTimeout(() => {
            sendBack({ type: 'timeout' });
        }, 1000);

        receive((event) => {
            if (event.type === 'cancel') {
                console.log('canceled');
                clearTimeout(i);
            }
        });

        return () => {
            clearTimeout(i);
        };
    }
);

const actor = createActor(callbackLogic);

actor.start();

actor.send({ type: 'cancel' });
// logs 'canceled'
```

[Подробнее об актерах обратного вызова](actors.md#fromcallback).

## Родительские состояния

```ts
import { setup, createActor } from 'xstate';

const machine = setup({
    /* ... */
}).createMachine({
    id: 'parent',
    initial: 'active',
    states: {
        active: {
            initial: 'one',
            states: {
                one: {
                    on: {
                        NEXT: { target: 'two' },
                    },
                },
                two: {},
            },
            on: {
                NEXT: { target: 'inactive' },
            },
        },
        inactive: {},
    },
});

const actor = createActor(machine);

actor.subscribe((snapshot) => {
    console.log(snapshot.value);
});

actor.start();
// logs { active: 'one' }

actor.send({ type: 'NEXT' });
// logs { active: 'two' }

actor.send({ type: 'NEXT' });
// logs 'inactive'
```

[Подробнее о родительских состояниях](parent-states.md).

## Действия

```ts
import { setup, createActor } from 'xstate';

const machine = setup({
    actions: {
        activate: () => {
            /* ... */
        },
        deactivate: () => {
            /* ... */
        },
        notify: (_, params: { message: string }) => {
            /* ... */
        },
    },
}).createMachine({
    id: 'toggle',
    initial: 'active',
    states: {
        active: {
            entry: { type: 'activate' },
            exit: { type: 'deactivate' },
            on: {
                toggle: {
                    target: 'inactive',
                    actions: [{ type: 'notify' }],
                },
            },
        },
        inactive: {
            on: {
                toggle: {
                    target: 'active',
                    actions: [
                        // action with params
                        {
                            type: 'notify',
                            params: {
                                message:
                                    'Some notification',
                            },
                        },
                    ],
                },
            },
        },
    },
});

const actor = createActor(
    machine.provide({
        actions: {
            notify: (_, params) => {
                console.log(
                    params.message ?? 'Default message'
                );
            },
            activate: () => {
                console.log('Activating');
            },
            deactivate: () => {
                console.log('Deactivating');
            },
        },
    })
);

actor.start();
// logs 'Activating'

actor.send({ type: 'toggle' });
// logs 'Deactivating'
// logs 'Default message'

actor.send({ type: 'toggle' });
// logs 'Some notification'
// logs 'Activating'
```

[Подробнее о действиях](actions.md).

## Условия (guards)

```ts
import { setup, createActor } from 'xstate';

const machine = setup({
    guards: {
        canBeToggled: ({ context }) => context.canActivate,
        isAfterTime: (_, params) => {
            const { time } = params;
            const [hour, minute] = time.split(':');
            const now = new Date();
            return (
                now.getHours() > hour &&
                now.getMinutes() > minute
            );
        },
    },
    actions: {
        notifyNotAllowed: () => {
            console.log('Cannot be toggled');
        },
    },
}).createMachine({
    id: 'toggle',
    initial: 'active',
    context: {
        canActivate: false,
    },
    states: {
        inactive: {
            on: {
                toggle: [
                    {
                        target: 'active',
                        guard: 'canBeToggled',
                    },
                    {
                        actions: 'notifyNotAllowed',
                    },
                ],
            },
        },
        active: {
            on: {
                toggle: {
                    // Guard with params
                    guard: {
                        type: 'isAfterTime',
                        params: { time: '16:00' },
                    },
                    target: 'inactive',
                },
            },
            // ...
        },
    },
});

const actor = createActor(machine);

actor.start();
// logs 'Cannot be toggled'
```

[Подробнее об условиях](guards.md).

## Вызов актеров

```ts
import {
    setup,
    fromPromise,
    createActor,
    assign,
} from 'xstate';

const loadUserLogic = fromPromise(async () => {
    const response = await fetch(
        'https://jsonplaceholder.typicode.com/users/1'
    );
    const user = await response.json();
    return user;
});

const machine = setup({
    actors: { loadUserLogic },
}).createMachine({
    id: 'toggle',
    initial: 'loading',
    context: {
        user: undefined,
    },
    states: {
        loading: {
            invoke: {
                id: 'loadUser',
                src: 'loadUserLogic',
                onDone: {
                    target: 'doSomethingWithUser',
                    actions: assign({
                        user: ({ event }) => event.output,
                    }),
                },
                onError: {
                    target: 'failure',
                    actions: ({ event }) => {
                        console.log(event.error);
                    },
                },
            },
        },
        doSomethingWithUser: {
            // ...
        },
        failure: {
            // ...
        },
    },
});

const actor = createActor(machine);

actor.subscribe((snapshot) => {
    console.log(snapshot.context.user);
});

actor.start();
// eventually logs:
// { id: 1, name: 'Leanne Graham', ... }
```

[Подробнее о вызове актеров](invoke.md).

## Порождение акторов

```ts
import {
    setup,
    fromPromise,
    createActor,
    assign,
} from 'xstate';

const loadUserLogic = fromPromise(async () => {
    const response = await fetch(
        'https://jsonplaceholder.typicode.com/users/1'
    );
    const user = await response.json();
    return user;
});

const machine = setup({
    actors: {
        loadUserLogic,
    },
}).createMachine({
    context: {
        userRef: undefined,
    },
    on: {
        loadUser: {
            actions: assign({
                userRef: ({ spawn }) =>
                    spawn('loadUserLogic'),
            }),
        },
    },
});

const actor = createActor(machine);
actor.subscribe((snapshot) => {
    const { userRef } = snapshot.context;
    console.log(userRef?.getSnapshot());
});
actor.start();

actor.send({ type: 'loadUser' });
// eventually logs:
// { id: 1, name: 'Leanne Graham', ... }
```

[Подробнее о порождении акторов](spawn.md).

## Input и output

```ts
import { setup, createActor } from 'xstate';

const greetMachine = setup({
    types: {
        context: {} as { message: string },
        input: {} as { name: string },
    },
}).createMachine({
    context: ({ input }) => ({
        message: `Hello, ${input.name}`,
    }),
    entry: ({ context }) => {
        console.log(context.message);
    },
});

const actor = createActor(greetMachine, {
    input: {
        name: 'David',
    },
});

actor.start();
// logs 'Hello, David'
```

[Подробнее о input](input.md).

## Вызов акторов с input

```ts
import { setup, createActor, fromPromise } from 'xstate';

const loadUserLogic = fromPromise(async ({ input }) => {
    const response = await fetch(
        `https://jsonplaceholder.typicode.com/users/${input.id}`
    );
    const user = await response.json();
    return user;
});

const machine = setup({
    actors: {
        loadUserLogic,
    },
}).createMachine({
    initial: 'loading user',
    states: {
        'loading user': {
            invoke: {
                id: 'loadUser',
                src: 'loadUserLogic',
                input: {
                    id: 3,
                },
                onDone: {
                    actions: ({ event }) => {
                        console.log(event.output);
                    },
                },
            },
        },
    },
});

const actor = createActor(machine);

actor.start();
// eventually logs:
// { id: 3, name: 'Clementine Bauch', ... }
```

[Подробнее о вызове акторов с input](input.md).

## Типы

```ts
import { setup, fromPromise } from 'xstate';

const promiseLogic = fromPromise(async () => {
  /* ... */
});

const machine = setup({
  types: {
    context: {} as {
      count: number;
    };
    events: {} as
      | { type: 'inc'; }
      | { type: 'dec' }
      | { type: 'incBy'; amount: number };
    actions: {} as
      | { type: 'notify'; params: { message: string } }
      | { type: 'handleChange' };
    guards: {} as
      | { type: 'canBeToggled' }
      | { type: 'isAfterTime'; params: { time: string } };
    children: {} as {
      promise1: 'someSrc';
      promise2: 'someSrc';
    };
    delays: 'shortTimeout' | 'longTimeout';
    tags: 'tag1' | 'tag2';
    input: number;
    output: string;
  },
  actors: {
    promiseLogic
  }
}).createMachine({
  // ...
});
```
