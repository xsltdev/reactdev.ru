---
description: API react-dom/static позволяют генерировать статический HTML для компонентов React. У них меньше возможностей, чем у потоковых API
---

# Обзор Static React DOM API

<big>API `react-dom/static` позволяют генерировать статический HTML для компонентов React. У них меньше возможностей, чем у потоковых API. [Фреймворк](../../../learn/start-a-new-react-project.md#full-stack-frameworks) может вызвать их за вас. Большинству ваших компонентов не нужно их импортировать или использовать.</big>

## Статические API для веб-потоков {#static-apis-for-web-streams}

Эти методы доступны только в окружениях с [Web Streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API), которые включают браузеры, Deno и некоторые современные граничные среды исполнения:

-   [`prerender`](prerender.md) рендерит дерево React в статический HTML с помощью [читаемого веб-потока.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)
-   [`resumeAndPrerender`](resumeAndPrerender.md) продолжает предварительно отрендеренное дерево React в статический HTML с помощью [читаемого веб-потока](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream).

В Node.js эти методы тоже есть ради совместимости, но из-за худшей производительности они не рекомендуются. Используйте [отдельные API Node.js](#static-apis-for-nodejs-streams).

## Статические API для потоков Node.js {#static-apis-for-nodejs-streams}

Эти методы доступны только в окружениях с [Node.js Streams](https://nodejs.org/api/stream.html):

-   [`prerenderToNodeStream`](prerenderToNodeStream.md) рендерит дерево React в статический HTML с помощью [Node.js Stream.](https://nodejs.org/api/stream.html)
-   [`resumeAndPrerenderToNodeStream`](resumeAndPrerenderToNodeStream.md) продолжает предварительно отрендеренное дерево React в статический HTML с помощью [Node.js Stream.](https://nodejs.org/api/stream.html)

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/static/index](https://react.dev/reference/react-dom/static/index)</small>
