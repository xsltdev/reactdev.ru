---
description: Помимо Hooks и Components, пакет react экспортирует еще несколько API, полезных для определения компонентов. На этой странице перечислены все оставшиеся современные API React
---

# Обзор React API

<big>Помимо [Hooks](./hooks.md) и [Components](./components.md), пакет `react` экспортирует еще несколько API, полезных для определения компонентов. На этой странице перечислены все оставшиеся современные API React.</big>

-   [`createContext`](./createContext.md) позволяет определить и предоставить контекст дочерним компонентам. Используется вместе с [`useContext`](./useContext.md).
-   [`forwardRef`](./forwardRef.md) позволяет вашему компоненту отображать узел DOM как ссылку на родительский. Используется с [`useRef`](./useRef.md).
-   [`lazy`](./lazy.md) позволяет отложить загрузку кода компонента до его первого отображения.
-   [`memo`](./memo.md) позволяет компоненту пропускать повторные рендеры с теми же реквизитами. Используется с [`useMemo`](./useMemo.md) и [`useCallback`](./useCallback.md).
-   [`startTransition`](./startTransition.md) позволяет пометить обновление состояния как несрочное. Аналогично [`useTransition`](./useTransition.md).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/apis](https://react.dev/reference/react/apis)</small>
