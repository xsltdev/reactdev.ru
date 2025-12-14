---
title: 'Акторы'
---

Когда вы запускаете конечный автомат, он становится актором: работающим процессом, который может получать события, отправлять события и изменять своё поведение на основе получаемых событий, что может вызывать эффекты за пределами актора.

В конечных автоматах акторы могут быть **вызваны** или **порождены**. По сути это одно и то же, с единственным различием в том, как контролируется жизненный цикл актора.

-   **Вызванный актор** запускается, когда его родительский автомат входит в [состояние](states.md), в котором он вызван, и останавливается при выходе из этого состояния.
-   **Порождённый актор** запускается в [переходе](transitions.md) и останавливается либо с помощью [действия `stop(...)`](actions.md#stop-action), либо при остановке родительского автомата.

![type:video](https://www.youtube.com/watch?v=Rj7lOvDwcYs)

## Модель акторов

В модели акторов акторы — это объекты, которые могут взаимодействовать друг с другом. Они являются независимыми «живыми» сущностями, которые общаются посредством асинхронной передачи сообщений. В XState эти сообщения называются _[событиями](transitions.md)_.

-   Актор имеет собственное внутреннее, инкапсулированное состояние, которое может обновляться только самим актором. Актор может обновить своё внутреннее состояние в ответ на полученное сообщение, но оно не может быть обновлено никакой другой сущностью.
-   Акторы общаются с другими акторами, отправляя и получая события асинхронно.
-   Акторы обрабатывают по одному сообщению за раз. Они имеют внутренний «почтовый ящик», который действует как очередь событий, обрабатывая события последовательно.
-   Внутреннее состояние актора не разделяется между акторами. Единственный способ для актора поделиться частью своего внутреннего состояния:
    -   Отправка событий другим акторам
    -   Или генерация снимков (`snapshots`), которые можно рассматривать как неявные события, отправляемые подписчикам.
-   Акторы могут создавать (`spawn`/`invoke`) новых акторов.

[Подробнее о модели акторов](actor-model.md)

## Логика актора

Логика актора — это логическая «модель» актора (мозг, чертёж, ДНК и т.д.). Она описывает, как актор должен изменять поведение при получении события. Вы можете создавать логику актора с помощью **[создателей логики актора](#actor-logic-creators)**.

В XState логика актора определяется объектом, реализующим интерфейс `ActorLogic`, содержащим методы, такие как `.transition(...)`, `.getInitialSnapshot()`, `.getPersistedSnapshot()` и другие. Этот объект сообщает интерпретатору, как обновлять внутреннее состояние актора при получении события и какие эффекты выполнять (если есть).

## Создание акторов

Вы можете создать актор, который является «живым» экземпляром некоторой логики актора, с помощью `createActor(actorLogic, options?)`. Функция `createActor(...)` принимает следующие аргументы:

-   `actorLogic`: [логика актора](actors.md#actor-logic) для создания актора
-   `options` (необязательно): опции актора

Когда вы создаёте актор из логики актора через `createActor(actorLogic)`, вы неявно создаёте [систему акторов](system.md), где созданный актор является корневым актором. Любые акторы, порождённые из этого корневого актора и его потомков, являются частью этой системы акторов. Актор должен быть запущен вызовом `actor.start()`, что также запустит систему акторов:

```ts
import { createActor } from 'xstate';
import { someActorLogic } from './someActorLogic.ts';

const actor = createActor(someActorLogic);

actor.subscribe((snapshot) => {
    console.log(snapshot);
});

actor.start();

// Теперь актор может получать события
actor.send({ type: 'someEvent' });
```

Вы можете остановить корневых акторов, вызвав `actor.stop()`, что также остановит систему акторов и всех акторов в этой системе:

```ts
// Останавливает корневой актор, систему акторов и акторов в системе
actor.stop();
```

### Вызов и порождение акторов

Вызванный актор представляет актор на основе состояния, поэтому он останавливается при выходе из вызывающего состояния. Вызванные акторы используются для конечного/известного количества акторов.

Порождённый актор представляет множество сущностей, которые могут быть запущены в любое время и остановлены в любое время. Порождённые акторы основаны на действиях и используются для динамического или неизвестного количества акторов.

Примером различия между вызовом и порождением акторов может быть приложение для задач. При загрузке задач актор `loadTodos` будет вызванным актором; он представляет одну задачу на основе состояния. Для сравнения, каждая из задач сама может быть порождённым актором, и их может быть динамическое количество.

-   [Подробнее о вызове акторов](invoke.md)
-   [Подробнее о порождении акторов](spawn.md)

## Снимки актора

Когда актор получает событие, его внутреннее состояние может измениться. Актор может генерировать **снимок** при переходе состояния. Вы можете синхронно прочитать снимок актора через `actor.getSnapshot()` или подписаться на снимки через `actor.subscribe(observer)`.

```ts
import { fromPromise, createActor } from 'xstate';

async function fetchCount() {
    return Promise.resolve(42);
}

const countLogic = fromPromise(async () => {
    const count = await fetchCount();

    return count;
});

const countActor = createActor(countLogic);

countActor.start();

countActor.getSnapshot(); // выводит undefined

// После разрешения промиса...
countActor.getSnapshot();
// => {
//   output: 42,
//   status: 'done',
//   ...
// }
```

## Подписки

Вы можете подписаться на значения снимков актора через `actor.subscribe(observer)`. Наблюдатель будет получать значение снимка актора при его генерации. Наблюдатель может быть:

-   Простой функцией, которая получает последний снимок, или
-   Объектом-наблюдателем, метод `.next(snapshot)` которого получает последний снимок

```ts
// Наблюдатель как простая функция
const subscription = actor.subscribe((snapshot) => {
    console.log(snapshot);
});
```

```ts
// Наблюдатель как объект
const subscription = actor.subscribe({
    next(snapshot) {
        console.log(snapshot);
    },
    error(err) {
        // ...
    },
    complete() {
        // ...
    },
});
```

Возвращаемое значение `actor.subscribe(observer)` — это объект подписки, у которого есть метод `.unsubscribe()`. Вы можете вызвать `subscription.unsubscribe()` для отписки наблюдателя:

```ts
const subscription = actor.subscribe((snapshot) => {
    /* ... */
});

// Отписка наблюдателя
subscription.unsubscribe();
```

Когда актор останавливается, все его наблюдатели будут автоматически отписаны.

Вы можете инициализировать логику актора в определённом сохранённом снимке (состоянии), передав состояние во втором аргументе `options` функции `createActor(logic, options)`. Если состояние совместимо с логикой актора, это создаст актор, который будет запущен в этом сохранённом состоянии:

```ts
const persistedState = JSON.parse(
    localStorage.getItem('some-persisted-state')
);

const actor = createActor(someLogic, {
    // highlight-start
    snapshot: persistedState,
    // highlight-end
});

actor.subscribe(() => {
    localStorage.setItem(
        'some-persisted-state',
        JSON.stringify(actor.getPersistedSnapshot())
    );
});

// Актор будет запущен в сохранённом состоянии
actor.start();
```

См. [персистентность](persistence.md) для получения дополнительной информации.

## `waitFor`

Вы можете дождаться, пока снимок актора удовлетворит предикат, используя вспомогательную функцию `waitFor(actor, predicate, options?)`. Функция `waitFor(...)` возвращает промис, который:

-   Разрешается, когда сгенерированный снимок удовлетворяет функцию `predicate`
-   Разрешается немедленно, если текущий снимок уже удовлетворяет функцию `predicate`
-   Отклоняется, если возникает ошибка или истекает значение `options.timeout`.

```ts
import { waitFor } from 'xstate';
import { countActor } from './countActor.ts';

const snapshot = await waitFor(
    countActor,
    (snapshot) => {
        return snapshot.context.count >= 100;
    },
    {
        timeout: 10_000, // 10 секунд (10 000 миллисекунд)
    }
);

console.log(snapshot.output);
// => 100
```

## Обработка ошибок

Вы можете подписаться на ошибки, выбрасываемые актором, используя колбэк `error` в объекте-наблюдателе, передаваемом в `actor.subscribe()`. Это позволяет обрабатывать ошибки, генерируемые логикой актора.

```ts
import { createActor } from 'xstate';
import { someMachine } from './someMachine';

const actor = createActor(someMachine);

actor.subscribe({
    next: (snapshot) => {
        // ...
    },
    // highlight-start
    error: (err) => {
        // Обработка ошибки здесь
        console.error(err);
    },
    // highlight-end
});

actor.start();
```

## Создатели логики актора {#actor-logic-creators}

Типы логики актора, которые вы можете создать из XState:

-   [Логика конечного автомата (`createMachine(...)`)](#createmachine)
-   [Логика промиса (`fromPromise(...)`)](#frompromise)
-   [Логика функции перехода (`fromTransition(...)`)](#fromtransition)
-   [Логика Observable (`fromObservable(...)`)](#fromobservable)
-   [Логика Event Observable (`fromEventObservable(...)`)](#fromeventobservable)
-   [Логика колбэка (`fromCallback(...)`)](#fromcallback)

### Возможности логики актора

|                                                      | Получение событий | Отправка событий | Порождение акторов | Input | Output |
| ---------------------------------------------------- | ----------------- | ---------------- | ------------------ | ----- | ------ |
| [Акторы конечных автоматов](state-machine-actors.md) | ✅                | ✅               | ✅                 | ✅    | ✅     |
| [Promise-акторы](promise-actors.md)                  | ❌                | ✅               | ❌                 | ✅    | ✅     |
| [Transition-акторы](transition-actors.md)            | ✅                | ✅               | ❌                 | ✅    | ❌     |
| [Observable-акторы](observable-actors.md)            | ❌                | ✅               | ❌                 | ✅    | ❌     |
| [Callback-акторы](callback-actors.md)                | ✅                | ✅               | ❌                 | ✅    | ❌     |

### Логика конечного автомата (`createMachine(...)`) {#createmachine}

Вы можете описать логику актора как [конечный автомат](machines.md). Акторы, созданные из логики актора конечного автомата, могут:

-   Получать события
-   Отправлять события другим акторам
-   Вызывать/порождать дочерних акторов
-   Генерировать снимки своего состояния
-   Выводить значение, когда автомат достигает финального состояния верхнего уровня

```ts
const toggleMachine = createMachine({
    id: 'toggle',
    initial: 'inactive',
    states: {
        inactive: {
            on: {
                toggle: 'inactive',
            },
        },
        active: {
            on: {
                toggle: 'active',
            },
        },
    },
});

const toggleActor = createActor(toggleMachine);

toggleActor.subscribe((snapshot) => {
    // snapshot — это состояние автомата
    console.log('state', snapshot.value);
    console.log('context', snapshot.context);
});
toggleActor.start();
// Выводит 'inactive'
toggleActor.send({ type: 'toggle' });
// Выводит 'active'
```

Узнайте больше об [акторах конечных автоматов](state-machine-actors.md).

### Логика промиса (`fromPromise(...)`) {#frompromise}

Логика promise-актора описывается асинхронным процессом, который разрешается или отклоняется через некоторое время. Акторы, созданные из логики промиса («promise-акторы»), могут:

-   Генерировать разрешённое значение промиса
-   Выводить разрешённое значение промиса

Отправка событий promise-акторам не будет иметь эффекта.

```ts
const promiseLogic = fromPromise(() => {
    return fetch('https://example.com/...').then((data) =>
        data.json()
    );
});

const promiseActor = createActor(promiseLogic);
promiseActor.subscribe((snapshot) => {
    console.log(snapshot);
});
promiseActor.start();
// => {
//   output: undefined,
//   status: 'active'
//   ...
// }

// После разрешения промиса
// => {
//   output: { ... },
//   status: 'done',
//   ...
// }
```

Узнайте больше о [promise-акторах](promise-actors.md).

### Логика функции перехода (`fromTransition(...)`) {#fromtransition}

Логика transition-актора описывается [функцией перехода](migration.md#use-actor-logic-creators-for-invokesrc-instead-of-functions), похожей на [редьюсер](cheatsheet.md#creating-transition-logic). Функции перехода принимают текущее `state` и полученный объект `event` в качестве аргументов и возвращают следующее состояние. Акторы, созданные из логики перехода («transition-акторы»), могут:

-   Получать события
-   Генерировать снимки своего состояния

```ts
const transitionLogic = fromTransition(
    (state, event) => {
        if (event.type === 'increment') {
            return {
                ...state,
                count: state.count + 1,
            };
        }
        return state;
    },
    { count: 0 }
);

const transitionActor = createActor(transitionLogic);
transitionActor.subscribe((snapshot) => {
    console.log(snapshot);
});
transitionActor.start();
// => {
//   status: 'active',
//   context: { count: 0 },
//   ...
// }

transitionActor.send({ type: 'increment' });
// => {
//   status: 'active',
//   context: { count: 1 },
//   ...
// }
```

Узнайте больше о [transition-акторах](transition-actors.md).

### Логика Observable (`fromObservable(...)`) {#fromobservable}

Логика observable-актора описывается [потоком наблюдаемых значений](#fromObservable). Акторы, созданные из логики observable («observable-акторы»), могут:

-   Генерировать снимки сгенерированного значения observable

Отправка событий observable-акторам не будет иметь эффекта.

```ts
import { interval } from 'rxjs';

const secondLogic = fromObservable(() => interval(1000));

const secondActor = createActor(secondLogic);

secondActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});

secondActor.start();
// Каждую секунду:
// Выводит 0
// Выводит 1
// Выводит 2
// ...
```

Узнайте больше об [observable-акторах](observable-actors.md).

### Логика Event Observable (`fromEventObservable(...)`) {#fromeventobservable}

Логика event observable-актора описывается потоком [объектов событий](transitions.md#event-objects). Акторы, созданные из логики event observable («event observable-акторы»), могут:

-   Неявно отправлять события родительскому актору
-   Генерировать снимки сгенерированных объектов событий

Отправка событий event observable-акторам не будет иметь эффекта.

```ts
import { setup, fromEventObservable } from 'xstate';
import { fromEvent } from 'rxjs';

const mouseClickLogic = fromEventObservable(
    () =>
        fromEvent(document.body, 'click') as Subscribable<
            EventObject
        >
);

const canvasMachine = setup({
    actors: {
        mouseClickLogic,
    },
}).createMachine({
    invoke: {
        // Будет отправлять события клика мыши актору canvas
        src: 'mouseClickLogic',
    },
});

const canvasActor = createActor(canvasMachine);
canvasActor.start();
```

Узнайте больше об [observable-акторах](observable-actors.md).

### Логика колбэка (`fromCallback(...)`) {#fromcallback}

Логика callback-актора описывается функцией колбэка, которая получает один объект-аргумент, включающий функцию `sendBack(event)` и функцию `receive(event => ...)`. Акторы, созданные из логики колбэка («callback-акторы»), могут:

-   Получать события через функцию `receive`
-   Отправлять события родительскому актору через функцию `sendBack`

```ts
const callbackLogic = fromCallback(
    ({ sendBack, receive }) => {
        let lockStatus = 'unlocked';

        const handler = (event) => {
            if (lockStatus === 'locked') {
                return;
            }
            sendBack(event);
        };

        receive((event) => {
            if (event.type === 'lock') {
                lockStatus = 'locked';
            } else if (event.type === 'unlock') {
                lockStatus = 'unlocked';
            }
        });

        document.body.addEventListener('click', handler);

        return () => {
            document.body.removeEventListener(
                'click',
                handler
            );
        };
    }
);
```

Callback-акторы немного отличаются от других акторов тем, что они не делают следующее:

-   Не работают с `onDone`
-   Не создают снимок с помощью `.getSnapshot()`
-   Не генерируют значения при использовании с `.subscribe()`

Вы можете использовать `sendBack` для сообщения о пойманных ошибках родительскому актору. Это особенно полезно для обработки отклонений промисов внутри функции колбэка, которые не будут перехвачены [`onError`](invoke.md#onerror).

Функции колбэка не могут быть `async` функциями. Но можно выполнить промис внутри функции колбэка.

```ts
import { setup, fromCallback } from 'xstate';

const someCallback = fromCallback(({ sendBack }) => {
    // highlight-start
    somePromise()
        .then((data) => sendBack({ type: 'done', data }))
        .catch((error) =>
            sendBack({ type: 'error', data: error })
        );
    // highlight-end

    return () => {
        /* функция очистки */
    };
});

const machine = setup({
    actors: {
        someCallback,
    },
}).createMachine({
    initial: 'running',
    states: {
        running: {
            invoke: {
                src: 'someCallback',
            },
            // highlight-start
            on: {
                error: {
                    actions: ({ event }) =>
                        console.error(event.data),
                },
            },
            // highlight-end
        },
    },
});
```

Узнайте больше о [callback-акторах](callback-actors.md).

## Акторы как промисы

Вы можете создать промис из любого актора, используя функцию `toPromise(actor)`. Промис разрешится с `.output` снимка актора, когда актор завершён (`snapshot.status === 'done'`), или отклонится с `.error` снимка актора, когда актор в ошибке (`snapshot.status === 'error'`).

```ts
import {
    createMachine,
    createActor,
    toPromise,
} from 'xstate';

const machine = createMachine({
    // ...
    states: {
        // ...
        done: { type: 'final' },
    },
    output: {
        count: 42,
    },
});

const actor = createActor(machine);
actor.start();

// highlight-start
// Создаёт промис, который разрешается с выводом актора
// или отклоняется с ошибкой актора
const output = await toPromise(actor);
// highlight-end

console.log(output);
// => { count: 42 }
```

Если актор уже завершён, промис разрешится с `snapshot.output` актора немедленно. Если актор уже в ошибке, промис отклонится с `snapshot.error` актора немедленно.

## Логика актора высшего порядка

Логика актора высшего порядка расширяет существующую логику актора дополнительной функциональностью. Например, вы можете создать логику актора, которая логирует или сохраняет состояние актора:

```ts
import { fromTransition, type AnyActorLogic } from 'xstate';

const toggleLogic = fromTransition((state, event) => {
  if (event.type === 'toggle') {
    return state === 'paused' ? 'playing' : 'paused';
  }

  return state;
}, 'paused');

// highlight-start
function withLogging<T extends AnyActorLogic>(actorLogic: T) {
  const enhancedLogic = {
    ...actorLogic,
    transition: (state, event, actorCtx) => {
      console.log('State:', state);
      return actorLogic.transition(state, event, actorCtx);
    },
  } satisfies T;

  return enhancedLogic;
}

const loggingToggleLogic = withLogging(toggleLogic);
// highlight-end
```

## Пользовательская логика актора

Пользовательская логика актора может быть определена с помощью объекта, реализующего интерфейс `ActorLogic`.

Например, вот пользовательский объект логики актора с функцией `transition`, которая работает как простой редьюсер:

```ts
import {
    createActor,
    EventObject,
    ActorLogic,
    Snapshot,
} from 'xstate';

const countLogic: ActorLogic<
    Snapshot<undefined> & { context: number },
    EventObject
> = {
    transition: (state, event) => {
        if (event.type === 'INC') {
            return {
                ...state,
                context: state.context + 1,
            };
        } else if (event.type === 'DEC') {
            return {
                ...state,
                context: state.context - 1,
            };
        }
        return state;
    },
    getInitialSnapshot: () => ({
        status: 'active',
        output: undefined,
        error: undefined,
        context: 0,
    }),
    getPersistedSnapshot: (s) => s,
};

const actor = createActor(countLogic);
actor.subscribe((state) => {
    console.log(state.context);
});
actor.start(); // => 0
actor.send({ type: 'INC' }); // => 1
actor.send({ type: 'INC' }); // => 2
```

Для дополнительных примеров см. реализации `ActorLogic` в исходном коде, например создатель логики актора `fromTransition`, или примеры в тестах.

## Пустые акторы

Актор, который ничего не делает и имеет только один сгенерированный снимок: `undefined`

В XState пустой актор — это актор, который ничего не делает и имеет только один сгенерированный снимок: `undefined`.

Это полезно для тестирования, например для заглушки актора, который ещё не реализован. Это также может быть полезно в интеграциях с фреймворками, таких как `@xstate/react`, где актор может быть ещё недоступен:

```ts
import { createEmptyActor, AnyActorRef } from 'xstate';
import { useSelector } from '@xstate/react';
const emptyActor = createEmptyActor();

function Component(props: { actor?: AnyActorRef }) {
    const data = useSelector(
        props.actor ?? emptyActor,
        (snapshot) => snapshot.context.data
    );

    // data равно `undefined`, если `props.actor` не определён
    // В противном случае это данные из актора

    // ...
}
```

## Акторы и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `actors` вашего автомата в свойстве `types.actors` конфигурации автомата.

```ts
const fetcher = fromPromise(
  async ({ input }: { input: { userId: string } }) => {
    const user = await fetchUser(input.userId);

    return user;
  },
);

const machine = setup({
  types: {
    children: {} as {
      fetch1: 'fetcher';
      fetch2: 'fetcher';
    }
  }
  // highlight-next-line
  actors: { fetcher }
}).createMachine({
  invoke: {
    // highlight-start
    src: 'fetchData', // строго типизировано
    id: 'fetch2', // строго типизировано
    onDone: {
      actions: ({ event }) => {
        event.output; // строго типизировано как { result: string }
      },
    },
    input: { userId: '42' }, // строго типизировано
    // highlight-end
  },
});
```

## Тестирование

Общая стратегия тестирования акторов — отправлять события и проверять, что актор достигает ожидаемого состояния, которое можно наблюдать либо:

-   Подписываясь на его сгенерированные снимки через `actor.subscribe(...)`
-   Или читая последний снимок через `actor.getSnapshot()`.

```ts
test('some actor', async () => {
    const actor = createActor(
        fromTransition(
            (state, event) => {
                if (event.type === 'inc') {
                    return { count: state.count + 1 };
                }
                return state;
            },
            { count: 0 }
        )
    );

    // Запуск актора
    actor.start();

    // Отправка событий
    actor.send({ type: 'inc' });
    actor.send({ type: 'inc' });
    actor.send({ type: 'inc' });

    // Проверка ожидаемого результата
    expect(actor.getSnapshot().context).toEqual({
        count: 3,
    });
});
```

## Шпаргалка по акторам

### Шпаргалка: создание актора

```ts
import { createActor } from 'xstate';
import { someActorLogic } from './someActorLogic.ts';

// Создание актора из логики актора
const actor = createActor(someActorLogic);

// Подписка на значения снимков актора и их логирование
actor.subscribe((snapshot) => {
    console.log(snapshot);
});

// Запуск системы акторов
actor.start();

// Теперь актор может получать события
actor.send({ type: 'someEvent' });

// Останавливает корневой актор, систему акторов и акторов в системе
actor.stop();
```

### Шпаргалка: логика конечного автомата

```ts
import { createMachine, createActor } from 'xstate';

const toggleMachine = createMachine({
    id: 'toggle',
    initial: 'inactive',
    states: {
        inactive: {},
        active: {},
    },
});

const toggleActor = createActor(toggleMachine);

toggleActor.subscribe((snapshot) => {
    // snapshot — это состояние автомата
    console.log('state', snapshot.value);
    console.log('context', snapshot.context);
});
toggleActor.start();
// Выводит 'inactive'
toggleActor.send({ type: 'toggle' });
// Выводит 'active'
```

### Шпаргалка: логика промиса

```ts
import { fromPromise, createActor } from 'xstate';

const promiseLogic = fromPromise(() => {
    return fetch('https://example.com/...').then((data) =>
        data.json()
    );
});

const promiseActor = createActor(promiseLogic);
promiseActor.subscribe((snapshot) => {
    console.log(snapshot);
});
promiseActor.start();
```

### Шпаргалка: логика функции перехода

```ts
import { fromTransition, createActor } from 'xstate';

const transitionLogic = fromTransition(
    (state, event) => {
        if (event.type === 'increment') {
            return {
                ...state,
                count: state.count + 1,
            };
        }
        return state;
    },
    { count: 0 }
);

const transitionActor = createActor(transitionLogic);
transitionActor.subscribe((snapshot) => {
    console.log(snapshot);
});
transitionActor.start();
// => {
//   status: 'active',
//   context: { count: 0 },
//   ...
// }

transitionActor.send({ type: 'increment' });
// => {
//   status: 'active',
//   context: { count: 1 },
//   ...
// }
```

### Шпаргалка: логика Observable

```ts
import { fromObservable, createActor } from 'xstate';
import { interval } from 'rxjs';

const secondLogic = fromObservable(() => interval(1000));

const secondActor = createActor(secondLogic);

secondActor.subscribe((snapshot) => {
    console.log(snapshot.context);
});

secondActor.start();
// Каждую секунду:
// Выводит 0
// Выводит 1
// Выводит 2
// ...
```

### Шпаргалка: логика Event Observable

```ts
import {
    setup,
    fromEventObservable,
    createActor,
} from 'xstate';
import { fromEvent } from 'rxjs';

const mouseClickLogic = fromEventObservable(
    () =>
        fromEvent(document.body, 'click') as Subscribable<
            EventObject
        >
);

const canvasMachine = setup({
    actors: {
        mouseClickLogic,
    },
}).createMachine({
    invoke: {
        // Будет отправлять события клика мыши актору canvas
        src: 'mouseClickLogic',
    },
});

const canvasActor = createActor(canvasMachine);
canvasActor.start();
```

### Шпаргалка: логика колбэка

```ts
import { fromCallback, createActor } from 'xstate';

const callbackLogic = fromCallback(
    ({ sendBack, receive }) => {
        let lockStatus = 'unlocked';

        const handler = (event) => {
            if (lockStatus === 'locked') {
                return;
            }
            sendBack(event);
        };

        receive((event) => {
            if (event.type === 'lock') {
                lockStatus = 'locked';
            } else if (event.type === 'unlock') {
                lockStatus = 'unlocked';
            }
        });

        document.body.addEventListener('click', handler);

        return () => {
            document.body.removeEventListener(
                'click',
                handler
            );
        };
    }
);
```
