# renderToStaticMarkup

`renderToStaticMarkup` рендерит неинтерактивное дерево React в строку HTML.

```js
const html = renderToStaticMarkup(reactNode);
```

## Описание

### `renderToStaticMarkup(reactNode)`

На сервере вызовите `renderToStaticMarkup` для рендеринга вашего приложения в HTML.

```js
import { renderToStaticMarkup } from 'react-dom/server';

const html = renderToStaticMarkup(<Page />);
```

Он будет создавать неинтерактивный HTML-вывод ваших компонентов React.

#### Параметры

-   `reactNode`: Узел React, который вы хотите вывести в HTML. Например, JSX-узел типа `<Page />`.

#### Возвращает

HTML-строку.

#### Предупреждения

-   Вывод `renderToStaticMarkup` не может быть гидратирован.
-   `renderToStaticMarkup` имеет ограниченную поддержку Suspense. Если компонент приостанавливается, `renderToStaticMarkup` немедленно отправляет его обратный вывод как HTML.
-   `renderToStaticMarkup` работает в браузере, но использовать его в клиентском коде не рекомендуется. Если вам нужно перевести компонент в HTML в браузере, [получите HTML, переведя его в узел DOM](renderToString.md#removing-rendertostring-from-the-client-code).

## Использование

### Рендеринг неинтерактивного дерева React как HTML в строку

Вызовите `renderToStaticMarkup` для рендеринга вашего приложения в HTML-строку, которую вы можете отправить с ответом сервера:

```js
import { renderToStaticMarkup } from 'react-dom/server';

// The route handler syntax depends on your backend framework
app.use('/', (request, response) => {
    const html = renderToStaticMarkup(<Page />);
    response.send(html);
});
```

Это создаст первоначальный неинтерактивный HTML-вывод ваших компонентов React.

!!!warning ""

    Этот метод рендерит **неинтерактивный HTML, который не может быть гидратирован.** Это полезно, если вы хотите использовать React как простой генератор статических страниц, или если вы рендерите полностью статический контент, например, электронные письма.

    Интерактивные приложения должны использовать [`renderToString`](renderToString.md) на сервере и [`hydrateRoot`](client-hydrateRoot.md) на клиенте.
