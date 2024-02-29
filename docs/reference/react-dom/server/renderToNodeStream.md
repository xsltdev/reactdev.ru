---
status: deprecated
---

# renderToNodeStream

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React. Вместо него используйте [`renderToPipeableStream`](renderToPipeableStream.md).

`renderToNodeStream` рендерит дерево React в [Node.js Readable Stream.](https://nodejsdev.ru/api/stream/#readable-streams).

```js
const stream = renderToNodeStream(reactNode);
```

## Описание

### `renderToNodeStream(reactNode)`

На сервере вызовите `renderToNodeStream`, чтобы получить [Node.js Readable Stream](https://nodejsdev.ru/api/stream/#readable-streams), который вы можете передать в ответ.

```js
import { renderToNodeStream } from 'react-dom/server';

const stream = renderToNodeStream(<App />);
stream.pipe(response);
```

На клиенте вызовите [`hydrateRoot`](../client/hydrateRoot.md), чтобы сделать сгенерированный сервером HTML интерактивным.

#### Параметры

-   `reactNode`: Узел React, который вы хотите отобразить в HTML. Например, JSX-элемент типа `<App />`.

#### Возвращает

[Node.js Readable Stream](https://nodejsdev.ru/api/stream/#readable-streams), который выводит строку HTML.

#### Ограничения

-   Этот метод будет ждать завершения всех [Suspense boundaries](../../react/Suspense.md), прежде чем вернуть любой вывод.
-   Начиная с React 18, этот метод буферизирует весь свой вывод, поэтому он не обеспечивает никаких преимуществ потоковой передачи. Поэтому рекомендуется вместо него перейти на [`renderToPipeableStream`](renderToPipeableStream.md).
-   Возвращаемый поток - это поток байтов, закодированный в utf-8. Если вам нужен поток в другой кодировке, обратите внимание на проект типа [iconv-lite](https://www.npmjs.com/package/iconv-lite), который предоставляет потоки преобразования для перекодировки текста.

## Использование

### Рендеринг дерева React в формате HTML в читаемый поток Node.js

Вызовите `renderToNodeStream` для получения [Node.js Readable Stream](https://nodejsdev.ru/api/stream/#readable-streams), который вы можете направить в ответ вашего сервера:

```js
import { renderToNodeStream } from 'react-dom/server';

// The route handler syntax depends on your backend framework
app.use('/', (request, response) => {
    const stream = renderToNodeStream(<App />);
    stream.pipe(response);
});
```

Этот поток будет создавать первоначальный неинтерактивный HTML-вывод ваших компонентов React. На клиенте вам нужно будет вызвать [`hydrateRoot`](../client/hydrateRoot.md), чтобы _гидратировать_ этот сгенерированный сервером HTML и сделать его интерактивным.
