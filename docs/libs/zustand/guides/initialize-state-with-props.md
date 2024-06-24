# Инициализируйте состояние с помощью свойств

В случаях, когда требуется [внедрение зависимостей](https://ru.wikipedia.org/wiki/Внедрение_зависимости), например, когда хранилище должно быть инициализировано реквизитами компонента, рекомендуется использовать ванильное хранилище с React.context.

## Создайте хранилище с помощью `createStore`

```ts
import { createStore } from 'zustand';

interface BearProps {
    bears: number;
}

interface BearState extends BearProps {
    addBear: () => void;
}

type BearStore = ReturnType<typeof createBearStore>;

const createBearStore = (
    initProps?: Partial<BearProps>
) => {
    const DEFAULT_PROPS: BearProps = {
        bears: 0,
    };
    return createStore<BearState>()((set) => ({
        ...DEFAULT_PROPS,
        ...initProps,
        addBear: () =>
            set((state) => ({ bears: ++state.bears })),
    }));
};
```

## Создание контекста с помощью `React.createContext`

```ts
import { createContext } from 'react';

export const BearContext = createContext<BearStore | null>(
    null
);
```

## Базовое использование компонентов

```tsx
// Provider implementation
import { useRef } from 'react';

function App() {
    const store = useRef(createBearStore()).current;
    return (
        <BearContext.Provider value={store}>
            <BasicConsumer />
        </BearContext.Provider>
    );
}
```

---

```tsx
// Consumer component
import { useContext } from 'react';
import { useStore } from 'zustand';

function BasicConsumer() {
    const store = useContext(BearContext);
    if (!store)
        throw new Error(
            'Missing BearContext.Provider in the tree'
        );
    const bears = useStore(store, (s) => s.bears);
    const addBear = useStore(store, (s) => s.addBear);
    return (
        <>
            <div>{bears} Bears.</div>
            <button onClick={addBear}>Add bear</button>
        </>
    );
}
```

## Общие шаблоны

### Обертывание поставщика контекста

```tsx
// Provider wrapper
import { useRef } from 'react';

type BearProviderProps = React.PropsWithChildren<BearProps>;

function BearProvider({
    children,
    ...props
}: BearProviderProps) {
    const storeRef = useRef<BearStore>();
    if (!storeRef.current) {
        storeRef.current = createBearStore(props);
    }
    return (
        <BearContext.Provider value={storeRef.current}>
            {children}
        </BearContext.Provider>
    );
}
```

### Извлечение контекстной логики в пользовательский хук

```tsx
// Mimic the hook returned by `create`
import { useContext } from 'react';
import { useStore } from 'zustand';

function useBearContext<T>(
    selector: (state: BearState) => T
): T {
    const store = useContext(BearContext);
    if (!store)
        throw new Error(
            'Missing BearContext.Provider in the tree'
        );
    return useStore(store, selector);
}
```

---

```tsx
// Consumer usage of the custom hook
function CommonConsumer() {
    const bears = useBearContext((s) => s.bears);
    const addBear = useBearContext((s) => s.addBear);
    return (
        <>
            <div>{bears} Bears.</div>
            <button onClick={addBear}>Add bear</button>
        </>
    );
}
```

### По желанию можно использовать пользовательскую функцию равенства

```tsx
// Allow custom equality function by using useStoreWithEqualityFn instead of useStore
import { useContext } from 'react';
import { useStoreWithEqualityFn } from 'zustand/traditional';

function useBearContext<T>(
    selector: (state: BearState) => T,
    equalityFn?: (left: T, right: T) => boolean
): T {
    const store = useContext(BearContext);
    if (!store)
        throw new Error(
            'Missing BearContext.Provider in the tree'
        );
    return useStoreWithEqualityFn(
        store,
        selector,
        equalityFn
    );
}
```

### Полный пример

```tsx
// Provider wrapper & custom hook consumer
function App2() {
    return (
        <BearProvider bears={2}>
            <HookConsumer />
        </BearProvider>
    );
}
```

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/initialize-state-with-props></small>
