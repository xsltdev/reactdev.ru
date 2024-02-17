---
status: deprecated
---

# createRef

!!!warning ""

    `createRef` в основном используется для [компонентов класса](Component.md). Функциональные компоненты обычно полагаются на [`useRef`](useRef.md).

`createRef` создает объект [ref](../learn/referencing-values-with-refs.md), который может содержать произвольное значение.

<!-- 0001.part.md -->

```js
class MyInput extends Component {
    inputRef = createRef();
    // ...
}
```

<!-- 0002.part.md -->

## Описание

### `createRef()`

Вызовите `createRef` для объявления [ссылки](../learn/referencing-values-with-refs.md) внутри [компонента класса.](Component.md)

<!-- 0003.part.md -->

```js
import { createRef, Component } from 'react';

class MyComponent extends Component {
    intervalRef = createRef();
    inputRef = createRef();
    // ...
}
```

#### Параметры

`createRef` не принимает никаких параметров.

#### Возвращает

`createRef` возвращает объект с одним свойством:

-   `current`: Изначально оно установлено в `null`. Позже вы можете установить его в другое значение. Если вы передадите объект ref в React как атрибут `ref` узла JSX, React установит его свойство `current`.

#### Предостережения

-   `createRef` всегда возвращает _различный_ объект. Это эквивалентно написанию `{ current: null }` самостоятельно.
-   В компоненте функции, вероятно, вместо этого вам нужен [`useRef`](useRef.md), который всегда возвращает один и тот же объект.
-   `const ref = useRef()` эквивалентно `const [ref, _] = useState(() => createRef(null))`.

## Использование

### Объявление ссылки в компоненте класса

Чтобы объявить реф внутри [компонента класса,](Component.md) вызовите `createRef` и присвойте его результат полю класса:

<!-- 0005.part.md -->

```js
import { Component, createRef } from 'react';

class Form extends Component {
    inputRef = createRef();

    // ...
}
```

<!-- 0006.part.md -->

Если теперь вы передадите `ref={this.inputRef}` к `<input>` в вашем JSX, React заполнит `this.inputRef.current` входным DOM-узлом. Например, вот как сделать кнопку, которая фокусирует ввод:

<!-- 0007.part.md -->

```js
import { Component, createRef } from 'react';

export default class Form extends Component {
    inputRef = createRef();

    handleClick = () => {
        this.inputRef.current.focus();
    };

    render() {
        return (
            <>
                <input ref={this.inputRef} />
                <button onClick={this.handleClick}>
                    Focus the input
                </button>
            </>
        );
    }
}
```

<!-- 0008.part.md -->

`createRef` в основном используется для [компонентов класса.](Component.md) Функциональные компоненты обычно полагаются на [`useRef`](useRef.md).

## Альтернативы

### Переход от класса с `createRef` к функции с `useRef`

Мы рекомендуем использовать компоненты функций вместо [компонентов классов](Component.md) в новом коде. Если у вас есть некоторые существующие компоненты классов, использующие `createRef`, вот как их можно преобразовать. Это оригинальный код:

<!-- 0009.part.md -->

```js
import { Component, createRef } from 'react';

export default class Form extends Component {
    inputRef = createRef();

    handleClick = () => {
        this.inputRef.current.focus();
    };

    render() {
        return (
            <>
                <input ref={this.inputRef} />
                <button onClick={this.handleClick}>
                    Focus the input
                </button>
            </>
        );
    }
}
```

<!-- 0010.part.md -->

Когда вы [преобразуете этот компонент из класса в функцию,](Component.md) замените вызовы `createRef` на вызовы [`useRef`:](useRef.md)

<!-- 0011.part.md -->

```js
import { useRef } from 'react';

export default function Form() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <input ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

## Ссылки

-   [https://react.dev/reference/react/createRef](https://react.dev/reference/react/createRef)
