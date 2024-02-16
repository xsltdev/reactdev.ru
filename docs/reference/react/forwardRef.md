# forwardRef

**`forwardRef`** позволяет вашему компоненту передать узел DOM родительскому компоненту с помощью [ref](../learn/manipulating-the-dom-with-refs.md).

```js
const SomeComponent = forwardRef(render);
```

## Описание

### `forwardRef(render)`

Вызовите `forwardRef()`, чтобы позволить вашему компоненту получить ссылку и переслать ее дочернему компоненту:

```js
import { forwardRef } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    // ...
});
```

**Параметры**

-   `render`: Функция рендеринга для вашего компонента. React вызывает эту функцию с props и `ref`, которые ваш компонент получил от своего родителя. JSX, который вы возвращаете, будет выходом вашего компонента.

**Возвращает**

`forwardRef` возвращает React-компонент, который вы можете отобразить в JSX. В отличие от компонентов React, определяемых как простые функции, компонент, возвращаемый `forwardRef`, также может принимать пропс `ref`.

**Предостережения**

-   В строгом режиме React будет **вызывать вашу функцию рендеринга дважды**, чтобы помочь вам найти случайные примеси. Это поведение только для разработчиков и не влияет на производство. Если ваша функция рендеринга чиста (как и должно быть), это не должно повлиять на логику вашего компонента. Результат одного из вызовов будет проигнорирован.

### `render` функция

`forwardRef` принимает функцию рендеринга в качестве аргумента. React вызывает эту функцию с `props` и `ref`:

```js
const MyInput = forwardRef(function MyInput(props, ref) {
    return (
        <label>
            {props.label}
            <input ref={ref} />
        </label>
    );
});
```

**Параметры**

-   `props`: Пропсы, переданные родительским компонентом.
-   `ref`: Атрибут `ref`, переданный родительским компонентом. Атрибут `ref` может быть объектом или функцией. Если родительский компонент не передал атрибут ref, он будет `null`. Вы должны либо передать полученный `ref` другому компоненту, либо передать его в [`useImperativeHandle`](useImperativeHandle.md).

**Возвращает**

`forwardRef` возвращает React-компонент, который вы можете отобразить в JSX. В отличие от компонентов React, определенных как простые функции, компонент, возвращаемый `forwardRef`, может принимать пропс `ref`.

## Использование

### Раскрытие узла DOM для родительского компонента

По умолчанию DOM-узлы каждого компонента являются приватными. Однако иногда полезно раскрыть узел DOM для родительского компонента - например, чтобы разрешить его фокусировку. Чтобы сделать это, оберните определение вашего компонента в `forwardRef()`:

```js
import { forwardRef } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    const { label, ...otherProps } = props;
    return (
        <label>
            {label}
            <input {...otherProps} />
        </label>
    );
});
```

Вы получите `ref` в качестве второго аргумента после props. Передайте его узлу DOM, который вы хотите раскрыть:

```js
import { forwardRef } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    const { label, ...otherProps } = props;
    return (
        <label>
            {label}
            <input {...otherProps} ref={ref} />
        </label>
    );
});
```

Это позволяет родительскому компоненту `Form` получить доступ к DOM-узлу `<input>`, открытому `MyInput`:

```js
function Form() {
    const ref = useRef(null);

    function handleClick() {
        ref.current.focus();
    }

    return (
        <form>
            <MyInput label="Enter your name:" ref={ref} />
            <button type="button" onClick={handleClick}>
                Edit
            </button>
        </form>
    );
}
```

Этот компонент `Form` [передает ссылку](useRef.md#manipulating-the-dom-with-a-ref) в `MyInput`. Компонент `MyInput` _передает_ эту ссылку в тег браузера `input`. В результате компонент `Form` может получить доступ к узлу DOM `input` и вызвать [`focus()`](https://developer.mozilla.org/docs/Web/API/HTMLElement/focus) для него.

Помните, что раскрытие ссылки на узел DOM внутри вашего компонента усложняет последующее изменение внутреннего устройства компонента. Обычно вы будете раскрывать узлы DOM из многократно используемых низкоуровневых компонентов, таких как кнопки или текстовые входы, но вы не будете делать этого для компонентов прикладного уровня, таких как аватар или комментарий.

### Примеры пересылки реферера

#### 1. Фокусировка текстового ввода

При нажатии на кнопку происходит фокусировка ввода. Компонент `Form` определяет ссылку и передает ее компоненту `MyInput`. Компонент `MyInput` передает эту ссылку браузеру `input`. Это позволяет компоненту `Form` сфокусировать `ввод`.

=== "App.js"

    ```js
    import { useRef } from 'react';
    import MyInput from './MyInput.js';

    export default function Form() {
    	const ref = useRef(null);

    	function handleClick() {
    		ref.current.focus();
    	}

    	return (
    		<form>
    			<MyInput label="Enter your name:" ref={ref} />
    			<button type="button" onClick={handleClick}>
    				Edit
    			</button>
    		</form>
    	);
    }
    ```

=== "MyInput.js"

    ```js
    import { forwardRef } from 'react';

    const MyInput = forwardRef(function MyInput(props, ref) {
    	const { label, ...otherProps } = props;
    	return (
    		<label>
    			{label}
    			<input {...otherProps} ref={ref} />
    		</label>
    	);
    });

    export default MyInput;
    ```

#### 2. Воспроизведение и приостановка видео

Нажатие на кнопку вызывает [`play()`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/play) и [`pause()`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/pause) на DOM-узле `<video>`. Компонент `App` определяет ссылку и передает ее компоненту `MyVideoPlayer`. Компонент `MyVideoPlayer` пересылает ссылку на узел `<video>` браузера. Это позволяет компоненту `App` воспроизводить и приостанавливать `<video>`.

=== "App.js"

    ```js
    import { useRef } from 'react';
    import MyVideoPlayer from './MyVideoPlayer.js';

    export default function App() {
    	const ref = useRef(null);
    	return (
    		<>
    			<button onClick={() => ref.current.play()}>
    				Play
    			</button>
    			<button onClick={() => ref.current.pause()}>
    				Pause
    			</button>
    			<br />
    			<MyVideoPlayer
    				ref={ref}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    				type="video/mp4"
    				width="250"
    			/>
    		</>
    	);
    }
    ```

=== "MyVideoPlayer.js"

    ```js
    import { forwardRef } from 'react';

    const VideoPlayer = forwardRef(function VideoPlayer(
    	{ src, type, width },
    	ref
    ) {
    	return (
    		<video width={width} ref={ref}>
    			<source src={src} type={type} />
    		</video>
    	);
    });

    export default VideoPlayer;
    ```

### Пересылка ссылки через несколько компонентов

Вместо пересылки `ref` на узел DOM, вы можете переслать его на свой собственный компонент, например `MyInput`:

```js
const FormField = forwardRef(function FormField(
    props,
    ref
) {
    // ...
    return (
        <>
            <MyInput ref={ref} />
            ...
        </>
    );
});
```

Если компонент `MyInput` передает ссылку на свой `<input>`, ссылка на `FormField` даст вам этот `<input>`:

```js
function Form() {
    const ref = useRef(null);

    function handleClick() {
        ref.current.focus();
    }

    return (
        <form>
            <FormField
                label="Enter your name:"
                ref={ref}
                isRequired={true}
            />
            <button type="button" onClick={handleClick}>
                Edit
            </button>
        </form>
    );
}
```

Компонент `Form` определяет ссылку и передает ее в `FormField`. Компонент `FormField` передает эту ссылку в `MyInput`, который передает ее в DOM-узел браузера `input`. Вот как `Form` получает доступ к этому DOM-узлу.

=== "App.js"

    ```js
    import { useRef } from 'react';
    import FormField from './FormField.js';

    export default function Form() {
    	const ref = useRef(null);

    	function handleClick() {
    		ref.current.focus();
    	}

    	return (
    		<form>
    			<FormField
    				label="Enter your name:"
    				ref={ref}
    				isRequired={true}
    			/>
    			<button type="button" onClick={handleClick}>
    				Edit
    			</button>
    		</form>
    	);
    }
    ```

=== "FormField.js"

    ```js
    import { forwardRef, useState } from 'react';
    import MyInput from './MyInput.js';

    const FormField = forwardRef(function FormField(
    	{ label, isRequired },
    	ref
    ) {
    	const [value, setValue] = useState('');
    	return (
    		<>
    			<MyInput
    				ref={ref}
    				label={label}
    				value={value}
    				onChange={(e) => setValue(e.target.value)}
    			/>
    			{isRequired && value === '' && <i>Required</i>}
    		</>
    	);
    });

    export default FormField;
    ```

=== "MyInput.js"

    ```js
    import { forwardRef } from 'react';

    const MyInput = forwardRef((props, ref) => {
    	const { label, ...otherProps } = props;
    	return (
    		<label>
    			{label}
    			<input {...otherProps} ref={ref} />
    		</label>
    	);
    });

    export default MyInput;
    ```

### Выставление императивного дескриптора вместо узла DOM

Вместо того чтобы раскрывать весь узел DOM, вы можете раскрыть пользовательский объект, называемый _императивным дескриптором_, с более ограниченным набором методов. Для этого вам нужно определить отдельный ref для хранения DOM-узла:

```js
const MyInput = forwardRef(function MyInput(props, ref) {
    const inputRef = useRef(null);

    // ...

    return <input {...props} ref={inputRef} />;
});
```

Передайте полученный `ref` в [`useImperativeHandle`](useImperativeHandle.md) и укажите значение, которое вы хотите передать `ref`:

```js
import {
    forwardRef,
    useRef,
    useImperativeHandle,
} from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    const inputRef = useRef(null);

    useImperativeHandle(
        ref,
        () => {
            return {
                focus() {
                    inputRef.current.focus();
                },
                scrollIntoView() {
                    inputRef.current.scrollIntoView();
                },
            };
        },
        []
    );

    return <input {...props} ref={inputRef} />;
});
```

Если какой-то компонент получит ссылку на `MyInput`, он получит только ваш объект `{ focus, scrollIntoView }` вместо узла DOM. Это позволяет вам ограничить информацию о вашем узле DOM до минимума.

=== "App.js"

    ```js
    import { useRef } from 'react';
    import MyInput from './MyInput.js';

    export default function Form() {
    	const ref = useRef(null);

    	function handleClick() {
    		ref.current.focus();
    		// This won't work because the DOM node isn't exposed:
    		// ref.current.style.opacity = 0.5;
    	}

    	return (
    		<form>
    			<MyInput label="Enter your name:" ref={ref} />
    			<button type="button" onClick={handleClick}>
    				Edit
    			</button>
    		</form>
    	);
    }
    ```

=== "MyInput.js"

    ```js
    import {
    	forwardRef,
    	useRef,
    	useImperativeHandle,
    } from 'react';

    const MyInput = forwardRef(function MyInput(props, ref) {
    	const inputRef = useRef(null);

    	useImperativeHandle(
    		ref,
    		() => {
    			return {
    				focus() {
    					inputRef.current.focus();
    				},
    				scrollIntoView() {
    					inputRef.current.scrollIntoView();
    				},
    			};
    		},
    		[]
    	);

    	return <input {...props} ref={inputRef} />;
    });

    export default MyInput;
    ```

[Подробнее об использовании императивных дескрипторов](useImperativeHandle.md)

!!!info ""

    **Не злоупотребляйте ссылками.** Ссылки следует использовать только для _императивного_ поведения, которое вы не можете выразить как пропс: например, прокрутка к узлу, фокусировка узла, запуск анимации, выделение текста и так далее.

    **Если вы можете выразить что-то как пропс, вы не должны использовать ссылку.** Например, вместо того, чтобы раскрывать императивный дескриптор типа `{ open, close }` из компонента `Modal`, лучше взять `isOpen` как пропс, например `<Modal isOpen={isOpen} />`. [Effects](../learn/synchronizing-with-effects.md) может помочь вам раскрыть императивное поведение через пропсы.

## Устранение неполадок

### Мой компонент обернут в `forwardRef`, но `реф` на него всегда `null`

Обычно это означает, что вы забыли использовать полученный `ref`.

Например, этот компонент ничего не делает со своим `ref`:

```js
const MyInput = forwardRef(function MyInput(
    { label },
    ref
) {
    return (
        <label>
            {label}
            <input />
        </label>
    );
});
```

Чтобы исправить это, передайте `ref` вниз к узлу DOM или другому компоненту, который может принимать ссылку:

```js
const MyInput = forwardRef(function MyInput(
    { label },
    ref
) {
    return (
        <label>
            {label}
            <input ref={ref} />
        </label>
    );
});
```

Ссылка `ref` на `MyInput` может также быть `null`, если некоторая логика является условной:

```js
const MyInput = forwardRef(function MyInput(
    { label, showInput },
    ref
) {
    return (
        <label>
            {label}
            {showInput && <input ref={ref} />}
        </label>
    );
});
```

Если `showInput` будет `false`, то ссылка не будет перенаправлена ни на какой узел, и ссылка на `MyInput` останется пустой. Это особенно легко пропустить, если условие скрыто внутри другого компонента, как `Panel` в этом примере:

```js
const MyInput = forwardRef(function MyInput(
    { label, showInput },
    ref
) {
    return (
        <label>
            {label}
            <Panel isExpanded={showInput}>
                <input ref={ref} />
            </Panel>
        </label>
    );
});
```

## Ссылки

-   [https://react.dev/reference/react/forwardRef](https://react.dev/reference/react/forwardRef)
