# Промежуточное ПО Immer

Промежуточное ПО [Immer](https://github.com/immerjs/immer) позволяет использовать неизменяемое состояние более удобным способом. Кроме того, с помощью Immer можно упростить работу с неизменяемыми структурами данных в Zustand.

## Установка

Чтобы использовать промежуточное ПО Immer в Zustand, вам нужно установить Immer как прямую зависимость.

```bash
npm install immer
```

## Использование

(Обратите внимание на дополнительные круглые скобки после параметра type, как указано в [Typescript Guide](../guides/typescript.md)).

Обновление простых состояний

```ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

type State = {
    count: number;
};

type Actions = {
    increment: (qty: number) => void;
    decrement: (qty: number) => void;
};

export const useCountStore = create<State & Actions>()(
    immer((set) => ({
        count: 0,
        increment: (qty: number) =>
            set((state) => {
                state.count += qty;
            }),
        decrement: (qty: number) =>
            set((state) => {
                state.count -= qty;
            }),
    }))
);
```

Обновление сложных состояний

```ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface Todo {
    id: string;
    title: string;
    done: boolean;
}

type State = {
    todos: Record<string, Todo>;
};

type Actions = {
    toggleTodo: (todoId: string) => void;
};

export const useTodoStore = create<State & Actions>()(
    immer((set) => ({
        todos: {
            '82471c5f-4207-4b1d-abcb-b98547e01a3e': {
                id: '82471c5f-4207-4b1d-abcb-b98547e01a3e',
                title: 'Learn Zustand',
                done: false,
            },
            '354ee16c-bfdd-44d3-afa9-e93679bda367': {
                id: '354ee16c-bfdd-44d3-afa9-e93679bda367',
                title: 'Learn Jotai',
                done: false,
            },
            '771c85c5-46ea-4a11-8fed-36cc2c7be344': {
                id: '771c85c5-46ea-4a11-8fed-36cc2c7be344',
                title: 'Learn Valtio',
                done: false,
            },
            '363a4bac-083f-47f7-a0a2-aeeee153a99c': {
                id: '363a4bac-083f-47f7-a0a2-aeeee153a99c',
                title: 'Learn Signals',
                done: false,
            },
        },
        toggleTodo: (todoId: string) =>
            set((state) => {
                state.todos[todoId].done = !state.todos[
                    todoId
                ].done;
            }),
    }))
);
```

## Gotchas

В этом разделе вы найдете некоторые моменты, о которых следует помнить при использовании Zustand с Immer.

### Мои подписки не вызываются

Если вы используете Immer, убедитесь, что вы действительно следуете [правилам Immer](https://immerjs.github.io/immer/pitfalls).

Например, вы должны добавить `[immerable] = true`, чтобы [объекты классов](https://immerjs.github.io/immer/complex-objects) работали. Если вы этого не сделаете, Immer все равно будет мутировать объект, но не как прокси, поэтому он также обновит текущее состояние. Zustand проверяет, действительно ли состояние изменилось, поэтому, поскольку и текущее состояние, и следующее состояние равны (если вы не сделаете это правильно), Zustand пропустит вызов подписки.

## CodeSandbox Demo

-   [Basic](https://codesandbox.io/p/sandbox/zustand-updating-draft-states-basic-demo-forked-96mkdw),
-   [Advanced](https://codesandbox.io/p/sandbox/zustand-updating-draft-states-advanced-demo-forked-phkzzg).

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/integrations/immer-middleware></small>
