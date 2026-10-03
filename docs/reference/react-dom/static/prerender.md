---
description: prerender рендерит дерево React в строку статического HTML с помощью Web Stream
---

# prerender

<big>`prerender` рендерит дерево React в строку статического HTML с помощью [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API).</big>

```js
const {prelude, postponed} = await prerender(reactNode, options?)
```

!!!note "Примечание"

    Этот API зависит от [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) Для Node.js используйте [`prerenderToNodeStream`](prerenderToNodeStream.md).

## Описание {#reference}

### `prerender(reactNode, options?)` {#prerender}

Вызовите `prerender`, чтобы отрендерить приложение в статический HTML.

```js
import { prerender } from 'react-dom/static';

async function handler(request, response) {
  const {prelude} = await prerender(<App />, {
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

-   `reactNode`: Узел React, который вы хотите отрендерить в HTML. Например, JSX-узел `<App />`. Ожидается, что он представляет весь документ, поэтому компонент App должен вывести тег `<html>`.
-   **опционально** `options`: Объект с опциями статической генерации.
    -   **опционально** `bootstrapScriptContent`: Если указано, эта строка будет помещена в инлайн-тег `<script>`.
    -   **опционально** `bootstrapScripts`: Массив URL-строк для тегов `<script>`, которые будут выведены на странице. Используйте его, чтобы включить `<script>`, вызывающий [`hydrateRoot`.](../client/hydrateRoot.md) Опустите его, если вы вообще не хотите запускать React на клиенте.
    -   **опционально** `bootstrapModules`: Аналогично `bootstrapScripts`, но вместо этого выводится [`<script type="module">`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules).
    -   **опционально** `identifierPrefix`: Строковый префикс, который React использует для идентификаторов, генерируемых [`useId`.](../../react/useId.md) Полезен, чтобы избежать конфликтов при использовании нескольких корней на одной странице. Должен совпадать с префиксом, переданным в [`hydrateRoot`.](../client/hydrateRoot.md#parameters)
    -   **опционально** `importMap`: Объект [карты импорта](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap) со свойствами `imports` и `scopes`. React выводит его как инлайн-тег `<script type="importmap">` перед любыми модульными скриптами, чтобы теги `<script type="module">` (например, из `bootstrapModules`) могли использовать спецификаторы модулей без пути.
    -   **опционально** `maxHeadersLength`: Максимальная суммарная длина содержимого заголовка, передаваемого в `onHeaders`, в единицах кода UTF-16. По умолчанию 2000. Когда предел достигнут, React перестаёт добавлять подсказки о ресурсах в заголовки.
    -   **опционально** `namespaceURI`: Строка с корневым [namespace URI](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElementNS#important_namespace_uris) для потока. По умолчанию используется обычный HTML. Передайте `'http://www.w3.org/2000/svg'` для SVG или `'http://www.w3.org/1998/Math/MathML'` для MathML.
    -   **опционально** `onBrowserBailout`: Обратный вызов, который React вызывает, когда восстанавливается после [`browser()`](../browser.md), оставляя фолбэк Suspense, который браузер заменит. Он получает `Error`, описывающий рендеринг только в браузере, и объект `errorInfo`, содержащий `componentStack`. Если в `browser` была передана причина, она доступна как `error.cause`. По умолчанию React ничего не делает. [Как сообщать о рендеринге только в браузере.](../browser.md#reporting-browser-only-rendering-on-the-server)
    -   **опционально** `onError`: Обратный вызов, который срабатывает при любой серверной ошибке, [восстановимой](../server/renderToReadableStream.md#recovering-from-errors-outside-the-shell) или [нет.](../server/renderToReadableStream.md#recovering-from-errors-inside-the-shell) По умолчанию он только вызывает `console.error`. Если вы переопределяете его, чтобы [записывать отчёты о сбоях,](../server/renderToReadableStream.md#logging-crashes-on-the-server) всё равно вызывайте `console.error`. Его также можно использовать, чтобы [изменить код состояния](../server/renderToReadableStream.md#setting-the-status-code) до того, как будет выдана оболочка.
    -   **опционально** `onHeaders`: Обратный вызов, который срабатывает, когда React определил подсказки о ресурсах документа, такие как preconnect и предварительная загрузка таблиц стилей, шрифтов или изображений с высоким приоритетом. Он получает экземпляр [`Headers`](https://developer.mozilla.org/en-US/docs/Web/API/Headers) с соответствующим значением [заголовка `Link`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/link), чтобы вы могли отправить его как HTTP-заголовок ответа или как ответ [103 Early Hints](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103). React вызывает его даже когда подсказок о ресурсах нет. Содержимое заголовка ограничено `maxHeadersLength`.
    -   **опционально** `progressiveChunkSize`: Количество байт в чанке. [Подробнее об эвристике по умолчанию.](https://github.com/react/react/blob/14c2be8dac2d5482fda8a0906a31d239df8551fc/packages/react-server/src/ReactFizzServer.js#L210-L225)
    -   **опционально** `signal`: [Сигнал прерывания](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), который позволяет [прервать пререндер](#aborting-prerendering) и дорендерить остальное на клиенте.

#### Возвращаемое значение {#returns}

`prerender` возвращает промис:

-   Если рендеринг прошёл успешно, промис разрешится в объект, содержащий:
    -   `prelude`: [веб-поток](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) HTML. Этот поток можно использовать, чтобы отправлять ответ частями, или прочитать весь поток в строку.
    -   `postponed`: непрозрачный объект, сериализуемый в JSON, который можно передать в [`resume`](../server/resume.md), если `prerender` не завершился. Иначе `null`: это значит, что `prelude` содержит всё содержимое и продолжение не нужно.
-   Если рендеринг не удался, промис будет отклонён. [Используйте это, чтобы вывести резервную оболочку.](../server/renderToReadableStream.md#recovering-from-errors-inside-the-shell)

#### Предупреждения {#caveats}

`nonce` недоступен при пререндере. Nonce должен быть уникальным для каждого запроса, и если вы защищаете приложение с помощью [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP), включать значение nonce в сам пререндер было бы неуместно и небезопасно.

!!!note "Когда использовать `prerender`?"

    Статический API `prerender` используется для статической генерации на сервере (SSG). В отличие от `renderToString`, `prerender` ждёт загрузки всех данных, прежде чем разрешиться. Поэтому он подходит для генерации статического HTML целой страницы, включая данные, которые нужно получить с помощью Suspense. Чтобы передавать содержимое потоком по мере загрузки, используйте потоковый API серверного рендеринга (SSR), например [renderToReadableStream](../server/renderToReadableStream.md).

    `prerender` можно прервать и позже либо продолжить с помощью `resumeAndPrerender`, либо возобновить с помощью `resume`, чтобы поддержать частичный пререндер.

## Использование {#usage}

### Рендеринг дерева React в поток статического HTML {#rendering-a-react-tree-to-a-stream-of-static-html}

Вызовите `prerender`, чтобы отрендерить дерево React в статический HTML в [читаемый веб-поток:](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)

```js hl_lines="4 5"
import { prerender } from 'react-dom/static';

async function handler(request) {
  const {prelude} = await prerender(<App />, {
    bootstrapScripts: ['/main.js']
  });
  return new Response(prelude, {
    headers: { 'content-type': 'text/html' },
  });
}
```

Наряду с корневым компонентом нужно передать список путей к bootstrap-тегам `<script>`. Корневой компонент должен возвращать **весь документ, включая корневой тег `<html>`.**

Например, он может выглядеть так:

```js hl_lines="1"
export default function App() {
  return (
    <html>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="/styles.css"></link>
        <title>My app</title>
      </head>
      <body>
        <Router />
      </body>
    </html>
  );
}
```

React внедрит [doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) и ваши bootstrap-теги `<script>` в результирующий поток HTML:

```html hl_lines="5"
<!DOCTYPE html>
<html>
  <!-- ... HTML from your components ... -->
</html>
<script src="/main.js" async=""></script>
```

На клиенте bootstrap-скрипт должен [гидратировать весь `document` вызовом `hydrateRoot`:](../client/hydrateRoot.md#hydrating-an-entire-document)

```js hl_lines="4"
import { hydrateRoot } from 'react-dom/client';
import App from './App.js';

hydrateRoot(document, <App />);
```

Это прикрепит обработчики событий к статическому HTML, сгенерированному сервером, и сделает его интерактивным.

??? note "Чтение путей CSS и JS активов из выходных данных сборки"

    Итоговые URL активов (например, файлов JavaScript и CSS) часто хешируются после сборки. Например, вместо `styles.css` может получиться `styles.123456.css`. Хеширование имён файлов статических активов гарантирует, что каждая отдельная сборка одного и того же актива получит другое имя файла. Это полезно, потому что позволяет безопасно включить долгосрочное кэширование статических активов: файл с определённым именем никогда не изменит содержимое.

    Однако, если URL активов неизвестны до окончания сборки, поместить их в исходный код нельзя. Например, жёстко заданный в JSX путь `"/styles.css"`, как выше, не сработает. Чтобы не держать их в исходном коде, корневой компонент может читать настоящие имена файлов из карты, переданной пропсом:

    ```js hl_lines="1 6"
    export default function App({ assetMap }) {
      return (
        <html>
          <head>
            <title>My app</title>
            <link rel="stylesheet" href={assetMap['styles.css']}></link>
          </head>
          ...
        </html>
      );
    }
    ```

    На сервере отрендерьте `<App assetMap={assetMap} />` и передайте `assetMap` с URL активов:

    ```js hl_lines="1-5 8 9"
    // You'd need to get this JSON from your build tooling, e.g. read it from the build output.
    const assetMap = {
      'styles.css': '/styles.123456.css',
      'main.js': '/main.123456.js'
    };

    async function handler(request) {
      const {prelude} = await prerender(<App assetMap={assetMap} />, {
        bootstrapScripts: [assetMap['/main.js']]
      });
      return new Response(prelude, {
        headers: { 'content-type': 'text/html' },
      });
    }
    ```

    Поскольку сервер теперь рендерит `<App assetMap={assetMap} />`, на клиенте его тоже нужно рендерить с `assetMap`, чтобы не было ошибок гидратации. `assetMap` можно сериализовать и передать клиенту так:

    ```js hl_lines="9-10"
    // You'd need to get this JSON from your build tooling.
    const assetMap = {
      'styles.css': '/styles.123456.css',
      'main.js': '/main.123456.js'
    };

    async function handler(request) {
      const {prelude} = await prerender(<App assetMap={assetMap} />, {
        // Careful: It's safe to stringify() this because this data isn't user-generated.
        bootstrapScriptContent: `window.assetMap = ${JSON.stringify(assetMap)};`,
        bootstrapScripts: [assetMap['/main.js']],
      });
      return new Response(prelude, {
        headers: { 'content-type': 'text/html' },
      });
    }
    ```

    В примере выше опция `bootstrapScriptContent` добавляет дополнительный инлайн-тег `<script>`, который задаёт на клиенте глобальную переменную `window.assetMap`. Так клиентский код читает тот же `assetMap`:

    ```js hl_lines="4"
    import { hydrateRoot } from 'react-dom/client';
    import App from './App.js';

    hydrateRoot(document, <App assetMap={window.assetMap} />);
    ```

    И клиент, и сервер рендерят `App` с одним и тем же пропсом `assetMap`, поэтому ошибок гидратации нет.

### Рендеринг дерева React в строку статического HTML {#rendering-a-react-tree-to-a-string-of-static-html}

Вызовите `prerender`, чтобы отрендерить приложение в строку статического HTML:

```js
import { prerender } from 'react-dom/static';

async function renderToString() {
  const {prelude} = await prerender(<App />, {
    bootstrapScripts: ['/main.js']
  });

  const reader = prelude.getReader();
  let content = '';
  while (true) {
    const {done, value} = await reader.read();
    if (done) {
      return content;
    }
    content += Buffer.from(value).toString('utf8');
  }
}
```

Так вы получите первоначальный неинтерактивный HTML-вывод компонентов React. На клиенте нужно вызвать [`hydrateRoot`](../client/hydrateRoot.md), чтобы *гидратировать* этот сгенерированный сервером HTML и сделать его интерактивным.

### Ожидание загрузки всех данных {#waiting-for-all-data-to-load}

`prerender` ждёт загрузки всех данных, прежде чем закончить генерацию статического HTML и разрешиться. Например, рассмотрим страницу профиля с обложкой, боковой панелью с друзьями и фотографиями и списком записей:

```js
function ProfilePage() {
  return (
    <ProfileLayout>
      <ProfileCover />
      <Sidebar>
        <Friends />
        <Photos />
      </Sidebar>
      <Suspense fallback={<PostsGlimmer />}>
        <Posts />
      </Suspense>
    </ProfileLayout>
  );
}
```

Представьте, что `<Posts />` нужно загрузить данные, и это занимает время. В идеале стоит дождаться записей, чтобы они попали в HTML. Для этого можно использовать Suspense и приостановиться на данных: `prerender` дождётся завершения приостановленного содержимого, прежде чем разрешиться в статический HTML.

!!!note "Примечание"

    Приостанавливаются только данные, прочитанные из источника, который [активирует границу Suspense](../../react/Suspense.md#what-activates-a-suspense-boundary), например промис, прочитанный через [`use`](../../react/use.md). Suspense не замечает данные, полученные внутри Эффекта или обработчика события.

### Прерывание пререндера {#aborting-prerendering}

Пререндер можно заставить «сдаться» после таймаута:

```js hl_lines="2-5 11"
async function renderToString() {
  const controller = new AbortController();
  setTimeout(() => {
    controller.abort()
  }, 10000);

  try {
    // the prelude will contain all the HTML that was prerendered
    // before the controller aborted.
    const {prelude} = await prerender(<App />, {
      signal: controller.signal,
    });
    //...
```

Любые границы Suspense с незавершёнными дочерними элементами попадут в prelude в состоянии фолбэка.

Это можно использовать для частичного пререндера вместе с [`resume`](../server/resume.md) или [`resumeAndPrerender`](resumeAndPrerender.md).

## Устранение неполадок {#troubleshooting}

### Поток не начинается, пока не отрендерится всё приложение {#my-stream-doesnt-start-until-the-entire-app-is-rendered}

Ответ `prerender` ждёт, пока отрендерится всё приложение, включая разрешение всех границ Suspense, и только потом разрешается. Он предназначен для статической генерации сайта (SSG) заранее и не поддерживает потоковую передачу содержимого по мере загрузки.

Чтобы передавать содержимое потоком по мере загрузки, используйте потоковый API серверного рендеринга, например [renderToReadableStream](../server/renderToReadableStream.md).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/static/prerender](https://react.dev/reference/react-dom/static/prerender)</small>
