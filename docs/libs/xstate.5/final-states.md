---
title: Финальные состояния
---

Финальное состояние — это состояние, которое представляет завершение или успешное окончание машины. Оно определяется свойством `type: 'final'` на узле состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            /* ... */
        },
        thanks: {
            /* ... */
        },
        closed: {
            type: 'final',
        },
        // ...
    },
    on: {
        'feedback.close': {
            target: '.closed',
        },
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=7d3feeca-1017-4d94-87b3-cd5128682440" width="100%" height="400"></iframe>

Когда машина достигает финального состояния, она больше не может получать события, и всё, что работает внутри неё, отменяется и очищается. Блок с окружающей рамкой представляет финальное состояние.

Машина может иметь несколько финальных состояний или не иметь финальных состояний.

-   Машина состояний может иметь ноль или более финальных состояний. Некоторые машины могут работать бесконечно и не нуждаться в завершении.
-   Финальные состояния могут иметь данные `output`, которые отправляются родительской машине при завершении машины.
-   Когда машина достигает финального состояния верхнего уровня, она завершается.
-   Финальные состояния не могут иметь переходов

## Финальные состояния верхнего уровня

Финальное состояние верхнего уровня — это финальное состояние, которое является непосредственным дочерним состоянием машины. Когда машина достигает финального состояния верхнего уровня, машина завершается. Когда машина завершается, она больше не может получать события и переходить.

## Дочерние финальные состояния

Когда достигается дочернее финальное состояние [родительского (составного) состояния](./parent-states.md), это родительское состояние считается «завершённым». Переход `onDone` этого родительского состояния выполняется автоматически.

```ts
import { createMachine } from 'xstate';

const coffeeMachine = createMachine({
    initial: 'preparation',
    states: {
        preparation: {
            initial: 'weighing',
            states: {
                weighing: {
                    on: {
                        weighed: {
                            target: 'grinding',
                        },
                    },
                },
                grinding: {
                    on: {
                        ground: 'ready',
                    },
                },
                // Дочернее финальное состояние родительского состояния 'preparation'
                ready: {
                    type: 'final',
                },
            },
            // Переход будет выполнен при достижении дочернего финального состояния
            onDone: {
                target: 'brewing',
            },
        },
        brewing: {
            // ...
        },
    },
});
```

## Финальные состояния в параллельных состояниях

Когда все регионы параллельного состояния «завершены», параллельное состояние считается «завершённым». Выполняется переход `onDone` параллельного состояния.

В этом примере состояние `preparation` является параллельным состоянием с двумя регионами: `beans` и `water`. Когда оба региона завершены, состояние `preparation` завершено, и происходит вход в состояние `brewing`.

```ts
import { createMachine, createActor } from 'xstate';

const coffeeMachine = createMachine({
    initial: 'preparation',
    states: {
        preparation: {
            type: 'parallel',
            states: {
                beans: {
                    initial: 'grinding',
                    states: {
                        grinding: {
                            on: {
                                grindingComplete: 'ground',
                            },
                        },
                        ground: {
                            type: 'final',
                        },
                    },
                },
                water: {
                    initial: 'heating',
                    states: {
                        heating: {
                            always: {
                                guard: 'waterBoiling',
                                target: 'heated',
                            },
                        },
                        heated: {
                            type: 'final',
                        },
                    },
                },
            },
            onDone: 'brewing',
        },
        brewing: {},
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=95504ba2-3da2-4d70-a3b5-59bbcd31bf2d" width="100%" height="400"></iframe>

## Выходные данные

Когда машина достигает своего финального состояния верхнего уровня, она может произвести выходные данные. Вы можете указать эти выходные данные в свойстве `.output` конфигурации машины:

```ts
import { createMachine, createActor } from 'xstate';

const currencyMachine = createMachine({
    // ...
    states: {
        converting: {
            // ...
        },
        converted: {
            type: 'final',
        },
    },
    output: ({ context }) => ({
        amount: context.amount,
        currency: context.currency,
    }),
});

const currencyActor = createActor(currencyMachine, {
    input: {
        amount: 10,
        fromCurrency: 'USD',
        toCurrency: 'EUR',
    },
});

currencyActor.subscribe({
    complete() {
        console.log(currencyActor.getSnapshot().output);
        // выводит, например, { amount: 12, currency: 'EUR' }
    },
});
```

Свойство `.output` также может быть статическим значением:

```ts
import { createMachine, createActor } from 'xstate';

const processMachine = createMachine({
    // ...
    output: {
        message: 'Process completed.',
    },
});
```

## Шпаргалка по финальным состояниям

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            /* ... */
        },
        thanks: {
            /* ... */
        },
        closed: {
            type: 'final',
        },
        // ...
    },
    on: {
        'feedback.close': {
            target: '.closed',
        },
    },
});
```

## Шпаргалка: финальные состояния в параллельных состояниях

```ts
import { createMachine } from 'xstate';

const coffeeMachine = createMachine({
    initial: 'preparation',
    states: {
        preparation: {
            type: 'parallel',
            states: {
                beans: {
                    initial: 'grinding',
                    states: {
                        grinding: {
                            on: {
                                grindingComplete: 'ground',
                            },
                        },
                        ground: {
                            type: 'final',
                        },
                    },
                },
                water: {
                    initial: 'heating',
                    states: {
                        heating: {
                            always: {
                                guard: 'waterBoiling',
                                target: 'heated',
                            },
                        },
                        heated: {
                            type: 'final',
                        },
                    },
                },
            },
            onDone: 'brewing',
        },
        brewing: {},
    },
});
```
