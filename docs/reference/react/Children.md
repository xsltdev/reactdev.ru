---
status: deprecated
---

# Children

!!!warning ""

    Использование `Children` является необычным и может привести к хрупкому коду.

`Children` позволяет вам манипулировать и преобразовывать JSX, который вы получили в качестве [`children` prop.](../../learn/passing-props-to-a-component.md#passing-jsx-as-children).

```js
const mappedChildren = Children.map(children, (child) => (
    <div className="Row">{child}</div>
));
```

## Описание

### `Children.count(children)`

Вызовите `Children.count(children)` для подсчета количества детей в структуре данных `children`.

```js
import { Children } from 'react';

function RowList({ children }) {
    return (
        <>
            <h1>Total rows: {Children.count(children)}</h1>
            ...
        </>
    );
}
```

**Параметры**

-   `children`: Значение пропса [`children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children), полученного вашим компонентом.

**Возвращает**

Количество узлов внутри этих `children`.

**Ограничения**

-   Пустые узлы (`null`, `undefined` и булевы), строки, числа и [React elements](createElement.md) считаются отдельными узлами. Массивы не считаются отдельными узлами, но их дочерние элементы считаются. **Обход не идет глубже, чем React-элементы:** они не отображаются, и их дочерние элементы не обходятся. [Фрагменты](Fragment.md) не обходятся.

### `Children.forEach(children, fn, thisArg?)`

Вызовите `Children.forEach(children, fn, thisArg?)`, чтобы выполнить некоторый код для каждого ребенка в структуре данных `children`.

```js
import { Children } from 'react';

function SeparatorList({ children }) {
  const result = [];
  Children.forEach(children, (child, index) => {
    result.push(child);
    result.push(<hr key={index} />);
  });
  // ...
```

**Параметры**

-   `children`: Значение свойства [`children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children), полученного вашим компонентом.
-   `fn`: Функция, которую вы хотите запускать для каждого ребенка, аналогично обратному вызову [метода массива `forEach`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach). Она будет вызвана с дочерним элементом в качестве первого аргумента и его индексом в качестве второго аргумента. Индекс начинается с `0` и увеличивается при каждом вызове.
-   **опционально** `thisArg`: Значение [`this`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/this), с которым должна быть вызвана функция `fn`. Если опущено, то `undefined`.

**Возвращает**

`Children.forEach` возвращает `undefined`.

**Ограничения**

-   Пустые узлы (`null`, `undefined` и булевы), строки, числа и [React elements](createElement.md) считаются отдельными узлами. Массивы не считаются отдельными узлами, но их дочерние элементы считаются. **Обход не идет глубже, чем React-элементы:** они не отображаются, и их дочерние элементы не обходятся. [Фрагменты](Fragment.md) не обходятся.

### `Children.map(children, fn, thisArg?)`

Вызовите `Children.map(children, fn, thisArg?)` для отображения или преобразования каждого ребенка в структуре данных `children`.

```js RowList.js active
import { Children } from 'react';

function RowList({ children }) {
    return (
        <div className="RowList">
            {Children.map(children, (child) => (
                <div className="Row">{child}</div>
            ))}
        </div>
    );
}
```

**Параметры**

-   `children`: Значение свойства [`children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children), полученного вашим компонентом.
-   `fn`: Функция отображения, аналогичная обратному вызову [array `map` method](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map). Она будет вызвана с дочерним элементом в качестве первого аргумента и его индексом в качестве второго аргумента. Индекс начинается с `0` и увеличивается при каждом вызове. Вы должны вернуть узел React из этой функции. Это может быть пустой узел (`null`, `undefined` или булево значение), строка, число, элемент React или массив других узлов React.
-   **опционально** `thisArg`: Значение [`this`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/this), с которым должна быть вызвана функция `fn`. Если оно опущено, то `undefined`.

**Возвращает**

Если `children` - `null` или `undefined`, возвращает то же значение.

В противном случае возвращает плоский массив, состоящий из узлов, которые вы вернули из функции `fn`. Возвращаемый массив будет содержать все узлы, которые вы вернули, за исключением `null` и `undefined`.

**Ограничения**

-   Пустые узлы (`null`, `undefined` и булевы), строки, числа и [React elements](createElement.md) считаются отдельными узлами. Массивы не считаются отдельными узлами, но их дочерние элементы считаются. **Обход не идет глубже, чем React-элементы:** они не отображаются, и их дочерние элементы не обходятся. [Фрагменты](Fragment.md) не обходятся.
-   Если вы возвращаете элемент или массив элементов с ключами из `fn`, **ключи возвращаемых элементов будут автоматически объединены с ключом соответствующего исходного элемента из `children`.** Когда вы возвращаете несколько элементов из `fn` в массиве, их ключи должны быть уникальными только локально друг для друга.

### `Children.only(children)`

Вызовите `Children.only(children)` для утверждения, что `children` представляют собой один элемент React.

```js
function Box({ children }) {
    const element = Children.only(children);
    // ...
}
```

**Параметры**

-   `children`: Значение свойства [`children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children), полученного вашим компонентом.

**Возвращает**

Если `children` [является допустимым элементом,](isValidElement.md) возвращает этот элемент.

В противном случае выбрасывает ошибку.

**Ограничения**

-   Этот метод всегда **отбрасывается, если вы передаете массив (например, возвращаемое значение `Children.map`) в качестве `children`.** Другими словами, он проверяет, что `children` - это один элемент React, а не массив с одним элементом.

### `Children.toArray(children)`

Вызовите `Children.toArray(children)` для создания массива из структуры данных `children`.

```js ReversedList.js active
import { Children } from 'react';

export default function ReversedList({ children }) {
    const result = Children.toArray(children);
    result.reverse();
    // ...
}
```

**Параметры**

-   `children`: Значение параметра [`children`](../../learn/passing-props-to-a-component#passing-jsx-as-children), полученное вашим компонентом.

**Возвращает**

Возвращает плоский массив элементов в `children`.

**Ограничения**

-   Пустые узлы (`null`, `undefined` и булевы) будут опущены в возвращаемом массиве. **Ключи возвращаемых элементов будут вычислены из ключей исходных элементов и их уровня вложенности и позиции.** Это гарантирует, что уплощение массива не приведет к изменениям в поведении.

## Использование

### Преобразование детей

Для преобразования дочерних JSX, которые ваш компонент [получает как пропс `children`,](../../learn/passing-props-to-a-component.md#passing-jsx-as-children) вызовите `Children.map`:

```js
import { Children } from 'react';

function RowList({ children }) {
    return (
        <div className="RowList">
            {Children.map(children, (child) => (
                <div className="Row">{child}</div>
            ))}
        </div>
    );
}
```

В приведенном выше примере `RowList` оборачивает каждого полученного дочернего элемента в контейнер `<div className="Row">`. Допустим, родительский компонент передает три тега `<p>` в качестве пропса `children` в `RowList`:

```js
<RowList>
    <p>This is the first item.</p>
    <p>This is the second item.</p>
    <p>This is the third item.</p>
</RowList>
```

Затем, с вышеуказанной реализацией `RowList`, окончательный результат рендеринга будет выглядеть следующим образом:

```js
<div className="RowList">
    <div className="Row">
        <p>This is the first item.</p>
    </div>
    <div className="Row">
        <p>This is the second item.</p>
    </div>
    <div className="Row">
        <p>This is the third item.</p>
    </div>
</div>
```

`Children.map` похож на [на преобразование массивов с помощью `map()`](../../learn/rendering-lists.md) Разница в том, что структура данных `children` считается _очевидной._ Это означает, что даже если иногда это массив, вы не должны предполагать, что это массив или любой другой конкретный тип данных. Вот почему вы должны использовать `Children.map`, если вам нужно преобразовать его.

=== "App.js"

    ```js
    import RowList from './RowList.js';

    export default function App() {
    	return (
    		<RowList>
    			<p>This is the first item.</p>
    			<p>This is the second item.</p>
    			<p>This is the third item.</p>
    		</RowList>
    	);
    }
    ```

=== "RowList.js"

    ```js
    import { Children } from 'react';

    export default function RowList({ children }) {
    	return (
    		<div className="RowList">
    			{Children.map(children, (child) => (
    				<div className="Row">{child}</div>
    			))}
    		</div>
    	);
    }
    ```

!!!note "Почему пропс children не всегда является массивом?"

    В React пропс `children` считается _прозрачной_ структурой данных. Это означает, что вы не должны полагаться на то, как он структурирован. Для преобразования, фильтрации или подсчета детей следует использовать методы `Children`.

    На практике структура данных `children` часто представляется в виде внутреннего массива. Однако если есть только один ребенок, то React не будет создавать дополнительный массив, так как это приведет к ненужным затратам памяти. Пока вы используете методы `Children` вместо прямого интроспекции пропса `children`, ваш код не сломается, даже если React изменит способ реализации структуры данных.

    Даже когда `children` является массивом, `Children.map` имеет полезное специальное поведение. Например, `Children.map` объединяет [keys](../../learn/rendering-lists.md#keeping-list-items-in-order-with-key) на возвращаемых элементах с ключами на `children`, которые вы ему передали. Это гарантирует, что оригинальные дочерние элементы JSX не "потеряют" ключи, даже если они будут обернуты, как в примере выше.

!!!warning ""

    Структура данных `children` **не включает рендеринг вывода** компонентов, которые вы передаете в виде JSX. В приведенном ниже примере `children`, полученный `RowList`, содержит только два элемента, а не три:

    1.  `<p>Это первый элемент.</p>`.
    2.  `<MoreRows />`.

    Вот почему в этом примере генерируются только две обертки строк:

    === "App.js"

    	```js
    	import RowList from './RowList.js';

    	export default function App() {
    		return (
    			<RowList>
    				<p>This is the first item.</p>
    				<MoreRows />
    			</RowList>
    		);
    	}

    	function MoreRows() {
    		return (
    			<>
    				<p>This is the second item.</p>
    				<p>This is the third item.</p>
    			</>
    		);
    	}
    	```

    === "RowList.js"

    	```js
    	import { Children } from 'react';

    	export default function RowList({ children }) {
    		return (
    			<div className="RowList">
    				{Children.map(children, (child) => (
    					<div className="Row">{child}</div>
    				))}
    			</div>
    		);
    	}
    	```

    **Невозможно получить рендерный вывод внутреннего компонента** типа `<MoreRows />` при манипулировании `children`. Вот почему обычно лучше использовать одно из альтернативных решений.

### Выполнение некоторого кода для каждого ребенка

Вызовите `Children.forEach` для перебора каждого ребенка в структуре данных `children`. Он не возвращает никакого значения и похож на метод [array `forEach`.](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) Вы можете использовать его для выполнения пользовательской логики, например, для создания собственного массива.

=== "App.js"

    ```js
    import SeparatorList from './SeparatorList.js';

    export default function App() {
    	return (
    		<SeparatorList>
    			<p>This is the first item.</p>
    			<p>This is the second item.</p>
    			<p>This is the third item.</p>
    		</SeparatorList>
    	);
    }
    ```

=== "SeparatorList.js"

    ```js
    import { Children } from 'react';

    export default function SeparatorList({ children }) {
    	const result = [];
    	Children.forEach(children, (child, index) => {
    		result.push(child);
    		result.push(<hr key={index} />);
    	});
    	result.pop(); // Remove the last separator
    	return result;
    }
    ```

!!!warning ""

    Как упоминалось ранее, не существует способа получить рендерный вывод внутреннего компонента при манипулировании `children`. Вот почему обычно лучше использовать одно из альтернативных решений.

### Подсчет детей

Вызовите `Children.count(children)` для подсчета количества детей.

=== "App.js"

    ```js
    import RowList from './RowList.js';

    export default function App() {
    	return (
    		<RowList>
    			<p>This is the first item.</p>
    			<p>This is the second item.</p>
    			<p>This is the third item.</p>
    		</RowList>
    	);
    }
    ```

=== "RowList.js"

    ```js
    import { Children } from 'react';

    export default function RowList({ children }) {
    	return (
    		<div className="RowList">
    			<h1 className="RowListHeader">
    				Total rows: {Children.count(children)}
    			</h1>
    			{Children.map(children, (child) => (
    				<div className="Row">{child}</div>
    			))}
    		</div>
    	);
    }
    ```

!!!warning ""

    Как упоминалось ранее, не существует способа получить рендерный вывод внутреннего компонента при манипулировании `children`. Вот почему обычно лучше использовать одно из альтернативных решений.

### Преобразование детей в массив

Вызовите команду `Children.toArray(children)`, чтобы превратить структуру данных `children` в обычный массив JavaScript. Это позволит вам манипулировать массивом с помощью встроенных методов массивов, таких как [`filter`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [`sort`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) или [`reverse`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse).

=== "App.js"

    ```js
    import ReversedList from './ReversedList.js';

    export default function App() {
    	return (
    		<ReversedList>
    			<p>This is the first item.</p>
    			<p>This is the second item.</p>
    			<p>This is the third item.</p>
    		</ReversedList>
    	);
    }
    ```

=== "ReversedList.js"

    ```js
    import { Children } from 'react';

    export default function ReversedList({ children }) {
    	const result = Children.toArray(children);
    	result.reverse();
    	return result;
    }
    ```

!!!warning ""

    Как упоминалось ранее, не существует способа получить рендерный вывод внутреннего компонента при манипулировании `children`. Вот почему обычно лучше использовать одно из альтернативных решений.

## Альтернативы

!!!note ""

    В этом разделе описаны альтернативы API `Children` (с большой буквы `C`), который импортируется следующим образом:

    ```js
    import { Children } from 'react';
    ```

    Не путайте это с [использованием свойства `children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children) (строчная буква `c`), что хорошо и поощряется.

### Раскрытие нескольких компонентов

Манипулирование дочерними компонентами с помощью методов `Children` часто приводит к хрупкому коду. Когда вы передаете дочерние элементы компоненту в JSX, вы обычно не ожидаете, что компонент будет манипулировать или преобразовывать отдельные дочерние элементы.

Когда это возможно, старайтесь избегать использования методов `Children`. Например, если вы хотите, чтобы каждый дочерний элемент `RowList` был обернут в `<div className="Row">`, экспортируйте компонент `Row` и вручную оберните каждый ряд в него следующим образом:

=== "App.js"

    ```js
    import { RowList, Row } from './RowList.js';

    export default function App() {
    	return (
    		<RowList>
    			<Row>
    				<p>This is the first item.</p>
    			</Row>
    			<Row>
    				<p>This is the second item.</p>
    			</Row>
    			<Row>
    				<p>This is the third item.</p>
    			</Row>
    		</RowList>
    	);
    }
    ```

=== "RowList.js"

    ```js
    export function RowList({ children }) {
    	return <div className="RowList">{children}</div>;
    }

    export function Row({ children }) {
    	return <div className="Row">{children}</div>;
    }
    ```

В отличие от использования `Children.map`, этот подход не оборачивает каждого ребенка автоматически. **Однако, этот подход имеет значительное преимущество по сравнению с предыдущим примером с `Children.map`, потому что он работает, даже если вы продолжаете извлекать больше компонентов.** Например, он все еще работает, если вы извлекаете свой собственный компонент `MoreRows`:

=== "App.js"

    ```js
    import { RowList, Row } from './RowList.js';

    export default function App() {
    	return (
    		<RowList>
    			<Row>
    				<p>This is the first item.</p>
    			</Row>
    			<MoreRows />
    		</RowList>
    	);
    }

    function MoreRows() {
    	return (
    		<>
    			<Row>
    				<p>This is the second item.</p>
    			</Row>
    			<Row>
    				<p>This is the third item.</p>
    			</Row>
    		</>
    	);
    }
    ```

=== "RowList.js"

    ```js
    export function RowList({ children }) {
    	return <div className="RowList">{children}</div>;
    }

    export function Row({ children }) {
    	return <div className="Row">{children}</div>;
    }
    ```

Это не будет работать с `Children.map`, потому что он будет "видеть" `<MoreRows />` как одного ребенка (и одну строку).

### Принятие массива объектов в качестве пропса

Вы также можете явно передать массив в качестве пропса. Например, этот `RowList` принимает в качестве пропса массив `rows`:

=== "App.js"

    ```js
    import { RowList, Row } from './RowList.js';

    export default function App() {
    	return (
    		<RowList
    			rows={[
    				{
    					id: 'first',
    					content: <p>This is the first item.</p>,
    				},
    				{
    					id: 'second',
    					content: (
    						<p>This is the second item.</p>
    					),
    				},
    				{
    					id: 'third',
    					content: <p>This is the third item.</p>,
    				},
    			]}
    		/>
    	);
    }
    ```

=== "RowList.js"

    ```js
    export function RowList({ rows }) {
    	return (
    		<div className="RowList">
    			{rows.map((row) => (
    				<div className="Row" key={row.id}>
    					{row.content}
    				</div>
    			))}
    		</div>
    	);
    }
    ```

Поскольку `rows` является обычным массивом JavaScript, компонент `RowList` может использовать для него встроенные методы массивов, такие как [`map`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map).

Этот паттерн особенно полезен, когда вы хотите иметь возможность передавать больше информации в виде структурированных данных вместе с дочерними элементами. В приведенном ниже примере компонент `TabSwitcher` получает массив объектов в качестве пропса `tabs`:

=== "App.js"

    ```js
    import TabSwitcher from './TabSwitcher.js';

    export default function App() {
    	return (
    		<TabSwitcher
    			tabs={[
    				{
    					id: 'first',
    					header: 'First',
    					content: <p>This is the first item.</p>,
    				},
    				{
    					id: 'second',
    					header: 'Second',
    					content: (
    						<p>This is the second item.</p>
    					),
    				},
    				{
    					id: 'third',
    					header: 'Third',
    					content: <p>This is the third item.</p>,
    				},
    			]}
    		/>
    	);
    }
    ```

=== "TabSwitcher.js"

    ```js
    import { useState } from 'react';

    export default function TabSwitcher({ tabs }) {
    	const [selectedId, setSelectedId] = useState(
    		tabs[0].id
    	);
    	const selectedTab = tabs.find(
    		(tab) => tab.id === selectedId
    	);
    	return (
    		<>
    			{tabs.map((tab) => (
    				<button
    					key={tab.id}
    					onClick={() => setSelectedId(tab.id)}
    				>
    					{tab.header}
    				</button>
    			))}
    			<hr />
    			<div key={selectedId}>
    				<h3>{selectedTab.header}</h3>
    				{selectedTab.content}
    			</div>
    		</>
    	);
    }
    ```

В отличие от передачи дочерних элементов как JSX, этот подход позволяет вам связать некоторые дополнительные данные, такие как `header`, с каждым элементом. Поскольку вы работаете с `tabs` напрямую, и это массив, вам не нужны методы `Children`.

### Вызов render prop для настройки рендеринга

Вместо того чтобы создавать JSX для каждого отдельного элемента, вы также можете передать функцию, которая возвращает JSX, и вызывать эту функцию, когда это необходимо. В этом примере компонент `App` передает функцию `renderContent` компоненту `TabSwitcher`. Компонент `TabSwitcher` вызывает `renderContent` только для выбранной вкладки:

=== "App.js"

    ```js
    import TabSwitcher from './TabSwitcher.js';

    export default function App() {
    	return (
    		<TabSwitcher
    			tabIds={['first', 'second', 'third']}
    			getHeader={(tabId) => {
    				return (
    					tabId[0].toUpperCase() + tabId.slice(1)
    				);
    			}}
    			renderContent={(tabId) => {
    				return <p>This is the {tabId} item.</p>;
    			}}
    		/>
    	);
    }
    ```

=== "TabSwitcher.js"

    ```js
    import { useState } from 'react';

    export default function TabSwitcher({
    	tabIds,
    	getHeader,
    	renderContent,
    }) {
    	const [selectedId, setSelectedId] = useState(tabIds[0]);
    	return (
    		<>
    			{tabIds.map((tabId) => (
    				<button
    					key={tabId}
    					onClick={() => setSelectedId(tabId)}
    				>
    					{getHeader(tabId)}
    				</button>
    			))}
    			<hr />
    			<div key={selectedId}>
    				<h3>{getHeader(selectedId)}</h3>
    				{renderContent(selectedId)}
    			</div>
    		</>
    	);
    }
    ```

Пропс типа `renderContent` называется _render prop_, потому что это пропс, определяющий, как отобразить часть пользовательского интерфейса. Однако в нем нет ничего особенного: это обычный пропс, который, как оказалось, является функцией.

Пропсы Render являются функциями, поэтому вы можете передавать им информацию. Например, компонент `RowList` передает `id` и `index` каждого ряда в пропс рендеринга `renderRow`, который использует `index` для выделения четных рядов:

=== "App.js"

    ```js
    import { RowList, Row } from './RowList.js';

    export default function App() {
    	return (
    		<RowList
    			rowIds={['first', 'second', 'third']}
    			renderRow={(id, index) => {
    				return (
    					<Row isHighlighted={index % 2 === 0}>
    						<p>This is the {id} item.</p>
    					</Row>
    				);
    			}}
    		/>
    	);
    }
    ```

=== "RowList.js"

    ```js
    import { Fragment } from 'react';

    export function RowList({ rowIds, renderRow }) {
    	return (
    		<div className="RowList">
    			<h1 className="RowListHeader">
    				Total rows: {rowIds.length}
    			</h1>
    			{rowIds.map((rowId, index) => (
    				<Fragment key={rowId}>
    					{renderRow(rowId, index)}
    				</Fragment>
    			))}
    		</div>
    	);
    }

    export function Row({ children, isHighlighted }) {
    	return (
    		<div
    			className={[
    				'Row',
    				isHighlighted ? 'RowHighlighted' : '',
    			].join(' ')}
    		>
    			{children}
    		</div>
    	);
    }
    ```

Это еще один пример того, как родительские и дочерние компоненты могут сотрудничать, не манипулируя детьми.

## Устранение неполадок

### Я передаю пользовательский компонент, но методы `Children` не показывают его результат рендеринга

Предположим, вы передаете два дочерних компонента в `RowList` следующим образом:

```js
<RowList>
    <p>First item</p>
    <MoreRows />
</RowList>
```

Если вы выполните `Children.count(children)` внутри `RowList`, вы получите `2`. Даже если `MoreRows` отобразит 10 различных элементов или вернет `null`, `Children.count(children)` все равно будет `2`. С точки зрения `RowList`, он "видит" только JSX, который он получил. Он не "видит" внутренности компонента `MoreRows`.

Это ограничение затрудняет извлечение компонента. Вот почему альтернативы предпочтительнее использования `Children`.
