---
title: XState
---

XState — это решение для управления состоянием и оркестрации для JavaScript и TypeScript приложений.

Он использует [событийно-ориентированное](transitions.md) программирование, [конечные автоматы, диаграммы состояний](state-machines-and-statecharts.md) и [модель акторов](actor-model.md) для обработки сложной логики предсказуемым, надёжным и визуальным способом. XState предоставляет мощный и гибкий способ управления состоянием приложений и рабочих процессов, позволяя разработчикам моделировать логику как акторы и конечные автоматы. Он хорошо интегрируется с React, Vue, Svelte и другими фреймворками и может использоваться на фронтенде, бэкенде или везде, где работает JavaScript.

!!!tip "Совет"

    Хотите узнать больше о конечных автоматах? [Читайте наше введение](state-machines-and-statecharts.md).

## Установка

XState доступен на [npm](https://www.npmjs.com/package/xstate):

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

## Создание простого автомата

```js
import { createMachine, assign, createActor } from 'xstate';

const countMachine = createMachine({
    context: {
        count: 0,
    },
    on: {
        INC: {
            actions: assign({
                count: ({ context }) => context.count + 1,
            }),
        },
        DEC: {
            actions: assign({
                count: ({ context }) => context.count - 1,
            }),
        },
        SET: {
            actions: assign({
                count: ({ event }) => event.value,
            }),
        },
    },
});

const countActor = createActor(countMachine).start();

countActor.subscribe((state) => {
    console.log(state.context.count);
});

countActor.send({ type: 'INC' });
// выводит 1
countActor.send({ type: 'DEC' });
// выводит 0
countActor.send({ type: 'SET', value: 10 });
// выводит 10
```

<iframe loading="lazy" src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?machineId=89e9d8f1-73d6-4dee-92bc-1796270e2f50&amp;mode=design&amp;colorMode=light" class="embed_rxbU" width="100%" height="500"></iframe>

[Больше примеров в шпаргалке](cheatsheet.md).

## Создание более сложного автомата

```js
import { createMachine, assign, createActor } from 'xstate';

const textMachine = createMachine({
    context: {
        committedValue: '',
        value: '',
    },
    initial: 'reading',
    states: {
        reading: {
            on: {
                'text.edit': { target: 'editing' },
            },
        },
        editing: {
            on: {
                'text.change': {
                    actions: assign({
                        value: ({ event }) => event.value,
                    }),
                },
                'text.commit': {
                    actions: assign({
                        committedValue: ({ context }) =>
                            context.value,
                    }),
                    target: 'reading',
                },
                'text.cancel': {
                    actions: assign({
                        value: ({ context }) =>
                            context.committedValue,
                    }),
                    target: 'reading',
                },
            },
        },
    },
});

const textActor = createActor(textMachine).start();

textActor.subscribe((state) => {
    console.log(state.context.value);
});

textActor.send({ type: 'text.edit' });
// выводит ''
textActor.send({ type: 'text.change', value: 'Hello' });
// выводит 'Hello'
textActor.send({ type: 'text.commit' });
// выводит 'Hello'
textActor.send({ type: 'text.edit' });
// выводит 'Hello'
textActor.send({
    type: 'text.change',
    value: 'Hello world',
});
// выводит 'Hello world'
textActor.send({ type: 'text.cancel' });
// выводит 'Hello'
```

<iframe loading="lazy" src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&amp;machineId=fa84c2d4-7c42-4f67-8bde-66f972133703&amp;colorMode=light" class="embed_rxbU" width="100%" height="400"></iframe>

## Скачать расширение XState для VS Code

!!!warning "Внимание"

    Расширение XState для VS Code пока не полностью поддерживает XState v5.

-   [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=statelyai.stately-vscode)
-   [Open VSX Registry](https://open-vsx.org/extension/statelyai/stately-vscode)

[Подробнее о наших инструментах для разработчиков](developer-tools.md).

## Пакеты

-   🤖 [xstate](https://github.com/statelyai/xstate/): Основная библиотека конечных автоматов и диаграмм состояний + акторы
-   📉 [@xstate/graph](https://github.com/statelyai/xstate/tree/main/packages/xstate-graph): Утилиты для обхода графов в XState
-   ⚛️ [@xstate/react](https://github.com/statelyai/xstate/tree/main/packages/xstate-react): React-хуки и утилиты для использования XState в React-приложениях
-   💚 [@xstate/vue](https://github.com/statelyai/xstate/tree/main/packages/xstate-vue): Vue composition-функции и утилиты для использования XState в Vue-приложениях
-   🎷 [@xstate/svelte](https://github.com/statelyai/xstate/tree/main/packages/xstate-svelte): Утилиты Svelte для использования XState в Svelte-приложениях
-   ✅ [@xstate/test](https://github.com/statelyai/xstate/tree/main/packages/xstate-test): Утилиты для тестирования на основе моделей (с использованием XState) для тестирования любого программного обеспечения
