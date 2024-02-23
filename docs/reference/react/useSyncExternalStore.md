---
description: useSyncExternalStore - это хук React, позволяющий подписаться на внешнее хранилище
---

# useSyncExternalStore

<big>**`useSyncExternalStore`** - это хук React, позволяющий подписаться на внешнее хранилище.</big>

```js
const snapshot = useSyncExternalStore(
	subscribe,
	getSnapshot,
	getServerSnapshot?
)
```

## Описание {#reference}

### `useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)` {#usesyncexternalstore}

Вызовите `useSyncExternalStore` на верхнем уровне вашего компонента для чтения значения из внешнего хранилища данных.

```js
import { useSyncExternalStore } from 'react';
import { todosStore } from './todoStore.js';

function TodosApp() {
    const todos = useSyncExternalStore(
        todosStore.subscribe,
        todosStore.getSnapshot
    );
    // ...
}
```

Она возвращает моментальный снимок данных в хранилище. В качестве аргументов необходимо передать две функции:

1.  Функция `subscribe` должна подписываться на стор и возвращать функцию, которая отписывается.
2.  Функция `getSnapshot` должна считывать моментальный снимок данных из хранилища.

#### Параметры {#parameters}

-   `subscribe`: Функция, принимающая один аргумент `callback` и подписывающаяся на стор. Когда стор изменяется, он должен вызвать предоставленный `callback`. Это приведет к повторному отображению компонента. Функция `subscribe` должна возвращать функцию, которая очищает подписку.

-   `getSnapshot`: Функция, которая возвращает снимок данных в хранилище, необходимых компоненту. Пока хранилище не изменилось, повторные вызовы `getSnapshot` должны возвращать одно и то же значение. Если стор изменился, а возвращаемое значение отличается (по сравнению с [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), React перерисовывает компонент.

-   **опциональная** `getServerSnapshot`: Функция, возвращающая начальный снимок данных в хранилище. Он будет использоваться только при рендеринге сервера и при гидратации рендеримого сервером контента на клиенте. Серверный снимок должен быть одинаковым для клиента и сервера, и обычно сериализуется и передается от сервера к клиенту. Если вы опустите этот аргумент, рендеринг компонента на сервере приведет к ошибке.

#### Возвращает {#returns}

Текущий снимок хранилища, который вы можете использовать в своей логике рендеринга.

#### Ограничения {#caveats}

-   Снимок хранилища, возвращаемый `getSnapshot`, должен быть неизменяемым. Если базовое хранилище имеет изменяемые данные, верните новый неизменяемый снимок, если данные изменились. В противном случае возвращается кэшированный последний снимок.

-   Если во время повторного рендеринга передается другая функция `subscribe`, React повторно подпишется на стор, используя новую переданную функцию `subscribe`. Вы можете предотвратить это, объявив `subscribe` вне компонента.

-   Если хранилище будет [изменено во время неблокируемого обновления перехода](useTransition.md), React вернется к выполнению этого обновления как блокирующего. В частности, при каждом обновлении перехода React будет вызывать `getSnapshot` второй раз непосредственно перед применением изменений к DOM. Если он вернет другое значение, чем при первоначальном вызове, React перезапустит обновление с нуля, на этот раз применяя его как блокирующее обновление, чтобы гарантировать, что каждый компонент на экране отражает одну и ту же версию хранилища.

-   Не рекомендуется приостанавливать рендеринг на основе значения хранилища, возвращаемого `useSyncExternalStore`. Причина в том, что мутации во внешнем хранилище не могут быть помечены как [неблокирующие обновления переходов](useTransition.md), поэтому они будут вызывать ближайший [фолбек `Suspense`](Suspense.md), заменяя уже отрендеренный контент на экране загрузочным спиннером, что, как правило, создает плохой UX.

    Например, не рекомендуется использовать следующее:

    ```js
    const LazyProductDetailPage = lazy(
    	() => import('./ProductDetailPage.js')
    );

    function ShoppingApp() {
    	const selectedProductId = useSyncExternalStore(...);

    	// ❌ Calling `use` with a Promise dependent on `selectedProductId`
    	const data = use(fetchItem(selectedProductId))

    	// ❌ Conditionally rendering a lazy component based
    	// on `selectedProductId`
    	return selectedProductId != null
    		? <LazyProductDetailPage />
    		: <FeaturedProducts />;
    }
    ```

## Использование {#usage}

### Подписка на внешний стор {#subscribing-to-an-external-store}

Большинство ваших компонентов React будут читать данные только из своих [пропсов](../../learn/passing-props-to-a-component.md), [состояния](useState.md) и [контекста](useContext.md). Однако иногда компоненту необходимо читать данные из какого-то хранилища вне React, которое меняется со временем. К ним относятся:

-   Сторонние библиотеки управления состоянием, которые хранят состояние вне React.
-   Браузерные API, которые предоставляют изменяемое значение и события для подписки на его изменения.

Вызовите `useSyncExternalStore` на верхнем уровне вашего компонента, чтобы прочитать значение из внешнего хранилища данных.

```js
import { useSyncExternalStore } from 'react';
import { todosStore } from './todoStore.js';

function TodosApp() {
    const todos = useSyncExternalStore(
        todosStore.subscribe,
        todosStore.getSnapshot
    );
    // ...
}
```

Она возвращает моментальный снимок данных в хранилище. Вам нужно передать две функции в качестве аргументов:

1.  Функция `subscribe` должна подписываться на стор и возвращать функцию, которая отписывается.
2.  `getSnapshot` функция должна прочитать снимок данных из стора.

React будет использовать эти функции, чтобы сохранить ваш компонент подписанным на стор и перерисовывать его при изменениях.

Например, в песочнице ниже, `todosStore` реализован как внешний стор, который хранит данные вне React. Компонент `TodosApp` подключается к этому внешнему хранилищу с помощью хука `useSyncExternalStore`.

=== "App.js"

    ```js
    import { useSyncExternalStore } from 'react';
    import { todosStore } from './todoStore.js';

    export default function TodosApp() {
    	const todos = useSyncExternalStore(
    		todosStore.subscribe,
    		todosStore.getSnapshot
    	);
    	return (
    		<>
    			<button onClick={() => todosStore.addTodo()}>
    				Add todo
    			</button>
    			<hr />
    			<ul>
    				{todos.map((todo) => (
    					<li key={todo.id}>{todo.text}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "todoStore.js"

    ```js
    // This is an example of a third-party store
    // that you might need to integrate with React.

    // If your app is fully built with React,
    // we recommend using React state instead.

    let nextId = 0;
    let todos = [{ id: nextId++, text: 'Todo #1' }];
    let listeners = [];

    export const todosStore = {
    	addTodo() {
    		todos = [
    			...todos,
    			{ id: nextId++, text: 'Todo #' + nextId },
    		];
    		emitChange();
    	},
    	subscribe(listener) {
    		listeners = [...listeners, listener];
    		return () => {
    			listeners = listeners.filter(
    				(l) => l !== listener
    			);
    		};
    	},
    	getSnapshot() {
    		return todos;
    	},
    };

    function emitChange() {
    	for (let listener of listeners) {
    		listener();
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/36pmft?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Встроенное состояние"

    Когда это возможно, мы рекомендуем использовать встроенное состояние React с помощью [`useState`](useState.md) и [`useReducer`](useReducer.md). API `useSyncExternalStore` в основном полезен, если вам нужно интегрироваться с существующим не-React кодом.

### Подписка на API браузера {#subscribing-to-a-browser-api}

Еще одна причина добавить `useSyncExternalStore` - это когда вы хотите подписаться на какое-то значение, предоставляемое браузером, которое меняется со временем. Например, предположим, что вы хотите, чтобы ваш компонент отображал, активно ли сетевое соединение. Браузер предоставляет эту информацию через свойство [`navigator.onLine`](https://developer.mozilla.org/docs/Web/API/Navigator/onLine).

Это значение может меняться без ведома React, поэтому вы должны считывать его с помощью `useSyncExternalStore`.

```js
import { useSyncExternalStore } from 'react';

function ChatIndicator() {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot
    );
    // ...
}
```

Чтобы реализовать функцию `getSnapshot`, прочитайте текущее значение из API браузера:

```js
function getSnapshot() {
    return navigator.onLine;
}
```

Далее необходимо реализовать функцию `subscribe`. Например, при изменении `navigator.onLine` браузер запускает события [`online`](https://developer.mozilla.org/docs/Web/API/Window/online_event) и [`offline`](https://developer.mozilla.org/docs/Web/API/Window/offline_event) на объекте `window`. Вам нужно подписать аргумент `callback` на соответствующие события, а затем вернуть функцию, которая очистит подписки:

```js
function subscribe(callback) {
    window.addEventListener('online', callback);
    window.addEventListener('offline', callback);
    return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
    };
}
```

Теперь React знает, как прочитать значение из внешнего API `navigator.onLine` и как подписаться на его изменения. Отключите устройство от сети и обратите внимание на то, что в ответ на это компонент снова отображается:

=== "App.js"

    ```js
    import { useSyncExternalStore } from 'react';

    export default function ChatIndicator() {
    	const isOnline = useSyncExternalStore(
    		subscribe,
    		getSnapshot
    	);
    	return (
    		<h1>
    			{isOnline ? '✅ Online' : '❌ Disconnected'}
    		</h1>
    	);
    }

    function getSnapshot() {
    	return navigator.onLine;
    }

    function subscribe(callback) {
    	window.addEventListener('online', callback);
    	window.addEventListener('offline', callback);
    	return () => {
    		window.removeEventListener('online', callback);
    		window.removeEventListener('offline', callback);
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dmhft8?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Извлечение логики в пользовательский хук {#extracting-the-logic-to-a-custom-hook}

Обычно вы не будете писать `useSyncExternalStore` непосредственно в своих компонентах. Вместо этого вы, как правило, вызываете его из своего собственного пользовательского хука. Это позволяет вам использовать одно и то же внешнее хранилище в разных компонентах.

Например, этот пользовательский хук `useOnlineStatus` отслеживает, находится ли сеть в режиме онлайн:

```js hl_lines="3 9"
import { useSyncExternalStore } from 'react';

export function useOnlineStatus() {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot
    );
    return isOnline;
}

function getSnapshot() {
    // ...
}

function subscribe(callback) {
    // ...
}
```

Теперь различные компоненты могут вызывать `useOnlineStatus` без повторения базовой реализации:

=== "App.js"

    ```js
    import { useOnlineStatus } from './useOnlineStatus.js';

    function StatusBar() {
    	const isOnline = useOnlineStatus();
    	return (
    		<h1>
    			{isOnline ? '✅ Online' : '❌ Disconnected'}
    		</h1>
    	);
    }

    function SaveButton() {
    	const isOnline = useOnlineStatus();

    	function handleSaveClick() {
    		console.log('✅ Progress saved');
    	}

    	return (
    		<button
    			disabled={!isOnline}
    			onClick={handleSaveClick}
    		>
    			{isOnline ? 'Save progress' : 'Reconnecting...'}
    		</button>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<SaveButton />
    			<StatusBar />
    		</>
    	);
    }
    ```

=== "useOnlineStatus.js"

    ```js
    import { useSyncExternalStore } from 'react';

    export function useOnlineStatus() {
    	const isOnline = useSyncExternalStore(
    		subscribe,
    		getSnapshot
    	);
    	return isOnline;
    }

    function getSnapshot() {
    	return navigator.onLine;
    }

    function subscribe(callback) {
    	window.addEventListener('online', callback);
    	window.addEventListener('offline', callback);
    	return () => {
    		window.removeEventListener('online', callback);
    		window.removeEventListener('offline', callback);
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/l88skq?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Добавление поддержки серверного рендеринга {#adding-support-for-server-rendering}

Если ваше приложение React использует [серверный рендеринг](../react-dom/server/index.md), ваши компоненты React также будут запускаться вне среды браузера для генерации начального HTML. Это создает несколько проблем при подключении к внешнему стору:

-   Если вы подключаетесь к API только для браузера, он не будет работать, поскольку не существует на сервере.
-   Если вы подключаетесь к стороннему хранилищу данных, вам потребуется, чтобы его данные совпадали на сервере и клиенте.

Чтобы решить эти проблемы, передайте функцию `getServerSnapshot` в качестве третьего аргумента в `useSyncExternalStore`:

```js hl_lines="4-8 16-18"
import { useSyncExternalStore } from 'react';

export function useOnlineStatus() {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot,
        getServerSnapshot
    );
    return isOnline;
}

function getSnapshot() {
    return navigator.onLine;
}

function getServerSnapshot() {
    return true; // Always show "Online" for server-generated HTML
}

function subscribe(callback) {
    // ...
}
```

Функция `getServerSnapshot` похожа на `getSnapshot`, но запускается только в двух ситуациях:

-   Она запускается на сервере при генерации HTML.
-   Она запускается на клиенте во время [hydration](../react-dom/client/hydrateRoot.md), т. е. когда React берет серверный HTML и делает его интерактивным.

Это позволяет указать начальное значение snapshot, которое будет использоваться до того, как приложение станет интерактивным. Если нет значимого начального значения для серверного рендеринга, опустите этот аргумент для [принудительного рендеринга на клиенте](Suspense.md).

!!!note ""

    Убедитесь, что `getServerSnapshot` возвращает те же данные при первоначальном рендеринге на клиенте, что и на сервере. Например, если `getServerSnapshot` вернул некоторое предварительно заполненное содержимое стора на сервере, вам нужно передать это содержимое клиенту. Один из способов сделать это - выдать тег `<script>` во время рендеринга сервера, который устанавливает глобал типа `window.MY_STORE_DATA`, и читать из этого глобала на клиенте в `getServerSnapshot`. Ваш внешний стор должен предоставить инструкции о том, как это сделать.

## Устранение неполадок {#troubleshooting}

### Я получаю ошибку: "The result of `getSnapshot` should be cached" {#im-getting-an-error-the-result-of-getsnapshot-should-be-cached}

Эта ошибка означает, что ваша функция `getSnapshot` возвращает новый объект при каждом вызове, например:

```js hl_lines="2-5"
function getSnapshot() {
    // 🔴 Do not return always different objects from getSnapshot
    return {
        todos: myStore.todos,
    };
}
```

React будет перерисовывать компонент, если возвращаемое значение `getSnapshot` отличается от предыдущего. Вот почему, если вы всегда возвращаете другое значение, вы попадете в бесконечный цикл и получите эту ошибку.

Ваш объект `getSnapshot` должен возвращать другой объект только в том случае, если что-то действительно изменилось. Если ваше хранилище содержит неизменяемые данные, вы можете возвращать эти данные напрямую:

```js hl_lines="2-3"
function getSnapshot() {
    // ✅ You can return immutable data
    return myStore.todos;
}
```

Если данные вашего стора изменчивы, ваша функция `getSnapshot` должна возвращать неизменяемый снимок. Это означает, что ей _нужно_ создавать новые объекты, но она не должна делать это при каждом вызове. Вместо этого она должна хранить последний вычисленный снимок и возвращать тот же снимок, что и в прошлый раз, если данные в хранилище не изменились. Как определить, изменились ли изменяемые данные, зависит от вашего хранилища изменяемых данных.

### Моя функция `subscribe` вызывается после каждого рендеринга {#my-subscribe-function-gets-called-after-every-re-render}

Эта функция `subscribe` определена _внутри_ компонента, поэтому при каждом повторном рендере она будет другой:

```js hl_lines="7-11"
function ChatIndicator() {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot
    );

    // 🚩 Always a different function,
    // so React will resubscribe on every re-render
    function subscribe() {
        // ...
    }

    // ...
}
```

React повторно подпишется на ваш стор, если вы передадите другую функцию `subscribe` между повторными рендерами. Если это вызывает проблемы с производительностью и вы хотите избежать повторной подписки, переместите функцию `subscribe` наружу:

```js hl_lines="9-12"
function ChatIndicator() {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot
    );
    // ...
}

// ✅ Always the same function, so React won't need to resubscribe
function subscribe() {
    // ...
}
```

Как вариант, оберните `subscribe` в [`useCallback`](useCallback.md), чтобы повторно подписываться только при изменении какого-либо аргумента:

```js hl_lines="7-10"
function ChatIndicator({ userId }) {
    const isOnline = useSyncExternalStore(
        subscribe,
        getSnapshot
    );

    // ✅ Same function as long as userId doesn't change
    const subscribe = useCallback(() => {
        // ...
    }, [userId]);

    // ...
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useSyncExternalStore](https://react.dev/reference/react/useSyncExternalStore)</small>
