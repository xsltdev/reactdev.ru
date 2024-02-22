# Обзор Server React DOM APIs

API `react-dom/server` позволяют рендерить компоненты React в HTML на сервере. Эти API используются только на сервере на верхнем уровне вашего приложения для генерации начального HTML. Фреймворк [framework](../../../learn/start-a-new-react-project.md) может вызвать их для вас. Большинству ваших компонентов не нужно их импортировать или использовать.

## Серверные API для потоков Node.js

Эти методы доступны только в окружениях с [Node.js Streams](https://nodejsdev.ru/api/stream/):

-   [`renderToPipeableStream`](renderToPipeableStream.md) рендерит дерево React в передаваемый [Node.js Stream](https://nodejsdev.ru/api/stream/).
-   [`renderToStaticNodeStream`](renderToStaticNodeStream.md) рендерит неинтерактивное дерево React в [Node.js Readable Stream](https://nodejsdev.ru/api/stream/).

## API сервера для веб-потоков

Эти методы доступны только в окружениях с [Web Streams](https://developer.mozilla.org/docs/Web/API/Streams_API), которые включают браузеры, Deno и некоторые современные граничные среды исполнения:

-   [`renderToReadableStream`](renderToReadableStream.md) рендерит дерево React в [читаемый веб-поток](https://developer.mozilla.org/docs/Web/API/ReadableStream).

## API сервера для не потоковых сред

Эти методы могут быть использованы в средах, не поддерживающих потоки:

-   [`renderToString`](renderToString.md) рендерит дерево React в строку.
-   [`renderToStaticMarkup`](renderToStaticMarkup.md) рендерит неинтерактивное дерево React в строку.

Они имеют ограниченную функциональность по сравнению с потоковыми API.

## Исчезнувшие серверные API

!!!danger "Устарело"

    Эти API будут удалены в одной из будущих основных версий React.

-   [`renderToNodeStream`](renderToNodeStream.md) рендерит дерево React в [Node.js Readable stream.](https://nodejsdev.ru/api/stream/) (Утратил силу.)

<!-- 0001.part.md -->

## Ссылки

-   [https://react.dev/reference/react-dom/server](https://react.dev/reference/react-dom/server)
