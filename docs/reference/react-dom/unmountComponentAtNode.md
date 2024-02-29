---
status: deprecated
---

# unmountComponentAtNode

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

    В React 18 функция `unmountComponentAtNode` была заменена на [`root.unmount()`](./client/createRoot.md#root-unmount).

`unmountComponentAtNode` удаляет смонтированный компонент React из DOM.

```js
unmountComponentAtNode(domNode);
```

## Описание

### `unmountComponentAtNode(domNode)`

Вызовите `unmountComponentAtNode`, чтобы удалить смонтированный React-компонент из DOM и очистить его обработчики событий и состояние.

```js
import { unmountComponentAtNode } from 'react-dom';

const domNode = document.getElementById('root');
render(<App />, domNode);

unmountComponentAtNode(domNode);
```

#### Параметры

-   `domNode`: [DOM-элемент.](https://developer.mozilla.org/docs/Web/API/Element) React удалит смонтированный React-компонент из этого элемента.

#### Возвращает

`unmountComponentAtNode` возвращает `true`, если компонент был размонтирован, и `false` в противном случае.

## Использование

Вызовите `unmountComponentAtNode` для удаления монтированного React компонента из узла DOM браузера и очистки его обработчиков событий и состояния.

```js
import { render, unmountComponentAtNode } from 'react-dom';
import App from './App.js';

const rootNode = document.getElementById('root');
render(<App />, rootNode);

// ...
unmountComponentAtNode(rootNode);
```

### Удаление приложения React из элемента DOM

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
