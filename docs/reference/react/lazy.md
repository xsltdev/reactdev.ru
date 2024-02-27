---
description: lazy позволяет отложить загрузку кода компонента до его первого отображения
---

# lazy

<big>`lazy` позволяет отложить загрузку кода компонента до его первого отображения.</big>

```js
const SomeComponent = lazy(load);
```

## Описание {#reference}

### `lazy(load)` {#lazy}

Вызывайте `lazy` вне ваших компонентов, чтобы объявить лениво загруженный компонент React:

```js
import { lazy } from 'react';

const MarkdownPreview = lazy(() =>
    import('./MarkdownPreview.js')
);
```

**Параметры**

-   `load`: Функция, возвращающая [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или другой _thenable_ (Promise-подобный объект с методом `then`). React не будет вызывать `load` до первой попытки рендеринга возвращаемого компонента. После того как React впервые вызовет `load`, он будет ждать разрешения Promise, а затем отобразит разрешенное значение как компонент React. И возвращаемое Promise, и разрешенное значение Promise будут кэшироваться, поэтому React не будет вызывать `load` более одного раза. Если Promise отклоняется, React будет `throw` причину отклонения для обработки ближайшей границы ошибок.

**Возвращает**

`lazy` возвращает компонент React, который вы можете отобразить в своем дереве. Пока код ленивого компонента загружается, попытка его рендеринга будет _приостановлена._ Используйте [`<Suspense>`](Suspense.md) для отображения индикатора загрузки во время загрузки.

### `load` функция {#load}

**Параметры**

`load` не получает никаких параметров.

**Возвращает**

Вы должны вернуть [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или какой-либо другой _thenable_ (объект типа Promise с методом `then`). В конечном итоге он должен разрешиться в допустимый тип компонента React, такой как функция, [`memo`](memo.md) или компонент [`forwardRef`](forwardRef.md).

## Использование {#usage}

### Ленивая загрузка компонентов с помощью Suspense {#suspense-for-code-splitting}

Обычно вы импортируете компоненты с помощью объявления static [`import`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import):

```js
import MarkdownPreview from './MarkdownPreview.js';
```

Чтобы отложить загрузку кода этого компонента до его первого отображения, замените этот импорт на:

```js
import { lazy } from 'react';

const MarkdownPreview = lazy(() =>
    import('./MarkdownPreview.js')
);
```

Этот код опирается на [dynamic `import()`,](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import), что может потребовать поддержки со стороны вашего бандлера или фреймворка.

Теперь, когда код вашего компонента загружается по требованию, вам также необходимо указать, что должно отображаться во время его загрузки. Вы можете сделать это, обернув ленивый компонент или любого из его родителей в границу [`<Suspense>`](Suspense.md):

```js hl_lines="1 4"
<Suspense fallback={<Loading />}>
    <h2>Preview</h2>
    <MarkdownPreview />
</Suspense>
```

В этом примере код для `MarkdownPreview` не будет загружен, пока вы не попытаетесь его отобразить. Если `MarkdownPreview` еще не загрузился, вместо него будет показан `Loading`. Попробуйте установить флажок:

=== "App.js"

    ```js
    import { useState, Suspense, lazy } from 'react';
    import Loading from './Loading.js';

    const MarkdownPreview = lazy(() =>
    	delayForDemo(import('./MarkdownPreview.js'))
    );

    export default function MarkdownEditor() {
    	const [showPreview, setShowPreview] = useState(false);
    	const [markdown, setMarkdown] = useState(
    		'Hello, **world**!'
    	);
    	return (
    		<>
    			<textarea
    				value={markdown}
    				onChange={(e) =>
    					setMarkdown(e.target.value)
    				}
    			/>
    			<label>
    				<input
    					type="checkbox"
    					checked={showPreview}
    					onChange={(e) =>
    						setShowPreview(e.target.checked)
    					}
    				/>
    				Show preview
    			</label>
    			<hr />
    			{showPreview && (
    				<Suspense fallback={<Loading />}>
    					<h2>Preview</h2>
    					<MarkdownPreview markdown={markdown} />
    				</Suspense>
    			)}
    		</>
    	);
    }

    // Add a fixed delay so you can see the loading state
    function delayForDemo(promise) {
    	return new Promise((resolve) => {
    		setTimeout(resolve, 2000);
    	}).then(() => promise);
    }
    ```

=== "Loading.js"

    ```js
    export default function Loading() {
    	return (
    		<p>
    			<i>Loading...</i>
    		</p>
    	);
    }
    ```

=== "MarkdownPreview.js"

    ```js
    import { Remarkable } from 'remarkable';

    const md = new Remarkable();

    export default function MarkdownPreview({ markdown }) {
    	return (
    		<div
    			className="content"
    			dangerouslySetInnerHTML={{
    				__html: md.render(markdown),
    			}}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/nvsn7g?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="laughing-borg-nvsn7g" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Эта демонстрация загружается с искусственной задержкой. В следующий раз, когда вы снимите и установите флажок, `Preview` будет кэширован, поэтому состояния загрузки не будет. Чтобы снова увидеть состояние загрузки, нажмите "Сброс" в песочнице.

Подробнее об [управлении состояниями загрузки с помощью Suspense](Suspense.md).

## Устранение неполадок {#troubleshooting}

### Состояние моего компонента `lazy` неожиданно сбрасывается {#my-lazy-components-state-gets-reset-unexpectedly}

Не объявляйте компоненты `lazy` _внутри_ других компонентов:

```js hl_lines="4-7"
import { lazy } from 'react';

function Editor() {
    // 🔴 Bad: This will cause all state to be reset on re-renders
    const MarkdownPreview = lazy(() =>
        import('./MarkdownPreview.js')
    );
    // ...
}
```

Вместо этого всегда объявляйте их на верхнем уровне вашего модуля:

```js hl_lines="3-6"
import { lazy } from 'react';

// ✅ Good: Declare lazy components outside of your components
const MarkdownPreview = lazy(() =>
    import('./MarkdownPreview.js')
);

function Editor() {
    // ...
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/lazy](https://react.dev/reference/react/lazy)</small>
