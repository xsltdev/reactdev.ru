---
status: deprecated
description: hydrate позволяет отображать компоненты React внутри узла DOM браузера, HTML-содержимое которого было предварительно сгенерировано react-dom/server в React 17 и ниже
---

# hydrate

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

    В React 18 `hydrate` был заменен на [`hydrateRoot`](./client/hydrateRoot.md). Использование `hydrate` в React 18 предупредит, что ваше приложение будет вести себя так, как будто оно работает под управлением React 17.

<big>`hydrate` позволяет отображать компоненты React внутри узла DOM браузера, HTML-содержимое которого было предварительно сгенерировано [`react-dom/server`](./server/index.md) в React 17 и ниже.</big>

```js
hydrate(reactNode, domNode, callback?)
```

## Описание {#reference}

### `hydrate(reactNode, domNode, callback?)` {#hydrate}

Вызывает `hydrate` в React 17 и ниже для "прикрепления" React к существующему HTML, который уже был отрисован React в серверной среде.

```js
import { hydrate } from 'react-dom';

hydrate(reactNode, domNode);
```

React присоединится к HTML, существующему внутри `domNode`, и возьмет на себя управление DOM внутри него. Приложение, полностью построенное на React, обычно имеет только один вызов `hydrate` со своим корневым компонентом.

**Параметры**

-   `reactNode`: "Узел React", используемый для рендеринга существующего HTML. Обычно это кусок JSX типа `<App />`, который был отрисован с помощью метода `ReactDOM Server`, такого как `renderToString(<App />)` в React 17.
-   `domNode`: [DOM-элемент](https://developer.mozilla.org/docs/Web/API/Element), который был отображен как корневой элемент на сервере.
-   **опционально**: `callback`: Функция. Если она передана, React вызовет ее после того, как ваш компонент будет гидратирован.

**Возвращает**

`hydrate` возвращает `null`.

**Ограничения**

-   `hydrate` ожидает, что отрисованное содержимое будет идентично содержимому, отрисованному на сервере. React может исправлять различия в текстовом содержимом, но вы должны рассматривать несоответствия как ошибки и исправлять их.
-   В режиме разработки React предупреждает о несоответствиях во время гидратации. Нет никаких гарантий, что различия между атрибутами будут исправлены в случае несовпадений. Это важно по соображениям производительности, поскольку в большинстве приложений несоответствия встречаются редко, и поэтому валидация всей разметки была бы непомерно дорогой.
-   Скорее всего, в вашем приложении будет только один вызов `hydrate`. Если вы используете фреймворк, он может сделать этот вызов за вас.
-   Если ваше приложение клиентское, без уже отрендеренного HTML, использование `hydrate()` не поддерживается. Вместо этого используйте [`render()`](render.md) (для React 17 и ниже) или [`createRoot()`](./client/createRoot.md) (для React v18).

## Использование {#usage}

Вызовите `hydrate` для вложения React компонента в отрендеренный сервером browser DOM node.

```js
import { hydrate } from 'react-dom';

hydrate(<App />, document.getElementById('root'));
```

Использование `hydrate()` для рендеринга приложения только для клиента (приложение без серверного рендеринга HTML) не поддерживается. Вместо этого используйте [`render()`](render.md) (в React 17 и ниже) или [`createRoot()`](./client/createRoot.md) (в React 18+).

### Гидратация серверного рендеринга HTML {#hydrating-server-rendered-html}

В React "гидратация" - это то, как React "присоединяется" к существующему HTML, который уже был отрисован React в серверной среде. Во время гидратации React попытается прикрепить слушателей событий к существующей разметке и взять на себя рендеринг приложения на клиенте.

В приложениях, полностью построенных на React, **вы обычно будете гидратировать только один "корень", один раз при запуске для всего приложения**.

=== "index.html"

    ```html
    <!--
    HTML content inside <div id="root">...</div>
    was generated from App by react-dom/server.
    -->
    <div id="root"><h1>Hello, world!</h1></div>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { hydrate } from 'react-dom';
    import App from './App.js';

    hydrate(<App />, document.getElementById('root'));
    ```

=== "App.js"

    ```js
    export default function App() {
    	return <h1>Hello, world!</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/plzccv?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обычно вам не нужно вызывать `hydrate` снова или вызывать его в других местах. С этого момента React будет управлять DOM вашего приложения. Для обновления пользовательского интерфейса ваши компоненты будут [использовать состояние](../react/useState.md).

Для получения дополнительной информации о гидратации смотрите документацию для [`hydrateRoot`](./client/hydrateRoot.md).

### Подавление неизбежных ошибок несоответствия гидратации {#suppressing-unavoidable-hydration-mismatch-errors}

Если атрибут или текстовое содержимое одного элемента неизбежно отличается на сервере и клиенте (например, метка времени), вы можете заглушить предупреждение о несоответствии гидратации.

Чтобы заглушить предупреждения о несоответствии гидратации для элемента, добавьте `suppressHydrationWarning={true}`:

=== "index.html"

    ```html
    <!--
    HTML content inside <div id="root">...</div>
    was generated from App by react-dom/server.
    -->
    <div id="root"><h1>Current Date: 01/01/2020</h1></div>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { hydrate } from 'react-dom';
    import App from './App.js';

    hydrate(<App />, document.getElementById('root'));
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

    <iframe src="https://codesandbox.io/embed/plzdp2?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Он действует только на глубине одного уровня и предназначен для эвакуации. Не злоупотребляйте им. Если это не текстовое содержимое, React не будет пытаться исправить его, поэтому оно может оставаться непоследовательным до будущих обновлений.

### Обработка различного содержимого клиента и сервера

Если вам намеренно нужно отобразить что-то разное на сервере и клиенте, вы можете сделать двухпроходной рендеринг. Компоненты, которые отображают что-то разное на клиенте, могут считывать [переменную состояния](../react/useState.md), например `isClient`, которую вы можете установить в значение `true` в [эффекте](../react/useEffect.md):

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
    import { hydrate } from 'react-dom';
    import App from './App.js';

    hydrate(<App />, document.getElementById('root'));
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

    <iframe src="https://codesandbox.io/embed/ws3l5c?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Таким образом, начальный проход рендеринга будет рендерить тот же контент, что и сервер, избегая несоответствий, но дополнительный проход будет происходить синхронно сразу после гидратации.

!!!warning ""

    Такой подход делает процесс гидратации медленнее, поскольку ваши компоненты должны отображаться дважды. Помните о пользовательском опыте на медленных соединениях. Код JavaScript может загружаться значительно позже, чем первоначальный HTML-рендеринг, поэтому отображение другого пользовательского интерфейса сразу после гидратации может показаться пользователю резким.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/hydrate></small>
