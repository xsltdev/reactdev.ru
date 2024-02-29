---
status: experimental
---

# &lt;style&gt;

!!!example "Canary"

    Расширения React для `<style>` в настоящее время доступны только в канале React canary и экспериментальном канале. В стабильных релизах React `<style>` работает только как [встроенный в браузер HTML-компонент](https://react.dev/reference/react-dom/components#all-html-components). Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>Встроенный компонент браузера [`<style>`](https://developer.mozilla.org/docs/Web/HTML/Element/style) позволяет добавлять в документ встроенные таблицы стилей CSS.</big>

```css
<style> p { color: red; } </style>
```

## Описание {#reference}

### `<style>` {#style}

Чтобы добавить инлайн-стили в документ, отрендерите [встроенный в браузер компонент `<style>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style). Вы можете рендерить `<style>` из любого компонента, и React [в определенных случаях](#special-rendering-behavior) поместит соответствующий элемент DOM в голову документа и удалит дублирование идентичных стилей.

```css
<style> p { color: red; } </style>
```

**Параметры**

`<style>` поддерживает все [общие пропсы элементов](./common.md#props).

-   `children`: строка, обязательна. Содержимое таблицы стилей.
-   `precedence`: строка. Указывает React, где ранжировать DOM-узел `<style>` относительно других в документе `<head>`, который определяет, какая таблица стилей может перекрывать другую. Его значение может быть (в порядке старшинства) `" reset"`, `"low"`, `"medium"`, `"high"`. Таблицы стилей с одинаковым старшинством идут вместе независимо от того, являются ли они тегами `<link>` или встроенными тегами `<style>` или загружаются с помощью функций [`preload`](../preload.md) или [`preinit`](../preinit.md).
-   `href`: строка. Позволяет React [де-дублировать стили](#special-rendering-behavior), которые имеют одинаковый `href`.
-   `media`: строка. Ограничивает таблицу определенным [media query](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries).
-   `nonce`: строка. Криптографический [nonce для разрешения ресурса](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) при использовании строгой политики безопасности содержимого.
-   `title`: строка. Указывает имя [альтернативной таблицы стилей](https://developer.mozilla.org/en-US/docs/Web/CSS/Alternative_style_sheets).

Пропсы, которые **не рекомендуется** использовать с React:

-   `blocking`: строка. Если установлено значение `"render"`, указывает браузеру не рендерить страницу до тех пор, пока не будет загружена таблица стилей. React обеспечивает более тонкий контроль с помощью Suspense.

#### Специальное поведение рендеринга {#special-rendering-behavior}

React может перемещать компоненты `<style>` в `<head>` документа, де-дублировать идентичные таблицы стилей и [приостанавливать](http://localhost:3000/reference/react/Suspense) загрузку таблицы стилей.

Чтобы принять это поведение, укажите параметры `href` и `precedence`. React будет де-дублировать стили, если у них одинаковый `href`. Проп `precedence` указывает React, где ранжировать DOM-узел `<style>` относительно других в документе `<head>`, что определяет, какая таблица стилей может переопределить другую.

Этот особый режим имеет две оговорки:

-   React будет игнорировать изменения пропсов после отрисовки стиля. (Если это произойдет, React выдаст предупреждение в процессе разработки).
-   React может оставить стиль в DOM даже после того, как компонент, который его отрисовал, будет размонтирован.

## Использование {#usage}

### Рендеринг встроенной таблицы стилей CSS {#rendering-an-inline-css-stylesheet}

Если компонент зависит от определенных стилей CSS для корректного отображения, вы можете отобразить встроенную таблицу стилей внутри компонента.

Если вы укажете параметры `href` и `precedence`, ваш компонент приостановится на время загрузки таблицы стилей. (Даже при использовании встроенных таблиц стилей может потребоваться время загрузки из-за шрифтов и изображений, на которые ссылается таблица стилей). Параметр `href` должен уникально идентифицировать таблицу стилей, потому что React будет удалять дубликаты таблиц стилей с одинаковым `href`.

=== "App.js"

    ```js
    import ShowRenderedHTML from './ShowRenderedHTML.js';
    import { useId } from 'react';

    function PieChart({ data, colors }) {
    	const id = useId();
    	const stylesheet = colors
    		.map(
    			(color, index) =>
    				`#${id} .color-${index}: \{ color: "${color}"; \}`
    		)
    		.join();
    	return (
    		<>
    			<style
    				href={'PieChart-' + JSON.stringify(colors)}
    				precedence="medium"
    			>
    				{stylesheet}
    			</style>
    			<svg id={id}>…</svg>
    		</>
    	);
    }

    export default function App() {
    	return (
    		<ShowRenderedHTML>
    			<PieChart
    				data="..."
    				colors={['red', 'green', 'blue']}
    			/>
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

    <iframe src="https://codesandbox.io/embed/y2773z?view=Editor+%2B+Preview&module=%2Fsrc%2FShowRenderedHTML.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="frosty-wright-y2773z" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/style](https://react.dev/reference/react-dom/components/style)</small>
