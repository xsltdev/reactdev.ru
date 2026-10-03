---
description: resumeAndPrerender продолжает предварительно отрендеренное дерево React в строку статического HTML с помощью Web Stream
---

# resumeAndPrerender

<big>`resumeAndPrerender` продолжает предварительно отрендеренное дерево React в строку статического HTML с помощью [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API).</big>

```js
const {prelude, postponed} = await resumeAndPrerender(reactNode, postponedState, options?)
```

!!!note "Примечание"

    Этот API зависит от [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) Для Node.js используйте [`resumeAndPrerenderToNodeStream`](resumeAndPrerenderToNodeStream.md).

## Описание {#reference}

### `resumeAndPrerender(reactNode, postponedState, options?)` {#resumeandprerender}

Вызовите `resumeAndPrerender`, чтобы продолжить предварительно отрендеренное дерево React в строку статического HTML.

```js
import { resumeAndPrerender } from 'react-dom/static';
import { getPostponedState } from 'storage';

async function handler(request, response) {
  const postponedState = getPostponedState(request);
  const { prelude } = await resumeAndPrerender(<App />, postponedState, {
    bootstrapScripts: ['/main.js']
  });
  return new Response(prelude, {
    headers: { 'content-type': 'text/html' },
  });
}
```

На клиенте вызовите [`hydrateRoot`](../client/hydrateRoot.md), чтобы сделать сгенерированный сервером HTML интерактивным.

[Больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   `reactNode`: Узел React, с которым вы вызывали `prerender` (или предыдущий `resumeAndPrerender`). Например, JSX-элемент `<App />`. Ожидается, что он представляет весь документ, поэтому компонент `App` должен вывести тег `<html>`.
-   `postponedState`: Непрозрачный объект `postpone`, возвращённый [API пререндера](index.md) и загруженный оттуда, где вы его сохранили (например, redis, файл или S3).
-   **опционально** `options`: Объект с опциями потоковой передачи.
    -   **опционально** `signal`: [Сигнал прерывания](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), который позволяет [прервать серверный рендеринг](../server/renderToReadableStream.md#aborting-server-rendering) и дорендерить остальное на клиенте.
    -   **опционально** `onBrowserBailout`: Обратный вызов, который React вызывает, когда восстанавливается после [`browser()`](../browser.md), оставляя фолбэк Suspense, который браузер заменит. Он получает `Error`, описывающий рендеринг только в браузере, и объект `errorInfo`, содержащий `componentStack`. Если в `browser` была передана причина, она доступна как `error.cause`. По умолчанию React ничего не делает. [Как сообщать о рендеринге только в браузере.](../browser.md#reporting-browser-only-rendering-on-the-server)
    -   **опционально** `onError`: Обратный вызов, который срабатывает при любой серверной ошибке, [восстановимой](../server/renderToReadableStream.md#recovering-from-errors-outside-the-shell) или [нет.](../server/renderToReadableStream.md#recovering-from-errors-inside-the-shell) По умолчанию он только вызывает `console.error`. Если вы переопределяете его, чтобы [записывать отчёты о сбоях,](../server/renderToReadableStream.md#logging-crashes-on-the-server) всё равно вызывайте `console.error`.

#### Возвращаемое значение {#returns}

`prerender` возвращает промис:

-   Если рендеринг прошёл успешно, промис разрешится в объект, содержащий:
    -   `prelude`: [веб-поток](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) HTML. Этот поток можно использовать, чтобы отправлять ответ частями, или прочитать весь поток в строку.
    -   `postponed`: непрозрачный объект, сериализуемый в JSON, который можно передать в [`resume`](../server/resume.md) или [`resumeAndPrerender`](resumeAndPrerender.md), если `prerender` прерван.
-   Если рендеринг не удался, промис будет отклонён. [Используйте это, чтобы вывести резервную оболочку.](../server/renderToReadableStream.md#recovering-from-errors-inside-the-shell)

#### Предупреждения {#caveats}

`nonce` недоступен при пререндере. Nonce должен быть уникальным для каждого запроса, и если вы защищаете приложение с помощью [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP), включать значение nonce в сам пререндер было бы неуместно и небезопасно.

!!!note "Когда использовать `resumeAndPrerender`?"

    Статический API `resumeAndPrerender` используется для статической генерации на сервере (SSG). В отличие от `renderToString`, `resumeAndPrerender` ждёт загрузки всех данных, прежде чем разрешиться. Поэтому он подходит для генерации статического HTML целой страницы, включая данные, которые нужно получить с помощью Suspense. Чтобы передавать содержимое потоком по мере загрузки, используйте потоковый API серверного рендеринга (SSR), например [renderToReadableStream](../server/renderToReadableStream.md).

    `resumeAndPrerender` можно прервать и позже либо продолжить ещё одним `resumeAndPrerender`, либо возобновить с помощью `resume`, чтобы поддержать частичный пререндер.

## Использование {#usage}

### Дополнительно {#further-reading}

`resumeAndPrerender` ведёт себя похоже на [`prerender`](prerender.md), но им можно продолжить ранее начатый и прерванный пререндер.
Подробнее о возобновлении предварительно отрендеренного дерева см. [документацию `resume`](../server/resume.md#resuming-a-prerender).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/static/resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender)</small>
