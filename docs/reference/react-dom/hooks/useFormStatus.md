---
status: experimental
---

# useFormStatus

!!!example "Canary"

    Хук `useFormStatus` в настоящее время доступен только в канале React canary и экспериментальном канале. Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

<big>`useFormStatus` - это хук, который предоставляет вам информацию о статусе последней отправки формы.</big>

```js
const { pending, data, method, action } = useFormStatus();
```

## Описание {#reference}

### `useFormStatus()` {#use-form-status}

Хук `useFormStatus` предоставляет информацию о статусе последней отправки формы.

```js
import { useFormStatus } from "react-dom";
import action from './actions';

function Submit() {
  const status = useFormStatus();
  return <button disabled={status.pending}>Submit</button>
}

export default App() {
  return (
    <form action={action}>
      <Submit />
    </form>
  );
}
```

Чтобы получить информацию о статусе, компонент `Submit` должен быть отображен внутри `<form>`. Хук возвращает информацию, например, свойство `pending`, которое говорит вам, активно ли отправляется форма.

В приведенном выше примере `Submit` использует эту информацию, чтобы отключить нажатие `<button>`, пока форма отправляется.

**Параметры**

`useFormStatus` не принимает никаких параметров.

**Возвращаемое значение**

Объект `status` со следующими свойствами:

-   `pending`: Булево. Если `true`, это означает, что родительская `<form>` ожидает отправки. В противном случае - `false`.

-   `data`: Объект, реализующий интерфейс [`FormData`](https://developer.mozilla.org/docs/Web/API/FormData), который содержит данные, отправляемые родительской `<form>`. Если нет активной отправки или нет родительской `<form>`, то это будет `null`.

-   `method`: Строковое значение либо `'get'`, либо `'post'`. Это означает, что родительская `<form>` отправляется с помощью `GET` или `POST` [HTTP-метода](https://developer.mozilla.org/docs/Web/HTTP/Methods). По умолчанию `<form>` использует метод `GET` и может быть указан свойством [`method`](https://developer.mozilla.org/docs/Web/HTML/Element/form#method).

-   `action`: Ссылка на функцию, переданную в свойство `action` на родительской `<form>`. Если родительская `<form>` отсутствует, свойство равно `null`. Если свойству `action` передано значение URI или свойство `action` не указано, `status.action` будет равно `null`.

**Ограничения**

-   Хук `useFormStatus` должен быть вызван из компонента, который отображается внутри `<form>`.
-   `useFormStatus` будет возвращать информацию о состоянии только для родительской `<form>`. Он не будет возвращать информацию о статусе для любой из `<form>`, отображаемой в том же компоненте или дочерних компонентах.

## Использование {#usage}

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

!!!warning "`useFormStatus` не будет возвращать информацию о статусе для `<form>`, отображаемой в том же компоненте"

    Хук `useFormStatus` возвращает информацию о статусе только для родительской `<form>`, но не для всех `<form>`, отображаемых в том же компоненте, который вызывает хук, или в дочерних компонентах.

    ```js
    function Form() {
    	// 🚩 `pending` will never be true
    	// useFormStatus does not track the form rendered in this component
    	const { pending } = useFormStatus();
    	return <form action={submit}></form>;
    }
    ```

    Вместо этого вызовите `useFormStatus` из компонента, который находится внутри `<form>`.

    ```js
    function Submit() {
    	// ✅ `pending` will be derived from the form that wraps the Submit component
    	const { pending } = useFormStatus();
    	return <button disabled={pending}>...</button>;
    }

    function Form() {
    	// This is the <form> `useFormStatus` tracks
    	return (
    		<form action={submit}>
    			<Submit />
    		</form>
    	);
    }
    ```

### Считывание данных из формы {#read-form-data-being-submitted}

Вы можете использовать свойство `data` информации о состоянии, возвращаемой из `useFormStatus`, чтобы показать, какие данные отправляет пользователь.

Здесь у нас есть форма, в которой пользователь может запросить имя пользователя. Мы можем использовать `useFormStatus` для отображения временного сообщения о статусе, подтверждающего, какое имя пользователя было запрошено.

=== "UsernameForm.js"

    ```js
    import { useState, useMemo, useRef } from 'react';
    import { useFormStatus } from 'react-dom';

    export default function UsernameForm() {
    	const { pending, data } = useFormStatus();

    	const [showSubmitted, setShowSubmitted] = useState(
    		false
    	);
    	const submittedUsername = useRef(null);
    	const timeoutId = useRef(null);

    	useMemo(() => {
    		if (pending) {
    			submittedUsername.current = data?.get(
    				'username'
    			);
    			if (timeoutId.current != null) {
    				clearTimeout(timeoutId.current);
    			}

    			timeoutId.current = setTimeout(() => {
    				timeoutId.current = null;
    				setShowSubmitted(false);
    			}, 2000);
    			setShowSubmitted(true);
    		}
    	}, [pending, data]);

    	return (
    		<>
    			<label>Request a Username: </label>
    			<br />
    			<input type="text" name="username" />
    			<button type="submit" disabled={pending}>
    				{pending ? 'Submitting...' : 'Submit'}
    			</button>
    			{showSubmitted ? (
    				<p>
    					Submitted request for username:{' '}
    					{submittedUsername.current}
    				</p>
    			) : null}
    		</>
    	);
    }
    ```

=== "App.js"

    ```js
    import UsernameForm from './UsernameForm';
    import { submitForm } from './actions.js';

    export default function App() {
    	return (
    		<form action={submitForm}>
    			<UsernameForm />
    		</form>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/sdgy2s?view=Editor+%2B+Preview&module=%2Fsrc%2FUsernameForm.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="zen-shannon-sdgy2s" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Решение проблем {#troubleshooting}

### `status.pending` никогда не бывает `true` {#pending-is-never-true}

`useFormStatus` будет возвращать информацию о статусе только для родительской `<form>`.

Если компонент, вызывающий `useFormStatus`, не вложен в `<form>`, `status.pending` всегда будет возвращать `false`. Убедитесь, что `useFormStatus` вызывается в компоненте, который является дочерним элементом `<form>`.

`useFormStatus` не будет отслеживать статус `<form>`, отображаемого в том же компоненте.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/hooks/useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus)</small>
