---
status: experimental
description: Компонент встроенный в браузер form позволяет создавать интерактивные элементы управления для отправки информации
---

# &lt;form&gt;

!!!example "Canary"

    Расширения для `<form>` в React в настоящее время доступны только в канале React canary и экспериментальном канале. В стабильных релизах React `<form>` работает только как [встроенный в браузер HTML-компонент](./index.md#all-html-components). Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>Компонент [встроенный в браузер `<form>`](https://hcdev.ru/html/form/) позволяет создавать интерактивные элементы управления для отправки информации.</big>

```js
<form action={search}>
    <input name="query" />
    <button type="submit">Search</button>
</form>
```

## Описание {#reference}

### `<form>` {#form}

Чтобы создать интерактивные элементы управления для отправки информации, используйте [встроенный компонент браузера `<form>`](https://hcdev.ru/html/form/).

```js
<form action={search}>
    <input name="query" />
    <button type="submit">Search</button>
</form>
```

#### Пропсы {#props}

`<form>` поддерживает все [общие пропсы элементов](./common.md#props)

[`action`](https://hcdev.ru/html/form#action): URL или функция. Когда в `action` передается URL, форма будет вести себя как компонент HTML-формы. Когда в `action` передается функция, она будет обрабатывать отправку формы. Функция, переданная в `action`, может быть асинхронной и будет вызвана с единственным аргументом, содержащим [данные формы](https://developer.mozilla.org/en-US/docs/Web/API/FormData) отправленной формы. Свойство `action` может быть переопределено атрибутом `formAction` компонента `<button>`, `<input type="submit">` или `<input type="image">`.

**Ограничения**

-   Когда функция передается в `action` или `formAction`, метод HTTP будет POST, независимо от значения параметра `method`.

## Использование {#usage}

### Обработка отправки формы на клиенте {#handle-form-submission-on-the-client}

Передайте функцию в свойство `action` формы для запуска функции при отправке формы. [`formData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) будет передан в функцию в качестве аргумента, чтобы вы могли получить доступ к данным, отправленным формой. Это отличается от обычного [HTML action](https://hcdev.ru/html/form/#action), который принимает только URL.

=== "App.js"

    ```js
    export default function Search() {
    	function search(formData) {
    		const query = formData.get('query');
    		alert(`You searched for '${query}'`);
    	}
    	return (
    		<form action={search}>
    			<input name="query" />
    			<button type="submit">Search</button>
    		</form>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6pyqcx?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="prod-fog-6pyqcx" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обработка отправки формы с помощью серверного действия {#handle-form-submission-with-a-server-action}

Отображение `<form>` с вводом и кнопкой отправки. Передайте серверное действие (функцию, помеченную [`'use server'`](../../rsc/use-server.md)) в свойство `action` формы, чтобы запустить функцию при отправке формы.

Передача серверного действия в `<form action>` позволяет пользователям отправлять формы без включенного JavaScript или до загрузки кода. Это полезно для пользователей, у которых медленное соединение, устройство или отключен JavaScript, и похоже на то, как работают формы, когда в свойство `action` передается URL.

Вы можете использовать скрытые поля формы для предоставления данных действию `<form>`. Серверное действие будет вызвано с данными скрытого поля формы в виде экземпляра [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

```js
import { updateCart } from './lib.js';

function AddToCart({ productId }) {
    async function addToCart(formData) {
        'use server';
        const productId = formData.get('productId');
        await updateCart(productId);
    }
    return (
        <form action={addToCart}>
            <input
                type="hidden"
                name="productId"
                value={productId}
            />
            <button type="submit">Add to Cart</button>
        </form>
    );
}
```

Вместо того чтобы использовать скрытые поля формы для передачи данных в действие `<form>`, вы можете вызвать метод `bind`, чтобы снабдить его дополнительными аргументами. Это приведет к привязке к функции нового аргумента (`productId`) в дополнение к `formData`, который передается в качестве аргумента функции.

```js
import { updateCart } from './lib.js';

function AddToCart({ productId }) {
    async function addToCart(productId, formData) {
        'use server';
        await updateCart(productId);
    }
    const addProductToCart = addToCart.bind(
        null,
        productId
    );
    return (
        <form action={addProductToCart}>
            <button type="submit">Add to Cart</button>
        </form>
    );
}
```

Когда `<form>` отображается [Серверным компонентом](../../rsc/use-client.md), а в параметр `action` формы `<form>` передается [Серверное действие](../../rsc/use-server.md), форма [прогрессивно улучшается](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement).

### Отображение состояния ожидания во время отправки формы {#display-a-pending-state-during-form-submission}

Чтобы отобразить состояние ожидания во время отправки формы, вы можете вызвать хук `useFormStatus` в компоненте, отображаемом в `<form>`, и прочитать возвращаемое свойство `pending`.

Здесь мы используем свойство `pending`, чтобы указать, что форма отправляется.

=== "App.js"

    ```js
    import { useFormStatus } from 'react-dom';
    import { submitForm } from './actions.js';

    function Submit() {
    	const { pending } = useFormStatus();
    	return (
    		<button type="submit" disabled={pending}>
    			{pending ? 'Submitting...' : 'Submit'}
    		</button>
    	);
    }

    function Form({ action }) {
    	return (
    		<form action={action}>
    			<Submit />
    		</form>
    	);
    }

    export default function App() {
    	return <Form action={submitForm} />;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/2qyqy4?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="serene-satoshi-2qyqy4" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Подробнее о хуке `useFormStatus` читайте в [справочной документации](../hooks/useFormStatus.md).

### Оптимистическое обновление данных формы {#optimistically-updating-form-data}

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
    		setMessages([...messages, { text: sentMessage }]);
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

    <iframe src="https://codesandbox.io/embed/g9tj8k?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="blue-wave-g9tj8k" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обработка ошибок отправки формы {#handling-form-submission-errors}

В некоторых случаях функция, вызываемая реквизитом `<form>` `action`, выбрасывает ошибку. Вы можете обработать эти ошибки, обернув `<form>` в границу ошибки. Если функция, вызываемая реквизитом `<form>` `action`, выдает ошибку, то будет отображена обратная связь для границы ошибки.

=== "App.js"

    ```js
    import { ErrorBoundary } from 'react-error-boundary';

    export default function Search() {
    	function search() {
    		throw new Error('search error');
    	}
    	return (
    		<ErrorBoundary
    			fallback={
    				<p>
    					There was an error while submitting the
    					form
    				</p>
    			}
    		>
    			<form action={search}>
    				<input name="query" />
    				<button type="submit">Search</button>
    			</form>
    		</ErrorBoundary>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xyv5wq?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="async-wave-xyv5wq" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Отображение ошибки отправки формы без JavaScript {#display-a-form-submission-error-without-javascript}

Отображение сообщения об ошибке отправки формы до загрузки пакета JavaScript для прогрессивного улучшения требует, чтобы:

1.  `<form>` должна быть отображена [серверным компонентом](../../rsc/use-client.md)
2.  функция, передаваемая в свойство `action` `<form>`, должна быть [Server Action](../../rsc/use-server.md)
3.  `useActionState` Hook будет использоваться для отображения сообщения об ошибке

`useActionState` принимает два параметра: [Server Action](../../rsc/use-server.md) и начальное состояние. `useActionState` возвращает два значения: переменную состояния и экшен. Действие, возвращаемое `useActionState`, должно быть передано в свойство `action` формы. Переменная состояния, возвращаемая `useActionState`, может быть использована для отображения сообщения об ошибке. Значение, возвращаемое [Server Action](../../rsc/use-server.md), переданное в `useActionState`, будет использовано для обновления переменной состояния.

=== "App.js"

    ```js
    import { useActionState } from 'react';
    import { signUpNewUser } from './api';

    export default function Page() {
    	async function signup(prevState, formData) {
    		'use server';
    		const email = formData.get('email');
    		try {
    			await signUpNewUser(email);
    			alert(`Added "${email}"`);
    		} catch (err) {
    			return err.toString();
    		}
    	}
    	const [message, formAction] = useActionState(
    		signup,
    		null
    	);
    	return (
    		<>
    			<h1>Signup for my newsletter</h1>
    			<p>
    				Signup with the same email twice to see an
    				error
    			</p>
    			<form action={formAction} id="signup-form">
    				<label htmlFor="email">Email: </label>
    				<input
    					name="email"
    					id="email"
    					placeholder="react@example.com"
    				/>
    				<button>Sign up</button>
    				{!!message && <p>{message}</p>}
    			</form>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/y4rgmr?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="vigorous-haibt-y4rgmr" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Подробнее об обновлении состояния из действия формы можно узнать из документации [`useActionState`](../../react/useActionState.md)

### Обработка нескольких типов отправки {#handling-multiple-submission-types}

Формы могут быть разработаны для обработки нескольких действий отправки, основанных на кнопке, нажатой пользователем. Каждая кнопка внутри формы может быть связана с определенным действием или поведением путем установки свойства `formAction`.

Когда пользователь нажимает определенную кнопку, форма отправляется, и выполняется соответствующее действие, определенное атрибутами и действием этой кнопки. Например, форма может по умолчанию отправлять статью на проверку, но иметь отдельную кнопку с `formAction`, установленную для сохранения статьи в черновик.

=== "App.js"

    ```js
    export default function Search() {
    	function publish(formData) {
    		const content = formData.get('content');
    		const button = formData.get('button');
    		alert(
    			`'${content}' was published with the '${button}' button`
    		);
    	}

    	function save(formData) {
    		const content = formData.get('content');
    		alert(`Your draft of '${content}' has been saved!`);
    	}

    	return (
    		<form action={publish}>
    			<textarea name="content" rows={4} cols={40} />
    			<br />
    			<button
    				type="submit"
    				name="button"
    				value="submit"
    			>
    				Publish
    			</button>
    			<button formAction={save}>Save draft</button>
    		</form>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/ql6qph?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="late-glade-ql6qph" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/form](https://react.dev/reference/react-dom/components/form)</small>
