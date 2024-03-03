---
description: hydrateRoot позволяет отображать компоненты React внутри узла DOM браузера, HTML-содержимое которого было предварительно сгенерировано react-dom/server
---

# hydrateRoot

<big>`hydrateRoot` позволяет отображать компоненты React внутри узла DOM браузера, HTML-содержимое которого было предварительно сгенерировано [`react-dom/server`](../server/index.md).</big>

```js
const root = hydrateRoot(domNode, reactNode, options?)
```

## Описание {#reference}

### `hydrateRoot(domNode, reactNode, options?)` {#hydrateroot}

Вызов `hydrateRoot` для "прикрепления" React к существующему HTML, который уже был отрисован React в серверной среде.

```js
import { hydrateRoot } from 'react-dom/client';

const domNode = document.getElementById('root');
const root = hydrateRoot(domNode, reactNode);
```

React подключится к HTML, существующему внутри `domNode`, и возьмет на себя управление DOM внутри него. Приложение, полностью построенное на React, обычно имеет только один вызов `hydrateRoot` с корневым компонентом.

**Параметры**

-   `domNode`: [DOM-элемент](https://developer.mozilla.org/docs/Web/API/Element), который был отображен как корневой элемент на сервере.
-   `reactNode`: "Узел React", используемый для рендеринга существующего HTML. Обычно это кусок JSX типа `<App />`, который был отрисован с помощью метода `ReactDOM Server`, такого как `renderToPipeableStream(<App />)`.
-   **опционально** `options`: Объект с опциями для этого корня React.
    -   **optional** `onRecoverableError`: Обратный вызов, вызываемый, когда React автоматически восстанавливается после ошибок.
    -   **optional** `identifierPrefix`: Строковый префикс, который React использует для идентификаторов, генерируемых [`useId`.](../../react/useId.md) Полезно для предотвращения конфликтов при использовании нескольких корней на одной странице. Должен быть тем же префиксом, который используется на сервере.

**Возвращает**

`hydrateRoot` возвращает объект с двумя методами: `render` и `unmount`.

**Ограничения**

-   `hydrateRoot()` ожидает, что отрендеренное содержимое будет идентично отрендеренному содержимому сервера. Несовпадения следует рассматривать как ошибки и исправлять их.
-   В режиме разработки React предупреждает о несоответствиях во время гидратации. Нет никаких гарантий, что различия атрибутов будут исправлены в случае несовпадений. Это важно по соображениям производительности, поскольку в большинстве приложений несоответствия встречаются редко, и поэтому валидация всей разметки была бы непомерно дорогой.
-   Скорее всего, в вашем приложении будет только один вызов `hydrateRoot`. Если вы используете фреймворк, он может сделать этот вызов за вас.
-   Если ваше приложение клиентское, без уже отрисованного HTML, использование `hydrateRoot()` не поддерживается. Вместо этого используйте [`createRoot()`](./createRoot.md).

### `root.render(reactNode)` {#root-render}

Вызов `root.render` для обновления компонента React внутри гидратированного корня React для элемента DOM браузера.

```js
root.render(<App />);
```

React обновит `<App />` в гидратированном `root`.

**Параметры**

-   `reactNode`: "React-узел", который вы хотите обновить. Обычно это кусок JSX типа `<App />`, но вы также можете передать элемент React, созданный с помощью [`createElement()`](../../react/createElement.md), строку, число, `null` или `undefined`.

**Возвраты**

`root.render` возвращает `undefined`.

**Предупреждения**

-   Если вы вызовете `root.render` до того, как корень закончит гидрирование, React очистит существующий HTML-контент, отрендеренный сервером, и переключит весь корень на клиентский рендеринг.

### `root.unmount()` {#root-unmount}

Вызовите `root.unmount`, чтобы уничтожить дерево рендеринга внутри корня React.

```js
root.unmount();
```

Приложение, полностью построенное на React, обычно не содержит вызовов `root.unmount`.

Это в основном полезно, если DOM-узел вашего React root (или любой из его предков) может быть удален из DOM каким-либо другим кодом. Например, представьте себе панель вкладок jQuery, которая удаляет неактивные вкладки из DOM. Если вкладка будет удалена, все внутри нее (включая React roots внутри) также будет удалено из DOM. Вам нужно сказать React "перестать" управлять содержимым удаленного корня, вызвав `root.unmount`. В противном случае компоненты внутри удаленного корня не очистятся и не освободят ресурсы, такие как подписки.

Вызов `root.unmount` размонтирует все компоненты в корне и "отсоединит" React от корневого DOM-узла, включая удаление любых обработчиков событий или состояния в дереве.

**Параметры**

`root.unmount` не принимает никаких параметров.

**Возвраты**

`render` возвращает `null`.

**Ограничения**

-   Вызов `root.unmount` размонтирует все компоненты в дереве и "отсоединит" React от корневого DOM-узла.
-   После вызова `root.unmount` вы не сможете снова вызвать `root.render` на корне. Попытка вызвать `root.render` на немонтированном корне приведет к ошибке "Cannot update an unmounted root".

## Использование {#usage}

### Гидрирование серверного HTML {#hydrating-server-rendered-html}

Если HTML вашего приложения был сгенерирован [`react-dom/server`](./createRoot.md), вам нужно _гидрировать_ его на клиенте.

```js
import { hydrateRoot } from 'react-dom/client';

hydrateRoot(document.getElementById('root'), <App />);
```

Это приведет к гидратации HTML сервера внутри узла browser DOM с компонентом React для вашего приложения. Обычно вы делаете это один раз при запуске. Если вы используете фреймворк, он может сделать это за кадром для вас.

Чтобы гидратировать ваше приложение, React "прикрепляет" логику ваших компонентов к первоначально сгенерированному HTML с сервера. Гидратация превращает первоначальный снимок HTML с сервера в полностью интерактивное приложение, которое запускается в браузере.

=== "index.html"

    ```html
    <!--
    HTML content inside <div id="root">...</div>
    was generated from App by react-dom/server.
    -->
    <div id="root">
    	<h1>Hello, world!</h1>
    	<button>
    		You clicked me
    		<!-- -->0<!-- -->
    		times
    	</button>
    </div>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { hydrateRoot } from 'react-dom/client';
    import App from './App.js';

    hydrateRoot(document.getElementById('root'), <App />);
    ```

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function App() {
    	return (
    		<>
    			<h1>Hello, world!</h1>
    			<Counter />
    		</>
    	);
    }

    function Counter() {
    	const [count, setCount] = useState(0);
    	return (
    		<button onClick={() => setCount(count + 1)}>
    			You clicked me {count} times
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/zwj2xg?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вам не придется вызывать `hydrateRoot` снова или вызывать его в других местах. С этого момента React будет управлять DOM вашего приложения. Для обновления пользовательского интерфейса ваши компоненты будут [использовать состояние](../../react/useState.md).

!!!warning ""

    Дерево React, которое вы передаете в `hydrateRoot`, должно выдавать **тот же результат**, что и на сервере.

    Это важно для пользовательского опыта. Пользователь потратит некоторое время на просмотр HTML, сгенерированного сервером, прежде чем загрузится ваш код JavaScript. Серверный рендеринг создает иллюзию того, что приложение загружается быстрее, показывая HTML-снимок его вывода. Внезапный показ другого содержимого разрушает эту иллюзию. Вот почему вывод серверного рендеринга должен совпадать с первоначальным выводом рендеринга на клиенте.

    Наиболее распространенные причины, приводящие к ошибкам гидратации, включают:

    -   Лишние пробельные символы (например, новые строки) вокруг сгенерированного React HTML внутри корневого узла.
    -   Использование проверок типа `typeof window !== 'undefined'` в логике рендеринга.
    -   Использование в логике рендеринга API, предназначенных только для браузера, таких как [`window.matchMedia`](https://developer.mozilla.org/docs/Web/API/Window/matchMedia).
    -   Рендеринг разных данных на сервере и клиенте.

    React восстанавливается после некоторых ошибок гидратации, но **вы должны исправлять их, как и другие ошибки.** В лучшем случае они приведут к замедлению работы; в худшем случае обработчики событий могут быть присоединены к неправильным элементам.

### Гидрирование всего документа {#hydrating-an-entire-document}

Приложения, полностью построенные на React, могут рендерить весь документ как JSX, включая тег [`<html>`](https://hcdev.ru/html/html/):

```js hl_lines="3 19"
function App() {
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

Чтобы гидратировать весь документ, передайте глобальный [`document`](https://developer.mozilla.org/docs/Web/API/Window/document) в качестве первого аргумента в `hydrateRoot`:

```js hl_lines="4"
import { hydrateRoot } from 'react-dom/client';
import App from './App.js';

hydrateRoot(document, <App />);
```

### Подавление неизбежных ошибок несоответствия гидратации {#suppressing-unavoidable-hydration-mismatch-errors}

Если атрибут или текстовое содержимое одного элемента неизбежно отличается на сервере и клиенте (например, метка времени), вы можете заглушить предупреждение о несоответствии гидратации.

Чтобы заглушить предупреждения о несоответствии гидратации для элемента, добавьте `suppressHydrationWarning={true}`:

=== "index.html"

    ```html
    <!--
    HTML content inside <div id="root">...</div>
    was generated from App by react-dom/server.
    -->
    <div id="root">
    	<h1>
    		Current Date:
    		<!-- -->01/01/2020
    	</h1>
    </div>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { hydrateRoot } from 'react-dom/client';
    import App from './App.js';

    hydrateRoot(document.getElementById('root'), <App />);
    ```

=== "App.js"

    ```js
    export default function App() {
    	return (
    		<h1 suppressHydrationWarning={true}>
    			Current Date: {new Date().toLocaleDateString()}
    		</h1>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/kctqrs?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Он действует только на глубине одного уровня и предназначен для эвакуации. Не злоупотребляйте им. Если это не текстовое содержимое, React не будет пытаться исправить его, поэтому оно может оставаться непоследовательным до будущих обновлений.

### Обработка различного содержимого клиента и сервера {#handling-different-client-and-server-content}

Если вам намеренно нужно отобразить что-то разное на сервере и клиенте, вы можете сделать двухпроходной рендеринг. Компоненты, которые отображают что-то разное на клиенте, могут читать [переменную состояния](../../react/useState.md), например `isClient`, которую вы можете установить в `true` в [Effect](../../react/useEffect.md):

=== "index.html"

    ```html
    <!--
    HTML content inside <div id="root">...</div>
    was generated from App by react-dom/server.
    -->
    <div id="root"><h1>Is Server</h1></div>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { hydrateRoot } from 'react-dom/client';
    import App from './App.js';

    hydrateRoot(document.getElementById('root'), <App />);
    ```

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function App() {
    	const [isClient, setIsClient] = useState(false);

    	useEffect(() => {
    		setIsClient(true);
    	}, []);

    	return <h1>{isClient ? 'Is Client' : 'Is Server'}</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/zwg748?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Таким образом, начальный проход рендеринга будет рендерить тот же контент, что и сервер, избегая несоответствий, но дополнительный проход будет происходить синхронно сразу после гидратации.

!!!warning ""

    Такой подход делает процесс гидратации медленнее, поскольку ваши компоненты должны отображаться дважды. Помните о пользовательском опыте на медленных соединениях. Код JavaScript может загружаться значительно позже, чем первоначальный HTML-рендеринг, поэтому рендеринг другого пользовательского интерфейса сразу после гидратации также может показаться пользователю резким.

### Обновление гидратированного корневого компонента {#updating-a-hydrated-root-component}

После завершения гидратации корня вы можете вызвать `root.render`, чтобы обновить корневой React-компонент. **В отличие от [`createRoot`](./createRoot.md), вам обычно не нужно этого делать, потому что исходное содержимое уже было отрендерено как HTML.**

Если вы вызовете `root.render` в какой-то момент после гидратации, и структура дерева компонентов совпадет с тем, что было отрисовано ранее, React [сохранит состояние](../../../learn/preserving-and-resetting-state.md) Обратите внимание, что вы можете вводить входные данные, что означает, что обновления от повторяющихся вызовов `render` каждую секунду в этом примере не являются разрушительными:

=== "index.html"

    ```html
    <!--
    All HTML content inside <div id="root">...</div> was
    generated by rendering <App /> with react-dom/server.
    -->
    <div id="root">
    	<h1>
    		Hello, world!
    		<!-- -->0
    	</h1>
    	<input placeholder="Type something here" />
    </div>
    ```

=== "index.js"

    ```js
    import { hydrateRoot } from 'react-dom/client';
    import './styles.css';
    import App from './App.js';

    const root = hydrateRoot(
    	document.getElementById('root'),
    	<App counter={0} />
    );

    let i = 0;
    setInterval(() => {
    	root.render(<App counter={i} />);
    	i++;
    }, 1000);
    ```

=== "App.js"

    ```js
    export default function App({ counter }) {
    	return (
    		<>
    			<h1>Hello, world! {counter}</h1>
    			<input placeholder="Type something here" />
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/l5vwx2?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вызывать `root.render` на гидратированном корне - редкость. Обычно вместо этого вы вызываете [обновление состояния](../../react/useState.md) внутри одного из компонентов.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/client/hydrateRoot></small>
