---
description: useId - это хук React для генерации уникальных идентификаторов, которые могут быть переданы атрибутам доступности
---

# useId

<big>**`useId`** - это хук React для генерации уникальных идентификаторов, которые могут быть переданы атрибутам доступности.</big>

```js
const id = useId();
```

## Описание {#reference}

### `useId()` {#useid}

Вызовите `useId` на верхнем уровне вашего компонента для генерации уникального ID:

```js
import { useId } from 'react';

function PasswordField() {
    const passwordHintId = useId();
    // ...
}
```

#### Параметры {#parameters}

`useId` не принимает никаких параметров.

#### Возвращает {#returns}

`useId` возвращает уникальную строку ID, связанную с данным конкретным вызовом `useId` в данном конкретном компоненте.

#### Ограничения {#caveats}

-   `useId` - это хук, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, создайте новый компонент и переместите состояние в него.
-   `useId` **не должен использоваться для генерации ключей** в списке. [Ключи должны генерироваться из ваших данных](../../learn/rendering-lists.md#where-to-get-your-key).

## Использование {#usage}

!!!note "Генерация ключей в списке"

    **Не вызывайте `useId` для генерации ключей в списке.** Ключи должны [генерироваться из ваших данных](../../learn/rendering-lists.md#where-to-get-your-key).

### Генерация уникальных идентификаторов для атрибутов доступности {#generating-unique-ids-for-accessibility-attributes}

Вызовите `useId` на верхнем уровне вашего компонента для генерации уникального ID:

```js hl_lines="4"
import { useId } from 'react';

function PasswordField() {
    const passwordHintId = useId();
    // ...
}
```

Затем вы можете передать сгенерированный ID различным атрибутам:

```js
<>
  <input type="password" aria-describedby={passwordHintId} />
  <p id={passwordHintId}>
</>
```

**Давайте рассмотрим пример, чтобы увидеть, когда это полезно.**.

[Атрибуты доступности HTML](https://developer.mozilla.org/docs/Web/Accessibility/ARIA), такие как [`aria-describedby`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Attributes/aria-describedby), позволяют указать, что два тега связаны друг с другом. Например, вы можете указать, что элемент (например, input) описывается другим элементом (например, абзацем).

В обычном HTML вы бы написали это следующим образом:

```html hl_lines="5 8"
<label>
    Password:
    <input
        type="password"
        aria-describedby="password-hint"
    />
</label>
<p id="password-hint">
    The password should contain at least 18 characters
</p>
```

Однако жесткое кодирование идентификаторов подобным образом не является хорошей практикой в React. Компонент может отображаться на странице более одного раза - но идентификаторы должны быть уникальными! Вместо жесткого кодирования ID сгенерируйте уникальный ID с помощью `useId`:

```js hl_lines="4 11 14"
import { useId } from 'react';

function PasswordField() {
    const passwordHintId = useId();
    return (
        <>
            <label>
                Password:
                <input
                    type="password"
                    aria-describedby={passwordHintId}
                />
            </label>
            <p id={passwordHintId}>
                The password should contain at least 18
                characters
            </p>
        </>
    );
}
```

Теперь, даже если `PasswordField` появляется на экране несколько раз, сгенерированные идентификаторы не будут пересекаться.

=== "App.js"

    ```js
    import { useId } from 'react';

    function PasswordField() {
    	const passwordHintId = useId();
    	return (
    		<>
    			<label>
    				Password:
    				<input
    					type="password"
    					aria-describedby={passwordHintId}
    				/>
    			</label>
    			<p id={passwordHintId}>
    				The password should contain at least 18
    				characters
    			</p>
    		</>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<h2>Choose password</h2>
    			<PasswordField />
    			<h2>Confirm password</h2>
    			<PasswordField />
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gpd3t4?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

[Посмотрите это видео](https://www.youtube.com/watch?v=0dNzNcuEuOo), чтобы увидеть разницу в пользовательском опыте при использовании вспомогательных технологий.

!!!info "Серверный рендеринг"

    При [серверном рендеринге](../react-dom/server/index.md), **`useId` требует идентичного дерева компонентов на сервере и клиенте**. Если деревья, отрисованные на сервере и клиенте, не совпадают, сгенерированные идентификаторы не будут совпадать.

!!!note "Почему `useId` лучше, чем инкрементный счетчик?"

    Возможно, вам интересно, почему `useId` лучше, чем инкрементная глобальная переменная типа `nextId++`.

    Основное преимущество `useId` заключается в том, что React обеспечивает работу с [серверным рендерингом](../react-dom/server/index.md). Во время серверного рендеринга ваши компоненты генерируют HTML-вывод. Позже, на клиенте, [гидрация](../react-dom/client/hydrateRoot.md) присоединяет ваши обработчики событий к сгенерированному HTML. Чтобы гидрация работала, клиентский вывод должен совпадать с серверным HTML.

    Это очень трудно гарантировать с помощью увеличивающегося счетчика, потому что порядок, в котором клиентские компоненты гидратируются, может не совпадать с порядком, в котором был выдан серверный HTML. Вызывая `useId`, вы гарантируете, что гидратация будет работать, и вывод будет совпадать между сервером и клиентом.

    В React `useId` генерируется из "родительского пути" вызывающего компонента. Вот почему, если дерево клиента и сервера одинаково, "родительский путь" будет совпадать независимо от порядка рендеринга.

### Генерация идентификаторов для нескольких связанных элементов {#generating-ids-for-several-related-elements}

Если вам нужно присвоить идентификаторы нескольким связанным элементам, вы можете вызвать `useId`, чтобы сгенерировать для них общий префикс:

=== "App.js"

    ```js
    import { useId } from 'react';

    export default function Form() {
    	const id = useId();
    	return (
    		<form>
    			<label htmlFor={id + '-firstName'}>
    				First Name:
    			</label>
    			<input id={id + '-firstName'} type="text" />
    			<hr />
    			<label htmlFor={id + '-lastName'}>
    				Last Name:
    			</label>
    			<input id={id + '-lastName'} type="text" />
    		</form>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/s57ktn?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Это позволит вам избежать вызова `useId` для каждого отдельного элемента, которому нужен уникальный ID.

### Указание общего префикса для всех генерируемых идентификаторов {#specifying-a-shared-prefix-for-all-generated-ids}

Если вы отображаете несколько независимых приложений React на одной странице, передайте `identifierPrefix` в качестве опции в вызовы [`createRoot`](../react-dom/client/createRoot.md#parameters) или [`hydrateRoot`](../react-dom/client/hydrateRoot.md). Это гарантирует, что идентификаторы, сгенерированные двумя разными приложениями, никогда не столкнутся, потому что каждый идентификатор, сгенерированный с помощью `useId`, будет начинаться с определенного префикса, который вы указали.

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';
    import App from './App.js';
    import './styles.css';

    const root1 = createRoot(document.getElementById('root1'), {
    	identifierPrefix: 'my-first-app-',
    });
    root1.render(<App />);

    const root2 = createRoot(document.getElementById('root2'), {
    	identifierPrefix: 'my-second-app-',
    });
    root2.render(<App />);
    ```

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    	<head>
    		<title>My app</title>
    	</head>
    	<body>
    		<div id="root1"></div>
    		<div id="root2"></div>
    	</body>
    </html>
    ```

=== "App.js"

    ```js
    import { useId } from 'react';

    function PasswordField() {
    	const passwordHintId = useId();
    	console.log('Generated identifier:', passwordHintId);
    	return (
    		<>
    			<label>
    				Password:
    				<input
    					type="password"
    					aria-describedby={passwordHintId}
    				/>
    			</label>
    			<p id={passwordHintId}>
    				The password should contain at least 18
    				characters
    			</p>
    		</>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<h2>Choose password</h2>
    			<PasswordField />
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/zwjv48?view=Editor+%2B+Preview&module=%2Fsrc%2Findex.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Использование одного и того же префикса идентификатора на клиенте и сервере {#using-the-same-id-prefix-on-the-client-and-the-server}

Если вы [отображаете несколько независимых приложений React на одной странице](#specifying-a-shared-prefix-for-all-generated-ids), и некоторые из этих приложений рендерятся на сервере, убедитесь, что `identifierPrefix`, который вы передаете в вызов [`hydrateRoot`](../react-dom/client/hydrateRoot.md) на стороне клиента, совпадает с `identifierPrefix`, который вы передаете в [серверные API](../react-dom/server/index.md), такие как [`renderToPipeableStream`](../react-dom/server/renderToPipeableStream.md).

```js
// Server
import { renderToPipeableStream } from 'react-dom/server';

const { pipe } = renderToPipeableStream(<App />, {
    identifierPrefix: 'react-app1',
});
```

---

```js
// Client
import { hydrateRoot } from 'react-dom/client';

const domNode = document.getElementById('root');
const root = hydrateRoot(domNode, reactNode, {
    identifierPrefix: 'react-app1',
});
```

Вам не нужно передавать `identifierPrefix`, если на странице установлено только одно приложение React.

## Видео

<iframe width="100%" height="400px" src="https://www.youtube.com/embed/GNVI9Pr_RKQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useId](https://react.dev/reference/react/useId)</small>
