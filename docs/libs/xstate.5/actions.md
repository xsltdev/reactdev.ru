---
title: Действия
---

**Действия** — это эффекты типа «выстрелил и забыл». Когда машина состояний выполняет переход, она может выполнять действия. Действия происходят в ответ на события и обычно определяются в переходах в свойстве `actions: [...]`. Действия также могут быть определены для любого перехода, который входит в состояние, в свойстве состояния `entry: [...]`, или для любого перехода, который выходит из состояния, в свойстве состояния `exit: [...]`.

Действия также могут быть в `entry` или `exit` состояния, как одиночное действие или как массив.

```ts
import { setup } from 'xstate';

function trackResponse(response: string) {
    // ...
}

const feedbackMachine = setup({
    actions: {
        track: (_, params: { response: string }) => {
            trackResponse(params.response);
            // Отслеживает { response: 'good' }
        },
        showConfetti: () => {
            // ...
        },
    },
}).createMachine({
    // ...
    states: {
        // ...
        question: {
            on: {
                'feedback.good': {
                    actions: [
                        {
                            type: 'track',
                            params: { response: 'good' },
                        },
                    ],
                },
            },
            exit: [{ type: 'exitAction' }],
        },
        thanks: {
            entry: [{ type: 'showConfetti' }],
        },
    },
});
```

Примеры действий:

-   Логирование сообщения
-   Отправка сообщения другому [актору](actors.md)
-   Обновление контекста

## Действия входа и выхода

Действия входа — это действия, которые происходят при любом переходе, который входит в узел состояния. Действия выхода — это действия, которые происходят при любом переходе, который выходит из узла состояния.

Действия входа и выхода определяются с помощью атрибутов `entry: [...]` и `exit: [...]` на узле состояния. Вы можете запускать несколько действий входа и выхода в состоянии. Финальные состояния верхнего уровня не могут иметь действий выхода, поскольку машина останавливается и дальнейшие переходы невозможны.

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=f46674a5-4da3-4aca-9900-17c6ef471f50" width="100%" height="400"></iframe>

!!!info "Информация"

    Порядок выполнения действий для перехода:

    1. Действия выхода — все действия выхода покидаемых узлов состояний, от атомарного узла состояния вверх
    2. Действия перехода — все действия, определённые на выбранном переходе
    3. Действия входа — все действия входа входимых узлов состояний, от родительского состояния вниз

    Это следует [алгоритму SCXML](https://www.w3.org/TR/scxml/#microstepProcedure) для выполнения микрошага.

## Объекты действий

Объекты действий имеют `type` действия и необязательный объект `params`:

-   Свойство `type` действия описывает действие. Действия с одинаковым типом имеют одинаковую реализацию.
-   Свойство `params` действия содержит параметризованные значения, относящиеся к действию.

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    actions: {
        track: (_, params: { response: string }) => {
            /* ... */
        },
    },
}).createMachine({
    // ...
    states: {
        // ...
        question: {
            on: {
                'feedback.good': {
                    actions: [
                        {
                            // Тип действия
                            type: 'track',
                            // Параметры действия
                            params: { response: 'good' },
                        },
                    ],
                },
            },
        },
    },
});
```

## Динамические параметры действий

Вы можете динамически передавать параметры в свойстве `params` объектам действий, используя функцию, которая возвращает параметры. Функция принимает объект, содержащий текущий `context` и `event` в качестве аргументов.

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    actions: {
        logInitialRating: (
            _,
            params: { initialRating: number }
        ) => {
            // ...
        },
    },
}).createMachine({
    context: {
        initialRating: 3,
    },
    entry: [
        {
            type: 'logInitialRating',
            params: ({ context }) => ({
                initialRating: context.initialRating,
            }),
        },
    ],
});
```

Это рекомендуемый подход для того, чтобы сделать действия более переиспользуемыми, поскольку вы можете определять действия, которые не зависят от типов `context` или `event` машины.

```ts
import { setup } from 'xstate';

function logInitialRating(
    _,
    params: { initialRating: number }
) {
    console.log(`Initial rating: ${params.initialRating}`);
}

const feedbackMachine = setup({
    actions: { logInitialRating },
}).createMachine({
    context: { initialRating: 3 },
    entry: [
        {
            type: 'logInitialRating',
            params: ({ context }) => ({
                initialRating: context.initialRating,
            }),
        },
    ],
});
```

## Встроенные действия

Вы можете объявлять действия как встроенные функции:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    entry: [
        // Встроенное действие
        ({ context, event }) => {
            console.log(/* ... */);
        },
    ],
});
```

Встроенные действия полезны для прототипирования и простых случаев, но мы обычно рекомендуем использовать объекты действий.

## Реализация действий

Вы можете настроить реализации для именованных действий в свойстве `actions` функции `setup(...)`:

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
    actions: {
        track: (_, params: { msg: string }) => {
            // Реализация действия
            // ...
        },
    },
}).createMachine({
    // Конфигурация машины
    entry: [{ type: 'track', params: { msg: 'entered' } }],
});
```

Вы также можете предоставить реализации действий для переопределения существующих действий в методе `machine.provide(...)`, который создаёт новую машину с той же конфигурацией, но с предоставленными реализациями:

```ts
const feedbackActor = createActor(
    feedbackMachine.provide({
        actions: {
            track: ({ context, event }, params) => {
                // Другая реализация действия
                // (переопределяет предыдущую реализацию)
                // ...
            },
        },
    })
);
```

## Встроенные действия XState

XState предоставляет ряд полезных встроенных действий, которые являются основной частью логики ваших машин состояний, а не просто побочными эффектами.

!!!warning "Внимание"

    Встроенные действия, такие как `assign(…)`, `sendTo(…)` и `raise(…)`, **не императивны**; они возвращают специальный [объект действия](#action-objects) (например, `{ type: 'xstate.assign', … }`), который интерпретируется машиной состояний. Не вызывайте встроенные действия в пользовательских функциях действий.

    ```ts
    // ❌ Это не будет иметь эффекта
    const machine = createMachine({
        context: { count: 0 },
        entry: ({ context }) => {
            // Этот создатель действия только возвращает объект действия
            // вида { type: 'xstate.assign', ... }
            assign({ count: context.count + 1 });
        },
    });

    // ✅ Это будет работать как ожидается
    const machine = createMachine({
        context: { count: 0 },
        entry: assign({
            count: ({ context }) => context.count + 1,
        }),
    });

    // ✅ Императивные встроенные действия доступны в `enqueueActions(…)`
    const machine = createMachine({
        context: { count: 0 },
        entry: enqueueActions(({ context, enqueue }) => {
            enqueue.assign({
                count: context.count + 1,
            });
        }),
    });
    ```

## Действие assign

Действие `assign(...)` — это специальное действие, которое присваивает данные контексту состояния. Аргумент `assignments` в `assign(assignments)` указывает, какие присвоения контексту должны быть выполнены.

Присвоения могут быть объектом пар ключ-значение, где ключи — это ключи `context`, а значения — либо статические значения, либо выражения, возвращающие новое значение:

```ts
import { setup } from 'xstate';

const countMachine = setup({
    types: {
        events: {} as { type: 'increment'; value: number },
    },
}).createMachine({
    context: {
        count: 0,
    },
    on: {
        increment: {
            actions: assign({
                count: ({ context, event }) =>
                    context.count + event.value,
            }),
        },
    },
});

const countActor = createActor(countMachine);
countActor.subscribe((state) => {
    console.log(state.context.count);
});
countActor.start();
// выводит 0

countActor.send({ type: 'increment', value: 3 });
// выводит 3

countActor.send({ type: 'increment', value: 2 });
// выводит 5
```

Для более динамических присвоений аргумент, переданный в `assign(...)`, также может быть функцией, которая возвращает частичное или полное значение `context`:

```ts
import { setup } from 'xstate';

const countMachine = setup({
    types: {
        events: {} as { type: 'increment'; value: number },
    },
}).createMachine({
    context: {
        count: 0,
    },
    on: {
        increment: {
            actions: assign(({ context, event }) => {
                return {
                    count: context.count + event.value,
                };
            }),
        },
    },
});
```

!!!warning "Внимание"

    Не мутируйте объект `context`. Вместо этого вы должны использовать действие `assign(...)` для иммутабельного обновления `context`. Если вы мутируете объект `context`, вы можете получить неожиданное поведение, такое как мутация `context` других акторов.

## Действие raise

Действие raise — это специальное действие, которое _поднимает_ событие, получаемое той же машиной. Поднятие события — это способ, которым машина может «отправить» событие самой себе:

```ts
import { createMachine, raise } from 'xstate';

const machine = createMachine({
    // ...
    entry: raise({ type: 'someEvent', data: 'someData' }),
});
```

Внутренне, когда событие поднимается, оно помещается во «внутреннюю очередь событий». После завершения текущего перехода эти события обрабатываются в порядке вставки ([первым пришёл — первым вышел, или FIFO](https://ru.wikipedia.org/wiki/FIFO)). Внешние события обрабатываются только после обработки всех событий во внутренней очереди событий.

Поднятые события могут быть динамическими:

```ts
import { createMachine, raise } from 'xstate';

const machine = createMachine({
    // ...
    entry: raise(({ context, event }) => ({
        type: 'dynamicEvent',
        data: context.someValue,
    })),
});
```

События также могут быть подняты с задержкой, что не поместит их во внутреннюю очередь событий, поскольку они не будут обработаны немедленно:

```ts
import { createMachine, raise } from 'xstate';

const machine = createMachine({
    // ...
    entry: raise({ type: 'someEvent' }, { delay: 1000 }),
});
```

## Действие sendTo

Действие `sendTo(...)` — это специальное действие, которое отправляет событие определённому актору.

```ts
const machine = createMachine({
    on: {
        transmit: {
            actions: sendTo('someActor', {
                type: 'someEvent',
            }),
        },
    },
});
```

Событие может быть динамическим:

```ts
const machine = createMachine({
    on: {
        transmit: {
            actions: sendTo(
                'someActor',
                ({ context, event }) => {
                    return {
                        type: 'someEvent',
                        data: context.someData,
                    };
                }
            ),
        },
    },
});
```

Целевой актор может быть ID актора или самой ссылкой на актора:

```ts
const machine = createMachine({
    context: ({ spawn }) => ({
        someActorRef: spawn(fromPromise(/* ... */)),
    }),
    on: {
        transmit: {
            actions: sendTo(
                ({ context }) => context.someActorRef,
                {
                    type: 'someEvent',
                }
            ),
        },
    },
});
```

Другие опции, такие как `delay` и `id`, могут быть переданы как 3-й аргумент:

```ts
const machine = createMachine({
    on: {
        transmit: {
            actions: sendTo(
                'someActor',
                { type: 'someEvent' },
                {
                    id: 'transmission',
                    delay: 1000,
                }
            ),
        },
    },
});
```

Отложенные действия могут быть отменены по их `id`. См. [`cancel(...)`](#cancel-action).

## Действие sendParent

Действие `sendParent(...)` — это специальное действие, которое отправляет событие родительскому актору, если он существует.

!!!tip "Совет"

    Рекомендуется использовать `sendTo(...)`, передавая ссылки на акторов (например, ссылку на родительского актора) другим акторам через [input](./input.md) или события и сохраняя эти ссылки на акторов в `context`, а не использовать `sendParent(...)`. Это избегает тесной связи между акторами и может быть более типобезопасным.

    Пример с использованием `input`:

    ```ts
    import { createMachine, sendTo } from 'xstate';

    const childMachine = createMachine({
        context: ({ input }) => ({
            parentRef: input.parentRef,
        }),
        on: {
            someEvent: {
                actions: sendTo(
                    ({ context }) => context.parentRef,
                    {
                        type: 'tellParentSomething',
                    }
                ),
            },
        },
    });

    const parentMachine = createMachine({
        // ...
        invoke: {
            id: 'child',
            src: childMachine,
            input: ({ self }) => ({
                parentRef: self,
            }),
        },
        on: {
            tellParentSomething: {
                actions: () => {
                    console.log(
                        'Child actor told parent something'
                    );
                },
            },
        },
    });

    const parentActor = createActor(parentMachine);

    parentActor.start();
    ```

    Пример с использованием `input` (TypeScript):

    ```ts
    import {
        ActorRef,
        createActor,
        log,
        sendTo,
        setup,
        Snapshot,
    } from 'xstate';

    type ChildEvent = {
        type: 'tellParentSomething';
        data?: string;
    };
    type ParentActor = ActorRef<Snapshot<unknown>, ChildEvent>;

    const childMachine = setup({
        types: {
            context: {} as {
                parentRef: ParentActor;
            },
            input: {} as {
                parentRef: ParentActor;
            },
        },
    }).createMachine({
        context: ({ input: { parentRef } }) => ({ parentRef }),
        entry: sendTo(({ context }) => context.parentRef, {
            type: 'tellParentSomething',
            data: 'Hi parent!',
        }),
    });

    export const parent = setup({
        actors: { child: childMachine },
    }).createMachine({
        invoke: {
            src: 'child',
            input: ({ self }) => ({
                parentRef: self,
            }),
        },
        on: {
            tellParentSomething: {
                actions: log(
                    ({ event: { data } }) =>
                        `Child actor says "${data}"`
                ),
            },
        },
    });

    createActor(parent).start();
    ```

## Действие enqueueActions

Создатель действия `enqueueActions(...)` — это действие высшего уровня, которое ставит в очередь действия для последовательного выполнения, фактически не выполняя ни одно из действий. Оно принимает функцию обратного вызова, которая получает `context`, `event`, а также функции `enqueue` и `check`:

-   Функция `enqueue(...)` используется для постановки действия в очередь. Она принимает объект действия или функцию действия:

    ```ts
    actions: enqueueActions(({ enqueue }) => {
        // Поставить в очередь объект действия
        enqueue({
            type: 'greet',
            params: { message: 'hi' },
        });

        // Поставить в очередь функцию действия
        enqueue(() => console.log('Hello'));

        // Поставить в очередь простое действие без параметров
        enqueue('doSomething');
    });
    ```

-   Функция `check(...)` используется для условной постановки действия в очередь. Она принимает объект условия или функцию условия и возвращает булево значение, представляющее, вычисляется ли условие как `true`:

    ```ts
    actions: enqueueActions(({ enqueue, check }) => {
        if (check({ type: 'everythingLooksGood' })) {
            enqueue('doSomething');
        }
    });
    ```

-   Также есть вспомогательные методы на `enqueue` для постановки встроенных действий в очередь:
    -   `enqueue.assign(...)`: Ставит в очередь действие `assign(...)`
    -   `enqueue.sendTo(...)`: Ставит в очередь действие `sendTo(...)`
    -   `enqueue.raise(...)`: Ставит в очередь действие `raise(...)`
    -   `enqueue.spawnChild(...)`: Ставит в очередь действие `spawnChild(...)`
    -   `enqueue.stopChild(...)`: Ставит в очередь действие `stopChild(...)`
    -   `enqueue.cancel(...)`: Ставит в очередь действие `cancel(...)`

Поставленные в очередь действия могут вызываться условно, но они не могут быть поставлены в очередь асинхронно.

```ts
const machine = createMachine({
    // ...
    entry: enqueueActions(
        ({ context, event, enqueue, check }) => {
            // действие assign
            enqueue.assign({
                count: context.count + 1,
            });

            // Условные действия (заменяет choose(...))
            if (event.someOption) {
                enqueue.sendTo('someActor', {
                    type: 'blah',
                    thing: context.thing,
                });

                // другие действия
                enqueue('namedAction');
                // с параметрами
                enqueue({
                    type: 'greet',
                    params: { message: 'hello' },
                });
            } else {
                // встроенное
                enqueue(() => console.log('hello'));

                // даже встроенные действия
            }

            // Используйте check(...) для условной постановки действий в очередь на основе условия
            if (check({ type: 'someGuard' })) {
                // ...
            }

            // без return
        }
    ),
});
```

Вы можете использовать параметры с ссылочными действиями enqueue:

```ts
import { setup, enqueueActions } from 'xstate';

const machine = setup({
    actions: {
        doThings: enqueueActions(
            ({ enqueue }, params: { name: string }) => {
                enqueue({
                    type: 'greet',
                    params: { name },
                });
                // ...
            }
        ),
        greet: (_, params: { name: string }) => {
            console.log(`Hello ${params.name}!`);
        },
    },
}).createMachine({
    // ...
    entry: {
        type: 'doThings',
        params: { name: 'World' },
    },
});
```

## Действие log

Действие `log(...)` — это простой способ логирования сообщений в консоль.

```ts
import { createMachine, log } from 'xstate';

const machine = createMachine({
    on: {
        someEvent: {
            actions: log('some message'),
        },
    },
});
```

## Действие cancel {#cancel-action}

Действие `cancel(...)` отменяет отложенное действие `sendTo(...)` или `raise(...)` по их ID:

```ts
import { createMachine, sendTo, cancel } from 'xstate';

const machine = createMachine({
    on: {
        event: {
            actions: sendTo(
                'someActor',
                { type: 'someEvent' },
                {
                    id: 'someId',
                    delay: 1000,
                }
            ),
        },
        cancelEvent: {
            actions: cancel('someId'),
        },
    },
});
```

## Действие stopChild

Действие `stopChild(...)` останавливает дочернего актора. Акторы могут быть остановлены только их родительским актором:

```ts
import { createMachine, stopChild } from 'xstate';

const machine = createMachine({
    context: ({ spawn }) => ({
        spawnedRef: spawn(fromPromise(/* ... */), {
            id: 'spawnedId',
        }),
    }),
    on: {
        stopById: {
            actions: stopChild('spawnedId'),
        },
        stopByRef: {
            actions: stopChild(
                ({ context }) => context.spawnedRef
            ),
        },
    },
});
```

## Моделирование

Если вам нужно только выполнять действия в ответ на события, вы можете создать [самопереход](transitions.md#self-transitions), который имеет только определённый `actions: [ ... ]`. Например, машина, которой нужно только присваивать значения в `context` в переходах, может выглядеть так:

```ts
import { createMachine } from 'xstate';

const countMachine = createMachine({
    context: {
        count: 0,
    },
    on: {
        increment: {
            actions: assign({
                count: ({ context, event }) =>
                    context.count + event.value,
            }),
        },
        decrement: {
            actions: assign({
                count: ({ context, event }) =>
                    context.count - event.value,
            }),
        },
    },
});
```

## Сокращения

Для простых действий вы можете указать строку действия вместо объекта действия. Хотя мы предпочитаем использовать объекты для согласованности.

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    // ...
    states: {
        // ...
        question: {
            on: {
                'feedback.good': {
                    actions: ['track'],
                },
            },
        },
    },
});
```

## Действия и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Чтобы строго настроить типы действий, используйте функцию `setup({ ... })` и поместите реализации действий в объект `actions: { ... }`. Ключ — это тип действия, а значение — реализация функции действия.

Вы также должны строго типизировать параметры функции действия, которые передаются как второй аргумент функции действия.

```ts
import { setup } from 'xstate';

const machine = setup({
    actions: {
        track: (_, params: { response: string }) => {
            // ...
        },
        increment: (_, params: { value: number }) => {
            // ...
        },
    },
}).createMachine({
    // ...
    entry: [
        { type: 'track', params: { response: 'good' } },
        { type: 'increment', params: { value: 1 } },
    ],
});
```

Если вы не используете `setup({ ... })` (настоятельно рекомендуется), вы можете строго типизировать `actions` вашей машины в свойстве `types.actions` конфигурации машины.

```ts
const machine = createMachine({
    types: {} as {
        actions:
            | {
                  type: 'track';
                  params: {
                      response: string;
                  };
              }
            | {
                  type: 'increment';
                  params: { value: number };
              };
    },
    // ...
    entry: [
        { type: 'track', params: { response: 'good' } },
        { type: 'increment', params: { value: 1 } },
    ],
});
```

## Шпаргалка по действиям

### Шпаргалка: действия входа и выхода

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    // Действие входа на корневом уровне
    entry: [{ type: 'entryAction' }],
    exit: [{ type: 'exitAction' }],
    initial: 'start',
    states: {
        start: {
            entry: [{ type: 'startEntryAction' }],
            exit: [{ type: 'startExitAction' }],
        },
    },
});
```

### Шпаргалка: действия перехода

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    on: {
        someEvent: {
            actions: [
                { type: 'doSomething' },
                { type: 'doSomethingElse' },
            ],
        },
    },
});
```

### Шпаргалка: встроенные функции действий

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    on: {
        someEvent: {
            actions: [
                ({ context, event }) => {
                    console.log(context, event);
                },
            ],
        },
    },
});
```

### Шпаргалка: настройка действий

```ts
import { setup } from 'xstate';

const someAction = () => {
    //...
};

const machine = setup({
    actions: {
        someAction,
    },
}).createMachine({
    entry: [{ type: 'someAction' }],
    // ...
});
```

### Шпаргалка: предоставление действий

```ts
import { setup } from 'xstate';

const someAction = () => {
    //...
};

const machine = setup({
    actions: {
        someAction,
    },
}).createMachine({
    // ...
});

const modifiedMachine = machine.provide({
    someAction: () => {
        // Переопределённая реализация действия
    },
});
```

### Шпаргалка: действие assign

#### С присваивателями свойств

```ts
import { createMachine } from 'xstate';

const countMachine = createMachine({
    context: {
        count: 0,
    },
    on: {
        increment: {
            actions: assign({
                count: ({ context, event }) => {
                    return context.count + event.value;
                },
            }),
        },
    },
});
```

#### С функциями-присваивателями

```ts
import { createMachine } from 'xstate';

const countMachine = createMachine({
    context: {
        count: 0,
    },
    on: {
        increment: {
            actions: assign(({ context, event }) => {
                return {
                    count: context.count + event.value,
                };
            }),
        },
    },
});
```

### Шпаргалка: действие raise

```ts
import { createMachine, raise } from 'xstate';

const machine = createMachine({
    on: {
        someEvent: {
            actions: raise({ type: 'anotherEvent' }),
        },
    },
});
```

### Шпаргалка: действие sendTo

```ts
const machine = createMachine({
    on: {
        transmit: {
            actions: sendTo('someActor', {
                type: 'someEvent',
            }),
        },
    },
});
```

### Шпаргалка: действие enqueueActions

```ts
import { createMachine, enqueueActions } from 'xstate';

const machine = createMachine({
    entry: enqueueActions(({ enqueue, check }) => {
        enqueue({ type: 'someAction' });

        if (check({ type: 'someGuard' })) {
            enqueue({ type: 'anotherAction' });
        }

        enqueue.assign({
            count: 0,
        });

        enqueue.sendTo('someActor', { type: 'someEvent' });

        enqueue.raise({ type: 'anEvent' });
    }),
});
```
