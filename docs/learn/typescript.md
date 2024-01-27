---
description: TypeScript - это популярный способ добавления определений типов в кодовые базы JavaScript. Из коробки TypeScript поддерживает JSX, и вы можете получить полную поддержку React Web, добавив @types/react и @types/react-dom
---

# Использование TypeScript

<big>[TypeScript](https://scriptdev.ru/guide/) &mdash; это популярный способ добавления определений типов в кодовые базы JavaScript. Из коробки TypeScript [поддерживает JSX](./writing-markup-with-jsx.md), и вы можете получить полную поддержку React Web, добавив [`@types/react`](https://www.npmjs.com/package/@types/react) и [`@types/react-dom`](https://www.npmjs.com/package/@types/react-dom) в ваш проект.</big>

!!!tip "Вы узнаете"

    -   TypeScript с компонентами React
    -   Примеры типизации с помощью хуков
    -   Общие типы из `@types/react`
    -   Дополнительные источники обучения

## Установка {#installation}

Все [продуктовые React-фреймворки](./start-a-new-react-project.md#production-grade-react-frameworks) поддерживают использование TypeScript. Для установки следуйте руководству по конкретным фреймворкам:

-   [Next.js](https://nextjs.org/docs/pages/building-your-application/configuring/typescript)
-   [Remix](https://remix.run/docs/en/1.19.2/guides/typescript)
-   [Gatsby](https://www.gatsbyjs.com/docs/how-to/custom-configuration/typescript/)
-   [Expo](https://docs.expo.dev/guides/typescript/)

### Добавление TypeScript в существующий проект React {#adding-typescript-to-an-existing-react-project}

Чтобы установить последнюю версию определений типов React:

```sh linenums="0"
npm install @types/react @types/react-dom
```

В файле `tsconfig.json` необходимо установить следующие параметры компилятора:

1.  `dom` должен быть включен в [`lib`](https://www.typescriptlang.org/tsconfig/#lib) (Примечание: Если опция `lib` не указана, `dom` будет включен по умолчанию).
2.  Для параметра [`jsx`](https://www.typescriptlang.org/tsconfig/#jsx) должна быть установлена одна из допустимых опций. Для большинства приложений достаточно `preserve`.

    Если вы публикуете библиотеку, обратитесь к документации [`jsx`](https://www.typescriptlang.org/tsconfig/#jsx), чтобы узнать, какое значение выбрать.

## TypeScript с компонентами React {#typescript-with-react-components}

!!!note ""

    Каждый файл, содержащий JSX, должен использовать расширение `.tsx`. Это специфическое для TypeScript расширение, которое сообщает TypeScript, что этот файл содержит JSX.

Написание TypeScript на React очень похоже на написание JavaScript на React. Ключевое отличие при работе с компонентом заключается в том, что вы можете предоставлять типы для реквизитов компонента. Эти типы можно использовать для проверки корректности и создания встроенной документации в редакторах.

Взяв компонент [`MyButton`](index.md#components) из руководства [Быстрый старт](index.md), мы можем добавить тип, описывающий `title` для кнопки:

=== "App.tsx"

    ```ts
    function MyButton({ title }: { title: string }) {
    	return <button>{title}</button>;
    }

    export default function MyApp() {
    	return (
    		<div>
    			<h1>Welcome to my app</h1>
    			<MyButton title="I'm a button" />
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/2zgc9z?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Песочницы"

    Эти песочницы могут работать с кодом TypeScript, но в них не запускается программа проверки типов. Это означает, что вы можете использовать песочницы TypeScript для обучения, но не получите никаких ошибок или предупреждений о типах. Чтобы получить проверку типов, вы можете использовать [TypeScript Playground](https://www.typescriptlang.org/play) или воспользоваться более полнофункциональной онлайн-песочницей.

Этот встроенный синтаксис - самый простой способ предоставить типы для компонента, но когда у вас появляется несколько полей для описания, он может стать громоздким. Вместо этого вы можете использовать `interface` или `type` для описания свойств компонента:

=== "App.tsx"

    ```ts
    interface MyButtonProps {
    	/** The text to display inside the button */
    	title: string;
    	/** Whether the button can be interacted with */
    	disabled: boolean;
    }

    function MyButton({ title, disabled }: MyButtonProps) {
    	return <button disabled={disabled}>{title}</button>;
    }

    export default function MyApp() {
    	return (
    		<div>
    			<h1>Welcome to my app</h1>
    			<MyButton
    				title="I'm a disabled button"
    				disabled={true}
    			/>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/85jjnx?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Тип, описывающий свойства вашего компонента, может быть простым или сложным, как вам нужно, но они должны быть объектным типом, описанным с помощью `type` или `interface`. Вы можете узнать о том, как TypeScript описывает объекты в [Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html), но вам также может быть интересно использовать [Union Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types) для описания свойства, которое может быть одним из нескольких различных типов, и руководство [Creating Types from Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html) для более сложных случаев использования.

## Примеры хуков {#example-hooks}

Определения типов из `@types/react` включают типы для встроенных хуков, так что вы можете использовать их в своих компонентах без дополнительных настроек. Они созданы с учетом кода, который вы пишете в своем компоненте, поэтому вы будете получать [выведенные типы](https://www.typescriptlang.org/docs/handbook/type-inference.html) большую часть времени, и в идеале вам не нужно будет заниматься тонкостями создания типов.

Тем не менее, мы можем рассмотреть несколько примеров того, как задавать типы для хуков.

### `useState` {#typing-usestate}

Хук [`useState`](../reference/useState.md) повторно использует значение, переданное в качестве начального состояния, чтобы определить, каким должен быть тип этого значения. Например:

```ts
// Infer the type as "boolean"
const [enabled, setEnabled] = useState(false);
```

присвоит `enabled` тип `boolean`, а `setEnabled` будет функцией, принимающей либо аргумент `boolean`, либо функцию, возвращающую `boolean`. Если вы хотите явно указать тип состояния, вы можете сделать это, указав тип аргумента в вызове `useState`:

```ts
// Explicitly set the type to "boolean"
const [enabled, setEnabled] = useState<boolean>(false);
```

В данном случае это не очень полезно, но часто тип может потребоваться, если у вас есть тип объединения. Например, `status` здесь может быть одной из нескольких различных строк:

```ts
type Status = 'idle' | 'loading' | 'success' | 'error';

const [status, setStatus] = useState<Status>('idle');
```

Или, как рекомендуется в [Принципах структурирования состояния](./choosing-the-state-structure.md#principles-for-structuring-state), вы можете сгруппировать связанные состояния как объект и описать различные возможности с помощью типов объектов:

```ts
type RequestState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: any }
    | { status: 'error'; error: Error };

const [requestState, setRequestState] = useState<
    RequestState
>({ status: 'idle' });
```

### `useReducer` {#typing-usereducer}

Хук [`useReducer`](../reference/useReducer.md) - это более сложный хук, который принимает функцию редуктора и начальное состояние. Типы для функции редуктора выводятся из начального состояния. Вы можете указать тип в аргументе в вызове `useReducer`, чтобы задать тип для состояния, но часто лучше установить тип в начальном состоянии:

=== "App.tsx"

    ```ts
    import { useReducer } from 'react';

    interface State {
    	count: number;
    }

    type CounterAction =
    	| { type: 'reset' }
    	| { type: 'setCount'; value: State['count'] };

    const initialState: State = { count: 0 };

    function stateReducer(
    	state: State,
    	action: CounterAction
    ): State {
    	switch (action.type) {
    		case 'reset':
    			return initialState;
    		case 'setCount':
    			return { ...state, count: action.value };
    		default:
    			throw new Error('Unknown action');
    	}
    }

    export default function App() {
    	const [state, dispatch] = useReducer(
    		stateReducer,
    		initialState
    	);

    	const addFive = () =>
    		dispatch({
    			type: 'setCount',
    			value: state.count + 5,
    		});
    	const reset = () => dispatch({ type: 'reset' });

    	return (
    		<div>
    			<h1>Welcome to my counter</h1>

    			<p>Count: {state.count}</p>
    			<button onClick={addFive}>Add 5</button>
    			<button onClick={reset}>Reset</button>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gvhjwv?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Мы используем TypeScript в нескольких ключевых местах:

-   `interface State` описывает форму состояния редуктора.
-   `type CounterAction` описывает различные действия, которые могут быть отправлены редуктору.
-   `const initialState: State` предоставляет тип для начального состояния, а также тип, который используется `useReducer` по умолчанию.
-   `stateReducer(state: State, action: CounterAction): State` устанавливает типы для аргументов и возвращаемого значения функции reducer.

Более явной альтернативой установке типа в `initialState` является предоставление аргумента типа в `useReducer`:

```ts
import {
    stateReducer,
    State,
} from './your-reducer-implementation';

const initialState = { count: 0 };

export default function App() {
    const [state, dispatch] = useReducer<State>(
        stateReducer,
        initialState
    );
}
```

### `useContext` {#typing-usecontext}

Хук [`useContext`](../reference/useContext.md) - это техника передачи данных по дереву компонентов без необходимости передавать реквизиты через компоненты. Она используется при создании компонента-провайдера и часто при создании хука для потребления значения в дочернем компоненте.

Тип значения, предоставляемого контекстом, выводится из значения, переданного в вызове `createContext`:

=== "App.tsx"

    ```ts
    import { createContext, useContext, useState } from 'react';

    type Theme = 'light' | 'dark' | 'system';
    const ThemeContext = createContext<Theme>('system');

    const useGetTheme = () => useContext(ThemeContext);

    export default function MyApp() {
    	const [theme, setTheme] = useState<Theme>('light');

    	return (
    		<ThemeContext.Provider value={theme}>
    			<MyComponent />
    		</ThemeContext.Provider>
    	);
    }

    function MyComponent() {
    	const theme = useGetTheme();

    	return (
    		<div>
    			<p>Current theme: {theme}</p>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/jwv9y3?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Эта техника работает, когда у вас есть значение по умолчанию, которое имеет смысл - но иногда бывают случаи, когда это не так, и в этих случаях `null` может показаться разумным значением по умолчанию. Однако, чтобы система типов могла понять ваш код, вам нужно явно установить `ContextShape | null` в `createContext`.

Это приводит к тому, что вам нужно исключить `| null` в типе для потребителей контекста. Мы рекомендуем, чтобы хук выполнял проверку на существование этого типа во время выполнения и выбрасывал ошибку при его отсутствии:

```js hl_lines="15 20-23"
import {
    createContext,
    useContext,
    useState,
    useMemo,
} from 'react';

// This is a simpler example, but you can
// imagine a more complex object here
type ComplexObject = {
    kind: string,
};

// The context is created with `| null` in the type,
// to accurately reflect the default value.
const Context =
    (createContext < ComplexObject) | (null > null);

// The `| null` will be removed via the check in the Hook.
const useGetComplexObject = () => {
    const object = useContext(Context);
    if (!object) {
        throw new Error(
            'useGetComplexObject must be used within a Provider'
        );
    }
    return object;
};

export default function MyApp() {
    const object = useMemo(() => ({ kind: 'complex' }), []);

    return (
        <Context.Provider value={object}>
            <MyComponent />
        </Context.Provider>
    );
}

function MyComponent() {
    const object = useGetComplexObject();

    return (
        <div>
            <p>Current object: {object.kind}</p>
        </div>
    );
}
```

### `useMemo` {#typing-usememo}

Хуки [`useMemo`](../reference/useMemo.md) создают/восстанавливают доступ к запомненному значению из вызова функции, перезапуская функцию только при изменении зависимостей, переданных в качестве второго параметра. Результат вызова хука определяется по возвращаемому значению функции в первом параметре. Вы можете быть более явными, указав аргумент типа в Hook.

```ts
// The type of visibleTodos is inferred from
// the return value of filterTodos
const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
);
```

### `useCallback` {#typing-usecallback}

[`useCallback`](../reference/useCallback.md) обеспечивают стабильную ссылку на функцию, пока зависимости, переданные во втором параметре, одинаковы. Как и в `useMemo`, тип функции определяется по возвращаемому значению функции в первом параметре, но вы можете быть более явными, указав аргумент типа в Hook.

```ts
const handleClick = useCallback(() => {
    // ...
}, [todos]);
```

При работе в строгом режиме TypeScript `useCallback` требует добавления типов для параметров обратного вызова. Это связано с тем, что тип обратного вызова выводится из возвращаемого значения функции, а без параметров тип не может быть полностью понят.

В зависимости от ваших предпочтений в стиле кода, вы можете использовать функции `*EventHandler` из типов React, чтобы задать тип обработчика события одновременно с определением обратного вызова:

```ts
import { useState, useCallback } from 'react';

export default function Form() {
    const [value, setValue] = useState('Change me');

    const handleChange = useCallback<
        React.ChangeEventHandler<HTMLInputElement>
    >(
        (event) => {
            setValue(event.currentTarget.value);
        },
        [setValue]
    );

    return (
        <>
            <input value={value} onChange={handleChange} />
            <p>Value: {value}</p>
        </>
    );
}
```

## Полезные типы {#useful-types}

Существует довольно обширный набор типов из пакета `@types/react`, его стоит прочитать, когда вы почувствуете, как взаимодействуют React и TypeScript. Вы можете найти их [в папке React в DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/react/index.d.ts). Здесь мы рассмотрим несколько наиболее распространенных типов.

### События DOM {#typing-dom-events}

При работе с событиями DOM в React тип события часто можно определить из обработчика события. Однако, если вы хотите извлечь функцию, которая будет передана обработчику события, вам нужно будет явно задать тип события.

=== "App.tsx"

    ```ts
    import { useState } from 'react';

    export default function Form() {
    	const [value, setValue] = useState('Change me');

    	function handleChange(
    		event: React.ChangeEvent<HTMLInputElement>
    	) {
    		setValue(event.currentTarget.value);
    	}

    	return (
    		<>
    			<input value={value} onChange={handleChange} />
    			<p>Value: {value}</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/r6dz5p?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В типах React предусмотрено множество типов событий - полный список можно найти [здесь](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/b580df54c0819ec9df62b0835a315dd48b8594a9/types/react/index.d.ts#L1247C1-L1373), который основан на [наиболее популярных событиях из DOM](https://developer.mozilla.org/docs/Web/Events).

При определении нужного типа вы можете сначала посмотреть на hover-информацию для используемого обработчика события, которая покажет тип события.

Если вам нужно использовать событие, которое не включено в этот список, вы можете использовать тип `React.SyntheticEvent`, который является базовым типом для всех событий.

### `Children` {#typing-children}

Существует два общих способа описания дочерних элементов компонента. Первый - использовать тип `React.ReactNode`, который представляет собой объединение всех возможных типов, которые могут быть переданы в качестве дочерних в JSX:

```ts
interface ModalRendererProps {
    title: string;
    children: React.ReactNode;
}
```

Это очень широкое определение детей. Второе - использовать тип `React.ReactElement`, который относится только к элементам JSX, а не к примитивам JavaScript вроде строк или чисел:

```ts
interface ModalRendererProps {
    title: string;
    children: React.ReactElement;
}
```

Обратите внимание, что вы не можете использовать TypeScript для описания того, что дочерние элементы являются определенным типом JSX-элементов, поэтому вы не можете использовать систему типов для описания компонента, который принимает только `<li>` дочерние элементы.

Вы можете увидеть все примеры как `React.ReactNode`, так и `React.ReactElement` с проверкой типов в [этой площадке TypeScript](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgIilQ3wChSB6CxYmAOmXRgDkIATJOdNJMGAZzgwAFpxAR+8YADswAVwGkZMJFEzpOjDKw4AFHGEEBvUnDhphwADZsi0gFw0mDWjqQBuUgF9yaCNMlENzgAXjgACjADfkctFnYkfQhDAEpQgD44AB42YAA3dKMo5P46C2tbJGkvLIpcgt9-QLi3AEEwMFCItJDMrPTTbIQ3dKywdIB5aU4kKyQQKpha8drhhIGzLLWODbNs3b3s8YAxKBQAcwXpAThMaGWDvbH0gFloGbmrgQfBzYpd1YjQZbEYARkB6zMwO2SHSAAlZlYIBCdtCRkZpHIrFYahQYQD8UYYFA5EhcfjyGYqHAXnJAsIUHlOOUbHYhMIIHJzsI0Qk4P9SLUBuRqXEXEwAKKfRZcNA8PiCfxWACecAAUgBlAAacFm80W-CU11U6h4TgwUv11yShjgJjMLMqDnN9Dilq+nh8pD8AXgCHdMrCkWisVoAet0R6fXqhWKhjKllZVVxMcavpd4Zg7U6Qaj+2hmdG4zeRF10uu-Aeq0LBfLMEe-V+T2L7zLVu+FBWLdLeq+lc7DYFf39deFVOotMCACNOCh1dq219a+30uC8YWoZsRyuEdjkevR8uvoVMdjyTWt4WiSSydXD4NqZP4AymeZE072ZzuUeZQKheQgA).

### Свойства стиля {#typing-style-props}

При использовании встроенных стилей в React вы можете использовать `React.CSSProperties` для описания объекта, передаваемого в реквизит `style`. Этот тип представляет собой объединение всех возможных CSS-свойств и является хорошим способом убедиться, что вы передаете действительные CSS-свойства в реквизит `style`, а также получить автозаполнение в вашем редакторе.

```ts
interface MyComponentProps {
    style: React.CSSProperties;
}
```

## Дальнейшее обучение {#further-learning}

В этом руководстве мы рассмотрели основы использования TypeScript с React, но вам предстоит узнать еще много нового. Отдельные страницы API в документации могут содержать более подробную документацию о том, как использовать их с TypeScript.

Мы рекомендуем следующие ресурсы:

-   [The TypeScript handbook](https://www.typescriptlang.org/docs/handbook/) - официальная документация по TypeScript, охватывающая большинство ключевых возможностей языка.

-   [The TypeScript release notes](https://devblogs.microsoft.com/typescript/) подробно рассказывает о каждой новой функции.

-   [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/) - это поддерживаемая сообществом шпаргалка по использованию TypeScript с React, охватывающая множество полезных крайних случаев и предоставляющая более широкую информацию, чем этот документ.

-   [TypeScript Community Discord](https://discord.com/invite/typescript) - отличное место, где можно задать вопросы и получить помощь по проблемам TypeScript и React.

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/typescript](https://react.dev/learn/typescript)</small>
