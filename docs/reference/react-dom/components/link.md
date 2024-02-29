---
status: experimental
description: Встроенный компонент браузера link позволяет использовать внешние ресурсы, такие как таблицы стилей, или аннотировать документ метаданными ссылок
---

# &lt;link&gt;

!!!example "Canary"

    Расширения React для `<link>` в настоящее время доступны только в канале React canary и экспериментальном канале. В стабильных релизах React `<link>` работает только как [встроенный в браузер HTML-компонент](https://react.dev/reference/react-dom/components#all-html-components). Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>Встроенный компонент браузера [`<link>`](https://hcdev.ru/html/link/) позволяет использовать внешние ресурсы, такие как таблицы стилей, или аннотировать документ метаданными ссылок.</big>

```js
<link rel="icon" href="favicon.ico" />
```

## Описание {#reference}

### `<link>` {#link}

Чтобы сделать ссылки на внешние ресурсы, такие как таблицы стилей, шрифты и иконки, или аннотировать документ метаданными ссылок, используйте [встроенный в браузер компонент `<link>`](https://hcdev.ru/html/link/). Вы можете рендерить `<link>` из любого компонента, и React [в большинстве случаев](#special-rendering-behavior) поместит соответствующий элемент DOM в голову документа.

```js
<link rel="icon" href="favicon.ico" />
```

**Параметры**

`<link>` поддерживает все [общие пропсы элементов](../components/common.md#props)

-   `rel`: строка, обязательна. Указывает [отношение к ресурсу](https://developer.mozilla.org/docs/Web/HTML/Attributes/rel). React [обрабатывает ссылки с `rel="stylesheet"` иначе](#special-rendering-behavior), чем другие ссылки.

Эти реквизиты применяются, когда `rel="stylesheet"`:

-   `precedence`: строка. Указывает React, где ранжировать DOM-узел `<link>` относительно других в документе `<head>`, что определяет, какая таблица стилей может перекрыть другую. Его значение может быть (в порядке старшинства) `" reset"`, `"low"`, `"medium"`, `"high"`. Таблицы стилей с одинаковым старшинством идут вместе независимо от того, являются ли они тегами `<link>` или встроенными тегами `<style>` или загружаются с помощью функций [`preload`](../preload.md) или [`preinit`](../preinit.md).
-   `media`: строка. Ограничивает электронную таблицу определенным [media query](https://developer.mozilla.org/docs/Web/CSS/CSS_media_queries/Using_media_queries).
-   `title`: строка. Задает имя [альтернативной таблицы стилей](https://developer.mozilla.org/docs/Web/CSS/Alternative_style_sheets).

Эти реквизиты применяются, когда `rel="stylesheet"`, но отключают [особое отношение React к таблицам стилей](#special-rendering-behavior):

-   `disabled`: булево. Отключает таблицу.
-   `onError`: функция. Вызывается, когда таблица стилей не загружается.
-   `onLoad`: функция. Вызывается, когда таблица стилей завершает загрузку.

Эти реквизиты применяются, когда `rel="preload"` или `rel="modulepreload"`:

-   `as`: строка. Тип ресурса. Возможные значения: `audio`, `document`, `embed`, `fetch`, `font`, `image`, `object`, `script`, `style`, `track`, `video`, `worker`.
-   `imageSrcSet`: строка. Применяется только в случае `as="image"`. Указывает [исходный набор изображения](https://developer.mozilla.org/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).
-   `imageSizes`: строка. Применяется только в случае `as="image"`. Указывает [размеры изображения](https://developer.mozilla.org/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

Этот реквизит применяется при `rel="icon"` или `rel="apple-touch-icon"`:

-   `sizes`: строка. [размеры иконки](https://developer.mozilla.org/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

Эти параметры применяются во всех случаях:

-   `href`: строка. URL-адрес связанного ресурса.
-   `crossOrigin`: строка. Используемая политика [CORS](https://developer.mozilla.org/docs/Web/HTML/Attributes/crossorigin). Возможные значения: `anonymous` и `use-credentials`. Требуется, если для параметра `as` установлено значение `"fetch"`.
-   `referrerPolicy`: строка. Заголовок [Referrer header](https://hcdev.ru/html/link/#referrerpolicy), который следует отправлять при выборке. Возможные значения: `no-referrer-when-downgrade` (по умолчанию), `no-referrer`, `origin`, `origin-when-cross-origin`, и `unsafe-url`.
-   `fetchPriority`: строка. Указывает относительный приоритет для получения ресурса. Возможные значения: `auto` (по умолчанию), `high` и `low`.
-   `hrefLang`: строка. Язык связанного ресурса.
-   `integrity`: строка. Криптографический хэш ресурса для [проверки его подлинности](https://developer.mozilla.org/docs/Web/Security/Subresource_Integrity).
-   `type`: строка. MIME-тип связанного ресурса.

Реквизиты, которые **не рекомендуется** использовать с React:

-   `blocking`: строка. Если установлено значение `"render"`, это указывает браузеру не рендерить страницу до тех пор, пока не будет загружена таблица стилей. React обеспечивает более тонкий контроль с помощью Suspense.

#### Особое поведение рендеринга {#special-rendering-behavior}

React всегда будет помещать элемент DOM, соответствующий компоненту `<link>`, в `<head>` документа, независимо от того, в каком месте дерева React он отрисовывается. `<head>` - единственное допустимое место для `<link>` в DOM, но это удобно и позволяет сохранить композитность, если компонент, представляющий определенную страницу, может сам рендерить компоненты `<link>`.

Из этого есть несколько исключений:

-   Если у `<link>` есть свойство `rel="stylesheet"`, то для получения такого особого поведения у него также должно быть свойство `precedence`. Это происходит потому, что порядок следования таблиц стилей в документе имеет значение, поэтому React должен знать, как упорядочить эту таблицу стилей относительно других, которые вы указываете с помощью свойства `precedence`. Если параметр `precedence` опущен, то никакого особого поведения не будет.
-   Если у `<link>` есть реквизит [`itemProp`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/itemprop), то никакого особого поведения не будет, потому что в этом случае она не относится к документу, а представляет собой метаданные о конкретной части страницы.
-   Если у `<link>` есть свойство `onLoad` или `onError`, то в этом случае вы управляете загрузкой связанного ресурса вручную внутри вашего компонента React.

#### Особое поведение для таблиц стилей {#special-behavior-for-stylesheets}

Кроме того, если `<link>` является ссылкой на таблицу стилей (а именно, имеет `rel="stylesheet"` в своем реквизите), React обрабатывает ее особым образом следующим образом:

-   Компонент, отображающий `<link>`, будет [приостановлен](../../react/Suspense.md) на время загрузки таблицы стилей.
-   Если несколько компонентов отображают ссылки на одну и ту же таблицу стилей, React будет дедублировать их и помещать в DOM только одну ссылку. Две ссылки считаются одинаковыми, если у них одинаковый параметр `href`.

Есть два исключения из этого особого поведения:

-   Если у ссылки нет свойства `precedence`, то особого поведения не будет, потому что порядок следования таблиц стилей в документе имеет значение, поэтому React должен знать, как упорядочить эту таблицу стилей относительно других, что вы и указываете с помощью свойства `precedence`.
-   Если вы предоставите любой из реквизитов `onLoad`, `onError` или `disabled`, то никакого особого поведения не будет, потому что эти реквизиты указывают на то, что вы управляете загрузкой таблицы стилей вручную внутри вашего компонента.

Это особое отношение сопровождается двумя оговорками:

-   React будет игнорировать изменения реквизитов после того, как ссылка будет отрисована. (Если это произойдет, React выдаст предупреждение в процессе разработки).
-   React может оставить ссылку в DOM даже после того, как компонент, который ее отобразил, будет размонтирован.

## Использование {#usage}

### Ссылки на связанные ресурсы {#linking-to-related-resources}

Вы можете аннотировать документ ссылками на связанные ресурсы, такие как иконка, канонический URL или pingback. React поместит эти метаданные в `<head>` документа, независимо от того, в каком месте дерева React он будет отображаться.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    export default function BlogPage() {
    	return (
    		<ShowRenderedHTML>
    			<link rel="icon" href="favicon.ico" />
    			<link
    				rel="pingback"
    				href="http://www.example.com/xmlrpc.php"
    			/>
    			<h1>My Blog</h1>
    			<p>...</p>
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

    <iframe src="https://codesandbox.io/embed/htpzgz?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="gracious-jerry-htpzgz" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Ссылка на таблицу стилей {#linking-to-a-stylesheet}

Если компонент зависит от определенной таблицы стилей для корректного отображения, вы можете отобразить ссылку на эту таблицу стилей внутри компонента. Ваш компонент будет [приостановлен](../../react/Suspense.md) на время загрузки таблицы стилей. Вы должны указать параметр `precedence`, который указывает React, куда поместить эту таблицу стилей относительно других - таблицы стилей с более высоким приоритетом могут перекрывать таблицы с более низким приоритетом.

!!!note ""

    Когда вы хотите использовать таблицу стилей, может быть полезно вызвать функцию [preinit](../preinit.md). Вызов этой функции может позволить браузеру начать поиск таблицы стилей раньше, чем если бы вы просто отобразили компонент `<link>`, например, отправив ответ [HTTP Early Hints response](https://developer.mozilla.org/docs/Web/HTTP/Status/103).

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    export default function SiteMapPage() {
    	return (
    		<ShowRenderedHTML>
    			<link
    				rel="stylesheet"
    				href="sitemap.css"
    				precedence="medium"
    			/>
    			<p>...</p>
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

    <iframe src="https://codesandbox.io/embed/q3m693?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="suspicious-shirley-q3m693" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Управление приоритетом таблиц стилей {#controlling-stylesheet-precedence}

Таблицы стилей могут конфликтовать друг с другом, и когда это происходит, браузер выбирает ту, которая находится позже в документе. React позволяет управлять порядком следования таблиц стилей с помощью свойства `precedence`. В этом примере два компонента рендерят таблицы стилей, и та, что имеет больший приоритет, идет позже в документе, хотя компонент, который ее рендерит, идет раньше.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    export default function HomePage() {
    	return (
    		<ShowRenderedHTML>
    			<FirstComponent />
    			<SecondComponent />
    			...
    		</ShowRenderedHTML>
    	);
    }

    function FirstComponent() {
    	return (
    		<link
    			rel="stylesheet"
    			href="first.css"
    			precedence="high"
    		/>
    	);
    }

    function SecondComponent() {
    	return (
    		<link
    			rel="stylesheet"
    			href="second.css"
    			precedence="low"
    		/>
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

    <iframe src="https://codesandbox.io/embed/n27jzp?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="gifted-moore-n27jzp" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Дублированный рендеринг таблицы стилей {#deduplicated-stylesheet-rendering}

Если вы рендерите одну и ту же таблицу стилей из нескольких компонентов, React поместит только одну `<link>` в шапку документа.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    export default function HomePage() {
    	return (
    		<ShowRenderedHTML>
    			<Component />
    			<Component />
    			...
    		</ShowRenderedHTML>
    	);
    }

    function Component() {
    	return (
    		<link
    			rel="stylesheet"
    			href="styles.css"
    			precedence="medium"
    		/>
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

    <iframe src="https://codesandbox.io/embed/z6742w?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="affectionate-architecture-z6742w" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Аннотирование определенных элементов в документе ссылками {#annotating-specific-items-within-the-document-with-links}

Вы можете использовать компонент `<link>` с параметром `itemProp` для аннотирования определенных элементов в документе ссылками на связанные ресурсы. В этом случае React не будет размещать эти аннотации внутри документа `<head>`, а разместит их как любой другой компонент React.

```js
<section itemScope>
    <h3>Annotating specific items</h3>
    <link itemProp="author" href="http://example.com/" />
    <p>...</p>
</section>
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/link](https://react.dev/reference/react-dom/components/link)</small>
