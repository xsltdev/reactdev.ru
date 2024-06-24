---
description: Автоматическая генерация селекторов
---

# Автоматическая генерация селекторов

Мы рекомендуем использовать селекторы при использовании свойств или действий из хранилища. Вы можете получить доступ к значениям из хранилища следующим образом:

```typescript
const bears = useBearStore((state) => state.bears);
```

Однако их написание может быть утомительным. Если это так, вы можете автоматически генерировать селекторы.

## создайте следующую функцию: `createSelectors`

```typescript
import { StoreApi, UseBoundStore } from 'zustand';

type WithSelectors<S> = S extends {
    getState: () => infer T;
}
    ? S & { use: { [K in keyof T]: () => T[K] } }
    : never;

const createSelectors = <
    S extends UseBoundStore<StoreApi<object>>
>(
    _store: S
) => {
    let store = _store as WithSelectors<typeof _store>;
    store.use = {};
    for (let k of Object.keys(store.getState())) {
        (store.use as any)[k] = () =>
            store((s) => s[k as keyof typeof s]);
    }

    return store;
};
```

Если у вас есть такое хранилище:

```typescript
interface BearState {
    bears: number;
    increase: (by: number) => void;
    increment: () => void;
}

const useBearStoreBase = create<BearState>()((set) => ({
    bears: 0,
    increase: (by) =>
        set((state) => ({ bears: state.bears + by })),
    increment: () =>
        set((state) => ({ bears: state.bears + 1 })),
}));
```

Примените эту функцию к своему хранилищу:

```typescript
const useBearStore = createSelectors(useBearStoreBase);
```

Теперь селекторы генерируются автоматически, и вы можете обращаться к ним напрямую:

```typescript
// get the property
const bears = useBearStore.use.bears();

// get the action
const increment = useBearStore.use.increment();
```

## Ванильное хранилище

Если вы используете ванильное хранилище, воспользуйтесь следующей функцией `createSelectors`:

```typescript
import { StoreApi, useStore } from 'zustand';

type WithSelectors<S> = S extends {
    getState: () => infer T;
}
    ? S & { use: { [K in keyof T]: () => T[K] } }
    : never;

const createSelectors = <S extends StoreApi<object>>(
    _store: S
) => {
    const store = _store as WithSelectors<typeof _store>;
    store.use = {};
    for (const k of Object.keys(store.getState())) {
        (store.use as any)[k] = () =>
            useStore(_store, (s) => s[k as keyof typeof s]);
    }

    return store;
};
```

Использование такое же, как и в хранилище React. Если у вас есть такое хранилище:

```typescript
import { createStore } from 'zustand';

interface BearState {
    bears: number;
    increase: (by: number) => void;
    increment: () => void;
}

const store = createStore<BearState>((set) => ({
    bears: 0,
    increase: (by) =>
        set((state) => ({ bears: state.bears + by })),
    increment: () =>
        set((state) => ({ bears: state.bears + 1 })),
}));
```

Примените эту функцию к своему хранилищу:

```typescript
const useBearStore = createSelectors(store);
```

Теперь селекторы генерируются автоматически, и вы можете обращаться к ним напрямую:

```typescript
// get the property
const bears = useBearStore.use.bears();

// get the action
const increment = useBearStore.use.increment();
```

## Живая демонстрация

Рабочий пример этого можно найти в [Code Sandbox](https://codesandbox.io/s/zustand-auto-generate-selectors-forked-rl8v5e?file=/src/selectors.ts).

## Библиотеки сторонних разработчиков

-   [auto-zustand-selectors-hook](https://github.com/Albert-Gao/auto-zustand-selectors-hook)
-   [react-hooks-global-state](https://github.com/dai-shi/react-hooks-global-state)
-   [zustood](https://github.com/udecode/zustood)
-   [@davstack/store](https://www.npmjs.com/package/@davstack/store)

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/auto-generating-selectors></small>
