# createFactory

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

`createFactory` позволяет вам создать функцию, которая производит элементы React заданного типа.

```js
const factory = createFactory(type);
```

## Описание

### `createFactory(type)`

Вызовите `createFactory(type)` для создания фабричной функции, которая производит элементы React заданного `типа`.

```js
import { createFactory } from 'react';

const button = createFactory('button');
```

Затем вы можете использовать его для создания элементов React без JSX:

```js
export default function App() {
    return button(
        {
            onClick: () => {
                alert('Clicked!');
            },
        },
        'Click me'
    );
}
```

#### Параметры

-   `type`: Аргумент `type` должен быть допустимым типом компонента React. Например, это может быть строка имени тега (например, `'div'` или `'span'`) или компонент React (функция, класс или специальный компонент типа [`Fragment`](Fragment.md)).

#### Возвращает

Возвращает фабричную функцию. Эта фабричная функция получает в качестве первого аргумента объект `props`, затем список аргументов `...children` и возвращает элемент React с заданными `type`, `props` и `children`.

## Использование

### Создание элементов React с помощью фабрики

Хотя большинство проектов React используют [JSX](../learn/writing-markup-with-jsx.md) для описания пользовательского интерфейса, JSX не обязателен. В прошлом `createFactory` был одним из способов описания пользовательского интерфейса без JSX.

Вызовите `createFactory`, чтобы создать _заводскую функцию_ для определенного типа элемента, например `'кнопка``:

```js
import { createFactory } from 'react';

const button = createFactory('button');
```

Вызов этой фабричной функции приведет к созданию элементов React с предоставленными вами реквизитами и дочерними элементами:

```js
import { createFactory } from 'react';

const button = createFactory('button');

export default function App() {
    return button(
        {
            onClick: () => {
                alert('Clicked!');
            },
        },
        'Click me'
    );
}
```

Так `createFactory` использовался в качестве альтернативы JSX. Однако `createFactory` устарел, и вы не должны вызывать `createFactory` в любом новом коде. О том, как отказаться от `createFactory`, читайте ниже.

## Альтернативы

### Копирование `createFactory` в ваш проект

Если в вашем проекте много вызовов `createFactory`, скопируйте эту реализацию `createFactory.js` в ваш проект:

=== "App.js"

    ```js
    import { createFactory } from './createFactory.js';

    const button = createFactory('button');

    export default function App() {
    	return button(
    		{
    			onClick: () => {
    				alert('Clicked!');
    			},
    		},
    		'Click me'
    	);
    }
    ```

=== "createFactory.js"

    ```js
    import { createElement } from 'react';

    export function createFactory(type) {
    	return createElement.bind(null, type);
    }
    ```

Это позволит вам сохранить весь ваш код неизменным, за исключением импорта.

### Замена `createFactory` на `createElement`

Если у вас есть несколько вызовов `createFactory`, которые вы не против перенести вручную, и вы не хотите использовать JSX, вы можете заменить каждый вызов функции фабрики вызовом [`createElement`](createElement.md). Например, вы можете заменить этот код:

```js
import { createFactory } from 'react';

const button = createFactory('button');

export default function App() {
    return button(
        {
            onClick: () => {
                alert('Clicked!');
            },
        },
        'Click me'
    );
}
```

с помощью этого кода:

```js
import { createElement } from 'react';

export default function App() {
    return createElement(
        'button',
        {
            onClick: () => {
                alert('Clicked!');
            },
        },
        'Click me'
    );
}
```

Вот полный пример использования React без JSX:

```js
import { createElement } from 'react';

export default function App() {
    return createElement(
        'button',
        {
            onClick: () => {
                alert('Clicked!');
            },
        },
        'Click me'
    );
}
```

### Замена `createFactory` на JSX

Наконец, вы можете использовать JSX вместо `createFactory`. Это наиболее распространенный способ использования React:

```js
export default function App() {
    return (
        <button
            onClick={() => {
                alert('Clicked!');
            }}
        >
            Click me
        </button>
    );
}
```

!!!warning ""

    Иногда существующий код может передавать некоторую переменную в качестве `type` вместо константы типа `'button'`:

    ```js
    function Heading({ isSubheading, ...props }) {
    	const type = isSubheading ? 'h2' : 'h1';
    	const factory = createFactory(type);
    	return factory(props);
    }
    ```

    Чтобы сделать то же самое в JSX, нужно переименовать переменную так, чтобы она начиналась с заглавной буквы, например `Type`:

    ```js
    function Heading({ isSubheading, ...props }) {
    	const Type = isSubheading ? 'h2' : 'h1';
    	return <Type {...props} />;
    }
    ```

    В противном случае React будет интерпретировать `<type>` как встроенный HTML-тег, поскольку он строчный.
