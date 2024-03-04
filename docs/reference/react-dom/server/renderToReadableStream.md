---
description: renderToReadableStream рендерит дерево React в Readable Web Stream
---

# renderToReadableStream

<big>`renderToReadableStream` рендерит дерево React в [Readable Web Stream](https://developer.mozilla.org/docs/Web/API/ReadableStream).</big>

```js
const stream = await renderToReadableStream(reactNode, options?)
```

!!!note ""

    Этот API зависит от [Web Streams](https://developer.mozilla.org/docs/Web/API/Streams_API). Для Node.js используйте [`renderToPipeableStream`](renderToPipeableStream.md) вместо этого.

## Описание {#reference}

### `renderToReadableStream(reactNode, options?)` {#rendertoreadablestream}

Вызовите `renderToReadableStream` для рендеринга вашего дерева React в формате HTML в [читаемый веб-поток](https://developer.mozilla.org/docs/Web/API/ReadableStream).

```js
import { renderToReadableStream } from 'react-dom/server';

async function handler(request) {
    const stream = await renderToReadableStream(<App />, {
        bootstrapScripts: ['/main.js'],
    });
    return new Response(stream, {
        headers: { 'content-type': 'text/html' },
    });
}
```

На клиенте вызовите [`hydrateRoot`](../client/hydrateRoot.md), чтобы сделать сгенерированный сервером HTML интерактивным.

**Параметры**

-   `reactNode`: Узел React, который вы хотите отобразить в HTML. Например, JSX-элемент типа `<App />`. Ожидается, что он будет представлять весь документ, поэтому компонент `App` должен вывести тег `<html>`.
-   **опционально** `options`: Объект с опциями потоковой передачи.
    -   **опционально** `bootstrapScriptContent`: Если указано, то эта строка будет помещена в инлайн тег `<script>`.
    -   **опционально** `bootstrapScripts`: Массив URL строк для тегов `<script>`, которые будут отображаться на странице. Используйте его для включения `<script>`, вызывающего [`hydrateRoot`](../client/hydrateRoot.md) Опустите его, если вы вообще не хотите запускать React на клиенте.
    -   **опционально** `bootstrapModules`: Аналогично `bootstrapScripts`, но вместо него выдается [`<script type="module">`](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Modules).
    -   **опционально** `identifierPrefix`: Строковый префикс, который React использует для идентификаторов, генерируемых [`useId`](../../react/useId.md) Полезно для предотвращения конфликтов при использовании нескольких корней на одной странице. Должен быть тем же префиксом, что передан в [`hydrateRoot`](../client/hydrateRoot.md#parameters)
    -   **опционально** `namespaceURI`: Строка с корневым [namespace URI](https://developer.mozilla.org/docs/Web/API/Document/createElementNS#important_namespace_uris) для потока. По умолчанию используется обычный HTML. Передайте `'http://www.w3.org/2000/svg'` для SVG или `'http://www.w3.org/1998/Math/MathML'` для MathML.
    -   **опционально** `nonce`: Строка [`nonce`](http://developer.mozilla.org/docs/Web/HTML/Element/script#nonce) для разрешения скриптов для [`script-src` Content-Security-Policy](https://developer.mozilla.org/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).
    -   **опционально** `onError`: Обратный вызов, который срабатывает всякий раз, когда происходит ошибка сервера, будь то восстанавливаемая или нет По умолчанию, он вызывает только `console.error`. Если вы переопределите его для регистрации сообщений о сбоях, убедитесь, что вы все еще вызываете `console.error`. Вы также можете использовать его для настройки кода состояния перед выдачей оболочки.
    -   **опционально** `progressiveChunkSize`: Количество байт в чанке. [Подробнее об эвристике по умолчанию.](https://github.com/facebook/react/blob/14c2be8dac2d5482fda8a0906a31d239df8551fc/packages/react-server/src/ReactFizzServer.js#L210-L225)
    -   **опционально** `signal`: Сигнал [прерывания](https://developer.mozilla.org/docs/Web/API/AbortSignal), который позволяет вам прервать серверный рендеринг и отрисовать все остальное на клиенте.

**Возвращает**

`renderToReadableStream` возвращает промис:

-   Если рендеринг оболочки прошел успешно, этот промис будет разрешен в [Readable Web Stream](https://developer.mozilla.org/docs/Web/API/ReadableStream).
-   Если рендеринг оболочки не удался, промис будет отклонен. Используйте это для вывода резервной оболочки.

Возвращаемый поток имеет дополнительное свойство:

-   `allReady`: Обещание, которое разрешается, когда весь рендеринг завершен, включая оболочку и весь дополнительный контент. Вы можете `дождаться stream.allReady` перед возвращением ответа для краулеров и статической генерации. Если вы сделаете это, вы не получите никакой прогрессивной загрузки. Поток будет содержать конечный HTML.

## Использование {#usage}

### Рендеринг дерева React в формате HTML в читаемый веб-поток {#rendering-a-react-tree-as-html-to-a-readable-web-stream}

Вызовите `renderToReadableStream` для рендеринга вашего дерева React в формате HTML в [Readable Web Stream:](https://developer.mozilla.org/docs/Web/API/ReadableStream)

```js
import { renderToReadableStream } from 'react-dom/server';

async function handler(request) {
    const stream = await renderToReadableStream(<App />, {
        bootstrapScripts: ['/main.js'],
    });
    return new Response(stream, {
        headers: { 'content-type': 'text/html' },
    });
}
```

Наряду с корневым компонентом, вам необходимо предоставить список путей к `<script>` бутстрапа. Ваш корневой компонент должен возвращать **весь документ, включая корневой тег `<html>`.**.

Например, это может выглядеть следующим образом:

```js
export default function App() {
    return (
        <html>
            <head>
                <meta charSet="utf-8" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <link
                    rel="stylesheet"
                    href="/styles.css"
                ></link>
                <title>My app</title>
            </head>
            <body>
                <Router />
            </body>
        </html>
    );
}
```

React внедрит [doctype](https://developer.mozilla.org/docs/Glossary/Doctype) и ваши теги bootstrap `<script>` в результирующий поток HTML:

```html
<!DOCTYPE html>
<html>
    <!-- ... HTML from your components ... -->
</html>
<script src="/main.js" async=""></script>
```

На клиенте ваш скрипт bootstrap должен [гидратировать весь `документ` с помощью вызова `hydrateRoot`:](../client/hydrateRoot.md#hydrating-an-entire-document)

```js
import { hydrateRoot } from 'react-dom/client';
import App from './App.js';

hydrateRoot(document, <App />);
```

Это позволит прикрепить слушателей событий к генерируемому сервером HTML и сделать его интерактивным.

!!!note "Чтение путей CSS и JS активов из выходных данных сборки"

    URL конечных активов (например, файлов JavaScript и CSS) часто хэшируются после сборки. Например, вместо `styles.css` вы можете получить `styles.123456.css`. Хеширование имен файлов статических активов гарантирует, что каждая отдельная сборка одного и того же актива будет иметь другое имя файла. Это полезно, поскольку позволяет безопасно включить долгосрочное кэширование для статических активов: файл с определенным именем никогда не изменит содержимое.

    Однако, если вы не знаете URL-адреса активов до окончания сборки, у вас нет возможности поместить их в исходный код. Например, жесткое кодирование `"/styles.css"` в JSX, как это было ранее, не сработает. Чтобы они не попадали в исходный код, ваш корневой компонент может считывать реальные имена файлов из карты, передаваемой в качестве пропса:

    ```js
    export default function App({ assetMap }) {
    	return (
    		<html>
    			<head>
    				<title>My app</title>
    				<link
    					rel="stylesheet"
    					href={assetMap['styles.css']}
    				></link>
    			</head>
    			...
    		</html>
    	);
    }
    ```

    На сервере выполните рендеринг `<App assetMap={assetMap} />` и передайте вашему `assetMap` URLs активов:

    ```js
    // You'd need to get this JSON from your build tooling, e.g. read it from the build output.
    const assetMap = {
    	'styles.css': '/styles.123456.css',
    	'main.js': '/main.123456.js',
    };

    async function handler(request) {
    	const stream = await renderToReadableStream(
    		<App assetMap={assetMap} />,
    		{
    			bootstrapScripts: [assetMap['/main.js']],
    		}
    	);
    	return new Response(stream, {
    		headers: { 'content-type': 'text/html' },
    	});
    }
    ```

    Поскольку ваш сервер теперь рендерит `<App assetMap={assetMap} />`, вам нужно отобразить его с `assetMap` на клиенте, чтобы избежать ошибок гидратации. Вы можете сериализовать и передать `assetMap` клиенту следующим образом:

    ```js
    // You'd need to get this JSON from your build tooling.
    const assetMap = {
    	'styles.css': '/styles.123456.css',
    	'main.js': '/main.123456.js',
    };

    async function handler(request) {
    	const stream = await renderToReadableStream(
    		<App assetMap={assetMap} />,
    		{
    			// Careful: It's safe to stringify() this because this data isn't user-generated.
    			bootstrapScriptContent: `window.assetMap = ${JSON.stringify(
    				assetMap
    			)};`,
    			bootstrapScripts: [assetMap['/main.js']],
    		}
    	);
    	return new Response(stream, {
    		headers: { 'content-type': 'text/html' },
    	});
    }
    ```

    В примере выше опция `bootstrapScriptContent` добавляет дополнительный встроенный тег `<script>`, который устанавливает глобальную переменную `window.assetMap` на клиенте. Это позволяет клиентскому коду читать ту же самую `assetMap`:

    ```js
    import { hydrateRoot } from 'react-dom/client';
    import App from './App.js';

    hydrateRoot(document, <App assetMap={window.assetMap} />);
    ```

    И клиент, и сервер рендерят `App` с одним и тем же пропсом `assetMap`, поэтому ошибок гидратации нет.

### Потоковая передача контента по мере его загрузки {#streaming-more-content-as-it-loads}

Потоковая передача позволяет пользователю начать видеть содержимое еще до того, как все данные загрузятся на сервер. Например, рассмотрим страницу профиля, на которой отображается обложка, боковая панель с друзьями и фотографиями, а также список сообщений:

```js
function ProfilePage() {
    return (
        <ProfileLayout>
            <ProfileCover />
            <Sidebar>
                <Friends />
                <Photos />
            </Sidebar>
            <Posts />
        </ProfileLayout>
    );
}
```

Представьте, что загрузка данных для `<Posts />` занимает некоторое время. В идеале вы хотели бы показать пользователю остальную часть содержимого страницы профиля, не дожидаясь сообщений. Для этого [оберните `Posts` в границу `<Suspense>`:](../../react/Suspense.md#displaying-a-fallback-while-content-is-loading)

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

Это указывает React начать передачу HTML до того, как `Posts` загрузит свои данные. Сначала React отправит HTML для резервной загрузки (`PostsGlimmer`), а затем, когда `Posts` закончит загрузку своих данных, React отправит оставшийся HTML вместе со встроенным тегом `<script>`, который заменит резервную загрузку этим HTML. С точки зрения пользователя, на странице сначала появится `PostsGlimmer`, а затем его заменит `Posts`.

Вы можете далее [вложить границы `<Suspense>`](../../react/Suspense.md#revealing-nested-content-as-it-loads) для создания более детальной последовательности загрузки:

```js
function ProfilePage() {
    return (
        <ProfileLayout>
            <ProfileCover />
            <Suspense fallback={<BigSpinner />}>
                <Sidebar>
                    <Friends />
                    <Photos />
                </Sidebar>
                <Suspense fallback={<PostsGlimmer />}>
                    <Posts />
                </Suspense>
            </Suspense>
        </ProfileLayout>
    );
}
```

В этом примере React может начать потоковую передачу страницы даже раньше. Только `ProfileLayout` и `ProfileCover` должны закончить рендеринг первыми, потому что они не обернуты в какую-либо границу `<Suspense>`. Однако, если `Sidebar`, `Friends` или `Photos` потребуется загрузить некоторые данные, React отправит HTML для фалбэка `BigSpinner` вместо них. Затем, по мере поступления данных, все большее количество содержимого будет продолжать отображаться, пока все не станет видимым.

Потоковая передача данных не требует ожидания загрузки самого React в браузере или интерактивности вашего приложения. HTML-содержимое с сервера будет постепенно раскрываться до загрузки любого из тегов `<script>`.

[Подробнее о том, как работает потоковый HTML.](https://github.com/reactwg/react-18/discussions/37)

!!!note ""

    **Только источники данных с поддержкой Suspense активируют компонент Suspense.** К ним относятся:

    -   Получение данных с помощью фреймворков с поддержкой Suspense, таких как [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) и [Next.js](https://nextjs.org/docs/getting-started/react-essentials).
    -   Ленивая загрузка кода компонента с помощью [`lazy`](../../react/lazy.md).

    Suspense **не** обнаруживает, когда данные извлекаются внутри Effect или обработчика события.

    Точный способ загрузки данных в компонент `Posts`, описанный выше, зависит от вашего фреймворка. Если вы используете фреймворк с поддержкой Suspense, вы найдете подробности в документации по получению данных.

    Получение данных с поддержкой Suspense без использования фреймворка с поддержкой мнений пока не поддерживается. Требования к реализации источника данных с поддержкой Suspense нестабильны и не документированы. Официальный API для интеграции источников данных с Suspense будет выпущен в одной из будущих версий React.

### Указание того, что входит в оболочку {#specifying-what-goes-into-the-shell}

Часть вашего приложения вне границ `<Suspense>` называется _оболочкой:_

```js
function ProfilePage() {
    return (
        <ProfileLayout>
            <ProfileCover />
            <Suspense fallback={<BigSpinner />}>
                <Sidebar>
                    <Friends />
                    <Photos />
                </Sidebar>
                <Suspense fallback={<PostsGlimmer />}>
                    <Posts />
                </Suspense>
            </Suspense>
        </ProfileLayout>
    );
}
```

Он определяет самое раннее состояние загрузки, которое может увидеть пользователь:

```js
<ProfileLayout>
    <ProfileCover />
    <BigSpinner />
</ProfileLayout>
```

Если вы обернете все приложение в границу `<Suspense>` в корне, оболочка будет содержать только этот спиннер. Однако это не очень приятно для пользователя, потому что видеть большой спиннер на экране может показаться более медленным и раздражающим, чем подождать еще немного и увидеть реальный макет. Вот почему обычно вы хотите разместить границы `<Suspense>` так, чтобы оболочка казалась _минимальной, но полной_ - как скелет всего макета страницы.

Асинхронный вызов `renderToReadableStream` разрешится в `поток`, как только вся оболочка будет отрисована. Обычно вы начинаете потоковую передачу, создавая и возвращая ответ с этим `потоком`:

```js
async function handler(request) {
    const stream = await renderToReadableStream(<App />, {
        bootstrapScripts: ['/main.js'],
    });
    return new Response(stream, {
        headers: { 'content-type': 'text/html' },
    });
}
```

К моменту возврата `stream`, компоненты во вложенных границах `<Suspense>` могут все еще загружать данные.

### Протоколирование аварий на сервере {#logging-crashes-on-the-server}

По умолчанию все ошибки на сервере записываются в консоль. Вы можете переопределить это поведение для записи отчетов о сбоях:

```js
async function handler(request) {
    const stream = await renderToReadableStream(<App />, {
        bootstrapScripts: ['/main.js'],
        onError(error) {
            console.error(error);
            logServerCrashReport(error);
        },
    });
    return new Response(stream, {
        headers: { 'content-type': 'text/html' },
    });
}
```

Если вы предоставляете пользовательскую реализацию `onError`, не забудьте также вести журнал ошибок в консоль, как описано выше.

### Восстановление после ошибок внутри оболочки {#recovering-from-errors-inside-the-shell}

В этом примере оболочка содержит `ProfileLayout`, `ProfileCover` и `PostsGlimmer`:

```js
function ProfilePage() {
    return (
        <ProfileLayout>
            <ProfileCover />
            <Suspense fallback={<PostsGlimmer />}>
                <Posts />
            </Suspense>
        </ProfileLayout>
    );
}
```

Если при рендеринге этих компонентов произойдет ошибка, у React не будет никакого осмысленного HTML для отправки клиенту. Оберните вызов `renderToReadableStream` в `try...catch` для отправки резервного HTML, который не полагается на серверный рендеринг в качестве последнего средства:

```js
async function handler(request) {
    try {
        const stream = await renderToReadableStream(
            <App />,
            {
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        return new Response(stream, {
            headers: { 'content-type': 'text/html' },
        });
    } catch (error) {
        return new Response(
            '<h1>Something went wrong</h1>',
            {
                status: 500,
                headers: { 'content-type': 'text/html' },
            }
        );
    }
}
```

Если при генерации оболочки произошла ошибка, сработает и `onError`, и ваш блок `catch`. Используйте `onError` для сообщения об ошибке и используйте блок `catch` для отправки резервного HTML-документа. Ваш резервный HTML не обязательно должен быть страницей ошибки. Вместо этого вы можете включить альтернативную оболочку, которая отображает ваше приложение только на клиенте.

### Восстановление после ошибок вне оболочки {#recovering-from-errors-outside-the-shell}

В этом примере компонент `<Posts />` обернут в `<Suspense>`, поэтому он _не_ является частью оболочки:

```js
function ProfilePage() {
    return (
        <ProfileLayout>
            <ProfileCover />
            <Suspense fallback={<PostsGlimmer />}>
                <Posts />
            </Suspense>
        </ProfileLayout>
    );
}
```

Если ошибка произойдет в компоненте `Posts` или где-то внутри него, React [попытается восстановиться после нее:](../../react/Suspense.md#providing-a-fallback-for-server-errors-and-server-only-content)

1.  Выдаст в HTML фаллбэк загрузки для ближайшей границы `<Suspense>` (`PostsGlimmer`).
2.  Он "откажется" от попыток рендеринга содержимого `Posts` на сервере.
3.  Когда код JavaScript загрузится на клиенте, React _повторит_ рендеринг `Posts` на клиенте.

Если повторная попытка рендеринга `Posts` на клиенте _также_ не удалась, React выбросит ошибку на клиент. Как и для всех ошибок, возникающих во время рендеринга, [ближайшая родительская граница ошибки](../../react/Component.md#static-getderivedstatefromerror) определяет, как представить ошибку пользователю. На практике это означает, что пользователь будет видеть индикатор загрузки до тех пор, пока не будет уверен, что ошибка не может быть устранена.

Если повторная попытка рендеринга `Posts` на клиенте будет успешной, индикатор загрузки с сервера будет заменен на вывод клиентского рендеринга. Пользователь не будет знать, что произошла ошибка сервера. Однако обратный вызов сервера `onError` и обратный вызов клиента [`onRecoverableError`](../client/hydrateRoot.md#hydrateroot) сработают, чтобы вы могли получить уведомление об ошибке.

### Установка кода состояния {#setting-the-status-code}

При потоковой передаче возникает компромисс. Вы хотите начать потоковую передачу страницы как можно раньше, чтобы пользователь мог быстрее увидеть содержимое. Однако после начала потоковой передачи вы больше не сможете установить код состояния ответа.

Разделив приложение на оболочку (выше всех границ `<Suspense>`) и остальное содержимое, вы уже решили часть этой проблемы. Если оболочка ошибется, будет запущен ваш блок `catch`, который позволит вам установить код состояния ошибки. В противном случае вы знаете, что приложение может восстановиться на клиенте, поэтому вы можете послать "OK".

```js
async function handler(request) {
    try {
        const stream = await renderToReadableStream(
            <App />,
            {
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        return new Response(stream, {
            status: 200,
            headers: { 'content-type': 'text/html' },
        });
    } catch (error) {
        return new Response(
            '<h1>Something went wrong</h1>',
            {
                status: 500,
                headers: { 'content-type': 'text/html' },
            }
        );
    }
}
```

Если компонент _за пределами_ оболочки (т.е. внутри границы `<Suspense>`) выдаст ошибку, React не остановит рендеринг. Это означает, что обратный вызов `onError` сработает, но ваш код продолжит выполняться, не попадая в блок `catch`. Это происходит потому, что React попытается восстановиться после этой ошибки на клиенте, как описано выше.

Однако, если вы хотите, вы можете использовать факт ошибки для установки кода состояния:

```js
async function handler(request) {
    try {
        let didError = false;
        const stream = await renderToReadableStream(
            <App />,
            {
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    didError = true;
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        return new Response(stream, {
            status: didError ? 500 : 200,
            headers: { 'content-type': 'text/html' },
        });
    } catch (error) {
        return new Response(
            '<h1>Something went wrong</h1>',
            {
                status: 500,
                headers: { 'content-type': 'text/html' },
            }
        );
    }
}
```

Это позволит отловить только те ошибки вне оболочки, которые возникли при генерации начального содержимого оболочки, так что этот способ не является исчерпывающим. Если знать, произошла ли ошибка для какого-то содержимого, очень важно, вы можете перенести ее в оболочку.

### Обработка различных ошибок различными способами {#handling-different-errors-in-different-ways}

Вы можете [создавать собственные подклассы `Error`](https://javascript.info/custom-errors) и использовать оператор [`instanceof`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/instanceof) для проверки того, какая ошибка была выброшена. Например, вы можете определить пользовательскую `NotFoundError` и выбросить ее из вашего компонента. Затем вы можете сохранить ошибку в `onError` и сделать что-то другое перед возвратом ответа в зависимости от типа ошибки:

```js
async function handler(request) {
    let didError = false;
    let caughtError = null;

    function getStatusCode() {
        if (didError) {
            if (caughtError instanceof NotFoundError) {
                return 404;
            } else {
                return 500;
            }
        } else {
            return 200;
        }
    }

    try {
        const stream = await renderToReadableStream(
            <App />,
            {
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    didError = true;
                    caughtError = error;
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        return new Response(stream, {
            status: getStatusCode(),
            headers: { 'content-type': 'text/html' },
        });
    } catch (error) {
        return new Response(
            '<h1>Something went wrong</h1>',
            {
                status: getStatusCode(),
                headers: { 'content-type': 'text/html' },
            }
        );
    }
}
```

Имейте в виду, что после эмиссии оболочки и начала потоковой передачи вы не сможете изменить код состояния.

### Ожидание загрузки всего содержимого для краулеров и статической генерации {#waiting-for-all-content-to-load-for-crawlers-and-static-generation}

Потоковая передача обеспечивает лучший пользовательский опыт, поскольку пользователь может видеть содержимое по мере его появления.

Однако, когда краулер посещает вашу страницу, или если вы генерируете страницы во время сборки, вы можете захотеть сначала позволить всему содержимому загрузиться, а затем создать окончательный HTML-вывод вместо того, чтобы раскрывать его постепенно.

Вы можете дождаться загрузки всего содержимого, ожидая выполнения промиса `stream.allReady`:

```js
async function handler(request) {
    try {
        let didError = false;
        const stream = await renderToReadableStream(
            <App />,
            {
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    didError = true;
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        let isCrawler = true; // ... depends on your bot detection strategy ...
        if (isCrawler) {
            await stream.allReady;
        }
        return new Response(stream, {
            status: didError ? 500 : 200,
            headers: { 'content-type': 'text/html' },
        });
    } catch (error) {
        return new Response(
            '<h1>Something went wrong</h1>',
            {
                status: 500,
                headers: { 'content-type': 'text/html' },
            }
        );
    }
}
```

Обычный посетитель получит поток постепенно загружаемого содержимого. Краулер получит окончательный HTML-вывод после загрузки всех данных. Однако это также означает, что краулеру придется ждать _все_ данные, некоторые из которых могут загружаться медленно или с ошибками. В зависимости от вашего приложения, вы можете выбрать вариант отправки оболочки краулерам.

### Прерывание рендеринга сервера {#aborting-server-rendering}

Вы можете заставить серверный рендеринг "сдаться" после таймаута:

```js
async function handler(request) {
    try {
        const controller = new AbortController();
        setTimeout(() => {
            controller.abort();
        }, 10000);

        const stream = await renderToReadableStream(
            <App />,
            {
                signal: controller.signal,
                bootstrapScripts: ['/main.js'],
                onError(error) {
                    didError = true;
                    console.error(error);
                    logServerCrashReport(error);
                },
            }
        );
        // ...
    }
}
```

React пропустит оставшиеся фаллаверы загрузки как HTML, а остальные попытается отобразить на клиенте.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/server/renderToReadableStream></small>
