---
title: События и переходы
---

**Переход** (transition) — это изменение одного конечного состояния на другое, инициируемое событием.

**Событие** (event) — это сигнал, триггер или сообщение, вызывающее переход. Когда актор получает событие, его машина определяет, есть ли в текущем состоянии активные переходы для этого события. Если активные переходы существуют, машина выполнит их и выполнит связанные с ними действия.

<iframe src="https://stately.ai/registry/editor/embed/e13bef2b-bb13-4465-96ac-0bc25340688e?machineId=9630e3b7-9f8e-4dc9-8b55-661f854d28b7&mode=Simulate" width="100%" height="400"></iframe>

Переходы являются «детерминированными»; каждая комбинация состояния и события всегда указывает на одно и то же следующее состояние. Когда машина состояний получает событие, только активные конечные состояния проверяются на наличие перехода для этого события. Такие переходы называются **активными переходами**. Если есть активный переход, машина состояний выполнит действия перехода, а затем перейдёт в целевое состояние.

Переходы представлены с помощью `on:` в состоянии:

```ts
import { createMachine } from 'xstate';
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'question',
    states: {
        question: {
            on: {
                'feedback.good': {
                    target: 'thanks',
                },
            },
        },
        thanks: {},
    },
});
```

## Объекты событий {#event-objects}

В XState события представлены объектами событий со свойством `type` и необязательной полезной нагрузкой:

-   Свойство `type` — это строка, представляющая тип события.
-   Полезная нагрузка — это объект, содержащий дополнительные данные о событии.

```ts
feedbackActor.send({
    // Тип события
    type: 'feedback.update',
    // Дополнительная полезная нагрузка
    feedback: 'This is great!',
    rating: 5,
});
```

## Выбор переходов

Переходы выбираются путём проверки сначала самых глубоких дочерних состояний. Если переход активен (то есть, если его защита проходит), он будет выполнен. Если нет, будет проверено родительское состояние и так далее.

1.  Начните с самых глубоких активных узлов состояния (также известных как атомарные узлы состояния)
2.  Если переход активен (нет `guard` или его `guard` вычисляется как `true`), выберите его.
3.  Если ни один переход не активен, перейдите к родительскому узлу состояния и повторите шаг 1.
4.  Наконец, если ни один переход не активен, переходы не будут выполнены, и состояние не изменится.

## Самопереходы {#self-transitions}

Состояние может переходить в себя. Это называется **самопереход** и полезно для изменения контекста и/или выполнения действий без изменения конечного состояния. Вы также можете использовать самопереходы для перезапуска состояния.

**Корневые самопереходы:**

```ts
import { createMachine, assign } from 'xstate';

const machine = createMachine({
    context: { count: 0 },
    on: {
        someEvent: {
            // Нет цели
            actions: assign({
                count: ({ context }) => context.count + 1,
            }),
        },
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=91da1d57-b146-48fd-82ce-a9dd28b7261a" width="100%" height="400"></iframe>

**Самопереходы в состояниях:**

```ts
import { createMachine, assign } from 'xstate';

const machine = createMachine({
    context: { count: 0 },
    initial: 'inactive',
    states: {
        inactive: {
            on: { activate: { target: 'active' } },
        },
        active: {
            on: {
                someEvent: {
                    // Нет цели
                    actions: assign({
                        count: ({ context }) =>
                            context.count + 1,
                    }),
                },
            },
        },
    },
});
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=8763e570-3535-42b3-a2a2-8edd82d1207a" width="100%" height="400"></iframe>

## Переходы между состояниями

Обычно переходы происходят между двумя соседними состояниями. Эти переходы определяются путём установки `target` в качестве ключа соседнего состояния.

```ts
const feedbackMachine = createMachine({
    // ...
    states: {
        form: {
            on: {
                submit: {
                    // Цель — это ключ соседнего состояния
                    target: 'submitting',
                },
            },
        },
        submitting: {
            // ...
        },
    },
});
```

## Переходы от родителя к потомку

Когда актор машины состояний получает событие, он сначала проверяет самое глубокое ([атомарное](state-machines-and-statecharts.md#atomic-states)) состояние, чтобы узнать, есть ли активный переход. Если нет, проверяется родительское состояние и так далее, пока машина состояний не достигнет корневого состояния.

Когда вы хотите, чтобы событие переходило в состояние независимо от того, какое соседнее состояние активно, полезным паттерном является переход от родительского состояния к дочернему.

Например, приведённая ниже машина состояний перейдёт в состояние `colorMode.system` при событии `mode.reset` независимо от того, в каком состоянии она находится в данный момент.

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    id: 'colorMode',
    initial: 'system',
    states: {
        system: {},
        auto: {},
        light: {
            on: {
                'mode.toggle': { target: 'dark' },
            },
        },
        dark: {
            on: {
                'mode.toggle': { target: 'light' },
            },
        },
    },
    on: {
        'mode.reset': {
            target: '.system',
        },
    },
});
```

## Повторный вход {#re-entering}

По умолчанию, когда машина состояний переходит из некоторого состояния в то же самое состояние или из родительского состояния в потомка (дочернее, внучатое и т.д.) этого родительского состояния, она не выполняет повторный вход в состояние; то есть она не будет выполнять [действия `exit` и `entry`](actions.md) родительского состояния. Она не остановит существующих вызванных акторов и не запустит новых.

Это можно изменить с помощью свойства перехода `reenter`: если вы хотите, чтобы родительское состояние было введено повторно, вы можете установить `reenter: true`. Это приведёт к повторному входу в состояние при переходе к себе или состояниям-потомкам, выполняя действия `exit` и `entry` состояния. Это остановит существующих вызванных акторов и запустит новых.

!!!tip "Совет"

    В XState v4 переходы с повторным входом были известны как **внешние переходы**, а переходы по умолчанию — как **внутренние переходы**.

**Самопереходы с `reenter: true`:**

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    initial: 'someState',
    states: {
        someState: {
            entry: () => console.log('someState entered'),
            exit: () => console.log('someState exited'),
            on: {
                'event.normal': {
                    target: 'someState', // или без цели
                },
                'event.thatReenters': {
                    target: 'someState', // или без цели
                    reenter: true,
                },
            },
        },
    },
});

const actor = createActor(machine);
actor.start();

actor.send({ type: 'event.normal' });
// Ничего не выводит

actor.send({ type: 'event.thatReenters' });
// Выводит:
// "someState exited"
// "someState entered"
```

**Переходы родитель-потомок с `reenter: true`:**

```ts
const machine = createMachine({
    initial: 'parentState',
    states: {
        parentState: {
            entry: () => console.log('parentState entered'),
            exit: () => console.log('parentState exited'),
            on: {
                'event.normal': {
                    target: '.someChildState',
                },
                'event.thatReenters': {
                    target: '.otherChildState',
                    reenter: true,
                },
            },
            initial: 'someChildState',
            states: {
                someChildState: {
                    entry: () =>
                        console.log(
                            'someChildState entered'
                        ),
                    exit: () =>
                        console.log(
                            'someChildState exited'
                        ),
                },
                otherChildState: {
                    entry: () =>
                        console.log(
                            'otherChildState entered'
                        ),
                    exit: () =>
                        console.log(
                            'otherChildState exited'
                        ),
                },
            },
        },
    },
});

const actor1 = createActor(machine);
actor1.start();
actor1.send({ type: 'event.normal' });
// Выводит:
// "someChildState exited"
// "someChildState entered"

const actor2 = createActor(machine);
actor2.start();
console.log('---');
actor2.send({ type: 'event.thatReenters' });
// Выводит:
// "someChildState exited"
// "parentState exited"
// "parentState entered"
// "otherChildState entered"
```

## Переходы в любое состояние

Соседние состояния-потомки: `{ target: 'sibling.child.grandchild' }`

Родительские к потомкам: `{ target: '.child.grandchild' }`

Состояние в любое состояние: `{ target: '#specificState' }`

## Запрещённые переходы

-   `{ on: { forbidden: {} } }`
-   Отличается от пропуска перехода; алгоритм выбора перехода прекратит поиск
-   То же самое, что `{ on: { forbidden: { target: undefined } } }`

## Переходы с подстановочными знаками

Переход с подстановочным знаком — это переход, который соответствует любому событию. Дескриптор события (ключ объекта `on: {...}`) определяется с использованием подстановочного символа `*` в качестве типа события:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'asleep',
    states: {
        asleep: {
            on: {
                // Этот переход будет соответствовать любому событию
                '*': { target: 'awake' },
            },
        },
        awake: {},
    },
});
```

Переходы с подстановочными знаками полезны для:

-   обработки событий, которые не обрабатываются никаким другим переходом.
-   в качестве перехода «на все случаи», который обрабатывает любое событие в состоянии.

Переход с подстановочным знаком имеет наименьший приоритет; он будет выполнен только в том случае, если никакие другие переходы не активны.

## Частичные переходы с подстановочными знаками {#partial-wildcard-transitions}

Частичный переход с подстановочным знаком — это переход, который соответствует любому событию, начинающемуся с определённого префикса. Дескриптор события определяется путём использования подстановочного символа (`*`) после точки (`.`) в качестве типа события:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                // Это будет соответствовать событию 'feedback', а также
                // любому событию, начинающемуся с 'feedback.', например:
                // 'feedback.good', 'feedback.bad' и т.д.
                'feedback.*': { target: 'form' },
            },
        },
        form: {},
        // ...
    },
});
```

Подстановочный символ (`*`) может использоваться только в суффиксе дескриптора события после точки (`.`):

### Допустимые примеры с подстановочными знаками

-   ✅ `mouse.*`: соответствует `mouse`, `mouse.click`, `mouse.move` и т.д.
-   ✅ `mouse.click.*`: соответствует `mouse.click`, `mouse.click.left`, `mouse.click.right` и т.д.

### Недопустимые подстановочные знаки

-   🚫 ~~`mouse*`~~: недопустимо; не соответствует никакому событию.
-   🚫 ~~`mouse.*.click`~~: недопустимо; `*` нельзя использовать в середине дескриптора события.
-   🚫 ~~`*.click`~~: недопустимо; `*` нельзя использовать в префиксе дескриптора события.
-   🚫 ~~`mouse.click*`~~: недопустимо; не соответствует никакому событию.
-   🚫 ~~`mouse.*.*`~~: недопустимо; `*` нельзя использовать в середине дескриптора события.

## Множественные переходы в параллельных состояниях

Поскольку параллельные состояния имеют несколько регионов, которые могут быть активны одновременно, возможно, чтобы несколько переходов были активны одновременно. В этом случае все активные переходы в эти регионы будут выполнены.

Множественные цели указываются как массив строк:

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    type: 'parallel',
    states: {
        mode: {
            initial: 'light',
            states: {
                light: {
                    on: {
                        toggle: { target: 'dark' },
                    },
                },
                dark: {
                    on: {
                        toggle: { target: 'light' },
                    },
                },
            },
        },
        theme: {
            initial: 'default',
            states: {
                default: {
                    on: {
                        change: { target: 'custom' },
                    },
                },
                custom: {
                    on: {
                        change: { target: 'default' },
                    },
                },
            },
        },
    },
    on: {
        // Это событие переведёт оба региона в определённые состояния
        'set.dark.custom': {
            target: ['.mode.dark', '.theme.custom'],
        },
        // Это событие переведёт один регион, оставив другой без изменений
        'set.light': {
            target: '.mode.light',
        },
    },
});
```

В этом примере:

-   Событие `set.dark.custom` одновременно переведёт оба региона: регион `mode` в `dark` и регион `theme` в `custom`
-   Событие `set.light` переведёт только регион `mode` в `light`, оставив регион `theme` в текущем состоянии
-   Каждый регион всё ещё может управляться независимо через свои собственные события (`toggle` и `change`)

## Другие переходы

-   [**Безсобытийные (always) переходы**](eventless-transitions.md) — это переходы без событий. Эти переходы _всегда_ выполняются после любого перехода в их состоянии, который активен.
-   [**Отложенные (after) переходы**](delayed-transitions.md) — это переходы, которые активируются после указанной продолжительности.

## Описания переходов

Вы можете добавить строку `.description` к переходу, чтобы описать его. Это полезно для объяснения назначения перехода в визуализированной машине состояний.

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    // ...
    on: {
        exit: {
            description: 'Закрывает форму обратной связи',
            target: '.closed',
        },
    },
});
```

## Сокращения

Если переход указывает только `target`, то строковая цель может использоваться как сокращение вместо всего объекта перехода:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                // Это сокращение для:
                // 'feedback': { target: 'form' }
                'feedback.good': 'thanks',
            },
        },
        thanks: {},
        // ...
    },
});
```

Использование сокращения строковой цели полезно для быстрого прототипирования машин состояний. В целом, мы рекомендуем использовать полный синтаксис объекта перехода, так как он будет согласован со всеми другими объектами перехода и будет легче добавлять действия, защиты и другие свойства к переходу в будущем.

## TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Переходы в основном используют тип события, которым они активируются.

```ts
import { setup } from 'xstate';

const machine = setup({
    types: {
        events: {} as
            | { type: 'greet'; message: string }
            | { type: 'submit' },
    },
}).createMachine({
    // ...
    on: {
        greet: {
            actions: ({ event }) => {
                event.type; // 'greet'
                event.message; // string
            },
        },
    },
});
```

## Часто задаваемые вопросы {#faqs}

**Как я могу прослушивать события, отправляемые акторам?**

Вы можете использовать [API инспекции](./inspection.md) для прослушивания всех событий инспекции в системе акторов. Событие инспекции `@xstate.event` содержит информацию о событиях, отправляемых от одного актора к другому (или самому себе):

```ts
import { createActor } from 'xstate';
import { someMachine } from './someMachine';

const actor = createActor(someMachine, {
    inspect: (inspectionEvent) => {
        if (inspectionEvent.type === '@xstate.event') {
            // Объект события, отправленный от одного актора к другому
            console.log(inspectionEvent.event);
        }
    },
});
```

## Шпаргалка по переходам

Используйте нашу шпаргалку по событиям и переходам XState ниже для быстрого старта.

### Шпаргалка: объекты событий

```ts
feedbackActor.send({
    // Тип события
    type: 'feedback.update',
    // Полезная нагрузка события
    feedback: 'A+ would use state machines again',
    rating: 5,
});
```

### Шпаргалка: цели переходов

```ts
const machine = createMachine({
    initial: 'a',
    states: {
        a: {
            on: {
                // Соседняя цель
                event: {
                    target: 'b',
                },
                // Дочерняя цель соседа
                otherEvent: {
                    target: 'b.c',
                },
            },
        },
        b: {
            on: {
                // Цель по ID
                event: {
                    target: '#c',
                },
            },
        },
        c: {
            id: 'c',
            on: {
                // Дочерняя цель
                event: {
                    target: '.child',
                },
            },
            initial: 'child',
            states: {
                child: {},
            },
        },
    },
    on: {
        // Дочерняя цель
        someEvent: {
            target: '.b',
        },
    },
});
```

## Чистые функции переходов

_Начиная с XState версии 5.19.0_

Вы можете вычислить следующее состояние и действия машины состояний без создания живого актора, используя чистые функции `transition(machine, state, event)` и `initialTransition(machine)`. Эти функции возвращают кортежи `[nextState, actions]`, которые представляют, что произойдёт во время перехода, но без выполнения каких-либо побочных эффектов.

Это полезно для:

-   Серверных приложений и API-эндпоинтов
-   Тестирования логики машины состояний
-   Предварительного просмотра состояний и отладки
-   Сценариев, где требуется детерминированное поведение

!!!tip "Совет"

    Для полной документации по чистым функциям переходов смотрите руководство [Чистые функции переходов](pure-transitions.md).

```ts
import {
    createMachine,
    initialTransition,
    transition,
} from 'xstate';

const machine = createMachine({
    initial: 'pending',
    states: {
        pending: {
            on: {
                start: { target: 'started' },
            },
        },
        started: {
            entry: 'doSomething',
        },
    },
});

const [initialState, initialActions] = initialTransition(
    machine
);
const [nextState, actions] = transition(
    machine,
    initialState,
    {
        type: 'start',
    }
);

console.log(nextState.value); // 'started'
console.log(actions); // [{ type: 'doSomething', … }]
```

## Определение следующего состояния

!!!warning "Внимание"

    Рекомендуется использовать функции `initialTransition(…)` и `transition(…)` вместо `getNextSnapshot(…)` и `getInitialSnapshot(…)`, которые будут объявлены устаревшими.

Когда вы создаёте актора машины состояний, следующее состояние определяется текущим состоянием машины и событием, отправленным актору. Если вы хотите определить следующее состояние вне актора, вы можете использовать функцию `getNextSnapshot(…)`:

```ts
import { getNextSnapshot } from 'xstate';
import { feedbackMachine } from './feedbackMachine';

const nextSnapshot = getNextSnapshot(
    feedbackMachine,
    feedbackMachine.resolveState({ value: 'question' }),
    { type: 'feedback.good' }
);

console.log(nextSnapshot.value);
// выводит 'thanks'
```

Вы также можете определить начальное состояние машины с помощью функции `getInitialSnapshot(…)`:

```ts
import { getInitialSnapshot } from 'xstate';
import { feedbackMachine } from './feedbackMachine';

const initialSnapshot = getInitialSnapshot(
    feedbackMachine,
    // необязательный ввод
    { defaultRating: 3 }
);

console.log(initialSnapshot.value);
// выводит 'question'
```
