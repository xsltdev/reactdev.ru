---
status: experimental
---

# useFormState

!!!example "Canary"

    Хук `useFormState` в настоящее время доступен только в канале React canary и experimental. Подробнее о [каналах выпуска здесь](https://react.dev/community/versioning-policy#all-release-channels). Кроме того, для получения всех преимуществ `useFormState` вам необходимо использовать фреймворк, поддерживающий [React Server Components](../../react/use-client.md).

<big>`useFormState` - это хук, который позволяет вам обновлять состояние на основе результата действия формы.</big>

```js
const [state, formAction] = useFormState(fn, initialState);
```

## Описание {#reference}

### `useFormState(action, initialState)` {#useformstate}

Вызовите `useFormState` на верхнем уровне вашего компонента, чтобы создать состояние компонента, которое обновляется [при вызове действия формы](../components/form.md). Вы передаете `useFormState` существующую функцию действия формы, а также начальное состояние, и она возвращает новое действие, которое вы используете в своей форме, вместе с последним состоянием формы. Последнее состояние формы также передается в указанную вами функцию.

```js
import { useFormState } from 'react-dom';

async function increment(previousState, formData) {
    return previousState + 1;
}

function StatefulForm({}) {
    const [state, formAction] = useFormState(increment, 0);
    return (
        <form>
            {state}
            <button formAction={formAction}>
                Increment
            </button>
        </form>
    );
}
```

Состояние формы - это значение, возвращенное действием, когда форма была отправлена в последний раз. Если форма еще не была отправлена, это начальное состояние, которое вы передаете.

При использовании с серверным действием `useFormState` позволяет показывать ответ сервера от отправки формы даже до завершения гидратации.

**Параметры**

-   `fn`: Функция, которая будет вызываться при отправке формы или нажатии кнопки. Когда функция вызывается, она получает предыдущее состояние формы (сначала `initialState`, которое вы передаете, а затем предыдущее возвращаемое значение) в качестве начального аргумента, а затем аргументы, которые обычно получает действие формы.
-   `initialState`: Значение, которое вы хотите получить в качестве начального состояния. Это может быть любое сериализуемое значение. Этот аргумент игнорируется после первого вызова действия.

**Возвращаемое значение**

`useFormState` возвращает массив, содержащий ровно два значения:

1.  Текущее состояние. Во время первого рендера оно будет соответствовать переданному вами значению `initialState`. После вызова действия оно будет соответствовать значению, возвращенному действием.
2.  Новое действие, которое вы можете передать в качестве свойства `action` компоненту `form` или свойства `formAction` любому компоненту `button` внутри формы.

**Ограничения**

-   При использовании с фреймворком, поддерживающим серверные компоненты React, `useFormState` позволяет сделать формы интерактивными до выполнения JavaScript на клиенте. При использовании без серверных компонентов это эквивалентно локальному состоянию компонента.
-   Функция, передаваемая `useFormState`, получает в качестве первого аргумента дополнительный аргумент - предыдущее или начальное состояние. Это делает ее сигнатуру иной, чем если бы она использовалась непосредственно как действие формы без использования `useFormState`.

## Использование {#usage}

### Использование информации, возвращаемой действием формы {#using-information-returned-by-a-form-action}

Вызовите `useFormState` на верхнем уровне вашего компонента, чтобы получить доступ к возвращаемому значению действия из последнего раза, когда форма была отправлена.

```js
import { useFormState } from 'react-dom';
import { action } from './actions.js';

function MyComponent() {
    const [state, formAction] = useFormState(action, null);
    // ...
    return <form action={formAction}>{/* ... */}</form>;
}
```

`useFormState` возвращает массив, содержащий ровно два элемента:

1.  Текущее состояние формы, которое первоначально устанавливается в указанное вами начальное состояние, а после отправки формы устанавливается в возвращаемое значение указанного вами действия.
2.  Новое действие, которое вы передаете в `<form>` в качестве его свойства `action`.

Когда форма будет отправлена, будет вызвана указанная вами функция действия. Ее возвращаемое значение станет новым текущим состоянием формы.

Предоставленное вами действие также получит новый первый аргумент, а именно текущее состояние формы. При первой отправке формы это будет начальное состояние, которое вы указали, а при последующих отправках - возвращаемое значение, полученное при последнем вызове действия. Остальные аргументы такие же, как если бы `useFormState` не использовался

```js
function action(currentState, formData) {
    // ...
    return 'next state';
}
```

### Отображение информации после отправки формы {#display-information-after-submitting-a-form}

**1. Отображение ошибок формы**

Чтобы отобразить сообщения, такие как сообщение об ошибке или тост, возвращаемый серверным действием, оберните действие вызовом `useFormState`.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useFormState } from 'react-dom';
    import { addToCart } from './actions.js';

    function AddToCartForm({ itemID, itemTitle }) {
    	const [message, formAction] = useFormState(
    		addToCart,
    		null
    	);
    	return (
    		<form action={formAction}>
    			<h2>{itemTitle}</h2>
    			<input
    				type="hidden"
    				name="itemID"
    				value={itemID}
    			/>
    			<button type="submit">Add to Cart</button>
    			{message}
    		</form>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<AddToCartForm
    				itemID="1"
    				itemTitle="JavaScript: The Definitive Guide"
    			/>
    			<AddToCartForm
    				itemID="2"
    				itemTitle="JavaScript: The Good Parts"
    			/>
    		</>
    	);
    }
    ```

=== "actions.js"

    ```js
    'use server';

    export async function addToCart(prevState, queryData) {
    	const itemID = queryData.get('itemID');
    	if (itemID === '1') {
    		return 'Added to cart';
    	} else {
    		return "Couldn't add to cart: the item is sold out.";
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yv2vzy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="damp-tree-yv2vzy" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Отображение структурированной информации после отправки формы**

Возвращаемое значение действия сервера может быть любым сериализуемым значением. Например, это может быть объект, содержащий логическое значение, указывающее на успешность выполнения действия, сообщение об ошибке или обновленную информацию.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useFormState } from 'react-dom';
    import { addToCart } from './actions.js';

    function AddToCartForm({ itemID, itemTitle }) {
    	const [formState, formAction] = useFormState(
    		addToCart,
    		{}
    	);
    	return (
    		<form action={formAction}>
    			<h2>{itemTitle}</h2>
    			<input
    				type="hidden"
    				name="itemID"
    				value={itemID}
    			/>
    			<button type="submit">Add to Cart</button>
    			{formState?.success && (
    				<div className="toast">
    					Added to cart! Your cart now has{' '}
    					{formState.cartSize} items.
    				</div>
    			)}
    			{formState?.success === false && (
    				<div className="error">
    					Failed to add to cart:{' '}
    					{formState.message}
    				</div>
    			)}
    		</form>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<AddToCartForm
    				itemID="1"
    				itemTitle="JavaScript: The Definitive Guide"
    			/>
    			<AddToCartForm
    				itemID="2"
    				itemTitle="JavaScript: The Good Parts"
    			/>
    		</>
    	);
    }
    ```

=== "actions.js"

    ```js
    'use server';

    export async function addToCart(prevState, queryData) {
    	const itemID = queryData.get('itemID');
    	if (itemID === '1') {
    		return {
    			success: true,
    			cartSize: 12,
    		};
    	} else {
    		return {
    			success: false,
    			message: 'The item is sold out.',
    		};
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/kmkspd?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="jolly-minsky-kmkspd" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Решение проблем {#troubleshooting}

### Мое действие больше не может читать данные отправленной формы {#my-action-can-no-longer-read-the-submitted-form-data}

Когда вы оборачиваете действие с помощью `useFormState`, оно получает дополнительный аргумент _в качестве первого аргумента_. Таким образом, отправленные данные формы являются его _вторым_ аргументом, а не первым, как это было бы обычно. Новый первый аргумент, который добавляется, - это текущее состояние формы.

```js
function action(currentState, formData) {
    // ...
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/hooks/useFormState](https://react.dev/reference/react-dom/hooks/useFormState)</small>
