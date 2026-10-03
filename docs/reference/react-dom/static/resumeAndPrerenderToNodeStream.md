---
description: resumeAndPrerenderToNodeStream продолжает предварительно отрендеренное дерево React в строку статического HTML с помощью потока Node.js Stream
---

# resumeAndPrerenderToNodeStream

<big>`resumeAndPrerenderToNodeStream` продолжает предварительно отрендеренное дерево React в строку статического HTML с помощью [Node.js Stream.](https://nodejs.org/api/stream.html).</big>

```js
const {prelude, postponed} = await resumeAndPrerenderToNodeStream(reactNode, postponedState, options?)
```

!!!note "Примечание"

    Этот API специфичен для Node.js. Окружения с [Web Streams,](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) такие как Deno и современные граничные среды исполнения, должны использовать [`prerender`](prerender.md).

## Описание {#reference}

### `resumeAndPrerenderToNodeStream(reactNode, postponedState, options?)` {#resumeandprerendertolnodestream}

Вызовите `resumeAndPrerenderToNodeStream`, чтобы продолжить предварительно отрендеренное дерево React в строку статического HTML.

```js
import { resumeAndPrerenderToNodeStream } from 'react-dom/static';
import { getPostponedState } from 'storage';

async function handler(request, writable) {
  const postponedState = getPostponedState(request);
  const { prelude } = await resumeAndPrerenderToNodeStream(<App />, JSON.parse(postponedState));
  prelude.pipe(writable);
}
```

На клиенте вызовите [`hydrateRoot`](../client/hydrateRoot.md), чтобы сделать сгенерированный сервером HTML интерактивным.

[Больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   `reactNode`: Узел React, с которым вы вызывали `prerender` (или предыдущий `resumeAndPrerenderToNodeStream`). Например, JSX-элемент `<App />`. Ожидается, что он представляет весь документ, поэтому компонент `App` должен вывести тег `<html>`.
-   `postponedState`: Непрозрачный объект `postpone`, возвращённый [API пререндера](index.md) и загруженный оттуда, где вы его сохранили (например, redis, файл или S3).
-   **опционально** `options`: Объект с опциями потоковой передачи.
    -   **опционально** `signal`: [Сигнал прерывания](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), который позволяет [прервать серверный рендеринг](../server/renderToPipeableStream.md#aborting-server-rendering) и дорендерить остальное на клиенте.
    -   **опционально** `onBrowserBailout`: Обратный вызов, который React вызывает, когда восстанавливается после [`browser()`](../browser.md), оставляя фолбэк Suspense, который браузер заменит. Он получает `Error`, описывающий рендеринг только в браузере, и объект `errorInfo`, содержащий `componentStack`. Если в `browser` была передана причина, она доступна как `error.cause`. По умолчанию React ничего не делает. [Как сообщать о рендеринге только в браузере.](../browser.md#reporting-browser-only-rendering-on-the-server)
    -   **опционально** `onError`: Обратный вызов, который срабатывает при любой серверной ошибке, [восстановимой](../server/renderToPipeableStream.md#recovering-from-errors-outside-the-shell) или [нет.](../server/renderToPipeableStream.md#recovering-from-errors-inside-the-shell) По умолчанию он только вызывает `console.error`. Если вы переопределяете его, чтобы [записывать отчёты о сбоях,](../server/renderToPipeableStream.md#logging-crashes-on-the-server) всё равно вызывайте `console.error`.

#### Возвращаемое значение {#returns}

`resumeAndPrerenderToNodeStream` возвращает промис:

-   Если рендеринг прошёл успешно, промис разрешится в объект, содержащий:
    -   `prelude`: [веб-поток](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) HTML. Этот поток можно использовать, чтобы отправлять ответ частями, или прочитать весь поток в строку.
    -   `postponed`: непрозрачный объект, сериализуемый в JSON, который можно передать в [`resumeToNodeStream`](../server/resume.md) или [`resumeAndPrerenderToNodeStream`](resumeAndPrerenderToNodeStream.md), если `resumeAndPrerenderToNodeStream` прерван.
-   Если рендеринг не удался, промис будет отклонён. [Используйте это, чтобы вывести резервную оболочку.](../server/renderToPipeableStream.md#recovering-from-errors-inside-the-shell)

#### Предупреждения {#caveats}

`nonce` недоступен при пререндере. Nonce должен быть уникальным для каждого запроса, и если вы защищаете приложение с помощью [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP), включать значение nonce в сам пререндер было бы неуместно и небезопасно.

!!!note "Когда использовать `resumeAndPrerenderToNodeStream`?"

    Статический API `resumeAndPrerenderToNodeStream` используется для статической генерации на сервере (SSG). В отличие от `renderToString`, `resumeAndPrerenderToNodeStream` ждёт загрузки всех данных, прежде чем разрешиться. Поэтому он подходит для генерации статического HTML целой страницы, включая данные, которые нужно получить с помощью Suspense. Чтобы передавать содержимое потоком по мере загрузки, используйте потоковый API серверного рендеринга (SSR), например [renderToReadableStream](../server/renderToReadableStream.md).

    `resumeAndPrerenderToNodeStream` можно прервать и позже либо продолжить ещё одним `resumeAndPrerenderToNodeStream`, либо возобновить с помощью `resume`, чтобы поддержать частичный пререндер.

## Использование {#usage}

### Дополнительно {#further-reading}

`resumeAndPrerenderToNodeStream` ведёт себя похоже на [`prerender`](prerender.md), но им можно продолжить ранее начатый и прерванный пререндер.
Подробнее о возобновлении предварительно отрендеренного дерева см. [документацию `resume`](../server/resume.md#resuming-a-prerender).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream)</small>
