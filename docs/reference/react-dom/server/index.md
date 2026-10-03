---
description: API react-dom/server позволяют рендерить компоненты React в HTML на сервере. Эти API используются только на сервере на верхнем уровне вашего приложения для генерации начального HTML
---

# Обзор Server React DOM APIs

API `react-dom/server` позволяют рендерить компоненты React в HTML на сервере. Эти API используются только на сервере на верхнем уровне вашего приложения для генерации начального HTML. [Фреймворк](../../../learn/start-a-new-react-project.md#full-stack-frameworks) может вызвать их за вас. Большинству ваших компонентов не нужно их импортировать или использовать.

## Серверные API для веб-потоков {#server-apis-for-web-streams}

Эти методы доступны только в окружениях с [Web Streams](https://developer.mozilla.org/docs/Web/API/Streams_API), которые включают браузеры, Deno и некоторые современные граничные среды исполнения:

-   [`renderToReadableStream`](renderToReadableStream.md) рендерит дерево React в [читаемый веб-поток](https://developer.mozilla.org/docs/Web/API/ReadableStream).
-   [`resume`](resume.md) продолжает [`prerender`](../static/prerender.md) в [читаемый веб-поток](https://developer.mozilla.org/docs/Web/API/ReadableStream).

!!!note "Примечание"

    В Node.js эти методы тоже есть ради совместимости, но из-за худшей производительности они не рекомендуются. Используйте [отдельные API Node.js](#server-apis-for-nodejs-streams).

## Серверные API для потоков Node.js {#server-apis-for-nodejs-streams}

Эти методы доступны только в окружениях с [Node.js Streams](https://nodejs.org/api/stream.html):

-   [`renderToPipeableStream`](renderToPipeableStream.md) рендерит дерево React в передаваемый [Node.js Stream](https://nodejs.org/api/stream.html).
-   [`resumeToPipeableStream`](resumeToPipeableStream.md) продолжает [`prerenderToNodeStream`](../static/prerenderToNodeStream.md) в передаваемый [Node.js Stream](https://nodejs.org/api/stream.html).

## Устаревшие серверные API для сред без потоков {#legacy-server-apis-for-non-streaming-environments}

Эти методы можно использовать в средах, которые не поддерживают потоки:

-   [`renderToString`](renderToString.md) рендерит дерево React в строку.
-   [`renderToStaticMarkup`](renderToStaticMarkup.md) рендерит неинтерактивное дерево React в строку.

У них меньше возможностей, чем у потоковых API.

[`renderToNodeStream`](renderToNodeStream.md) и [`renderToStaticNodeStream`](renderToStaticNodeStream.md) удалены в React 19. Их прежние описания оставлены в справочнике.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/server></small>
