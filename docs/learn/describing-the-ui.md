---
description: React — это библиотека JavaScript для визуализации пользовательских интерфейсов (UI). Пользовательский интерфейс строится из небольших блоков, таких как кнопки, текст и изображения
---

# Разработка интерфейса

<big>**React** — это библиотека JavaScript для визуализации пользовательских интерфейсов (UI). Пользовательский интерфейс строится из небольших блоков, таких как кнопки, текст и изображения. React позволяет объединять их в многократно используемые, вложенные _компоненты._ От веб-сайтов до приложений для телефонов — все на экране может быть разбито на компоненты. В этой главе вы научитесь создавать, настраивать и условно отображать компоненты React.</big>

!!!tip "В этой главе"

    -   [Как написать свой первый компонент React](your-first-component.md)
    -   [Когда и как создавать многокомпонентные файлы](importing-and-exporting-components.md)
    -   [Как добавить разметку в JavaScript с помощью JSX](writing-markup-with-jsx.md)
    -   [Как использовать фигурные скобки в JSX для доступа к функциональности JavaScript из ваших компонентов](javascript-in-jsx-with-curly-braces.md)
    -   [Как конфигурировать компоненты с помощью props](passing-props-to-a-component.md)
    -   [Как условно отрисовывать компоненты](conditional-rendering.md)
    -   [Как отрисовывать несколько компонентов одновременно](rendering-lists.md)
    -   [Как избежать запутанных ошибок, сохраняя чистоту компонентов](keeping-components-pure.md)

## Ваш первый компонент {#your-first-component}

Приложения React строятся из изолированных частей пользовательского интерфейса, называемых _компонентами_. Компонент React — это функция JavaScript, которую вы можете посыпать разметкой. Компоненты могут быть как маленькими, как кнопка, так и большими, как целая страница. Вот компонент `Gallery`, отображающий три компонента `Profile`:

=== "App.js"

    ```js
    function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/MK3eW3As.jpg"
    			alt="Katherine Johnson"
    		/>
    	);
    }

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/xgy8t9?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Ваш первый компонент](your-first-component.md), чтобы узнать, как объявлять и использовать компоненты React.

## Импорт и экспорт компонентов {#importing-and-exporting-components}

Вы можете объявить много компонентов в одном файле, но в больших файлах может быть трудно ориентироваться. Чтобы решить эту проблему, вы можете _экспортировать_ компонент в свой собственный файл, а затем _импортировать_ этот компонент из другого файла:

=== "Gallery.js"

    ```js
    import Profile from './Profile.js';

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "Profile.js"

    ```js
    export default function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/QIrZWGIs.jpg"
    			alt="Alan L. Hart"
    		/>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/5cgscd?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Импорт и экспорт компонентов](importing-and-exporting-components.md), чтобы узнать, как разделить компоненты на собственные файлы.

## Написание разметки с помощью JSX {#writing-markup-with-jsx}

Каждый компонент React — это функция JavaScript, которая может содержать некоторую разметку, которую React отображает в браузере. Компоненты React используют расширение синтаксиса под названием JSX для представления этой разметки. JSX очень похож на HTML, но он немного строже и может отображать динамическую информацию.

Если мы вставим существующую HTML-разметку в компонент React, она не будет работать:

=== "App.js"

    ```js
    export default function TodoList() {
    return (
    	// This doesn't quite work!
    	<h1>Hedy Lamarr's Todos</h1>
    	<img
    	src="https://i.imgur.com/yXOvdOSs.jpg"
    	alt="Hedy Lamarr"
    	class="photo"
    	>
    	<ul>
    	<li>Invent new traffic lights
    	<li>Rehearse a movie scene
    	<li>Improve spectrum technology
    	</ul>
    );
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/xg5wpt?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Если у вас есть HTML, подобный этому, вы можете исправить его с помощью [конвертера](https://transform.tools/html-to-jsx):

=== "App.js"

    ```js
    export default function TodoList() {
    	return (
    		<>
    			<h1>Hedy Lamarr's Todos</h1>
    			<img
    				src="https://i.imgur.com/yXOvdOSs.jpg"
    				alt="Hedy Lamarr"
    				className="photo"
    			/>
    			<ul>
    				<li>Invent new traffic lights</li>
    				<li>Rehearse a movie scene</li>
    				<li>Improve spectrum technology</li>
    			</ul>
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/w89p79?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Writing Markup with JSX](writing-markup-with-jsx.md), чтобы узнать, как писать правильный JSX.

## JavaScript в JSX с фигурными скобками {#javascript-in-jsx-with-curly-braces}

JSX позволяет вам писать HTML-подобную разметку внутри JavaScript-файла, сохраняя логику рендеринга и содержимое в одном месте. Иногда вы захотите добавить немного логики JavaScript или сослаться на динамическое свойство внутри этой разметки. В этой ситуации вы можете использовать фигурные скобки в JSX, чтобы "открыть окно" в JavaScript:

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

=== "Результат"

    <iframe src="https://codesandbox.io/embed/vppdcf?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Читайте [JavaScript в JSX с фигурными скобками](javascript-in-jsx-with-curly-braces.md), чтобы узнать, как получить доступ к данным JavaScript из JSX.

## Передача пропсов компоненту {#passing-props-to-a-component}

Компоненты React используют _props_ для взаимодействия друг с другом. Каждый родительский компонент может передавать некоторую информацию своим дочерним компонентам, передавая им пропсы. пропсы могут напомнить вам атрибуты HTML, но вы можете передавать через них любые значения JavaScript, включая объекты, массивы, функции и даже JSX!

=== "App.js"

    ```js
    import { getImageUrl } from './utils.js';

    export default function Profile() {
    	return (
    		<Card>
    			<Avatar
    				size={100}
    				person={{
    					name: 'Katsuko Saruhashi',
    					imageId: 'YfeOqp2',
    				}}
    			/>
    		</Card>
    	);
    }

    function Avatar({ person, size }) {
    	return (
    		<img
    			className="avatar"
    			src={getImageUrl(person)}
    			alt={person.name}
    			width={size}
    			height={size}
    		/>
    	);
    }

    function Card({ children }) {
    	return <div className="card">{children}</div>;
    }
    ```

=== "utils.js"

    ```js
    export function getImageUrl(person, size = 's') {
    	return (
    		'https://i.imgur.com/' +
    		person.imageId +
    		size +
    		'.jpg'
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/hqwkhw?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Передача пропсов компоненту](passing-props-to-a-component.md), чтобы узнать, как передавать и читать пропсы.

## Условный рендеринг {#conditional-rendering}

Ваши компоненты часто должны отображать разные вещи в зависимости от различных условий. В React вы можете условно отображать JSX, используя синтаксис JavaScript, такой как операторы `if`, `&&` и `? :`.

В этом примере оператор JavaScript `&&` используется для условного отображения галочки:

=== "App.js"

    ```js
    function Item({ name, isPacked }) {
    	return (
    		<li className="item">
    			{name} {isPacked && '✔'}
    		</li>
    	);
    }

    export default function PackingList() {
    	return (
    		<section>
    			<h1>Sally Ride's Packing List</h1>
    			<ul>
    				<Item isPacked={true} name="Space suit" />
    				<Item
    					isPacked={true}
    					name="Helmet with a golden leaf"
    				/>
    				<Item
    					isPacked={false}
    					name="Photo of Tam"
    				/>
    			</ul>
    		</section>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/lcr4mw?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Условный рендеринг](conditional-rendering.md), чтобы узнать о различных способах условного рендеринга контента.

## Рендеринг списков {#rendering-lists}

Часто требуется отобразить несколько одинаковых компонентов из коллекции данных. Вы можете использовать JavaScript `filter()` и `map()` в React для фильтрации и преобразования массива данных в массив компонентов.

Для каждого элемента массива необходимо указать `ключ`. Обычно в качестве `ключа` используется идентификатор из базы данных. Ключи позволяют React отслеживать место каждого элемента в списке, даже если список меняется.

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

    <iframe src="https://codesandbox.io/embed/gw7t58?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Rendering Lists](rendering-lists.md), чтобы узнать, как отобразить список компонентов и как выбрать ключ.

## Соблюдение чистоты компонентов {#keeping-components-pure}

Некоторые функции JavaScript являются _чистыми._ Чистая функция:

-   **занимается своими делами.** Она не изменяет никаких объектов или переменных, которые существовали до ее вызова.
-   **Одинаковые входные данные, одинаковый выход.** При одинаковых входных данных чистая функция всегда должна возвращать один и тот же результат.

Если вы будете писать свои компоненты только как чистые функции, вы сможете избежать целого класса непонятных ошибок и непредсказуемого поведения по мере роста вашей кодовой базы. Вот пример нечистого компонента:

=== "App.js"

    ```js
    let guest = 0;

    function Cup() {
    	// Bad: changing a preexisting variable!
    	guest = guest + 1;
    	return <h2>Tea cup for guest #{guest}</h2>;
    }

    export default function TeaSet() {
    	return (
    		<>
    			<Cup />
    			<Cup />
    			<Cup />
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/p4p73k?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вы можете сделать этот компонент чистым, передав ему параметр вместо изменения предварительно существующей переменной:

=== "App.js"

    ```js
    function Cup({ guest }) {
    	return <h2>Tea cup for guest #{guest}</h2>;
    }

    export default function TeaSet() {
    	return (
    		<>
    			<Cup guest={1} />
    			<Cup guest={2} />
    			<Cup guest={3} />
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/3mjqv8?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Готовы изучить эту тему?"

    Прочитайте [Keeping Components Pure](keeping-components-pure.md), чтобы узнать, как писать компоненты как чистые, предсказуемые функции.

## Ваш UI как дерево {#your-ui-as-a-tree}

React использует деревья для моделирования отношений между компонентами и модулями.

Дерево рендеринга React - это представление родительских и дочерних отношений между компонентами.

![Древовидный граф с пятью узлами, каждый из которых представляет компонент. Корневой узел расположен в верхней части древовидного графа и обозначен как "Корневой компонент". От него вниз отходят две стрелки, ведущие к двум узлам с метками "Компонент A" и "Компонент C". Каждая из стрелок помечена символом 'renders'. У 'Component A' есть одна стрелка 'renders' к узлу с меткой 'Component B'. У компонента C есть единственная стрелка 'renders' к узлу с меткой 'Component D'.](generic_render_tree.webp)

_Пример дерева рендеринга React._

Компоненты, расположенные в верхней части дерева, рядом с корневым компонентом, считаются компонентами верхнего уровня. Компоненты, не имеющие дочерних компонентов, являются листовыми компонентами. Такое распределение компонентов по категориям полезно для понимания потока данных и производительности рендеринга.

Моделирование отношений между модулями JavaScript - еще один полезный способ понять работу приложения. Мы называем это деревом зависимостей модулей.

![Древовидный граф с пятью узлами. Каждый узел представляет собой модуль JavaScript. Самый верхний узел обозначен как 'RootModule.js'. От него отходят три стрелки к узлам: 'ModuleA.js', 'ModuleB.js' и 'ModuleC.js'. Каждая стрелка обозначена как 'imports'. Узел 'ModuleC.js' имеет единственную стрелку 'imports', которая указывает на узел с меткой 'ModuleD.js'.](generic_dependency_tree.webp)

_Пример дерева зависимостей модулей._

Дерево зависимостей часто используется инструментами сборки для компоновки всего необходимого JavaScript-кода для загрузки и рендеринга клиентом. Большой размер пакета ухудшает пользовательский опыт в React-приложениях. Понимание дерева зависимостей модулей помогает отлаживать такие проблемы.

!!!note "Готовы изучить эту тему?"

    Прочитайте **[Ваш пользовательский интерфейс в виде дерева](./understanding-your-ui-as-a-tree.md)**, чтобы узнать, как создавать деревья зависимостей рендеринга и модулей для приложения React и как они являются полезными ментальными моделями для улучшения пользовательского опыта и производительности.

## Что дальше? {#whats-next}

Перейдите по ссылке [Ваш первый компонент](your-first-component.md), чтобы начать читать эту главу страница за страницей!

Или, если вы уже знакомы с этими темами, почему бы не прочитать [Добаление интерактивности](adding-interactivity.md)?

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/describing-the-ui](https://react.dev/learn/describing-the-ui)</small>
