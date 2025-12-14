---
title: 'Вызов акторов'
---

[Конечные автоматы](machines.md) могут «вызывать» одного или нескольких [акторов](actors.md) в заданном состоянии. Вызванный актор запускается при входе в состояние и останавливается при выходе из него. Можно вызвать любой актор XState, включая простых Promise-акторов или даже сложных акторов на основе автоматов.

Вызов актора полезен для управления синхронной или асинхронной работой, которую конечный автомат должен оркестрировать и с которой взаимодействовать на высоком уровне, но не нуждается в детальном знании о ней.

!!!tip "Совет"

    [Узнайте о разнице между вызовом и порождением акторов](actors.md#invoking-and-spawning-actors).

<iframe loading="lazy" src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?machineId=7f8f7dfb-f9a0-4e37-9c2a-bbca9f093d21&amp;mode=design&amp;colorMode=light" class="embed_rxbU" width="100%" height="500"></iframe>

Акторы могут быть вызваны в любом состоянии, _кроме_ [финального состояния верхнего уровня](final-states.md). В следующем примере состояние `loading` вызывает Promise-актор:

```ts
import {
    setup,
    createActor,
    fromPromise,
    assign,
} from 'xstate';

const fetchUser = (userId: string) =>
    fetch(
        `https://example.com/${userId}`
    ).then((response) => response.text());

const userMachine = setup({
    types: {
        context: {} as {
            userId: string;
            user: object | undefined;
            error: unknown;
        },
    },
    actors: {
        fetchUser: fromPromise(
            async ({
                input,
            }: {
                input: { userId: string };
            }) => {
                const user = await fetchUser(input.userId);

                return user;
            }
        ),
    },
}).createMachine({
    id: 'user',
    initial: 'idle',
    context: {
        userId: '42',
        user: undefined,
        error: undefined,
    },
    states: {
        idle: {
            on: {
                FETCH: { target: 'loading' },
            },
        },
        loading: {
            // highlight-start
            invoke: {
                id: 'getUser',
                src: 'fetchUser',
                input: ({ context: { userId } }) => ({
                    userId,
                }),
                onDone: {
                    target: 'success',
                    actions: assign({
                        user: ({ event }) => event.output,
                    }),
                },
                onError: {
                    target: 'failure',
                    actions: assign({
                        error: ({ event }) => event.error,
                    }),
                },
            },
            // highlight-end
        },
        success: {},
        failure: {
            on: {
                RETRY: { target: 'loading' },
            },
        },
    },
});
```

Акторы также могут быть вызваны в _корне_ автомата, и они будут активны в течение всего времени жизни родительского актора автомата:

```ts
import { fromEvent } from 'rxjs';
import { fromEventObservable } from 'xstate';
const interactiveMachine = createMachine({
    // highlight-start
    invoke: {
        src: fromEventObservable(
            () =>
                fromEvent(
                    document.body,
                    'click'
                ) as Subscribable<EventObject>
        ),
    },
    // highlight-end
    on: {
        click: {
            actions: ({ event }) => console.log(event),
        },
    },
});
```

И `invoke` может быть массивом для вызова [нескольких акторов](#multiple-actors):

```ts
const vitalsWorkflow = createMachine({
    states: {
        CheckVitals: {
            // highlight-start
            invoke: [
                { src: 'checkTirePressure' },
                { src: 'checkOilPressure' },
                { src: 'checkCoolantLevel' },
                { src: 'checkBattery' },
            ],
            // highlight-end
        },
    },
});
```

Дополнительные примеры:

-   [Рабочий процесс с повторным использованием функций и определений событий](https://github.com/statelyai/xstate/tree/main/examples/workflow-reusing-functions/main.ts)
-   [Периодическая проверка почтового ящика (cron-рабочий процесс)](https://github.com/statelyai/xstate/tree/main/examples/workflow-check-inbox/main.ts)
-   [Проверка показателей автомобиля (SubFlow Repeat) рабочий процесс](https://github.com/statelyai/xstate/tree/main/examples/workflow-car-vitals)

## Чем акторы отличаются от действий?

Действия выполняются по принципу «запустил и забыл»; как только их выполнение начинается, конечный автомат, выполняющий действия, забывает о них. Если вы укажете действие как `async`, **действие не будет ожидаться перед переходом в следующее состояние**. Помните: переходы всегда _мгновенны_ (состояния переходят синхронно).

Вызванные акторы могут выполнять асинхронную работу _и_ взаимодействовать со своим родительским актором автомата. Они могут отправлять и получать события. Вызванные акторы автоматов могут даже вызывать или порождать собственных дочерних акторов.

В отличие от действий, ошибки, выбрасываемые вызванными акторами, могут быть обработаны напрямую:

```ts
invoke: {
  src: 'fetchUser',
  // highlight-start
  onError: {
    target: 'failure',
    actions: assign({ error: ({ event }) => event.error })
  }
  // highlight-end
}
```

В то время как ошибки, выбрасываемые действиями, могут быть обработаны только глобально подписчиком их родительского конечного автомата:

```ts
actor.subscribe({
    error: (err) => {
        console.error(err);
    },
});
```

## Жизненный цикл

Вызванные акторы имеют жизненный цикл, управляемый состоянием, в котором они вызваны. Они создаются и запускаются при входе в состояние и останавливаются при выходе из него.

Если в состояние входят и сразу же выходят из него, например, из-за безусловного («always») перехода, то в этом состоянии акторы не будут вызваны.

### Повторный вход

По умолчанию, когда конечный автомат переходит из родительского состояния в то же родительское состояние или в потомка (дочернее или глубже), он _не_ повторно входит в родительское состояние. Поскольку переход не является повторным входом, существующие вызванные акторы родительского состояния _не_ будут остановлены, и новые вызванные акторы _не_ будут запущены.

Однако, если вы хотите, чтобы переход повторно вошёл в родительское состояние, установите свойство `reenter` перехода в `true`. Переходы, которые повторно входят в состояние, _будут_ останавливать существующих вызванных акторов и запускать новых.

[Подробнее о повторном входе в состояния](transitions.md#re-entering).

## API свойства `invoke` {#api}

Вызов определяется в конфигурации узла состояния с помощью свойства `invoke`, значение которого является объектом, содержащим:

-   `src` - Источник [логики актора](actors.md#actor-logic) для вызова при создании актора, или строка, ссылающаяся на логику актора, определённую в [предоставленной реализации](machines.md#providing-implementations) автомата.
-   `id` - Строка, идентифицирующая актор, уникальная в пределах родительского автомата.
-   `input` - Входные данные для передачи актору.
-   `onDone` - Переход, который происходит при завершении актора.
-   `onError` - Переход, который происходит при выбросе ошибки актором.
-   `onSnapshot` - Переход, который происходит при генерации актором нового значения.
-   `systemId` - Строка, идентифицирующая актор, уникальная в масштабе всей системы.

### Источник {#src}

`src` представляет [логику актора](actors.md#actor-logic-creators), которую автомат должен использовать при создании актора. В XState доступно несколько создателей логики актора:

-   [Логика конечного автомата (`createMachine`)](actors.md#createmachine)
-   [Логика промиса (`fromPromise`)](actors.md#frompromise), где invoke выполнит переход `onDone` при `resolve` или переход `onError` при `reject`
-   [Логика функции перехода (`fromTransition`)](actors.md#fromtransition), которая следует паттерну редьюсера
-   [Логика Observable (`fromObservable`)](actors.md#fromobservable), которая может отправлять события родительскому автомату, и где invoke выполнит переход `onDone` при завершении
-   [Логика Event Observable (`fromEventObservable`)](actors.md#fromeventobservable), как логика Observable, но для потоков объектов событий
-   [Логика колбэка (`fromCallback`)](actors.md#fromcallback), которая может отправлять события родительскому автомату и получать от него

`src` вызова может быть _встроенным_ или _предоставленным_.

#### Встроенный `src`

Либо напрямую встроенный:

```ts
invoke: {
  src: fromPromise(…)
}
```

Либо из некоторой логики в той же области видимости, что и автомат:

```ts
const logic = fromPromise(…)
const machine = createMachine({
  // …
  invoke: {
    src: logic
  }
});
```

#### Предоставленный `src`

`src` может быть [предоставлен в реализации автомата](machines.md#providing-implementations) и указан с помощью строки или объекта.

```ts
const machine = createMachine({
    // …
    invoke: {
        src: 'workflow', // строковая ссылка
    },
});

const actor = createActor(
    machine.provide({
        actors: {
            workflow: fromPromise(/* ... */), // предоставлено
        },
    })
);
```

### `onDone`

-   Переход при завершении вызванного актора
-   Свойство `output` объекта события предоставляется с выходными данными актора
-   Недоступно для callback-акторов

!!!warning "Внимание"

    Не путайте свойство `onDone` состояния с `invoke.onDone` — это похожие переходы, но они относятся к разным вещам.

    -   Свойство `onDone` на узле [состояния](states.md) относится к достижению составным узлом состояния [финального состояния](final-states.md).
    -   Свойство `invoke.onDone` относится к завершению вызова (`invoke.src`).

    ```js
    // ...
    loading: {
      invoke: {
        src: someSrc,
        // относится к завершению `someSrc`
        // highlight-next-line
        onDone: {/* ... */}
      },
      initial: 'loadFoo',
      states: {
        loadFoo: {/* ... */},
        loadBar: {/* ... */},
        loadingComplete: { type: 'final' }
      },
      // относится к достижению 'loading.loadingComplete'
      // highlight-next-line
      onDone: { target: 'loaded' }
    }
    // ...
    ```

Переход `onDone` может быть объектом:

```ts
{
  invoke: {
    src: 'fetchItem',
    // highlight-start
    onDone: {
      target: 'success',
      actions: ({ event }) => {
        console.log(event.output);
      }
    }
    // highlight-end
  }
}
```

Или, для простоты, переходы только с целью могут быть строками:

```ts
{
  invoke: {
    src: 'fetchItem',
    // highlight-start
    onDone: 'success',
    // highlight-end
  }
}
```

### `onError`

-   Переход при выбросе ошибки вызванным актором, или (для Promise-акторов) при отклонении промиса
-   Свойство `error` объекта события предоставляется с данными ошибки актора

Переход `onError` может быть объектом:

```ts
invoke: {
  src: 'getUser',
  // highlight-start
  onError: {
    target: 'failure',
    actions: ({ event }) => {
      console.error(event.error);
    }
  }
  // highlight-end
}
```

Или, для простоты, переходы только с целью могут быть строками:

```ts
{
  invoke: {
    src: 'getUser',
    // highlight-start
    onError: 'failure'
    // highlight-end
  }
}
```

### `onSnapshot`

-   Переход при генерации вызванным актором нового снимка
-   Событие получает `snapshot` со снимком актора
-   Недоступно для callback-акторов

```ts
invoke: {
  src: 'getUser',
  // highlight-start
  onSnapshot: {
    actions: ({ event }) => console.log(event.snapshot)
  }
  // highlight-end
}
```

[Подробнее о снимках актора](actors.md#actor-snapshots).

### Входные данные

Для определения входных данных вызванного актора используйте `input`.

Свойство `input` может быть статическим входным значением или функцией, возвращающей входное значение. Функция получит объект, содержащий текущий `context` и `event`.

!!!tip "Совет"

    За кулисами input передаётся актору через событие:
    `{ type: 'xstate.init', input: ... }`.

#### Входные данные из статического значения

```ts
invoke: {
  src: 'liveFeedback',
  // highlight-start
  input: {
    domain: 'stately.ai'
  }
  // highlight-end
}
```

#### Входные данные из функции

```ts
invoke: {
  src: fromPromise(({ input: { endpoint, userId } }) => {
    return fetch(`${endpoint}/${userId}`).then((res) => res.json());
  }),
  // highlight-start
  input: ({ context, event }) => ({
    endpoint: context.endpoint,
    userId: event.userId
  })
  // highlight-end
}
```

См. [Входные данные](input.md) для подробностей.

## Вызов промисов

Наиболее распространённый тип акторов, которые вы будете вызывать — это promise-акторы. Promise-акторы позволяют дождаться результата промиса, прежде чем решать, что делать дальше.

XState может вызывать промисы как акторов с помощью создателя логики актора `fromPromise`. Промисы могут:

-   `resolve()`, что выполнит переход `onDone`
-   `reject()` (или выбросить ошибку), что выполнит переход `onError`

Если состояние, в котором активен вызванный промис, покидается до завершения промиса, результат промиса отбрасывается.

```ts
import {
    setup,
    createActor,
    fromPromise,
    assign,
} from 'xstate';

// Функция, возвращающая промис,
// который разрешается с полезным значением
// например: { name: 'David', location: 'Florida' }
const fetchUser = (userId: string) =>
    fetch(`/api/users/${userId}`).then((response) =>
        response.json()
    );

const userMachine = setup({
    types: {
        context: {} as {
            userId: string;
            user: object | undefined;
            error: unknown;
        },
    },
}).createMachine({
    id: 'user',
    initial: 'idle',
    context: {
        userId: '42',
        user: undefined,
        error: undefined,
    },
    states: {
        idle: {
            on: {
                FETCH: { target: 'loading' },
            },
        },
        loading: {
            // highlight-start
            invoke: {
                id: 'getUser',
                src: fromPromise(({ input }) =>
                    fetchUser(input.userId)
                ),
                input: ({ context: { userId } }) => ({
                    userId,
                }),
                onDone: {
                    target: 'success',
                    actions: assign({
                        user: ({ event }) => event.output,
                    }),
                },
                onError: {
                    target: 'failure',
                    actions: assign({
                        error: ({ event }) => event.error,
                    }),
                },
            },
            // highlight-end
        },
        success: {},
        failure: {
            on: {
                RETRY: { target: 'loading' },
            },
        },
    },
});
```

Разрешённый вывод помещается в событие `'xstate.done.actor.<id>'` в свойстве `output`, например:

```js
{
  type: 'xstate.done.actor.getUser',
  output: {
    name: 'David',
    location: 'Florida'
  }
}
```

### Отклонение промиса

Если промис отклоняется, будет выполнен переход `onError` с событием `{ type: 'xstate.error.actor.<id>' }`. Данные ошибки доступны в свойстве `error` события:

```ts
import {
    setup,
    createActor,
    fromPromise,
    assign,
} from 'xstate';

const search = (query: string) =>
    new Promise((resolve, reject) => {
        if (!query.length) {
            return reject('Запрос не указан');
            // или:
            // throw new Error('Запрос не указан');
        }

        return resolve(getSearchResults(query));
    });

// ...
const searchMachine = setup({
    types: {
        context: {} as {
            results: object | undefined;
            errorMessage: unknown;
        },
    },
}).createMachine({
    id: 'search',
    initial: 'idle',
    context: {
        results: undefined,
        errorMessage: undefined,
    },
    states: {
        idle: {
            on: {
                SEARCH: { target: 'searching' },
            },
        },
        searching: {
            // highlight-start
            invoke: {
                id: 'search',
                src: fromPromise(({ input: { query } }) =>
                    search(query)
                ),
                input: ({ event }) => ({
                    query: event.query,
                }),
                onError: {
                    target: 'failure',
                    actions: assign({
                        errorMessage: ({
                            context,
                            event,
                        }) => {
                            // event это:
                            // { type: 'xstate.error.actor.<id>', error: 'Запрос не указан' }
                            return event.error;
                        },
                    }),
                },
                onDone: {
                    target: 'success',
                    actions: assign({
                        results: ({ event }) =>
                            event.output,
                    }),
                },
            },
            // highlight-end
        },
        success: {},
        failure: {},
    },
});
```

Если переход `onError` отсутствует и промис отклонён, ошибка будет выброшена. Однако вы можете обработать все выброшенные ошибки актора, подписавшись с объектом-наблюдателем с функцией `error`:

```ts
actor.subscribe({
  error: (err) => { ... }
})
```

## Вызов колбэков

Вы можете вызвать [логику callback-актора](./callback-actors.md) следующим образом:

1.  Настройте логику callback-актора в объекте `actors` вызова `setup({ actors: { ... } })`
2.  Вызовите логику callback-актора по имени источника (`src`) в свойстве `invoke` состояния

```ts
import { setup, fromCallback } from 'xstate';

const machine = setup({
    actors: {
        // highlight-start
        someCallback: fromCallback(
            ({ input, sendBack, receive }) => {
                // ...
            }
        ),
        // highlight-end
    },
}).createMachine({
    // ...
    // highlight-start
    invoke: {
        src: 'someCallback',
        input: {
            /* ... */
        },
    },
    // highlight-end
});
```

Читайте [логика callback-актора](./callback-actors.md) для получения дополнительной информации о callback-акторах.

## Вызов Observable

Вы можете вызвать [логику observable](./observable-actors.md) следующим образом:

1.  Настройте логику observable в объекте `actors` вызова `setup({ actors: { ... } })`
2.  Вызовите логику observable по имени источника (`src`) в свойстве `invoke` состояния

```ts
import { setup, fromObservable } from 'xstate';
import { interval } from 'rxjs';

const machine = setup({
    actors: {
        // highlight-start
        someObservable: fromObservable(
            ({ input }: { input: number }) => {
                return interval(input.ms);
            }
        ),
        // highlight-end
    },
}).createMachine({
    // ...
    // highlight-start
    invoke: {
        src: 'someObservable',
        input: { ms: 1000 },
        onSnapshot: {
            actions: ({ event }) => {
                console.log(event.snapshot.context); // 1, 2, 3, ...
            },
        },
    },
    // highlight-end
});
```

Читайте [логика observable-актора](./observable-actors.md) для получения дополнительной информации об observable-акторах.

## Вызов Event Observable

Вы можете вызвать Event Observable с помощью создателя логики актора `fromEventObservable(...)`. Логика event observable похожа на логику observable в том, что родительский актор подписывается на event observable; однако генерируемые значения event observable ожидаются как события, которые _отправляются_ вызывающему (родительскому) актору напрямую.

```ts
import { setup, fromEventObservable } from 'xstate';

const mouseClicks = fromEventObservable(/* ... */);

const machine = setup({
    actors: {
        mouseClicks,
    },
}).createMachine({
    // ...
    invoke: {
        src: 'mouseClicks',
        // Не нужны `onSnapshot` или `onDone`; события отправляются напрямую
        // актору автомата
    },
    on: {
        // Отправлено event observable актором
        click: {
            // ...
        },
    },
});
```

## Вызов переходов

Вы можете вызвать [логику transition-актора](./transition-actors.md) следующим образом:

1.  Настройте логику transition-актора в объекте `actors` вызова `setup({ actors: { ... } })`
2.  Вызовите логику transition-актора по имени источника (`src`) в свойстве `invoke` состояния

```ts
import { setup, fromTransition } from 'xstate';

const machine = setup({
    actors: {
        // highlight-start
        someTransition: fromTransition(
            (state, event, { input }) => {
                // ...
                return state;
            }
        ),
        // highlight-end
    },
}).createMachine({
    // ...
    // highlight-start
    invoke: {
        src: 'someTransition',
        input: {
            /* ... */
        },
        onSnapshot: {
            actions: ({ event }) => {
                console.log(event.context);
            },
        },
    },
    // highlight-end
});
```

Читайте [логика transition-актора](./transition-actors.md) для получения дополнительной информации о transition-акторах.

## Вызов автоматов

Вы можете вызвать [логику актора конечного автомата](./state-machine-actors.md) следующим образом:

1.  Настройте логику актора конечного автомата в объекте `actors` вызова `setup({ actors: { ... } })`
2.  Вызовите логику актора конечного автомата по имени источника (`src`) в свойстве `invoke` состояния

```ts
import { setup } from 'xstate';

const childMachine = setup({
    /* ... */
}).createMachine({
    context: ({ input }) => ({
        // ...
    }),
    // ...
});

const machine = setup({
    actors: {
        // highlight-start
        someMachine: childMachine,
        // highlight-end
    },
}).createMachine({
    // ...
    // highlight-start
    invoke: {
        src: 'someMachine',
        input: {
            /* ... */
        },
    },
    // highlight-end
});
```

Читайте [логика актора конечного автомата](./state-machine-actors.md) для получения дополнительной информации об акторах конечных автоматов.

## Отправка ответов

Вызванный актор (или [порождённый актор](./spawn.md)) может _отвечать_ другому актору; т.е. он может отправить событие _в ответ на_ событие, отправленное другим актором. Для этого предоставьте ссылку на отправляющего актора как пользовательское свойство объекта отправляемого события. В следующем примере мы используем `event.sender`, но подойдёт любое имя.

```js
// Родитель
actions: sendTo('childActor', ({ self }) => ({
    type: 'ping',
    // highlight-next-line
    sender: self,
}));

// Дочерний
actions: sendTo(
    // highlight-next-line
    ({ event }) => event.sender,
    { type: 'pong' }
);
```

В следующем примере автомат `'client'` отправляет событие `'CODE'` вызванному актору `'auth-server'`, который затем отвечает событием `'TOKEN'` через 1 секунду.

```js
import { createActor, createMachine, sendTo } from 'xstate';

const authServerMachine = createMachine({
    id: 'server',
    initial: 'waitingForCode',
    states: {
        waitingForCode: {
            on: {
                CODE: {
                    // highlight-start
                    actions: sendTo(
                        ({ event }) => event.sender,
                        { type: 'TOKEN' },
                        { delay: 1000 }
                    ),
                    // highlight-end
                },
            },
        },
    },
});

const authClientMachine = createMachine({
    id: 'client',
    initial: 'idle',
    states: {
        idle: {
            on: {
                AUTH: { target: 'authorizing' },
            },
        },
        authorizing: {
            invoke: {
                id: 'auth-server',
                src: authServerMachine,
            },
            // highlight-start
            entry: sendTo('auth-server', ({ self }) => ({
                type: 'CODE',
                sender: self,
            })),
            // highlight-end
            on: {
                TOKEN: { target: 'authorized' },
            },
        },
        authorized: {
            type: 'final',
        },
    },
});
```

Обратите внимание, что по умолчанию `sendTo` отправляет события анонимно, в этом случае получатель не будет знать источник события.

!!!note "Примечание"

    В XState v4 для этой цели использовался создатель действия `respond(...)`. В XState v5 вместо этого используйте `sendTo(...)`.

## Несколько акторов {#multiple-actors}

Вы можете вызвать несколько акторов, указав каждого в массиве:

```ts
invoke: [
    { id: 'actor1', src: 'someActor' },
    { id: 'actor2', src: 'someActor' },
    { id: 'logActor', src: 'logActor' },
];
```

Каждый вызов создаст новый экземпляр этого актора, поэтому даже если `src` нескольких акторов одинаков (например, `someActor` выше), будет вызвано несколько экземпляров `someActor`.

## Тестирование

Вы можете тестировать вызванных акторов, проверяя, что родительский актор получает ожидаемые события от вызванного актора.

```ts
const machine = setup({
    actors: {
        countLogic,
    },
}).createMachine({
    invoke: {
        src: 'countLogic',
    },
});
```

## Ссылки на вызванных акторов

Акторы могут быть прочитаны из `snapshot.children.<actorId>`. Возвращаемое значение — объект `ActorRef` со свойствами:

-   `id` - ID актора
-   `send()`
-   `getSnapshot()`

```ts
actor.subscribe({
    next(snapshot) {
        console.log(Object.keys(snapshot.children));
    },
});
```

`snapshot.children` — это объект ключ-значение, где ключи — это ID актора, а значения — это `ActorRef`.

## Invoke и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы должны использовать API `setup({ ... })` для правильного вывода типов для логики вызываемого актора.

```ts
import { setup, fromPromise, assign } from 'xstate';

interface User {
    id: string;
    name: string;
}

const machine = setup({
    actors: {
        // highlight-start
        fetchUser: fromPromise<User, { userId: string }>(
            async ({ input }) => {
                const response = await fetch(
                    `https://example.com/${input.userId}`
                );

                return response.json();
            }
        ),
        // highlight-end
    },
}).createMachine({
    // ...
    context: {
        user: null,
        userId: 42,
    },
    initial: 'idle',
    states: {
        idle: {
            on: {
                editUserDetails: { target: 'loadingUser' },
            },
        },
        loadingUser: {
            invoke: {
                // highlight-start
                src: 'fetchUser',
                input: ({ context }) => ({
                    userId: context.userId, // Тип строго определён как string
                }),
                onDone: {
                    actions: assign({
                        user: ({ event }) => event.output, // Строго типизирован как User
                    }),
                },
                // highlight-end
            },
        },
    },
});
```

Читайте документацию по [настройке конечных автоматов](./setup.md) для получения дополнительной информации.

## Шпаргалка по invoke

### Шпаргалка: вызов актора

```ts
import {
    setup,
    createActor,
    fromPromise,
    assign,
} from 'xstate';

const fetchUser = (userId: string) =>
    fetch(
        `https://example.com/${userId}`
    ).then((response) => response.text());

const userMachine = setup({
    actors: {
        getUser: fromPromise(
            async ({
                input,
            }: {
                input: { userId: string };
            }) => {
                const data = await fetchUser(input.userId);

                return data;
            }
        ),
    },
}).createMachine({
    // …
    states: {
        idle: {
            on: {
                FETCH: { target: 'loading' },
            },
        },
        loading: {
            // highlight-start
            invoke: {
                id: 'getUser',
                src: 'getUser',
                input: ({ context: { userId } }) => ({
                    userId,
                }),
                onDone: {
                    target: 'success',
                    actions: assign({
                        user: ({ event }) => event.output,
                    }),
                },
                onError: {
                    target: 'failure',
                    actions: assign({
                        error: ({ event }) => event.error,
                    }),
                },
            },
            // highlight-end
        },
        success: {},
        failure: {
            on: {
                RETRY: { target: 'loading' },
            },
        },
    },
});
```

### Шпаргалка: вызов актора в корне автомата

```ts
import { createMachine } from 'xstate';
import { fromEventObservable, fromEvent } from 'rxjs';

const interactiveMachine = createMachine({
    // highlight-start
    invoke: {
        src: fromEventObservable(
            () =>
                fromEvent(
                    document.body,
                    'click'
                ) as Subscribable<EventObject>
        ),
    },
    // highlight-end
    on: {
        click: {
            actions: ({ event }) => console.log(event),
        },
    },
});
```

### Шпаргалка: вызов нескольких акторов как массив

```ts
import { createMachine } from 'xstate';

const vitalsWorkflow = createMachine({
    states: {
        CheckVitals: {
            // highlight-start
            invoke: [
                { src: 'checkTirePressure' /* ... */ },
                { src: 'checkOilPressure' /* ... */ },
                { src: 'checkCoolantLevel' /* ... */ },
                { src: 'checkBattery' /* ... */ },
            ],
            // highlight-end
        },
    },
});
```
