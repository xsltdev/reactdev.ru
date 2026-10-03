---
description: В этом разделе представлена подробная справочная документация по работе с React
hide:
    - toc
---

# Справочник API

<big>В этом разделе представлена подробная справочная документация по работе с React. Для ознакомления с React посетите раздел [Обучения](../learn/index.md).</big>

## React <small>19</small> {#react}

Программные возможности React:

<div class="grid cards" style="margin-top: 1.6em" markdown>

-   :material-hook:{ .lg .middle } **Хуки**

    ***

    Используйте различные функции React в своих компонентах

    [:octicons-arrow-right-24: Хуки](./react/hooks.md)

-   :material-code-block-tags:{ .lg .middle } **Компоненты**

    ***

    Документирует встроенные компоненты, которые вы можете использовать в своем JSX

    [:octicons-arrow-right-24: Компоненты](./react/components.md)

-   :material-api:{ .lg .middle } **API**

    ***

    API, полезные для определения компонентов

    [:octicons-arrow-right-24: API](./react/apis.md)

-   :material-sign-direction:{ .lg .middle } **Директивы**

    ***

    Предоставляют инструкции для бандлеров, совместимых с React Server Components

    [:octicons-arrow-right-24: Директивы](./rsc/directives.md)

</div>

## React DOM <small>19</small> {#react-dom}

React DOM содержит функции, которые поддерживаются только для веб-приложений (которые работают в среде DOM браузера). Этот раздел разбит на следующие части:

<div class="grid cards" style="margin-top: 1.6em" markdown>

-   :material-hook:{ .lg .middle } **Хуки**

    ***

    Хуки для веб-приложений, которые работают в среде DOM браузера

    [:octicons-arrow-right-24: Хуки](./react-dom/hooks/index.md)

-   :material-code-block-tags:{ .lg .middle } **Компоненты**

    ***

    React поддерживает все встроенные в браузер компоненты HTML и SVG

    [:octicons-arrow-right-24: Компоненты](./react-dom/components/index.md)

-   :material-api:{ .lg .middle } **API**

    ***

    Пакет `react-dom` содержит методы, поддерживаемые только в веб-приложениях

    [:octicons-arrow-right-24: API](./react-dom/index.md)

-   :octicons-browser-24:{ .lg .middle } **Клиентские API**

    ***

    API `react-dom/client` позволяют рендерить компоненты React на клиенте (в браузере)

    [:octicons-arrow-right-24: Клиентские API](./react-dom/client/index.md)

-   :material-server:{ .lg .middle } **Серверные API**

    ***

    API `react-dom/server` позволяют рендерить компоненты React в HTML на сервере

    [:octicons-arrow-right-24: Серверные API](./react-dom/server/index.md)

-   :material-file-code-outline:{ .lg .middle } **Статические API**

    ***

    API `react-dom/static` генерируют статический HTML для компонентов React

    [:octicons-arrow-right-24: Статические API](./react-dom/static/index.md)

</div>

## React Compiler {#react-compiler}

Компилятор React — это инструмент оптимизации на этапе сборки, который автоматически мемоизирует компоненты и значения:

<div class="grid cards" style="margin-top: 1.6em" markdown>

-   :material-cog:{ .lg .middle } **Конфигурация**

    ***

    Параметры компилятора, включая совместимость с версией React

    [:octicons-arrow-right-24: Конфигурация](./react-compiler/configuration.md)

-   :material-code-tags:{ .lg .middle } **Директивы**

    ***

    Директивы уровня функции, которые управляют компиляцией

    [:octicons-arrow-right-24: Директивы](./react-compiler/directives/index.md)

-   :material-package-variant:{ .lg .middle } **Компиляция библиотек**

    ***

    Как поставлять заранее скомпилированный код библиотеки

    [:octicons-arrow-right-24: Компиляция библиотек](./react-compiler/compiling-libraries.md)

</div>

## Инструменты {#tools}

<div class="grid cards" style="margin-top: 1.6em" markdown>

-   :material-shield-check:{ .lg .middle } **eslint-plugin-react-hooks**

    ***

    Правила ESLint, которые проверяют правила React и диагностики компилятора

    [:octicons-arrow-right-24: Линты](./eslint-plugin-react-hooks/index.md)

-   :material-chart-bar:{ .lg .middle } **Дорожки производительности**

    ***

    Как читать дорожки производительности React в DevTools

    [:octicons-arrow-right-24: Дорожки производительности](./dev-tools/react-performance-tracks.md)

</div>

## Устаревшие API

-   [Обзор устаревших API](./react/legacy.md) - Экспортируется из пакета `react`, но не рекомендуется для использования во вновь написанном коде.
