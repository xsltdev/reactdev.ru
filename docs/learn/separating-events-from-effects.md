---
description: В отличие от обработчиков событий, эффекты повторно синхронизируются, если какое-либо значение, которое они считывают, например пропс или переменная состояния, отличается от того, что было во время последнего рендеринга
---

# Отделение событий от эффектов

<big>Обработчики событий запускаются повторно только при повторном выполнении того же взаимодействия. В отличие от обработчиков событий, эффекты повторно синхронизируются, если какое-либо значение, которое они считывают, например пропс или переменная состояния, отличается от того, что было во время последнего рендеринга. Иногда требуется сочетание обоих типов поведения: Эффект, который повторно запускается в ответ на некоторые значения, но не на другие. На этой странице вы узнаете, как это сделать.</big>

!!!tip "Вы узнаете"

    -   Как выбрать между обработчиком событий и эффектом
    -   Почему эффекты являются реактивными, а обработчики событий - нет
    -   Что делать, если вы хотите, чтобы часть кода вашего Эффекта не была реактивной
    -   Что такое события эффектов и как извлекать их из эффектов
    -   Как считывать последние пропсы и состояние из Эффектов с помощью событий эффектов

## Выбор между обработчиками событий и Эффектами {#choosing-between-event-handlers-and-effects}

Во-первых, давайте вспомним разницу между обработчиками событий и Эффектами.

Представьте, что вы реализуете компонент чата. Ваши требования выглядят следующим образом:

1.  Ваш компонент должен автоматически подключаться к выбранному чату.
2.  Когда вы нажимаете кнопку "Отправить", он должен отправлять сообщение в чат.

Допустим, вы уже реализовали код для них, но не уверены, куда его поместить. Следует ли вам использовать обработчики событий или эффекты? Каждый раз, когда вам нужно ответить на этот вопрос, подумайте [_почему_ код должен выполняться](synchronizing-with-effects.md)

### Обработчики событий запускаются в ответ на конкретные взаимодействия {#event-handlers-run-in-response-to-specific-interactions}

С точки зрения пользователя, отправка сообщения должна произойти _потому что_ была нажата конкретная кнопка "Отправить". Пользователь будет очень расстроен, если вы отправите его сообщение в любое другое время или по любой другой причине. Вот почему отправка сообщения должна быть обработчиком событий. Обработчики событий позволяют вам обрабатывать определенные взаимодействия:

```js hl_lines="4-6"
function ChatRoom({ roomId }) {
    const [message, setMessage] = useState('');
    // ...
    function handleSendClick() {
        sendMessage(message);
    }
    // ...
    return (
        <>
            <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <button onClick={handleSendClick}>Send</button>;
        </>
    );
}
```

С обработчиком событий вы можете быть уверены, что `sendMessage(message)` будет _только_ если пользователь нажмет на кнопку.

### Эффекты запускаются всякий раз, когда необходима синхронизация {#effects-run-whenever-synchronization-is-needed}

Вспомните, что вам также нужно, чтобы компонент был подключен к чату. Где находится этот код?

Причиной для запуска этого кода не является какое-то конкретное взаимодействие. Неважно, почему или как пользователь перешел на экран чата. Теперь, когда они смотрят на него и могут взаимодействовать с ним, компонент должен оставаться подключенным к выбранному серверу чата. Даже если компонент чата был начальным экраном вашего приложения, и пользователь не выполнял никаких действий, вам _все равно_ потребуется подключение. Вот почему это Эффект:

```js hl_lines="3-12"
function ChatRoom({ roomId }) {
    // ...
    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => {
            connection.disconnect();
        };
    }, [roomId]);
    // ...
}
```

С помощью этого кода вы можете быть уверены, что всегда будет активное соединение с выбранным сервером чата, _независимо_ от конкретных действий, выполняемых пользователем. Открыл ли пользователь ваше приложение, выбрал другую комнату или перешел на другой экран и обратно, ваш эффект гарантирует, что компонент будет _оставаться синхронизированным_ с текущей выбранной комнатой и будет [переподключаться, когда это необходимо](lifecycle-of-reactive-effects.md).

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection, sendMessage } from './chat.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId }) {
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	function handleSendClick() {
    		sendMessage(message);
    	}

    	return (
    		<>
    			<h1>Welcome to the {roomId} room!</h1>
    			<input
    				value={message}
    				onChange={(e) => setMessage(e.target.value)}
    			/>
    			<button onClick={handleSendClick}>Send</button>
    		</>
    	);
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Close chat' : 'Open chat'}
    			</button>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function sendMessage(message) {
    	console.log('🔵 You sent: ' + message);
    }

    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log(
    				'✅ Connecting to "' +
    					roomId +
    					'" room at ' +
    					serverUrl +
    					'...'
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    		},
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/rtzvf2?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Реактивные значения и реактивная логика {#reactive-values-and-reactive-logic}

Интуитивно можно сказать, что обработчики событий всегда запускаются "вручную", например, при нажатии на кнопку. Эффекты, с другой стороны, являются "автоматическими": они запускаются и перезапускаются так часто, как это необходимо для сохранения синхронизации.

Есть более точный способ подумать об этом.

пропсы, состояния и переменные, объявленные в теле компонента, называются реактивными значениями. В этом примере `serverUrl` не является реактивным значением, но `roomId` и `message` являются таковыми. Они участвуют в потоке данных рендеринга:

```js
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
    const [message, setMessage] = useState('');

    // ...
}
```

Реактивные значения, такие как эти, могут измениться в результате повторного рендеринга. Например, пользователь может изменить `сообщение` или выбрать другой `номер комнаты` в выпадающем списке. Обработчики событий и эффекты по-разному реагируют на изменения:

-   **Логика внутри обработчиков событий _не реактивна._** Она не будет запущена снова, пока пользователь не выполнит то же самое действие (например, щелчок) снова. Обработчики событий могут считывать реактивные значения, не "реагируя" на их изменения.
-   Если ваш эффект считывает реактивное значение, [вы должны указать его как зависимость](lifecycle-of-reactive-effects.md), то, если при повторном рендеринге это значение изменится, React запустит логику вашего эффекта заново с новым значением.

Давайте вернемся к предыдущему примеру, чтобы проиллюстрировать эту разницу.

### Логика внутри обработчиков событий не является реактивной {#logic-inside-event-handlers-is-not-reactive}

Взгляните на эту строку кода. Должна ли эта логика быть реактивной или нет?

```js
// ...
sendMessage(message);
// ...
```

С точки зрения пользователя, **изменение `message` не означает, что он хочет отправить сообщение.** Это означает только то, что пользователь набирает текст. Другими словами, логика, отправляющая сообщение, не должна быть реактивной. Она не должна запускаться снова только потому, что реактивное значение изменилось. Вот почему она должна находиться в обработчике событий:

```js hl_lines="2"
function handleSendClick() {
    sendMessage(message);
}
```

Обработчики событий не являются реактивными, поэтому `sendMessage(message)` будет выполняться только тогда, когда пользователь нажмет кнопку Send.

### Логика внутри Effects является реактивной {#logic-inside-effects-is-reactive}

Теперь давайте вернемся к этим строкам:

```js
// ...
const connection = createConnection(serverUrl, roomId);
connection.connect();
// ...
```

С точки зрения пользователя, **изменение `roomId` _означает_, что он хочет подключиться к другой комнате.** Другими словами, логика подключения к комнате должна быть реактивной. Вы _хотите_, чтобы эти строки кода "шли в ногу" с реактивным значением, и запускались снова, если это значение изменилось. Вот почему это должно быть в Эффекте:

```js hl_lines="2-3"
useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
        connection.disconnect();
    };
}, [roomId]);
```

Эффекты являются реактивными, поэтому `createConnection(serverUrl, roomId)` и `connection.connect()` будут выполняться для каждого отдельного значения `roomId`. Ваш эффект сохраняет соединение чата синхронизированным с текущей выбранной комнатой.

## Извлечение нереактивной логики из эффектов {#extracting-non-reactive-logic-out-of-effects}

Ситуация усложняется, когда вы хотите смешать реактивную логику с нереактивной.

Например, представьте, что вы хотите показать уведомление, когда пользователь подключается к чату. Вы считываете текущую тему (темную или светлую) из пропса, чтобы показать уведомление нужного цвета:

```js hl_lines="1 7-9"
function ChatRoom({ roomId, theme }) {
    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.on('connected', () => {
            showNotification('Connected!', theme);
        });
        connection.connect();
        // ...
    });
}
```

Однако `theme` является реактивным значением (оно может меняться в результате перерисовки), и [каждое реактивное значение, считываемое Эффектом, должно быть объявлено его зависимостью](lifecycle-of-reactive-effects.md) Теперь вы должны указать `theme` как зависимость вашего Эффекта:

```js hl_lines="8 14"
function ChatRoom({ roomId, theme }) {
    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.on('connected', () => {
            showNotification('Connected!', theme);
        });
        connection.connect();
        return () => {
            connection.disconnect();
        };
    }, [roomId, theme]); // ✅ All dependencies declared
    // ...
}
```

Поиграйте с этим примером и посмотрите, сможете ли вы найти проблему в этом пользовательском опыте:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection, sendMessage } from './chat.js';
    import { showNotification } from './notifications.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId, theme }) {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.on('connected', () => {
    			showNotification('Connected!', theme);
    		});
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId, theme]);

    	return <h1>Welcome to the {roomId} room!</h1>;
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Use dark theme
    			</label>
    			<hr />
    			<ChatRoom
    				roomId={roomId}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	let connectedCallback;
    	let timeout;
    	return {
    		connect() {
    			timeout = setTimeout(() => {
    				if (connectedCallback) {
    					connectedCallback();
    				}
    			}, 100);
    		},
    		on(event, callback) {
    			if (connectedCallback) {
    				throw Error(
    					'Cannot add the handler twice.'
    				);
    			}
    			if (event !== 'connected') {
    				throw Error(
    					'Only "connected" event is supported.'
    				);
    			}
    			connectedCallback = callback;
    		},
    		disconnect() {
    			clearTimeout(timeout);
    		},
    	};
    }
    ```

=== "notifications.js"

    ```js
    import Toastify from 'toastify-js';
    import 'toastify-js/src/toastify.css';

    export function showNotification(message, theme) {
    	Toastify({
    		text: message,
    		duration: 2000,
    		gravity: 'top',
    		position: 'right',
    		style: {
    			background:
    				theme === 'dark' ? 'black' : 'white',
    			color: theme === 'dark' ? 'white' : 'black',
    		},
    	}).showToast();
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5dn4kh?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="broken-snowflake-5dn4kh" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

При изменении `roomId` чат переподключается, как и следовало ожидать. Но поскольку `theme` также является зависимостью, чат _также_ переподключается каждый раз, когда вы переключаетесь между темной и светлой темой. Это не здорово!

Другими словами, вы _не_ хотите, чтобы эта строка была реактивной, даже если она находится внутри Effect (который является реактивным):

```js
// ...
showNotification('Connected!', theme);
// ...
```

Вам нужен способ отделить эту нереактивную логику от реактивного Эффекта вокруг нее.

### Объявление события эффекта {#declaring-an-effect-event}

!!!warning "В разработке"

    Этот раздел описывает **экспериментальный API, который еще не был выпущен** в стабильной версии React.

Используйте специальный хук под названием [`useEffectEvent`](../reference/react/useEffectEvent.md), чтобы извлечь эту нереактивную логику из вашего Эффекта:

```js hl_lines="1 4-6"
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId, theme }) {
    const onConnected = useEffectEvent(() => {
        showNotification('Connected!', theme);
    });
    // ...
}
```

Здесь `onConnected` называется _событием эффекта._ Это часть логики вашего эффекта, но она ведет себя гораздо больше как обработчик событий. Логика внутри него не является реактивной, и он всегда "видит" последние значения ваших пропсов и состояния.

Теперь вы можете вызывать событие Эффекта `onConnected` изнутри вашего Эффекта:

```js hl_lines="2-4 12 16"
function ChatRoom({ roomId, theme }) {
    const onConnected = useEffectEvent(() => {
        showNotification('Connected!', theme);
    });

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.on('connected', () => {
            onConnected();
        });
        connection.connect();
        return () => connection.disconnect();
    }, [roomId]); // ✅ All dependencies declared
    // ...
}
```

Это решает проблему. Обратите внимание, что вам пришлось _удалить_ `onConnected` из списка зависимостей вашего Эффекта. **События эффектов не являются реактивными и должны быть исключены из зависимостей.**.

Проверьте, что новое поведение работает так, как вы ожидаете:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { useEffectEvent } from 'react';
    import { createConnection, sendMessage } from './chat.js';
    import { showNotification } from './notifications.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId, theme }) {
    	const onConnected = useEffectEvent(() => {
    		showNotification('Connected!', theme);
    	});

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.on('connected', () => {
    			onConnected();
    		});
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return <h1>Welcome to the {roomId} room!</h1>;
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Use dark theme
    			</label>
    			<hr />
    			<ChatRoom
    				roomId={roomId}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	let connectedCallback;
    	let timeout;
    	return {
    		connect() {
    			timeout = setTimeout(() => {
    				if (connectedCallback) {
    					connectedCallback();
    				}
    			}, 100);
    		},
    		on(event, callback) {
    			if (connectedCallback) {
    				throw Error(
    					'Cannot add the handler twice.'
    				);
    			}
    			if (event !== 'connected') {
    				throw Error(
    					'Only "connected" event is supported.'
    				);
    			}
    			connectedCallback = callback;
    		},
    		disconnect() {
    			clearTimeout(timeout);
    		},
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/7szywk?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="late-cherry-7szywk" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

События эффектов можно считать очень похожими на обработчики событий. Основное различие заключается в том, что обработчики событий запускаются в ответ на действия пользователя, в то время как События эффектов запускаются вами из Эффектов. События эффектов позволяют вам "разорвать цепь" между реактивностью эффектов и кодом, который не должен быть реактивным.

### Чтение последних пропсов и состояния с помощью событий эффектов {#reading-latest-props-and-state-with-effect-events}

!!!warning "В разработке"

    Этот раздел описывает **экспериментальный API, который еще не был выпущен** в стабильной версии React.

События Effect Events позволяют исправить многие паттерны, где может возникнуть соблазн подавить линтер зависимостей.

Например, у вас есть эффект для регистрации посещений страницы:

```js
function Page() {
    useEffect(() => {
        logVisit();
    }, []);
    // ...
}
```

Позже вы добавляете несколько маршрутов на свой сайт. Теперь ваш компонент `Page` получает пропс `url` с текущим путем. Вы хотите передать `url` как часть вашего вызова `logVisit`, но линтер зависимостей жалуется:

```js hl_lines="1 3"
function Page({ url }) {
    useEffect(() => {
        logVisit(url);
    }, []); // 🔴 React Hook useEffect has a missing dependency: 'url'
    // ...
}
```

Подумайте, что вы хотите сделать с помощью кода. Вы _хотите_ регистрировать отдельные посещения для разных URL, поскольку каждый URL представляет собой отдельную страницу. Другими словами, этот вызов `logVisit` _должен_ быть реактивным по отношению к `url`. Вот почему в данном случае имеет смысл следовать указателю зависимостей и добавить `url` в качестве зависимости:

```js hl_lines="4"
function Page({ url }) {
    useEffect(() => {
        logVisit(url);
    }, [url]); // ✅ All dependencies declared
    // ...
}
```

Теперь предположим, что вы хотите включать количество товаров в корзине вместе с каждым посещением страницы:

```js hl_lines="2-3 6"
function Page({ url }) {
    const { items } = useContext(ShoppingCartContext);
    const numberOfItems = items.length;

    useEffect(() => {
        logVisit(url, numberOfItems);
    }, [url]); // 🔴 React Hook useEffect has a missing dependency: 'numberOfItems'
    // ...
}
```

Вы использовали `numberOfItems` внутри Effect, поэтому линтер просит вас добавить его в качестве зависимости. Однако, вы _не_ хотите, чтобы вызов `logVisit` был реактивным по отношению к `numberOfItems`. Если пользователь положил что-то в корзину, и `numberOfItems` изменилось, это _не означает_, что пользователь снова посетил страницу. Другими словами, _посещение страницы_ - это, в некотором смысле, "событие". Оно происходит в определенный момент времени.

Разделите код на две части:

```js hl_lines="5-7 10"
function Page({ url }) {
    const { items } = useContext(ShoppingCartContext);
    const numberOfItems = items.length;

    const onVisit = useEffectEvent((visitedUrl) => {
        logVisit(visitedUrl, numberOfItems);
    });

    useEffect(() => {
        onVisit(url);
    }, [url]); // ✅ All dependencies declared
    // ...
}
```

Здесь `onVisit` - это событие эффекта. Код внутри него не является реактивным. Вот почему вы можете использовать `numberOfItems` (или любое другое реактивное значение!), не беспокоясь о том, что оно заставит окружающий код повторно выполняться при изменениях.

С другой стороны, сам Эффект остается реактивным. Код внутри Эффекта использует пропс `url`, поэтому Эффект будет запускаться заново после каждого повторного рендеринга с другим `url`. Это, в свою очередь, вызовет событие эффекта `onVisit`.

В результате вы будете вызывать `logVisit` для каждого изменения `url`, и всегда считывать последнее `numberOfItems`. Однако, если `numberOfItems` изменится сам по себе, это не приведет к повторному выполнению кода.

!!!note ""

    Вам может быть интересно, можно ли вызвать функцию `onVisit()` без аргументов и прочитать `url` внутри нее:

    ```js hl_lines="2 6"
    const onVisit = useEffectEvent(() => {
    	logVisit(url, numberOfItems);
    });

    useEffect(() => {
    	onVisit();
    }, [url]);
    ```

    Это сработает, но лучше передавать `url` в событие Effect Event явно. **Передавая `url` в качестве аргумента в событие Effect Event, вы говорите, что посещение страницы с другим `url` представляет собой отдельное "событие" с точки зрения пользователя.** `visitedUrl` является _частью_ произошедшего "события":

    ```js hl_lines="1-2 6"
    const onVisit = useEffectEvent((visitedUrl) => {
    	logVisit(visitedUrl, numberOfItems);
    });

    useEffect(() => {
    	onVisit(url);
    }, [url]);
    ```

    Поскольку событие вашего эффекта явно "запрашивает" `visitedUrl`, теперь вы не сможете случайно удалить `url` из зависимостей эффекта. Если вы удалите зависимость `url` (в результате чего посещение разных страниц будет считаться за одно), линтер предупредит вас об этом. Вы хотите, чтобы `onVisit` был реактивным по отношению к `url`, поэтому вместо того, чтобы читать `url` внутри (где он не будет реактивным), вы передаете его _из_ вашего Эффекта.

    Это становится особенно важным, если внутри Эффекта есть какая-то асинхронная логика:

    ```js hl_lines="6 8"
    const onVisit = useEffectEvent((visitedUrl) => {
    	logVisit(visitedUrl, numberOfItems);
    });

    useEffect(() => {
    	setTimeout(() => {
    		onVisit(url);
    	}, 5000); // Delay logging visits
    }, [url]);
    ```

    Здесь `url` внутри `onVisit` соответствует _последнему_ `url` (который мог уже измениться), но `visitedUrl` соответствует `url`, который первоначально вызвал запуск этого Effect (и этого вызова `onVisit`).

!!!note "Можно ли вместо этого подавить линтер зависимостей?"

    В существующих кодовых базах иногда можно встретить подавление правила lint следующим образом:

    ```js hl_lines="7-9"
    function Page({ url }) {
    	const { items } = useContext(ShoppingCartContext);
    	const numberOfItems = items.length;

    	useEffect(() => {
    		logVisit(url, numberOfItems);
    		// 🔴 Avoid suppressing the linter like this:
    		// eslint-disable-next-line react-hooks/exhaustive-deps
    	}, [url]);
    	// ...
    }
    ```

    После того, как `useEffectEvent` станет стабильной частью React, мы рекомендуем **никогда не подавлять линтер**.

    Первый недостаток подавления правила заключается в том, что React больше не будет предупреждать вас, когда ваш Эффект должен "отреагировать" на новую реактивную зависимость, которую вы добавили в свой код. В предыдущем примере вы добавили `url` к зависимостям _потому что_ React напомнил вам сделать это. Если вы отключите линтер, вы больше не будете получать такие напоминания для любых будущих правок этого Эффекта. Это приводит к ошибкам.

    Вот пример запутанной ошибки, вызванной подавлением линтера. В этом примере функция `handleMove` должна прочитать текущее значение переменной состояния `canMove`, чтобы решить, должна ли точка следовать за курсором. Однако, `canMove` всегда `true` внутри `handleMove`.

    Вы можете понять, почему?

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';

    	export default function App() {
    		const [position, setPosition] = useState({
    			x: 0,
    			y: 0,
    		});
    		const [canMove, setCanMove] = useState(true);

    		function handleMove(e) {
    			if (canMove) {
    				setPosition({ x: e.clientX, y: e.clientY });
    			}
    		}

    		useEffect(() => {
    			window.addEventListener('pointermove', handleMove);
    			return () =>
    				window.removeEventListener(
    					'pointermove',
    					handleMove
    				);
    			// eslint-disable-next-line react-hooks/exhaustive-deps
    		}, []);

    		return (
    			<>
    				<label>
    					<input
    						type="checkbox"
    						checked={canMove}
    						onChange={(e) =>
    							setCanMove(e.target.checked)
    						}
    					/>
    					The dot is allowed to move
    				</label>
    				<hr />
    				<div
    					style={{
    						position: 'absolute',
    						backgroundColor: 'pink',
    						borderRadius: '50%',
    						opacity: 0.6,
    						transform: `translate(${position.x}px, ${position.y}px)`,
    						pointerEvents: 'none',
    						left: -20,
    						top: -20,
    						width: 40,
    						height: 40,
    					}}
    				/>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/mttx99?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Проблема с этим кодом заключается в подавлении линтера зависимостей. Если вы уберете подавление, то увидите, что этот Effect должен зависеть от функции `handleMove`. Это имеет смысл: `handleMove` объявлена внутри тела компонента, что делает ее реактивным значением. Каждое реактивное значение должно быть указано как зависимость, иначе оно может устареть со временем!

    Автор оригинального кода "соврал" React, сказав, что Effect не зависит (`[]`) ни от каких реактивных значений. Именно поэтому React не пересинхронизировал Effect после изменения `canMove` (и `handleMove` вместе с ним). Поскольку React не пересинхронизировал Effect, `handleMove`, прикрепленная в качестве слушателя, является функцией `handleMove`, созданной во время первоначального рендеринга. Во время первоначального рендера `canMove` было `true`, поэтому `handleMove` из первоначального рендера всегда будет видеть это значение.

    **Если вы никогда не подавляете линтер, вы никогда не увидите проблем с устаревшими значениями.**

    С `useEffectEvent` нет необходимости "врать" линтеру, и код работает так, как вы ожидаете:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { useEffectEvent } from 'react';

    	export default function App() {
    		const [position, setPosition] = useState({
    			x: 0,
    			y: 0,
    		});
    		const [canMove, setCanMove] = useState(true);

    		const onMove = useEffectEvent((e) => {
    			if (canMove) {
    				setPosition({ x: e.clientX, y: e.clientY });
    			}
    		});

    		useEffect(() => {
    			window.addEventListener('pointermove', onMove);
    			return () =>
    				window.removeEventListener(
    					'pointermove',
    					onMove
    				);
    		}, []);

    		return (
    			<>
    				<label>
    					<input
    						type="checkbox"
    						checked={canMove}
    						onChange={(e) =>
    							setCanMove(e.target.checked)
    						}
    					/>
    					The dot is allowed to move
    				</label>
    				<hr />
    				<div
    					style={{
    						position: 'absolute',
    						backgroundColor: 'pink',
    						borderRadius: '50%',
    						opacity: 0.6,
    						transform: `translate(${position.x}px, ${position.y}px)`,
    						pointerEvents: 'none',
    						left: -20,
    						top: -20,
    						width: 40,
    						height: 40,
    					}}
    				/>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/3xd8d3?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="condescending-worker-3xd8d3" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Это не означает, что `useEffectEvent` - это _всегда_ правильное решение. Вы должны применять его только к тем строкам кода, которые вы не хотите, чтобы были реактивными. В приведенной выше песочнице вы не хотели, чтобы код Эффекта был реактивным в отношении `canMove`. Вот почему имело смысл извлечь событие эффекта.

    Читайте [Удаление зависимостей эффектов](removing-effect-dependencies.md) о других правильных альтернативах подавления линтера.

### Ограничения событий эффектов {#limitations-of-effect-events}

!!!warning "В разработке"

    Этот раздел описывает **экспериментальный API, который еще не был выпущен** в стабильной версии React.

События эффектов очень ограничены в том, как вы можете их использовать:

-   **Вызывать их только изнутри Эффектов.**
-   **Никогда не передавайте их другим компонентам или хукам.**

Например, не объявляйте и не передавайте событие эффекта следующим образом:

```js hl_lines="4-6 8"
function Timer() {
    const [count, setCount] = useState(0);

    const onTick = useEffectEvent(() => {
        setCount(count + 1);
    });

    useTimer(onTick, 1000); // 🔴 Avoid: Passing Effect Events

    return <h1>{count}</h1>;
}

function useTimer(callback, delay) {
    useEffect(() => {
        const id = setInterval(() => {
            callback();
        }, delay);
        return () => {
            clearInterval(id);
        };
    }, [delay, callback]); // Need to specify "callback" in dependencies
}
```

Вместо этого всегда объявляйте события эффектов непосредственно рядом с эффектами, которые их используют:

```js hl_lines="10-12 16 21"
function Timer() {
    const [count, setCount] = useState(0);
    useTimer(() => {
        setCount(count + 1);
    }, 1000);
    return <h1>{count}</h1>;
}

function useTimer(callback, delay) {
    const onTick = useEffectEvent(() => {
        callback();
    });

    useEffect(() => {
        const id = setInterval(() => {
            onTick(); // ✅ Good: Only called locally inside an Effect
        }, delay);
        return () => {
            clearInterval(id);
        };
    }, [delay]); // No need to specify "onTick" (an Effect Event) as a dependency
}
```

События эффектов - это нереактивные "куски" кода вашего эффекта. Они должны находиться рядом с использующим их Эффектом.

!!!note "Итого"

    -   Обработчики событий запускаются в ответ на определенные взаимодействия.
    -   Эффекты запускаются всякий раз, когда требуется синхронизация.
    -   Логика внутри обработчиков событий не является реактивной.
    -   Логика внутри эффектов реактивна.
    -   Вы можете перенести нереактивную логику из Эффектов в События Эффектов.
    -   Вызывайте события эффектов только из самих эффектов.
    -   Не передавайте события эффектов другим компонентам или хукам.

## Задачи {#challenges}

### 1. Исправление переменной, которая не обновляется {#fix-a-variable-that-doesnt-update}

Этот компонент `Timer` хранит переменную состояния `count`, которая увеличивается каждую секунду. Значение, на которое она увеличивается, хранится в переменной состояния `increment`. Вы можете управлять переменной `increment` с помощью кнопок плюс и минус.

Однако, сколько бы раз вы ни нажали на кнопку с плюсом, счетчик все равно увеличивается на единицу каждую секунду. Что не так с этим кодом? Почему `increment` всегда равен `1` в коде Effect'а? Найдите ошибку и исправьте ее.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function Timer() {
    	const [count, setCount] = useState(0);
    	const [increment, setIncrement] = useState(1);

    	useEffect(() => {
    		const id = setInterval(() => {
    			setCount((c) => c + increment);
    		}, 1000);
    		return () => {
    			clearInterval(id);
    		};
    		// eslint-disable-next-line react-hooks/exhaustive-deps
    	}, []);

    	return (
    		<>
    			<h1>
    				Counter: {count}
    				<button onClick={() => setCount(0)}>
    					Reset
    				</button>
    			</h1>
    			<hr />
    			<p>
    				Every second, increment by:
    				<button
    					disabled={increment === 0}
    					onClick={() => {
    						setIncrement((i) => i - 1);
    					}}
    				>
    					–
    				</button>
    				<b>{increment}</b>
    				<button
    					onClick={() => {
    						setIncrement((i) => i + 1);
    					}}
    				>
    					+
    				</button>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/8y52w4?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Чтобы исправить этот код, достаточно следовать правилам.

???success "Показать решение"

    Как обычно, когда вы ищете ошибки в Эффектах, начните с поиска подавлений линтера.

    Если вы удалите комментарий о подавлении, React скажет вам, что код этого Эффекта зависит от `increment`, но вы "солгали" React, утверждая, что этот Эффект не зависит ни от каких реактивных значений (`[]`). Добавьте `increment` в массив зависимостей:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';

    	export default function Timer() {
    		const [count, setCount] = useState(0);
    		const [increment, setIncrement] = useState(1);

    		useEffect(() => {
    			const id = setInterval(() => {
    				setCount((c) => c + increment);
    			}, 1000);
    			return () => {
    				clearInterval(id);
    			};
    		}, [increment]);

    		return (
    			<>
    				<h1>
    					Counter: {count}
    					<button onClick={() => setCount(0)}>
    						Reset
    					</button>
    				</h1>
    				<hr />
    				<p>
    					Every second, increment by:
    					<button
    						disabled={increment === 0}
    						onClick={() => {
    							setIncrement((i) => i - 1);
    						}}
    					>
    						–
    					</button>
    					<b>{increment}</b>
    					<button
    						onClick={() => {
    							setIncrement((i) => i + 1);
    						}}
    					>
    						+
    					</button>
    				</p>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/cc3ckc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Теперь, когда `increment` изменится, React пересинхронизирует ваш Effect, что перезапустит интервал.

### 2. Исправьте зависший счетчик {#fix-a-freezing-counter}

Этот компонент `Timer` хранит переменную состояния `count`, которая увеличивается каждую секунду. Значение, на которое она увеличивается, хранится в переменной состояния `increment`, которой вы можете управлять с помощью кнопок плюс и минус. Например, попробуйте нажать кнопку плюс девять раз и заметите, что теперь `count` увеличивается каждую секунду на десять, а не на один.

Есть небольшая проблема с этим пользовательским интерфейсом. Вы можете заметить, что если вы продолжаете нажимать на кнопки плюс или минус быстрее, чем один раз в секунду, то сам таймер как бы приостанавливается. Он возобновляется только после того, как пройдет секунда с момента последнего нажатия любой из кнопок. Выясните, почему это происходит, и устраните проблему, чтобы таймер тикал _каждую_ секунду без перерывов.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { useEffectEvent } from 'react';

    export default function Timer() {
    	const [count, setCount] = useState(0);
    	const [increment, setIncrement] = useState(1);

    	useEffect(() => {
    		const id = setInterval(() => {
    			setCount((c) => c + increment);
    		}, 1000);
    		return () => {
    			clearInterval(id);
    		};
    	}, [increment]);

    	return (
    		<>
    			<h1>
    				Counter: {count}
    				<button onClick={() => setCount(0)}>
    					Reset
    				</button>
    			</h1>
    			<hr />
    			<p>
    				Every second, increment by:
    				<button
    					disabled={increment === 0}
    					onClick={() => {
    						setIncrement((i) => i - 1);
    					}}
    				>
    					–
    				</button>
    				<b>{increment}</b>
    				<button
    					onClick={() => {
    						setIncrement((i) => i + 1);
    					}}
    				>
    					+
    				</button>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xtvpn9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="objective-ramanujan-xtvpn9" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Похоже, что Effect, который устанавливает таймер, "реагирует" на значение `increment`. Действительно ли строка, которая использует текущее значение `increment` для вызова `setCount` должна быть реактивной?

???success "Показать решение"

    Проблема в том, что код внутри Эффекта использует переменную состояния `increment`. Поскольку она зависит от вашего Эффекта, каждое изменение `increment` заставляет Эффект пересинхронизироваться, что приводит к очистке интервала. Если вы будете очищать интервал каждый раз, прежде чем он успеет сработать, то будет казаться, что таймер остановился.

    Чтобы решить эту проблему, извлеките из Эффекта событие Эффекта `onTick`:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { useEffectEvent } from 'react';

    	export default function Timer() {
    		const [count, setCount] = useState(0);
    		const [increment, setIncrement] = useState(1);

    		const onTick = useEffectEvent(() => {
    			setCount((c) => c + increment);
    		});

    		useEffect(() => {
    			const id = setInterval(() => {
    				onTick();
    			}, 1000);
    			return () => {
    				clearInterval(id);
    			};
    		}, []);

    		return (
    			<>
    				<h1>
    					Counter: {count}
    					<button onClick={() => setCount(0)}>
    						Reset
    					</button>
    				</h1>
    				<hr />
    				<p>
    					Every second, increment by:
    					<button
    						disabled={increment === 0}
    						onClick={() => {
    							setIncrement((i) => i - 1);
    						}}
    					>
    						–
    					</button>
    					<b>{increment}</b>
    					<button
    						onClick={() => {
    							setIncrement((i) => i + 1);
    						}}
    					>
    						+
    					</button>
    				</p>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/3zl5mk?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="sharp-colden-3zl5mk" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Поскольку `onTick` является событием Эффекта, код внутри него не является реактивным. Изменение `increment` не вызывает никаких Эффектов.

### 3. Исправление нерегулируемой задержки {#fix-a-non-adjustable-delay}

В этом примере вы можете настроить интервальную задержку. Она хранится в переменной состояния `delay`, которая обновляется двумя кнопками. Однако, даже если вы будете нажимать кнопку "плюс 100 мс", пока `delay` не станет равной 1000 миллисекунд (то есть секунде), вы заметите, что таймер все равно увеличивается очень быстро (каждые 100 мс). Как будто ваши изменения `delay` игнорируются. Найдите и исправьте ошибку.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { useEffectEvent } from 'react';

    export default function Timer() {
    	const [count, setCount] = useState(0);
    	const [increment, setIncrement] = useState(1);
    	const [delay, setDelay] = useState(100);

    	const onTick = useEffectEvent(() => {
    		setCount((c) => c + increment);
    	});

    	const onMount = useEffectEvent(() => {
    		return setInterval(() => {
    			onTick();
    		}, delay);
    	});

    	useEffect(() => {
    		const id = onMount();
    		return () => {
    			clearInterval(id);
    		};
    	}, []);

    	return (
    		<>
    			<h1>
    				Counter: {count}
    				<button onClick={() => setCount(0)}>
    					Reset
    				</button>
    			</h1>
    			<hr />
    			<p>
    				Increment by:
    				<button
    					disabled={increment === 0}
    					onClick={() => {
    						setIncrement((i) => i - 1);
    					}}
    				>
    					–
    				</button>
    				<b>{increment}</b>
    				<button
    					onClick={() => {
    						setIncrement((i) => i + 1);
    					}}
    				>
    					+
    				</button>
    			</p>
    			<p>
    				Increment delay:
    				<button
    					disabled={delay === 100}
    					onClick={() => {
    						setDelay((d) => d - 100);
    					}}
    				>
    					–100 ms
    				</button>
    				<b>{delay} ms</b>
    				<button
    					onClick={() => {
    						setDelay((d) => d + 100);
    					}}
    				>
    					+100 ms
    				</button>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/chx4tj?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="crazy-booth-chx4tj" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Код внутри Effect Events не является реактивным. Есть ли случаи, в которых вы _хотели бы_, чтобы вызов `setInterval` выполнялся повторно?

???success "Показать решение"

    Проблема приведенного выше примера заключается в том, что он извлек событие Effect Event под названием `onMount`, не задумываясь о том, что на самом деле должен делать код. Вы должны извлекать события Effect Events только по определенной причине: когда вы хотите сделать часть вашего кода нереактивной. Однако вызов `setInterval` _должен_ быть реактивным по отношению к переменной состояния `delay`. Если `delay` меняется, вы хотите установить интервал с нуля! Чтобы исправить этот код, перенесите весь реактивный код обратно в Effect:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { useEffectEvent } from 'react';

    	export default function Timer() {
    		const [count, setCount] = useState(0);
    		const [increment, setIncrement] = useState(1);
    		const [delay, setDelay] = useState(100);

    		const onTick = useEffectEvent(() => {
    			setCount((c) => c + increment);
    		});

    		useEffect(() => {
    			const id = setInterval(() => {
    				onTick();
    			}, delay);
    			return () => {
    				clearInterval(id);
    			};
    		}, [delay]);

    		return (
    			<>
    				<h1>
    					Counter: {count}
    					<button onClick={() => setCount(0)}>
    						Reset
    					</button>
    				</h1>
    				<hr />
    				<p>
    					Increment by:
    					<button
    						disabled={increment === 0}
    						onClick={() => {
    							setIncrement((i) => i - 1);
    						}}
    					>
    						–
    					</button>
    					<b>{increment}</b>
    					<button
    						onClick={() => {
    							setIncrement((i) => i + 1);
    						}}
    					>
    						+
    					</button>
    				</p>
    				<p>
    					Increment delay:
    					<button
    						disabled={delay === 100}
    						onClick={() => {
    							setDelay((d) => d - 100);
    						}}
    					>
    						–100 ms
    					</button>
    					<b>{delay} ms</b>
    					<button
    						onClick={() => {
    							setDelay((d) => d + 100);
    						}}
    					>
    						+100 ms
    					</button>
    				</p>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/p4swy2?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="jovial-poitras-p4swy2" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    В целом, вы должны с подозрением относиться к функциям типа `onMount`, которые сосредоточены на _времени_, а не на _цели_ части кода. Поначалу это может показаться "более описательным", но это затуманивает ваш замысел. Как правило, события эффектов должны соответствовать чему-то, что происходит с точки зрения _пользователя_. Например, `onMessage`, `onTick`, `onVisit` или `onConnected` - хорошие названия событий эффектов. Код внутри них, скорее всего, не должен быть реактивным. С другой стороны, `onMount`, `onUpdate`, `onUnmount` или `onAfterRender` настолько общие, что в них легко случайно поместить код, который _должен_ быть реактивным. Вот почему вы должны называть свои события Effect Events в соответствии с тем, _что, по мнению пользователя, произошло,_ а не с тем, когда был запущен какой-то код.

### 4. Исправление отложенного уведомления {#fix-a-delayed-notification}

Когда вы присоединяетесь к чату, этот компонент показывает уведомление. Однако он не показывает уведомление немедленно. Вместо этого уведомление искусственно задерживается на две секунды, чтобы у пользователя была возможность осмотреться в пользовательском интерфейсе.

Это почти работает, но есть ошибка. Попробуйте быстро изменить выпадающий список с "общие" на "путешествия", а затем на "музыка". Если вы сделаете это достаточно быстро, вы увидите два уведомления (как и ожидалось!), но в обоих будет написано "Добро пожаловать в музыку".

Исправьте это так, чтобы при быстром переключении с "общего" на "путешествия" и затем на "музыку" вы видели два уведомления, первое из которых было бы "Добро пожаловать в путешествие", а второе - "Добро пожаловать в музыку". (Для дополнительной сложности, если вы _уже_ сделали так, чтобы уведомления показывали правильные комнаты, измените код так, чтобы отображалось только последнее уведомление).

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { useEffectEvent } from 'react';
    import { createConnection, sendMessage } from './chat.js';
    import { showNotification } from './notifications.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId, theme }) {
    	const onConnected = useEffectEvent(() => {
    		showNotification('Welcome to ' + roomId, theme);
    	});

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.on('connected', () => {
    			setTimeout(() => {
    				onConnected();
    			}, 2000);
    		});
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return <h1>Welcome to the {roomId} room!</h1>;
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Use dark theme
    			</label>
    			<hr />
    			<ChatRoom
    				roomId={roomId}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	let connectedCallback;
    	let timeout;
    	return {
    		connect() {
    			timeout = setTimeout(() => {
    				if (connectedCallback) {
    					connectedCallback();
    				}
    			}, 100);
    		},
    		on(event, callback) {
    			if (connectedCallback) {
    				throw Error(
    					'Cannot add the handler twice.'
    				);
    			}
    			if (event !== 'connected') {
    				throw Error(
    					'Only "connected" event is supported.'
    				);
    			}
    			connectedCallback = callback;
    		},
    		disconnect() {
    			clearTimeout(timeout);
    		},
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/9mgdl8?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="blissful-monad-9mgdl8" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Ваш Эффект знает, к какой комнате он подключился. Есть ли какая-нибудь информация, которую вы могли бы передать в событие вашего Эффекта?

???success "Показать решение"

    Внутри вашего события Effect Event, `roomId` - это значение _в момент вызова Effect Event._.

    Ваше Событие Эффекта вызывается с двухсекундной задержкой. Если вы быстро переключаетесь из комнаты для путешествий в музыкальную комнату, то к тому времени, когда появится уведомление комнаты для путешествий, `roomId` уже будет `"music"`. Вот почему оба уведомления говорят "Добро пожаловать в музыкальную комнату".

    Чтобы решить эту проблему, вместо чтения _последнего_ `roomId` внутри события эффекта, сделайте его параметром события эффекта, как `connectedRoomId` ниже. Затем передавайте `roomId` из вашего Эффекта, вызывая `onConnected(roomId)`:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { useEffectEvent } from 'react';
    	import { createConnection, sendMessage } from './chat.js';
    	import { showNotification } from './notifications.js';

    	const serverUrl = 'https://localhost:1234';

    	function ChatRoom({ roomId, theme }) {
    		const onConnected = useEffectEvent(
    			(connectedRoomId) => {
    				showNotification(
    					'Welcome to ' + connectedRoomId,
    					theme
    				);
    			}
    		);

    		useEffect(() => {
    			const connection = createConnection(
    				serverUrl,
    				roomId
    			);
    			connection.on('connected', () => {
    				setTimeout(() => {
    					onConnected(roomId);
    				}, 2000);
    			});
    			connection.connect();
    			return () => connection.disconnect();
    		}, [roomId]);

    		return <h1>Welcome to the {roomId} room!</h1>;
    	}

    	export default function App() {
    		const [roomId, setRoomId] = useState('general');
    		const [isDark, setIsDark] = useState(false);
    		return (
    			<>
    				<label>
    					Choose the chat room:{' '}
    					<select
    						value={roomId}
    						onChange={(e) =>
    							setRoomId(e.target.value)
    						}
    					>
    						<option value="general">general</option>
    						<option value="travel">travel</option>
    						<option value="music">music</option>
    					</select>
    				</label>
    				<label>
    					<input
    						type="checkbox"
    						checked={isDark}
    						onChange={(e) =>
    							setIsDark(e.target.checked)
    						}
    					/>
    					Use dark theme
    				</label>
    				<hr />
    				<ChatRoom
    					roomId={roomId}
    					theme={isDark ? 'dark' : 'light'}
    				/>
    			</>
    		);
    	}
    	```

    === "chat.js"

    	```js
    	export function createConnection(serverUrl, roomId) {
    		// A real implementation would actually connect to the server
    		let connectedCallback;
    		let timeout;
    		return {
    			connect() {
    				timeout = setTimeout(() => {
    					if (connectedCallback) {
    						connectedCallback();
    					}
    				}, 100);
    			},
    			on(event, callback) {
    				if (connectedCallback) {
    					throw Error(
    						'Cannot add the handler twice.'
    					);
    				}
    				if (event !== 'connected') {
    					throw Error(
    						'Only "connected" event is supported.'
    					);
    				}
    				connectedCallback = callback;
    			},
    			disconnect() {
    				clearTimeout(timeout);
    			},
    		};
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/2ydfk9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="elastic-vaughan-2ydfk9" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Эффект, у которого `roomId` был установлен на `"travel"` (поэтому он подключился к комнате `"travel"`), покажет уведомление для `"travel"`. Эффект, у которого `roomId` установлен в `"music"` (поэтому он подключился к комнате `"music"`), покажет уведомление для `"music"`. Другими словами, `connectedRoomId` приходит от вашего Эффекта (который является реактивным), в то время как `theme` всегда использует последнее значение.

    Чтобы решить дополнительную проблему, сохраните идентификатор таймаута уведомления и очистите его в функции очистки вашего Эффекта:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { useEffectEvent } from 'react';
    	import { createConnection, sendMessage } from './chat.js';
    	import { showNotification } from './notifications.js';

    	const serverUrl = 'https://localhost:1234';

    	function ChatRoom({ roomId, theme }) {
    		const onConnected = useEffectEvent(
    			(connectedRoomId) => {
    				showNotification(
    					'Welcome to ' + connectedRoomId,
    					theme
    				);
    			}
    		);

    		useEffect(() => {
    			const connection = createConnection(
    				serverUrl,
    				roomId
    			);
    			let notificationTimeoutId;
    			connection.on('connected', () => {
    				notificationTimeoutId = setTimeout(() => {
    					onConnected(roomId);
    				}, 2000);
    			});
    			connection.connect();
    			return () => {
    				connection.disconnect();
    				if (notificationTimeoutId !== undefined) {
    					clearTimeout(notificationTimeoutId);
    				}
    			};
    		}, [roomId]);

    		return <h1>Welcome to the {roomId} room!</h1>;
    	}

    	export default function App() {
    		const [roomId, setRoomId] = useState('general');
    		const [isDark, setIsDark] = useState(false);
    		return (
    			<>
    				<label>
    					Choose the chat room:{' '}
    					<select
    						value={roomId}
    						onChange={(e) =>
    							setRoomId(e.target.value)
    						}
    					>
    						<option value="general">general</option>
    						<option value="travel">travel</option>
    						<option value="music">music</option>
    					</select>
    				</label>
    				<label>
    					<input
    						type="checkbox"
    						checked={isDark}
    						onChange={(e) =>
    							setIsDark(e.target.checked)
    						}
    					/>
    					Use dark theme
    				</label>
    				<hr />
    				<ChatRoom
    					roomId={roomId}
    					theme={isDark ? 'dark' : 'light'}
    				/>
    			</>
    		);
    	}
    	```

    === "chat.js"

    	```js
    	export function createConnection(serverUrl, roomId) {
    		// A real implementation would actually connect to the server
    		let connectedCallback;
    		let timeout;
    		return {
    			connect() {
    				timeout = setTimeout(() => {
    					if (connectedCallback) {
    						connectedCallback();
    					}
    				}, 100);
    			},
    			on(event, callback) {
    				if (connectedCallback) {
    					throw Error(
    						'Cannot add the handler twice.'
    					);
    				}
    				if (event !== 'connected') {
    					throw Error(
    						'Only "connected" event is supported.'
    					);
    				}
    				connectedCallback = callback;
    			},
    			disconnect() {
    				clearTimeout(timeout);
    			},
    		};
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/sw6wx7?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="quizzical-sun-sw6wx7" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Это гарантирует, что уже запланированные (но еще не отображенные) уведомления будут отменены, когда вы смените комнату.

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/separating-events-from-effects](https://react.dev/learn/separating-events-from-effects)</small>
