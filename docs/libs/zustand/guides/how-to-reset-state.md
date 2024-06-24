# Как сбросить состояние

Для возврата состояния к исходному значению можно использовать следующий шаблон.

```ts
import { create } from 'zustand';

// define types for state values and actions separately
type State = {
    salmon: number;
    tuna: number;
};

type Actions = {
    addSalmon: (qty: number) => void;
    addTuna: (qty: number) => void;
    reset: () => void;
};

// define the initial state
const initialState: State = {
    salmon: 0,
    tuna: 0,
};

// create store
const useSlice = create<State & Actions>()((set, get) => ({
    ...initialState,
    addSalmon: (qty: number) => {
        set({ salmon: get().salmon + qty });
    },
    addTuna: (qty: number) => {
        set({ tuna: get().tuna + qty });
    },
    reset: () => {
        set(initialState);
    },
}));
```

Сброс нескольких хранилищ одновременно

```ts
import { create as _create } from 'zustand';
import type { StateCreator } from 'zustand';

const storeResetFns = new Set<() => void>();

const resetAllStores = () => {
    storeResetFns.forEach((resetFn) => {
        resetFn();
    });
};

export const create = (<T extends unknown>() => {
    return (stateCreator: StateCreator<T>) => {
        const store = _create(stateCreator);
        const initialState = store.getState();
        storeResetFns.add(() => {
            store.setState(initialState, true);
        });
        return store;
    };
}) as typeof _create;
```

Сброс связанного хранилища с помощью шаблона Slices

```ts
import create from 'zustand';
import type { StateCreator } from 'zustand';

const sliceResetFns = new Set<() => void>();

export const resetAllSlices = () => {
    sliceResetFns.forEach((resetFn) => {
        resetFn();
    });
};

const initialBearState = { bears: 0 };

interface BearSlice {
    bears: number;
    addBear: () => void;
    eatFish: () => void;
}

const createBearSlice: StateCreator<
    BearSlice & FishSlice,
    [],
    [],
    BearSlice
> = (set) => {
    sliceResetFns.add(() => set(initialBearState));
    return {
        ...initialBearState,
        addBear: () =>
            set((state) => ({ bears: state.bears + 1 })),
        eatFish: () =>
            set((state) => ({ fishes: state.fishes - 1 })),
    };
};

const initialStateFish = { fishes: 0 };

interface FishSlice {
    fishes: number;
    addFish: () => void;
}

const createFishSlice: StateCreator<
    BearSlice & FishSlice,
    [],
    [],
    FishSlice
> = (set) => {
    sliceResetFns.add(() => set(initialStateFish));
    return {
        ...initialStateFish,
        addFish: () =>
            set((state) => ({ fishes: state.fishes + 1 })),
    };
};

const useBoundStore = create<BearSlice & FishSlice>()(
    (...a) => ({
        ...createBearSlice(...a),
        ...createFishSlice(...a),
    })
);

export default useBoundStore;
```

## CodeSandbox Demo

-   Basic: <https://codesandbox.io/s/zustand-how-to-reset-state-basic-demo-rrqyon>
-   Advanced: <https://codesandbox.io/s/zustand-how-to-reset-state-advanced-demo-gtu0qe>
-   Immer: <https://codesandbox.io/s/how-to-reset-state-advance-immer-demo-nyet3f>

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/how-to-reset-state></small>
