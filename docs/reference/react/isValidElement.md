---
status: deprecated
---

# isValidElement

`isValidElement` проверяет, является ли значение элементом React.

```js
const isElement = isValidElement(value);
```

## Описание

### `isValidElement(value)`

Вызовите `isValidElement(value)`, чтобы проверить, является ли `value` элементом React.

```js
import { isValidElement, createElement } from 'react';

// ✅ React elements
console.log(isValidElement(<p />)); // true
console.log(isValidElement(createElement('p'))); // true

// ❌ Not React elements
console.log(isValidElement(25)); // false
console.log(isValidElement('Hello')); // false
console.log(isValidElement({ age: 42 })); // false
```

**Параметры**

-   `value`: `value`, которое вы хотите проверить. Это может быть любое значение любого типа.

**Возвращает**

`isValidElement` возвращает `true`, если `value` является элементом React. В противном случае возвращается `false`.

**Ограничения**

-   **В качестве элементов React рассматриваются только [JSX-теги](../../learn/writing-markup-with-jsx.md) и объекты, возвращаемые [`createElement`](createElement.md).** Например, даже если число типа `42` является допустимым React _узлом_ (и может быть возвращено из компонента), оно не является допустимым элементом React. Массивы и порталы, созданные с помощью [`createPortal`](createPortal.md), также _не_ считаются элементами React.

## Использование

### Проверка, является ли что-то элементом React

Вызовите `isValidElement`, чтобы проверить, является ли некоторое значение _React-элементом_.

React-элементы - это:

-   Значения, создаваемые при написании [JSX-тега] (../../learn/writing-markup-with-jsx.md)
-   Значения, создаваемые вызовом [`createElement`](createElement.md)

Для элементов React функция `isValidElement` возвращает значение `true`:

```js
import { isValidElement, createElement } from 'react';

// ✅ JSX tags are React elements
console.log(isValidElement(<p />)); // true
console.log(isValidElement(<MyComponent />)); // true

// ✅ Values returned by createElement are React elements
console.log(isValidElement(createElement('p'))); // true
console.log(isValidElement(createElement(MyComponent))); // true
```

Любые другие значения, такие как строки, числа или произвольные объекты и массивы, не являются элементами React.

Для них `isValidElement` возвращает `false`:

```js
// ❌ These are *not* React elements
console.log(isValidElement(null)); // false
console.log(isValidElement(25)); // false
console.log(isValidElement('Hello')); // false
console.log(isValidElement({ age: 42 })); // false
console.log(isValidElement([<div />, <div />])); // false
console.log(isValidElement(MyComponent)); // false
```

Необходимость в `isValidElement` возникает крайне редко. В основном она полезна, если вы вызываете другой API, который _только_ принимает элементы (как это делает [`cloneElement`](cloneElement.md)), и вы хотите избежать ошибки, если ваш аргумент не является элементом React.

Если у вас нет какой-то очень специфической причины для добавления проверки `isValidElement`, она вам, вероятно, не нужна.

!!!note "React elements vs React nodes"

    Когда вы пишете компонент, вы можете вернуть из него любой тип _React-узла_:

    ```js
    function MyComponent() {
    	// ... you can return any React node ...
    }
    ```

    Узел React может быть:

    -   Элемент React, созданный как `div` или `createElement('div')`.
    -   Портал, созданный с помощью [`createPortal`](createPortal.md)
    -   строка
    -   число
    -   `true`, `false`, `null` или `undefined` (которые не отображаются)
    -   Массив других узлов React

    **Примечание: `isValidElement` проверяет, является ли аргумент _React-элементом,_ а не React-узлом.** Например, `42` не является допустимым React-элементом. Однако это вполне допустимый узел React:

    ```js
    function MyComponent() {
    	return 42; // It's ok to return a number from component
    }
    ```

    Вот почему вы не должны использовать `isValidElement` как способ проверить, можно ли что-то отобразить.
