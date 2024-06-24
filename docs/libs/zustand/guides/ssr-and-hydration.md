# SSR и гидратация

## Рендеринг на стороне сервера (SSR)

Server-side Rendering (SSR) - это техника, которая помогает нам рендерить наши компоненты в HTML-строки на сервере, отправлять их непосредственно в браузер и, наконец, "гидратировать" статическую разметку в полностью интерактивное приложение на клиенте.

**React**

Допустим, мы хотим создать приложение без статических данных с помощью React. Для этого нам нужно использовать `express`, `react` и `react-dom/server`. Нам не нужен `react-dom/client`, поскольку это приложение stateless.

Давайте погрузимся в это:

-   `express` помогает нам создать веб-приложение, которое мы можем запустить с помощью Node,
-   `react` помогает нам создать компоненты пользовательского интерфейса, которые мы используем в нашем приложении,
-   `react-dom/server` помогает нам рендерить наши компоненты на сервере.

```json
// tsconfig.json
{
    "compilerOptions": {
        "noImplicitAny": false,
        "noEmitOnError": true,
        "removeComments": false,
        "sourceMap": true,
        "target": "esnext"
    },
    "include": ["**/*"]
}
```

> **Примечание:** не забудьте удалить все комментарии из файла `tsconfig.json`.

```tsx
// app.tsx
export const App = () => {
    return (
        <html>
            <head>
                <meta charSet="utf-8" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <title>
                    Static Server-side-rendered App
                </title>
            </head>
            <body>
                <div>Hello World!</div>
            </body>
        </html>
    );
};
```

```tsx
// server.tsx
import express from 'express';
import React from 'react';
import ReactDOMServer from 'react-dom/server';

import { App } from './app.tsx';

const port = Number.parseInt(
    process.env.PORT || '3000',
    10
);
const app = express();

app.get('/', (_, res) => {
    const { pipe } = ReactDOMServer.renderToPipeableStream(
        <App />,
        {
            onShellReady() {
                res.setHeader('content-type', 'text/html');
                pipe(res);
            },
        }
    );
});

app.listen(port, () => {
    console.log(`Server is listening at ${port}`);
});
```

```sh
tsc --build
```

```sh
node server.js
```

## Гидратация

Hydration превращает исходный HTML-снимок с сервера в полностью интерактивное приложение, запускаемое в браузере. Правильный способ "гидратации" компонента - использование `hydrateRoot`.

**React**

Допустим, мы хотим создать приложение с состоянием, используя React. Для этого нам нужно использовать `express`, `react`, `react-dom/server` и `react-dom/client`.

Давайте разберемся в этом:

-   `express` помогает нам создать веб-приложение, которое мы можем запустить с помощью Node,
-   `react` помогает нам создавать компоненты пользовательского интерфейса, которые мы используем в нашем приложении,
-   `react-dom/server` помогает нам рендерить наши компоненты на сервере,
-   `react-dom/client` помогает нам гидрировать наши компоненты на клиенте.

> **Примечание:** Не забывайте, что даже если мы можем визуализировать наши компоненты на сервере, важно "гидратировать" их на клиенте, чтобы сделать их интерактивными.

```json
// tsconfig.json
{
    "compilerOptions": {
        "noImplicitAny": false,
        "noEmitOnError": true,
        "removeComments": false,
        "sourceMap": true,
        "target": "esnext"
    },
    "include": ["**/*"]
}
```

> **Примечание:** не забудьте удалить все комментарии в файле `tsconfig.json`.

```tsx
// app.tsx
export const App = () => {
    return (
        <html>
            <head>
                <meta charSet="utf-8" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <title>
                    Static Server-side-rendered App
                </title>
            </head>
            <body>
                <div>Hello World!</div>
            </body>
        </html>
    );
};
```

```tsx
// main.tsx
import ReactDOMClient from 'react-dom/client';

import { App } from './app.tsx';

ReactDOMClient.hydrateRoot(<App />, document);
```

```tsx
// server.tsx
import express from 'express';
import React from 'react';
import ReactDOMServer from 'react-dom/server';

import { App } from './app.tsx';

const port = Number.parseInt(
    process.env.PORT || '3000',
    10
);
const app = express();

app.use('/', (_, res) => {
    const { pipe } = ReactDOMServer.renderToPipeableStream(
        <App />,
        {
            bootstrapScripts: ['/main.js'],
            onShellReady() {
                res.setHeader('content-type', 'text/html');
                pipe(res);
            },
        }
    );
});

app.listen(port, () => {
    console.log(`Server is listening at ${port}`);
});
```

```sh
tsc --build
```

```sh
node server.js
```

> **Предупреждение:** Дерево React, которое вы передаете в `hydrateRoot`, должно выдавать тот же результат, что и на сервере. Наиболее распространенные причины, приводящие к ошибкам гидратации, включают:
>
> -   Лишние пробельные символы (например, новые строки) вокруг сгенерированного React HTML внутри корневого узла.
> -   Использование проверок типа typeof window !== 'undefined' в логике рендеринга.
> -   Использование в логике рендеринга API, предназначенных только для браузера, например `window.matchMedia`.
> -   Рендеринг разных данных на сервере и клиенте.
>
> > React восстанавливается после некоторых ошибок гидратации, но вы должны исправлять их, как и другие ошибки. В лучшем случае они приведут к замедлению работы, в худшем - обработчики событий могут быть привязаны не к тем элементам.

Подробнее о предостережениях и подводных камнях можно прочитать здесь: [hydrateRoot](../../../reference/react-dom/client/hydrateRoot.md)

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/ssr-and-hydration></small>
