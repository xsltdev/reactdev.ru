---
description: Описание функции cloneElement из устаревшего API React
status: deprecated
---

# cloneElement

!!!warning ""

    Использование `cloneElement` встречается редко и может привести к нестабильности кода. [См. распространенные альтернативы.](#alternatives)

`cloneElement` позволяет создать новый элемент React, используя другой элемент в качестве отправной точки.

```js
const clonedElement = cloneElement(
    element,
    props,
    ...children
);
```

## Описание {#reference}

### **`cloneElement(element, props, ...children)`** {#cloneelement}

Вызовите `cloneElement` для создания элемента React, основанного на `element`, но с различными `props` и `children`:

```js
import { cloneElement } from 'react';

// ...
const clonedElement = cloneElement(
    <Row title="Cabbage">Hello</Row>,
    { isHighlighted: true },
    'Goodbye'
);

console.log(clonedElement); // <Row title="Cabbage">Goodbye</Row>
```

#### Параметры {#parameters}

-   `element`: Аргумент `element` должен быть действительным элементом React. Например, это может быть JSX-узел типа `<Something />`, результат вызова [`createElement`](createElement.md) или результат другого вызова `cloneElement`.
-   `props`: Аргумент `props` должен быть либо объектом, либо `null`. Если вы передадите `null`, клонированный элемент сохранит все исходные `element.props`. В противном случае для каждого пропса в объекте `props` возвращаемый элемент "предпочтет" значение из `props` значению из `element.props`. Остальные пропсы будут заполнены из исходного `element.props`. Если вы передадите `props.key` или `props.ref`, они заменят исходные.
-   **опционально** `...children`: Ноль или более дочерних узлов. Это могут быть любые узлы React, включая элементы React, строки, числа, [порталы](../react-dom/createPortal.md), пустые узлы (`null`, `undefined`, `true` и `false`) и массивы узлов React. Если вы не передадите никаких аргументов `...children`, исходные `element.props.children` будут сохранены.

#### Возвращает {#returns}

`cloneElement` возвращает объект React element с несколькими свойствами:

-   `type`: Такой же, как `element.type`.
-   `props`: Результат неглубокого слияния `element.props` с переданными вам переопределяющими `props`.
-   `ref`: Оригинальный `element.ref`, если только он не был переопределен `props.ref`.
-   `key`: Оригинальный `element.key`, если он не был переопределен `props.key`.

Обычно вы возвращаете элемент из своего компонента или делаете его дочерним элементом другого элемента. Хотя вы можете читать свойства элемента, лучше всего рассматривать каждый элемент как непрозрачный после его создания и только отображать его.

#### Предостережения {#caveats}

-   Клонирование элемента **не изменяет исходный элемент.**
-   Вы должны **передавать дочерние элементы в качестве нескольких аргументов `cloneElement`, только если они все статически известны,** например, `cloneElement(element, null, child1, child2, child3)`. Если ваши дочерние элементы динамические, передайте весь массив в качестве третьего аргумента: `cloneElement(element, null, listItems)`. Это гарантирует, что React [предупредит вас об отсутствии `ключей`](../../learn/rendering-lists.md#keeping-list-items-in-order-with-key) для любых динамических списков. Для статических списков это не нужно, потому что они никогда не меняют порядок.
-   `cloneElement` затрудняет отслеживание потока данных, поэтому **вместо этого попробуйте [альтернативы](#alternatives).**

## Использование {#usage}

### Переопределение пропсов элемента {#overriding-props-of-an-element}

Чтобы переопределить пропсы некоторого реактивного элемента, передайте его в `cloneElement` с пропсами, которые вы хотите переопределить:

```js
import { cloneElement } from 'react';

// ...
const clonedElement = cloneElement(
    <Row title="Cabbage" />,
    { isHighlighted: true }
);
```

Здесь результирующим клонированным элементом будет `<Row title="Cabbage" isHighlighted={true} />`.

**Давайте рассмотрим пример, чтобы увидеть, когда это полезно.**.

Представьте себе компонент `List`, который отображает своих [`детей`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children) как список выбираемых строк с кнопкой "Next", которая изменяет выбранную строку. Компонент `List` должен отображать выбранный `Row` по-разному, поэтому он клонирует каждый дочерний `<Row>`, который он получил, и добавляет дополнительный параметр `isHighlighted: true` или `isHighlighted: false`:

```js
export default function List({ children }) {
    const [selectedIndex, setSelectedIndex] = useState(0);
    return (
        <div className="List">
            {Children.map(children, (child, index) =>
                cloneElement(child, {
                    isHighlighted: index === selectedIndex,
                })
            )}
        </div>
    );
}
```

Допустим, исходный JSX, полученный `List`, выглядит следующим образом:

```js
<List>
    <Row title="Cabbage" />
    <Row title="Garlic" />
    <Row title="Apple" />
</List>
```

Клонируя свои дочерние элементы, `List` может передавать дополнительную информацию каждому `Row` внутри. Результат выглядит следующим образом:

```js
<List>
    <Row title="Cabbage" isHighlighted={true} />
    <Row title="Garlic" isHighlighted={false} />
    <Row title="Apple" isHighlighted={false} />
</List>
```

Обратите внимание, как нажатие кнопки "Next" обновляет состояние `List` и выделяет другую строку:

=== "App.js"

    ```js
    import List from './List.js';
    import Row from './Row.js';
    import { products } from './data.js';

    export default function App() {
    	return (
    		<List>
    			{products.map((product) => (
    				<Row
    					key={product.id}
    					title={product.title}
    				/>
    			))}
    		</List>
    	);
    }
    ```

=== "List.js"

    ```js
    import { Children, cloneElement, useState } from 'react';

    export default function List({ children }) {
    	const [selectedIndex, setSelectedIndex] = useState(0);
    	return (
    		<div className="List">
    			{Children.map(children, (child, index) =>
    				cloneElement(child, {
    					isHighlighted: index === selectedIndex,
    				})
    			)}
    			<hr />
    			<button
    				onClick={() => {
    					setSelectedIndex(
    						(i) =>
    							(i + 1) %
    							Children.count(children)
    					);
    				}}
    			>
    				Next
    			</button>
    		</div>
    	);
    }
    ```

=== "Row.js"

    ```js
    export default function Row({ title, isHighlighted }) {
    	return (
    		<div
    			className={[
    				'Row',
    				isHighlighted ? 'RowHighlighted' : '',
    			].join(' ')}
    		>
    			{title}
    		</div>
    	);
    }
    ```

=== "data.js"

    ```js
    export const products = [
    	{ title: 'Cabbage', id: 1 },
    	{ title: 'Garlic', id: 2 },
    	{ title: 'Apple', id: 3 },
    ];
    ```

Короче говоря, `List` клонирует полученные элементы `<Row />` и добавляет к ним дополнительный пропс.

!!!warning ""

    При клонировании детей трудно определить, как данные проходят через ваше приложение. Попробуйте один из [альтернативных вариантов](#alternatives).

## Альтернативы {#alternatives}

### Передача данных с пропсом рендеринга {#passing-data-with-a-render-prop}

Вместо того чтобы использовать `cloneElement`, подумайте о том, чтобы принимать _render prop_, например `renderItem`. Здесь `List` принимает `renderItem` в качестве пропса. `List` вызывает `renderItem` для каждого элемента и передает `isHighlighted` в качестве аргумента:

```js
export default function List({ items, renderItem }) {
    const [selectedIndex, setSelectedIndex] = useState(0);
    return (
        <div className="List">
            {items.map((item, index) => {
                const isHighlighted =
                    index === selectedIndex;
                return renderItem(item, isHighlighted);
            })}
        </div>
    );
}
```

Пропс `renderItem` называют "пропсом рендеринга", потому что он определяет, как рендерить что-либо. Например, вы можете передать реализацию `renderItem`, которая рендерит `<Row>` с заданным значением `isHighlighted`:

```js
<List
    items={products}
    renderItem={(product, isHighlighted) => (
        <Row
            key={product.id}
            title={product.title}
            isHighlighted={isHighlighted}
        />
    )}
/>
```

Конечный результат такой же, как и при использовании `cloneElement`:

```js
<List>
    <Row title="Cabbage" isHighlighted={true} />
    <Row title="Garlic" isHighlighted={false} />
    <Row title="Apple" isHighlighted={false} />
</List>
```

Однако вы можете четко проследить, откуда берется значение `isHighlighted`.

=== "App.js"

    ```js
    import List from './List.js';
    import Row from './Row.js';
    import { products } from './data.js';

    export default function App() {
        return (
            <List
                items={products}
                renderItem={(product, isHighlighted) => (
                    <Row
                        key={product.id}
                        title={product.title}
                        isHighlighted={isHighlighted}
                    />
                )}
            />
        );
    }
    ```

=== "List.js"

    ```js
    import { useState } from 'react';

    export default function List({ items, renderItem }) {
    	const [selectedIndex, setSelectedIndex] = useState(0);
    	return (
    		<div className="List">
    			{items.map((item, index) => {
    				const isHighlighted =
    					index === selectedIndex;
    				return renderItem(item, isHighlighted);
    			})}
    			<hr />
    			<button
    				onClick={() => {
    					setSelectedIndex(
    						(i) => (i + 1) % items.length
    					);
    				}}
    			>
    				Next
    			</button>
    		</div>
    	);
    }
    ```

=== "Row.js"

    ```js
    export default function Row({ title, isHighlighted }) {
    	return (
    		<div
    			className={[
    				'Row',
    				isHighlighted ? 'RowHighlighted' : '',
    			].join(' ')}
    		>
    			{title}
    		</div>
    	);
    }
    ```

=== "data.js"

    ```js
    export const products = [
    	{ title: 'Cabbage', id: 1 },
    	{ title: 'Garlic', id: 2 },
    	{ title: 'Apple', id: 3 },
    ];
    ```

Этот шаблон предпочтительнее, чем `cloneElement`, поскольку он более явный.

### Передача данных через контекст {#passing-data-through-context}

Другой альтернативой `cloneElement` является [передача данных через контекст](../../learn/passing-data-deeply-with-context.md).

Например, вы можете вызвать [`createContext`](createContext.md), чтобы определить `HighlightContext`:

```js
export const HighlightContext = createContext(false);
```

Ваш компонент `List` может обернуть каждый элемент, который он отображает, в провайдер `HighlightContext`:

```js
export default function List({ items, renderItem }) {
    const [selectedIndex, setSelectedIndex] = useState(0);
    return (
        <div className="List">
            {items.map((item, index) => {
                const isHighlighted =
                    index === selectedIndex;
                return (
                    <HighlightContext.Provider
                        key={item.id}
                        value={isHighlighted}
                    >
                        {renderItem(item)}
                    </HighlightContext.Provider>
                );
            })}
        </div>
    );
}
```

При таком подходе `Row` вообще не нужно получать пропс `isHighlighted`. Вместо этого он считывает контекст:

```js
export default function Row({ title }) {
    const isHighlighted = useContext(HighlightContext);
    // ...
}
```

Это позволяет вызывающему компоненту не знать и не беспокоиться о передаче `isHighlighted` в `<Row>`:

```js
<List
    items={products}
    renderItem={(product) => <Row title={product.title} />}
/>
```

Вместо этого `List` и `Row` координируют логику выделения через контекст.

=== "App.js"

    ```js
    import List from './List.js';
    import Row from './Row.js';
    import { products } from './data.js';

    export default function App() {
    	return (
    		<List
    			items={products}
    			renderItem={(product) => (
    				<Row title={product.title} />
    			)}
    		/>
    	);
    }
    ```

=== "List.js"

    ```js
    import { useState } from 'react';
    import { HighlightContext } from './HighlightContext.js';

    export default function List({ items, renderItem }) {
    	const [selectedIndex, setSelectedIndex] = useState(0);
    	return (
    		<div className="List">
    			{items.map((item, index) => {
    				const isHighlighted =
    					index === selectedIndex;
    				return (
    					<HighlightContext.Provider
    						key={item.id}
    						value={isHighlighted}
    					>
    						{renderItem(item)}
    					</HighlightContext.Provider>
    				);
    			})}
    			<hr />
    			<button
    				onClick={() => {
    					setSelectedIndex(
    						(i) => (i + 1) % items.length
    					);
    				}}
    			>
    				Next
    			</button>
    		</div>
    	);
    }
    ```

=== "Row.js"

    ```js
    import { useContext } from 'react';
    import { HighlightContext } from './HighlightContext.js';

    export default function Row({ title }) {
    	const isHighlighted = useContext(HighlightContext);
    	return (
    		<div
    			className={[
    				'Row',
    				isHighlighted ? 'RowHighlighted' : '',
    			].join(' ')}
    		>
    			{title}
    		</div>
    	);
    }
    ```

=== "HighlightContext.js"

    ```js
    import { createContext } from 'react';

    export const HighlightContext = createContext(false);
    ```

=== "data.js"

    ```js
    export const products = [
    	{ title: 'Cabbage', id: 1 },
    	{ title: 'Garlic', id: 2 },
    	{ title: 'Apple', id: 3 },
    ];
    ```

[Подробнее о передаче данных через контекст.](useContext.md#passing-data-deeply-into-the-tree)

### Извлечение логики в пользовательский хук {#extracting-logic-into-a-custom-hook}

Другой подход, который вы можете попробовать - это извлечь "невизуальную" логику в свой собственный хук, и использовать информацию, возвращаемую вашим хуком, чтобы решить, что отображать. Например, вы можете написать пользовательский хук `useList` следующим образом:

```js
import { useState } from 'react';

export default function useList(items) {
    const [selectedIndex, setSelectedIndex] = useState(0);

    function onNext() {
        setSelectedIndex((i) => (i + 1) % items.length);
    }

    const selected = items[selectedIndex];
    return [selected, onNext];
}
```

Тогда вы можете использовать его следующим образом:

```js
export default function App() {
    const [selected, onNext] = useList(products);
    return (
        <div className="List">
            {products.map((product) => (
                <Row
                    key={product.id}
                    title={product.title}
                    isHighlighted={selected === product}
                />
            ))}
            <hr />
            <button onClick={onNext}>Next</button>
        </div>
    );
}
```

Поток данных является явным, но состояние находится внутри пользовательского хука `useList`, который вы можете использовать из любого компонента:

=== "App.js"

    ```js
    import Row from './Row.js';
    import useList from './useList.js';
    import { products } from './data.js';

    export default function App() {
    	const [selected, onNext] = useList(products);
    	return (
    		<div className="List">
    			{products.map((product) => (
    				<Row
    					key={product.id}
    					title={product.title}
    					isHighlighted={selected === product}
    				/>
    			))}
    			<hr />
    			<button onClick={onNext}>Next</button>
    		</div>
    	);
    }
    ```

=== "useList.js"

    ```js
    import { useState } from 'react';

    export default function useList(items) {
    	const [selectedIndex, setSelectedIndex] = useState(0);

    	function onNext() {
    		setSelectedIndex((i) => (i + 1) % items.length);
    	}

    	const selected = items[selectedIndex];
    	return [selected, onNext];
    }
    ```

=== "Row.js"

    ```js
    export default function Row({ title, isHighlighted }) {
    	return (
    		<div
    			className={[
    				'Row',
    				isHighlighted ? 'RowHighlighted' : '',
    			].join(' ')}
    		>
    			{title}
    		</div>
    	);
    }
    ```

=== "data.js"

    ```js
    export const products = [
    	{ title: 'Cabbage', id: 1 },
    	{ title: 'Garlic', id: 2 },
    	{ title: 'Apple', id: 3 },
    ];
    ```

Этот подход особенно полезен, если вы хотите повторно использовать эту логику между различными компонентами.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/cloneElement](https://react.dev/reference/react/cloneElement)</small>
