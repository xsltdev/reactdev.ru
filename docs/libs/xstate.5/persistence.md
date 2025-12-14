---
title: Персистентность
---

[Акторы](actors.md) могут сохранять своё внутреннее состояние и восстанавливать его позже. **Персистентность** означает сохранение состояния актора в постоянное хранилище, такое как localStorage или база данных. **Восстановление** означает восстановление состояния актора из постоянного хранилища.

Во фронтенд-приложениях персистентность полезна для сохранения состояния между перезагрузками браузера. В бэкенд-приложениях персистентность позволяет рабочим процессам охватывать несколько запросов, переживать перезапуски сервисов, быть отказоустойчивыми, представлять длительные процессы и быть аудируемыми и отслеживаемыми.

В XState вы можете получить снимок (состояние) для сохранения через `actor.getPersistedSnapshot()` и восстановить его через `createActor(behavior, { snapshot: restoredState }).start()`:

```ts
const feedbackActor = createActor(feedbackMachine).start();

// Получение состояния для сохранения
const persistedState = feedbackActor.getPersistedSnapshot();

// Сохранение состояния
localStorage.setItem(
    'feedback',
    JSON.stringify(persistedState)
);

// Восстановление состояния
const restoredState = JSON.parse(
    localStorage.getItem('feedback')
);

const restoredFeedbackActor = createActor(feedbackMachine, {
    snapshot: restoredState,
}).start();
```

## Сохранение состояния

Вы можете получить состояние для сохранения через `actor.getPersistedSnapshot()`:

```ts
const feedbackActor = createActor(feedbackMachine).start();

// Получение состояния для сохранения
const persistedState = feedbackActor.getPersistedSnapshot();
```

Внутреннее состояние можно сохранить от любого актора, не только от машин. Обратите внимание, что сохранённое состояние — это _не_ то же самое, что снимок из `actor.getSnapshot()`; сохранённое состояние представляет внутреннее состояние актора, тогда как снимки представляют последнее эмитированное значение актора:

```ts
const promiseActor = fromPromise(() => Promise.resolve(42));

// Получение последнего эмитированного значения
const snapshot = promiseActor.getSnapshot();
console.log(snapshot);
// выводит 42

// Получение сохранённого состояния
const persistedState = promiseActor.getPersistedSnapshot();
console.log(persistedState);
// выводит { status: 'done', data: 42 }
```

## Восстановление состояния

Вы можете восстановить актор в сохранённое состояние, передав сохранённое состояние в опцию `state` второго аргумента `createActor(logic, { snapshot: restoredState })`:

```ts
// Получение сохранённого состояния
const restoredState = JSON.parse(
    localStorage.getItem('feedback')
);

// Восстановление состояния
const feedbackActor = createActor(feedbackMachine, {
    snapshot: restoredState,
});

feedbackActor.start();
```

Действия из акторов машин _не_ будут выполнены повторно, потому что предполагается, что они уже были выполнены. Однако вызовы (invocations) будут перезапущены, а порождённые (spawned) акторы будут восстановлены рекурсивно.

## Глубокая персистентность

Сохранение и восстановление состояния из акторов машин является глубоким; все [вызванные](invoke.md) и [порождённые акторы](spawn.md) будут сохранены и восстановлены рекурсивно.

```ts
const feedbackMachine = createMachine({
    // ...
    states: {
        form: {
            invoke: {
                id: 'form',
                src: formMachine,
            },
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

// Сохранение состояния
const persistedState = feedbackActor.getPersistedSnapshot();
localStorage.setItem(
    'feedback',
    JSON.stringify(persistedState)
);

//  ...

// Восстановление состояния
const restoredState = JSON.parse(
    localStorage.getItem('feedback')
);

const restoredFeedbackActor = createActor(feedbackMachine, {
    snapshot: restoredState,
}).start();
// Восстановит как feedbackActor, так и вызванный form-актор
// в их сохранённых состояниях
```

## Сохранение значений машины состояний

Если вы хотите сохранить только конечное состояние `value` (и опционально `context`) актора машины состояний, вы можете использовать метод `machine.resolveState(...)`:

```ts
import { someMachine } from './someMachine';

const restoredStateValue = localStorage.getItem(
    'someState'
);
// Предположим, что это "pending"

const resolvedState = someMachine.resolveState({
    value: restoredStateValue,
    // context: { ... }
});

// Восстановление актора
const restoredActor = createActor(someMachine, {
    snapshot: resolvedState,
});

restoredActor.start();
```

## Источник событий (Event sourcing) {#event-sourcing}

Альтернативой сохранению состояния является **источник событий** (event sourcing) — способ восстановления состояния актора путём воспроизведения [событий](transitions.md), которые привели к этому состоянию. Источник событий может быть более надёжным, чем сохранение состояния, потому что он менее подвержен [несовместимому состоянию](#caveats), а также позволяет воспроизводить действия.

Один из способов реализовать источник событий — сохранять события по мере их возникновения с помощью [API инспекции](inspection.md), а затем воспроизводить их для восстановления состояния актора:

```ts
const events = [];

const someActor = createActor(someMachine, {
    // Инспектирование и сохранение событий
    inspect: (inspectionEvent) => {
        if (inspectionEvent.type === '@xstate.event') {
            const event = inspectionEvent.event;

            // Прослушивать только события, отправленные корневому актору
            if (inspectionEvent.actorRef !== someActor) {
                return;
            }

            events.push(event);
        }
    },
});

someActor.start();

// ...

// Предполагая, что события где-то сохранены, например в localStorage,
// вы можете воспроизвести их для восстановления состояния актора

const restoredActor = createActor(someMachine);
restoredActor.start();

for (const event of events) {
    // Воспроизведение событий
    restoredActor.send(event);
}
```

## Предостережения {#caveats}

Есть некоторые предостережения относительно сохранения и восстановления состояния, о которых вам следует знать:

-   Несовместимое состояние: если машина или логика актора изменяется, восстановленное состояние может быть несовместимо с новой логикой.
-   Воспроизведение действий: действия, которые уже были выполнены, не будут выполнены повторно. [Источник событий](#event-sourcing) предпочтительнее для этого случая.
-   Сериализация: состояние должно быть сериализуемым, то есть JSON-сериализуемым. Это означает, что вы не можете сохранять функции, классы или другие несериализуемые значения.

## Шпаргалка по персистентности

### Шпаргалка: сохранение состояния

```ts
const persistedState = actor.getPersistedSnapshot();
```

### Шпаргалка: восстановление состояния

```ts
const restoredState = JSON.parse(
    localStorage.getItem('feedback')
);

const restoredActor = createActor(actorMachine, {
    snapshot: restoredState,
}).start();
```
