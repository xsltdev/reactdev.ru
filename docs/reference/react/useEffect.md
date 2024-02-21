---
description: useEffect - это хук React, который позволяет вам синхронизировать компонент с внешней системой
---

# useEffect

<big>**`useEffect`** - это хук React, который позволяет вам [синхронизировать компонент с внешней системой](../../learn/synchronizing-with-effects.md).</big>

```js
useEffect(setup, dependencies?)
```

## Описание {#reference}

### `useEffect(setup, dependencies?)` {#useeffect}

Вызовите `useEffect` на верхнем уровне вашего компонента, чтобы объявить Эффект:

```js
import { useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) {
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    );

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => {
            connection.disconnect();
        };
    }, [serverUrl, roomId]);
    // ...
}
```

#### Параметры {#parameters}

-   `setup`: Функция с логикой вашего Эффекта. Ваша функция настройки может также по желанию возвращать функцию _cleanup_. Когда ваш компонент будет добавлен в DOM, React запустит вашу функцию настройки. После каждого повторного рендеринга с измененными зависимостями React будет сначала запускать функцию очистки (если вы ее предоставили) со старыми значениями, а затем запускать вашу функцию настройки с новыми значениями. После удаления вашего компонента из DOM React запустит вашу функцию очистки.
-   **опциональные** `dependencies`: Список всех реактивных значений, на которые ссылается код `setup`. Реактивные значения включают props, state, а также все переменные и функции, объявленные непосредственно в теле вашего компонента. Если ваш линтер [настроен на React](../../learn/editor-setup.md), он проверит, что каждое реактивное значение правильно указано в качестве зависимости. Список зависимостей должен иметь постоянное количество элементов и быть написан inline по типу `[dep1, dep2, dep3]`. React будет сравнивать каждую зависимость с предыдущим значением, используя сравнение [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Если вы опустите этот аргумент, ваш Effect будет запускаться заново после каждого повторного рендеринга компонента.

#### Возврат {#returns}

`useEffect` возвращает `undefined`.

#### Ограничения {#caveats}

-   `useEffect` - это хук, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, создайте новый компонент и переместите состояние в него.

-   Если вы **не пытаетесь синхронизироваться с какой-то внешней системой,** [вам, вероятно, не нужен Эффект](../../learn/you-might-not-need-an-effect.md).

-   Когда включен строгий режим, React будет **проводить один дополнительный цикл настройки+очистки** только для разработки перед первой реальной настройкой. Это стресс-тест, который гарантирует, что ваша логика очистки "отражает" вашу логику настройки и что она останавливает или отменяет все, что делает настройка. Если это вызывает проблему, [реализуйте функцию очистки](../../learn/synchronizing-with-effects.md).

-   Если некоторые из ваших зависимостей являются объектами или функциями, определенными внутри компонента, есть риск, что они **приведут к тому, что Эффект будет перезапускаться чаще, чем нужно.** Чтобы исправить это, удалите ненужные зависимости `object` и `function`. Вы также можете извлекать обновления состояния и нереактивную логику вне вашего Эффекта.

-   Если ваш Эффект не был вызван взаимодействием (например, щелчком мыши), React позволит браузеру сначала нарисовать обновленный экран, прежде чем запустить ваш Эффект. Если ваш Эффект делает что-то визуальное (например, позиционирует всплывающую подсказку), и задержка заметна (например, она мерцает), замените `useEffect` на `useLayoutEffect`.

-   Даже если ваш Эффект был вызван взаимодействием (например, щелчком), **браузер может перерисовать экран до обработки обновлений состояния внутри вашего Эффекта.** Обычно это то, что вам нужно. Однако, если вы должны запретить браузеру перерисовывать экран, вам нужно заменить `useEffect` на [`useLayoutEffect`](useLayoutEffect.md).

-   Эффекты **работают только на клиенте.** Они не работают во время серверного рендеринга.

## Использование {#usage}

### Подключение к внешней системе {#connecting-to-an-external-system}

Некоторые компоненты должны оставаться подключенными к сети, API браузера или сторонней библиотеке, пока они отображаются на странице. Эти системы не контролируются React, поэтому их называют _внешними_.

Чтобы [подключить ваш компонент к какой-либо внешней системе,](../../learn/synchronizing-with-effects.md) вызовите `useEffect` на верхнем уровне вашего компонента:

```js hl_lines="10-14 16 18"
import { useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) {
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    );

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => {
            connection.disconnect();
        };
    }, [serverUrl, roomId]);
    // ...
}
```

Вам необходимо передать два аргумента в `useEffect`:

1.  Функция _setup_ с _установочным кодом_, которая подключается к этой системе.
    -   Она должна возвращать _функцию очистки_ с кодом очистки, которая отсоединяется от этой системы.
2.  Список зависимостей, включающий каждое значение из вашего компонента, используемое внутри этих функций.

**React вызывает ваши функции установки и очистки всякий раз, когда это необходимо, что может происходить несколько раз:**.

1.  Ваш _код установки_ выполняется, когда ваш компонент добавляется на страницу _(mounts)_.
2.  После каждого повторного рендеринга вашего компонента, когда зависимости изменились:
    -   Сначала ваш _очищающий код_ запускается со старыми пропсами и состоянием.
    -   Затем, ваш _установочный код_ запускается с новыми пропсами и состоянием.
3.  Ваш _очищающий код_ запускается в последний раз после того, как ваш компонент удаляется со страницы _(размонтируется)_.

**Давайте проиллюстрируем эту последовательность на примере выше.**

Когда вышеуказанный компонент `ChatRoom` добавляется на страницу, он подключается к чату с начальными `serverUrl` и `roomId`. Если `serverUrl` или `roomId` изменятся в результате повторного рендеринга (например, если пользователь выберет другую комнату в выпадающем списке), ваш Эффект _отключится от предыдущей комнаты и подключится к следующей._ Когда компонент `ChatRoom` будет удален со страницы, ваш Эффект отключится в последний раз.

**Чтобы [помочь вам найти ошибки](../../learn/synchronizing-with-effects.md), при разработке React запускает setup и cleanup один дополнительный раз перед setup.** Это стресс-тест, который проверяет правильность реализации логики вашего Эффекта. Если это вызывает видимые проблемы, значит, вашей функции очистки не хватает логики. Функция очистки должна остановить или отменить все, что делала функция настройки. Эмпирическое правило гласит, что пользователь не должен различать между однократным вызовом функции setup (как в продакшене) и последовательностью _setup_ → _cleanup_ → _setup_ (как в разработке). [См. общие решения](../../learn/synchronizing-with-effects.md).

**Попробуйте [писать каждый эффект как независимый процесс](../../learn/lifecycle-of-reactive-effects.md) и [думать об одном цикле установки/очистки за раз](../../learn/lifecycle-of-reactive-effects.md)**. Не должно иметь значения, монтируется, обновляется или размонтируется ваш компонент. Когда ваша логика очистки правильно "зеркалит" логику установки, ваш Эффект устойчив к запуску установки и очистки так часто, как это необходимо.

!!!note "Подключение к внешней системе"

    Эффект позволяет [синхронизировать ваш компонент](../../learn/synchronizing-with-effects.md) с какой-либо внешней системой (например, с чат-службой). Здесь под внешней системой подразумевается любой кусок кода, не контролируемый React, например:

    -   Таймер, управляемый с помощью [`setInterval()`](https://developer.mozilla.org/docs/Web/API/setInterval) и [`clearInterval()`](https://developer.mozilla.org/docs/Web/API/clearInterval).
    -   Подписка на события с помощью [`window.addEventListener()`](https://developer.mozilla.org/docs/Web/API/EventTarget/addEventListener) и [`window.removeEventListener()`](https://developer.mozilla.org/docs/Web/API/EventTarget/removeEventListener).
    -   Сторонняя библиотека анимации с API типа `animation.start()` и `animation.reset()`.

    **Если вы не подключаетесь к какой-либо внешней системе, [вам, вероятно, не нужен эффект](../../learn/you-might-not-need-an-effect.md)**.

### Примеры подключения к внешней системе {#examples-connecting}

**1. Подключение к чат-серверу**

В этом примере компонент `ChatRoom` использует эффект, чтобы оставаться подключенным к внешней системе, определенной в `chat.js`. Нажмите "Открыть чат", чтобы появился компонент `ChatRoom`. Эта песочница работает в режиме разработки, поэтому существует дополнительный цикл подключения и отключения, как [объясняется здесь](../../learn/synchronizing-with-effects.md) Попробуйте изменить `roomId` и `erverUrl` с помощью выпадающего списка и ввода, и посмотрите, как Эффект снова подключается к чату. Нажмите "Закрыть чат", чтобы увидеть, как Эффект отключится в последний раз.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    function ChatRoom({ roomId }) {
    	const [serverUrl, setServerUrl] = useState(
    		'https://localhost:1234'
    	);

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => {
    			connection.disconnect();
    		};
    	}, [roomId, serverUrl]);

    	return (
    		<>
    			<label>
    				Server URL:{' '}
    				<input
    					value={serverUrl}
    					onChange={(e) =>
    						setServerUrl(e.target.value)
    					}
    				/>
    			</label>
    			<h1>Welcome to the {roomId} room!</h1>
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

    <iframe src="https://codesandbox.io/embed/gs96tv?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Прослушивание глобального события браузера**

В этом примере внешней системой является сам DOM браузера. Обычно вы указываете слушателей событий с помощью JSX, но вы не можете прослушивать глобальный объект [`window`](https://developer.mozilla.org/docs/Web/API/Window) таким образом. Эффект позволяет вам подключиться к объекту `window` и прослушивать его события. Прослушивание события `pointermove` позволяет отслеживать положение курсора (или пальца) и обновлять красную точку, чтобы она двигалась вместе с ним.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function App() {
    	const [position, setPosition] = useState({
    		x: 0,
    		y: 0,
    	});

    	useEffect(() => {
    		function handleMove(e) {
    			setPosition({ x: e.clientX, y: e.clientY });
    		}
    		window.addEventListener('pointermove', handleMove);
    		return () => {
    			window.removeEventListener(
    				'pointermove',
    				handleMove
    			);
    		};
    	}, []);

    	return (
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
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/jqknkk?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**3. Запуск анимации**

В этом примере внешней системой является библиотека анимации в `animation.js`. Она предоставляет класс JavaScript под названием `FadeInAnimation`, который принимает узел DOM в качестве аргумента и раскрывает методы `start()` и `stop()` для управления анимацией. Этот компонент [использует ссылку](../../learn/manipulating-the-dom-with-refs.md) для доступа к базовому узлу DOM. Эффект считывает узел DOM из ссылки и автоматически запускает анимацию для этого узла при появлении компонента.

=== "App.js"

    ```js
    import { useState, useEffect, useRef } from 'react';
    import { FadeInAnimation } from './animation.js';

    function Welcome() {
    	const ref = useRef(null);

    	useEffect(() => {
    		const animation = new FadeInAnimation(ref.current);
    		animation.start(1000);
    		return () => {
    			animation.stop();
    		};
    	}, []);

    	return (
    		<h1
    			ref={ref}
    			style={{
    				opacity: 0,
    				color: 'white',
    				padding: 50,
    				textAlign: 'center',
    				fontSize: 50,
    				backgroundImage:
    					'radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(252,70,107,1) 100%)',
    			}}
    		>
    			Welcome
    		</h1>
    	);
    }

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Remove' : 'Show'}
    			</button>
    			<hr />
    			{show && <Welcome />}
    		</>
    	);
    }
    ```

=== "animation.js"

    ```js
    export class FadeInAnimation {
    	constructor(node) {
    		this.node = node;
    	}
    	start(duration) {
    		this.duration = duration;
    		if (this.duration === 0) {
    			// Jump to end immediately
    			this.onProgress(1);
    		} else {
    			this.onProgress(0);
    			// Start animating
    			this.startTime = performance.now();
    			this.frameId = requestAnimationFrame(() =>
    				this.onFrame()
    			);
    		}
    	}
    	onFrame() {
    		const timePassed =
    			performance.now() - this.startTime;
    		const progress = Math.min(
    			timePassed / this.duration,
    			1
    		);
    		this.onProgress(progress);
    		if (progress < 1) {
    			// We still have more frames to paint
    			this.frameId = requestAnimationFrame(() =>
    				this.onFrame()
    			);
    		}
    	}
    	onProgress(progress) {
    		this.node.style.opacity = progress;
    	}
    	stop() {
    		cancelAnimationFrame(this.frameId);
    		this.startTime = null;
    		this.frameId = null;
    		this.duration = 0;
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5vnp4z?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**4. Управление модальным диалогом**

В этом примере внешней системой является DOM браузера. Компонент `ModalDialog` отображает элемент [`<dialog>`](https://hcdev.ru/html/dialog/). Он использует Effect для синхронизации свойства `isOpen` с вызовами методов [`showModal()`](https://developer.mozilla.org/docs/Web/API/HTMLDialogElement/showModal) и [`close()`](https://developer.mozilla.org/docs/Web/API/HTMLDialogElement/close).

=== "App.js"

    ```js
    import { useState } from 'react';
    import ModalDialog from './ModalDialog.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Open dialog
    			</button>
    			<ModalDialog isOpen={show}>
    				Hello there!
    				<br />
    				<button
    					onClick={() => {
    						setShow(false);
    					}}
    				>
    					Close
    				</button>
    			</ModalDialog>
    		</>
    	);
    }
    ```

=== "ModalDialog.js"

    ```js
    import { useEffect, useRef } from 'react';

    export default function ModalDialog({ isOpen, children }) {
    	const ref = useRef();

    	useEffect(() => {
    		if (!isOpen) {
    			return;
    		}
    		const dialog = ref.current;
    		dialog.showModal();
    		return () => {
    			dialog.close();
    		};
    	}, [isOpen]);

    	return <dialog ref={ref}>{children}</dialog>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gp73hp?view=Editor+%2B+Preview&module=%2Fsrc%2FModalDialog.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**5. Отслеживание видимости элемента**

В этом примере внешней системой снова является DOM браузера. Компонент `App` отображает длинный список, затем компонент `Box`, а затем еще один длинный список. Прокрутите список вниз. Обратите внимание, что когда компонент `Box` появляется в области просмотра, цвет фона меняется на черный. Чтобы реализовать это, компонент `Box` использует Effect для управления [`IntersectionObserver`](https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API). Этот API браузера уведомляет вас, когда элемент DOM становится видимым в области просмотра.

=== "App.js"

    ```js
    import Box from './Box.js';

    export default function App() {
    	return (
    		<>
    			<LongSection />
    			<Box />
    			<LongSection />
    			<Box />
    			<LongSection />
    		</>
    	);
    }

    function LongSection() {
    	const items = [];
    	for (let i = 0; i < 50; i++) {
    		items.push(
    			<li key={i}>Item #{i} (keep scrolling)</li>
    		);
    	}
    	return <ul>{items}</ul>;
    }
    ```

=== "Box.js"

    ```js
    import { useRef, useEffect } from 'react';

    export default function Box() {
    	const ref = useRef(null);

    	useEffect(() => {
    		const div = ref.current;
    		const observer = new IntersectionObserver(
    			(entries) => {
    				const entry = entries[0];
    				if (entry.isIntersecting) {
    					document.body.style.backgroundColor =
    						'black';
    					document.body.style.color = 'white';
    				} else {
    					document.body.style.backgroundColor =
    						'white';
    					document.body.style.color = 'black';
    				}
    			}
    		);
    		observer.observe(div, {
    			threshold: 1.0,
    		});
    		return () => {
    			observer.disconnect();
    		};
    	}, []);

    	return (
    		<div
    			ref={ref}
    			style={{
    				margin: 20,
    				height: 100,
    				width: 100,
    				border: '2px solid black',
    				backgroundColor: 'blue',
    			}}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/zkrpcj?view=Editor+%2B+Preview&module=%2Fsrc%2FBox.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обертывание эффектов в пользовательские хуки {#wrapping-effects-in-custom-hooks}

Эффекты - это ["аварийный люк"](../../learn/escape-hatches.md): Вы используете их, когда вам нужно "выйти за пределы React" и когда нет лучшего встроенного решения для вашего случая использования. Если вы часто сталкиваетесь с необходимостью вручную писать Effects, это обычно признак того, что вам нужно извлечь некоторые [пользовательские хуки](../../learn/reusing-logic-with-custom-hooks.md) для общего поведения, на которое полагаются ваши компоненты.

Например, этот пользовательский хук `useChatRoom` "прячет" логику вашего Эффекта за более декларативным API:

```js hl_lines="1 11"
function useChatRoom({ serverUrl, roomId }) {
    useEffect(() => {
        const options = {
            serverUrl: serverUrl,
            roomId: roomId,
        };
        const connection = createConnection(options);
        connection.connect();
        return () => connection.disconnect();
    }, [roomId, serverUrl]);
}
```

Затем вы можете использовать его из любого компонента, как это сделано здесь:

```js hl_lines="6-9"
function ChatRoom({ roomId }) {
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    );

    useChatRoom({
        roomId: roomId,
        serverUrl: serverUrl,
    });
    // ...
}
```

В экосистеме React также существует множество отличных пользовательских хуков для любых целей.

Подробнее об [обертывании эффектов в пользовательские хуки :octicons-arrow-right-24:](../../learn/reusing-logic-with-custom-hooks.md)

### Примеры обертывания эффектов в пользовательские хуки {#examples-custom-hooks}

**1. Пользовательский хук `useChatRoom`**

Этот пример идентичен одному из предыдущих примеров, но логика вынесена в пользовательский хук.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useChatRoom } from './useChatRoom.js';

    function ChatRoom({ roomId }) {
    	const [serverUrl, setServerUrl] = useState(
    		'https://localhost:1234'
    	);

    	useChatRoom({
    		roomId: roomId,
    		serverUrl: serverUrl,
    	});

    	return (
    		<>
    			<label>
    				Server URL:{' '}
    				<input
    					value={serverUrl}
    					onChange={(e) =>
    						setServerUrl(e.target.value)
    					}
    				/>
    			</label>
    			<h1>Welcome to the {roomId} room!</h1>
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

=== "useChatRoom.js"

    ```js
    import { useEffect } from 'react';
    import { createConnection } from './chat.js';

    export function useChatRoom({ serverUrl, roomId }) {
    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => {
    			connection.disconnect();
    		};
    	}, [roomId, serverUrl]);
    }
    ```

=== "chat.js"

    ```js
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

    <iframe src="https://codesandbox.io/embed/fq28gy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Пользовательский хук `useWindowListener`**

Этот пример идентичен одному из предыдущих примеров, но логика вынесена в пользовательский хук.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useWindowListener } from './useWindowListener.js';

    export default function App() {
    	const [position, setPosition] = useState({
    		x: 0,
    		y: 0,
    	});

    	useWindowListener('pointermove', (e) => {
    		setPosition({ x: e.clientX, y: e.clientY });
    	});

    	return (
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
    	);
    }
    ```

=== "useWindowListener.js"

    ```js
    import { useState, useEffect } from 'react';

    export function useWindowListener(eventType, listener) {
    	useEffect(() => {
    		window.addEventListener(eventType, listener);
    		return () => {
    			window.removeEventListener(eventType, listener);
    		};
    	}, [eventType, listener]);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/2h5qzn?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**3. Пользовательский хук `useIntersectionObserver`**

Этот пример идентичен одному из предыдущих примеров, но логика частично вынесена в пользовательский хук.

=== "App.js"

    ```js
    import Box from './Box.js';

    export default function App() {
    	return (
    		<>
    			<LongSection />
    			<Box />
    			<LongSection />
    			<Box />
    			<LongSection />
    		</>
    	);
    }

    function LongSection() {
    	const items = [];
    	for (let i = 0; i < 50; i++) {
    		items.push(
    			<li key={i}>Item #{i} (keep scrolling)</li>
    		);
    	}
    	return <ul>{items}</ul>;
    }
    ```

=== "Box.js"

    ```js
    import { useRef, useEffect } from 'react';
    import { useIntersectionObserver } from './useIntersectionObserver.js';

    export default function Box() {
    	const ref = useRef(null);
    	const isIntersecting = useIntersectionObserver(ref);

    	useEffect(() => {
    		if (isIntersecting) {
    			document.body.style.backgroundColor = 'black';
    			document.body.style.color = 'white';
    		} else {
    			document.body.style.backgroundColor = 'white';
    			document.body.style.color = 'black';
    		}
    	}, [isIntersecting]);

    	return (
    		<div
    			ref={ref}
    			style={{
    				margin: 20,
    				height: 100,
    				width: 100,
    				border: '2px solid black',
    				backgroundColor: 'blue',
    			}}
    		/>
    	);
    }
    ```

=== "useIntersectionObserver.js"

    ```js
    import { useState, useEffect } from 'react';

    export function useIntersectionObserver(ref) {
    	const [isIntersecting, setIsIntersecting] = useState(
    		false
    	);

    	useEffect(() => {
    		const div = ref.current;
    		const observer = new IntersectionObserver(
    			(entries) => {
    				const entry = entries[0];
    				setIsIntersecting(entry.isIntersecting);
    			}
    		);
    		observer.observe(div, {
    			threshold: 1.0,
    		});
    		return () => {
    			observer.disconnect();
    		};
    	}, [ref]);

    	return isIntersecting;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6lpngr?view=Editor+%2B+Preview&module=%2Fsrc%2FBox.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Управление виджетом без React {#controlling-a-non-react-widget}

Иногда вы хотите, чтобы внешняя система синхронизировалась с каким-либо параметром или состоянием вашего компонента.

Например, если у вас есть сторонний виджет карты или компонент видеоплеера, написанный без React, вы можете использовать эффект для вызова методов, которые заставят его состояние соответствовать текущему состоянию вашего компонента React. Этот Эффект создает экземпляр класса `MapWidget`, определенного в `map-widget.js`. Когда вы изменяете параметр `zoomLevel` компонента `Map`, Эффект вызывает `setZoom()` для экземпляра класса, чтобы сохранить его синхронизацию:

=== "App.js"

    ```js
    import { useState } from 'react';
    import Map from './Map.js';

    export default function App() {
    	const [zoomLevel, setZoomLevel] = useState(0);
    	return (
    		<>
    			Zoom level: {zoomLevel}x
    			<button
    				onClick={() => setZoomLevel(zoomLevel + 1)}
    			>
    				+
    			</button>
    			<button
    				onClick={() => setZoomLevel(zoomLevel - 1)}
    			>
    				-
    			</button>
    			<hr />
    			<Map zoomLevel={zoomLevel} />
    		</>
    	);
    }
    ```

=== "Map.js"

    ```js
    import { useRef, useEffect } from 'react';
    import { MapWidget } from './map-widget.js';

    export default function Map({ zoomLevel }) {
    	const containerRef = useRef(null);
    	const mapRef = useRef(null);

    	useEffect(() => {
    		if (mapRef.current === null) {
    			mapRef.current = new MapWidget(
    				containerRef.current
    			);
    		}

    		const map = mapRef.current;
    		map.setZoom(zoomLevel);
    	}, [zoomLevel]);

    	return (
    		<div
    			style={{ width: 200, height: 200 }}
    			ref={containerRef}
    		/>
    	);
    }
    ```

=== "map-widget.js"

    ```js
    import 'leaflet/dist/leaflet.css';
    import * as L from 'leaflet';

    export class MapWidget {
    	constructor(domNode) {
    		this.map = L.map(domNode, {
    			zoomControl: false,
    			doubleClickZoom: false,
    			boxZoom: false,
    			keyboard: false,
    			scrollWheelZoom: false,
    			zoomAnimation: false,
    			touchZoom: false,
    			zoomSnap: 0.1,
    		});
    		L.tileLayer(
    			'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    			{
    				maxZoom: 19,
    				attribution: '© OpenStreetMap',
    			}
    		).addTo(this.map);
    		this.map.setView([0, 0], 0);
    	}
    	setZoom(level) {
    		this.map.setZoom(level);
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/znlk2c?view=Editor+%2B+Preview&module=%2Fsrc%2FMap.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="summer-glade-znlk2c" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В данном примере функция очистки не нужна, поскольку класс `MapWidget` управляет только узлом DOM, который был ему передан. После удаления React-компонента `Map` из дерева, и DOM-узел, и экземпляр класса `MapWidget` будут автоматически очищены от мусора JavaScript-движком браузера.

### Получение данных с помощью эффектов {#fetching-data-with-effects}

Вы можете использовать Эффект для получения данных для вашего компонента. Обратите внимание, что [если вы используете фреймворк](../../learn/start-a-new-react-project.md), использование механизма получения данных вашего фреймворка будет намного эффективнее, чем написание эффектов вручную.

Если вы хотите получить данные из Эффекта вручную, ваш код может выглядеть следующим образом:

```js
import { useState, useEffect } from 'react';
import { fetchBio } from './api.js';

export default function Page() {
    const [person, setPerson] = useState('Alice');
    const [bio, setBio] = useState(null);

    useEffect(() => {
        let ignore = false;
        setBio(null);
        fetchBio(person).then((result) => {
            if (!ignore) {
                setBio(result);
            }
        });
        return () => {
            ignore = true;
        };
    }, [person]);
    // ...
}
```

Обратите внимание на переменную `ignore`, которая инициализируется в `false` и устанавливается в `true` во время очистки. Это гарантирует, что [ваш код не пострадает от "условий гонки":](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect) ответы сети могут приходить не в том порядке, в котором вы их отправили.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { fetchBio } from './api.js';

    export default function Page() {
    	const [person, setPerson] = useState('Alice');
    	const [bio, setBio] = useState(null);
    	useEffect(() => {
    		let ignore = false;
    		setBio(null);
    		fetchBio(person).then((result) => {
    			if (!ignore) {
    				setBio(result);
    			}
    		});
    		return () => {
    			ignore = true;
    		};
    	}, [person]);

    	return (
    		<>
    			<select
    				value={person}
    				onChange={(e) => {
    					setPerson(e.target.value);
    				}}
    			>
    				<option value="Alice">Alice</option>
    				<option value="Bob">Bob</option>
    				<option value="Taylor">Taylor</option>
    			</select>
    			<hr />
    			<p>
    				<i>{bio ?? 'Loading...'}</i>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6k6p5h?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вы также можете переписать, используя синтаксис [`async` / `await`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function), но вам все равно придется предоставить функцию очистки:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { fetchBio } from './api.js';

    export default function Page() {
    	const [person, setPerson] = useState('Alice');
    	const [bio, setBio] = useState(null);
    	useEffect(() => {
    		async function startFetching() {
    			setBio(null);
    			const result = await fetchBio(person);
    			if (!ignore) {
    				setBio(result);
    			}
    		}

    		let ignore = false;
    		startFetching();
    		return () => {
    			ignore = true;
    		};
    	}, [person]);

    	return (
    		<>
    			<select
    				value={person}
    				onChange={(e) => {
    					setPerson(e.target.value);
    				}}
    			>
    				<option value="Alice">Alice</option>
    				<option value="Bob">Bob</option>
    				<option value="Taylor">Taylor</option>
    			</select>
    			<hr />
    			<p>
    				<i>{bio ?? 'Loading...'}</i>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/y2jgqx?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Запись получения данных непосредственно в Effects становится повторяющейся и затрудняет добавление таких оптимизаций, как кэширование и серверный рендеринг. [Проще использовать пользовательский хук - либо свой собственный, либо поддерживаемый сообществом](../../learn/reusing-logic-with-custom-hooks.md).

!!!note "Какие есть хорошие альтернативы для получения данных в Effects?"

    Написание вызовов `fetch` внутри Effects является [популярным способом получения данных](https://www.robinwieruch.de/react-hooks-fetch-data/), особенно в полностью клиентских приложениях. Однако это очень ручной подход, и у него есть существенные недостатки:

    -   **Эффекты не запускаются на сервере.** Это означает, что первоначальный HTML, отрисованный на сервере, будет содержать только состояние загрузки без каких-либо данных. Клиентский компьютер должен будет загрузить весь JavaScript и отобразить ваше приложение только для того, чтобы обнаружить, что теперь ему нужно загрузить данные. Это не очень эффективно.
    -   **Получение данных непосредственно в Effects позволяет легко создавать "сетевые водопады".** Вы рендерите родительский компонент, он получает некоторые данные, рендерит дочерние компоненты, а затем они начинают получать свои данные. Если сеть не очень быстрая, это значительно медленнее, чем параллельная выборка всех данных.
    -   Например, если компонент размонтируется, а затем снова монтируется, ему придется снова получать данные.
    -   **Это не очень эргономично.** Существует довольно много кода, связанного с написанием вызовов `fetch` таким образом, чтобы не страдать от ошибок типа [race conditions.](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect)

    Этот список недостатков не является специфическим для React. Он применим к выборке данных при подключении с помощью любой библиотеки. Как и в случае с маршрутизацией, выборка данных не является тривиальной задачей, поэтому мы рекомендуем следующие подходы:

    -   **Если вы используете [фреймворк](../../learn/start-a-new-react-project.md), используйте его встроенный механизм выборки данных.** Современные фреймворки React имеют встроенные механизмы выборки данных, которые эффективны и не страдают от описанных выше подводных камней.
    -   В противном случае, рассмотрите возможность использования или создания кэша на стороне клиента. Популярные решения с открытым исходным кодом включают [React Query](../../libs/react-query.md), [useSWR](https://swr.vercel.app/) и [React Router 6.4+.](../../libs/react-router.6/index.md) Вы также можете создать собственное решение, в этом случае вы будете использовать Effects под капотом, но также добавите логику для дедупликации запросов, кэширования ответов и избежания сетевых водопадов (путем предварительной загрузки данных или поднятия требований к данным в маршрутах).

    Вы можете продолжать получать данные непосредственно в Effects, если ни один из этих подходов вам не подходит.

### Указание реактивных зависимостей {#specifying-reactive-dependencies}

**Обратите внимание, что вы не можете "выбрать" зависимости вашего Эффекта.** Каждый реактивное значение, используемое вашим Эффектом, может быть использован в качестве зависимого.

```js
function ChatRoom({ roomId }) {
    // This is a reactive value
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    ); // This is a reactive value too

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        ); // This Effect reads these reactive values
        connection.connect();
        return () => connection.disconnect();
    }, [serverUrl, roomId]);
    // ✅ So you must specify them as dependencies of your Effect
    // ...
}
```

Если `serverUrl` или `roomId` изменятся, ваш Эффект переподключится к чату, используя новые значения.

**[Реактивные значения](../../learn/lifecycle-of-reactive-effects.md) включают пропсы и все переменные и функции, объявленные непосредственно внутри вашего компонента.** Поскольку `roomId` и `erverUrl` являются реактивными значениями, вы не можете удалить их из зависимостей. Если вы попытаетесь опустить их и [ваш линтер правильно настроен для React](../../learn/editor-setup.md), линтер отметит это как ошибку, которую нужно исправить:

```js hl_lines="13-14"
function ChatRoom({ roomId }) {
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    );

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => connection.disconnect();
    }, []); // 🔴 React Hook useEffect has missing dependencies:
    //           'roomId' and 'serverUrl'
    // ...
}
```

**Чтобы удалить зависимость, вам нужно ["доказать" линтеру, что она _не должна_ быть зависимостью](../../learn/removing-effect-dependencies.md)**. Например, вы можете убрать `serverUrl` из вашего компонента, чтобы доказать, что он не реактивный и не будет меняться при повторных рендерах:

```js hl_lines="2 12"
// Not a reactive value anymore
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => connection.disconnect();
    }, [roomId]); // ✅ All dependencies declared
    // ...
}
```

Теперь, когда `serverUrl` не является реактивным значением (и не может меняться при повторном рендере), ему не нужно быть зависимостью. **Если код вашего Эффекта не использует никаких реактивных значений, его список зависимостей должен быть пустым (`[]`):**

```js hl_lines="1-2 12"
const serverUrl = 'https://localhost:1234'; // Not a reactive value anymore
const roomId = 'music'; // Not a reactive value anymore

function ChatRoom() {
    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => connection.disconnect();
    }, []); // ✅ All dependencies declared
    // ...
}
```

[Эффект с пустыми зависимостями](../../learn/lifecycle-of-reactive-effects.md) не перезапускается при изменении пропсов или состояния вашего компонента.

!!!warning "Подавление линтера"

    Если у вас есть существующая кодовая база, у вас могут быть некоторые Эффекты, которые подавляют линтер подобным образом:

    ```js hl_lines="3-4"
    useEffect(() => {
    	// ...
    	// 🔴 Avoid suppressing the linter like this:
    	// eslint-ignore-next-line react-hooks/exhaustive-deps
    }, []);
    ```

    **Когда зависимости не соответствуют коду, существует высокий риск появления ошибок.** Подавляя линтер, вы "лжете" React о значениях, от которых зависит ваш Эффект. Вместо этого [докажите, что они не нужны](../../learn/removing-effect-dependencies.md).

### Примеры передачи реактивных зависимостей {#examples-dependencies}

**1. Передача массива зависимостей**

Если вы укажете зависимости, ваш Эффект запустится **после первоначального рендера** и _после повторных рендеров с измененными зависимостями_.

```js hl_lines="3"
useEffect(() => {
    // ...
}, [a, b]); // Runs again if a or b are different
```

В приведенном ниже примере `serverUrl` и `roomId` являются [реактивными значениями](../learn/lifecycle-of-reactive-effects.md), поэтому они оба должны быть указаны как зависимости. В результате выбор другой комнаты в выпадающем списке или редактирование URL сервера приводит к повторному подключению чата. Однако, поскольку `message` не используется в эффекте (и поэтому не является зависимостью), редактирование сообщения не приводит к повторному подключению к чату.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    function ChatRoom({ roomId }) {
    	const [serverUrl, setServerUrl] = useState(
    		'https://localhost:1234'
    	);
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => {
    			connection.disconnect();
    		};
    	}, [serverUrl, roomId]);

    	return (
    		<>
    			<label>
    				Server URL:{' '}
    				<input
    					value={serverUrl}
    					onChange={(e) =>
    						setServerUrl(e.target.value)
    					}
    				/>
    			</label>
    			<h1>Welcome to the {roomId} room!</h1>
    			<label>
    				Your message:{' '}
    				<input
    					value={message}
    					onChange={(e) =>
    						setMessage(e.target.value)
    					}
    				/>
    			</label>
    		</>
    	);
    }

    export default function App() {
    	const [show, setShow] = useState(false);
    	const [roomId, setRoomId] = useState('general');
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
    				<button onClick={() => setShow(!show)}>{show ? 'Close chat' : 'Open chat'}</button>
    			</label>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
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

    <iframe src="https://codesandbox.io/embed/sf2k8h?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Передача пустого массива зависимостей**

Если ваш Эффект действительно не использует никаких реактивных значений, он будет запущен только **после начального рендеринга**.

```js hl_lines="3"
useEffect(() => {
    // ...
}, []); // Does not run again (except once in development)
```

**Даже при пустых зависимостях, setup и cleanup будут [выполняться один дополнительный раз в разработке](../../learn/synchronizing-with-effects.md), чтобы помочь вам найти ошибки.**

В этом примере и `serverUrl` и `roomId` жестко закодированы. Поскольку они объявлены вне компонента, они не являются реактивными значениями, а значит, не являются зависимостями. Список зависимостей пуст, поэтому Effect не запускается при повторном рендере.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';
    const roomId = 'music';

    function ChatRoom() {
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => connection.disconnect();
    	}, []);

    	return (
    		<>
    			<h1>Welcome to the {roomId} room!</h1>
    			<label>
    				Your message:{' '}
    				<input
    					value={message}
    					onChange={(e) =>
    						setMessage(e.target.value)
    					}
    				/>
    			</label>
    		</>
    	);
    }

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Close chat' : 'Open chat'}
    			</button>
    			{show && <hr />}
    			{show && <ChatRoom />}
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
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

    <iframe src="https://codesandbox.io/embed/5tzrg6?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**3. Непередача массива зависимостей вообще**

Если вы не передаете массив зависимостей вообще, ваш Effect запускается **после каждого рендера (и повторного рендера)** вашего компонента.

```js hl_lines="3"
useEffect(() => {
    // ...
}); // Always runs again
```

В этом примере Effect повторно запускается при изменении `serverUrl` и `roomId`, что вполне разумно. Однако он _также_ запускается повторно, когда вы изменяете `message`, что, вероятно, нежелательно. Вот почему обычно указывается массив зависимостей.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    function ChatRoom({ roomId }) {
    	const [serverUrl, setServerUrl] = useState(
    		'https://localhost:1234'
    	);
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => {
    			connection.disconnect();
    		};
    	}); // No dependency array at all

    	return (
    		<>
    			<label>
    				Server URL:{' '}
    				<input
    					value={serverUrl}
    					onChange={(e) =>
    						setServerUrl(e.target.value)
    					}
    				/>
    			</label>
    			<h1>Welcome to the {roomId} room!</h1>
    			<label>
    				Your message:{' '}
    				<input
    					value={message}
    					onChange={(e) =>
    						setMessage(e.target.value)
    					}
    				/>
    			</label>
    		</>
    	);
    }

    export default function App() {
    	const [show, setShow] = useState(false);
    	const [roomId, setRoomId] = useState('general');
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
    				<button onClick={() => setShow(!show)}>{show ? 'Close chat' : 'Open chat'}</button>
    			</label>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
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

    <iframe src="https://codesandbox.io/embed/cjt9gy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обновление состояния на основе предыдущего состояния от Эффекта {#updating-state-based-on-previous-state-from-an-effect}

Когда вы хотите обновить состояние на основе предыдущего состояния Эффекта, вы можете столкнуться с проблемой:

```js hl_lines="6 9"
function Counter() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setCount(count + 1); // You want to increment the counter every second...
        }, 1000);
        return () => clearInterval(intervalId);
    }, [count]); // 🚩 ... but specifying `count` as a dependency always resets the interval.
    // ...
}
```

Поскольку `count` является реактивным значением, оно должно быть указано в списке зависимостей. Однако это заставляет Effect очищать и устанавливать заново каждый раз, когда изменяется `count`. Это не идеально.

Чтобы исправить это, [передайте функцию обновления состояния `c => c + 1`](useState.md) в `setCount`:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function Counter() {
    	const [count, setCount] = useState(0);

    	useEffect(() => {
    		const intervalId = setInterval(() => {
    			setCount((c) => c + 1); // ✅ Pass a state updater
    		}, 1000);
    		return () => clearInterval(intervalId);
    	}, []); // ✅ Now count is not a dependency

    	return <h1>{count}</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/rx8zj6?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Теперь, когда вы передаете `c => c + 1` вместо `count + 1`, [вашему Эффекту больше не нужно зависеть от `count`](../../learn/removing-effect-dependencies.md). В результате этого исправления, ему не нужно будет очищать и устанавливать интервал заново каждый раз, когда `count` меняется.

### Удаление ненужных объектных зависимостей {#removing-unnecessary-object-dependencies}

Если ваш Эффект зависит от объекта или функции, созданной во время рендеринга, он может запускаться слишком часто. Например, этот Эффект переподключается после каждого рендеринга, потому что объект `options` [разный для каждого рендеринга](../../learn/removing-effect-dependencies.md):

```js hl_lines="6-10 13 16"
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
    const [message, setMessage] = useState('');

    const options = {
        // 🚩 This object is created from scratch on every re-render
        serverUrl: serverUrl,
        roomId: roomId,
    };

    useEffect(() => {
        const connection = createConnection(options); // It's used inside the Effect
        connection.connect();
        return () => connection.disconnect();
    }, [options]); // 🚩 As a result, these dependencies are always different on a re-render
    // ...
}
```

Избегайте использования объекта, созданного во время рендеринга, в качестве зависимого. Вместо этого создайте объект внутри Effect:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId }) {
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		const options = {
    			serverUrl: serverUrl,
    			roomId: roomId,
    		};
    		const connection = createConnection(options);
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return (
    		<>
    			<h1>Welcome to the {roomId} room!</h1>
    			<input
    				value={message}
    				onChange={(e) => setMessage(e.target.value)}
    			/>
    		</>
    	);
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
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
    			<hr />
    			<ChatRoom roomId={roomId} />
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection({ serverUrl, roomId }) {
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

    <iframe src="https://codesandbox.io/embed/9lfgyv?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Теперь, когда вы создаете объект `options` внутри эффекта, сам эффект зависит только от строки `roomId`.

С этим исправлением ввод ввода не переподключает чат. В отличие от объекта, который создается заново, строка типа `roomId` не меняется, пока вы не зададите ей другое значение. Подробнее об [удалении зависимостей :octicons-arrow-right-24:](../../learn/removing-effect-dependencies.md).

### Удаление ненужных зависимостей от функций {#removing-unnecessary-function-dependencies}

Если ваш Эффект зависит от объекта или функции, созданной во время рендеринга, он может запускаться слишком часто. Например, этот Эффект переподключается после каждого рендера, потому что функция `createOptions` [разная для каждого рендера](../../learn/removing-effect-dependencies.md):

```js hl_lines="4-10 13 17"
function ChatRoom({ roomId }) {
    const [message, setMessage] = useState('');

    function createOptions() {
        // 🚩 This function is created from scratch on every re-render
        return {
            serverUrl: serverUrl,
            roomId: roomId,
        };
    }

    useEffect(() => {
        const options = createOptions(); // It's used inside the Effect
        const connection = createConnection();
        connection.connect();
        return () => connection.disconnect();
    }, [createOptions]); // 🚩 As a result, these dependencies are always different on a re-render
    // ...
}
```

Само по себе создание функции с нуля при каждом повторном рендере не является проблемой. Вам не нужно ее оптимизировать. Однако если вы используете ее в качестве зависимости от вашего Эффекта, это приведет к тому, что ваш Эффект будет запускаться заново после каждого повторного рендеринга.

Избегайте использования функции, созданной во время рендеринга, в качестве зависимости. Вместо этого объявите ее внутри Эффекта:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    const serverUrl = 'https://localhost:1234';

    function ChatRoom({ roomId }) {
    	const [message, setMessage] = useState('');

    	useEffect(() => {
    		function createOptions() {
    			return {
    				serverUrl: serverUrl,
    				roomId: roomId,
    			};
    		}

    		const options = createOptions();
    		const connection = createConnection(options);
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return (
    		<>
    			<h1>Welcome to the {roomId} room!</h1>
    			<input
    				value={message}
    				onChange={(e) => setMessage(e.target.value)}
    			/>
    		</>
    	);
    }

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
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
    			<hr />
    			<ChatRoom roomId={roomId} />
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection({ serverUrl, roomId }) {
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

    <iframe src="https://codesandbox.io/embed/xjmhvg?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Теперь, когда вы определяете функцию `createOptions` внутри эффекта, сам эффект зависит только от строки `roomId`. С этим исправлением ввод в input не переподключает чат. В отличие от функции, которая создается заново, такая строка, как `roomId`, не меняется, пока вы не установите для нее другое значение. Подробнее об [удалении зависимостей :octicons-arrow-right-24:](../../learn/removing-effect-dependencies.md).

### Чтение последних пропсов и состояния из эффекта {#reading-the-latest-props-and-state-from-an-effect}

!!!warning "Экспериментальный API"

    Этот раздел описывает **экспериментальный API, который еще не был выпущен** в стабильной версии React.

По умолчанию, когда вы читаете реактивное значение из Эффекта, вы должны добавить его как зависимость. Это гарантирует, что ваш Эффект "реагирует" на каждое изменение этого значения. Для большинства зависимостей это именно то поведение, которое вам нужно.

Однако иногда вы хотите читать **последние пропсы и состояния из Эффекта без "реакции" на них.** Например, представьте, что вы хотите регистрировать количество товаров в корзине при каждом посещении страницы:

```js hl_lines="3"
function Page({ url, shoppingCart }) {
    useEffect(() => {
        logVisit(url, shoppingCart.length);
    }, [url, shoppingCart]); // ✅ All dependencies declared
    // ...
}
```

**Что если вы хотите регистрировать посещение новой страницы после каждого изменения `url`, но _не_, если меняется только `shoppingCart`?** Вы не можете исключить `shoppingCart` из зависимостей, не нарушая правила реактивности. Однако вы можете выразить, что вы _не хотите_, чтобы часть кода "реагировала" на изменения, даже если она вызывается из Эффекта. [Объявите событие _Эффекта_](../../learn/separating-events-from-effects.md) с помощью хука [`useEffectEvent`](experimental_useEffectEvent.md) и переместите код, читающий `shoppingCart`, внутрь него:

```js hl_lines="2-4 7-8"
function Page({ url, shoppingCart }) {
    const onVisit = useEffectEvent((visitedUrl) => {
        logVisit(visitedUrl, shoppingCart.length);
    });

    useEffect(() => {
        onVisit(url);
    }, [url]); // ✅ All dependencies declared
    // ...
}
```

**События Эффекта не являются реактивными и всегда должны быть исключены из зависимостей вашего Эффекта.** Именно это позволяет вам поместить нереактивный код (где вы можете прочитать последнее значение некоторых пропсов и состояния) внутрь них. Читая `shoppingCart` внутри `onVisit`, вы гарантируете, что `shoppingCart` не будет повторно запускать ваш Эффект.

Подробнее о том, как [события Effect Events позволяют разделить реактивный и нереактивный код :octicons-arrow-right-24:](../../learn/separating-events-from-effects.md).

### Отображение разного содержимого на сервере и клиенте {#displaying-different-content-on-the-server-and-the-client}

Если ваше приложение использует серверный рендеринг (либо [напрямую](server.md), либо через [фреймворк](../../learn/start-a-new-react-project.md)), ваш компонент будет отображаться в двух разных средах. На сервере он будет рендериться для создания исходного HTML. На клиенте React снова запустит код рендеринга, чтобы прикрепить обработчики событий к этому HTML. Вот почему, чтобы [hydration](client-hydrateRoot.md) работал, ваш первоначальный вывод рендеринга должен быть идентичным на клиенте и на сервере.

В редких случаях вам может понадобиться отобразить разное содержимое на клиенте. Например, если ваше приложение считывает некоторые данные из [`localStorage`](https://developer.mozilla.org/docs/Web/API/Window/localStorage), оно не может сделать это на сервере. Вот как это можно реализовать:

```js
function MyComponent() {
    const [didMount, setDidMount] = useState(false);

    useEffect(() => {
        setDidMount(true);
    }, []);

    if (didMount) {
        // ... return client-only JSX ...
    } else {
        // ... return initial JSX ...
    }
}
```

Пока приложение загружается, пользователь будет видеть начальный вывод рендера. Затем, после загрузки и гидратации, ваш Effect запустится и установит `didMount` в `true`, вызывая повторный рендеринг. При этом произойдет переключение на вывод рендера только для клиента. Эффекты не запускаются на сервере, поэтому `didMount` было `false` во время первоначального серверного рендеринга.

Используйте этот паттерн экономно. Помните, что пользователи с медленным соединением будут видеть начальное содержимое довольно долго - потенциально много секунд - поэтому вы не захотите вносить резкие изменения во внешний вид вашего компонента. Во многих случаях вы можете избежать этого, условно показывая различные вещи с помощью CSS.

## Устранение неполадок {#troubleshooting}

### Мой эффект запускается дважды, когда компонент монтируется {#my-effect-runs-twice-when-the-component-mounts}

Когда включен строгий режим, в процессе разработки React запускает установку и очистку один дополнительный раз перед фактической установкой.

Это стресс-тест, который проверяет правильность реализации логики вашего Эффекта. Если это вызывает видимые проблемы, значит, вашей функции очистки не хватает логики. Функция очистки должна остановить или отменить все, что делала функция настройки. Эмпирическое правило гласит, что пользователь не должен различать между однократным вызовом функции setup (как в производстве) и последовательностью setup → cleanup → setup (как в разработке).

Подробнее о [как это помогает найти ошибки](../../learn/synchronizing-with-effects.md) и [как исправить логику](../../learn/synchronizing-with-effects.md)

### Мой эффект запускается после каждого рендера {#my-effect-runs-after-every-re-render}

Во-первых, проверьте, не забыли ли вы указать массив зависимостей:

```js hl_lines="3"
useEffect(() => {
    // ...
}); // 🚩 No dependency array: re-runs after every render!
```

Если вы указали массив зависимостей, но ваш Effect все равно перезапускается в цикле, это связано с тем, что одна из ваших зависимостей отличается при каждом повторном рендере.

Вы можете отладить эту проблему, вручную записав журнал зависимостей в консоль:

```js hl_lines="5"
useEffect(() => {
    // ..
}, [serverUrl, roomId]);

console.log([serverUrl, roomId]);
```

Затем вы можете щелкнуть правой кнопкой мыши на массивах из разных рендеров в консоли и выбрать "Store as a global variable" для обоих. Предположив, что первый массив был сохранен как `temp1`, а второй - как `temp2`, вы можете использовать консоль браузера, чтобы проверить, является ли каждая зависимость в обоих массивах одинаковой:

```js
// Is the first dependency the same between the arrays?
Object.is(temp1[0], temp2[0]);

// Is the second dependency the same between the arrays?
Object.is(temp1[1], temp2[1]);

// ... and so on for every dependency ...
Object.is(temp1[2], temp2[2]);
```

Когда вы обнаружите зависимость, которая отличается при каждом повторном рендере, вы обычно можете исправить ее одним из этих способов:

-   [Обновление состояния на основе предыдущего состояния эффекта](#updating-state-based-on-previous-state-from-an-effect)
-   [Удаление ненужных объектных зависимостей](#removing-unnecessary-object-dependencies)
-   [Удаление ненужных зависимостей функций](#removing-unnecessary-function-dependencies)
-   [Чтение последних пропсов и состояния из эффекта](#reading-the-latest-props-and-state-from-an-effect)

В крайнем случае (если эти методы не помогли), оберните его создание с помощью [`useMemo`](useMemo.md) или [`useCallback`](useCallback.md) (для функций).

### Мой Эффект повторяется в бесконечном цикле {#my-effect-keeps-re-running-in-an-infinite-cycle}

Если ваш Эффект запускается в бесконечном цикле, эти две вещи должны быть верны:

-   Ваш Эффект обновляет некоторое состояние.
-   Это состояние приводит к повторному рендерингу, что вызывает изменение зависимостей Эффекта.

Прежде чем приступить к устранению проблемы, спросите себя, подключается ли ваш Эффект к какой-либо внешней системе (например, DOM, сеть, сторонний виджет и так далее). Зачем вашему Эффекту нужно устанавливать состояние? Синхронизируется ли он с этой внешней системой? Или вы пытаетесь управлять потоком данных вашего приложения вместе с ней?

Если внешней системы нет, подумайте, не упростит ли вашу логику [полное удаление эффекта](../../learn/you-might-not-need-an-effect.md).

Если вы действительно синхронизируетесь с какой-то внешней системой, подумайте, почему и при каких условиях ваш Эффект должен обновлять состояние. Изменилось ли что-то, что влияет на визуальный вывод вашего компонента? Если вам нужно отслеживать какие-то данные, которые не используются при визуализации, то более подходящим вариантом может быть [ref](useRef.md) (который не вызывает повторного рендеринга). Убедитесь, что ваш эффект не обновляет состояние (и не запускает повторные рендеринги) чаще, чем это необходимо.

Наконец, если ваш Эффект обновляет состояние в нужное время, но цикл все еще существует, это связано с тем, что обновление состояния приводит к изменению одной из зависимостей Эффекта.

### Моя логика очистки выполняется, даже если компонент не был размонтирован {#my-cleanup-logic-runs-even-though-my-component-didnt-unmount}

Функция очистки запускается не только во время размонтирования, но и перед каждым повторным рендерингом с измененными зависимостями. Кроме того, в процессе разработки React запускает setup+cleanup один дополнительный раз сразу после монтирования компонента.

Если у вас есть код очистки без соответствующего кода установки, это обычно запах кода:

```js hl_lines="2-5"
useEffect(() => {
    // 🔴 Avoid: Cleanup logic without corresponding setup logic
    return () => {
        doSomething();
    };
}, []);
```

Ваша логика очистки должна быть "симметрична" логике настройки и должна останавливать или отменять все, что сделала настройка:

```js hl_lines="2-3 5"
useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
        connection.disconnect();
    };
}, [serverUrl, roomId]);
```

Узнайте, чем [жизненный цикл эффекта отличается от жизненного цикла компонента :octicons-arrow-right-24:](../../learn/lifecycle-of-reactive-effects.md).

### Мой эффект делает что-то визуальное, и я вижу мерцание перед его запуском {#my-effect-does-something-visual-and-i-see-a-flicker-before-it-runs}

Если ваш Эффект должен блокировать браузер от [рисования экрана](../../learn/render-and-commit.md), замените `useEffect` на [`useLayoutEffect`](useLayoutEffect.md). Обратите внимание, что **это не нужно для подавляющего большинства Эффектов.** Это понадобится только в том случае, если очень важно запустить ваш Эффект до рисования браузера: например, для измерения и позиционирования всплывающей подсказки до того, как пользователь ее увидит.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useEffect](https://react.dev/reference/react/useEffect)</small>
