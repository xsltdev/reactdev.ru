---
description: resumeToPipeableStream передаёт предварительно отрендеренное дерево React в передаваемый поток Node.js Stream
---

# resumeToPipeableStream

<big>`resumeToPipeableStream` передаёт предварительно отрендеренное дерево React в передаваемый [Node.js Stream.](https://nodejs.org/api/stream.html)</big>

```js
const {pipe, abort} = await resumeToPipeableStream(reactNode, postponedState, options?)
```

!!!note "Примечание"

    Этот API специфичен для Node.js. Окружения с [Web Streams,](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) такие как Deno и современные граничные среды исполнения, должны использовать [`resume`](resume.md).

## Описание {#reference}

### `resumeToPipeableStream(node, postponed, options?)` {#resume-to-pipeable-stream}

Вызовите `resumeToPipeableStream`, чтобы возобновить рендеринг предварительно отрендеренного дерева React в HTML в [Node.js Stream.](https://nodejs.org/api/stream.html#writable-streams)

```js
import { resumeToPipeableStream } from 'react-dom/server';
import {getPostponedState} from './storage';

async function handler(request, response) {
  const postponed = await getPostponedState(request);
  const {pipe} = resumeToPipeableStream(<App />, postponed, {
    onShellReady: () => {
      pipe(response);
    }
  });
}
```

[Больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   `reactNode`: Узел React, с которым вы вызывали `prerender`. Например, JSX-элемент `<App />`. Ожидается, что он представляет весь документ, поэтому компонент `App` должен вывести тег `<html>`.
-   `postponedState`: Непрозрачный объект `postpone`, возвращённый [API пререндера](../static/index.md) и загруженный оттуда, где вы его сохранили (например, redis, файл или S3).
-   **опционально** `options`: Объект с опциями потоковой передачи.
    -   **опционально** `nonce`: Строка [`nonce`](http://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#nonce), разрешающая скрипты для [`script-src` Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).
    -   **опционально** `onAllReady`: Обратный вызов, который срабатывает, когда весь рендеринг завершён, включая оболочку и всё дополнительное содержимое. Здесь можно вызвать `pipe` вместо `onShellReady` для краулеров и статической генерации. Поток будет содержать окончательный HTML.
    -   **опционально** `onBrowserBailout`: Обратный вызов, который React вызывает, когда восстанавливается после [`browser()`](../browser.md), оставляя фолбэк Suspense, который браузер заменит. Он получает `Error`, описывающий рендеринг только в браузере, и объект `errorInfo`, содержащий `componentStack`. Если в `browser` была передана причина, она доступна как `error.cause`. По умолчанию React ничего не делает. [Как сообщать о рендеринге только в браузере.](../browser.md#reporting-browser-only-rendering-on-the-server)
    -   **опционально** `onError`: Обратный вызов, который срабатывает при любой серверной ошибке, [восстановимой](renderToPipeableStream.md#recovering-from-errors-outside-the-shell) или [нет.](renderToPipeableStream.md#recovering-from-errors-inside-the-shell) По умолчанию он только вызывает `console.error`. Если вы переопределяете его, чтобы [записывать отчёты о сбоях,](renderToPipeableStream.md#logging-crashes-on-the-server) всё равно вызывайте `console.error`.
    -   **опционально** `onShellReady`: Обратный вызов, который срабатывает сразу после завершения [оболочки](renderToPipeableStream.md#specifying-what-goes-into-the-shell). Здесь можно вызвать `pipe`, чтобы начать потоковую передачу. React будет [передавать дополнительное содержимое потоком](renderToPipeableStream.md#streaming-more-content-as-it-loads) после оболочки вместе с инлайн-тегами `<script>`, которые заменяют HTML-фолбэки загрузки содержимым.
    -   **опционально** `onShellError`: Обратный вызов, который срабатывает, если при рендеринге оболочки произошла ошибка. Он получает ошибку аргументом. Из потока ещё не было отдано ни одного байта, и ни `onShellReady`, ни `onAllReady` не будут вызваны, поэтому можно [вывести резервную HTML-оболочку](renderToPipeableStream.md#recovering-from-errors-inside-the-shell) или использовать prelude.

#### Возвращаемое значение {#returns}

`resumeToPipeableStream` возвращает объект с двумя методами:

-   `pipe` выводит HTML в переданный [записываемый поток Node.js.](https://nodejs.org/api/stream.html#writable-streams) Вызовите `pipe` в `onShellReady`, если хотите включить потоковую передачу, или в `onAllReady` для краулеров и статической генерации.
-   `abort` позволяет [прервать серверный рендеринг](renderToPipeableStream.md#aborting-server-rendering) и дорендерить остальное на клиенте.

#### Предупреждения {#caveats}

-   `resumeToPipeableStream` не принимает опции `bootstrapScripts`, `bootstrapScriptContent` и `bootstrapModules`. Эти опции нужно передать в вызов `prerender`, который создаёт `postponedState`. Содержимое бутстрапа также можно вручную вставить в записываемый поток.
-   `resumeToPipeableStream` не принимает `identifierPrefix`, потому что префикс должен совпадать в `prerender` и `resumeToPipeableStream`.
-   Поскольку `nonce` нельзя передать в пререндер, передавайте `nonce` в `resumeToPipeableStream`, только если вы не передаёте скрипты в пререндер.
-   `resumeToPipeableStream` заново рендерит дерево от корня, пока не найдёт компонент, который не был полностью предварительно отрендерен. Полностью пререндеренные компоненты (сам компонент и его дочерние элементы закончили пререндер) пропускаются целиком.

## Использование {#usage}

### Дополнительно {#further-reading}

Возобновление ведёт себя как `renderToReadableStream`. Больше примеров — в [разделе использования `renderToReadableStream`](renderToReadableStream.md#usage).
[Раздел использования `prerender`](../static/prerender.md#usage) содержит примеры того, как использовать именно `prerenderToNodeStream`.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/server/resumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream)</small>
