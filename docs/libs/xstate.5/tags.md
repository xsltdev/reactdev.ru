---
title: Теги
---

Узлы состояний могут иметь **теги** — строковые термины, которые помогают группировать или категоризировать узел состояния. Например, вы можете указать, какие узлы состояний представляют состояния, в которых загружаются данные, используя тег "loading", и определить, содержит ли состояние эти помеченные узлы состояний с помощью `state.hasTag(tag)`:

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'prompt',
    states: {
        prompt: {
            tags: ['visible'],
            // ...
        },
        form: {
            tags: ['visible'],
            // ...
        },
        thanks: {
            tags: ['visible', 'confetti'],
            // ...
        },
        closed: {
            tags: ['hidden'],
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

console.log(feedbackActor.getSnapshot().hasTag('visible'));
// выводит true
```

## Теги и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `tags` вашей машины в свойстве `types.tags` настройки машины.

```ts
import { setup } from 'xstate';

const machine = setup({
    types: {
        tags: {} as 'pending' | 'success' | 'error',
    },
}).createMachine({
    // ...
    states: {
        loadingUser: {
            tags: ['pending'], // Строго типизировано
        },
    },
});

const actor = createActor(machine).start();

actor
    .getSnapshot()
    // Автодополнение
    .hasTag('pending');
```
