---
description: Состояние может хранить любые значения JavaScript, включая объекты. Но вы не должны изменять объекты, которые хранятся в состоянии React, напрямую. Вместо этого, когда вы хотите обновить объект, вам нужно создать новый
---

# Обновление объектов в состоянии

<big>Состояние может хранить любые значения JavaScript, включая объекты. Но вы не должны изменять объекты, которые хранятся в состоянии React, напрямую. Вместо этого, когда вы хотите обновить объект, вам нужно создать новый (или сделать копию существующего), а затем настроить состояние на использование этой копии.</big>

!!!tip "Вы узнаете"

    -   Как правильно обновить объект в состоянии React
    -   Как обновить вложенный объект без его мутирования
    -   Что такое неизменяемость и как ее не нарушить
    -   Как сделать копирование объектов менее повторяющимся с помощью Immer

## Что такое мутация? {#whats-a-mutation}

В состоянии можно хранить любые значения JavaScript.

```js
const [x, setX] = useState(0);
```

До сих пор вы работали с числами, строками и булевыми числами. Эти типы значений JavaScript являются "неизменяемыми", то есть неизменяемыми или "только для чтения". Чтобы _заменить_ значение, можно вызвать повторный рендеринг:

```js
setX(5);
```

Состояние `x` изменилось с `0` на `5`, но само число `0` не изменилось. В JavaScript невозможно внести какие-либо изменения во встроенные примитивные значения, такие как числа, строки и булевы.

Теперь рассмотрим объект в состоянии:

```js
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Технически, можно изменить содержимое _самого объекта_. **Это называется мутацией:**.

```js
position.x = 5;
```

Однако, хотя объекты в React state технически являются изменяемыми, вы должны относиться к ним **как** к неизменяемым, как к числам, булевым числам и строкам. Вместо того чтобы изменять их, вы всегда должны заменять их.

## Рассматривайте состояние как доступное только для чтения {#treat-state-as-read-only}

Другими словами, вы должны _относиться к любому объекту JavaScript, который вы помещаете в состояние, как к объекту только для чтения_.

В этом примере в состоянии находится объект, представляющий текущее положение указателя. Красная точка должна перемещаться при касании или перемещении курсора по области предварительного просмотра. Но точка остается в исходном положении:

=== "App.js"

    ```js
    import { useState } from 'react';
    export default function MovingDot() {
    	const [position, setPosition] = useState({
    		x: 0,
    		y: 0,
    	});
    	return (
    		<div
    			onPointerMove={(e) => {
    				position.x = e.clientX;
    				position.y = e.clientY;
    			}}
    			style={{
    				position: 'relative',
    				width: '100vw',
    				height: '100vh',
    			}}
    		>
    			<div
    				style={{
    					position: 'absolute',
    					backgroundColor: 'red',
    					borderRadius: '50%',
    					transform: `translate(${position.x}px, ${position.y}px)`,
    					left: -10,
    					top: -10,
    					width: 20,
    					height: 20,
    				}}
    			/>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/pytl78?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Проблема заключается в этом фрагменте кода.

```js
onPointerMove={e => {
  position.x = e.clientX;
  position.y = e.clientY;
}}
```

Этот код изменяет объект, назначенный на `position` из [предыдущего рендера](state-as-a-snapshot.md#rendering-takes-a-snapshot-in-time). Но без использования функции установки состояния React не знает, что объект изменился. Поэтому React ничего не делает в ответ. Это все равно что пытаться изменить заказ после того, как вы уже поели. Хотя мутирование состояния может работать в некоторых случаях, мы не рекомендуем этого делать. Вы должны рассматривать значение состояния, к которому вы имеете доступ во время рендеринга, как доступное только для чтения.

Чтобы действительно [вызвать повторный рендеринг](state-as-a-snapshot.md#setting-state-triggers-renders) в этом случае, **создайте _новый_ объект и передайте его в функцию установки состояния:**.

```js
onPointerMove={e => {
  setPosition({
    x: e.clientX,
    y: e.clientY
  });
}}
```

С помощью `setPosition` вы говорите React:

-   Замените `position` на этот новый объект.
-   И снова отобразите этот компонент

Обратите внимание, что красная точка теперь следует за вашим указателем, когда вы касаетесь или наводите курсор на область предварительного просмотра:

=== "App.js"

    ```js
    import { useState } from 'react';
    export default function MovingDot() {
    	const [position, setPosition] = useState({
    		x: 0,
    		y: 0,
    	});
    	return (
    		<div
    			onPointerMove={(e) => {
    				setPosition({
    					x: e.clientX,
    					y: e.clientY,
    				});
    			}}
    			style={{
    				position: 'relative',
    				width: '100vw',
    				height: '100vh',
    			}}
    		>
    			<div
    				style={{
    					position: 'absolute',
    					backgroundColor: 'red',
    					borderRadius: '50%',
    					transform: `translate(${position.x}px, ${position.y}px)`,
    					left: -10,
    					top: -10,
    					width: 20,
    					height: 20,
    				}}
    			/>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5tfwx3?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Локальная мутация — это нормально"

    Код, подобный этому, является проблемой, потому что он изменяет _существующий_ объект в состоянии:

    ```js
    position.x = e.clientX;
    position.y = e.clientY;
    ```

    Но такой код **абсолютно нормален**, потому что вы мутируете свежий объект, который вы _только что создали_:

    ```js
    const nextPosition = {};
    nextPosition.x = e.clientX;
    nextPosition.y = e.clientY;
    setPosition(nextPosition);
    ```

    На самом деле, это совершенно равносильно тому, чтобы написать это:

    ```js
    setPosition({
    	x: e.clientX,
    	y: e.clientY,
    });
    ```

    Мутация является проблемой только тогда, когда вы изменяете _существующие_ объекты, которые уже находятся в состоянии. Мутация только что созданного объекта - это нормально, потому что _на него пока не ссылается никакой другой код._ Изменение объекта не окажет случайного влияния на что-то, что от него зависит. Это называется "локальной мутацией". Вы даже можете делать локальную мутацию [во время рендеринга](keeping-components-pure.md#local-mutation-your-components-little-secret) Очень удобно и совершенно нормально!

## Копирование объектов с синтаксисом `...` {#copying-objects-with-the-spread-syntax}

В предыдущем примере объект `position` всегда создается свежим из текущей позиции курсора. Но часто возникает необходимость включить _существующие_ данные как часть нового создаваемого объекта. Например, вы можете захотеть обновить _только одно_ поле в форме, но сохранить прежние значения для всех остальных полей.

Такие поля ввода не работают, потому что обработчики `onChange` изменяют состояние:

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Form() {
    	const [person, setPerson] = useState({
    		firstName: 'Barbara',
    		lastName: 'Hepworth',
    		email: 'bhepworth@sculpture.com',
    	});

    	function handleFirstNameChange(e) {
    		person.firstName = e.target.value;
    	}

    	function handleLastNameChange(e) {
    		person.lastName = e.target.value;
    	}

    	function handleEmailChange(e) {
    		person.email = e.target.value;
    	}

    	return (
    		<>
    			<label>
    				First name:
    				<input
    					value={person.firstName}
    					onChange={handleFirstNameChange}
    				/>
    			</label>
    			<label>
    				Last name:
    				<input
    					value={person.lastName}
    					onChange={handleLastNameChange}
    				/>
    			</label>
    			<label>
    				Email:
    				<input
    					value={person.email}
    					onChange={handleEmailChange}
    				/>
    			</label>
    			<p>
    				{person.firstName} {person.lastName} (
    				{person.email})
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xjd24m?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Например, эта строка мутирует состояние из прошлого рендеринга:

```js
person.firstName = e.target.value;
```

Надежный способ добиться нужного вам поведения — создать новый объект и передать его в `setPerson`. Но здесь вы хотите также **копировать в него существующие данные**, поскольку изменилось только одно из полей:

```js
setPerson({
    firstName: e.target.value, // New first name from the input
    lastName: person.lastName,
    email: person.email,
});
```

Вы можете использовать спреад-синтаксис `...` [распространение объекта](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Operators/Spread_syntax#spread_in_object_literals), чтобы не копировать каждое свойство отдельно.

```js
setPerson({
    ...person, // Copy the old fields
    firstName: e.target.value, // But override this one
});
```

Теперь форма работает!

Обратите внимание, что вы не объявили отдельную переменную состояния для каждого поля ввода. Для больших форм очень удобно хранить все данные, сгруппированные в одном объекте — при условии, что вы правильно их обновляете!

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Form() {
    	const [person, setPerson] = useState({
    		firstName: 'Barbara',
    		lastName: 'Hepworth',
    		email: 'bhepworth@sculpture.com',
    	});

    	function handleFirstNameChange(e) {
    		setPerson({
    			...person,
    			firstName: e.target.value,
    		});
    	}

    	function handleLastNameChange(e) {
    		setPerson({
    			...person,
    			lastName: e.target.value,
    		});
    	}

    	function handleEmailChange(e) {
    		setPerson({
    			...person,
    			email: e.target.value,
    		});
    	}

    	return (
    		<>
    			<label>
    				First name:
    				<input
    					value={person.firstName}
    					onChange={handleFirstNameChange}
    				/>
    			</label>
    			<label>
    				Last name:
    				<input
    					value={person.lastName}
    					onChange={handleLastNameChange}
    				/>
    			</label>
    			<label>
    				Email:
    				<input
    					value={person.email}
    					onChange={handleEmailChange}
    				/>
    			</label>
    			<p>
    				{person.firstName} {person.lastName} (
    				{person.email})
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/x4ltt8?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что синтаксис распространения `...` является "неглубоким" - он копирует объекты только на один уровень вглубь. Это делает его быстрым, но это также означает, что если вы хотите обновить вложенное свойство, вам придется использовать его несколько раз.

!!!note "Использование одного обработчика событий для нескольких полей"

    Вы также можете использовать скобки `[` и `]` внутри определения объекта, чтобы указать свойство с динамическим именем. Вот тот же пример, но с одним обработчиком событий вместо трех разных:

    === "App.js"

    	```js
    	import { useState } from 'react';

    	export default function Form() {
    		const [person, setPerson] = useState({
    			firstName: 'Barbara',
    			lastName: 'Hepworth',
    			email: 'bhepworth@sculpture.com',
    		});

    		function handleChange(e) {
    			setPerson({
    				...person,
    				[e.target.name]: e.target.value,
    			});
    		}

    		return (
    			<>
    				<label>
    					First name:
    					<input
    						name="firstName"
    						value={person.firstName}
    						onChange={handleChange}
    					/>
    				</label>
    				<label>
    					Last name:
    					<input
    						name="lastName"
    						value={person.lastName}
    						onChange={handleChange}
    					/>
    				</label>
    				<label>
    					Email:
    					<input
    						name="email"
    						value={person.email}
    						onChange={handleChange}
    					/>
    				</label>
    				<p>
    					{person.firstName} {person.lastName} (
    					{person.email})
    				</p>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/vhvm8s?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Здесь `e.target.name` относится к свойству `name`, заданному DOM-элементу `<input>`.

## Обновление вложенного объекта {#updating-a-nested-object}

Рассмотрим структуру вложенного объекта следующим образом:

```js
const [person, setPerson] = useState({
    name: 'Niki de Saint Phalle',
    artwork: {
        title: 'Blue Nana',
        city: 'Hamburg',
        image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    },
});
```

Если вы хотите обновить `person.artwork.city`, то понятно, как это сделать с помощью мутации:

```js
person.artwork.city = 'New Delhi';
```

Но в React состояние рассматривается как неизменяемое! Чтобы изменить `city`, вам сначала нужно создать новый объект `artwork` (предварительно заполненный данными из предыдущего объекта), а затем создать новый объект `person`, который указывает на новый `artwork`:

```js
const nextArtwork = {
    ...person.artwork,
    city: 'New Delhi',
};
const nextPerson = { ...person, artwork: nextArtwork };
setPerson(nextPerson);
```

Или записанный как вызов одной функции:

```js
setPerson({
    ...person, // Copy other fields
    artwork: {
        // but replace the artwork
        ...person.artwork, // with the same one
        city: 'New Delhi', // but in New Delhi!
    },
});
```

Это немного многословно, но для многих случаев подходит:

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Form() {
    	const [person, setPerson] = useState({
    		name: 'Niki de Saint Phalle',
    		artwork: {
    			title: 'Blue Nana',
    			city: 'Hamburg',
    			image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    		},
    	});

    	function handleNameChange(e) {
    		setPerson({
    			...person,
    			name: e.target.value,
    		});
    	}

    	function handleTitleChange(e) {
    		setPerson({
    			...person,
    			artwork: {
    				...person.artwork,
    				title: e.target.value,
    			},
    		});
    	}

    	function handleCityChange(e) {
    		setPerson({
    			...person,
    			artwork: {
    				...person.artwork,
    				city: e.target.value,
    			},
    		});
    	}

    	function handleImageChange(e) {
    		setPerson({
    			...person,
    			artwork: {
    				...person.artwork,
    				image: e.target.value,
    			},
    		});
    	}

    	return (
    		<>
    			<label>
    				Name:
    				<input
    					value={person.name}
    					onChange={handleNameChange}
    				/>
    			</label>
    			<label>
    				Title:
    				<input
    					value={person.artwork.title}
    					onChange={handleTitleChange}
    				/>
    			</label>
    			<label>
    				City:
    				<input
    					value={person.artwork.city}
    					onChange={handleCityChange}
    				/>
    			</label>
    			<label>
    				Image:
    				<input
    					value={person.artwork.image}
    					onChange={handleImageChange}
    				/>
    			</label>
    			<p>
    				<i>{person.artwork.title}</i>
    				{' by '}
    				{person.name}
    				<br />
    				(located in {person.artwork.city})
    			</p>
    			<img
    				src={person.artwork.image}
    				alt={person.artwork.title}
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/3zdnr9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Объекты на самом деле не являются вложенными"

    Объект, подобный этому, появляется "вложенным" в код:

    ```js
    let obj = {
    	name: 'Niki de Saint Phalle',
    	artwork: {
    		title: 'Blue Nana',
    		city: 'Hamburg',
    		image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    	},
    };
    ```

    Однако "вложенность" - это неточный способ представления о том, как ведут себя объекты. Когда код выполняется, не существует такого понятия, как "вложенный" объект. На самом деле вы рассматриваете два разных объекта:

    ```js
    let obj1 = {
    	title: 'Blue Nana',
    	city: 'Hamburg',
    	image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    };

    let obj2 = {
    	name: 'Niki de Saint Phalle',
    	artwork: obj1,
    };
    ```

    Объект `obj1` не находится "внутри" `obj2`. Например, `obj3` может "указывать" и на `obj1`:

    ```js
    let obj1 = {
    	title: 'Blue Nana',
    	city: 'Hamburg',
    	image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    };

    let obj2 = {
    	name: 'Niki de Saint Phalle',
    	artwork: obj1,
    };

    let obj3 = {
    	name: 'Copycat',
    	artwork: obj1,
    };
    ```

    Если бы вы изменили `obj3.artwork.city`, это повлияло бы и на `obj2.artwork.city`, и на `obj1.city`. Это происходит потому, что `obj3.artwork`, `obj2.artwork` и `obj1` являются одним и тем же объектом. Это трудно заметить, когда вы думаете об объектах как о "вложенных". Вместо этого они представляют собой отдельные объекты, "указывающие" друг на друга с помощью свойств.

### Напишите лаконичную логику обновления с помощью Immer {#write-concise-update-logic-with-immer}

Если ваше состояние глубоко вложенное, вы можете рассмотреть возможность [сглаживания](choosing-the-state-structure.md#avoid-deeply-nested-state). Но если вы не хотите менять структуру состояния, вы можете предпочесть быстрый путь к вложенным спредам. [Immer](https://github.com/immerjs/use-immer) - это популярная библиотека, которая позволяет вам писать, используя удобный, но мутирующий синтаксис, и заботится о создании копий за вас. С Immer написанный вами код выглядит так, как будто вы "нарушаете правила" и мутируете объект:

```js
updatePerson((draft) => {
    draft.artwork.city = 'Lagos';
});
```

Но в отличие от обычной мутации, она не переписывает прошлое состояние!

!!!note "Как работает Immer?"

    "Черновик", предоставляемый Immer, является особым типом объекта, называемым [Proxy](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Proxy), который "записывает" то, что вы с ним делаете. Именно поэтому вы можете свободно мутировать его сколько угодно! Под капотом Immer определяет, какие части `черновика` были изменены, и создает совершенно новый объект, содержащий ваши правки.

Чтобы попробовать Immer:

1.  Запустите `npm install use-immer`, чтобы добавить Immer в качестве зависимости.
2.  Затем замените `import { useState } из 'react'` на `import { useImmer } из 'use-immer'`.

Вот вышеприведенный пример, преобразованный в Immer:

=== "App.js"

    ```js
    import { useImmer } from 'use-immer';

    export default function Form() {
    	const [person, updatePerson] = useImmer({
    		name: 'Niki de Saint Phalle',
    		artwork: {
    			title: 'Blue Nana',
    			city: 'Hamburg',
    			image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    		},
    	});

    	function handleNameChange(e) {
    		updatePerson((draft) => {
    			draft.name = e.target.value;
    		});
    	}

    	function handleTitleChange(e) {
    		updatePerson((draft) => {
    			draft.artwork.title = e.target.value;
    		});
    	}

    	function handleCityChange(e) {
    		updatePerson((draft) => {
    			draft.artwork.city = e.target.value;
    		});
    	}

    	function handleImageChange(e) {
    		updatePerson((draft) => {
    			draft.artwork.image = e.target.value;
    		});
    	}

    	return (
    		<>
    			<label>
    				Name:
    				<input
    					value={person.name}
    					onChange={handleNameChange}
    				/>
    			</label>
    			<label>
    				Title:
    				<input
    					value={person.artwork.title}
    					onChange={handleTitleChange}
    				/>
    			</label>
    			<label>
    				City:
    				<input
    					value={person.artwork.city}
    					onChange={handleCityChange}
    				/>
    			</label>
    			<label>
    				Image:
    				<input
    					value={person.artwork.image}
    					onChange={handleImageChange}
    				/>
    			</label>
    			<p>
    				<i>{person.artwork.title}</i>
    				{' by '}
    				{person.name}
    				<br />
    				(located in {person.artwork.city})
    			</p>
    			<img
    				src={person.artwork.image}
    				alt={person.artwork.title}
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/522ghd?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="optimistic-panna-522ghd" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, насколько более лаконичными стали обработчики событий. Вы можете смешивать и сочетать `useState` и `useImmer` в одном компоненте сколько угодно. Immer — отличный способ сохранить обработчики обновлений лаконичными, особенно если в вашем состоянии есть вложенность, и копирование объектов приводит к повторяющемуся коду.

!!!note "Почему мутирование состояния не рекомендуется в React?"

    Есть несколько причин:

    -   **Отладка:** Если вы используете `console.log` и не мутируете состояние, ваши прошлые логи не будут забиты недавними изменениями состояния. Таким образом, вы можете четко видеть, как изменялось состояние между рендерами.
    -   **Оптимизация:** Обычные [стратегии оптимизации React](../reference/react/memo.md) полагаются на пропуск работы, если предыдущие пропсы или состояние совпадают с последующими. Если вы никогда не изменяете состояние, то проверить, были ли изменения, можно очень быстро. Если `prevObj === obj`, вы можете быть уверены, что внутри него ничего не могло измениться.
    -   **Новые возможности:** Новые возможности React, которые мы создаем, зависят от того, что состояние [рассматривается как снимок](state-as-a-snapshot.md). Если вы мутируете прошлые версии состояния, это может помешать вам использовать новые возможности.
    -   **Изменения требований:** Некоторые возможности приложения, такие как реализация Undo/Redo, показ истории изменений или предоставление пользователю возможности вернуть форму к прежним значениям, проще сделать, если ничего не мутировать. Это происходит потому, что вы можете хранить в памяти прошлые копии состояния и использовать их повторно, когда это необходимо. Если вы начнете с мутативного подхода, такие функции, как эта, будет трудно добавить позже.
    -   **Простая реализация:** Поскольку React не полагается на мутацию, ему не нужно делать ничего особенного с вашими объектами. Ему не нужно перехватывать их свойства, всегда оборачивать их в прокси или выполнять другую работу при инициализации, как это делают многие "реактивные" решения. Именно поэтому React позволяет вам поместить любой объект в состояние - независимо от его размера - без дополнительных проблем с производительностью и корректностью.

    На практике вы часто можете "уйти" от мутирования состояния в React, но мы настоятельно рекомендуем вам не делать этого, чтобы вы могли использовать новые возможности React, разработанные с учетом этого подхода. Будущие разработчики и, возможно, даже ваше будущее "я" скажут вам спасибо!

!!!tip "Резюме"

    -   Рассматривайте все состояния в React как неизменяемые.
    -   Когда вы храните объекты в состоянии, их изменение не вызовет рендеринга и изменит состояние в предыдущих "снимках" рендеринга.
    -   Вместо того чтобы мутировать объект, создайте _новую_ его версию и вызовите повторный рендеринг, установив для нее состояние.
    -   Вы можете использовать синтаксис распространения объектов `{...obj, something: 'newValue'}` для создания копий объектов.
    -   Синтаксис распространения является неглубоким: он копирует только один уровень в глубину.
    -   Чтобы обновить вложенный объект, вам нужно создать копии по всему пути вверх от того места, которое вы обновляете.
    -   Чтобы уменьшить количество повторяющегося кода копирования, используйте Immer.

## Задачи {#challenges}

### 1. Исправление некорректных обновлений состояния {#fix-incorrect-state-updates}

В этой форме есть несколько ошибок. Несколько раз нажмите на кнопку, увеличивающую оценку. Заметьте, что он не увеличивается. Затем отредактируйте имя и фамилию и заметите, что оценка внезапно "подхватила" ваши изменения. Наконец, отредактируйте фамилию, и заметите, что оценка полностью исчезла.

Ваша задача — исправить все эти ошибки. Исправляя их, объясните, почему происходит каждая из них.

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Scoreboard() {
    	const [player, setPlayer] = useState({
    		firstName: 'Ranjani',
    		lastName: 'Shettar',
    		score: 10,
    	});

    	function handlePlusClick() {
    		player.score++;
    	}

    	function handleFirstNameChange(e) {
    		setPlayer({
    			...player,
    			firstName: e.target.value,
    		});
    	}

    	function handleLastNameChange(e) {
    		setPlayer({
    			lastName: e.target.value,
    		});
    	}

    	return (
    		<>
    			<label>
    				Score: <b>{player.score}</b>{' '}
    				<button onClick={handlePlusClick}>
    					+1
    				</button>
    			</label>
    			<label>
    				First name:
    				<input
    					value={player.firstName}
    					onChange={handleFirstNameChange}
    				/>
    			</label>
    			<label>
    				Last name:
    				<input
    					value={player.lastName}
    					onChange={handleLastNameChange}
    				/>
    			</label>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/rztj2r?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Вот версия, в которой исправлены обе ошибки:

    === "App.js"

    	```js
    	import { useState } from 'react';

    	export default function Scoreboard() {
    		const [player, setPlayer] = useState({
    			firstName: 'Ranjani',
    			lastName: 'Shettar',
    			score: 10,
    		});

    		function handlePlusClick() {
    			setPlayer({
    				...player,
    				score: player.score + 1,
    			});
    		}

    		function handleFirstNameChange(e) {
    			setPlayer({
    				...player,
    				firstName: e.target.value,
    			});
    		}

    		function handleLastNameChange(e) {
    			setPlayer({
    				...player,
    				lastName: e.target.value,
    			});
    		}

    		return (
    			<>
    				<label>
    					Score: <b>{player.score}</b>{' '}
    					<button onClick={handlePlusClick}>
    						+1
    					</button>
    				</label>
    				<label>
    					First name:
    					<input
    						value={player.firstName}
    						onChange={handleFirstNameChange}
    					/>
    				</label>
    				<label>
    					Last name:
    					<input
    						value={player.lastName}
    						onChange={handleLastNameChange}
    					/>
    				</label>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/pr37rg?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Проблема с `handlePlusClick` заключалась в том, что он мутировал объект `player`. В результате React не знал, что есть причина для повторного рендеринга, и не обновлял счет на экране. Вот почему, когда вы редактировали первое имя, состояние обновлялось, вызывая повторный рендеринг, который _также_ обновлял счет на экране.

    Проблема с `handleLastNameChange` заключалась в том, что он не копировал существующие поля `...player` в новый объект. Вот почему счет терялся после редактирования фамилии.

### 2. Найти и исправить мутацию {#find-and-fix-the-mutation}

Имеется перетаскиваемый ящик на статичном фоне. Вы можете изменить цвет поля с помощью кнопки select.

Но есть ошибка. Если сначала переместить ящик, а затем изменить его цвет, фон (который не должен двигаться!) "перепрыгнет" на позицию ящика. Но этого не должно произойти: параметр `position` у `Background` установлен в `initialPosition`, что равно `{ x: 0, y: 0 }`. Почему фон перемещается после изменения цвета?

Найдите ошибку и исправьте ее.

=== "App.js"

    ```js
    import { useState } from 'react';
    import Background from './Background.js';
    import Box from './Box.js';

    const initialPosition = {
    	x: 0,
    	y: 0,
    };

    export default function Canvas() {
    	const [shape, setShape] = useState({
    		color: 'orange',
    		position: initialPosition,
    	});

    	function handleMove(dx, dy) {
    		shape.position.x += dx;
    		shape.position.y += dy;
    	}

    	function handleColorChange(e) {
    		setShape({
    			...shape,
    			color: e.target.value,
    		});
    	}

    	return (
    		<>
    			<select
    				value={shape.color}
    				onChange={handleColorChange}
    			>
    				<option value="orange">orange</option>
    				<option value="lightpink">lightpink</option>
    				<option value="aliceblue">aliceblue</option>
    			</select>
    			<Background position={initialPosition} />
    			<Box
    				color={shape.color}
    				position={shape.position}
    				onMove={handleMove}
    			>
    				Drag me!
    			</Box>
    		</>
    	);
    }
    ```

=== "Box.js"

    ```js
    import { useState } from 'react';

    export default function Box({
    	children,
    	color,
    	position,
    	onMove,
    }) {
    	const [lastCoordinates, setLastCoordinates] = useState(
    		null
    	);

    	function handlePointerDown(e) {
    		e.target.setPointerCapture(e.pointerId);
    		setLastCoordinates({
    			x: e.clientX,
    			y: e.clientY,
    		});
    	}

    	function handlePointerMove(e) {
    		if (lastCoordinates) {
    			setLastCoordinates({
    				x: e.clientX,
    				y: e.clientY,
    			});
    			const dx = e.clientX - lastCoordinates.x;
    			const dy = e.clientY - lastCoordinates.y;
    			onMove(dx, dy);
    		}
    	}

    	function handlePointerUp(e) {
    		setLastCoordinates(null);
    	}

    	return (
    		<div
    			onPointerDown={handlePointerDown}
    			onPointerMove={handlePointerMove}
    			onPointerUp={handlePointerUp}
    			style={{
    				width: 100,
    				height: 100,
    				cursor: 'grab',
    				backgroundColor: color,
    				position: 'absolute',
    				border: '1px solid black',
    				display: 'flex',
    				justifyContent: 'center',
    				alignItems: 'center',
    				transform: `translate(
    		${position.x}px,
    		${position.y}px
    		)`,
    			}}
    		>
    			{children}
    		</div>
    	);
    }
    ```

=== "Background.js"

    ```js
    export default function Background({ position }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				transform: `translate(
    		${position.x}px,
    		${position.y}px
    	)`,
    				width: 250,
    				height: 250,
    				backgroundColor: 'rgba(200, 200, 0, 0.2)',
    			}}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dtjnrl?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Если что-то неожиданно меняется, значит, произошла мутация. Найдите мутацию в `App.js` и исправьте ее.

???success "Показать решение"

    Проблема была в мутации внутри `handleMove`. Она мутировала `shape.position`, но это тот же объект, на который указывает `initialPosition`. Поэтому и форма, и фон перемещаются. (Это мутация, поэтому изменение не отражается на экране до тех пор, пока не произойдет несвязанное обновление - изменение цвета - не вызовет повторный рендеринг).

    Исправление заключается в удалении мутации из `handleMove` и использовании синтаксиса распространения для копирования формы. Обратите внимание, что `+=` - это мутация, поэтому вам нужно переписать ее, чтобы использовать обычную операцию `+`.

    === "App.js"

    	```js
    	import { useState } from 'react';
    	import Background from './Background.js';
    	import Box from './Box.js';

    	const initialPosition = {
    		x: 0,
    		y: 0,
    	};

    	export default function Canvas() {
    		const [shape, setShape] = useState({
    			color: 'orange',
    			position: initialPosition,
    		});

    		function handleMove(dx, dy) {
    			setShape({
    				...shape,
    				position: {
    					x: shape.position.x + dx,
    					y: shape.position.y + dy,
    				},
    			});
    		}

    		function handleColorChange(e) {
    			setShape({
    				...shape,
    				color: e.target.value,
    			});
    		}

    		return (
    			<>
    				<select
    					value={shape.color}
    					onChange={handleColorChange}
    				>
    					<option value="orange">orange</option>
    					<option value="lightpink">lightpink</option>
    					<option value="aliceblue">aliceblue</option>
    				</select>
    				<Background position={initialPosition} />
    				<Box
    					color={shape.color}
    					position={shape.position}
    					onMove={handleMove}
    				>
    					Drag me!
    				</Box>
    			</>
    		);
    	}
    	```

    === "Box.js"

    	```js
    	import { useState } from 'react';

    	export default function Box({
    		children,
    		color,
    		position,
    		onMove,
    	}) {
    		const [lastCoordinates, setLastCoordinates] = useState(
    			null
    		);

    		function handlePointerDown(e) {
    			e.target.setPointerCapture(e.pointerId);
    			setLastCoordinates({
    				x: e.clientX,
    				y: e.clientY,
    			});
    		}

    		function handlePointerMove(e) {
    			if (lastCoordinates) {
    				setLastCoordinates({
    					x: e.clientX,
    					y: e.clientY,
    				});
    				const dx = e.clientX - lastCoordinates.x;
    				const dy = e.clientY - lastCoordinates.y;
    				onMove(dx, dy);
    			}
    		}

    		function handlePointerUp(e) {
    			setLastCoordinates(null);
    		}

    		return (
    			<div
    				onPointerDown={handlePointerDown}
    				onPointerMove={handlePointerMove}
    				onPointerUp={handlePointerUp}
    				style={{
    					width: 100,
    					height: 100,
    					cursor: 'grab',
    					backgroundColor: color,
    					position: 'absolute',
    					border: '1px solid black',
    					display: 'flex',
    					justifyContent: 'center',
    					alignItems: 'center',
    					transform: `translate(
    			${position.x}px,
    			${position.y}px
    			)`,
    				}}
    			>
    				{children}
    			</div>
    		);
    	}
    	```

    === "Background.js"

    	```js
    	export default function Background({ position }) {
    		return (
    			<div
    				style={{
    					position: 'absolute',
    					transform: `translate(
    			${position.x}px,
    			${position.y}px
    		)`,
    					width: 250,
    					height: 250,
    					backgroundColor: 'rgba(200, 200, 0, 0.2)',
    				}}
    			/>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/vf5x9l?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 3. Обновление объекта с помощью Immer {#update-an-object-with-immer}

Это тот же пример с ошибкой, что и в предыдущей задаче. На этот раз исправьте мутацию, используя Immer. Для вашего удобства функция `useImmer` уже импортирована, поэтому вам нужно изменить переменную состояния `shape`, чтобы использовать ее.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { useImmer } from 'use-immer';
    import Background from './Background.js';
    import Box from './Box.js';

    const initialPosition = {
    	x: 0,
    	y: 0,
    };

    export default function Canvas() {
    	const [shape, setShape] = useState({
    		color: 'orange',
    		position: initialPosition,
    	});

    	function handleMove(dx, dy) {
    		shape.position.x += dx;
    		shape.position.y += dy;
    	}

    	function handleColorChange(e) {
    		setShape({
    			...shape,
    			color: e.target.value,
    		});
    	}

    	return (
    		<>
    			<select
    				value={shape.color}
    				onChange={handleColorChange}
    			>
    				<option value="orange">orange</option>
    				<option value="lightpink">lightpink</option>
    				<option value="aliceblue">aliceblue</option>
    			</select>
    			<Background position={initialPosition} />
    			<Box
    				color={shape.color}
    				position={shape.position}
    				onMove={handleMove}
    			>
    				Drag me!
    			</Box>
    		</>
    	);
    }
    ```

=== "Box.js"

    ```js
    import { useState } from 'react';

    export default function Box({
    	children,
    	color,
    	position,
    	onMove,
    }) {
    	const [lastCoordinates, setLastCoordinates] = useState(
    		null
    	);

    	function handlePointerDown(e) {
    		e.target.setPointerCapture(e.pointerId);
    		setLastCoordinates({
    			x: e.clientX,
    			y: e.clientY,
    		});
    	}

    	function handlePointerMove(e) {
    		if (lastCoordinates) {
    			setLastCoordinates({
    				x: e.clientX,
    				y: e.clientY,
    			});
    			const dx = e.clientX - lastCoordinates.x;
    			const dy = e.clientY - lastCoordinates.y;
    			onMove(dx, dy);
    		}
    	}

    	function handlePointerUp(e) {
    		setLastCoordinates(null);
    	}

    	return (
    		<div
    			onPointerDown={handlePointerDown}
    			onPointerMove={handlePointerMove}
    			onPointerUp={handlePointerUp}
    			style={{
    				width: 100,
    				height: 100,
    				cursor: 'grab',
    				backgroundColor: color,
    				position: 'absolute',
    				border: '1px solid black',
    				display: 'flex',
    				justifyContent: 'center',
    				alignItems: 'center',
    				transform: `translate(
    		${position.x}px,
    		${position.y}px
    		)`,
    			}}
    		>
    			{children}
    		</div>
    	);
    }
    ```

=== "Background.js"

    ```js
    export default function Background({ position }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				transform: `translate(
    		${position.x}px,
    		${position.y}px
    	)`,
    				width: 250,
    				height: 250,
    				backgroundColor: 'rgba(200, 200, 0, 0.2)',
    			}}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/59wcld?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="pedantic-ramanujan-59wcld" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Это решение переписано с помощью Immer. Обратите внимание, что обработчики событий написаны мутирующим образом, но ошибка не возникает. Это потому, что Immer никогда не мутирует существующие объекты.

    === "App.js"

    	```js
    	import { useImmer } from 'use-immer';
    	import Background from './Background.js';
    	import Box from './Box.js';

    	const initialPosition = {
    		x: 0,
    		y: 0,
    	};

    	export default function Canvas() {
    		const [shape, updateShape] = useImmer({
    			color: 'orange',
    			position: initialPosition,
    		});

    		function handleMove(dx, dy) {
    			updateShape((draft) => {
    				draft.position.x += dx;
    				draft.position.y += dy;
    			});
    		}

    		function handleColorChange(e) {
    			updateShape((draft) => {
    				draft.color = e.target.value;
    			});
    		}

    		return (
    			<>
    				<select
    					value={shape.color}
    					onChange={handleColorChange}
    				>
    					<option value="orange">orange</option>
    					<option value="lightpink">lightpink</option>
    					<option value="aliceblue">aliceblue</option>
    				</select>
    				<Background position={initialPosition} />
    				<Box
    					color={shape.color}
    					position={shape.position}
    					onMove={handleMove}
    				>
    					Drag me!
    				</Box>
    			</>
    		);
    	}
    	```

    === "Box.js"

    	```js
    	import { useState } from 'react';

    	export default function Box({
    		children,
    		color,
    		position,
    		onMove,
    	}) {
    		const [lastCoordinates, setLastCoordinates] = useState(
    			null
    		);

    		function handlePointerDown(e) {
    			e.target.setPointerCapture(e.pointerId);
    			setLastCoordinates({
    				x: e.clientX,
    				y: e.clientY,
    			});
    		}

    		function handlePointerMove(e) {
    			if (lastCoordinates) {
    				setLastCoordinates({
    					x: e.clientX,
    					y: e.clientY,
    				});
    				const dx = e.clientX - lastCoordinates.x;
    				const dy = e.clientY - lastCoordinates.y;
    				onMove(dx, dy);
    			}
    		}

    		function handlePointerUp(e) {
    			setLastCoordinates(null);
    		}

    		return (
    			<div
    				onPointerDown={handlePointerDown}
    				onPointerMove={handlePointerMove}
    				onPointerUp={handlePointerUp}
    				style={{
    					width: 100,
    					height: 100,
    					cursor: 'grab',
    					backgroundColor: color,
    					position: 'absolute',
    					border: '1px solid black',
    					display: 'flex',
    					justifyContent: 'center',
    					alignItems: 'center',
    					transform: `translate(
    			${position.x}px,
    			${position.y}px
    			)`,
    				}}
    			>
    				{children}
    			</div>
    		);
    	}
    	```

    === "Background.js"

    	```js
    	export default function Background({ position }) {
    		return (
    			<div
    				style={{
    					position: 'absolute',
    					transform: `translate(
    			${position.x}px,
    			${position.y}px
    		)`,
    					width: 250,
    					height: 250,
    					backgroundColor: 'rgba(200, 200, 0, 0.2)',
    				}}
    			/>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/2f8vcv?view=Editor+%2B+Preview&module=%2Fpackage.json" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="priceless-hertz-2f8vcv" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/updating-objects-in-state](https://react.dev/learn/updating-objects-in-state)</small>
