# Добавление интерактивности

Некоторые элементы на экране обновляются в ответ на ввод пользователя. Например, щелчок по галерее изображений переключает активное изображение. В React данные, которые изменяются со временем, называются _состояние_. Вы можете добавить состояние в любой компонент и обновлять его по мере необходимости. В этой главе вы узнаете, как писать компоненты, которые обрабатывают взаимодействия, обновляют свое состояние и отображают различные результаты с течением времени.

-   [Как обрабатывать события, инициированные пользователем](responding-to-events.md)
-   [Как заставить компоненты "запоминать" информацию с помощью состояния](state-a-components-memory.md)
-   [Как React обновляет UI в два этапа](render-and-commit.md)
-   [Почему состояние не обновляется сразу после его изменения](state-as-a-snapshot.md)
-   [Как поставить в очередь несколько обновлений состояния](queueing-a-series-of-state-updates.md)
-   [Как обновить объект в состоянии](updating-objects-in-state.md)
-   [Как обновить массив в состоянии](updating-arrays-in-state.md)

## Реагирование на события

React позволяет добавлять _обработчики событий_ в JSX. Обработчики событий - это ваши собственные функции, которые будут запускаться в ответ на действия пользователя, такие как нажатие, наведение курсора, фокусировка на вводе формы и так далее.

Встроенные компоненты, такие как `<button>`, поддерживают только встроенные события браузера, такие как `onClick`. Однако вы также можете создавать собственные компоненты и давать их реквизитам обработчиков событий любые имена, специфичные для конкретного приложения.

<!-- 0001.part.md -->

```js
export default function App() {
    return (
        <Toolbar
            onPlayMovie={() => alert('Playing!')}
            onUploadImage={() => alert('Uploading!')}
        />
    );
}

function Toolbar({ onPlayMovie, onUploadImage }) {
    return (
        <div>
            <Button onClick={onPlayMovie}>
                Play Movie
            </Button>
            <Button onClick={onUploadImage}>
                Upload Image
            </Button>
        </div>
    );
}

function Button({ onClick, children }) {
    return <button onClick={onClick}>{children}</button>;
}
```

<!-- 0004.part.md -->

Прочитайте **[Responding to Events](responding-to-events.md)**, чтобы узнать, как добавлять обработчики событий.

## Состояние: память компонента

Компоненты часто нуждаются в изменении того, что отображается на экране в результате взаимодействия. Ввод текста в форму должен обновить поле ввода, нажатие кнопки "next" на карусели изображений должно изменить отображаемое изображение, нажатие кнопки "buy" помещает товар в корзину. Компоненты должны "запоминать" вещи: текущее значение ввода, текущее изображение, корзину. В React такая память, специфичная для компонента, называется _state._.

Вы можете добавить состояние в компонент с помощью хука [`useState`](../reference/useState.md). _Хуки_ - это специальные функции, которые позволяют вашим компонентам использовать возможности React (состояние - одна из таких возможностей). Хук `useState` позволяет вам объявить переменную состояния. Он принимает начальное состояние и возвращает пару значений: текущее состояние и функцию-установщик состояния, которая позволяет вам обновить его.

<!-- 0005.part.md -->

```js
const [index, setIndex] = useState(0);
const [showMore, setShowMore] = useState(false);
```

<!-- 0006.part.md -->

Вот как галерея изображений использует и обновляет состояние по щелчку мыши:

<!-- 0007.part.md -->

=== "App.js"

    ```js
    import { useState } from 'react';
    import { sculptureList } from './data.js';

    export default function Gallery() {
    	const [index, setIndex] = useState(0);
    	const [showMore, setShowMore] = useState(false);
    	const hasNext = index < sculptureList.length - 1;

    	function handleNextClick() {
    		if (hasNext) {
    			setIndex(index + 1);
    		} else {
    			setIndex(0);
    		}
    	}

    	function handleMoreClick() {
    		setShowMore(!showMore);
    	}

    	let sculpture = sculptureList[index];
    	return (
    		<>
    			<button onClick={handleNextClick}>Next</button>
    			<h2>
    				<i>{sculpture.name} </i>
    				by {sculpture.artist}
    			</h2>
    			<h3>
    				({index + 1} of {sculptureList.length})
    			</h3>
    			<button onClick={handleMoreClick}>
    				{showMore ? 'Hide' : 'Show'} details
    			</button>
    			{showMore && <p>{sculpture.description}</p>}
    			<img src={sculpture.url} alt={sculpture.alt} />
    		</>
    	);
    }
    ```

=== "data.js"

    ```js
    export const sculptureList = [
    	{
    		name: 'Homenaje a la Neurocirugía',
    		artist: 'Marta Colvin Andrade',
    		description:
    			'Although Colvin is predominantly known for abstract themes that allude to pre-Hispanic symbols, this gigantic sculpture, an homage to neurosurgery, is one of her most recognizable public art pieces.',
    		url: 'https://i.imgur.com/Mx7dA2Y.jpg',
    		alt:
    			'A bronze statue of two crossed hands delicately holding a human brain in their fingertips.',
    	},
    	{
    		name: 'Floralis Genérica',
    		artist: 'Eduardo Catalano',
    		description:
    			'This enormous (75 ft. or 23m) silver flower is located in Buenos Aires. It is designed to move, closing its petals in the evening or when strong winds blow and opening them in the morning.',
    		url: 'https://i.imgur.com/ZF6s192m.jpg',
    		alt:
    			'A gigantic metallic flower sculpture with reflective mirror-like petals and strong stamens.',
    	},
    	{
    		name: 'Eternal Presence',
    		artist: 'John Woodrow Wilson',
    		description:
    			'Wilson was known for his preoccupation with equality, social justice, as well as the essential and spiritual qualities of humankind. This massive (7ft. or 2,13m) bronze represents what he described as "a symbolic Black presence infused with a sense of universal humanity."',
    		url: 'https://i.imgur.com/aTtVpES.jpg',
    		alt:
    			'The sculpture depicting a human head seems ever-present and solemn. It radiates calm and serenity.',
    	},
    	{
    		name: 'Moai',
    		artist: 'Unknown Artist',
    		description:
    			'Located on the Easter Island, there are 1,000 moai, or extant monumental statues, created by the early Rapa Nui people, which some believe represented deified ancestors.',
    		url: 'https://i.imgur.com/RCwLEoQm.jpg',
    		alt:
    			'Three monumental stone busts with the heads that are disproportionately large with somber faces.',
    	},
    	{
    		name: 'Blue Nana',
    		artist: 'Niki de Saint Phalle',
    		description:
    			'The Nanas are triumphant creatures, symbols of femininity and maternity. Initially, Saint Phalle used fabric and found objects for the Nanas, and later on introduced polyester to achieve a more vibrant effect.',
    		url: 'https://i.imgur.com/Sd1AgUOm.jpg',
    		alt:
    			'A large mosaic sculpture of a whimsical dancing female figure in a colorful costume emanating joy.',
    	},
    	{
    		name: 'Ultimate Form',
    		artist: 'Barbara Hepworth',
    		description:
    			'This abstract bronze sculpture is a part of The Family of Man series located at Yorkshire Sculpture Park. Hepworth chose not to create literal representations of the world but developed abstract forms inspired by people and landscapes.',
    		url: 'https://i.imgur.com/2heNQDcm.jpg',
    		alt:
    			'A tall sculpture made of three elements stacked on each other reminding of a human figure.',
    	},
    	{
    		name: 'Cavaliere',
    		artist: 'Lamidi Olonade Fakeye',
    		description:
    			"Descended from four generations of woodcarvers, Fakeye's work blended traditional and contemporary Yoruba themes.",
    		url: 'https://i.imgur.com/wIdGuZwm.png',
    		alt:
    			'An intricate wood sculpture of a warrior with a focused face on a horse adorned with patterns.',
    	},
    	{
    		name: 'Big Bellies',
    		artist: 'Alina Szapocznikow',
    		description:
    			'Szapocznikow is known for her sculptures of the fragmented body as a metaphor for the fragility and impermanence of youth and beauty. This sculpture depicts two very realistic large bellies stacked on top of each other, each around five feet (1,5m) tall.',
    		url: 'https://i.imgur.com/AlHTAdDm.jpg',
    		alt:
    			'The sculpture reminds a cascade of folds, quite different from bellies in classical sculptures.',
    	},
    	{
    		name: 'Terracotta Army',
    		artist: 'Unknown Artist',
    		description:
    			'The Terracotta Army is a collection of terracotta sculptures depicting the armies of Qin Shi Huang, the first Emperor of China. The army consisted of more than 8,000 soldiers, 130 chariots with 520 horses, and 150 cavalry horses.',
    		url: 'https://i.imgur.com/HMFmH6m.jpg',
    		alt:
    			'12 terracotta sculptures of solemn warriors, each with a unique facial expression and armor.',
    	},
    	{
    		name: 'Lunar Landscape',
    		artist: 'Louise Nevelson',
    		description:
    			'Nevelson was known for scavenging objects from New York City debris, which she would later assemble into monumental constructions. In this one, she used disparate parts like a bedpost, juggling pin, and seat fragment, nailing and gluing them into boxes that reflect the influence of Cubism’s geometric abstraction of space and form.',
    		url: 'https://i.imgur.com/rN7hY6om.jpg',
    		alt:
    			'A black matte sculpture where the individual elements are initially indistinguishable.',
    	},
    	{
    		name: 'Aureole',
    		artist: 'Ranjani Shettar',
    		description:
    			'Shettar merges the traditional and the modern, the natural and the industrial. Her art focuses on the relationship between man and nature. Her work was described as compelling both abstractly and figuratively, gravity defying, and a "fine synthesis of unlikely materials."',
    		url: 'https://i.imgur.com/okTpbHhm.jpg',
    		alt:
    			'A pale wire-like sculpture mounted on concrete wall and descending on the floor. It appears light.',
    	},
    	{
    		name: 'Hippos',
    		artist: 'Taipei Zoo',
    		description:
    			'The Taipei Zoo commissioned a Hippo Square featuring submerged hippos at play.',
    		url: 'https://i.imgur.com/6o5Vuyu.jpg',
    		alt:
    			'A group of bronze hippo sculptures emerging from the sett sidewalk as if they were swimming.',
    	},
    ];
    ```

Прочитайте **[State: A Component's Memory](state-a-components-memory.md)**, чтобы узнать, как запомнить значение и обновлять его при взаимодействии.

## Рендеринг и фиксация

Прежде чем ваши компоненты будут отображены на экране, они должны быть отрендерены React. Понимание этапов этого процесса поможет вам задуматься о том, как выполняется ваш код, и объяснить его поведение.

Представьте, что ваши компоненты - это повара на кухне, собирающие вкусные блюда из ингредиентов. В этом сценарии React - это официант, который выполняет запросы клиентов и приносит им их заказы. Этот процесс запроса и подачи пользовательского интерфейса состоит из трех этапов:

1.  **Триггер** рендеринга (доставка заказа посетителя на кухню).
2.  **Рендеринг** компонента (подготовка заказа на кухне)
3.  **Коммитирование** в DOM (размещение заказа на столе)

Прочитайте **[Render and Commit](render-and-commit.md)**, чтобы узнать о жизненном цикле обновления пользовательского интерфейса.

## Состояние как моментальный снимок

В отличие от обычных переменных JavaScript, состояние в React ведет себя скорее как моментальный снимок. Его установка не изменяет уже имеющуюся переменную state, а вместо этого вызывает повторный рендеринг. Это может быть удивительно при первом!

<!-- 0013.part.md -->

```js
console.log(count); // 0
setCount(count + 1); // Request a re-render with 1
console.log(count); // Still 0!
```

<!-- 0014.part.md -->

Такое поведение поможет вам избежать мелких ошибок. Вот небольшое приложение для чата. Попробуйте угадать, что произойдет, если вы сначала нажмете "Отправить", а затем _потом_ измените получателя на Боба. Чье имя появится в `оповещении` пять секунд спустя?

<!-- 0015.part.md -->

```js
import { useState } from 'react';

export default function Form() {
    const [to, setTo] = useState('Alice');
    const [message, setMessage] = useState('Hello');

    function handleSubmit(e) {
        e.preventDefault();
        setTimeout(() => {
            alert(`You said ${message} to ${to}`);
        }, 5000);
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>
                To:{' '}
                <select
                    value={to}
                    onChange={(e) => setTo(e.target.value)}
                >
                    <option value="Alice">Alice</option>
                    <option value="Bob">Bob</option>
                </select>
            </label>
            <textarea
                placeholder="Message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <button type="submit">Send</button>
        </form>
    );
}
```

Прочитайте **[State as a Snapshot](state-as-a-snapshot.md)**, чтобы узнать, почему состояние кажется "фиксированным" и неизменным внутри обработчиков событий.

## Постановка в очередь серии обновлений состояния

Этот компонент имеет ошибку: нажатие на "+3" увеличивает счет только один раз.

<!-- 0019.part.md -->

```js
import { useState } from 'react';

export default function Counter() {
    const [score, setScore] = useState(0);

    function increment() {
        setScore(score + 1);
    }

    return (
        <>
            <button onClick={() => increment()}>+1</button>
            <button
                onClick={() => {
                    increment();
                    increment();
                    increment();
                }}
            >
                +3
            </button>
            <h1>Score: {score}</h1>
        </>
    );
}
```

<!-- 0022.part.md -->

[State as a Snapshot](state-as-a-snapshot.md) объясняет, почему это происходит. Установка состояния запрашивает новый рендеринг, но не изменяет его в уже запущенном коде. Поэтому `score` продолжает быть `0` сразу после вызова `setScore(score + 1)`.

<!-- 0023.part.md -->

```js
console.log(score); // 0
setScore(score + 1); // setScore(0 + 1);
console.log(score); // 0
setScore(score + 1); // setScore(0 + 1);
console.log(score); // 0
setScore(score + 1); // setScore(0 + 1);
console.log(score); // 0
```

<!-- 0024.part.md -->

Это можно исправить, передав _обновляющую функцию_ при установке состояния. Обратите внимание, как замена `setScore(score + 1)` на `setScore(s => s + 1)` исправляет кнопку "+3". Это позволяет поставить в очередь несколько обновлений состояния.

<!-- 0025.part.md -->

```js
import { useState } from 'react';

export default function Counter() {
    const [score, setScore] = useState(0);

    function increment() {
        setScore((s) => s + 1);
    }

    return (
        <>
            <button onClick={() => increment()}>+1</button>
            <button
                onClick={() => {
                    increment();
                    increment();
                    increment();
                }}
            >
                +3
            </button>
            <h1>Score: {score}</h1>
        </>
    );
}
```

Читайте **[Постановка в очередь серии обновлений состояния](queueing-a-series-of-state-updates.md)**, чтобы узнать, как поставить в очередь последовательность обновлений состояния.

## Обновление объектов в состоянии

Состояние может содержать любые значения JavaScript, включая объекты. Но вы не должны изменять объекты и массивы, которые хранятся в состоянии React, напрямую. Вместо этого, когда вы хотите обновить объект или массив, вам нужно создать новый (или сделать копию существующего), а затем обновить состояние, чтобы использовать эту копию.

Обычно для копирования объектов и массивов, которые вы хотите изменить, используется синтаксис распространения `...`. Например, обновление вложенного объекта может выглядеть следующим образом:

<!-- 0029.part.md -->

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

<!-- 0032.part.md -->

Если копирование объектов в коде становится утомительным, вы можете использовать библиотеку типа [Immer](https://github.com/immerjs/use-immer) для сокращения повторяющегося кода:

<!-- 0033.part.md -->

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

Прочитайте **[Обновление объектов в состоянии](updating-objects-in-state.md)**, чтобы узнать, как правильно обновлять объекты.

## Обновление массивов в состоянии

Массивы - это еще один тип изменяемых объектов JavaScript, которые вы можете хранить в состоянии и должны рассматривать как доступные только для чтения. Как и в случае с объектами, когда вы хотите обновить массив, хранящийся в состоянии, вам нужно создать новый массив (или сделать копию существующего), а затем установить состояние для использования нового массива:

<!-- 0039.part.md -->

```js
import { useState } from 'react';

let nextId = 3;
const initialList = [
    { id: 0, title: 'Big Bellies', seen: false },
    { id: 1, title: 'Lunar Landscape', seen: false },
    { id: 2, title: 'Terracotta Army', seen: true },
];

export default function BucketList() {
    const [list, setList] = useState(initialList);

    function handleToggle(artworkId, nextSeen) {
        setList(
            list.map((artwork) => {
                if (artwork.id === artworkId) {
                    return { ...artwork, seen: nextSeen };
                } else {
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
                artworks={list}
                onToggle={handleToggle}
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

<!-- 0040.part.md -->

Если копирование массивов в коде становится утомительным, вы можете использовать библиотеку типа [Immer](https://github.com/immerjs/use-immer) для сокращения повторяющегося кода:

<!-- 0041.part.md -->

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
    const [list, updateList] = useImmer(initialList);

    function handleToggle(artworkId, nextSeen) {
        updateList((draft) => {
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
                artworks={list}
                onToggle={handleToggle}
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

Прочитайте **[Обновление массивов в состоянии](updating-arrays-in-state.md)**, чтобы узнать, как правильно обновлять массивы.

## Что дальше?

Перейдите по ссылке [Responding to Events](responding-to-events.md), чтобы начать читать эту главу страница за страницей!

Или, если вы уже знакомы с этими темами, почему бы не прочитать [Управление состоянием](managing-state.md)?

<!-- 0045.part.md -->
