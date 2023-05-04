# Рендеринг списков

Часто требуется отобразить несколько одинаковых компонентов из набора данных. Для работы с массивом данных можно использовать методы [JavaScript array methods](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array#). На этой странице вы будете использовать [`filter()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) и [`map()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map) в React для фильтрации и преобразования массива данных в массив компонентов.

-   Как выводить компоненты из массива с помощью JavaScript `map()`.
-   Как отобразить только определенные компоненты с помощью JavaScript `filter()`.
-   Когда и зачем использовать ключи React

## Рендеринг данных из массивов

Допустим, у вас есть список содержимого.

<!-- 0001.part.md -->

```js
<ul>
    <li>Creola Katherine Johnson: mathematician</li>
    <li>Mario José Molina-Pasquel Henríquez: chemist</li>
    <li>Mohammad Abdus Salam: physicist</li>
    <li>Percy Lavon Julian: chemist</li>
    <li>Subrahmanyan Chandrasekhar: astrophysicist</li>
</ul>
```

<!-- 0002.part.md -->

Единственное различие между этими элементами списка - это их содержимое, их данные. При построении интерфейсов часто требуется отображать несколько экземпляров одного и того же компонента, используя разные данные: от списков комментариев до галерей изображений профиля. В таких ситуациях вы можете хранить эти данные в объектах и массивах JavaScript и использовать такие методы, как [`map()`](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Array/map) и [`filter()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) для вывода списков компонентов на их основе.

Вот краткий пример того, как сформировать список элементов из массива:

**1. Переместите** данные в массив:

<!-- конец списка -->

<!-- 0003.part.md -->

```js
const people = [
    'Creola Katherine Johnson: mathematician',
    'Mario José Molina-Pasquel Henríquez: chemist',
    'Mohammad Abdus Salam: physicist',
    'Percy Lavon Julian: chemist',
    'Subrahmanyan Chandrasekhar: astrophysicist',
];
```

<!-- 0004.part.md -->

**2. Мап** членов `people` в новый массив узлов JSX, `listItems`:

<!-- конец списка -->

<!-- 0005.part.md -->

```js
const listItems = people.map((person) => <li>{person}</li>);
```

<!-- 0006.part.md -->

**3. Возвращает** `listItems` из вашего компонента, обернутого в `<ul>`:

<!-- end list -->

<!-- 0007.part.md -->

```js
return <ul>{listItems}</ul>;
```

<!-- 0008.part.md -->

Вот результат:

<!-- 0009.part.md -->

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

<!-- 0012.part.md -->

Обратите внимание, что в песочнице выше отображается консольная ошибка:

Предупреждение: Каждый дочерний элемент списка должен иметь уникальный реквизит "ключ".

Как исправить эту ошибку, вы узнаете позже на этой странице. Прежде чем мы приступим к этому, давайте добавим немного структуры в ваши данные.

## Фильтрация массивов элементов

Эти данные можно структурировать еще больше.

<!-- 0013.part.md -->

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

<!-- 0014.part.md -->

Допустим, вам нужно показать только людей, чья профессия - `химик`. Вы можете использовать метод JavaScript `filter()`, чтобы вернуть только таких людей. Этот метод принимает массив элементов, пропускает их через "тест" (функцию, которая возвращает `true` или `false`) и возвращает новый массив только тех элементов, которые прошли тест (вернули `true`).

Вам нужны только те элементы, где `профессия` - `"химик"`. Функция "test" для этого выглядит как `(person) => person.profession === 'chemist'`. Вот как это можно сделать:

**1.** **Создаем** новый массив только "химиков", `chemists`, вызывая `filter()` на `people`, фильтруя по `person.profession === 'chemist'`:

<!-- конец списка -->

<!-- 0015.part.md -->

```js
const chemists = people.filter(
    (person) => person.profession === 'chemist'
);
```

<!-- 0016.part.md -->

**2.** Теперь **составьте карту** над `химиками`:

<!-- конец списка -->

<!-- 0017.part.md -->

```js
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

<!-- 0018.part.md -->

**3.** И наконец, **возвратите** список `listItems` из вашего компонента:

<!-- конец списка -->

<!-- 0019.part.md -->

```js
return <ul>{listItems}</ul>;
```

<!-- 0020.part.md -->

<!-- 0021.part.md -->

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

<!-- 0022.part.md -->

<!-- 0023.part.md -->

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

<!-- 0024.part.md -->

<!-- 0025.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0028.part.md -->

Стрелочные функции неявно возвращают выражение сразу после `=>`, поэтому оператор `возврата` не нужен:

<!-- 0029.part.md -->

```js
const listItems = chemists.map(
    (person) => <li>...</li> // Implicit return!
);
```

<!-- 0030.part.md -->

Однако **вы должны явно написать `return`, если за вашим `=>` следует `{` фигурная скобка\!**.

<!-- 0031.part.md -->

```js
const listItems = chemists.map((person) => {
    // Curly brace
    return <li>...</li>;
});
```

<!-- 0032.part.md -->

Стрелочные функции, содержащие `=> {`, как говорят, имеют ["тело блока".](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Functions/Arrow_functions#function_body) Они позволяют вам написать больше, чем одну строку кода, но вы _должны_ сами написать оператор `возврата`. Если вы забудете об этом, ничего не будет возвращено!

## Упорядочивание элементов списка по `ключу`

Обратите внимание, что все приведенные выше песочницы выдают ошибку в консоли:

Предупреждение: Каждый дочерний элемент списка должен иметь уникальный реквизит "ключ".

Вам нужно дать каждому элементу массива `ключ` - строку или число, которое уникально идентифицирует его среди других элементов этого массива:

<!-- 0033.part.md -->

```js
<li key={person.id}>...</li>
```

<!-- 0034.part.md -->

JSX-элементы непосредственно внутри вызова `map()` всегда нуждаются в ключах!

Ключи указывают React, какому элементу массива соответствует каждый компонент, чтобы он мог сопоставить их позже. Это становится важным, если элементы массива могут перемещаться (например, из-за сортировки), вставляться или удаляться. Хорошо подобранный `ключ` помогает React понять, что именно произошло, и сделать правильные обновления в DOM-дереве.

Вместо того чтобы генерировать ключи "на лету", вы должны включать их в свои данные:

<!-- 0035.part.md -->

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

<!-- 0036.part.md -->

<!-- 0037.part.md -->

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

<!-- 0038.part.md -->

<!-- 0039.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0042.part.md -->

#### Отображение нескольких узлов DOM для каждого элемента списка

Что делать, если каждый элемент должен отображать не один, а несколько узлов DOM?

Короткий синтаксис [`<>...</>` Fragment](/reference/react/Fragment) не позволит вам передать ключ, поэтому вам нужно либо сгруппировать их в один `<div>`, либо использовать немного более длинный и [более явный синтаксис `<Fragment>`:](/reference/react/Fragment#rendering-a-list-of-fragments)

<!-- 0043.part.md -->

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

<!-- 0044.part.md -->

Фрагменты исчезают из DOM, поэтому будет получен плоский список `<h1>`, `<p>`, `<h1>`, `<p>` и так далее.

### Где взять ваш `ключ`

Различные источники данных предоставляют различные источники ключей:

-   **Данные из базы данных:** Если ваши данные поступают из базы данных, вы можете использовать ключи/идентификаторы базы данных, которые уникальны по своей природе.
-   **Локально генерируемые данные:** Если ваши данные генерируются и сохраняются локально (например, заметки в приложении для ведения записей), при создании элементов используйте инкрементирующий счетчик, [`crypto.randomUUID()`](https://developer.mozilla.org/ru/docs/Web/API/Crypto/randomUUID) или пакет типа [`uuid`](https://www.npmjs.com/package/uuid).

### Правила ключей

-   **Ключи должны быть уникальными среди братьев и сестер.** Однако, можно использовать одинаковые ключи для JSX-узлов в _разных_ массивах.
-   **Ключи не должны меняться**, иначе это противоречит их назначению! Не генерируйте их во время рендеринга.

### Зачем React нужны ключи?

Представьте, что файлы на вашем рабочем столе не имеют имен. Вместо этого вы обращаетесь к ним по порядку - первый файл, второй файл и так далее. К этому можно было бы привыкнуть, но когда вы удалите файл, все запутается. Второй файл станет первым, третий - вторым и так далее.

Имена файлов в папке и JSX-ключи в массиве служат аналогичной цели. Они позволяют нам однозначно идентифицировать элемент между его родственниками. Хорошо подобранный ключ предоставляет больше информации, чем позиция в массиве. Даже если _позиция_ меняется из-за переупорядочивания, `ключ` позволяет React идентифицировать элемент на протяжении всего его существования.

У вас может возникнуть соблазн использовать индекс элемента в массиве в качестве ключа. На самом деле, именно это будет использовать React, если вы вообще не укажете `key`. Но порядок, в котором вы отображаете элементы, будет меняться со временем, если элемент будет вставлен, удален или массив будет переупорядочен. Индекс в качестве ключа часто приводит к тонким и запутанным ошибкам.

Аналогично, не генерируйте ключи на лету, например, с помощью `key={Math.random()}`. Это приведет к тому, что ключи никогда не будут совпадать между рендерами, что приведет к тому, что все ваши компоненты и DOM будут каждый раз создаваться заново. Это не только медленно, но и приведет к потере пользовательского ввода внутри элементов списка. Вместо этого используйте стабильный идентификатор, основанный на данных.

Обратите внимание, что ваши компоненты не будут получать `key` в качестве реквизита. Он используется только в качестве подсказки самим React. Если вашему компоненту нужен ID, вы должны передать его как отдельный реквизит: `<Profile key={id} userId={id} />`.

На этой странице вы узнали:

-   Как перемещать данные из компонентов в структуры данных, такие как массивы и объекты.
-   Как генерировать наборы похожих компонентов с помощью функции JavaScript `map()`.
-   Как создавать массивы отфильтрованных элементов с помощью функции JavaScript `filter()`.
-   Зачем и как устанавливать `key` для каждого компонента в коллекции, чтобы React мог отслеживать каждый из них, даже если их положение или данные меняются.

#### Разделение списка на две части

<!-- 0045.part.md -->

В этом примере показан список всех людей.

Измените его, чтобы последовательно вывести два отдельных списка: **Химики** и **Все остальные.** Как и ранее, вы можете определить, является ли человек химиком, проверив, что `person.profession === 'chemist'`.

<!-- 0046.part.md -->

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

<!-- 0047.part.md -->

<!-- 0048.part.md -->

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

<!-- 0049.part.md -->

<!-- 0050.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0053.part.md -->

Вы можете использовать `filter()` дважды, создавая два отдельных массива, а затем `map` над обоими массивами:

<!-- 0054.part.md -->

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

<!-- 0055.part.md -->

<!-- 0056.part.md -->

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

<!-- 0057.part.md -->

<!-- 0058.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0061.part.md -->

В данном решении вызовы `map` размещены непосредственно в родительских элементах `<ul>`, но вы можете ввести для них переменные, если считаете это более читабельным.

Между отображаемыми списками все еще есть некоторое дублирование. Можно пойти дальше и извлечь повторяющиеся части в компонент `<ListSection>`:

<!-- 0062.part.md -->

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

<!-- 0063.part.md -->

<!-- 0064.part.md -->

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

<!-- 0065.part.md -->

<!-- 0066.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0069.part.md -->

Очень внимательный читатель может заметить, что при двух вызовах `filter` мы проверяем профессию каждого человека дважды. Проверка свойства происходит очень быстро, поэтому в данном примере это нормально. Если бы ваша логика была более дорогой, вы могли бы заменить вызовы `фильтра` циклом, который вручную строит массивы и проверяет каждого человека один раз.

На самом деле, если `people` никогда не меняется, вы можете вынести этот код за пределы вашего компонента. С точки зрения React, все, что имеет значение, это то, что в конечном итоге вы даете ему массив JSX-узлов. Ему все равно, как вы создадите этот массив:

<!-- 0070.part.md -->

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

<!-- 0071.part.md -->

<!-- 0072.part.md -->

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

<!-- 0073.part.md -->

<!-- 0074.part.md -->

```js
export function getImageUrl(person) {
    return (
        'https://i.imgur.com/' + person.imageId + 's.jpg'
    );
}
```

<!-- 0077.part.md -->

#### Вложенные списки в одном компоненте

Создайте список рецептов из этого массива! Для каждого рецепта в массиве выведите его название в виде `<h2>` и список ингредиентов в виде `<ul>`.

Это потребует вложения двух различных вызовов `map`.

<!-- 0078.part.md -->

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

<!-- 0079.part.md -->

<!-- 0080.part.md -->

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

<!-- 0081.part.md -->

Вот один из способов, которым вы можете воспользоваться:

<!-- 0082.part.md -->

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

<!-- 0083.part.md -->

<!-- 0084.part.md -->

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

<!-- 0085.part.md -->

Каждый из `рецептов` уже содержит поле `id`, поэтому именно его использует внешний цикл для своего `ключа`. Нет никакого идентификатора, который можно было бы использовать для перебора ингредиентов. Однако разумно предположить, что один и тот же ингредиент не будет указан дважды в одном рецепте, поэтому его название может служить в качестве `ключа`. В качестве альтернативы можно изменить структуру данных, добавив идентификаторы, или использовать индекс в качестве `ключа` (с оговоркой, что вы не сможете безопасно переупорядочить ингредиенты).

#### Извлечение компонента элемента списка

Этот компонент `RecipeList` содержит два вложенных вызова `map`. Чтобы упростить его, извлеките из него компонент `Recipe`, который будет принимать реквизиты `id`, `name` и `ingredients`. Где вы разместите внешний `key` и почему?

<!-- 0086.part.md -->

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

<!-- 0087.part.md -->

<!-- 0088.part.md -->

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

<!-- 0089.part.md -->

Вы можете скопировать-вставить JSX из внешней `map` в новый компонент `Recipe` и вернуть этот JSX. Затем вы можете изменить `recipe.name` на `name`, `recipe.id` на `id`, и так далее, и передать их в качестве реквизитов в `Recipe`:

<!-- 0090.part.md -->

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

<!-- 0091.part.md -->

<!-- 0092.part.md -->

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

<!-- 0093.part.md -->

Здесь `<Recipe {...recipe} key={recipe.id} />` - это синтаксическое сокращение, говорящее "передать все свойства объекта `recipe` в качестве реквизитов компоненту `Recipe`". Вы также можете записать каждый реквизит в явном виде: `<Recipe id={recipe.id} name={recipe.name} ingredients={recipe.ingredients} key={recipe.id} />`.

**Обратите внимание, что `key` указывается на самом `<Recipe>`, а не на корне `<div>`, возвращаемом из `Recipe`.** Это потому, что этот `key` нужен непосредственно в контексте окружающего массива. Раньше у вас был массив `<div>`, и каждый из них нуждался в `ключе`, а теперь у вас есть массив `<Recipe>`. Другими словами, когда вы извлекаете компонент, не забудьте оставить `ключ` вне JSX, который вы копируете и вставляете.

#### Список с разделителем

Этот пример отображает знаменитое хайку Кацусики Хокусая, каждая строка которого обернута в тег `<p>`. Ваша задача - вставить разделитель `<hr />` между каждым абзацем. Ваша результирующая структура должна выглядеть следующим образом:

<!-- 0094.part.md -->

```js
<article>
    <p>I write, erase, rewrite</p>
    <hr />
    <p>Erase again, and then</p>
    <hr />
    <p>A poppy blooms.</p>
</article>
```

<!-- 0095.part.md -->

В хайку всего три строки, но ваше решение должно работать с любым количеством строк. Обратите внимание, что элементы `<hr />` появляются только _между_ элементами `<p>`, а не в начале или конце!

<!-- 0096.part.md -->

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

<!-- 0099.part.md -->

(Это редкий случай, когда индекс в качестве ключа допустим, потому что строки стихотворения никогда не будут перестраиваться).

Вам нужно либо преобразовать `map` в ручной цикл, либо использовать фрагмент.

Вы можете написать ручной цикл, вставляя `<hr />` и `<p>...</p>` в выходной массив по мере выполнения:

<!-- 0100.part.md -->

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

<!-- 0103.part.md -->

Использование исходного индекса строки в качестве `ключа` больше не работает, поскольку каждый разделитель и абзац теперь находятся в одном массиве. Однако вы можете дать каждому из них отдельный ключ, используя суффикс, например, `key={i + '-text'}`.

В качестве альтернативы можно вывести коллекцию фрагментов, содержащих `<hr />` и `<p>...</p>`. Однако синтаксис сокращения `<>...</>` не поддерживает передачу ключей, поэтому вам придется явно написать `<фрагмент>`:

<!-- 0104.part.md -->

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

<!-- 0107.part.md -->

Помните, что фрагменты (часто записываемые как `<> </>`) позволяют вам группировать узлы JSX без добавления лишних `<div>`!

<!-- 0108.part.md -->
