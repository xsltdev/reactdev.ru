---
status: experimental
description: use - это хук React, который позволяет вам прочитать значение ресурса, например промиса или контекста
---

# use

!!!example "Canary"

    В настоящее время хук `use` доступен только в канале React canary и экспериментальном канале.

<big>`use` - это хук React, который позволяет вам прочитать значение ресурса, например [промиса](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекста](../../learn/passing-data-deeply-with-context.md).</big>

```js
const value = use(resource);
```

---

## Описание {#reference}

### `use(resource)` {#use}

Вызовите `use` в вашем компоненте, чтобы прочитать значение ресурса, например [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [context](../../learn/passing-data-deeply-with-context.md).

```js
import { use } from 'react';

function MessageComponent({ messagePromise }) {
    const message = use(messagePromise);
    const theme = use(ThemeContext);
    // ...
}
```

В отличие от всех остальных хуков React, `use` можно вызывать в циклах и условных операторах, таких как `if`. Как и другие хуки React, функция, вызывающая `use`, должна быть компонентом или хуком.

При вызове с `Promise` хук `use` интегрируется с [`Suspense`](Suspense.md) и [error boundaries](Component.md#catching-rendering-errors-with-an-error-boundary). Компонент, вызывающий `use`, _приостанавливается_ на время выполнения `Promise`, переданного `use`. Если компонент, вызывающий `use`, обернут в границу `Suspense`, то будет отображен `fallback`. После разрешения `Promise`, Suspense fallback заменяется рендерингом компонентов, использующих данные, возвращенные хуком `use`. Если промис, переданный в `use`, отклонен, будет отображен фаллбек ближайшей границы ошибки.

#### Параметры {#parameters}

-   `resource`: это источник данных, из которого вы хотите прочитать значение. Ресурсом может быть [промис](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекст](../../learn/passing-data-deeply-with-context.md).

#### Возвращает {#returns}

Хук `use` возвращает значение, которое было прочитано из ресурса, как разрешенное значение [промиса](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекст](../../learn/passing-data-deeply-with-context.md).

#### Замечания {#caveats}

-   Хук `use` должен быть вызван внутри компонента или хука.
-   При получении данных в [серверном компоненте](../rsc/use-server.md) отдавайте предпочтение `async` и `await`, а не `use`. `async` и `await` выполняют рендеринг с того момента, когда был вызван `await`, в то время как `use` повторно рендерит компонент после разрешения данных.
-   Предпочтительнее создавать промисы в [Компонентах сервера](../rsc/use-server.md) и передавать их в [Компоненты клиента](../rsc/use-client.md), чем создавать обещания в компонентах клиента. Обещания, созданные в клиентских компонентах, пересоздаются при каждом рендере. Обещания, переданные из серверного компонента в клиентский компонент, стабильны при каждом рендере. [См. этот пример](#streaming-data-from-server-to-client).

## Использование {#usage}

### Чтение контекста с помощью `use` {#reading-context-with-use}

Когда в `use` передается [context](../../learn/passing-data-deeply-with-context.md), он работает аналогично [`useContext`](useContext.md). В то время как `useContext` должен вызываться на верхнем уровне вашего компонента, `use` можно вызывать внутри условий типа `if` и циклов типа `for`. `use` предпочтительнее, чем `useContext`, потому что он более гибкий.

```js hl_lines="4"
import { use } from 'react';

function Button() {
    const theme = use(ThemeContext);
    // ...
}
```

`use` возвращает значение контекста для переданного вами контекста. Чтобы определить значение контекста, React просматривает дерево компонентов и находит **ближайший провайдер контекста выше** для данного контекста.

Чтобы передать контекст кнопке `Button`, оберните ее или один из ее родительских компонентов в соответствующий провайдер контекста.

```js hl_lines="3 5"
function MyPage() {
    return (
        <ThemeContext.Provider value="dark">
            <Form />
        </ThemeContext.Provider>
    );
}

function Form() {
    // ... renders buttons inside ...
}
```

Не имеет значения, сколько слоев компонентов находится между провайдером и `Button`. Когда `Button` _в любом месте_ внутри `Form` вызывает `use(ThemeContext)`, она получит `"dark"` в качестве значения.

В отличие от [`useContext`](useContext.md), `use` можно вызывать в условиях и циклах, как `if`.

```js hl_lines="2-3"
function HorizontalRule({ show }) {
    if (show) {
        const theme = use(ThemeContext);
        return <hr className={theme} />;
    }
    return false;
}
```

`use` вызывается внутри оператора `if`, позволяя вам условно считывать значения из Context.

!!!warning "Ближайший провайдер"

    Как и `useContext`, `use(context)` всегда ищет ближайшего провайдера контекста _выше_ компонента, который его вызывает. Он ищет вверх и **не** рассматривает провайдеров контекста в компоненте, из которого вы вызываете `use(context)`.

</Pitfall>

<Sandpack>

=== "App.js"

    ```js
    import { createContext, use } from 'react';

    const ThemeContext = createContext(null);

    export default function MyApp() {
    	return (
    		<ThemeContext.Provider value="dark">
    			<Form />
    		</ThemeContext.Provider>
    	);
    }

    function Form() {
    	return (
    		<Panel title="Welcome">
    			<Button show={true}>Sign up</Button>
    			<Button show={false}>Log in</Button>
    		</Panel>
    	);
    }

    function Panel({ title, children }) {
    	const theme = use(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ show, children }) {
    	if (show) {
    		const theme = use(ThemeContext);
    		const className = 'button-' + theme;
    		return (
    			<button className={className}>
    				{children}
    			</button>
    		);
    	}
    	return false;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/68ryxj?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="silly-dijkstra-68ryxj" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Потоковая передача данных от сервера к клиенту {#streaming-data-from-server-to-client}

Данные могут передаваться от сервера к клиенту путем передачи Promise в качестве реквизита от серверного компонента к клиентскому компоненту.

```js
import { fetchMessage } from './lib.js';
import { Message } from './message.js';

export default function App() {
    const messagePromise = fetchMessage();
    return (
        <Suspense fallback={<p>waiting for message...</p>}>
            <Message messagePromise={messagePromise} />
        </Suspense>
    );
}
```

Затем клиентский компонент принимает полученное обещание в качестве реквизита и передает его хуку `use`. Это позволяет клиентскому компоненту прочитать значение из обещания, которое было первоначально создано серверным компонентом.

```js
// message.js
'use client';

import { use } from 'react';

export function Message({ messagePromise }) {
    const messageContent = use(messagePromise);
    return <p>Here is the message: {messageContent}</p>;
}
```

Поскольку `Message` обернут в [`Suspense`](Suspense.md), fallback будет отображаться до тех пор, пока Promise не будет разрешен. Когда обещание будет разрешено, значение будет считано хуком `use` и компонент `Message` заменит фаллбэк Suspense.

=== "message.js"

    ```js
    'use client';

    import { use, Suspense } from 'react';

    function Message({ messagePromise }) {
    	const messageContent = use(messagePromise);
    	return <p>Here is the message: {messageContent}</p>;
    }

    export function MessageContainer({ messagePromise }) {
    	return (
    		<Suspense
    			fallback={<p>⌛Downloading message...</p>}
    		>
    			<Message messagePromise={messagePromise} />
    		</Suspense>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/8dg646?view=Editor+%2B+Preview&module=%2Fsrc%2Fmessage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="happy-shadow-8dg646" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Сериализуемость значений"

    При передаче Promise от серверного компонента к клиентскому компоненту его разрешенное значение должно быть сериализуемым для передачи между сервером и клиентом. Типы данных, такие как функции, не являются сериализуемыми и не могут быть разрешенным значением такого промиса.

!!!info "Как разрешить промис в серверном или клиентском компоненте?"

    Промис можно передать из серверного компонента в клиентский компонент и разрешить его в клиентском компоненте с помощью хука `use`. Вы также можете разрешить промис в серверном компоненте с помощью `await` и передать необходимые данные клиентскому компоненту в качестве свойства.

    ```js
    export default function App() {
    	const messageContent = await fetchMessage();
    	return <Message messageContent={messageContent} />
    }
    ```

    Но использование `await` в компоненте [Server Component](components.md#server-components) заблокирует его рендеринг до завершения оператора `await`. Передача промиса от серверного компонента клиентскому компоненту не позволяет промису блокировать отрисовку серверного компонента.

### Работа с отклоненными промисами {#dealing-with-rejected-promises}

В некоторых случаях промис, переданный в `use`, может быть отклонен. Вы можете обработать отклоненные промисы следующим образом:

1.  [Отображение ошибки для пользователей с границей ошибки](#displaying-an-error-to-users-with-error-boundary).
2.  [Предоставить альтернативное значение с помощью `Promise.catch`](#providing-an-alternative-value-with-promise-catch)

!!!warning "try-catch"

    `use` нельзя вызывать в блоке `try-catch`. Вместо блока `try-catch` [оберните ваш компонент в границу ошибки](#displaying-an-error-to-users-with-error-boundary) или [предоставьте альтернативное значение для использования в методе `.catch` промиса](#providing-an-alternative-value-with-promise-catch).

#### Отображение ошибки для пользователей с границей ошибки {#displaying-an-error-to-users-with-error-boundary}

Если вы хотите отобразить ошибку для пользователей, когда промис отклоняется, вы можете использовать [границу ошибки](Component.md#catching-rendering-errors-with-an-error-boundary). Чтобы использовать границу ошибки, оберните компонент, в котором вы вызываете хук `use`, в границу ошибки. Если промис, переданный в `use`, будет отклонен, то будет отображен обратный вариант границы ошибки.

=== "message.js"

    ```js
    'use client';

    import { use, Suspense } from 'react';
    import { ErrorBoundary } from 'react-error-boundary';

    export function MessageContainer({ messagePromise }) {
    	return (
    		<ErrorBoundary
    			fallback={<p>⚠️Something went wrong</p>}
    		>
    			<Suspense
    				fallback={<p>⌛Downloading message...</p>}
    			>
    				<Message messagePromise={messagePromise} />
    			</Suspense>
    		</ErrorBoundary>
    	);
    }

    function Message({ messagePromise }) {
    	const content = use(messagePromise);
    	return <p>Here is the message: {content}</p>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dzl7jd?view=Editor+%2B+Preview&module=%2Fsrc%2Fmessage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="funny-cherry-dzl7jd" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### Предоставление альтернативного значения с помощью `Promise.catch` {#providing-an-alternative-value-with-promise-catch}

Если вы хотите предоставить альтернативное значение, когда промис, переданный в `use`, будет отклонен, вы можете использовать метод [`catch`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch) промиса.

```js hl_lines="8"
import { Message } from './message.js';

export default function App() {
    const messagePromise = new Promise(
        (resolve, reject) => {
            reject();
        }
    ).catch(() => {
        return 'no new message found.';
    });

    return (
        <Suspense fallback={<p>waiting for message...</p>}>
            <Message messagePromise={messagePromise} />
        </Suspense>
    );
}
```

Чтобы использовать метод `catch` промиса, вызовите `catch` на объекте промиса. `catch` принимает единственный аргумент: функцию, которая принимает в качестве аргумента сообщение об ошибке. То, что будет возвращено функцией, переданной в `catch`, будет использовано в качестве разрешенного значения промиса.

## Устранение неполадок {#troubleshooting}

### "Suspense Exception: This is not a real error!" {#suspense-exception-error}

Вы либо вызываете `use` вне компонента React или функции Hook, либо вызываете `use` в блоке try-catch. Если вы вызываете `use` внутри блока try-catch, оберните ваш компонент в границу ошибки или вызовите `catch` промиса, чтобы поймать ошибку и разрешить промис другим значением. [См. эти примеры](#dealing-with-rejected-promises).

Если вы вызываете `use` вне компонента React или функции Hook, перенесите вызов `use` в компонент React или функцию Hook.

```jsx
function MessageComponent({messagePromise}) {
  function download() {
    // ❌ the function calling `use` is not a Component or Hook
    const message = use(messagePromise);
    // ...
```

Вместо этого вызывайте `use` вне закрытий компонентов, если функция, вызывающая `use`, является компонентом или хуком.

```jsx
function MessageComponent({messagePromise}) {
  // ✅ `use` is being called from a component.
  const message = use(messagePromise);
  // ...
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/use](https://react.dev/reference/react/use)</small>
