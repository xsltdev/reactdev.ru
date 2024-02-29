---
status: experimental
description: Встроенный компонент браузера script позволяет добавить скрипт в документ
---

# &lt;script&gt;

!!!example "Canary"

    Расширения для `<script>` в React в настоящее время доступны только в канале React canary и экспериментальном канале. В стабильных релизах React `<script>` работает только как [встроенный в браузер HTML-компонент](https://react.dev/reference/react-dom/components#all-html-components). Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>Встроенный компонент браузера [`<script>`](https://hcdev.ru/html/script) позволяет добавить скрипт в документ.</big>

```js
<script> alert("hi!") </script>
```

## Описание {#reference}

### `<script>` {#script}

Чтобы добавить в документ встроенные или внешние скрипты, отобразите [встроенный в браузер компонент `<script>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script). Вы можете рендерить `<script>` из любого компонента, и React [в определенных случаях](#special-rendering-behavior) поместит соответствующий элемент DOM в голову документа и удалит дублирование идентичных скриптов.

```js
<script> alert("hi!") </script>
<script src="script.js" />
```

**Параметры**

`<script>` поддерживает все [общие свойства элементов](./common.md#props).

У него должны быть _либо_ `children`, либо проп `src`.

-   `children`: строка. Исходный код встроенного скрипта.
-   `src`: строка. URL-адрес внешнего скрипта.

Другие поддерживаемые пропсы:

-   `async`: булево. Позволяет браузеру отложить выполнение скрипта до тех пор, пока не будет обработана остальная часть документа - предпочтительное поведение для повышения производительности.
-   `crossOrigin`: строка. Политика [CORS](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin), которую следует использовать. Возможные значения: `anonymous` и `use-credentials`.
-   `fetchPriority`: строка. Позволяет браузеру ранжировать скрипты по приоритету при одновременной выборке нескольких скриптов. Может быть `"high"`, `"low"` или `"auto"` (по умолчанию).
-   `integrity`: строка. Криптографический хэш скрипта для [проверки его подлинности](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
-   `noModule`: булево. Отключает скрипт в браузерах, поддерживающих ES-модули, и позволяет использовать запасной скрипт в браузерах, которые этого не делают.
-   `nonce`: строка. Криптографический [nonce для разрешения ресурса](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) при использовании строгой политики безопасности содержимого.
-   `referrer`: строка. Указывает [какой заголовок Referer отправить](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#referrerpolicy) при выборке скрипта и любых ресурсов, которые скрипт в свою очередь берет.
-   `type`: строка. Указывает, является ли скрипт [классическим скриптом, ES-модулем или import map](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type).

Реквизиты, отключающие [особое отношение React к скриптам](#special-rendering-behavior):

-   `onError`: функция. Вызывается, когда скрипт не загружается.
-   `onLoad`: функция. Вызывается, когда скрипт завершает загрузку.

Пропсы, которые **не рекомендуется** использовать с React:

-   `blocking`: строка. Если установлено значение `"render"`, это указывает браузеру не рендерить страницу до тех пор, пока не будет загружен лист скриптов. React обеспечивает более тонкий контроль с помощью Suspense.
-   `defer`: строка. Запрещает браузеру выполнять скрипт до окончания загрузки документа. Не совместим с потоковыми компонентами, рендеримыми сервером. Вместо этого используйте параметр `async`.

#### Специальное поведение рендеринга {#special-rendering-behavior}

React может перемещать компоненты `<script>` в `<head>` документа, де-дублировать идентичные скрипты и [приостанавливать](http://localhost:3000/reference/react/Suspense) загрузку скрипта.

Для того, чтобы принять это поведение, укажите свойства `src` и `async={true}`. React будет дедублировать скрипты, если у них одинаковый `src`. Свойство `async` должно быть истинным, чтобы скрипты можно было безопасно перемещать.

Если вы передадите любой из параметров `onLoad` или `onError`, то никакого особого поведения не будет, поскольку эти параметры указывают на то, что вы управляете загрузкой скрипта вручную внутри вашего компонента.

Это особое обращение сопровождается двумя оговорками:

-   React будет игнорировать изменения пропсов после рендеринга скрипта. (React выдаст предупреждение в процессе разработки, если это произойдет).
-   React может оставить скрипт в DOM даже после того, как компонент, который его отрисовал, будет размонтирован. (Это не имеет никакого эффекта, так как скрипты выполняются только один раз, когда их вставляют в DOM).

## Использование {#usage}

### Рендеринг внешнего скрипта {#rendering-an-external-script}

Если компонент зависит от определенных скриптов для корректного отображения, вы можете отобразить `<script>` внутри компонента.

Если вы укажете свойства `src` и `async`, ваш компонент приостановится на время загрузки скрипта. React будет де-дублировать скрипты с одинаковым `src`, вставляя в DOM только один из них, даже если его рендерят несколько компонентов.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    function Map({ lat, long }) {
    	return (
    		<>
    			<script async src="map-api.js" />
    			<div id="map" data-lat={lat} data-long={long} />
    		</>
    	);
    }

    export default function Page() {
    	return (
    		<ShowRenderedHTML>
    			<Map />
    		</ShowRenderedHTML>
    	);
    }
    ```

=== "ShowRenderedHTML.js"

    ```js
    import { renderToStaticMarkup } from 'react-dom/server';
    import formatHTML from './formatHTML.js';

    export default function ShowRenderedHTML({ children }) {
    	const markup = renderToStaticMarkup(
    		<html>
    			<head />
    			<body>{children}</body>
    		</html>
    	);
    	return (
    		<>
    			<h1>Rendered HTML:</h1>
    			<pre>{formatHTML(markup)}</pre>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xc2xj8?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="interesting-mendel-xc2xj8" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note ""

    Когда вы хотите использовать скрипт, может быть полезно вызвать функцию [preinit](../preinit.md). Вызов этой функции может позволить браузеру начать выборку скрипта раньше, чем если бы вы просто отобразили компонент `<script>`, например, отправив ответ [HTTP Early Hints response](https://developer.mozilla.org/docs/Web/HTTP/Status/103).

### Рендеринг встроенного скрипта {#rendering-an-inline-script}

Чтобы включить встроенный скрипт, отобразите компонент `<script>` с исходным кодом скрипта в качестве его дочерних элементов. Встроенные скрипты не дублируются и не перемещаются в документ `<head>`, а поскольку они не загружают никаких внешних ресурсов, они не приведут к приостановке работы вашего компонента.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    function Tracking() {
    	return <script>ga('send', 'pageview');</script>;
    }

    export default function Page() {
    	return (
    		<ShowRenderedHTML>
    			<h1>My Website</h1>
    			<Tracking />
    			<p>Welcome</p>
    		</ShowRenderedHTML>
    	);
    }
    ```

=== "ShowRenderedHTML.js"

    ```js
    import { renderToStaticMarkup } from 'react-dom/server';
    import formatHTML from './formatHTML.js';

    export default function ShowRenderedHTML({ children }) {
    	const markup = renderToStaticMarkup(
    		<html>
    			<head />
    			<body>{children}</body>
    		</html>
    	);
    	return (
    		<>
    			<h1>Rendered HTML:</h1>
    			<pre>{formatHTML(markup)}</pre>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/q6mk6v?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="eloquent-microservice-q6mk6v" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/script](https://react.dev/reference/react-dom/components/script)</small>
