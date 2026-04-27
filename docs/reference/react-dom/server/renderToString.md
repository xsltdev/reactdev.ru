---
description: renderToString преобразует дерево React в строку HTML
---

# renderToString

!!!warning ""

    `renderToString` не поддерживает потоковую передачу или ожидание данных.

<big>`renderToString` преобразует дерево React в строку HTML.</big>

```js
const html = renderToString(reactNode);
```

## Описание {#reference}

### `renderToString(reactNode)` {#rendertostaticnodestream}

На сервере вызовите `renderToString` для рендеринга вашего приложения в HTML.

```js
import { renderToString } from 'react-dom/server';

const html = renderToString(<App />);
```

На клиенте вызовите [`hydrateRoot`](../client/hydrateRoot.md), чтобы сделать сгенерированный сервером HTML интерактивным.

**Параметры**

-   `reactNode`: Узел React, который вы хотите преобразовать в HTML. Например, JSX-узел типа `<App />`.

**Возвращает**

HTML-строку.

**Предостережения**

-   `renderToString` имеет ограниченную поддержку приостановки. Если компонент приостанавливается, `renderToString` немедленно отправляет его обратную версию как HTML.
-   `renderToString` работает в браузере, но использовать его в клиентском коде не рекомендуется.

## Использование {#usage}

### Рендеринг дерева React как HTML в строку {#rendering-a-react-tree-as-static-html-to-a-nodejs-readable-stream}

Вызовите `renderToString` для рендеринга вашего приложения в HTML-строку, которую вы можете отправить с ответом сервера:

```js
import { renderToString } from 'react-dom/server';

// The route handler syntax depends on your backend framework
app.use('/', (request, response) => {
    const html = renderToString(<App />);
    response.send(html);
});
```

Это создаст первоначальный неинтерактивный HTML-вывод ваших компонентов React. На клиенте вам нужно будет вызвать [`hydrateRoot`](../client/hydrateRoot.md), чтобы _гидратировать_ этот сгенерированный сервером HTML и сделать его интерактивным.

!!!warning ""

    `renderToString` не поддерживает потоковую передачу или ожидание данных.

## Альтернативы

### Переход от `renderToString` к потоковому методу на сервере

`renderToString` возвращает строку немедленно, поэтому он не поддерживает потоковую передачу или ожидание данных.

Когда это возможно, мы рекомендуем использовать эти полнофункциональные альтернативы:

-   Если вы используете Node.js, используйте [`renderToPipeableStream`.](renderToPipeableStream.md)
-   Если вы используете Deno или современную edge runtime с [Web Streams](https://developer.mozilla.org/docs/Web/API/Streams_API), используйте [`renderToReadableStream`](renderToReadableStream.md).

Вы можете продолжать использовать `renderToString`, если ваше серверное окружение не поддерживает потоки.

### Удаление `renderToString` из кода клиента {#removing-rendertostring-from-the-client-code}

Иногда `renderToString` используется на клиенте для преобразования какого-либо компонента в HTML.

```js
// 🚩 Unnecessary: using renderToString on the client
import { renderToString } from 'react-dom/server';

const html = renderToString(<MyIcon />);
console.log(html); // For example, "<svg>...</svg>"
```

Импорт `react-dom/server` **на клиенте** неоправданно увеличивает размер вашего пакета и его следует избегать. Если вам нужно вывести какой-то компонент в HTML в браузере, используйте [`createRoot`](../client/createRoot.md) и читайте HTML из DOM:

```js
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';

const div = document.createElement('div');
const root = createRoot(div);
flushSync(() => {
    root.render(<MyIcon />);
});
console.log(div.innerHTML); // For example, "<svg>...</svg>"
```

Вызов [`flushSync`](../flushSync.md) необходим для того, чтобы DOM был обновлен до чтения его свойства [`innerHTML`](https://developer.mozilla.org/docs/Web/API/Element/innerHTML).

## Устранение неполадок

### Когда компонент приостанавливает работу, HTML всегда содержит обратный ход

`renderToString` не полностью поддерживает Suspense.

Если какой-то компонент приостанавливается (например, потому что он определен с помощью [`lazy`](../../react/lazy.md) или получает данные), `renderToString` не будет ждать, пока его содержимое разрешится. Вместо этого `renderToString` найдет ближайшую границу [`<Suspense>`](../../react/Suspense.md) над ним и отобразит его `fallback` prop в HTML. Содержимое не появится до тех пор, пока не загрузится клиентский код.

Чтобы решить эту проблему, используйте одно из рекомендуемых потоковых решений. Они могут передавать содержимое частями по мере его разрешения на сервере, чтобы пользователь видел, как страница постепенно заполняется до загрузки клиентского кода.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/server/renderToStaticNodeStream></small>
