---
description: createRoot позволяет создать корень для отображения компонентов React внутри узла DOM браузера
---

# createRoot

<big>`createRoot` позволяет создать корень для отображения компонентов React внутри узла DOM браузера.</big>

```js
const root = createRoot(domNode, options?)
```

## Описание {#reference}

### `createRoot(domNode, options?)` {#createroot}

Вызовите `createRoot` для создания корня React для отображения содержимого внутри элемента DOM браузера.

```js
import { createRoot } from 'react-dom/client';

const domNode = document.getElementById('root');
const root = createRoot(domNode);
```

React создаст корень для `domNode` и возьмет на себя управление DOM внутри него. После создания корня необходимо вызвать `root.render`, чтобы отобразить внутри него компонент React:

```js
root.render(<App />);
```

Приложение, полностью построенное на React, обычно имеет только один вызов `createRoot` для своего корневого компонента. Страница, которая использует "брызги" React для частей страницы, может иметь столько отдельных корней, сколько необходимо.

#### Параметры {#parameters}

-   `domNode`: [DOM-элемент.](https://developer.mozilla.org/docs/Web/API/Element) React создаст корень для этого DOM-элемента и позволит вам вызывать функции на корне, такие как `render` для отображения отрисованного содержимого React.
-   **опционально** `options`: Объект с опциями для этого корня React.
    -   **optional** `onRecoverableError`: Обратный вызов, вызываемый, когда React автоматически восстанавливает ошибки.
    -   **optional** `identifierPrefix`: Строковый префикс, который React использует для идентификаторов, генерируемых [`useId`.](../../react/useId.md) Полезно для предотвращения конфликтов при использовании нескольких корней на одной странице.

**Возвращает**

`createRoot` возвращает объект с двумя методами: `render` и `unmount`.

**Ограничения**

-   Если ваше приложение рендерится на сервере, использование `createRoot()` не поддерживается. Вместо этого используйте [`hydrateRoot()`](./hydrateRoot.md).
-   Скорее всего, в вашем приложении будет только один вызов `createRoot`. Если вы используете фреймворк, он может выполнить этот вызов за вас.
-   Когда вы хотите отобразить JSX в другой части дерева DOM, которая не является дочерней для вашего компонента (например, модальный экран или всплывающая подсказка), используйте [`createPortal`](../createPortal.md) вместо `createRoot`.

### `root.render(reactNode)` {#root-render}

Вызовите `root.render` для отображения части [JSX](../../../learn/writing-markup-with-jsx.md) ("React node") в DOM-узел браузера React root.

```js
root.render(<App />);
```

React отобразит `<App />` в `root` и возьмет на себя управление DOM внутри него.

**Параметры**

-   `reactNode`: _React-узел_, который вы хотите отобразить. Обычно это кусок JSX типа `<App />`, но вы также можете передать элемент React, созданный с помощью [`createElement()`](../../react/createElement.md), строку, число, `null` или `undefined`.

**Возвраты**

`root.render` возвращает `undefined`.

**Предупреждения**

-   При первом вызове `root.render`, React очистит все существующее HTML-содержимое внутри корня React перед рендерингом в него компонента React.
-   Если узел DOM вашего корня содержит HTML, сгенерированный React на сервере или во время сборки, используйте вместо этого [`hydrateRoot()`](./hydrateRoot.md), который прикрепляет обработчики событий к существующему HTML.
-   Если вы вызываете `render` на одном и том же корне более одного раза, React будет обновлять DOM по мере необходимости, чтобы отразить последний JSX, который вы передали. React будет решать, какие части DOM могут быть использованы повторно, а какие должны быть созданы заново, ["сопоставляя их"](../../../learn/preserving-and-resetting-state.md) с ранее отрисованным деревом. Повторный вызов `render` на том же корне аналогичен вызову функции [`set`](../../react/useState.md#setstate) на корневом компоненте: React позволяет избежать ненужных обновлений DOM.

### `root.unmount()` {#root-unmount}

Вызовите `root.unmount`, чтобы уничтожить дерево рендеринга внутри корня React.

```js
root.unmount();
```

Приложение, полностью построенное на React, обычно не содержит вызовов `root.unmount`.

Это в основном полезно, если DOM-узел вашего React root (или любой из его предков) может быть удален из DOM каким-либо другим кодом. Например, представьте себе панель вкладок jQuery, которая удаляет неактивные вкладки из DOM. Если вкладка будет удалена, все внутри нее (включая React roots внутри) также будет удалено из DOM. В этом случае вам нужно сказать React "прекратить" управление содержимым удаленного корня, вызвав `root.unmount`. В противном случае компоненты внутри удаленного корня не будут знать, что нужно очистить и освободить глобальные ресурсы, такие как подписки.

Вызов `root.unmount` размонтирует все компоненты в корне и "отсоединит" React от корневого DOM-узла, включая удаление любых обработчиков событий или состояния в дереве.

**Параметры**

`root.unmount` не принимает никаких параметров.

**Возвраты**

`root.unmount` возвращает `не определено`.

**Ограничения**

-   Вызов `root.unmount` приведет к размонтированию всех компонентов в дереве и "отсоединению" React от корневого DOM-узла.
-   После вызова `root.unmount` вы не сможете снова вызвать `root.render` на том же корне. Попытка вызвать `root.render` на немонтированном корне приведет к ошибке "Cannot update an unmounted root". Однако вы можете создать новый корень для одного и того же узла DOM после того, как предыдущий корень для этого узла был размонтирован.

## Использование {#usage}

### Рендеринг приложения, полностью построенного на React {#rendering-an-app-fully-built-with-react}

Если ваше приложение полностью построено с помощью React, создайте единый корень для всего приложения.

```js
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

Обычно этот код нужно запускать только один раз при запуске. Он выполнит:

1.  Найдет узел DOM браузера, определенный в вашем HTML.
2.  Отобразит компонент React для вашего приложения внутри.

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    	<head>
    		<title>My app</title>
    	</head>
    	<body>
    		<!-- This is the DOM node -->
    		<div id="root"></div>
    	</body>
    </html>
    ```

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import App from './App.js';
    import './styles.css';

    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
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

    <iframe src="https://codesandbox.io/embed/6r52t7?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**Если ваше приложение полностью построено на React, вам не нужно больше создавать корни или снова вызывать `root.render`**

С этого момента React будет управлять DOM всего вашего приложения. Чтобы добавить больше компонентов, [вложите их внутрь компонента `App`](../../../learn/importing-and-exporting-components.md) Когда вам нужно обновить пользовательский интерфейс, каждый из ваших компонентов может сделать это, [используя состояние](../../react/useState.md) Когда вам нужно отобразить дополнительный контент, например, модальное окно или подсказку, вне узла DOM, [отобразите его с помощью портала](../createPortal.md).

!!!note ""

    Когда ваш HTML пуст, пользователь видит пустую страницу, пока не загрузится и не запустится код JavaScript приложения:

    ```html
    <div id="root"></div>
    ```

    Это может показаться очень медленным! Чтобы решить эту проблему, вы можете генерировать исходный HTML из ваших компонентов [на сервере или во время сборки](../server/index.md). Тогда ваши посетители смогут читать текст, видеть изображения и нажимать на ссылки до того, как загрузится код JavaScript. Мы рекомендуем [использовать фреймворк](../../../learn/start-a-new-react-project.md#production-grade-react-frameworks), который выполняет эту оптимизацию из коробки. В зависимости от того, когда она выполняется, это называется _рендеринг на стороне сервера (SSR)_ или _статическая генерация сайта (SSG)_.

!!!warning "Серверный рендеринг"

    **Приложения, использующие серверный рендеринг или статическую генерацию, должны вызывать [`hydrateRoot`](./hydrateRoot.md) вместо `createRoot`.** React будет _гидрировать_ (повторно использовать) узлы DOM из вашего HTML вместо их уничтожения и повторного создания.

### Рендеринг страницы, частично построенной на React {#rendering-a-page-partially-built-with-react}

Если ваша страница [не полностью построена на React](../../../learn/add-react-to-an-existing-project.md#using-react-for-a-part-of-your-existing-page), вы можете вызвать `createRoot` несколько раз, чтобы создать корень для каждой части пользовательского интерфейса верхнего уровня, управляемой React. Вы можете отображать различное содержимое в каждом корне, вызывая `root.render`.

Здесь два разных компонента React отображаются в двух узлах DOM, определенных в файле `index.html`:

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    	<head>
    		<title>My app</title>
    	</head>
    	<body>
    		<nav id="navigation"></nav>
    		<main>
    			<p>
    				This paragraph is not rendered by React
    				(open index.html to verify).
    			</p>
    			<section id="comments"></section>
    		</main>
    	</body>
    </html>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { createRoot } from 'react-dom/client';
    import { Comments, Navigation } from './Components.js';

    const navDomNode = document.getElementById('navigation');
    const navRoot = createRoot(navDomNode);
    navRoot.render(<Navigation />);

    const commentDomNode = document.getElementById('comments');
    const commentRoot = createRoot(commentDomNode);
    commentRoot.render(<Comments />);
    ```

=== "Components.js"

    ```js
    export function Navigation() {
    	return (
    		<ul>
    			<NavLink href="/">Home</NavLink>
    			<NavLink href="/about">About</NavLink>
    		</ul>
    	);
    }

    function NavLink({ href, children }) {
    	return (
    		<li>
    			<a href={href}>{children}</a>
    		</li>
    	);
    }

    export function Comments() {
    	return (
    		<>
    			<h2>Comments</h2>
    			<Comment text="Hello!" author="Sophie" />
    			<Comment text="How are you?" author="Sunil" />
    		</>
    	);
    }

    function Comment({ text, author }) {
    	return (
    		<p>
    			{text} — <i>{author}</i>
    		</p>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/4z8jhc?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вы также можете создать новый узел DOM с помощью [`document.createElement()`](https://developer.mozilla.org/docs/Web/API/Document/createElement) и добавить его в документ вручную.

```js
const domNode = document.createElement('div');
const root = createRoot(domNode);
root.render(<Comment />);
// You can add it anywhere in the document
document.body.appendChild(domNode);
```

Чтобы удалить дерево React из узла DOM и очистить все используемые им ресурсы, вызовите `root.unmount`.

```js
root.unmount();
```

Это особенно полезно, если ваши компоненты React находятся внутри приложения, написанного на другом фреймворке.

### Обновление корневого компонента {#updating-a-root-component}

Вы можете вызывать `render` более одного раза для одного и того же корня. Пока структура дерева компонентов соответствует тому, что было отображено ранее, React будет [сохранять состояние.](../../../learn/preserving-and-resetting-state.md) Обратите внимание, что вы можете вводить данные, что означает, что обновления от повторных вызовов `render` каждую секунду в этом примере не являются разрушительными:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import './styles.css';
    import App from './App.js';

    const root = createRoot(document.getElementById('root'));

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

    <iframe src="https://codesandbox.io/embed/dz8j76?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Очень редко приходится вызывать `render` несколько раз. Обычно вместо этого ваши компоненты будут [обновлять состояние](../../react/useState.md).

## Устранение неполадок {#troubleshooting}

### Я создал корень, но ничего не отображается {#ive-created-a-root-but-nothing-is-displayed}

Убедитесь, что вы не забыли на самом деле _создать_ ваше приложение в корне:

```js hl_lines="5"
import { createRoot } from 'react-dom/client';
import App from './App.js';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

Пока вы этого не сделаете, ничего не будет отображаться.

### Я получаю ошибку: "Target container is not a DOM element" {#im-getting-an-error-target-container-is-not-a-dom-element}

Эта ошибка означает, что все, что вы передаете в `createRoot`, не является узлом DOM.

Если вы не уверены в том, что происходит, попробуйте записать лог:

```js hl_lines="2"
const domNode = document.getElementById('root');
console.log(domNode); // ???
const root = createRoot(domNode);
root.render(<App />);
```

Например, если `domNode` равен `null`, это означает, что [`getElementById`](https://developer.mozilla.org/docs/Web/API/Document/getElementById) вернул `null`. Это произойдет, если в документе нет узла с заданным ID на момент вашего вызова. Причин может быть несколько:

1.  Идентификатор, который вы ищете, может отличаться от идентификатора, который вы использовали в HTML-файле. Проверьте, нет ли опечаток!
2.  Тег `<script>` вашего пакета не может "увидеть" узлы DOM, которые появляются _после_ него в HTML.

Другой распространенный способ получить эту ошибку - написать `createRoot(<App />)` вместо `createRoot(domNode)`.

### Я получаю ошибку: "Функции не действительны как дочерние React" {#im-getting-an-error-functions-are-not-valid-as-a-react-child}

Эта ошибка означает, что все, что вы передаете в `root.render`, не является компонентом React.

Это может произойти, если вы вызываете `root.render` с `Component` вместо `<Component />`:

```js hl_lines="2 5"
// 🚩 Wrong: App is a function, not a Component.
root.render(App);

// ✅ Correct: <App /> is a component.
root.render(<App />);
```

Или если вы передаете функцию в `root.render`, а не результат ее вызова:

```js hl_lines="2 5"
// 🚩 Wrong: createApp is a function, not a component.
root.render(createApp);

// ✅ Correct: call createApp to return a component.
root.render(createApp());
```

### Мой серверный рендеринг HTML создается заново {#my-server-rendered-html-gets-re-created-from-scratch}

Если ваше приложение рендерится на сервере и включает первоначальный HTML, сгенерированный React, вы можете заметить, что создание корня и вызов `root.render` удаляет весь этот HTML, а затем заново создает все узлы DOM с нуля. Это может быть медленнее, сбрасывает фокус и позиции прокрутки, а также может потерять другие пользовательские данные.

Приложения с серверным рендерингом должны использовать [`hydrateRoot`](./hydrateRoot.md) вместо `createRoot`:

```js hl_lines="1 4"
import { hydrateRoot } from 'react-dom/client';
import App from './App.js';

hydrateRoot(document.getElementById('root'), <App />);
```

Обратите внимание, что его API отличается. В частности, обычно не происходит дальнейшего вызова `root.render`.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/client/createRoot></small>
