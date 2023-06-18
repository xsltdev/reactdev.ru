# createElement

Функция `createElement` позволяет создать элемент React. Он служит альтернативой написанию [JSX.](../learn/writing-markup-with-jsx.md)

```js
const element = createElement(type, props, ...children);
```

## Описание

### `createElement(type, props, ...children)`

Вызывает `createElement` для создания элемента React с заданными `type`, `props` и `children`.

```js
import { createElement } from 'react';

function Greeting({ name }) {
    return createElement(
        'h1',
        { className: 'greeting' },
        'Hello'
    );
}
```

#### Параметры

-   `type`: Аргумент `type` должен быть допустимым типом компонента React. Например, это может быть строка имени тега (например, `'div'` или `'span'`) или компонент React (функция, класс или специальный компонент типа [`Fragment`](Fragment.md)).
-   `props`: Аргумент `props` должен быть либо объектом, либо `null`. Если вы передадите `null`, он будет рассматриваться так же, как пустой объект. React создаст элемент с реквизитами, соответствующими переданным вами `props`. Обратите внимание, что `ref` и `key` из вашего объекта `props` являются специальными и _не_ будут доступны как `element.props.ref` и `element.props.key` в возвращаемом `element`. Они будут доступны как `element.ref` и `element.key`.
-   **опционально** `...children`: Ноль или более дочерних узлов. Это могут быть любые узлы React, включая элементы React, строки, числа, [порталы](createPortal.md), пустые узлы (`null`, `undefined`, `true` и `false`) и массивы узлов React.

#### Возвраты

`createElement` возвращает объект элемента React с несколькими свойствами:

-   `type`: `тип`, который вы передали.
-   `props`: Все `props`, которые вы передали, за исключением `ref` и `key`. Если `type` является компонентом с унаследованным `type.defaultProps`, то все отсутствующие или неопределенные `props` получат значения из `type.defaultProps`.
-   `ref`: Переданный вами `ref`. Если отсутствует, то `null`.
-   `key`: Переданный вами `key`, принудительно преобразованный в строку. Если отсутствует, то `null`.

Обычно вы возвращаете элемент из своего компонента или делаете его дочерним элементом другого элемента. Хотя вы можете читать свойства элемента, лучше всего рассматривать каждый элемент как непрозрачный после его создания и только отображать его.

#### Предостережения

-   Вы должны **обращаться с элементами React и их реквизитами как с [неизменяемыми](https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82)** и никогда не изменять их содержимое после создания. В процессе разработки React будет [замораживать](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze) возвращаемый элемент и его свойство `props` неглубоко, чтобы обеспечить это.
-   Когда вы используете JSX, **вы должны начинать тег с заглавной буквы для рендеринга вашего собственного компонента.** Другими словами, `<Something />` эквивалентно `createElement(Something)`, но `<something />` (в нижнем регистре) эквивалентно `createElement('something')` (обратите внимание, что это строка, поэтому она будет рассматриваться как встроенный HTML тег).
-   Вы должны **передавать дочерние элементы в качестве нескольких аргументов в `createElement`, только если они все статически известны,** например, `createElement('h1', {}, child1, child2, child3)`. Если дочерние элементы динамические, передайте весь массив в качестве третьего аргумента: `createElement('ul', {}, listItems)`. Это гарантирует, что React будет [предупреждать вас об отсутствии `ключей`](../learn/rendering-lists.md#keeping-list-items-in-order-with-key) для любых динамических списков. Для статических списков это не нужно, потому что они никогда не меняют порядок.

## Использование

### Создание элемента без JSX

Если вам не нравится [JSX](../learn/writing-markup-with-jsx.md) или вы не можете использовать его в своем проекте, вы можете использовать `createElement` в качестве альтернативы.

Чтобы создать элемент без JSX, вызовите `createElement` с некоторыми type, props и children:

```js [[1, 5, "'h1'"], [2, 6, "{ className: 'greeting' }"], [3, 7, "'Hello ',"], [3, 8, "createElement('i', null, name),"], [3, 9, "'. Welcome!'"]]
import { createElement } from 'react';

function Greeting({ name }) {
    return createElement(
        'h1',
        { className: 'greeting' },
        'Hello ',
        createElement('i', null, name),
        '. Welcome!'
    );
}
```

children необязательны, и вы можете передать столько дочерних элементов, сколько вам нужно (в приведенном выше примере их три). Этот код выведет заголовок `<h1>` с приветствием. Для сравнения, вот тот же пример, переписанный с помощью JSX:

```js
function Greeting({ name }) {
    return (
        <h1 className="greeting">
            Hello <i>{name}</i>. Welcome!
        </h1>
    );
}
```

Чтобы вывести собственный компонент React, передайте функцию типа `Greeting` в качестве type вместо строки типа `'h1'`:

```js
export default function App() {
    return createElement(Greeting, { name: 'Taylor' });
}
```

В JSX это будет выглядеть следующим образом:

```js
export default function App() {
    return <Greeting name="Taylor" />;
}
```

Вот полный пример, написанный с помощью `createElement`:

```js
import { createElement } from 'react';

function Greeting({ name }) {
    return createElement(
        'h1',
        { className: 'greeting' },
        'Hello ',
        createElement('i', null, name),
        '. Welcome!'
    );
}

export default function App() {
    return createElement(Greeting, { name: 'Taylor' });
}
```

А вот тот же пример, написанный с использованием JSX:

```js
function Greeting({ name }) {
    return (
        <h1 className="greeting">
            Hello <i>{name}</i>. Welcome!
        </h1>
    );
}

export default function App() {
    return <Greeting name="Taylor" />;
}
```

Оба стиля кодирования подходят, поэтому для своего проекта вы можете использовать тот, который вам больше нравится. Основное преимущество использования JSX по сравнению с `createElement` заключается в том, что легко увидеть, какой закрывающий тег соответствует какому открывающему тегу.

!!!note "Что такое React-элемент?"

    Элемент - это легкое описание части пользовательского интерфейса. Например, и `<Greeting name="Taylor" />`, и `createElement(Greeting, { name: 'Taylor' })` создают объект, подобный этому:

    ```js
    // Slightly simplified
    {
    	type: Greeting,
    	props: {
    		name: 'Taylor'
    	},
    	key: null,
    	ref: null,
    }
    ```

    **Обратите внимание, что при создании этого объекта компонент `Greeting` не отрисовывается и не создается никаких элементов DOM.**.

    Элемент React больше похож на описание - инструкцию для React по последующему рендерингу компонента `Greeting`. Возвращая этот объект из компонента `App`, вы указываете React, что делать дальше.

    Создание элементов чрезвычайно дешево, поэтому вам не нужно пытаться оптимизировать или избегать этого.
