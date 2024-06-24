---
description: Как Zustand выглядит в сравнении с аналогичными библиотеками
---

# Сравнение

Zustand - одна из многих библиотек управления состояниями для React. На этой странице мы рассмотрим Zustand в сравнении с некоторыми из этих библиотек, включая Redux, Valtio, Jotai и Recoil.

У каждой библиотеки есть свои сильные и слабые стороны, и мы сравним ключевые различия и сходства между ними.

## Redux

## Модель состояний (против Redux)

Концептуально Zustand и Redux довольно похожи, обе основаны на неизменяемой модели состояний. Однако Redux требует, чтобы ваше приложение было обернуто в контекстные провайдеры, а Zustand - нет.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    increment: (qty: number) => void;
    decrement: (qty: number) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    increment: (qty: number) =>
        set((state) => ({ count: state.count + qty })),
    decrement: (qty: number) =>
        set((state) => ({ count: state.count - qty })),
}));
```

---

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    increment: (qty: number) => void;
    decrement: (qty: number) => void;
};

type Action = {
    type: keyof Actions;
    qty: number;
};

const countReducer = (state: State, action: Action) => {
    switch (action.type) {
        case 'increment':
            return { count: state.count + action.qty };
        case 'decrement':
            return { count: state.count - action.qty };
        default:
            return state;
    }
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    dispatch: (action: Action) =>
        set((state) => countReducer(state, action)),
}));
```

**Redux**

```ts
import { createStore } from 'redux';
import { useSelector, useDispatch } from 'react-redux';

type State = {
    count: number;
};

type Action = {
    type: 'increment' | 'decrement';
    qty: number;
};

const countReducer = (state: State, action: Action) => {
    switch (action.type) {
        case 'increment':
            return { count: state.count + action.qty };
        case 'decrement':
            return { count: state.count - action.qty };
        default:
            return state;
    }
};

const countStore = createStore(countReducer);
```

---

```ts
import {
    createSlice,
    configureStore,
} from '@reduxjs/toolkit';

const countSlice = createSlice({
    name: 'count',
    initialState: { value: 0 },
    reducers: {
        incremented: (state, qty: number) => {
            // Redux Toolkit does not mutate the state, it uses the Immer library
            // behind scenes, allowing us to have something called "draft state".
            state.value += qty;
        },
        decremented: (state, qty: number) => {
            state.value -= qty;
        },
    },
});

const countStore = configureStore({
    reducer: countSlice.reducer,
});
```

### Оптимизация рендеринга (в сравнении с Redux)

Когда дело доходит до оптимизации рендеринга в вашем приложении, между Zustand и Redux нет существенных различий в подходах. В обеих библиотеках рекомендуется вручную применять оптимизацию рендеринга с помощью селекторов.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    increment: (qty: number) => void;
    decrement: (qty: number) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    increment: (qty: number) =>
        set((state) => ({ count: state.count + qty })),
    decrement: (qty: number) =>
        set((state) => ({ count: state.count - qty })),
}));

const Component = () => {
    const count = useCountStore((state) => state.count);
    const increment = useCountStore(
        (state) => state.increment
    );
    const decrement = useCountStore(
        (state) => state.decrement
    );
    // ...
};
```

**Redux**

```ts
import { createStore } from 'redux';
import { useSelector, useDispatch } from 'react-redux';

type State = {
    count: number;
};

type Action = {
    type: 'increment' | 'decrement';
    qty: number;
};

const countReducer = (state: State, action: Action) => {
    switch (action.type) {
        case 'increment':
            return { count: state.count + action.qty };
        case 'decrement':
            return { count: state.count - action.qty };
        default:
            return state;
    }
};

const countStore = createStore(countReducer);

const Component = () => {
    const count = useSelector((state) => state.count);
    const dispatch = useDispatch();
    // ...
};
```

---

```ts
import { useSelector } from 'react-redux';
import type { TypedUseSelectorHook } from 'react-redux';
import {
    createSlice,
    configureStore,
} from '@reduxjs/toolkit';

const countSlice = createSlice({
    name: 'count',
    initialState: { value: 0 },
    reducers: {
        incremented: (state, qty: number) => {
            // Redux Toolkit does not mutate the state, it uses the Immer library
            // behind scenes, allowing us to have something called "draft state".
            state.value += qty;
        },
        decremented: (state, qty: number) => {
            state.value -= qty;
        },
    },
});

const countStore = configureStore({
    reducer: countSlice.reducer,
});

const useAppSelector: TypedUseSelectorHook<typeof countStore.getState> = useSelector;

const useAppDispatch: () => typeof countStore.dispatch = useDispatch;

const Component = () => {
    const count = useAppSelector(
        (state) => state.count.value
    );
    const dispatch = useAppDispatch();
    // ...
};
```

## Valtio

### Модель состояний (в сравнении с Valtio)

Zustand и Valtio принципиально по-разному подходят к управлению состояниями. Zustand основан на **неизменяемой** модели состояний, а Valtio - на **изменяемой** модели состояний.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    obj: { count: number };
};

const store = create<State>(() => ({ obj: { count: 0 } }));

store.setState((prev) => ({
    obj: { count: prev.obj.count + 1 },
}));
```

**Valtio**

```ts
import { proxy } from 'valtio';

const state = proxy({ obj: { count: 0 } });

state.obj.count += 1;
```

### Оптимизация рендеринга (в сравнении с Valtio)

Еще одно различие между Zustand и Valtio заключается в том, что Valtio оптимизирует рендеринг через доступ к свойствам. Однако в Zustand рекомендуется вручную применять оптимизацию рендеринга с помощью селекторов.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

const useCountStore = create<State>(() => ({
    count: 0,
}));

const Component = () => {
    const count = useCountStore((state) => state.count);
    // ...
};
```

**Valtio**

```ts
import { proxy, useSnapshot } from 'valtio';

const state = proxy({
    count: 0,
});

const Component = () => {
    const { count } = useSnapshot(state);
    // ...
};
```

## Jotai

### Модель состояния (в сравнении с Jotai)

Между Zustand и Jotai есть два основных различия. Во-первых, Zustand - это единое хранилище, в то время как Jotai состоит из примитивных атомов, которые можно компоновать друг с другом. Во-вторых, хранилище Zustand - это внешнее хранилище, что делает его более подходящим, когда требуется доступ за пределами React.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    updateCount: (
        countCallback: (
            count: State['count']
        ) => State['count']
    ) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    updateCount: (countCallback) =>
        set((state) => ({
            count: countCallback(state.count),
        })),
}));
```

**Jotai**

```ts
import { atom } from 'jotai';

const countAtom = atom<number>(0);
```

### Оптимизация рендеринга (в сравнении с Jotai)

В Jotai оптимизация рендеринга достигается за счет зависимости от атомов. Однако в Zustand рекомендуется вручную применять оптимизацию рендеринга с помощью селекторов.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    updateCount: (
        countCallback: (
            count: State['count']
        ) => State['count']
    ) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    updateCount: (countCallback) =>
        set((state) => ({
            count: countCallback(state.count),
        })),
}));

const Component = () => {
    const count = useCountStore((state) => state.count);
    const updateCount = useCountStore(
        (state) => state.updateCount
    );
    // ...
};
```

**Jotai**

```ts
import { atom, useAtom } from 'jotai';

const countAtom = atom<number>(0);

const Component = () => {
    const [count, updateCount] = useAtom(countAtom);
    // ...
};
```

## Recoil

### Модель состояния (в сравнении с Recoil)

Разница между Zustand и Recoil аналогична разнице между Zustand и Jotai. Recoil зависит от ключей строк атомов вместо ссылочных идентичностей объектов атомов. Кроме того, Recoil необходимо обернуть ваше приложение в контекстный провайдер.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    setCount: (
        countCallback: (
            count: State['count']
        ) => State['count']
    ) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    setCount: (countCallback) =>
        set((state) => ({
            count: countCallback(state.count),
        })),
}));
```

**Recoil**

```ts
import { atom } from 'recoil';

const count = atom({
    key: 'count',
    default: 0,
});
```

### Оптимизация рендеринга (в сравнении с Recoil)

Как и в предыдущих сравнениях оптимизаций, Recoil оптимизирует рендеринг через зависимость от атомов. В то время как в случае с Zustand рекомендуется вручную применять оптимизацию рендеринга с помощью селекторов.

**Zustand**

```ts
import { create } from 'zustand';

type State = {
    count: number;
};

type Actions = {
    setCount: (
        countCallback: (
            count: State['count']
        ) => State['count']
    ) => void;
};

const useCountStore = create<State & Actions>((set) => ({
    count: 0,
    setCount: (countCallback) =>
        set((state) => ({
            count: countCallback(state.count),
        })),
}));

const Component = () => {
    const count = useCountStore((state) => state.count);
    const setCount = useCountStore(
        (state) => state.setCount
    );
    // ...
};
```

**Recoil**

```ts
import { atom, useRecoilState } from 'recoil';

const countAtom = atom({
    key: 'count',
    default: 0,
});

const Component = () => {
    const [count, setCount] = useRecoilState(countAtom);
    // ...
};
```

## Тренд загрузок Npm

-   [Npm Тренд загрузок библиотек управления состоянием для React](https://npm-stat.com/charts.html?package=zustand&package=jotai&package=valtio&package=%40reduxjs%2Ftoolkit&package=recoil)

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/getting-started/comparison></small>
