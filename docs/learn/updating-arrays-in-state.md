---
description: В JavaScript массивы являются изменяемыми, но при хранении их в состоянии вы должны относиться к ним как к неизменяемым. Как и в случае с объектами, когда вы хотите обновить массив, хранящийся в состоянии, вам нужно создать новый массив
---

# Обновление массивов в состоянии

<big>В JavaScript массивы являются изменяемыми, но при хранении их в состоянии вы должны относиться к ним как к неизменяемым. Как и в случае с объектами, когда вы хотите обновить массив, хранящийся в состоянии, вам нужно создать новый массив (или сделать копию существующего), а затем установить состояние для использования нового массива.</big>

!!!tip "Вы узнаете"

    -   Как добавлять, удалять или изменять элементы в массиве в состоянии React
    -   Как обновить объект внутри массива
    -   Как сделать копирование массива менее повторяющимся с помощью Immer

## Обновление массивов без мутации {#updating-arrays-without-mutation}

В JavaScript массивы - это просто еще один вид объектов. [Как и с объектами](updating-objects-in-state.md), **вы должны рассматривать массивы в React state как доступные только для чтения**. Это означает, что вы не должны переназначать элементы внутри массива, например `arr[0] = 'bird'`, а также не должны использовать методы, которые изменяют массив, такие как `push()` и `pop()`.

Вместо этого, каждый раз, когда вы хотите обновить массив, вы должны передавать _новый_ массив в вашу функцию установки состояния. Для этого вы можете создать новый массив из исходного массива вашего состояния, вызвав его не изменяющие методы, такие как `filter()` и `map()`. Затем вы можете установить свое состояние на полученный новый массив.

Вот справочная таблица распространенных операций с массивами. При работе с массивами внутри React state вам нужно избегать методов в левой колонке, а предпочесть методы в правой колонке:

|            | избегать (изменяет массив)            | предпочитать (возвращает новый массив)         |
| ---------- | ------------------------------------- | ---------------------------------------------- |
| добавление | `push`, `unshift`                     | `concat`, `[...arr]` синтаксис распространения |
| удаление   | `pop`, `shift`, `splice`              | `filter`, `slice`                              |
| замена     | `splice`, `arr[i] = ...` присваивание | `map`                                          |
| сортировка | `reverse`, `sort`                     | сначала копируем массив                        |

В качестве альтернативы можно использовать Immer, который позволяет использовать методы из обоих столбцов.

!!!warning "Внимание"

    К сожалению, [`slice`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/slice) и [`splice`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/splice) называются похоже, но являются совершенно разными:

    -   `slice` позволяет копировать массив или его часть.
    -   `splice` **изменяет** массив (для вставки или удаления элементов).

    В React вы будете использовать `slice` (без `p`!) гораздо чаще, потому что вы не хотите изменять объекты или массивы в состоянии. В [Обновление объектов в состоянии](updating-objects-in-state.md) объясняется, что такое мутация и почему она не рекомендуется для состояния.

### Добавление в массив {#adding-to-an-array}

`push()` будет мутировать массив, чего вы не хотите:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 0;

    export default function List() {
    	const [name, setName] = useState('');
    	const [artists, setArtists] = useState([]);

    	return (
    		<>
    			<h1>Inspiring sculptors:</h1>
    			<input
    				value={name}
    				onChange={(e) => setName(e.target.value)}
    			/>
    			<button
    				onClick={() => {
    					artists.push({
    						id: nextId++,
    						name: name,
    					});
    				}}
    			>
    				Add
    			</button>
    			<ul>
    				{artists.map((artist) => (
    					<li key={artist.id}>{artist.name}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/s46kl6?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вместо этого создайте _новый_ массив, который содержит существующие элементы _и_ новый элемент в конце. Существует несколько способов сделать это, но самый простой - использовать [spread синтаксис `...`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Spread_syntax#spread_in_array_literals):

```js
setArtists(
    // Replace the state
    [
        // with a new array
        ...artists, // that contains all the old items
        { id: nextId++, name: name }, // and one new item at the end
    ]
);
```

Теперь он работает правильно:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 0;

    export default function List() {
    	const [name, setName] = useState('');
    	const [artists, setArtists] = useState([]);

    	return (
    		<>
    			<h1>Inspiring sculptors:</h1>
    			<input
    				value={name}
    				onChange={(e) => setName(e.target.value)}
    			/>
    			<button
    				onClick={() => {
    					setArtists([
    						...artists,
    						{ id: nextId++, name: name },
    					]);
    				}}
    			>
    				Add
    			</button>
    			<ul>
    				{artists.map((artist) => (
    					<li key={artist.id}>{artist.name}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yy44zn?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Spread синтаксис массива также позволяет добавлять элемент, помещая его _перед_ исходным `...artists`:

```js
setArtists([
    { id: nextId++, name: name },
    ...artists, // Put old items at the end
]);
```

Таким образом, spread может выполнять работу как `push()`, добавляя в конец массива, так и `unshift()`, добавляя в начало массива.

### Удаление из массива {#removing-from-an-array}

Самый простой способ удалить элемент из массива - это _отфильтровать его_. Другими словами, вы создадите новый массив, который не будет содержать этот элемент. Для этого используйте метод `filter`, например:

=== "App.js"

    ```js
    import { useState } from 'react';

    let initialArtists = [
    	{ id: 0, name: 'Marta Colvin Andrade' },
    	{ id: 1, name: 'Lamidi Olonade Fakeye' },
    	{ id: 2, name: 'Louise Nevelson' },
    ];

    export default function List() {
    	const [artists, setArtists] = useState(initialArtists);

    	return (
    		<>
    			<h1>Inspiring sculptors:</h1>
    			<ul>
    				{artists.map((artist) => (
    					<li key={artist.id}>
    						{artist.name}{' '}
    						<button
    							onClick={() => {
    								setArtists(
    									artists.filter(
    										(a) =>
    											a.id !==
    											artist.id
    									)
    								);
    							}}
    						>
    							Delete
    						</button>
    					</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gzr5t6?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Несколько раз нажмите кнопку "Удалить" и посмотрите на ее обработчик нажатия.

```js
setArtists(artists.filter((a) => a.id !== artist.id));
```

Здесь `artists.filter(a => a.id !== artist.id)` означает "создать массив, состоящий из тех `artist`, чьи ID отличаются от `artist.id`". Другими словами, при нажатии кнопки "Удалить" каждого артиста из массива будет отфильтровываться _этот_ артист, а затем запрашиваться повторный рендеринг с полученным массивом. Обратите внимание, что `filter` не изменяет исходный массив.

### Преобразование массива {#transforming-an-array}

Если вы хотите изменить некоторые или все элементы массива, вы можете использовать `map()` для создания **нового** массива. Функция, которую вы передадите в `map`, может решить, что делать с каждым элементом, основываясь на его данных или индексе (или на обоих).

В этом примере массив содержит координаты двух кругов и квадрата. Когда вы нажимаете на кнопку, она перемещает только круги вниз на 50 пикселей. Для этого создается новый массив данных с помощью `map()`:

=== "App.js"

    ```js
    import { useState } from 'react';

    let initialShapes = [
    	{ id: 0, type: 'circle', x: 50, y: 100 },
    	{ id: 1, type: 'square', x: 150, y: 100 },
    	{ id: 2, type: 'circle', x: 250, y: 100 },
    ];

    export default function ShapeEditor() {
    	const [shapes, setShapes] = useState(initialShapes);

    	function handleClick() {
    		const nextShapes = shapes.map((shape) => {
    			if (shape.type === 'square') {
    				// No change
    				return shape;
    			} else {
    				// Return a new circle 50px below
    				return {
    					...shape,
    					y: shape.y + 50,
    				};
    			}
    		});
    		// Re-render with the new array
    		setShapes(nextShapes);
    	}

    	return (
    		<>
    			<button onClick={handleClick}>
    				Move circles down!
    			</button>
    			{shapes.map((shape) => (
    				<div
    					key={shape.id}
    					style={{
    						background: 'purple',
    						position: 'absolute',
    						left: shape.x,
    						top: shape.y,
    						borderRadius:
    							shape.type === 'circle'
    								? '50%'
    								: '',
    						width: 20,
    						height: 20,
    					}}
    				/>
    			))}
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/jtr9d8?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Замена элементов в массиве {#replacing-items-in-an-array}

Особенно часто возникает необходимость заменить один или несколько элементов в массиве. Назначения типа `arr[0] = 'bird'` изменяют исходный массив, поэтому для этого лучше использовать `map`.

Чтобы заменить элемент, создайте новый массив с помощью `map`. Внутри вашего вызова `map` вы получите индекс элемента в качестве второго аргумента. Используйте его, чтобы решить, вернуть ли исходный элемент (первый аргумент) или что-то другое:

=== "App.js"

    ```js
    import { useState } from 'react';

    let initialCounters = [0, 0, 0];

    export default function CounterList() {
    	const [counters, setCounters] = useState(
    		initialCounters
    	);

    	function handleIncrementClick(index) {
    		const nextCounters = counters.map((c, i) => {
    			if (i === index) {
    				// Increment the clicked counter
    				return c + 1;
    			} else {
    				// The rest haven't changed
    				return c;
    			}
    		});
    		setCounters(nextCounters);
    	}

    	return (
    		<ul>
    			{counters.map((counter, i) => (
    				<li key={i}>
    					{counter}
    					<button
    						onClick={() => {
    							handleIncrementClick(i);
    						}}
    					>
    						+1
    					</button>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dshfhy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Вставка в массив {#inserting-into-an-array}

Иногда вам может понадобиться вставить элемент в определенную позицию, которая не находится ни в начале, ни в конце. Для этого вы можете использовать синтаксис расширения массива `...` вместе с методом `slice()`. Метод `slice()` позволяет вам вырезать "кусочек" массива. Чтобы вставить элемент, вы создадите массив, который будет использовать часть _до_ точки вставки, затем новый элемент, а затем остальную часть исходного массива.

В этом примере кнопка Insert всегда вставляет в индекс `1`:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 3;
    const initialArtists = [
    	{ id: 0, name: 'Marta Colvin Andrade' },
    	{ id: 1, name: 'Lamidi Olonade Fakeye' },
    	{ id: 2, name: 'Louise Nevelson' },
    ];

    export default function List() {
    	const [name, setName] = useState('');
    	const [artists, setArtists] = useState(initialArtists);

    	function handleClick() {
    		const insertAt = 1; // Could be any index
    		const nextArtists = [
    			// Items before the insertion point:
    			...artists.slice(0, insertAt),
    			// New item:
    			{ id: nextId++, name: name },
    			// Items after the insertion point:
    			...artists.slice(insertAt),
    		];
    		setArtists(nextArtists);
    		setName('');
    	}

    	return (
    		<>
    			<h1>Inspiring sculptors:</h1>
    			<input
    				value={name}
    				onChange={(e) => setName(e.target.value)}
    			/>
    			<button onClick={handleClick}>Insert</button>
    			<ul>
    				{artists.map((artist) => (
    					<li key={artist.id}>{artist.name}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/slvv47?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Внесение других изменений в массив {#making-other-changes-to-an-array}

Есть некоторые вещи, которые нельзя сделать с помощью spread-синтаксиса и таких неизменяющих методов, как `map()` и `filter()`. Например, вы можете захотеть развернуть или отсортировать массив. Методы JavaScript `reverse()` и `sort()` мутируют исходный массив, поэтому вы не можете использовать их напрямую.

**Однако можно сначала скопировать массив, а затем внести в него изменения**.

Например:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 3;
    const initialList = [
    	{ id: 0, title: 'Big Bellies' },
    	{ id: 1, title: 'Lunar Landscape' },
    	{ id: 2, title: 'Terracotta Army' },
    ];

    export default function List() {
    	const [list, setList] = useState(initialList);

    	function handleClick() {
    		const nextList = [...list];
    		nextList.reverse();
    		setList(nextList);
    	}

    	return (
    		<>
    			<button onClick={handleClick}>Reverse</button>
    			<ul>
    				{list.map((artwork) => (
    					<li key={artwork.id}>
    						{artwork.title}
    					</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/2f2652?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Здесь вы используете spread-синтаксис `[...list]`, чтобы сначала создать копию исходного массива. Теперь, когда у вас есть копия, вы можете использовать такие мутирующие методы, как `nextList.reverse()` или `nextList.sort()`, или даже назначить отдельные элементы с помощью `nextList[0] = "something"`.

Однако, **даже если вы копируете массив, вы не можете изменять существующие элементы _внутри_ массива напрямую.** Это происходит потому, что копирование неглубокое - новый массив будет содержать те же элементы, что и исходный. Поэтому если вы изменяете объект внутри скопированного массива, вы изменяете существующее состояние. Например, такой код представляет собой проблему.

```js
const nextList = [...list];
nextList[0].seen = true; // Problem: mutates list[0]
setList(nextList);
```

Хотя `nextList` и `list` являются двумя разными массивами, **`nextList[0]` и `list[0]` указывают на один и тот же объект.** Поэтому, изменяя `nextList[0].seen`, вы также изменяете `list[0].seen`. Это мутация состояния, которой следует избегать! Вы можете решить эту проблему аналогично [обновлению вложенных объектов JavaScript](updating-objects-in-state.md#updating-a-nested-object), путем копирования отдельных элементов, которые вы хотите изменить, вместо их мутации. Вот как это делается.

## Обновление объектов внутри массивов {#updating-objects-inside-arrays}

Объекты _на самом деле_ расположены не "внутри" массивов. В коде они могут казаться "внутри", но каждый объект в массиве - это отдельное значение, на которое "указывает" массив. Вот почему нужно быть осторожным при изменении вложенных полей типа `list[0]`. Список произведений искусства другого человека может указывать на тот же элемент массива!

**При обновлении вложенного состояния необходимо создавать копии от точки, где вы хотите обновить, и до самого верхнего уровня.** Давайте посмотрим, как это работает.

В этом примере два отдельных списка произведений искусства имеют одинаковое начальное состояние. Они должны быть изолированы, но из-за мутации их состояние случайно стало общим, и установка флажка в одном списке влияет на другой список:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 3;
    const initialList = [
    	{ id: 0, title: 'Big Bellies', seen: false },
    	{ id: 1, title: 'Lunar Landscape', seen: false },
    	{ id: 2, title: 'Terracotta Army', seen: true },
    ];

    export default function BucketList() {
    	const [myList, setMyList] = useState(initialList);
    	const [yourList, setYourList] = useState(initialList);

    	function handleToggleMyList(artworkId, nextSeen) {
    		const myNextList = [...myList];
    		const artwork = myNextList.find(
    			(a) => a.id === artworkId
    		);
    		artwork.seen = nextSeen;
    		setMyList(myNextList);
    	}

    	function handleToggleYourList(artworkId, nextSeen) {
    		const yourNextList = [...yourList];
    		const artwork = yourNextList.find(
    			(a) => a.id === artworkId
    		);
    		artwork.seen = nextSeen;
    		setYourList(yourNextList);
    	}

    	return (
    		<>
    			<h1>Art Bucket List</h1>
    			<h2>My list of art to see:</h2>
    			<ItemList
    				artworks={myList}
    				onToggle={handleToggleMyList}
    			/>
    			<h2>Your list of art to see:</h2>
    			<ItemList
    				artworks={yourList}
    				onToggle={handleToggleYourList}
    			/>
    		</>
    	);
    }

    function ItemList({ artworks, onToggle }) {
    	return (
    		<ul>
    			{artworks.map((artwork) => (
    				<li key={artwork.id}>
    					<label>
    						<input
    							type="checkbox"
    							checked={artwork.seen}
    							onChange={(e) => {
    								onToggle(
    									artwork.id,
    									e.target.checked
    								);
    							}}
    						/>
    						{artwork.title}
    					</label>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/z569tj?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Проблема возникает в коде, подобном этому:

```js
const myNextList = [...myList];
const artwork = myNextList.find((a) => a.id === artworkId);
artwork.seen = nextSeen; // Problem: mutates an existing item
setMyList(myNextList);
```

Хотя сам массив `myNextList` является новым, сами _элементы_ являются теми же, что и в исходном массиве `myList`. Таким образом, изменение `artwork.seen` изменяет _оригинальный_ элемент произведения искусства. Этот элемент также находится в `yourList`, что и вызывает ошибку. О таких ошибках сложно думать, но, к счастью, они исчезают, если вы избегаете мутирования состояния.

**Вы можете использовать `map` для замены старого элемента на его обновленную версию без мутации состояния.**

```js
setMyList(
    myList.map((artwork) => {
        if (artwork.id === artworkId) {
            // Create a *new* object with changes
            return { ...artwork, seen: nextSeen };
        } else {
            // No changes
            return artwork;
        }
    })
);
```

Здесь `...` - это spread-синтаксис объекта, используемый для [создания копии объекта](updating-objects-in-state.md#copying-objects-with-the-spread-syntax).

При таком подходе ни один из существующих элементов состояния не изменяется, и ошибка исправлена:

=== "App.js"

    ```js
    import { useState } from 'react';

    let nextId = 3;
    const initialList = [
    	{ id: 0, title: 'Big Bellies', seen: false },
    	{ id: 1, title: 'Lunar Landscape', seen: false },
    	{ id: 2, title: 'Terracotta Army', seen: true },
    ];

    export default function BucketList() {
    	const [myList, setMyList] = useState(initialList);
    	const [yourList, setYourList] = useState(initialList);

    	function handleToggleMyList(artworkId, nextSeen) {
    		setMyList(
    			myList.map((artwork) => {
    				if (artwork.id === artworkId) {
    					// Create a *new* object with changes
    					return { ...artwork, seen: nextSeen };
    				} else {
    					// No changes
    					return artwork;
    				}
    			})
    		);
    	}

    	function handleToggleYourList(artworkId, nextSeen) {
    		setYourList(
    			yourList.map((artwork) => {
    				if (artwork.id === artworkId) {
    					// Create a *new* object with changes
    					return { ...artwork, seen: nextSeen };
    				} else {
    					// No changes
    					return artwork;
    				}
    			})
    		);
    	}

    	return (
    		<>
    			<h1>Art Bucket List</h1>
    			<h2>My list of art to see:</h2>
    			<ItemList
    				artworks={myList}
    				onToggle={handleToggleMyList}
    			/>
    			<h2>Your list of art to see:</h2>
    			<ItemList
    				artworks={yourList}
    				onToggle={handleToggleYourList}
    			/>
    		</>
    	);
    }

    function ItemList({ artworks, onToggle }) {
    	return (
    		<ul>
    			{artworks.map((artwork) => (
    				<li key={artwork.id}>
    					<label>
    						<input
    							type="checkbox"
    							checked={artwork.seen}
    							onChange={(e) => {
    								onToggle(
    									artwork.id,
    									e.target.checked
    								);
    							}}
    						/>
    						{artwork.title}
    					</label>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/sn8rk7?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В общем, **вы должны мутировать только те объекты, которые вы только что создали.** Если вы вставляете _новый_ объект, вы можете мутировать его, но если вы имеете дело с чем-то, что уже находится в состоянии, вам нужно сделать копию.

### Пишем лаконичную логику обновления с помощью Immer {#write-concise-update-logic-with-immer}

Обновление вложенных массивов без мутации может стать немного повторяющимся. [Как и в случае с объектами](updating-objects-in-state.md#write-concise-update-logic-with-immer):

-   Как правило, вам не нужно обновлять состояние глубже, чем на пару уровней. Если ваши объекты состояния очень глубокие, возможно, вы захотите [перестроить их по-другому](choosing-the-state-structure.md#avoid-deeply-nested-state), чтобы они были плоскими.
-   Если вы не хотите менять структуру состояний, лучше использовать [Immer](https://github.com/immerjs/use-immer), который позволяет писать, используя удобный, но мутирующий синтаксис, и заботится о создании копий за вас.

Вот пример Art Bucket List, переписанный с помощью Immer:

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useImmer } from 'use-immer';

    let nextId = 3;
    const initialList = [
    	{ id: 0, title: 'Big Bellies', seen: false },
    	{ id: 1, title: 'Lunar Landscape', seen: false },
    	{ id: 2, title: 'Terracotta Army', seen: true },
    ];

    export default function BucketList() {
    	const [myList, updateMyList] = useImmer(initialList);
    	const [yourList, updateYourList] = useImmer(
    		initialList
    	);

    	function handleToggleMyList(id, nextSeen) {
    		updateMyList((draft) => {
    			const artwork = draft.find((a) => a.id === id);
    			artwork.seen = nextSeen;
    		});
    	}

    	function handleToggleYourList(artworkId, nextSeen) {
    		updateYourList((draft) => {
    			const artwork = draft.find(
    				(a) => a.id === artworkId
    			);
    			artwork.seen = nextSeen;
    		});
    	}

    	return (
    		<>
    			<h1>Art Bucket List</h1>
    			<h2>My list of art to see:</h2>
    			<ItemList
    				artworks={myList}
    				onToggle={handleToggleMyList}
    			/>
    			<h2>Your list of art to see:</h2>
    			<ItemList
    				artworks={yourList}
    				onToggle={handleToggleYourList}
    			/>
    		</>
    	);
    }

    function ItemList({ artworks, onToggle }) {
    	return (
    		<ul>
    			{artworks.map((artwork) => (
    				<li key={artwork.id}>
    					<label>
    						<input
    							type="checkbox"
    							checked={artwork.seen}
    							onChange={(e) => {
    								onToggle(
    									artwork.id,
    									e.target.checked
    								);
    							}}
    						/>
    						{artwork.title}
    					</label>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/k2pfly?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="upbeat-fog-k2pfly" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что с Immer, **мутация типа `artwork.seen = nextSeen` теперь в порядке:**

```js
updateMyTodos((draft) => {
    const artwork = draft.find((a) => a.id === artworkId);
    artwork.seen = nextSeen;
});
```

Это происходит потому, что вы не изменяете _оригинальное_ состояние, а изменяете специальный объект `draft`, предоставленный Immer. Аналогично, вы можете применять такие мутирующие методы, как `push()` и `pop()` к содержимому `draft`.

За кулисами Immer всегда строит следующее состояние с нуля в соответствии с изменениями, которые вы внесли в `draft`. Это позволяет сделать обработчики событий очень лаконичными, не изменяя состояние.

!!!tip "Итоги"

    -   Вы можете поместить массивы в состояние, но вы не можете их изменить.
    -   Вместо того, чтобы изменять массив, создайте _новую_ его версию и обновите состояние на нее.
    -   Вы можете использовать синтаксис `[...arr, newItem]` для создания массивов с новыми элементами.
    -   Вы можете использовать `filter()` и `map()` для создания новых массивов с отфильтрованными или преобразованными элементами.
    -   Вы можете использовать Immer для сохранения краткости кода.

## Задачи {#challenges}

### 1. Обновление элемента в корзине {#update-an-item-in-the-shopping-cart}

Заполните логику `handleIncreaseClick` так, чтобы нажатие "+" увеличивало соответствующее число:

=== "App.js"

    ```js
    import { useState } from 'react';

    const initialProducts = [
    	{
    		id: 0,
    		name: 'Baklava',
    		count: 1,
    	},
    	{
    		id: 1,
    		name: 'Cheese',
    		count: 5,
    	},
    	{
    		id: 2,
    		name: 'Spaghetti',
    		count: 2,
    	},
    ];

    export default function ShoppingCart() {
    	const [products, setProducts] = useState(
    		initialProducts
    	);

    	function handleIncreaseClick(productId) {}

    	return (
    		<ul>
    			{products.map((product) => (
    				<li key={product.id}>
    					{product.name} (<b>{product.count}</b>)
    					<button
    						onClick={() => {
    							handleIncreaseClick(product.id);
    						}}
    					>
    						+
    					</button>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/m59pxc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Вы можете использовать функцию `map` для создания нового массива, а затем использовать синтаксис распространения объектов `...` для создания копии измененного объекта для нового массива:

    === "App.js"

    	```js
    	import { useState } from 'react';

    	const initialProducts = [
    		{
    			id: 0,
    			name: 'Baklava',
    			count: 1,
    		},
    		{
    			id: 1,
    			name: 'Cheese',
    			count: 5,
    		},
    		{
    			id: 2,
    			name: 'Spaghetti',
    			count: 2,
    		},
    	];

    	export default function ShoppingCart() {
    		const [products, setProducts] = useState(
    			initialProducts
    		);

    		function handleIncreaseClick(productId) {
    			setProducts(
    				products.map((product) => {
    					if (product.id === productId) {
    						return {
    							...product,
    							count: product.count + 1,
    						};
    					} else {
    						return product;
    					}
    				})
    			);
    		}

    		return (
    			<ul>
    				{products.map((product) => (
    					<li key={product.id}>
    						{product.name} (<b>{product.count}</b>)
    						<button
    							onClick={() => {
    								handleIncreaseClick(product.id);
    							}}
    						>
    							+
    						</button>
    					</li>
    				))}
    			</ul>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/kkwj9n?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 2. Удаление товара из корзины {#remove-an-item-from-the-shopping-cart}

В этой корзине есть рабочая кнопка "+", но кнопка "-" ничего не делает. Вам нужно добавить обработчик события, чтобы нажатие на нее уменьшало `count` соответствующего товара. Если вы нажмете "-", когда счетчик будет равен 1, товар должен автоматически удалиться из корзины. Убедитесь, что он никогда не показывает 0.

=== "App.js"

    ```js
    import { useState } from 'react';

    const initialProducts = [
    	{
    		id: 0,
    		name: 'Baklava',
    		count: 1,
    	},
    	{
    		id: 1,
    		name: 'Cheese',
    		count: 5,
    	},
    	{
    		id: 2,
    		name: 'Spaghetti',
    		count: 2,
    	},
    ];

    export default function ShoppingCart() {
    	const [products, setProducts] = useState(
    		initialProducts
    	);

    	function handleIncreaseClick(productId) {
    		setProducts(
    			products.map((product) => {
    				if (product.id === productId) {
    					return {
    						...product,
    						count: product.count + 1,
    					};
    				} else {
    					return product;
    				}
    			})
    		);
    	}

    	return (
    		<ul>
    			{products.map((product) => (
    				<li key={product.id}>
    					{product.name} (<b>{product.count}</b>)
    					<button
    						onClick={() => {
    							handleIncreaseClick(product.id);
    						}}
    					>
    						+
    					</button>
    					<button>–</button>
    				</li>
    			))}
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/kzq2m8?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Вы можете сначала использовать `map` для создания нового массива, а затем `filter` для удаления продуктов с `count`, установленным в `0`:

    === "App.js"

    	```js
    	import { useState } from 'react';

    	const initialProducts = [
    		{
    			id: 0,
    			name: 'Baklava',
    			count: 1,
    		},
    		{
    			id: 1,
    			name: 'Cheese',
    			count: 5,
    		},
    		{
    			id: 2,
    			name: 'Spaghetti',
    			count: 2,
    		},
    	];

    	export default function ShoppingCart() {
    		const [products, setProducts] = useState(
    			initialProducts
    		);

    		function handleIncreaseClick(productId) {
    			setProducts(
    				products.map((product) => {
    					if (product.id === productId) {
    						return {
    							...product,
    							count: product.count + 1,
    						};
    					} else {
    						return product;
    					}
    				})
    			);
    		}

    		function handleDecreaseClick(productId) {
    			let nextProducts = products.map((product) => {
    				if (product.id === productId) {
    					return {
    						...product,
    						count: product.count - 1,
    					};
    				} else {
    					return product;
    				}
    			});
    			nextProducts = nextProducts.filter(
    				(p) => p.count > 0
    			);
    			setProducts(nextProducts);
    		}

    		return (
    			<ul>
    				{products.map((product) => (
    					<li key={product.id}>
    						{product.name} (<b>{product.count}</b>)
    						<button
    							onClick={() => {
    								handleIncreaseClick(product.id);
    							}}
    						>
    							+
    						</button>
    						<button
    							onClick={() => {
    								handleDecreaseClick(product.id);
    							}}
    						>
    							–
    						</button>
    					</li>
    				))}
    			</ul>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/y9yttz?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 3. Исправьте мутации, используя немутационные методы {#fix-the-mutations-using-non-mutative-methods}

В этом примере все обработчики событий в `App.js` используют мутацию. В результате редактирование и удаление `todos` не работает. Перепишите `handleAddTodo`, `handleChangeTodo` и `handleDeleteTodo`, чтобы они использовали немутационные методы:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AddTodo from './AddTodo.js';
    import TaskList from './TaskList.js';

    let nextId = 3;
    const initialTodos = [
    	{ id: 0, title: 'Buy milk', done: true },
    	{ id: 1, title: 'Eat tacos', done: false },
    	{ id: 2, title: 'Brew tea', done: false },
    ];

    export default function TaskApp() {
    	const [todos, setTodos] = useState(initialTodos);

    	function handleAddTodo(title) {
    		todos.push({
    			id: nextId++,
    			title: title,
    			done: false,
    		});
    	}

    	function handleChangeTodo(nextTodo) {
    		const todo = todos.find(
    			(t) => t.id === nextTodo.id
    		);
    		todo.title = nextTodo.title;
    		todo.done = nextTodo.done;
    	}

    	function handleDeleteTodo(todoId) {
    		const index = todos.findIndex(
    			(t) => t.id === todoId
    		);
    		todos.splice(index, 1);
    	}

    	return (
    		<>
    			<AddTodo onAddTodo={handleAddTodo} />
    			<TaskList
    				todos={todos}
    				onChangeTodo={handleChangeTodo}
    				onDeleteTodo={handleDeleteTodo}
    			/>
    		</>
    	);
    }
    ```

=== "AddTodo.js"

    ```js
    import { useState } from 'react';

    export default function AddTodo({ onAddTodo }) {
    	const [title, setTitle] = useState('');
    	return (
    		<>
    			<input
    				placeholder="Add todo"
    				value={title}
    				onChange={(e) => setTitle(e.target.value)}
    			/>
    			<button
    				onClick={() => {
    					setTitle('');
    					onAddTodo(title);
    				}}
    			>
    				Add
    			</button>
    		</>
    	);
    }
    ```

=== "TaskList.js"

    ```js
    import { useState } from 'react';

    export default function TaskList({
    	todos,
    	onChangeTodo,
    	onDeleteTodo,
    }) {
    	return (
    		<ul>
    			{todos.map((todo) => (
    				<li key={todo.id}>
    					<Task
    						todo={todo}
    						onChange={onChangeTodo}
    						onDelete={onDeleteTodo}
    					/>
    				</li>
    			))}
    		</ul>
    	);
    }

    function Task({ todo, onChange, onDelete }) {
    	const [isEditing, setIsEditing] = useState(false);
    	let todoContent;
    	if (isEditing) {
    		todoContent = (
    			<>
    				<input
    					value={todo.title}
    					onChange={(e) => {
    						onChange({
    							...todo,
    							title: e.target.value,
    						});
    					}}
    				/>
    				<button onClick={() => setIsEditing(false)}>
    					Save
    				</button>
    			</>
    		);
    	} else {
    		todoContent = (
    			<>
    				{todo.title}
    				<button onClick={() => setIsEditing(true)}>
    					Edit
    				</button>
    			</>
    		);
    	}
    	return (
    		<label>
    			<input
    				type="checkbox"
    				checked={todo.done}
    				onChange={(e) => {
    					onChange({
    						...todo,
    						done: e.target.checked,
    					});
    				}}
    			/>
    			{todoContent}
    			<button onClick={() => onDelete(todo.id)}>
    				Delete
    			</button>
    		</label>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/zhntxc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    В `handleAddTodo` вы можете использовать синтаксис распространения массива. В `handleChangeTodo` вы можете создать новый массив с помощью `map`. В `handleDeleteTodo` можно создать новый массив с помощью `filter`. Теперь список работает правильно:

    === "App.js"

    	```js
    	import { useState } from 'react';
    	import AddTodo from './AddTodo.js';
    	import TaskList from './TaskList.js';

    	let nextId = 3;
    	const initialTodos = [
    		{ id: 0, title: 'Buy milk', done: true },
    		{ id: 1, title: 'Eat tacos', done: false },
    		{ id: 2, title: 'Brew tea', done: false },
    	];

    	export default function TaskApp() {
    		const [todos, setTodos] = useState(initialTodos);

    		function handleAddTodo(title) {
    			setTodos([
    				...todos,
    				{
    					id: nextId++,
    					title: title,
    					done: false,
    				},
    			]);
    		}

    		function handleChangeTodo(nextTodo) {
    			setTodos(
    				todos.map((t) => {
    					if (t.id === nextTodo.id) {
    						return nextTodo;
    					} else {
    						return t;
    					}
    				})
    			);
    		}

    		function handleDeleteTodo(todoId) {
    			setTodos(todos.filter((t) => t.id !== todoId));
    		}

    		return (
    			<>
    				<AddTodo onAddTodo={handleAddTodo} />
    				<TaskList
    					todos={todos}
    					onChangeTodo={handleChangeTodo}
    					onDeleteTodo={handleDeleteTodo}
    				/>
    			</>
    		);
    	}
    	```

    === "AddTodo.js"

    	```js
    	import { useState } from 'react';

    	export default function AddTodo({ onAddTodo }) {
    		const [title, setTitle] = useState('');
    		return (
    			<>
    				<input
    					placeholder="Add todo"
    					value={title}
    					onChange={(e) => setTitle(e.target.value)}
    				/>
    				<button
    					onClick={() => {
    						setTitle('');
    						onAddTodo(title);
    					}}
    				>
    					Add
    				</button>
    			</>
    		);
    	}
    	```

    === "TaskList.js"

    	```js
    	import { useState } from 'react';

    	export default function TaskList({
    		todos,
    		onChangeTodo,
    		onDeleteTodo,
    	}) {
    		return (
    			<ul>
    				{todos.map((todo) => (
    					<li key={todo.id}>
    						<Task
    							todo={todo}
    							onChange={onChangeTodo}
    							onDelete={onDeleteTodo}
    						/>
    					</li>
    				))}
    			</ul>
    		);
    	}

    	function Task({ todo, onChange, onDelete }) {
    		const [isEditing, setIsEditing] = useState(false);
    		let todoContent;
    		if (isEditing) {
    			todoContent = (
    				<>
    					<input
    						value={todo.title}
    						onChange={(e) => {
    							onChange({
    								...todo,
    								title: e.target.value,
    							});
    						}}
    					/>
    					<button onClick={() => setIsEditing(false)}>
    						Save
    					</button>
    				</>
    			);
    		} else {
    			todoContent = (
    				<>
    					{todo.title}
    					<button onClick={() => setIsEditing(true)}>
    						Edit
    					</button>
    				</>
    			);
    		}
    		return (
    			<label>
    				<input
    					type="checkbox"
    					checked={todo.done}
    					onChange={(e) => {
    						onChange({
    							...todo,
    							done: e.target.checked,
    						});
    					}}
    				/>
    				{todoContent}
    				<button onClick={() => onDelete(todo.id)}>
    					Delete
    				</button>
    			</label>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/6hs78d?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 4. Исправьте мутации с помощью Immer {#fix-the-mutations-using-immer}

Это тот же пример, что и в предыдущей задаче. На этот раз исправьте мутации с помощью Immer. Для вашего удобства, `useImmer` уже импортирован, поэтому вам нужно изменить переменную состояния `todos`, чтобы использовать его.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useImmer } from 'use-immer';
    import AddTodo from './AddTodo.js';
    import TaskList from './TaskList.js';

    let nextId = 3;
    const initialTodos = [
    	{ id: 0, title: 'Buy milk', done: true },
    	{ id: 1, title: 'Eat tacos', done: false },
    	{ id: 2, title: 'Brew tea', done: false },
    ];

    export default function TaskApp() {
    	const [todos, setTodos] = useState(initialTodos);

    	function handleAddTodo(title) {
    		todos.push({
    			id: nextId++,
    			title: title,
    			done: false,
    		});
    	}

    	function handleChangeTodo(nextTodo) {
    		const todo = todos.find(
    			(t) => t.id === nextTodo.id
    		);
    		todo.title = nextTodo.title;
    		todo.done = nextTodo.done;
    	}

    	function handleDeleteTodo(todoId) {
    		const index = todos.findIndex(
    			(t) => t.id === todoId
    		);
    		todos.splice(index, 1);
    	}

    	return (
    		<>
    			<AddTodo onAddTodo={handleAddTodo} />
    			<TaskList
    				todos={todos}
    				onChangeTodo={handleChangeTodo}
    				onDeleteTodo={handleDeleteTodo}
    			/>
    		</>
    	);
    }
    ```

=== "AddTodo.js"

    ```js
    import { useState } from 'react';

    export default function AddTodo({ onAddTodo }) {
    	const [title, setTitle] = useState('');
    	return (
    		<>
    			<input
    				placeholder="Add todo"
    				value={title}
    				onChange={(e) => setTitle(e.target.value)}
    			/>
    			<button
    				onClick={() => {
    					setTitle('');
    					onAddTodo(title);
    				}}
    			>
    				Add
    			</button>
    		</>
    	);
    }
    ```

=== "TaskList.js"

    ```js
    import { useState } from 'react';

    export default function TaskList({
    	todos,
    	onChangeTodo,
    	onDeleteTodo,
    }) {
    	return (
    		<ul>
    			{todos.map((todo) => (
    				<li key={todo.id}>
    					<Task
    						todo={todo}
    						onChange={onChangeTodo}
    						onDelete={onDeleteTodo}
    					/>
    				</li>
    			))}
    		</ul>
    	);
    }

    function Task({ todo, onChange, onDelete }) {
    	const [isEditing, setIsEditing] = useState(false);
    	let todoContent;
    	if (isEditing) {
    		todoContent = (
    			<>
    				<input
    					value={todo.title}
    					onChange={(e) => {
    						onChange({
    							...todo,
    							title: e.target.value,
    						});
    					}}
    				/>
    				<button onClick={() => setIsEditing(false)}>
    					Save
    				</button>
    			</>
    		);
    	} else {
    		todoContent = (
    			<>
    				{todo.title}
    				<button onClick={() => setIsEditing(true)}>
    					Edit
    				</button>
    			</>
    		);
    	}
    	return (
    		<label>
    			<input
    				type="checkbox"
    				checked={todo.done}
    				onChange={(e) => {
    					onChange({
    						...todo,
    						done: e.target.checked,
    					});
    				}}
    			/>
    			{todoContent}
    			<button onClick={() => onDelete(todo.id)}>
    				Delete
    			</button>
    		</label>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/rs5nkk?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="wonderful-gould-rs5nkk" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    С Immer вы можете писать код мутативным способом, пока вы мутируете только части `draft`, который дает вам Immer. Здесь все мутации выполняются над `draft`, так что код работает:

    === "App.js"

    	```js
    	import { useState } from 'react';
    	import { useImmer } from 'use-immer';
    	import AddTodo from './AddTodo.js';
    	import TaskList from './TaskList.js';

    	let nextId = 3;
    	const initialTodos = [
    		{ id: 0, title: 'Buy milk', done: true },
    		{ id: 1, title: 'Eat tacos', done: false },
    		{ id: 2, title: 'Brew tea', done: false },
    	];

    	export default function TaskApp() {
    		const [todos, updateTodos] = useImmer(initialTodos);

    		function handleAddTodo(title) {
    			updateTodos((draft) => {
    				draft.push({
    					id: nextId++,
    					title: title,
    					done: false,
    				});
    			});
    		}

    		function handleChangeTodo(nextTodo) {
    			updateTodos((draft) => {
    				const todo = draft.find(
    					(t) => t.id === nextTodo.id
    				);
    				todo.title = nextTodo.title;
    				todo.done = nextTodo.done;
    			});
    		}

    		function handleDeleteTodo(todoId) {
    			updateTodos((draft) => {
    				const index = draft.findIndex(
    					(t) => t.id === todoId
    				);
    				draft.splice(index, 1);
    			});
    		}

    		return (
    			<>
    				<AddTodo onAddTodo={handleAddTodo} />
    				<TaskList
    					todos={todos}
    					onChangeTodo={handleChangeTodo}
    					onDeleteTodo={handleDeleteTodo}
    				/>
    			</>
    		);
    	}
    	```

    === "AddTodo.js"

    	```js
    	import { useState } from 'react';

    	export default function AddTodo({ onAddTodo }) {
    		const [title, setTitle] = useState('');
    		return (
    			<>
    				<input
    					placeholder="Add todo"
    					value={title}
    					onChange={(e) => setTitle(e.target.value)}
    				/>
    				<button
    					onClick={() => {
    						setTitle('');
    						onAddTodo(title);
    					}}
    				>
    					Add
    				</button>
    			</>
    		);
    	}
    	```

    === "TaskList.js"

    	```js
    	import { useState } from 'react';

    	export default function TaskList({
    		todos,
    		onChangeTodo,
    		onDeleteTodo,
    	}) {
    		return (
    			<ul>
    				{todos.map((todo) => (
    					<li key={todo.id}>
    						<Task
    							todo={todo}
    							onChange={onChangeTodo}
    							onDelete={onDeleteTodo}
    						/>
    					</li>
    				))}
    			</ul>
    		);
    	}

    	function Task({ todo, onChange, onDelete }) {
    		const [isEditing, setIsEditing] = useState(false);
    		let todoContent;
    		if (isEditing) {
    			todoContent = (
    				<>
    					<input
    						value={todo.title}
    						onChange={(e) => {
    							onChange({
    								...todo,
    								title: e.target.value,
    							});
    						}}
    					/>
    					<button onClick={() => setIsEditing(false)}>
    						Save
    					</button>
    				</>
    			);
    		} else {
    			todoContent = (
    				<>
    					{todo.title}
    					<button onClick={() => setIsEditing(true)}>
    						Edit
    					</button>
    				</>
    			);
    		}
    		return (
    			<label>
    				<input
    					type="checkbox"
    					checked={todo.done}
    					onChange={(e) => {
    						onChange({
    							...todo,
    							done: e.target.checked,
    						});
    					}}
    				/>
    				{todoContent}
    				<button onClick={() => onDelete(todo.id)}>
    					Delete
    				</button>
    			</label>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/6qyz5s?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="elastic-wave-6qyz5s" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Вы также можете смешивать и сочетать мутативные и немутативные подходы в Immer.

    Например, в этой версии `handleAddTodo` реализована путем мутации Immer `draft`, а `handleChangeTodo` и `handleDeleteTodo` используют немутативные методы `map` и `filter`:

    === "App.js"

    	```js
    	import { useState } from 'react';
    	import { useImmer } from 'use-immer';
    	import AddTodo from './AddTodo.js';
    	import TaskList from './TaskList.js';

    	let nextId = 3;
    	const initialTodos = [
    		{ id: 0, title: 'Buy milk', done: true },
    		{ id: 1, title: 'Eat tacos', done: false },
    		{ id: 2, title: 'Brew tea', done: false },
    	];

    	export default function TaskApp() {
    		const [todos, updateTodos] = useImmer(initialTodos);

    		function handleAddTodo(title) {
    			updateTodos((draft) => {
    				draft.push({
    					id: nextId++,
    					title: title,
    					done: false,
    				});
    			});
    		}

    		function handleChangeTodo(nextTodo) {
    			updateTodos(
    				todos.map((todo) => {
    					if (todo.id === nextTodo.id) {
    						return nextTodo;
    					} else {
    						return todo;
    					}
    				})
    			);
    		}

    		function handleDeleteTodo(todoId) {
    			updateTodos(todos.filter((t) => t.id !== todoId));
    		}

    		return (
    			<>
    				<AddTodo onAddTodo={handleAddTodo} />
    				<TaskList
    					todos={todos}
    					onChangeTodo={handleChangeTodo}
    					onDeleteTodo={handleDeleteTodo}
    				/>
    			</>
    		);
    	}
    	```

    === "AddTodo.js"

    	```js
    	import { useState } from 'react';

    	export default function AddTodo({ onAddTodo }) {
    		const [title, setTitle] = useState('');
    		return (
    			<>
    				<input
    					placeholder="Add todo"
    					value={title}
    					onChange={(e) => setTitle(e.target.value)}
    				/>
    				<button
    					onClick={() => {
    						setTitle('');
    						onAddTodo(title);
    					}}
    				>
    					Add
    				</button>
    			</>
    		);
    	}
    	```

    === "TaskList.js"

    	```js
    	import { useState } from 'react';

    	export default function TaskList({
    		todos,
    		onChangeTodo,
    		onDeleteTodo,
    	}) {
    		return (
    			<ul>
    				{todos.map((todo) => (
    					<li key={todo.id}>
    						<Task
    							todo={todo}
    							onChange={onChangeTodo}
    							onDelete={onDeleteTodo}
    						/>
    					</li>
    				))}
    			</ul>
    		);
    	}

    	function Task({ todo, onChange, onDelete }) {
    		const [isEditing, setIsEditing] = useState(false);
    		let todoContent;
    		if (isEditing) {
    			todoContent = (
    				<>
    					<input
    						value={todo.title}
    						onChange={(e) => {
    							onChange({
    								...todo,
    								title: e.target.value,
    							});
    						}}
    					/>
    					<button onClick={() => setIsEditing(false)}>
    						Save
    					</button>
    				</>
    			);
    		} else {
    			todoContent = (
    				<>
    					{todo.title}
    					<button onClick={() => setIsEditing(true)}>
    						Edit
    					</button>
    				</>
    			);
    		}
    		return (
    			<label>
    				<input
    					type="checkbox"
    					checked={todo.done}
    					onChange={(e) => {
    						onChange({
    							...todo,
    							done: e.target.checked,
    						});
    					}}
    				/>
    				{todoContent}
    				<button onClick={() => onDelete(todo.id)}>
    					Delete
    				</button>
    			</label>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/m4xw2k?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="brave-williamson-m4xw2k" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    С Immer вы можете выбрать стиль, который кажется наиболее естественным для каждого отдельного случая.

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/updating-arrays-in-state](https://react.dev/learn/updating-arrays-in-state)</small>
