# Slices Pattern

## Разбивка хранилища на более мелкие части

По мере добавления новых функций ваше хранилище может становиться все больше и больше, и поддерживать его становится все сложнее.

Для достижения модульности вы можете разделить ваше основное хранилище на более мелкие отдельные магазины. В Zustand это делается очень просто!

Первое отдельное хранилище:

```js
export const createFishSlice = (set) => ({
    fishes: 0,
    addFish: () =>
        set((state) => ({ fishes: state.fishes + 1 })),
});
```

Еще одно индивидуальное хранилище:

```js
export const createBearSlice = (set) => ({
    bears: 0,
    addBear: () =>
        set((state) => ({ bears: state.bears + 1 })),
    eatFish: () =>
        set((state) => ({ fishes: state.fishes - 1 })),
});
```

Теперь вы можете объединить оба хранилища в **одно ограниченное хранилище**:

```js
import { create } from 'zustand';
import { createBearSlice } from './bearSlice';
import { createFishSlice } from './fishSlice';

export const useBoundStore = create((...a) => ({
    ...createBearSlice(...a),
    ...createFishSlice(...a),
}));
```

### Использование в компоненте React

```jsx
import { useBoundStore } from './stores/useBoundStore';

function App() {
    const bears = useBoundStore((state) => state.bears);
    const fishes = useBoundStore((state) => state.fishes);
    const addBear = useBoundStore((state) => state.addBear);
    return (
        <div>
            <h2>Number of bears: {bears}</h2>
            <h2>Number of fishes: {fishes}</h2>
            <button onClick={() => addBear()}>
                Add a bear
            </button>
        </div>
    );
}

export default App;
```

### Обновление нескольких хранилищ

В одной функции можно обновить несколько хранилищ одновременно.

```js
export const createBearFishSlice = (set, get) => ({
    addBearAndFish: () => {
        get().addBear();
        get().addFish();
    },
});
```

Объединить все хранилища вместе - то же самое, что и раньше.

```js
import { create } from 'zustand';
import { createBearSlice } from './bearSlice';
import { createFishSlice } from './fishSlice';
import { createBearFishSlice } from './createBearFishSlice';

export const useBoundStore = create((...a) => ({
    ...createBearSlice(...a),
    ...createFishSlice(...a),
    ...createBearFishSlice(...a),
}));
```

## Добавление промежуточных товаров

Добавление промежуточных модулей в комбинированное хранилище происходит так же, как и в обычные хранилища.

Добавляем промежуточное ПО `persist` в наш `useBoundStore`:

```js
import { create } from 'zustand';
import { createBearSlice } from './bearSlice';
import { createFishSlice } from './fishSlice';
import { persist } from 'zustand/middleware';

export const useBoundStore = create(
    persist(
        (...a) => ({
            ...createBearSlice(...a),
            ...createFishSlice(...a),
        }),
        { name: 'bound-store' }
    )
);
```

Помните, что применять промежуточные модули следует только в объединенном хранилище. Применение их внутри отдельных фрагментов может привести к неожиданным проблемам.

## Использование с TypeScript

Подробное руководство по использованию шаблона slice в Zustand с TypeScript можно найти [здесь](./typescript.md#slices-pattern).

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/slices-pattern></small>
