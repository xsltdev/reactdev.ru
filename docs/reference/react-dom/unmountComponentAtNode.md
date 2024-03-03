---
status: deprecated
description: unmountComponentAtNode удаляет смонтированный компонент React из DOM
---

# unmountComponentAtNode

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

    В React 18 функция `unmountComponentAtNode` была заменена на [`root.unmount()`](./client/createRoot.md#root-unmount).

<big>`unmountComponentAtNode` удаляет смонтированный компонент React из DOM.</big>

```js
unmountComponentAtNode(domNode);
```

## Описание {#reference}

### `unmountComponentAtNode(domNode)` {#unmountcomponentatnode}

Вызовите `unmountComponentAtNode`, чтобы удалить смонтированный React-компонент из DOM и очистить его обработчики событий и состояние.

```js
import { unmountComponentAtNode } from 'react-dom';

const domNode = document.getElementById('root');
render(<App />, domNode);

unmountComponentAtNode(domNode);
```

**Параметры**

-   `domNode`: [DOM-элемент.](https://developer.mozilla.org/docs/Web/API/Element) React удалит смонтированный React-компонент из этого элемента.

**Возвращает**

`unmountComponentAtNode` возвращает `true`, если компонент был размонтирован, и `false` в противном случае.

## Использование {#usage}

Вызовите `unmountComponentAtNode` для удаления монтированного React компонента из узла DOM браузера и очистки его обработчиков событий и состояния.

```js
import { render, unmountComponentAtNode } from 'react-dom';
import App from './App.js';

const rootNode = document.getElementById('root');
render(<App />, rootNode);

// ...
unmountComponentAtNode(rootNode);
```

### Удаление приложения React из элемента DOM {#removing-a-react-app-from-a-dom-element}

Иногда вам может понадобиться "рассыпать" React на существующую страницу или страницу, которая не полностью написана на React. В таких случаях вам может понадобиться "остановить" React-приложение, удалив весь пользовательский интерфейс, состояние и слушателей из узла DOM, в который оно было отображено.

В этом примере нажатие кнопки "Render React App" приведет к рендерингу приложения React. Нажмите "Unmount React App", чтобы уничтожить его:

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    	<head>
    		<title>My app</title>
    	</head>
    	<body>
    		<button id="render">Render React App</button>
    		<button id="unmount">Unmount React App</button>
    		<!-- This is the React App node -->
    		<div id="root"></div>
    	</body>
    </html>
    ```

=== "index.js"

    ```js
    import './styles.css';
    import { render, unmountComponentAtNode } from 'react-dom';
    import App from './App.js';

    const domNode = document.getElementById('root');

    document
    	.getElementById('render')
    	.addEventListener('click', () => {
    		render(<App />, domNode);
    	});

    document
    	.getElementById('unmount')
    	.addEventListener('click', () => {
    		unmountComponentAtNode(domNode);
    	});
    ```

=== "App.js"

    ```js
    export default function App() {
    	return <h1>Hello, world!</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/7d7spl?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/unmountComponentAtNode></small>
