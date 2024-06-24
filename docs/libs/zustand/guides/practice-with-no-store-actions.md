---
description: Практика без действий в хранилище
---

# Практика без действий в хранилище

Рекомендуется размещать действия и состояния в хранилище (пусть ваши действия будут расположены вместе с состоянием).

Например:

```js
export const useBoundStore = create((set) => ({
    count: 0,
    text: 'hello',
    inc: () => set((state) => ({ count: state.count + 1 })),
    setText: (text) => set({ text }),
}));
```

Таким образом, создается автономное хранилище с данными и действиями вместе.

---

Альтернативный подход заключается в определении действий на уровне модуля, внешнего по отношению к хранилищу.

```js
export const useBoundStore = create(() => ({
    count: 0,
    text: 'hello',
}));

export const inc = () =>
    useBoundStore.setState((state) => ({
        count: state.count + 1,
    }));

export const setText = (text) =>
    useBoundStore.setState({ text });
```

У этого способа есть несколько преимуществ:

-   Для вызова действия не требуется хук;
-   облегчает разделение кода.

Хотя этот паттерн не имеет недостатков, некоторые могут предпочесть colocating из-за его инкапсулированной природы.

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/practice-with-no-store-actions></small>
