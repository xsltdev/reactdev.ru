---
description: Практика, вдохновленная flux
---

# Практика, вдохновленная flux

Несмотря на то, что Zustand - это библиотека, не имеющая собственного мнения, мы все же рекомендуем несколько паттернов. Они вдохновлены практиками, которые изначально присутствовали в [Flux](https://github.com/facebookarchive/flux), а в последнее время - в [Redux](https://redux.js.org/understanding/thinking-in-redux/three-principles), поэтому если вы пришли из другой библиотеки, вы должны чувствовать себя как дома.

Тем не менее, Zustand отличается в некоторых фундаментальных аспектах, поэтому некоторая терминология может не полностью совпадать с другими библиотеками.

## Рекомендуемые шаблоны

### Единое хранилище

Глобальное состояние вашего приложения должно быть расположено в одном хранилище Zustand.

Если у вас большое приложение, Zustand поддерживает [разбиение хранилища на фрагменты](./slices-pattern.md).

### Используйте `set` / `setState` для обновления хранилища

Всегда используйте `set` (или `setState`) для обновления вашего хранилища. `set` (и `setState`) гарантирует, что описанное обновление будет корректно объединено и слушатели получат соответствующее уведомление.

### Размещайте действия в хранилище

В Zustand состояние можно обновлять без использования диспетчерских действий и редукторов, которые есть в других библиотеках Flux. Эти действия хранилища могут быть добавлены непосредственно в хранилище, как показано ниже.

По желанию, с помощью `setState` они могут быть [расположены вне хранилища](./practice-with-no-store-actions.md)

```js
const useBoundStore = create((set) => ({
  storeSliceA: ...,
  storeSliceB: ...,
  storeSliceC: ...,
  updateX: () => set(...),
  updateY: () => set(...),
}))
```

## Redux-подобные паттерны

Если вы не можете жить без Redux-подобных редукторов, вы можете определить функцию `dispatch` на корневом уровне хранилища:

```typescript
const types = {
    increase: 'INCREASE',
    decrease: 'DECREASE',
};

const reducer = (state, { type, by = 1 }) => {
    switch (type) {
        case types.increase:
            return { grumpiness: state.grumpiness + by };
        case types.decrease:
            return { grumpiness: state.grumpiness - by };
    }
};

const useGrumpyStore = create((set) => ({
    grumpiness: 0,
    dispatch: (args) =>
        set((state) => reducer(state, args)),
}));

const dispatch = useGrumpyStore((state) => state.dispatch);
dispatch({ type: types.increase, by: 2 });
```

Вы также можете использовать наш redux-middleware. Он подключает ваш главный редуктор, устанавливает начальное состояние и добавляет функцию диспетчеризации к самому состоянию и ванильному api.

```typescript
import { redux } from 'zustand/middleware';

const useReduxStore = create(redux(reducer, initialState));
```

Другим способом обновления хранилища могут быть функции, оборачивающие функции состояния. Они также могут обрабатывать побочные эффекты действий. Например, с помощью HTTP-вызовов. Чтобы использовать Zustand нереактивным способом, смотрите [readme](https://github.com/pmndrs/zustand#readingwriting-state-and-reacting-to-changes-outside-of-components).

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/flux-inspired-practice></small>
