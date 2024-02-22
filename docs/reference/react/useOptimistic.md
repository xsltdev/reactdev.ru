---
description: useOptimistic - это React хук, позволяющий оптимистично обновлять пользовательский интерфейс.
status: experimental
---

# useOptimistic

!!!example "Canary"

    Хук `useOptimistic` в настоящее время доступен только в Canary и экспериментальных каналах React.

<big>`useOptimistic` - это React хук, позволяющий "оптимистично" обновлять пользовательский интерфейс.</big>

```js
const [optimisticState, addOptimistic] = useOptimistic(
    state,
    updateFn
);
```

## Описание {#reference}

### `useOptimistic(state, updateFn)` {#useoptimistic}

`useOptimistic` - это React хук, который позволяет показывать другое состояние во время выполнения асинхронного действия. Он принимает некоторое состояние в качестве аргумента и возвращает копию этого состояния, которая может быть разной в течение всего времени выполнения асинхронного действия, например, сетевого запроса. Вы предоставляете функцию, которая принимает текущее состояние и входные данные для действия и возвращает оптимистичное состояние, которое будет использоваться, пока действие находится в процессе выполнения.

Это состояние называется "оптимистичным", потому что оно обычно используется для немедленного представления пользователю результата выполнения действия, даже если на его выполнение требуется время.

```js
import { useOptimistic } from 'react';

function AppContainer() {
    const [optimisticState, addOptimistic] = useOptimistic(
        state,
        // updateFn
        (currentState, optimisticValue) => {
            // merge and return new state
            // with optimistic value
        }
    );
}
```

#### Параметры {#parameters}

-   `state`: значение, которое будет возвращаться изначально и всякий раз, когда никаких действий не ожидается.
-   `updateFn(currentState, optimisticValue)`: функция, которая принимает текущее состояние и оптимистическое значение, переданное в `addOptimistic`, и возвращает полученное оптимистическое состояние. Это должна быть чистая функция. `updateFn` принимает два параметра. Это `currentState` и `optimisticValue`. Возвращаемое значение будет представлять собой объединенное значение `currentState` и `optimisticValue`.

#### Возвращаемое значение {#returns}

-   `optimisticState`: Результирующее оптимистичное состояние. Оно равно `state`, если только действие не ожидается, в этом случае оно равно значению, возвращаемому `updateFn`.
-   `addOptimistic`: `addOptimistic` - это диспетчерская функция, которую следует вызывать при оптимистическом обновлении. Она принимает один аргумент, `optimisticValue`, любого типа, и вызывает `updateFn` с `state` и `optimisticValue`.

## Использование {#usage}

### Оптимистическое обновление форм {#optimistically-updating-with-forms}

Хук `useOptimistic` предоставляет возможность оптимистично обновлять пользовательский интерфейс до завершения фоновой операции, например, сетевого запроса. В контексте форм эта техника помогает сделать приложения более отзывчивыми. Когда пользователь отправляет форму, вместо того чтобы ждать, пока ответ сервера отразит изменения, интерфейс сразу же обновляется с ожидаемым результатом.

Например, когда пользователь вводит сообщение в форму и нажимает кнопку "Отправить", хук `useOptimistic` позволяет сообщению сразу же появиться в списке с надписью "Отправка...", еще до того, как оно будет отправлено на сервер. Такой "оптимистичный" подход создает впечатление скорости и оперативности. Затем форма пытается действительно отправить сообщение в фоновом режиме. Как только сервер подтверждает, что сообщение получено, метка "Отправка..." удаляется.

=== "App.js"

    ```js
    import { useOptimistic, useState, useRef } from 'react';
    import { deliverMessage } from './actions.js';

    function Thread({ messages, sendMessage }) {
    	const formRef = useRef();
    	async function formAction(formData) {
    		addOptimisticMessage(formData.get('message'));
    		formRef.current.reset();
    		await sendMessage(formData);
    	}
    	const [
    		optimisticMessages,
    		addOptimisticMessage,
    	] = useOptimistic(messages, (state, newMessage) => [
    		...state,
    		{
    			text: newMessage,
    			sending: true,
    		},
    	]);

    	return (
    		<>
    			{optimisticMessages.map((message, index) => (
    				<div key={index}>
    					{message.text}
    					{!!message.sending && (
    						<small> (Sending...)</small>
    					)}
    				</div>
    			))}
    			<form action={formAction} ref={formRef}>
    				<input
    					type="text"
    					name="message"
    					placeholder="Hello!"
    				/>
    				<button type="submit">Send</button>
    			</form>
    		</>
    	);
    }

    export default function App() {
    	const [messages, setMessages] = useState([
    		{ text: 'Hello there!', sending: false, key: 1 },
    	]);
    	async function sendMessage(formData) {
    		const sentMessage = await deliverMessage(
    			formData.get('message')
    		);
    		setMessages((messages) => [
    			...messages,
    			{ text: sentMessage },
    		]);
    	}
    	return (
    		<Thread
    			messages={messages}
    			sendMessage={sendMessage}
    		/>
    	);
    }
    ```

=== "actions.js"

    ```js
    export async function deliverMessage(message) {
    	await new Promise((res) => setTimeout(res, 1000));
    	return message;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/hsvs2d?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="nostalgic-cdn-hsvs2d" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useOptimistic](https://react.dev/reference/react/useOptimistic)</small>
