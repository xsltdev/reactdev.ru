---
description: Иногда вы захотите добавить немного логики JavaScript или сослаться на динамическое свойство внутри этой разметки. В этой ситуации вы можете использовать фигурные скобки в JSX, чтобы открыть окно для JavaScript
---

# JavaScript в JSX с фигурными скобками

<big>JSX позволяет вам писать HTML-подобную разметку внутри файла JavaScript, сохраняя логику рендеринга и содержимое в одном месте. Иногда вы захотите добавить немного логики JavaScript или сослаться на динамическое свойство внутри этой разметки. В этой ситуации вы можете использовать **фигурные скобки** в JSX, чтобы использовать JavaScript.</big>

!!!tip "Вы узнаете"

    -   Как передавать строки с кавычками
    -   Как ссылаться на переменную JavaScript внутри JSX с помощью фигурных скобок
    -   Как вызвать функцию JavaScript в JSX с помощью фигурных скобок
    -   Как использовать объект JavaScript внутри JSX с фигурными скобками

## Передача строк с кавычками {#passing-strings-with-quotes}

Когда вы хотите передать строковый атрибут в JSX, вы заключаете его в одинарные или двойные кавычки:

=== "App.js"

    ```js
    export default function Avatar() {
    	return (
    		<img
    			className="avatar"
    			src="https://i.imgur.com/7vQD0fPs.jpg"
    			alt="Gregorio Y. Zara"
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/c3tksl?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Здесь `"https://i.imgur.com/7vQD0fPs.jpg"` и `"Gregorio Y. Zara"` передаются как строки.

Но что если вы хотите динамически указать текст `src` или `alt`? Вы можете **использовать значение из JavaScript, заменив `"` и `"` на `{` и `}`**:

=== "App.js"

    ```js
    export default function Avatar() {
    	const avatar = 'https://i.imgur.com/7vQD0fPs.jpg';
    	const description = 'Gregorio Y. Zara';
    	return (
    		<img
    			className="avatar"
    			src={avatar}
    			alt={description}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/k9s9n2?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание на разницу между `className="avatar"`, которая определяет имя CSS-класса `"avatar"`, который делает изображение круглым, и `src={avatar}`, которая читает значение переменной JavaScript под названием `avatar`. Это потому, что фигурные скобки позволяют вам работать с JavaScript прямо в вашей разметке!

## Использование фигурных скобок: Окно в мир JavaScript {#using-curly-braces-a-window-into-the-javascript-world}

JSX - это особый способ написания JavaScript. Это означает, что можно использовать JavaScript внутри него - с фигурными скобками `{ }`. В приведенном ниже примере сначала объявляется имя ученого, `name`, затем оно помещается в фигурные скобки внутри `<h1>`:

=== "App.js"

    ```js
    export default function TodoList() {
    	const name = 'Gregorio Y. Zara';
    	return <h1>{name}'s To Do List</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/hyqdsw?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Попробуйте изменить значение `name` с `Грегорио Й. Зара` на `Хеди Ламарр`. Видите, как изменился заголовок списка?

Любое выражение JavaScript будет работать между фигурными скобками, включая вызовы функций, таких как `formatDate()`:

=== "App.js"

    ```js
    const today = new Date();

    function formatDate(date) {
    	return new Intl.DateTimeFormat('en-US', {
    		weekday: 'long',
    	}).format(date);
    }

    export default function TodoList() {
    	return <h1>To Do List for {formatDate(today)}</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/3lkz77?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Где использовать фигурные скобки {#where-to-use-curly-braces}

В JSX фигурные скобки можно использовать только двумя способами:

1.  **В качестве текста** непосредственно внутри тега JSX: `<h1>{name}'s To Do List</h1>` работает, а <code>&lt;{tag}&gt;Gregorio Y. Zara's To Do List&lt;/{tag}&gt;</code> не работает.
2.  **Атрибуты** сразу после знака `=`: `src={avatar}` прочитает переменную `avatar`, но `src="{avatar}"` передаст строку `"{avatar}"`.

## Использование "двойных завитушек": CSS и другие объекты в JSX {#using-double-curlies-css-and-other-objects-in-jsx}

Помимо строк, чисел и других выражений JavaScript, в JSX можно передавать даже объекты. Объекты также обозначаются фигурными скобками, например `{ name: "Hedy Lamarr", inventions: 5 }`. Поэтому, чтобы передать объект JS в JSX, вы должны обернуть объект в другую пару фигурных скобок: `person={{ name: "Hedy Lamarr", inventions: 5 }}`.

Подобное можно увидеть при использовании встроенных стилей CSS в JSX. React не требует использования встроенных стилей (классы CSS отлично подходят для большинства случаев). Но когда вам нужен встроенный стиль, вы передаете объект в атрибут `style`:

=== "App.js"

    ```js
    export default function TodoList() {
    	return (
    		<ul
    			style={{
    				backgroundColor: 'black',
    				color: 'pink',
    			}}
    		>
    			<li>Improve the videophone</li>
    			<li>Prepare aeronautics lectures</li>
    			<li>Work on the alcohol-fuelled engine</li>
    		</ul>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6twv9v?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Попробуйте изменить значения `backgroundColor` и `color`.

Вы действительно можете увидеть объект JavaScript внутри фигурных скобок, если напишете его так:

```js hl_lines="2-5"
<ul style={
  {
    backgroundColor: 'black',
    color: 'pink'
  }
}>
```

Когда в следующий раз вы увидите `{{` и `}}` в JSX, знайте, что это не что иное, как объект внутри JSX curlies!

!!!warning "Внимание"

    Инлайн-свойства `style` записываются в camelCase. Например, HTML `<ul style="background-color: black">` будет записан как `<ul style={{ backgroundColor: 'black' }}>` в вашем компоненте.

## Больше веселья с объектами JavaScript и фигурными скобками {#more-fun-with-javascript-objects-and-curly-braces}

Вы можете поместить несколько выражений в один объект и ссылаться на них в JSX внутри фигурных скобок:

=== "App.js"

    ```js
    const person = {
    	name: 'Gregorio Y. Zara',
    	theme: {
    		backgroundColor: 'black',
    		color: 'pink',
    	},
    };

    export default function TodoList() {
    	return (
    		<div style={person.theme}>
    			<h1>{person.name}'s Todos</h1>
    			<img
    				className="avatar"
    				src="https://i.imgur.com/7vQD0fPs.jpg"
    				alt="Gregorio Y. Zara"
    			/>
    			<ul>
    				<li>Improve the videophone</li>
    				<li>Prepare aeronautics lectures</li>
    				<li>Work on the alcohol-fuelled engine</li>
    			</ul>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/vppdcf?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В этом примере объект JavaScript `person` содержит строку `name` и объект `theme`:

```js
const person = {
    name: 'Gregorio Y. Zara',
    theme: {
        backgroundColor: 'black',
        color: 'pink',
    },
};
```

Компонент может использовать эти значения из `person` следующим образом:

```js
<div style={person.theme}>
    <h1>{person.name}'s Todos</h1>
</div>
```

JSX очень минимален как язык шаблонов, потому что он позволяет организовать данные и логику с помощью JavaScript.

!!!note "Итого"

    Теперь вы знаете почти все о JSX:

    -   Атрибуты JSX, заключенные в кавычки, передаются как строки.
    -   Фигурные скобки позволяют вам привнести логику и переменные JavaScript в вашу разметку.
    -   Они работают внутри содержимого тега JSX или сразу после `=` в атрибутах.
    -   `{{` и `}}` - это не специальный синтаксис: это объект JavaScript, помещенный в фигурные скобки JSX.

## Задачи {#challenges}

### 1. Исправьте ошибку {#fix-the-mistake}

Этот код аварийно завершается с ошибкой `Objects are not valid as a React child`:

=== "App.js"

    ```js
    const person = {
    	name: 'Gregorio Y. Zara',
    	theme: {
    		backgroundColor: 'black',
    		color: 'pink',
    	},
    };

    export default function TodoList() {
    	return (
    		<div style={person.theme}>
    			<h1>{person}'s Todos</h1>
    			<img
    				className="avatar"
    				src="https://i.imgur.com/7vQD0fPs.jpg"
    				alt="Gregorio Y. Zara"
    			/>
    			<ul>
    				<li>Improve the videophone</li>
    				<li>Prepare aeronautics lectures</li>
    				<li>Work on the alcohol-fuelled engine</li>
    			</ul>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/4skw7f?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Можете ли вы найти проблему?

???tip "Показать подсказку"

    Посмотрите, что находится внутри фигурных скобок. Мы поместили туда то, что нужно?

???success "Показать решение"

    Это происходит потому, что в данном примере в разметку помещается _сам объект_, а не строка: `<h1>{person}'s Todos</h1>` пытается отобразить весь объект `person`! Включение необработанных объектов в текстовое содержимое приводит к ошибке, потому что React не знает, как вы хотите их отобразить.

    Чтобы исправить это, замените `<h1>{person}'s Todos</h1>` на `<h1>{person.name}'s Todos</h1>`:

    === "App.js"

    	```js
    	const person = {
    		name: 'Gregorio Y. Zara',
    		theme: {
    			backgroundColor: 'black',
    			color: 'pink',
    		},
    	};

    	export default function TodoList() {
    		return (
    			<div style={person.theme}>
    				<h1>{person.name}'s Todos</h1>
    				<img
    					className="avatar"
    					src="https://i.imgur.com/7vQD0fPs.jpg"
    					alt="Gregorio Y. Zara"
    				/>
    				<ul>
    					<li>Improve the videophone</li>
    					<li>Prepare aeronautics lectures</li>
    					<li>Work on the alcohol-fuelled engine</li>
    				</ul>
    			</div>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/vppdcf?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 2. Извлечение информации в объект {#extract-information-into-an-object}

Извлеките URL изображения в объект `person`.

=== "App.js"

    ```js
    const person = {
    	name: 'Gregorio Y. Zara',
    	theme: {
    		backgroundColor: 'black',
    		color: 'pink',
    	},
    };

    export default function TodoList() {
    	return (
    		<div style={person.theme}>
    			<h1>{person.name}'s Todos</h1>
    			<img
    				className="avatar"
    				src="https://i.imgur.com/7vQD0fPs.jpg"
    				alt="Gregorio Y. Zara"
    			/>
    			<ul>
    				<li>Improve the videophone</li>
    				<li>Prepare aeronautics lectures</li>
    				<li>Work on the alcohol-fuelled engine</li>
    			</ul>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/vppdcf?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Переместите URL изображения в свойство `person.imageUrl` и считайте его из тега `<img>` с помощью фигурных символов:

    === "App.js"

    	```js
    	const person = {
    		name: 'Gregorio Y. Zara',
    		imageUrl: 'https://i.imgur.com/7vQD0fPs.jpg',
    		theme: {
    			backgroundColor: 'black',
    			color: 'pink',
    		},
    	};

    	export default function TodoList() {
    		return (
    			<div style={person.theme}>
    				<h1>{person.name}'s Todos</h1>
    				<img
    					className="avatar"
    					src={person.imageUrl}
    					alt="Gregorio Y. Zara"
    				/>
    				<ul>
    					<li>Improve the videophone</li>
    					<li>Prepare aeronautics lectures</li>
    					<li>Work on the alcohol-fuelled engine</li>
    				</ul>
    			</div>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/zyjp7m?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 3. Запишите выражение внутри фигурных скобок JSX {#write-an-expression-inside-jsx-curly-braces}

В приведенном ниже объекте полный URL изображения разделен на четыре части: базовый URL, `imageId`, `imageSize` и расширение файла.

Мы хотим, чтобы URL изображения объединял эти атрибуты: базовый URL (всегда `'https://i.imgur.com/'`), `imageId` (`'7vQD0fP'`), `imageSize` (`'s'`) и расширение файла (всегда `'jpg'`). Однако что-то не так с тем, как тег `<img>` указывает свой `src`.

Вы можете это исправить?

=== "App.js"

    ```js
    const baseUrl = 'https://i.imgur.com/';
    const person = {
    	name: 'Gregorio Y. Zara',
    	imageId: '7vQD0fP',
    	imageSize: 's',
    	theme: {
    		backgroundColor: 'black',
    		color: 'pink',
    	},
    };

    export default function TodoList() {
    	return (
    		<div style={person.theme}>
    			<h1>{person.name}'s Todos</h1>
    			<img
    				className="avatar"
    				src="{baseUrl}{person.imageId}{person.imageSize}.jpg"
    				alt={person.name}
    			/>
    			<ul>
    				<li>Improve the videophone</li>
    				<li>Prepare aeronautics lectures</li>
    				<li>Work on the alcohol-fuelled engine</li>
    			</ul>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/53y3sy?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Чтобы проверить, что ваше исправление сработало, попробуйте изменить значение `imageSize` на `'b'`. Размер изображения должен измениться после вашей правки.

???success "Показать решение"

    Вы можете записать это как `src={baseUrl + person.imageId + person.imageSize + '.jpg'}`.

    1.  `{` открывает выражение JavaScript
    2.  `baseUrl + person.imageId + person.imageSize + '.jpg'` выдает правильную строку URL
    3.  `}` закрывает выражение JavaScript

    === "App.js"

    	```js
    	const baseUrl = 'https://i.imgur.com/';
    	const person = {
    		name: 'Gregorio Y. Zara',
    		imageId: '7vQD0fP',
    		imageSize: 's',
    		theme: {
    			backgroundColor: 'black',
    			color: 'pink',
    		},
    	};

    	export default function TodoList() {
    		return (
    			<div style={person.theme}>
    				<h1>{person.name}'s Todos</h1>
    				<img
    					className="avatar"
    					src={
    						baseUrl +
    						person.imageId +
    						person.imageSize +
    						'.jpg'
    					}
    					alt={person.name}
    				/>
    				<ul>
    					<li>Improve the videophone</li>
    					<li>Prepare aeronautics lectures</li>
    					<li>Work on the alcohol-fuelled engine</li>
    				</ul>
    			</div>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/zft27p?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Вы также можете перенести это выражение в отдельную функцию, как `getImageUrl` ниже:

    === "App.js"

    	```js
    	import { getImageUrl } from './utils.js';

    	const person = {
    		name: 'Gregorio Y. Zara',
    		imageId: '7vQD0fP',
    		imageSize: 's',
    		theme: {
    			backgroundColor: 'black',
    			color: 'pink',
    		},
    	};

    	export default function TodoList() {
    		return (
    			<div style={person.theme}>
    				<h1>{person.name}'s Todos</h1>
    				<img
    					className="avatar"
    					src={getImageUrl(person)}
    					alt={person.name}
    				/>
    				<ul>
    					<li>Improve the videophone</li>
    					<li>Prepare aeronautics lectures</li>
    					<li>Work on the alcohol-fuelled engine</li>
    				</ul>
    			</div>
    		);
    	}
    	```

    === "utils.js"

    	```js
    	export function getImageUrl(person) {
    		return (
    			'https://i.imgur.com/' +
    			person.imageId +
    			person.imageSize +
    			'.jpg'
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/gw42dp?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Переменные и функции помогут вам сохранить простоту разметки!

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/javascript-in-jsx-with-curly-braces](https://react.dev/learn/javascript-in-jsx-with-curly-braces)</small>
