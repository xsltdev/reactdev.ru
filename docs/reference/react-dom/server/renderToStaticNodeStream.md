---
description: renderToStaticNodeStream рендерит неинтерактивное дерево React в Node.js Readable Stream
---

# renderToStaticNodeStream

<big>`renderToStaticNodeStream` рендерит неинтерактивное дерево React в [Node.js Readable Stream](https://nodejsdev.ru/api/stream/#streamreadable).</big>

```js
const stream = renderToStaticNodeStream(reactNode);
```

## Описание {#reference}

### `renderToStaticNodeStream(reactNode)` {#rendertostaticnodestream}

На сервере вызовите `renderToStaticNodeStream`, чтобы получить [Node.js Readable Stream](https://nodejsdev.ru/api/stream/#streamreadable).

```js
import { renderToStaticNodeStream } from 'react-dom/server';

const stream = renderToStaticNodeStream(<Page />);
stream.pipe(response);
```

Поток будет производить неинтерактивный HTML вывод ваших React компонентов.

**Параметры**

-   `reactNode`: Узел React, который вы хотите вывести в HTML. Например, JSX-элемент типа `<Page />`.

**Возвращает**

[Node.js Readable Stream](https://nodejsdev.ru/api/stream/#streamreadable), который выводит строку HTML. Полученный HTML не может быть гидирован на клиенте.

**Предостережения**

-   Вывод `renderToStaticNodeStream` не может быть гидратирован.
-   Этот метод будет ждать завершения всех [Suspense boundaries](../../react/Suspense.md), прежде чем вернуть любой вывод.
-   Начиная с React 18, этот метод буферизирует весь свой вывод, поэтому он не предоставляет никаких преимуществ потоковой передачи.
-   Возвращаемый поток - это поток байтов, закодированный в utf-8. Если вам нужен поток в другой кодировке, обратите внимание на проект типа [iconv-lite](https://www.npmjs.com/package/iconv-lite), который предоставляет потоки преобразования для перекодировки текста.

## Использование {#usage}

### Рендеринг дерева React как статического HTML в поток Node.js для чтения {#rendering-a-react-tree-as-static-html-to-a-nodejs-readable-stream}

Вызовите `renderToStaticNodeStream` для получения [Node.js Readable Stream](https://nodejsdev.ru/api/stream/#streamreadable), который вы можете направить в ответ вашего сервера:

```js
import { renderToStaticNodeStream } from 'react-dom/server';

// The route handler syntax depends on your backend framework
app.use('/', (request, response) => {
    const stream = renderToStaticNodeStream(<Page />);
    stream.pipe(response);
});
```

Поток будет производить первоначальный неинтерактивный HTML-вывод ваших компонентов React.

!!!warning ""

    Этот метод рендерит **неинтерактивный HTML, который не может быть гидратирован.** Это полезно, если вы хотите использовать React как простой генератор статических страниц, или если вы рендерите полностью статический контент, например, электронные письма.

    Интерактивные приложения должны использовать [`renderToPipeableStream`](renderToPipeableStream.md) на сервере и [`hydrateRoot`](../client/hydrateRoot.md) на клиенте.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/server/renderToStaticNodeStream></small>
