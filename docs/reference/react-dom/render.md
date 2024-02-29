# render

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

    В React 18 `render` был заменен на [`createRoot`](./client/createRoot.md). Использование `render` в React 18 предупредит, что ваше приложение будет вести себя так, как будто оно работает на React 17.

`render` рендерит часть [JSX](../../learn/writing-markup-with-jsx.md) ("узел React") в DOM-узел браузера.

```js
render(reactNode, domNode, callback?)
```

## Описание

### `render(reactNode, domNode, callback?)`

Вызывает `render` для отображения компонента React внутри элемента DOM браузера.

```js
import { render } from 'react-dom';

const domNode = document.getElementById('root');
render(<App />, domNode);
```

React отобразит `<App />` в `domNode` и возьмет на себя управление DOM внутри него.

Приложение, полностью построенное на React, обычно имеет только один вызов `render` со своим корневым компонентом. Страница, использующая "брызги" React для отдельных частей страницы, может иметь столько вызовов `render`, сколько необходимо.

#### Параметры

-   `reactNode`: _React-узел_, который вы хотите отобразить. Обычно это кусок JSX типа `<App />`, но вы также можете передать элемент React, созданный с помощью [`createElement()`](../react/createElement.md), строку, число, `null` или `undefined`.
-   `domNode`: [DOM-элемент.](https://developer.mozilla.org/docs/Web/API/Element) React отобразит `reactNode`, который вы передадите внутри этого DOM-элемента. С этого момента React будет управлять DOM внутри `domNode` и обновлять его при изменении вашего дерева React.
-   **опционально** `callback`: Функция. Если она передана, React вызовет ее после того, как ваш компонент будет помещен в DOM.

#### Возврат

Функция `render` обычно возвращает `null`. Однако, если переданный вами `reactNode` является компонентом _класса_, то он вернет экземпляр этого компонента.

#### Предостережения

-   В React 18 `render` был заменен на [`createRoot`.](./client/createRoot.md) Пожалуйста, используйте `createRoot` для React 18 и последующих версий.
-   При первом вызове `render`, React очистит все существующее HTML содержимое внутри `domNode` перед рендерингом React компонента в него. Если ваш `domNode` содержит HTML, сгенерированный React на сервере или во время сборки, используйте вместо этого [`hydrate()`](hydrate.md), который прикрепляет обработчики событий к существующему HTML.
-   Если вы вызываете `render` на одном и том же `domNode` более одного раза, React будет обновлять DOM по мере необходимости, чтобы отразить последний JSX, который вы передали. React будет решать, какие части DOM могут быть использованы повторно, а какие должны быть созданы заново, ["сопоставляя их"](../../learn/preserving-and-resetting-state.md) с ранее отрисованным деревом. Повторный вызов `render` на том же `domNode` аналогичен вызову функции [`set`](../react/useState.md#setstate) на корневом компоненте: React позволяет избежать ненужных обновлений DOM.
-   Если ваше приложение полностью построено на React, то, скорее всего, в вашем приложении будет только один вызов `render`. (Если вы используете фреймворк, он может сделать этот вызов за вас.) Когда вы хотите отобразить часть JSX в другой части дерева DOM, которая не является дочерней для вашего компонента (например, модальный или всплывающий экран), используйте [`createPortal`](createPortal.md) вместо `render`.

## Использование

Вызовите `render` для отображения компонента React внутри DOM-узла браузера.

```js
import { render } from 'react-dom';
import App from './App.js';

render(<App />, document.getElementById('root'));
```

### Рендеринг корневого компонента

В приложениях, полностью построенных на React, **вы обычно делаете это только один раз при запуске** - для рендеринга "корневого" компонента.

=== "index.js"

    ```js
    import './styles.css';
    import { render } from 'react-dom';
    import App from './App.js';

    render(<App />, document.getElementById('root'));
    ```

=== "App.js"

    ```js
    export default function App() {
    	return <h1>Hello, world!</h1>;
    }
    ```

Обычно вам не нужно вызывать `render` снова или вызывать его в других местах. С этого момента React будет управлять DOM вашего приложения. Для обновления пользовательского интерфейса ваши компоненты будут [использовать состояние](../react/useState.md).

### Рендеринг нескольких корней

Если ваша страница [не полностью построена на React](../../learn/add-react-to-an-existing-project.md#using-react-for-a-part-of-your-existing-page), вызовите `render` для каждой части пользовательского интерфейса верхнего уровня, управляемой React.

=== "public/index.html"

    ```html
    <nav id="navigation"></nav>
    <main>
    	<p>
    		This paragraph is not rendered by React (open
    		index.html to verify).
    	</p>
    	<section id="comments"></section>
    </main>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { render } from 'react-dom';
    import { Comments, Navigation } from './Components.js';

    render(
    	<Navigation />,
    	document.getElementById('navigation')
    );

    render(<Comments />, document.getElementById('comments'));
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

Вы можете уничтожить отрисованные деревья с помощью [`unmountComponentAtNode()`.](unmountComponentAtNode.md)

### Обновление отрисованного дерева

Вы можете вызывать `render` более одного раза на одном и том же узле DOM. До тех пор, пока структура дерева компонентов будет соответствовать тому, что было отрисовано ранее, React будет [сохранять состояние.](../../learn/preserving-and-resetting-state.md) Обратите внимание, что вы можете вводить данные, что означает, что обновления от повторных вызовов `render` каждую секунду не являются разрушительными:

=== "index.js"

    ```js
    import { render } from 'react-dom';
    import './styles.css';
    import App from './App.js';

    let i = 0;
    setInterval(() => {
    	render(
    		<App counter={i} />,
    		document.getElementById('root')
    	);
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

Очень редко приходится вызывать `render` несколько раз. Обычно вместо этого вы будете [обновлять состояние](../react/useState.md) внутри своих компонентов.
