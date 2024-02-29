---
status: experimental
---

# &lt;meta&gt;

!!!example "Canary"

    Расширения React для `<meta>` в настоящее время доступны только в канале React canary и экспериментальном канале. В стабильных релизах React `<meta>` работает только как [встроенный HTML-компонент браузера](https://react.dev/reference/react-dom/components#all-html-components). Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>Встроенный компонент браузера [`<meta>`](https://hcdev.ru/html/meta/) позволяет добавлять метаданные к документу.</big>

```js
<meta
    name="keywords"
    content="React, JavaScript, semantic markup, html"
/>
```

## Описание {#reference}

### `<meta>` {#meta}

Чтобы добавить метаданные документа, отобразите [встроенный в браузер компонент `<meta>`](https://hcdev.ru/html/meta/). Вы можете рендерить `<meta>` из любого компонента, и React всегда будет помещать соответствующий элемент DOM в голову документа.

```js
<meta
    name="keywords"
    content="React, JavaScript, semantic markup, html"
/>
```

**Параметры**

`<meta>` поддерживает все [общие реквизиты элементов](./common.md#props).

Он должен иметь _точно один_ из следующих реквизитов: `name`, `httpEquiv`, `charset`, `itemProp`. Компонент `<meta>` выполняет разные действия в зависимости от того, какой из этих реквизитов указан.

-   `name`: строка. Указывает [вид метаданных](https://hcdev.ru/html/meta/#name), которые будут прикреплены к документу.
-   `charset`: строка. Указывает набор символов, используемый документом. Единственное допустимое значение - `"utf-8"`.
-   `httpEquiv`: строка. Указывает директиву для обработки документа.
-   `itemProp`: строка. Указывает метаданные о конкретном элементе в документе, а не о документе в целом.
-   `content`: строка. Определяет метаданные, которые должны быть присоединены при использовании реквизитов `name` или `itemProp`, или поведение директивы при использовании реквизита `httpEquiv`.

#### Специальное поведение рендеринга {#special-rendering-behavior}

React всегда будет помещать элемент DOM, соответствующий компоненту `<meta>`, в `<head>` документа, независимо от того, в каком месте дерева React он отрисован. `<head>` - единственное допустимое место для `<meta>` в DOM, однако это удобно и позволяет сохранить композитность, если компонент, представляющий определенную страницу, может сам рендерить компоненты `<meta>`.

Есть одно исключение: если у `<meta>` есть реквизит [`itemProp`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/itemprop), то никакого особого поведения не будет, потому что в этом случае он представляет не метаданные о документе, а метаданные о конкретной части страницы.

## Использование {#usage}

### Аннотирование документа метаданными {#annotating-the-document-with-metadata}

Вы можете аннотировать документ метаданными, такими как ключевые слова, краткое содержание или имя автора. React поместит эти метаданные в `<head>` документа, независимо от того, в каком месте дерева React он будет отображаться.

```html
<meta name="author" content="John Smith" />
<meta
    name="keywords"
    content="React, JavaScript, semantic markup, html"
/>
<meta
    name="description"
    content="API reference for the <meta> component in React DOM"
/>
```

Вы можете отобразить компонент `<meta>` из любого компонента. React поместит DOM-узел `<meta>` в документ `<head>`.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';

    export default function SiteMapPage() {
    	return (
    		<ShowRenderedHTML>
    			<meta name="keywords" content="React" />
    			<meta
    				name="description"
    				content="A site map for the React website"
    			/>
    			<h1>Site Map</h1>
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

    <iframe src="https://codesandbox.io/embed/6gdxf2?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="wandering-https-6gdxf2" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Аннотирование конкретных элементов в документе с помощью метаданных {#annotating-specific-items-within-the-document-with-metadata}

Вы можете использовать компонент `<meta>` с параметром `itemProp` для аннотирования конкретных элементов в документе с метаданными. В этом случае React не будет размещать эти аннотации внутри документа `<head>`, а разместит их как любой другой компонент React.

```js
<section itemScope>
    <h3>Annotating specific items</h3>
    <meta
        itemProp="description"
        content="API reference for using <meta> with itemProp"
    />
    <p>...</p>
</section>
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/meta](https://react.dev/reference/react-dom/components/meta)</small>
