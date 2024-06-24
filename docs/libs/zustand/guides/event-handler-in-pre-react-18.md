# Вызов действий за пределами обработчика событий React в версии до React 18

Поскольку React обрабатывает `setState` синхронно, если он вызывается вне обработчика события, обновление состояния вне обработчика события заставит react синхронно обновлять компоненты. Поэтому есть риск столкнуться с эффектом "зомби-ребенка". Чтобы исправить это, действие нужно обернуть в `unstable_batchedUpdates` следующим образом:

```jsx
import { unstable_batchedUpdates } from 'react-dom'; // or 'react-native'

const useFishStore = create((set) => ({
    fishes: 0,
    increaseFishes: () =>
        set((prev) => ({ fishes: prev.fishes + 1 })),
}));

const nonReactCallback = () => {
    unstable_batchedUpdates(() => {
        useFishStore.getState().increaseFishes();
    });
};
```

Подробнее: <https://github.com/pmndrs/zustand/issues/302>
