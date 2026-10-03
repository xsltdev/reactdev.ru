---
description: Помимо хуков и компонентов, пакет react экспортирует ещё несколько API, полезных для определения компонентов. На этой странице перечислены все оставшиеся современные API React
---

# Обзор React API

<big>Помимо [хуков](./hooks.md) и [компонентов](./components.md), пакет `react` экспортирует ещё несколько API, полезных для определения компонентов. На этой странице перечислены все оставшиеся современные API React.</big>

-   [`createContext`](./createContext.md) позволяет определить контекст и предоставить его дочерним компонентам. Используется вместе с [`useContext`](./useContext.md).
-   [`lazy`](./lazy.md) позволяет отложить загрузку кода компонента до его первого отображения.
-   [`memo`](./memo.md) позволяет компоненту пропускать повторные рендеры с теми же пропсами. Используется с [`useMemo`](./useMemo.md) и [`useCallback`](./useCallback.md).
-   [`startTransition`](./startTransition.md) позволяет пометить обновление состояния как несрочное. Аналогично [`useTransition`](./useTransition.md).
-   [`addTransitionType`](./addTransitionType.md) позволяет указать причину перехода. Используется с [`startTransition`](./startTransition.md) и [`<ViewTransition>`](./ViewTransition.md).
-   [`act`](./act.md) позволяет обернуть рендеринг и взаимодействия в тестах, чтобы обновления применились до проверок.
-   [`cache`](./cache.md) позволяет кэшировать результат запроса данных или вычисления.
-   [`cacheSignal`](./cacheSignal.md) позволяет узнать, когда время жизни `cache()` закончилось.
-   [`captureOwnerStack`](./captureOwnerStack.md) в режиме разработки читает текущий стек владельцев и возвращает его строкой, если он доступен.

## API ресурсов {#resource-apis}

_Ресурсы_ доступны компоненту, даже если они не являются частью его состояния. Например, компонент может прочитать сообщение из промиса или информацию о стиле из контекста.

Эти виды ресурсов можно передать в [`use`](./use.md):

-   [Промис](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise), чтобы прочитать его значение после выполнения.
-   [Контекст](../../learn/passing-data-deeply-with-context.md), чтобы прочитать его значение.
-   Значение, которое возвращает [`browser`](../react-dom/browser.md), чтобы пометить компонент как доступный только в браузере во время серверного рендеринга.

```js
function MessageComponent({ messagePromise }) {
    const message = use(messagePromise);
    const theme = use(ThemeContext);
    use(browser());
    // ...
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/apis](https://react.dev/reference/react/apis)</small>
