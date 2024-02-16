# useImperativeHandle

**`useImperativeHandle`** - это хук React, который позволяет вам настроить ручку, отображаемую как [ссылка](../learn/manipulating-the-dom-with-refs.md).

```js
useImperativeHandle(ref, createHandle, dependencies?)
```

## Описание

### `useImperativeHandle(ref, createHandle, dependencies?)`

Вызовите `useImperativeHandle` на верхнем уровне вашего компонента, чтобы настроить экспортируемый им ref handle:

```js
import { forwardRef, useImperativeHandle } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    useImperativeHandle(
        ref,
        () => {
            return {
                // ... your methods ...
            };
        },
        []
    );
    // ...
});
```

#### Параметры

-   `ref`: `ref`, полученный в качестве второго аргумента от функции рендеринга [`forwardRef`](forwardRef.md#render-function).
-   `createHandle`: Функция, которая не принимает аргументов и возвращает хэндл ссылки, которую вы хотите раскрыть. Этот ref handle может иметь любой тип. Обычно вы возвращаете объект с методами, которые вы хотите раскрыть.
-   **опционально** `dependencies`: Список всех реактивных значений, на которые ссылается код `createHandle`. Реактивные значения включают пропсы, состояние, а также все переменные и функции, объявленные непосредственно в теле вашего компонента. Если ваш линтер [настроен на React](../learn/editor-setup.md#linting), он проверит, что каждое реактивное значение правильно указано в качестве зависимости. Список зависимостей должен иметь постоянное количество элементов и быть написан inline по типу `[dep1, dep2, dep3]`. React будет сравнивать каждую зависимость с предыдущим значением, используя сравнение [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Если в результате повторного рендеринга изменилась какая-то зависимость, или если вы опустили этот аргумент, ваша функция `createHandle` будет повторно выполнена, и вновь созданный хэндл будет назначен ссылке.

#### Возвращает

Функция `useImperativeHandle` возвращает `undefined`.

## Использование

### Exposing a custom ref handle to the parent component

По умолчанию компоненты не открывают свои DOM-узлы родительским компонентам. Например, если вы хотите, чтобы родительский компонент `MyInput` имел [доступ](../learn/manipulating-the-dom-with-refs.md) к DOM-узлу `<input>`, вы должны выбрать [`forwardRef`:](forwardRef.md)

```js
import { forwardRef } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    return <input {...props} ref={ref} />;
});
```

С помощью приведенного выше кода [ссылка на `MyInput` получит DOM-узел `<input>`](forwardRef.md#exposing-a-dom-node-to-the-parent-component) Однако вместо этого вы можете выставить пользовательское значение. Чтобы настроить пользовательский дескриптор, вызовите `useImperativeHandle` на верхнем уровне вашего компонента:

```js
import { forwardRef, useImperativeHandle } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
    useImperativeHandle(
        ref,
        () => {
            return {
                // ... your methods ...
            };
        },
        []
    );

    return <input {...props} />;
});
```

Обратите внимание, что в приведенном выше коде `ref` больше не пересылается на `input`.

Например, предположим, что вы не хотите раскрывать весь DOM-узел `input`, но хотите раскрыть два его метода: `focus` и `scrollIntoView`. Для этого сохраните реальный DOM браузера в отдельном реферере. Затем используйте `useImperativeHandle`, чтобы раскрыть дескриптор только с теми методами, которые вы хотите, чтобы вызывал родительский компонент:

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

Теперь, если родительский компонент получит ссылку на `MyInput`, он сможет вызвать для него методы `focus` и `scrollIntoView`. Однако у него не будет полного доступа к лежащему в основе DOM-узлу `input`.

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

### Выставление собственных императивных методов

Методы, которые вы раскрываете через императивный дескриптор, не обязательно должны точно соответствовать методам DOM. Например, этот компонент `Post` раскрывает метод `scrollAndFocusAddComment` через императивный хэндл. Это позволяет родительской `Page` прокручивать список комментариев _и_ фокусировать поле ввода, когда вы нажимаете на кнопку:

=== "App.js"

    ```js
    import { useRef } from 'react';
    import Post from './Post.js';

    export default function Page() {
    	const postRef = useRef(null);

    	function handleClick() {
    		postRef.current.scrollAndFocusAddComment();
    	}

    	return (
    		<>
    			<button onClick={handleClick}>
    				Write a comment
    			</button>
    			<Post ref={postRef} />
    		</>
    	);
    }
    ```

=== "Post.js"

    ```js
    import {
    	forwardRef,
    	useRef,
    	useImperativeHandle,
    } from 'react';
    import CommentList from './CommentList.js';
    import AddComment from './AddComment.js';

    const Post = forwardRef((props, ref) => {
    	const commentsRef = useRef(null);
    	const addCommentRef = useRef(null);

    	useImperativeHandle(
    		ref,
    		() => {
    			return {
    				scrollAndFocusAddComment() {
    					commentsRef.current.scrollToBottom();
    					addCommentRef.current.focus();
    				},
    			};
    		},
    		[]
    	);

    	return (
    		<>
    			<article>
    				<p>Welcome to my blog!</p>
    			</article>
    			<CommentList ref={commentsRef} />
    			<AddComment ref={addCommentRef} />
    		</>
    	);
    });

    export default Post;
    ```

=== "CommentList.js"

    ```js
    import {
    	forwardRef,
    	useRef,
    	useImperativeHandle,
    } from 'react';

    const CommentList = forwardRef(function CommentList(
    	props,
    	ref
    ) {
    	const divRef = useRef(null);

    	useImperativeHandle(
    		ref,
    		() => {
    			return {
    				scrollToBottom() {
    					const node = divRef.current;
    					node.scrollTop = node.scrollHeight;
    				},
    			};
    		},
    		[]
    	);

    	let comments = [];
    	for (let i = 0; i < 50; i++) {
    		comments.push(<p key={i}>Comment #{i}</p>);
    	}

    	return (
    		<div className="CommentList" ref={divRef}>
    			{comments}
    		</div>
    	);
    });

    export default CommentList;
    ```

=== "AddComment.js"

    ```js
    import {
    	forwardRef,
    	useRef,
    	useImperativeHandle,
    } from 'react';

    const AddComment = forwardRef(function AddComment(
    	props,
    	ref
    ) {
    	return <input placeholder="Add comment..." ref={ref} />;
    });

    export default AddComment;
    ```

!!!note ""

    **Не злоупотребляйте ссылками.** Ссылки следует использовать только для _императивного_ поведения, которое вы не можете выразить как пропс: например, прокрутка к узлу, фокусировка узла, запуск анимации, выделение текста и так далее.

    **Если вы можете выразить что-то как пропс, вы не должны использовать ссылку.** Например, вместо того, чтобы раскрывать императивный дескриптор типа `{ open, close }` из компонента `Modal`, лучше взять `isOpen` как пропс, например `<Modal isOpen={isOpen} />`. [Effects](../learn/synchronizing-with-effects.md) может помочь вам раскрыть императивное поведение через пропсы.

## Ссылки

-   [https://react.dev/reference/react/useImperativeHandle](https://react.dev/reference/react/useImperativeHandle)
