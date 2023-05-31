# StrictMode

Режим `<StrictMode>` позволяет находить распространенные ошибки в компонентах на ранних стадиях разработки.

<!-- 0001.part.md -->

```js
<StrictMode>
    <App />
</StrictMode>
```

## Описание

### `<StrictMode>`

Используйте `StrictMode` для включения дополнительных поведений разработки и предупреждений для внутреннего дерева компонентов:

<!-- 0003.part.md -->

```js
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <App />
    </StrictMode>
);
```

Строгий режим включает следующие модели поведения, доступные только для разработчиков:

-   Ваши компоненты будут перерендериваться дополнительно для поиска ошибок, вызванных нечистым рендерингом.
-   Ваши компоненты будут перезапускать эффекты дополнительно, чтобы найти ошибки, вызванные отсутствием очистки эффектов.
-   Ваши компоненты будут проверяться на использование устаревших API.

#### Пропсы

`StrictMode` не принимает никаких реквизитов.

#### Предупреждения

-   Не существует способа отказаться от строгого режима внутри дерева, обернутого в `<StrictMode>`. Это дает уверенность в том, что все компоненты внутри `<StrictMode>` проверены. Если две команды, работающие над продуктом, расходятся во мнении, считают ли они проверки ценными, им нужно либо прийти к консенсусу, либо переместить `<StrictMode>` вниз в дереве.

## Использование

### Включение строгого режима для всего приложения

Строгий режим включает дополнительные проверки, предназначенные только для разработчиков, для всего дерева компонентов внутри компонента `<StrictMode>`. Эти проверки помогут вам найти распространенные ошибки в ваших компонентах на ранних стадиях разработки.

Чтобы включить режим Strict Mode для всего приложения, оберните корневой компонент компонентом `<StrictMode>` при его рендеринге:

<!-- 0005.part.md -->

```js
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <App />
    </StrictMode>
);
```

<!-- 0006.part.md -->

Мы рекомендуем обернуть все ваше приложение в режим Strict Mode, особенно для вновь созданных приложений. Если вы используете фреймворк, который вызывает для вас `createRoot`, ознакомьтесь с его документацией, чтобы узнать, как включить строгий режим.

Хотя проверки в строгом режиме **работают только в разработке,** они помогают найти ошибки, которые уже существуют в вашем коде, но могут быть трудно воспроизводимы в производстве. Строгий режим позволяет исправлять ошибки до того, как пользователи сообщат о них.

!!!note ""

    Строгий режим включает следующие проверки в процессе разработки:

    -   Ваши компоненты будут перерендериваться дополнительно для поиска ошибок, вызванных нечистым рендерингом.
    -   Ваши компоненты будут перезапускать эффекты дополнительно, чтобы найти ошибки, вызванные отсутствием очистки эффектов.
    -   Ваши компоненты будут проверяться на использование устаревших API.

    **Все эти проверки предназначены только для разработки и не влияют на производственную сборку.**

### Включение строгого режима для части приложения

Вы также можете включить строгий режим для любой части вашего приложения:

<!-- 0007.part.md -->

```js
import { StrictMode } from 'react';

function App() {
    return (
        <>
            <Header />
            <StrictMode>
                <main>
                    <Sidebar />
                    <Content />
                </main>
            </StrictMode>
            <Footer />
        </>
    );
}
```

<!-- 0008.part.md -->

В этом примере проверки строгого режима не будут выполняться для компонентов `Header` и `Footer`. Однако они будут выполняться для `Sidebar` и `Content`, а также для всех компонентов внутри них, независимо от их глубины.

### Исправление ошибок, найденных при двойном рендеринге в разработке

[React предполагает, что каждый написанный вами компонент является чистой функцией](../learn/keeping-components-pure.md) Это означает, что написанные вами компоненты React должны всегда возвращать один и тот же JSX при одинаковых входных данных (props, state и context).

Компоненты, нарушающие это правило, ведут себя непредсказуемо и вызывают ошибки. Чтобы помочь вам найти случайно нечистый код, Strict Mode вызывает некоторые из ваших функций (только те, которые должны быть чистыми) **дважды в процессе разработки.** Это включает в себя:

-   тело функции вашего компонента (только логика верхнего уровня, поэтому сюда не входит код внутри обработчиков событий).
-   Функции, которые вы передаете в [`useState`](useState.md), [`set` functions](useState.md), [`useMemo`](useMemo.md), или [`useReducer`](useReducer.md).
-   Некоторые методы компонентов класса, такие как `constructor`, `render`, `shouldComponentUpdate` ([посмотреть весь список](https://reactjs.org/docs/strict-mode.html#detecting-unexpected-side-effects)).

Если функция чистая, то ее повторный запуск не изменит ее поведения, потому что чистая функция каждый раз выдает один и тот же результат. Однако, если функция нечистая (например, она мутирует полученные данные), ее повторный запуск будет заметен (вот что делает ее нечистой!) Это поможет вам обнаружить и исправить ошибку на ранней стадии.

**Здесь приведен пример, иллюстрирующий, как двойной рендеринг в строгом режиме помогает найти ошибку на ранней стадии.**

Этот компонент `StoryTray` берет массив `историй` и добавляет последний элемент "Create Story" в конце:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
    ```

=== "App.js"

    ```js
    import { useState } from 'react';
    import StoryTray from './StoryTray.js';

    let initialStories = [
    	{ id: 0, label: "Ankit's Story" },
    	{ id: 1, label: "Taylor's Story" },
    ];

    export default function App() {
    	let [stories, setStories] = useState(initialStories);
    	return (
    		<div
    			style={{
    				width: '100%',
    				height: '100%',
    				textAlign: 'center',
    			}}
    		>
    			<StoryTray stories={stories} />
    		</div>
    	);
    }
    ```

=== "StoryTray.js"

    ```js
    export default function StoryTray({ stories }) {
    	const items = stories;
    	items.push({ id: 'create', label: 'Create Story' });
    	return (
    		<ul>
    			{items.map((story) => (
    				<li key={story.id}>{story.label}</li>
    			))}
    		</ul>
    	);
    }
    ```

В приведенном выше коде есть ошибка. Однако ее легко не заметить, поскольку первоначальный вывод выглядит правильным.

Эта ошибка станет более заметной, если компонент `StoryTray` будет рендериться несколько раз. Например, давайте заставим `StoryTray` повторно отображаться с другим цветом фона при каждом наведении на него курсора:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
    ```

=== "App.js"

    ```js
    import { useState } from 'react';
    import StoryTray from './StoryTray.js';

    let initialStories = [
    	{ id: 0, label: "Ankit's Story" },
    	{ id: 1, label: "Taylor's Story" },
    ];

    export default function App() {
    	let [stories, setStories] = useState(initialStories);
    	return (
    		<div
    			style={{
    				width: '100%',
    				height: '100%',
    				textAlign: 'center',
    			}}
    		>
    			<StoryTray stories={stories} />
    		</div>
    	);
    }
    ```

=== "StoryTray.js"

    ```js
    import { useState } from 'react';

    export default function StoryTray({ stories }) {
    	const [isHover, setIsHover] = useState(false);
    	const items = stories;
    	items.push({ id: 'create', label: 'Create Story' });
    	return (
    		<ul
    			onPointerEnter={() => setIsHover(true)}
    			onPointerLeave={() => setIsHover(false)}
    			style={{
    				backgroundColor: isHover ? '#ddd' : '#fff',
    			}}
    		>
    			{items.map((story) => (
    				<li key={story.id}>{story.label}</li>
    			))}
    		</ul>
    	);
    }
    ```

Обратите внимание, что каждый раз, когда вы наводите курсор на компонент `StoryTray`, "Create Story" снова добавляется в список. Замысел кода заключался в том, чтобы добавить его один раз в конце. Но `StoryTray` напрямую изменяет массив `stories` из реквизита. Каждый раз, когда `StoryTray` рендерит, он снова добавляет "Create Story" в конец того же массива. Другими словами, `StoryTray` не является чистой функцией - ее многократный запуск приводит к различным результатам.

Чтобы решить эту проблему, вы можете сделать копию массива и изменить эту копию вместо оригинальной:

<!-- 0025.part.md -->

```js
export default function StoryTray({ stories }) {
  const items = stories.slice(); // Clone the array
  // ✅ Good: Pushing into a new array
  items.push({ id: 'create', label: 'Create Story' });
```

<!-- 0026.part.md -->

Это [сделает функцию `StoryTray` чистой](../learn/keeping-components-pure.md). При каждом вызове она будет модифицировать только новую копию массива и не будет влиять на внешние объекты или переменные. Это решает проблему, но вам придется заставлять компонент перерисовываться чаще, прежде чем станет очевидно, что в его поведении что-то не так.

**В исходном примере ошибка не была очевидной. Теперь давайте обернем исходный (баговый) код в `<StrictMode>`:**.

=== "index.js"

    ```js
    import { StrictMode } from 'react';
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(
    	<StrictMode>
    		<App />
    	</StrictMode>
    );
    ```

=== "App.js"

    ```js
    import { useState } from 'react';
    import StoryTray from './StoryTray.js';

    let initialStories = [
    	{ id: 0, label: "Ankit's Story" },
    	{ id: 1, label: "Taylor's Story" },
    ];

    export default function App() {
    	let [stories, setStories] = useState(initialStories);
    	return (
    		<div
    			style={{
    				width: '100%',
    				height: '100%',
    				textAlign: 'center',
    			}}
    		>
    			<StoryTray stories={stories} />
    		</div>
    	);
    }
    ```

=== "StoryTray.js"

    ```js
    export default function StoryTray({ stories }) {
    	const items = stories;
    	items.push({ id: 'create', label: 'Create Story' });
    	return (
    		<ul>
    			{items.map((story) => (
    				<li key={story.id}>{story.label}</li>
    			))}
    		</ul>
    	);
    }
    ```

**Строгий режим _всегда_ вызывает вашу функцию рендеринга дважды, чтобы вы могли сразу увидеть ошибку** ("Create Story" появляется дважды). Это позволяет заметить такие ошибки на ранней стадии процесса. Когда вы исправляете свой компонент для рендеринга в строгом режиме, вы _также_ исправляете многие возможные будущие ошибки производства, такие как функциональность hover, о которой говорилось ранее:

=== "index.js"

    ```js
    import { StrictMode } from 'react';
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(
    	<StrictMode>
    		<App />
    	</StrictMode>
    );
    ```

=== "App.js"

    ```js
    import { useState } from 'react';
    import StoryTray from './StoryTray.js';

    let initialStories = [
    	{ id: 0, label: "Ankit's Story" },
    	{ id: 1, label: "Taylor's Story" },
    ];

    export default function App() {
    	let [stories, setStories] = useState(initialStories);
    	return (
    		<div
    			style={{
    				width: '100%',
    				height: '100%',
    				textAlign: 'center',
    			}}
    		>
    			<StoryTray stories={stories} />
    		</div>
    	);
    }
    ```

=== "StoryTray.js"

    ```js
    import { useState } from 'react';

    export default function StoryTray({ stories }) {
    	const [isHover, setIsHover] = useState(false);
    	const items = stories.slice(); // Clone the array
    	items.push({ id: 'create', label: 'Create Story' });
    	return (
    		<ul
    			onPointerEnter={() => setIsHover(true)}
    			onPointerLeave={() => setIsHover(false)}
    			style={{
    				backgroundColor: isHover ? '#ddd' : '#fff',
    			}}
    		>
    			{items.map((story) => (
    				<li key={story.id}>{story.label}</li>
    			))}
    		</ul>
    	);
    }
    ```

Без режима Strict Mode ошибку легко было не заметить, пока вы не добавляли больше рендеров. В режиме Strict Mode та же ошибка появлялась сразу же. Режим Strict Mode помогает найти ошибки до того, как вы передадите их команде и пользователям.

[Подробнее о поддержании чистоты компонентов](../learn/keeping-components-pure.md).

!!!note ""

    Если у вас установлен [React DevTools](../learn/react-developer-tools.md), все вызовы `console.log` во время второго вызова рендеринга будут выглядеть слегка затемненными. React DevTools также предлагает настройку (по умолчанию выключена) для их полного подавления.

### Исправление ошибок, найденных при повторном запуске эффектов в разработке

Строгий режим также может помочь найти ошибки в [Эффектах](../learn/synchronizing-with-effects.md).

Каждый Эффект имеет некоторый код настройки и может иметь некоторый код очистки. Обычно React вызывает setup, когда компонент _mounts_ (добавляется на экран) и вызывает cleanup, когда компонент _unmounts_ (удаляется с экрана). Затем React снова вызывает cleanup и setup, если его зависимости изменились с момента последнего рендеринга.

Когда включен строгий режим, React также будет выполнять **один дополнительный цикл setup+cleanup в процессе разработки для каждого Effect.** Это может показаться удивительным, но это помогает выявить тонкие ошибки, которые трудно обнаружить вручную.

**Вот пример, иллюстрирующий, как повторный запуск Эффектов в строгом режиме помогает найти ошибки на ранней стадии.**.

Рассмотрим этот пример, который соединяет компонент с чатом:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
    ```

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';
    const roomId = 'general';

    export default function ChatRoom() {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    	}, []);
    	return <h1>Welcome to the {roomId} room!</h1>;
    }
    ```

=== "chat.js"

    ```js
    let connections = 0;

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
    			connections++;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    			connections--;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    	};
    }
    ```

В этом коде есть проблема, но она может быть не сразу понятна.

Чтобы сделать проблему более очевидной, давайте реализуем функцию. В приведенном ниже примере `roomId` не является жестко закодированным. Вместо этого пользователь может выбрать `roomId`, к которому он хочет подключиться, из выпадающего списка. Нажмите "Открыть чат", а затем выберите по очереди разные комнаты чата. Следите за количеством активных подключений в консоли:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
    ```

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId }) {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    	}, [roomId]);

    	return <h1>Welcome to the {roomId} room!</h1>;
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
    let connections = 0;

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
    			connections++;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    			connections--;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    	};
    }
    ```

Вы заметите, что количество открытых соединений постоянно растет. В реальном приложении это вызвало бы проблемы с производительностью и сетью. Проблема в том, что [вашему Эффекту не хватает функции очистки:](../learn/synchronizing-with-effects.md)

<!-- 0059.part.md -->

```js
useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
}, [roomId]);
```

<!-- 0060.part.md -->

Теперь, когда ваш Effect "убирает" за собой и уничтожает устаревшие связи, утечка решена. Однако обратите внимание, что проблема не стала заметной, пока вы не добавили больше возможностей (поле выбора).

**В исходном примере ошибка не была очевидной. Теперь давайте обернем исходный (баговый) код в `<StrictMode>`:**.

=== "index.js"

    ```js
    import { StrictMode } from 'react';
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(
    	<StrictMode>
    		<App />
    	</StrictMode>
    );
    ```

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';
    const roomId = 'general';

    export default function ChatRoom() {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    	}, []);
    	return <h1>Welcome to the {roomId} room!</h1>;
    }
    ```

=== "chat.js"

    ```js
    let connections = 0;

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
    			connections++;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    			connections--;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    	};
    }
    ```

**В строгом режиме вы сразу увидите, что есть проблема** (количество активных соединений подскочит до 2). Строгий режим запускает дополнительный цикл настройки+очистки для каждого Эффекта. Этот Эффект не имеет логики очистки, поэтому он создает дополнительное соединение, но не уничтожает его. Это намек на то, что вам не хватает функции очистки.

Строгий режим позволяет заметить такие ошибки на ранней стадии процесса. Когда вы исправляете свой Эффект, добавляя функцию очистки в строгом режиме, вы _также_ исправляете многие возможные будущие ошибки производства, такие как поле выбора из предыдущей версии:

=== "index.js"

    ```js
    import { StrictMode } from 'react';
    import { createRoot } from 'react-dom/client';
    import './styles.css';

    import App from './App';

    const root = createRoot(document.getElementById('root'));
    root.render(
    	<StrictMode>
    		<App />
    	</StrictMode>
    );
    ```

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId }) {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return <h1>Welcome to the {roomId} room!</h1>;
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
    let connections = 0;

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
    			connections++;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    			connections--;
    			console.log(
    				'Active connections: ' + connections
    			);
    		},
    	};
    }
    ```

Обратите внимание, что количество активных соединений в консоли больше не растет.

Без режима Strict Mode можно было легко пропустить, что ваш Эффект нуждается в очистке. Выполняя _setup → cleanup → setup_ вместо _setup_ для вашего Эффекта в разработке, Строгий режим сделал недостающую логику очистки более заметной.

[Подробнее о реализации очистки эффектов](../learn/synchronizing-with-effects.md)

### Исправление предупреждений об износе, включенных в строгом режиме

React предупреждает, если какой-то компонент в любом месте дерева `<StrictMode>` использует один из этих устаревших API:

-   `findDOMNode`. [См. альтернативы.](https://reactjs.org/docs/strict-mode.html#warning-about-deprecated-finddomnode-usage).
-   Методы жизненного цикла класса `UNSAFE_`, такие как `UNSAFE_componentWillMount`. [См. альтернативы.](https://reactjs.org/blog/2018/03/27/update-on-async-rendering.html#migrating-from-legacy-lifecycles).
-   Наследный контекст (`childContextTypes`, `contextTypes`, и `getChildContext`). [См. альтернативы](createContext.md).
-   Legacy string refs (`this.refs`). [См. альтернативы.](https://reactjs.org/docs/strict-mode.html#warning-about-legacy-string-ref-api-usage).

Эти API в основном используются в старых [компонентах классов](Component.md), поэтому они редко появляются в современных приложениях.

## Ссылки

-   [https://react.dev/reference/react/StrictMode](https://react.dev/reference/react/StrictMode)
