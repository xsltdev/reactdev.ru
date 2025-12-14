---
title: 'Системы'
---

Система акторов — это коллекция акторов, которые могут взаимодействовать друг с другом. Акторы могут вызывать/порождать других акторов, что формирует естественную иерархию акторов, принадлежащих одной системе.

В XState система неявно создаётся из корневого актора, который возвращается из `createActor(machine).start()`. К системе можно получить доступ через свойство `actor.system` акторов и через деструктурированное свойство `{ system }` в действиях конечного автомата:

```ts
import { createMachine, createActor } from 'xstate';

const machine = createMachine({
    // highlight-next-line
    entry: ({ system }) => {
        // ...
    },
});

const actor = createActor(machine).start();
// highlight-next-line
actor.system;
```

Корню системы также можно явно назначить `systemId` в функции `createActor(...)`:

```ts
import { createActor } from 'xstate';

const actor = createActor(machine, {
    systemId: 'root-id',
});

actor.start();
```

Это полезно для того, чтобы акторы в системе могли отправлять события корневому актору.

## Регистрация акторов

Акторы могут быть зарегистрированы в системе, чтобы любой другой актор в системе мог получить ссылку на него.

Вызванные акторы регистрируются с системным `systemId` в объекте `invoke`:

```ts
import { createMachine, createActor, sendTo } from 'xstate';

const formMachine = createMachine({
    // ...
    on: {
        submit: {
            // highlight-next-line
            actions: sendTo(
                ({ system }) => system.get('notifier'),
                {
                    type: 'notify',
                    message: 'Форма отправлена!',
                }
            ),
        },
    },
});

const feedbackMachine = createMachine({
    invoke: {
        // highlight-next-line
        systemId: 'formMachine',
        src: formMachine,
    },
    // ...
    states: {
        // ...
        form: {
            invoke: formMachine,
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();
```

Порождённые акторы регистрируются с системным `systemId` во втором аргументе функции `spawn`:

```ts
import { createMachine, createActor, assign } from 'xstate';

const todoMachine = createMachine({
    // ...
});

const todosMachine = createMachine({
    // ...
    on: {
        'todo.add': {
            actions: assign({
                todos: ({ context, spawn }) => {
                    const newTodo = spawn(todoMachine, {
                        // highlight-next-line
                        systemId: `todo-${context.todos.length}`,
                    });

                    return context.todos.concat(newTodo);
                },
            }),
        },
    },
});
```

## Коммуникация акторов

Вы также можете получить ссылку на конкретного актора из системы, используя `system.get('actorId')`:

## Остановка системы

-   Остановка из корневого актора: `actor.stop()`
-   Невозможно остановить из акторов-потомков
    -   Будет выведено предупреждение

## Системы и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

-   `invoke.systemId`
-   `spawn(thing, { systemId })`
-   `system.get('actorId')`
-   `rootActor.stop()`

## Шпаргалка по системам

### Шпаргалка: система акторов

```ts
import { createMachine, createActor } from 'xstate';

const machine = createMachine({
    // highlight-next-line
    entry: ({ system }) => {
        // ...
    },
});

const actor = createActor(machine).start();
// highlight-next-line
actor.system;
```

### Шпаргалка: явное назначение `systemId`

```ts
import { createActor } from 'xstate';

const actor = createActor(machine, {
    // highlight-next-line
    systemId: 'root-id',
});

actor.start();
```

### Шпаргалка: регистрация вызванного актора в системе

```ts
import { createMachine, createActor, sendTo } from 'xstate';

const formMachine = createMachine({
    // ...
    on: {
        submit: {
            // highlight-next-line
            actions: sendTo(
                ({ system }) => system.get('notifier'),
                {
                    type: 'notify',
                    message: 'Форма отправлена!',
                }
            ),
        },
    },
});

const feedbackMachine = createMachine({
    invoke: {
        // highlight-next-line
        systemId: 'formMachine',
        src: formMachine,
    },
    // ...
    states: {
        // ...
        form: {
            invoke: formMachine,
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();
```

### Шпаргалка: регистрация порождённого актора в системе

```ts
import { createMachine, createActor, assign } from 'xstate';

const todoMachine = createMachine({
    // ...
});

const todosMachine = createMachine({
    // ...
    on: {
        'todo.add': {
            actions: assign({
                todos: ({ context, spawn }) => {
                    const newTodo = spawn(todoMachine, {
                        // highlight-next-line
                        systemId: `todo-${context.todos.length}`,
                    });

                    return context.todos.concat(newTodo);
                },
            }),
        },
    },
});
```
