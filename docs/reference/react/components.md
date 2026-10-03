---
description: React предлагает несколько встроенных компонентов, которые вы можете использовать в своем JSX
---

# Обзор компонентов

<big>React предлагает несколько встроенных компонентов, которые вы можете использовать в своем JSX.</big>

## Компоненты сервера {#server-components}

Документация по серверным и клиентским компонентам: [`use server`](../rsc/use-server.md), [`use client`](../rsc/use-client.md).

## Встроенные компоненты {#built-in-components}

-   [`<Fragment>`](./Fragment.md), альтернативно записываемый как <code>&lt;>...&lt;/></code>, позволяет группировать несколько узлов JSX вместе.
-   [`<Profiler>`](./Profiler.md) позволяет программно измерить производительность рендеринга дерева React.
-   [`<Suspense>`](./Suspense.md) позволяет отображать откат во время загрузки дочерних компонентов.
-   [`<StrictMode>`](./StrictMode.md) включает дополнительные проверки, предназначенные только для разработчиков, которые помогают находить ошибки на ранней стадии.
-   [`<Activity>`](./Activity.md) позволяет скрывать и восстанавливать интерфейс и внутреннее состояние дочерних элементов.
-   [`<ViewTransition>`](./ViewTransition.md) позволяет анимировать дерево компонентов вместе с переходами и Suspense.

## Ваши компоненты {#your-own-components}

Вы также можете [определить собственные компоненты](../../learn/your-first-component.md) как функции JavaScript.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/components](https://react.dev/reference/react/components)</small>
