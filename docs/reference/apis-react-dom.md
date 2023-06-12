# React DOM API

Пакет `react-dom` содержит методы, которые поддерживаются только для веб-приложений (которые работают в среде DOM браузера). Они не поддерживаются для React Native.

## API

Эти API могут быть импортированы из ваших компонентов. Они используются редко:

-   [`createPortal`](createPortal.md) позволяет вам отображать дочерние компоненты в другой части дерева DOM.
-   [`flushSync`](flushSync.md) позволяет заставить React промыть обновление состояния и синхронно обновить DOM.

## Точки входа

Пакет `react-dom` предоставляет две дополнительные точки входа:

-   [`react-dom/client`](client.md) содержит API для рендеринга компонентов React на клиенте (в браузере).
-   [`react-dom/server`](server.md) содержит API для рендеринга компонентов React на сервере.

## Утратившие актуальность API

!!!danger "Устарело"

    Эти API будут удалены в будущей основной версии React.

-   [`findDOMNode`](findDOMNode.md) находит ближайший узел DOM, соответствующий экземпляру компонента класса.
-   [`hydrate`](hydrate.md) монтирует дерево в DOM, созданное из серверного HTML. Исправлено в пользу [`hydrateRoot`](client-hydrateRoot.md).
-   [`render`](render.md) монтирует дерево в DOM. Исправлено в пользу [`createRoot`](client-createRoot.md).
-   [`unmountComponentAtNode`](unmountComponentAtNode.md) размонтирует дерево из DOM. Исправлено в пользу [`root.unmount()`](client-createRoot.md#root-unmount)
