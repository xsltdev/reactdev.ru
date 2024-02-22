---
description: Часто требуется отобразить несколько одинаковых компонентов из набора данных. Для работы с массивом данных можно использовать методы JavaScript массива. На этой странице вы будете использовать filter() и map() в React для фильтрации и преобразования массива данных в массив компонентов
---

# Рендеринг списков

<big>Часто требуется отобразить несколько одинаковых компонентов из набора данных. Для работы с массивом данных можно использовать методы [JavaScript массива](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array#). На этой странице вы будете использовать [`filter()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) и [`map()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map) в React для фильтрации и преобразования массива данных в массив компонентов.</big>

!!!tip "Вы узнаете"

    -   Как выводить компоненты из массива с помощью JavaScript `map()`.
    -   Как отобразить только определенные компоненты с помощью JavaScript `filter()`.
    -   Когда и зачем использовать ключи React

## Рендеринг данных из массивов {#rendering-data-from-arrays}

Допустим, у вас есть список содержимого.

```html
<ul>
    <li>Creola Katherine Johnson: mathematician</li>
    <li>Mario José Molina-Pasquel Henríquez: chemist</li>
    <li>Mohammad Abdus Salam: physicist</li>
    <li>Percy Lavon Julian: chemist</li>
    <li>Subrahmanyan Chandrasekhar: astrophysicist</li>
</ul>
```

Единственное различие между этими элементами списка — это их содержимое, их данные. При построении интерфейсов часто требуется отображать несколько экземпляров одного и того же компонента, используя разные данные: от списков комментариев до галерей изображений профиля. В таких ситуациях вы можете хранить эти данные в объектах и массивах JavaScript и использовать такие методы, как [`map()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map) и [`filter()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) для вывода списков компонентов на их основе.

Вот краткий пример того, как сформировать список элементов из массива:

**1. Переместите** данные в массив:

```js
const people = [
    'Creola Katherine Johnson: mathematician',
    'Mario José Molina-Pasquel Henríquez: chemist',
    'Mohammad Abdus Salam: physicist',
    'Percy Lavon Julian: chemist',
    'Subrahmanyan Chandrasekhar: astrophysicist',
];
```

**2. Мап** членов `people` в новый массив узлов JSX, `listItems`:

```js
const listItems = people.map((person) => <li>{person}</li>);
```

**3. Возвращает** `listItems` из вашего компонента, обернутого в `<ul>`:

```js
return <ul>{listItems}</ul>;
```

Вот результат:

=== "App.js"

    ```js
    const people = [
    	'Creola Katherine Johnson: mathematician',
    	'Mario José Molina-Pasquel Henríquez: chemist',
    	'Mohammad Abdus Salam: physicist',
    	'Percy Lavon Julian: chemist',
    	'Subrahmanyan Chandrasekhar: astrophysicist',
    ];

    export default function List() {
    	const listItems = people.map((person) => (
    		<li>{person}</li>
    	));
    	return <ul>{listItems}</ul>;
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/wykp7w?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

=== "Console"

    ```
    Warning: Each child in a list should have a unique "key" prop.

    Check the render method of `List`.
    See https://reactjs.org/link/warning-keys for more information.
    	at li
    	at List
    ```

Обратите внимание, что в песочнице выше отображается консольная ошибка:

!!!danger "Console"

    <pre style="white-space: normal">Warning: Each child in a list should have a unique “key” prop.</pre>

Как исправить эту ошибку, вы узнаете позже на этой странице. Прежде чем мы приступим к этому, давайте добавим немного структуры в ваши данные.

## Фильтрация массивов элементов {#filtering-arrays-of-items}

Эти данные можно структурировать еще больше.

```js
const people = [
    {
        id: 0,
        name: 'Creola Katherine Johnson',
        profession: 'mathematician',
    },
    {
        id: 1,
        name: 'Mario José Molina-Pasquel Henríquez',
        profession: 'chemist',
    },
    {
        id: 2,
        name: 'Mohammad Abdus Salam',
        profession: 'physicist',
    },
    {
        name: 'Percy Lavon Julian',
        profession: 'chemist',
    },
    {
        name: 'Subrahmanyan Chandrasekhar',
        profession: 'astrophysicist',
    },
];
```

Допустим, вам нужно показать только людей, чья профессия — `chemist`. Вы можете использовать метод JavaScript `filter()`, чтобы вернуть только таких людей. Этот метод принимает массив элементов, пропускает их через "тест" (функцию, которая возвращает `true` или `false`) и возвращает новый массив только тех элементов, которые прошли тест (вернули `true`).

Вам нужны только те элементы, где `profession` — `"chemist"`. Функция "test" для этого выглядит как `(person) => person.profession === 'chemist'`. Вот как это можно сделать:

**1.** **Создаем** новый массив только "химиков", `chemists`, вызывая `filter()` на `people`, фильтруя по `person.profession === 'chemist'`:

```js
const chemists = people.filter(
    (person) => person.profession === 'chemist'
);
```

**2.** Теперь **составьте карту** над `химиками`:

```js hl_lines="1 10"
const listItems = chemists.map((person) => (
    <li>
        <img src={getImageUrl(person)} alt={person.name} />
        <p>
            <b>{person.name}:</b>
            {' ' + person.profession + ' '}
            known for {person.accomplishment}
        </p>
    </li>
));
```

**3.** И наконец, **возвратите** список `listItems` из вашего компонента:

```js
return <ul>{listItems}</ul>;
```

=== "App.js"

    ```js
    import { people } from './data.js';
    import { getImageUrl } from './utils.js';

    export default function List() {
    	const chemists = people.filter(
    		(person) => person.profession === 'chemist'
    	);
    	const listItems = chemists.map((person) => (
    		<li>
    			<img
    				src={getImageUrl(person)}
    				alt={person.name}
    			/>
    			<p>
    				<b>{person.name}:</b>
    				{' ' + person.profession + ' '}
    				known for {person.accomplishment}
    			</p>
    		</li>
    	));
    	return <ul>{listItems}</ul>;
    }
    ```

=== "data.js"

    ```js
    export const people = [
    	{
    		id: 0,
    		name: 'Creola Katherine Johnson',
    		profession: 'mathematician',
    		accomplishment: 'spaceflight calculations',
    		imageId: 'MK3eW3A',
    	},
    	{
    		id: 1,
    		name: 'Mario José Molina-Pasquel Henríquez',
    		profession: 'chemist',
    		accomplishment: 'discovery of Arctic ozone hole',
    		imageId: 'mynHUSa',
    	},
    	{
    		id: 2,
    		name: 'Mohammad Abdus Salam',
    		profession: 'physicist',
    		accomplishment: 'electromagnetism theory',
    		imageId: 'bE7W1ji',
    	},
    	{
    		id: 3,
    		name: 'Percy Lavon Julian',
    		profession: 'chemist',
    		accomplishment:
    			'pioneering cortisone drugs, steroids and birth control pills',
    		imageId: 'IOjWm71',
    	},
    	{
    		id: 4,
    		name: 'Subrahmanyan Chandrasekhar',
    		profession: 'astrophysicist',
    		accomplishment:
    			'white dwarf star mass calculations',
    		imageId: 'lrWQx8l',
    	},
    ];
    ```

=== "utils.js"

    ```js
    export function getImageUrl(person) {
    	return (
    		'https://i.imgur.com/' + person.imageId + 's.jpg'
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/wz4mln?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!warning "Внимание"

    Стрелочные функции неявно возвращают выражение сразу после `=>`, поэтому оператор `возврата` не нужен:

    ```js
    const listItems = chemists.map(
    	(person) => <li>...</li> // Implicit return!
    );
    ```

    Однако **вы должны явно написать `return`, если за вашим `=>` следует `{` фигурная скобка\!**.

    ```js
    const listItems = chemists.map((person) => {
    	// Curly brace
    	return <li>...</li>;
    });
    ```

    Стрелочные функции, содержащие `=> {`, как говорят, имеют ["тело блока"](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Functions/Arrow_functions#function_body). Они позволяют вам написать больше, чем одну строку кода, но вы _должны_ сами написать оператор `возврата`. Если вы забудете об этом, ничего не будет возвращено!

## Упорядочивание элементов списка по `key` {#keeping-list-items-in-order-with-key}

Обратите внимание, что все приведенные выше песочницы выдают ошибку в консоли:

!!!danger "Console"

    <pre style="white-space: normal">Warning: Each child in a list should have a unique “key” prop.</pre>

Вам нужно дать каждому элементу массива `key` — строку или число, которое уникально идентифицирует его среди других элементов этого массива:

```js
<li key={person.id}>...</li>
```

!!!note "Ключи внутри map()"

    JSX-элементы непосредственно внутри вызова `map()` всегда нуждаются в ключах!

Ключи указывают React, какому элементу массива соответствует каждый компонент, чтобы он мог сопоставить их позже. Это становится важным, если элементы массива могут перемещаться (например, из-за сортировки), вставляться или удаляться. Хорошо подобранный `key` помогает React понять, что именно произошло, и сделать правильные обновления в DOM-дереве.

Вместо того чтобы генерировать ключи "на лету", вы должны включать их в свои данные:

=== "App.js"

    ```js
    import { people } from './data.js';
    import { getImageUrl } from './utils.js';

    export default function List() {
    	const listItems = people.map((person) => (
    		<li key={person.id}>
    			<img
    				src={getImageUrl(person)}
    				alt={person.name}
    			/>
    			<p>
    				<b>{person.name}</b>
    				{' ' + person.profession + ' '}
    				known for {person.accomplishment}
    			</p>
    		</li>
    	));
    	return <ul>{listItems}</ul>;
    }
    ```

=== "data.js"

    ```js
    export const people = [
    	{
    		id: 0, // Used in JSX as a key
    		name: 'Creola Katherine Johnson',
    		profession: 'mathematician',
    		accomplishment: 'spaceflight calculations',
    		imageId: 'MK3eW3A',
    	},
    	{
    		id: 1, // Used in JSX as a key
    		name: 'Mario José Molina-Pasquel Henríquez',
    		profession: 'chemist',
    		accomplishment: 'discovery of Arctic ozone hole',
    		imageId: 'mynHUSa',
    	},
    	{
    		id: 2, // Used in JSX as a key
    		name: 'Mohammad Abdus Salam',
    		profession: 'physicist',
    		accomplishment: 'electromagnetism theory',
    		imageId: 'bE7W1ji',
    	},
    	{
    		id: 3, // Used in JSX as a key
    		name: 'Percy Lavon Julian',
    		profession: 'chemist',
    		accomplishment:
    			'pioneering cortisone drugs, steroids and birth control pills',
    		imageId: 'IOjWm71',
    	},
    	{
    		id: 4, // Used in JSX as a key
    		name: 'Subrahmanyan Chandrasekhar',
    		profession: 'astrophysicist',
    		accomplishment:
    			'white dwarf star mass calculations',
    		imageId: 'lrWQx8l',
    	},
    ];
    ```

=== "utils.js"

    ```js
    export function getImageUrl(person) {
    	return (
    		'https://i.imgur.com/' + person.imageId + 's.jpg'
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/8cdgfk?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Отображение нескольких узлов DOM для каждого элемента списка"

    Что делать, если каждый элемент должен отображать не один, а несколько узлов DOM?

    Короткий синтаксис [<code>&lt;&gt;...&lt;/&gt;</code> Fragment](../reference/react/Fragment.md) не позволит вам передать ключ, поэтому вам нужно либо сгруппировать их в один `<div>`, либо использовать немного более длинный и более явный синтаксис `<Fragment>`:

    ```js
    import { Fragment } from 'react';

    // ...

    const listItems = people.map((person) => (
    	<Fragment key={person.id}>
    		<h1>{person.name}</h1>
    		<p>{person.bio}</p>
    	</Fragment>
    ));
    ```

    Фрагменты исчезают из DOM, поэтому будет получен плоский список `<h1>`, `<p>`, `<h1>`, `<p>` и так далее.

### Где взять ваш `key` {#where-to-get-your-key}

Различные источники данных предоставляют различные источники ключей:

-   **Данные из базы данных:** Если ваши данные поступают из базы данных, вы можете использовать ключи/идентификаторы базы данных, которые уникальны по своей природе.
-   **Локально генерируемые данные:** Если ваши данные генерируются и сохраняются локально (например, заметки в приложении для ведения записей), при создании элементов используйте инкрементирующий счетчик, [`crypto.randomUUID()`](https://developer.mozilla.org/docs/Web/API/Crypto/randomUUID) или пакет типа [`uuid`](https://www.npmjs.com/package/uuid).

### Правила ключей {#rules-of-keys}

-   **Ключи должны быть уникальными среди братьев и сестер.** Однако, можно использовать одинаковые ключи для JSX-узлов в _разных_ массивах.
-   **Ключи не должны меняться**, иначе это противоречит их назначению! Не генерируйте их во время рендеринга.

### Зачем React нужны ключи? {#why-does-react-need-keys}

Представьте, что файлы на вашем рабочем столе не имеют имен. Вместо этого вы обращаетесь к ним по порядку — первый файл, второй файл и так далее. К этому можно было бы привыкнуть, но когда вы удалите файл, все запутается. Второй файл станет первым, третий — вторым и так далее.

Имена файлов в папке и JSX-ключи в массиве служат аналогичной цели. Они позволяют нам однозначно идентифицировать элемент между его родственниками. Хорошо подобранный ключ предоставляет больше информации, чем позиция в массиве. Даже если _позиция_ меняется из-за переупорядочивания, `key` позволяет React идентифицировать элемент на протяжении всего его существования.

!!!warning "Внимание"

    У вас может возникнуть соблазн использовать индекс элемента в массиве в качестве ключа. На самом деле, именно это будет использовать React, если вы вообще не укажете `key`. Но порядок, в котором вы отображаете элементы, будет меняться со временем, если элемент будет вставлен, удален или массив будет переупорядочен. Индекс в качестве ключа часто приводит к тонким и запутанным ошибкам.

    Аналогично, не генерируйте ключи на лету, например, с помощью `key={Math.random()}`. Это приведет к тому, что ключи никогда не будут совпадать между рендерами, что приведет к тому, что все ваши компоненты и DOM будут каждый раз создаваться заново. Это не только медленно, но и приведет к потере пользовательского ввода внутри элементов списка. Вместо этого используйте стабильный идентификатор, основанный на данных.

    Обратите внимание, что ваши компоненты не будут получать `key` в качестве пропса. Он используется только в качестве подсказки самим React. Если вашему компоненту нужен ID, вы должны передать его как отдельный пропс: `<Profile key={id} userId={id} />`.

!!!note "Итоги"

    На этой странице вы узнали:

    -   Как перемещать данные из компонентов в структуры данных, такие как массивы и объекты.
    -   Как генерировать наборы похожих компонентов с помощью функции JavaScript `map()`.
    -   Как создавать массивы отфильтрованных элементов с помощью функции JavaScript `filter()`.
    -   Зачем и как устанавливать `key` для каждого компонента в коллекции, чтобы React мог отслеживать каждый из них, даже если их положение или данные меняются.

## Задачи {#challenges}

### 1. Разделение списка на две части {#splitting-a-list-in-two}

В этом примере показан список всех людей.

Измените его, чтобы последовательно вывести два отдельных списка: **Химики** и **Все остальные.** Как и ранее, вы можете определить, является ли человек химиком, проверив, что `person.profession === 'chemist'`.

=== "App.js"

    ```js
    import { people } from './data.js';
    import { getImageUrl } from './utils.js';

    export default function List() {
    	const listItems = people.map((person) => (
    		<li key={person.id}>
    			<img
    				src={getImageUrl(person)}
    				alt={person.name}
    			/>
    			<p>
    				<b>{person.name}:</b>
    				{' ' + person.profession + ' '}
    				known for {person.accomplishment}
    			</p>
    		</li>
    	));
    	return (
    		<article>
    			<h1>Scientists</h1>
    			<ul>{listItems}</ul>
    		</article>
    	);
    }
    ```

=== "data.js"

    ```js
    export const people = [
    	{
    		id: 0,
    		name: 'Creola Katherine Johnson',
    		profession: 'mathematician',
    		accomplishment: 'spaceflight calculations',
    		imageId: 'MK3eW3A',
    	},
    	{
    		id: 1,
    		name: 'Mario José Molina-Pasquel Henríquez',
    		profession: 'chemist',
    		accomplishment: 'discovery of Arctic ozone hole',
    		imageId: 'mynHUSa',
    	},
    	{
    		id: 2,
    		name: 'Mohammad Abdus Salam',
    		profession: 'physicist',
    		accomplishment: 'electromagnetism theory',
    		imageId: 'bE7W1ji',
    	},
    	{
    		id: 3,
    		name: 'Percy Lavon Julian',
    		profession: 'chemist',
    		accomplishment:
    			'pioneering cortisone drugs, steroids and birth control pills',
    		imageId: 'IOjWm71',
    	},
    	{
    		id: 4,
    		name: 'Subrahmanyan Chandrasekhar',
    		profession: 'astrophysicist',
    		accomplishment:
    			'white dwarf star mass calculations',
    		imageId: 'lrWQx8l',
    	},
    ];
    ```

=== "utils.js"

    ```js
    export function getImageUrl(person) {
    	return (
    		'https://i.imgur.com/' + person.imageId + 's.jpg'
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/dmv7s7?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Вы можете использовать `filter()` дважды, создавая два отдельных массива, а затем `map` над обоими массивами:

    === "App.js"

    	```js
    	import { people } from './data.js';
    	import { getImageUrl } from './utils.js';

    	export default function List() {
    		const chemists = people.filter(
    			(person) => person.profession === 'chemist'
    		);
    		const everyoneElse = people.filter(
    			(person) => person.profession !== 'chemist'
    		);
    		return (
    			<article>
    				<h1>Scientists</h1>
    				<h2>Chemists</h2>
    				<ul>
    					{chemists.map((person) => (
    						<li key={person.id}>
    							<img
    								src={getImageUrl(person)}
    								alt={person.name}
    							/>
    							<p>
    								<b>{person.name}:</b>
    								{' ' + person.profession + ' '}
    								known for{' '}
    								{person.accomplishment}
    							</p>
    						</li>
    					))}
    				</ul>
    				<h2>Everyone Else</h2>
    				<ul>
    					{everyoneElse.map((person) => (
    						<li key={person.id}>
    							<img
    								src={getImageUrl(person)}
    								alt={person.name}
    							/>
    							<p>
    								<b>{person.name}:</b>
    								{' ' + person.profession + ' '}
    								known for{' '}
    								{person.accomplishment}
    							</p>
    						</li>
    					))}
    				</ul>
    			</article>
    		);
    	}
    	```

    === "data.js"

    	```js
    	export const people = [
    		{
    			id: 0,
    			name: 'Creola Katherine Johnson',
    			profession: 'mathematician',
    			accomplishment: 'spaceflight calculations',
    			imageId: 'MK3eW3A',
    		},
    		{
    			id: 1,
    			name: 'Mario José Molina-Pasquel Henríquez',
    			profession: 'chemist',
    			accomplishment: 'discovery of Arctic ozone hole',
    			imageId: 'mynHUSa',
    		},
    		{
    			id: 2,
    			name: 'Mohammad Abdus Salam',
    			profession: 'physicist',
    			accomplishment: 'electromagnetism theory',
    			imageId: 'bE7W1ji',
    		},
    		{
    			id: 3,
    			name: 'Percy Lavon Julian',
    			profession: 'chemist',
    			accomplishment:
    				'pioneering cortisone drugs, steroids and birth control pills',
    			imageId: 'IOjWm71',
    		},
    		{
    			id: 4,
    			name: 'Subrahmanyan Chandrasekhar',
    			profession: 'astrophysicist',
    			accomplishment:
    				'white dwarf star mass calculations',
    			imageId: 'lrWQx8l',
    		},
    	];
    	```

    === "utils.js"

    	```js
    	export function getImageUrl(person) {
    		return (
    			'https://i.imgur.com/' + person.imageId + 's.jpg'
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/956sdv?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    В данном решении вызовы `map` размещены непосредственно в родительских элементах `<ul>`, но вы можете ввести для них переменные, если считаете это более читабельным.

    Между отображаемыми списками все еще есть некоторое дублирование. Можно пойти дальше и извлечь повторяющиеся части в компонент `<ListSection>`:

    === "App.js"

    	```js
    	import { people } from './data.js';
    	import { getImageUrl } from './utils.js';

    	function ListSection({ title, people }) {
    		return (
    			<>
    				<h2>{title}</h2>
    				<ul>
    					{people.map((person) => (
    						<li key={person.id}>
    							<img
    								src={getImageUrl(person)}
    								alt={person.name}
    							/>
    							<p>
    								<b>{person.name}:</b>
    								{' ' + person.profession + ' '}
    								known for{' '}
    								{person.accomplishment}
    							</p>
    						</li>
    					))}
    				</ul>
    			</>
    		);
    	}

    	export default function List() {
    		const chemists = people.filter(
    			(person) => person.profession === 'chemist'
    		);
    		const everyoneElse = people.filter(
    			(person) => person.profession !== 'chemist'
    		);
    		return (
    			<article>
    				<h1>Scientists</h1>
    				<ListSection
    					title="Chemists"
    					people={chemists}
    				/>
    				<ListSection
    					title="Everyone Else"
    					people={everyoneElse}
    				/>
    			</article>
    		);
    	}
    	```

    === "data.js"

    	```js
    	export const people = [
    		{
    			id: 0,
    			name: 'Creola Katherine Johnson',
    			profession: 'mathematician',
    			accomplishment: 'spaceflight calculations',
    			imageId: 'MK3eW3A',
    		},
    		{
    			id: 1,
    			name: 'Mario José Molina-Pasquel Henríquez',
    			profession: 'chemist',
    			accomplishment: 'discovery of Arctic ozone hole',
    			imageId: 'mynHUSa',
    		},
    		{
    			id: 2,
    			name: 'Mohammad Abdus Salam',
    			profession: 'physicist',
    			accomplishment: 'electromagnetism theory',
    			imageId: 'bE7W1ji',
    		},
    		{
    			id: 3,
    			name: 'Percy Lavon Julian',
    			profession: 'chemist',
    			accomplishment:
    				'pioneering cortisone drugs, steroids and birth control pills',
    			imageId: 'IOjWm71',
    		},
    		{
    			id: 4,
    			name: 'Subrahmanyan Chandrasekhar',
    			profession: 'astrophysicist',
    			accomplishment:
    				'white dwarf star mass calculations',
    			imageId: 'lrWQx8l',
    		},
    	];
    	```

    === "utils.js"

    	```js
    	export function getImageUrl(person) {
    		return (
    			'https://i.imgur.com/' + person.imageId + 's.jpg'
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/vw6w5l?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Очень внимательный читатель может заметить, что при двух вызовах `filter` мы проверяем профессию каждого человека дважды. Проверка свойства происходит очень быстро, поэтому в данном примере это нормально. Если бы ваша логика была более дорогой, вы могли бы заменить вызовы `filter` циклом, который вручную строит массивы и проверяет каждого человека один раз.

    На самом деле, если `people` никогда не меняется, вы можете вынести этот код за пределы вашего компонента. С точки зрения React, все, что имеет значение, это то, что в конечном итоге вы даете ему массив JSX-узлов. Ему все равно, как вы создадите этот массив:

    === "App.js"

    	```js
    	import { people } from './data.js';
    	import { getImageUrl } from './utils.js';

    	let chemists = [];
    	let everyoneElse = [];
    	people.forEach((person) => {
    		if (person.profession === 'chemist') {
    			chemists.push(person);
    		} else {
    			everyoneElse.push(person);
    		}
    	});

    	function ListSection({ title, people }) {
    		return (
    			<>
    				<h2>{title}</h2>
    				<ul>
    					{people.map((person) => (
    						<li key={person.id}>
    							<img
    								src={getImageUrl(person)}
    								alt={person.name}
    							/>
    							<p>
    								<b>{person.name}:</b>
    								{' ' + person.profession + ' '}
    								known for{' '}
    								{person.accomplishment}
    							</p>
    						</li>
    					))}
    				</ul>
    			</>
    		);
    	}

    	export default function List() {
    		return (
    			<article>
    				<h1>Scientists</h1>
    				<ListSection
    					title="Chemists"
    					people={chemists}
    				/>
    				<ListSection
    					title="Everyone Else"
    					people={everyoneElse}
    				/>
    			</article>
    		);
    	}
    	```

    === "data.js"

    	```js
    	export const people = [
    		{
    			id: 0,
    			name: 'Creola Katherine Johnson',
    			profession: 'mathematician',
    			accomplishment: 'spaceflight calculations',
    			imageId: 'MK3eW3A',
    		},
    		{
    			id: 1,
    			name: 'Mario José Molina-Pasquel Henríquez',
    			profession: 'chemist',
    			accomplishment: 'discovery of Arctic ozone hole',
    			imageId: 'mynHUSa',
    		},
    		{
    			id: 2,
    			name: 'Mohammad Abdus Salam',
    			profession: 'physicist',
    			accomplishment: 'electromagnetism theory',
    			imageId: 'bE7W1ji',
    		},
    		{
    			id: 3,
    			name: 'Percy Lavon Julian',
    			profession: 'chemist',
    			accomplishment:
    				'pioneering cortisone drugs, steroids and birth control pills',
    			imageId: 'IOjWm71',
    		},
    		{
    			id: 4,
    			name: 'Subrahmanyan Chandrasekhar',
    			profession: 'astrophysicist',
    			accomplishment:
    				'white dwarf star mass calculations',
    			imageId: 'lrWQx8l',
    		},
    	];
    	```

    === "utils.js"

    	```js
    	export function getImageUrl(person) {
    		return (
    			'https://i.imgur.com/' + person.imageId + 's.jpg'
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/tklwgq?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 2. Вложенные списки в одном компоненте {#nested-lists-in-one-component}

Создайте список рецептов из этого массива! Для каждого рецепта в массиве выведите его название в виде `<h2>` и список ингредиентов в виде `<ul>`.

Это потребует вложения двух различных вызовов `map`.

=== "App.js"

    ```js
    import { recipes } from './data.js';

    export default function RecipeList() {
    	return (
    		<div>
    			<h1>Recipes</h1>
    		</div>
    	);
    }
    ```

=== "data.js"

    ```js
    export const recipes = [
    	{
    		id: 'greek-salad',
    		name: 'Greek Salad',
    		ingredients: [
    			'tomatoes',
    			'cucumber',
    			'onion',
    			'olives',
    			'feta',
    		],
    	},
    	{
    		id: 'hawaiian-pizza',
    		name: 'Hawaiian Pizza',
    		ingredients: [
    			'pizza crust',
    			'pizza sauce',
    			'mozzarella',
    			'ham',
    			'pineapple',
    		],
    	},
    	{
    		id: 'hummus',
    		name: 'Hummus',
    		ingredients: [
    			'chickpeas',
    			'olive oil',
    			'garlic cloves',
    			'lemon',
    			'tahini',
    		],
    	},
    ];
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/sh2fz3?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Это потребует вложения двух различных вызовов `map`.

???success "Показать решение"

    Вот один из способов, которым вы можете воспользоваться:

    === "App.js"

    	```js
    	import { recipes } from './data.js';

    	export default function RecipeList() {
    		return (
    			<div>
    				<h1>Recipes</h1>
    				{recipes.map((recipe) => (
    					<div key={recipe.id}>
    						<h2>{recipe.name}</h2>
    						<ul>
    							{recipe.ingredients.map(
    								(ingredient) => (
    									<li key={ingredient}>
    										{ingredient}
    									</li>
    								)
    							)}
    						</ul>
    					</div>
    				))}
    			</div>
    		);
    	}
    	```

    === "data.js"

    	```js
    	export const recipes = [
    		{
    			id: 'greek-salad',
    			name: 'Greek Salad',
    			ingredients: [
    				'tomatoes',
    				'cucumber',
    				'onion',
    				'olives',
    				'feta',
    			],
    		},
    		{
    			id: 'hawaiian-pizza',
    			name: 'Hawaiian Pizza',
    			ingredients: [
    				'pizza crust',
    				'pizza sauce',
    				'mozzarella',
    				'ham',
    				'pineapple',
    			],
    		},
    		{
    			id: 'hummus',
    			name: 'Hummus',
    			ingredients: [
    				'chickpeas',
    				'olive oil',
    				'garlic cloves',
    				'lemon',
    				'tahini',
    			],
    		},
    	];
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/hv95s2?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Каждый из `recipes` уже содержит поле `id`, поэтому именно его использует внешний цикл для своего `key`. Нет никакого идентификатора, который можно было бы использовать для перебора ингредиентов. Однако разумно предположить, что один и тот же ингредиент не будет указан дважды в одном рецепте, поэтому его название может служить в качестве `key`. В качестве альтернативы можно изменить структуру данных, добавив идентификаторы, или использовать индекс в качестве `key` (с оговоркой, что вы не сможете безопасно переупорядочить ингредиенты).

### 3. Извлечение компонента элемента списка {#extracting-a-list-item-component}

Этот компонент `RecipeList` содержит два вложенных вызова `map`. Чтобы упростить его, извлеките из него компонент `Recipe`, который будет принимать пропсы `id`, `name` и `ingredients`. Где вы разместите внешний `key` и почему?

=== "App.js"

    ```js
    import { recipes } from './data.js';

    export default function RecipeList() {
    	return (
    		<div>
    			<h1>Recipes</h1>
    			{recipes.map((recipe) => (
    				<div key={recipe.id}>
    					<h2>{recipe.name}</h2>
    					<ul>
    						{recipe.ingredients.map(
    							(ingredient) => (
    								<li key={ingredient}>
    									{ingredient}
    								</li>
    							)
    						)}
    					</ul>
    				</div>
    			))}
    		</div>
    	);
    }
    ```

=== "data.js"

    ```js
    export const recipes = [
    	{
    		id: 'greek-salad',
    		name: 'Greek Salad',
    		ingredients: [
    			'tomatoes',
    			'cucumber',
    			'onion',
    			'olives',
    			'feta',
    		],
    	},
    	{
    		id: 'hawaiian-pizza',
    		name: 'Hawaiian Pizza',
    		ingredients: [
    			'pizza crust',
    			'pizza sauce',
    			'mozzarella',
    			'ham',
    			'pineapple',
    		],
    	},
    	{
    		id: 'hummus',
    		name: 'Hummus',
    		ingredients: [
    			'chickpeas',
    			'olive oil',
    			'garlic cloves',
    			'lemon',
    			'tahini',
    		],
    	},
    ];
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/hv95s2?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Вы можете скопировать-вставить JSX из внешней `map` в новый компонент `Recipe` и вернуть этот JSX. Затем вы можете изменить `recipe.name` на `name`, `recipe.id` на `id`, и так далее, и передать их в качестве пропсов в `Recipe`:

    === "App.js"

    	```js
    	import { recipes } from './data.js';

    	function Recipe({ id, name, ingredients }) {
    		return (
    			<div>
    				<h2>{name}</h2>
    				<ul>
    					{ingredients.map((ingredient) => (
    						<li key={ingredient}>{ingredient}</li>
    					))}
    				</ul>
    			</div>
    		);
    	}

    	export default function RecipeList() {
    		return (
    			<div>
    				<h1>Recipes</h1>
    				{recipes.map((recipe) => (
    					<Recipe {...recipe} key={recipe.id} />
    				))}
    			</div>
    		);
    	}
    	```

    === "data.js"

    	```js
    	export const recipes = [
    		{
    			id: 'greek-salad',
    			name: 'Greek Salad',
    			ingredients: [
    				'tomatoes',
    				'cucumber',
    				'onion',
    				'olives',
    				'feta',
    			],
    		},
    		{
    			id: 'hawaiian-pizza',
    			name: 'Hawaiian Pizza',
    			ingredients: [
    				'pizza crust',
    				'pizza sauce',
    				'mozzarella',
    				'ham',
    				'pineapple',
    			],
    		},
    		{
    			id: 'hummus',
    			name: 'Hummus',
    			ingredients: [
    				'chickpeas',
    				'olive oil',
    				'garlic cloves',
    				'lemon',
    				'tahini',
    			],
    		},
    	];
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/2g4rnl?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Здесь `<Recipe {...recipe} key={recipe.id} />` — это синтаксическое сокращение, говорящее "передать все свойства объекта `recipe` в качестве пропсов компоненту `Recipe`". Вы также можете записать каждый пропс в явном виде: `<Recipe id={recipe.id} name={recipe.name} ingredients={recipe.ingredients} key={recipe.id} />`.

    **Обратите внимание, что `key` указывается на самом `<Recipe>`, а не на корне `<div>`, возвращаемом из `Recipe`**. Это потому, что этот `key` нужен непосредственно в контексте окружающего массива. Раньше у вас был массив `<div>`, и каждый из них нуждался в `key`, а теперь у вас есть массив `<Recipe>`. Другими словами, когда вы извлекаете компонент, не забудьте оставить `key` вне JSX, который вы копируете и вставляете.

### 4. Список с разделителем {#list-with-a-separator}

Этот пример отображает знаменитое хайку Кацусики Хокусая, каждая строка которого обернута в тег `<p>`. Ваша задача — вставить разделитель `<hr />` между каждым абзацем. Ваша результирующая структура должна выглядеть следующим образом:

```html
<article>
    <p>I write, erase, rewrite</p>
    <hr />
    <p>Erase again, and then</p>
    <hr />
    <p>A poppy blooms.</p>
</article>
```

В хайку всего три строки, но ваше решение должно работать с любым количеством строк. Обратите внимание, что элементы `<hr />` появляются только _между_ элементами `<p>`, а не в начале или конце!

=== "App.js"

    ```js
    const poem = {
    	lines: [
    		'I write, erase, rewrite',
    		'Erase again, and then',
    		'A poppy blooms.',
    	],
    };

    export default function Poem() {
    	return (
    		<article>
    			{poem.lines.map((line, index) => (
    				<p key={index}>{line}</p>
    			))}
    		</article>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/dt98cj?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Это редкий случай, когда индекс в качестве ключа допустим, потому что строки стихотворения никогда не будут перестраиваться.

???tip "Показать подсказку"

    Вам нужно либо преобразовать `map` в ручной цикл, либо использовать фрагмент.

???success "Показать решение"

    Вы можете написать ручной цикл, вставляя `<hr />` и `<p>...</p>` в выходной массив по мере выполнения:

    === "App.js"

    	```js
    	const poem = {
    		lines: [
    			'I write, erase, rewrite',
    			'Erase again, and then',
    			'A poppy blooms.',
    		],
    	};

    	export default function Poem() {
    		let output = [];

    		// Fill the output array
    		poem.lines.forEach((line, i) => {
    			output.push(<hr key={i + '-separator'} />);
    			output.push(<p key={i + '-text'}>{line}</p>);
    		});
    		// Remove the first <hr />
    		output.shift();

    		return <article>{output}</article>;
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/rf3qh5?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Использование исходного индекса строки в качестве `key` больше не работает, поскольку каждый разделитель и абзац теперь находятся в одном массиве. Однако вы можете дать каждому из них отдельный ключ, используя суффикс, например, `key={i + '-text'}`.

    В качестве альтернативы можно вывести коллекцию фрагментов, содержащих `<hr />` и `<p>...</p>`. Однако синтаксис сокращения <code>&lt;>...&lt;/></code> не поддерживает передачу ключей, поэтому вам придется явно написать `<Fragment>`:

    === "App.js"

    	```js
    	import { Fragment } from 'react';

    	const poem = {
    		lines: [
    			'I write, erase, rewrite',
    			'Erase again, and then',
    			'A poppy blooms.',
    		],
    	};

    	export default function Poem() {
    		return (
    			<article>
    				{poem.lines.map((line, i) => (
    					<Fragment key={i}>
    						{i > 0 && <hr />}
    						<p>{line}</p>
    					</Fragment>
    				))}
    			</article>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/syqgzq?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Помните, что фрагменты (часто записываемые как <code>&lt;>...&lt;/&gt;</code>) позволяют вам группировать узлы JSX без добавления лишних `<div>`!

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/rendering-lists](https://react.dev/learn/rendering-lists)</small>
