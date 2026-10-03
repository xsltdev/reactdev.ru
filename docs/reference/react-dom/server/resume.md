---
description: resume передаёт предварительно отрендеренное дерево React в читаемый веб-поток
---

# resume

<big>`resume` передаёт предварительно отрендеренное дерево React в [читаемый веб-поток.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)</big>

```js
const stream = await resume(reactNode, postponedState, options?)
```

!!!note "Примечание"

    Этот API зависит от [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) Для Node.js используйте [`resumeToNodeStream`](renderToPipeableStream.md).

## Описание {#reference}

### `resume(node, postponedState, options?)` {#resume}

Вызовите `resume`, чтобы возобновить рендеринг предварительно отрендеренного дерева React в HTML в [читаемый веб-поток.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)

```js
import { resume } from 'react-dom/server';
import {getPostponedState} from './storage';

async function handler(request, writable) {
  const postponed = await getPostponedState(request);
  const resumeStream = await resume(<App />, postponed);
  return resumeStream.pipeTo(writable)
}
```

[Больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   `reactNode`: Узел React, с которым вы вызывали `prerender`. Например, JSX-элемент `<App />`. Ожидается, что он представляет весь документ, поэтому компонент `App` должен вывести тег `<html>`.
-   `postponedState`: Непрозрачный объект `postpone`, возвращённый [API пререндера](../static/index.md) и загруженный оттуда, где вы его сохранили (например, redis, файл или S3).
-   **опционально** `options`: Объект с опциями потоковой передачи.
    -   **опционально** `nonce`: Строка [`nonce`](http://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#nonce), разрешающая скрипты для [`script-src` Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).
    -   **опционально** `signal`: [Сигнал прерывания](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), который позволяет [прервать серверный рендеринг](renderToReadableStream.md#aborting-server-rendering) и дорендерить остальное на клиенте.
    -   **опционально** `onBrowserBailout`: Обратный вызов, который React вызывает, когда восстанавливается после [`browser()`](../browser.md), оставляя фолбэк Suspense, который браузер заменит. Он получает `Error`, описывающий рендеринг только в браузере, и объект `errorInfo`, содержащий `componentStack`. Если в `browser` была передана причина, она доступна как `error.cause`. По умолчанию React ничего не делает. [Как сообщать о рендеринге только в браузере.](../browser.md#reporting-browser-only-rendering-on-the-server)
    -   **опционально** `onError`: Обратный вызов, который срабатывает при любой серверной ошибке, [восстановимой](renderToReadableStream.md#recovering-from-errors-outside-the-shell) или [нет.](renderToReadableStream.md#recovering-from-errors-inside-the-shell) По умолчанию он только вызывает `console.error`. Если вы переопределяете его, чтобы [записывать отчёты о сбоях,](renderToReadableStream.md#logging-crashes-on-the-server) всё равно вызывайте `console.error`.

#### Возвращаемое значение {#returns}

`resume` возвращает промис:

-   Если `resume` успешно создал [оболочку](renderToReadableStream.md#specifying-what-goes-into-the-shell), промис разрешится в [читаемый веб-поток,](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream) который можно направить в [записываемый веб-поток.](https://developer.mozilla.org/en-US/docs/Web/API/WritableStream)
-   Если в оболочке произойдёт ошибка, промис будет отклонён с этой ошибкой.

У возвращённого потока есть дополнительное свойство:

-   `allReady`: Промис, который разрешается, когда весь рендеринг завершён. Можно выполнить `await stream.allReady` перед возвратом ответа [для краулеров и статической генерации.](renderToReadableStream.md#waiting-for-all-content-to-load-for-crawlers-and-static-generation) Если сделать так, прогрессивной загрузки не будет. Поток будет содержать окончательный HTML.

#### Предупреждения {#caveats}

-   `resume` не принимает опции `bootstrapScripts`, `bootstrapScriptContent` и `bootstrapModules`. Эти опции нужно передать в вызов `prerender`, который создаёт `postponedState`. Содержимое бутстрапа также можно вручную вставить в записываемый поток.
-   `resume` не принимает `identifierPrefix`, потому что префикс должен совпадать в `prerender` и `resume`.
-   Поскольку `nonce` нельзя передать в пререндер, передавайте `nonce` в `resume`, только если вы не передаёте скрипты в пререндер.
-   `resume` заново рендерит дерево от корня, пока не найдёт компонент, который не был полностью предварительно отрендерен. Полностью пререндеренные компоненты (сам компонент и его дочерние элементы закончили пререндер) пропускаются целиком.

## Использование {#usage}

### Возобновление пререндера {#resuming-a-prerender}

=== "App.js"

    ```js

    ```

=== "public/index.html"

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
    </head>
    <body>
      <iframe id="container"></iframe>
    </body>
    </html>
    ```

=== "index.js"

    ```js
    import {
        flushReadableStreamToFrame,
        getUser,
        Postponed,
        sleep,
    } from "./demo-helpers";
    import { StrictMode, Suspense, use, useEffect } from "react";
    import { prerender } from "react-dom/static";
    import { resume } from "react-dom/server";
    import { hydrateRoot } from "react-dom/client";

    function Header() {
        return <header>Me and my descendants can be prerendered</header>;
    }

    const { promise: cookies, resolve: resolveCookies } = Promise.withResolvers();

    function Main() {
        const { sessionID } = use(cookies);
        const user = getUser(sessionID);

        useEffect(() => {
            console.log("reached interactivity!");
        }, []);

        return (
            <main>
                Hello, {user.name}!
                <button onClick={() => console.log("hydrated!")}>
                    Clicking me requires hydration.
                </button>
            </main>
        );
    }

    function Shell({ children }) {
        // In a real app, this is where you would put your html and body.
        // We're just using tags here we can include in an existing body for demonstration purposes
        return (
            <html>
                <body>{children}</body>
            </html>
        );
    }

    function App() {
        return (
            <Shell>
                <Suspense fallback="loading header">
                    <Header />
                </Suspense>
                <Suspense fallback="loading main">
                    <Main />
                </Suspense>
            </Shell>
        );
    }

    async function main(frame) {
        // Layer 1
        const controller = new AbortController();
        const prerenderedApp = prerender(<App />, {
            signal: controller.signal,
            onError(error) {
                if (error instanceof Postponed) {
                } else {
                    console.error(error);
                }
            },
        });
        // We're immediately aborting in a macrotask.
        // Any data fetching that's not available synchronously, or in a microtask, will not have finished.
        setTimeout(() => {
            controller.abort(new Postponed());
        });

        const { prelude, postponed } = await prerenderedApp;
        await flushReadableStreamToFrame(prelude, frame);

        // Layer 2
        // Just waiting here for demonstration purposes.
        // In a real app, the prelude and postponed state would've been serialized in Layer 1 and Layer would deserialize them.
        // The prelude content could be flushed immediated as plain HTML while
        // React is continuing to render from where the prerender left off.
        await sleep(2000);

        // You would get the cookies from the incoming HTTP request
        resolveCookies({ sessionID: "abc" });

        const stream = await resume(<App />, postponed);

        await flushReadableStreamToFrame(stream, frame);

        // Layer 3
        // Just waiting here for demonstration purposes.
        await sleep(2000);

        hydrateRoot(frame.contentWindow.document, <App />);
    }

    main(document.getElementById("container"));
    ```

=== "demo-helpers.js"

    ```js
    export async function flushReadableStreamToFrame(readable, frame) {
        const document = frame.contentWindow.document;
        const decoder = new TextDecoder();
        const reader = readable.getReader();

        while (true) {
            const {done, value} = await reader.read();
            if (done) {
                break;
            }
            const partialHTML = decoder.decode(value, {stream: true});
            document.write(partialHTML);
        }

        document.write(decoder.decode());
    }

    // This doesn't need to be an error.
    // You can use any other means to check if an error during prerender was
    // from an intentional abort or a real error.
    export class Postponed extends Error {}

    // We're just hardcoding a session here.
    export function getUser(sessionID) {
        return {
            name: "Alice",
        };
    }

    export function sleep(timeoutMS) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, timeoutMS);
        });
    }
    ```

### Дополнительно {#further-reading}

Возобновление ведёт себя как `renderToReadableStream`. Больше примеров — в [разделе использования `renderToReadableStream`](renderToReadableStream.md#usage).
[Раздел использования `prerender`](../static/prerender.md#usage) содержит примеры того, как использовать именно `prerender`.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/server/resume](https://react.dev/reference/react-dom/server/resume)</small>
