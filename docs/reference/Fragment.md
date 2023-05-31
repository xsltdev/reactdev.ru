# Fragment

`<Fragment>`, часто используемый через синтаксис <code><>...&lt;/&gt;</code>, позволяет группировать элементы без узла-обертки.

```js
<>
    <OneChild />
    <AnotherChild />
</>
```

## Описание

### `<Fragment>`

Оберните элементы в `<Fragment>`, чтобы сгруппировать их вместе в ситуациях, когда вам нужен один элемент. Группировка элементов в `Fragment` не влияет на результирующий DOM; он такой же, как если бы элементы не были сгруппированы. Пустой JSX-тег <code><>&lt;/&gt;</code> в большинстве случаев является сокращением для `<Fragment></Fragment>`.

#### Параметры

-   **опционально** `key`: Фрагменты, объявленные с явным синтаксисом `<Fragment>`, могут иметь [ключи](../learn/rendering-lists.md).

#### Предупреждения

-   Если вы хотите передать `key` фрагменту, вы не можете использовать синтаксис <code><>...&lt;/&gt;</code>. Вы должны явно импортировать `Fragment` из `'react'` и передать `<Fragment key={yourKey}>...</Fragment>`.

-   React не [сбрасывает состояние](../learn/preserving-and-resetting-state.md), когда вы переходите от рендеринга <code><>&lt;Child /&gt;&lt;/&gt;</code> к `[<Child />]` или обратно, или когда вы переходите от рендеринга <code><><Child /&gt;&lt;/&gt;</code> к `<Child />` и обратно. Это работает только на одном уровне в глубину: например, переход от <code><><><Child /&gt;</&gt;</&gt;</code> к `<Child />` сбрасывает состояние. Точную семантику можно посмотреть [здесь](https://gist.github.com/clemmy/b3ef00f9507909429d8aa0d3ee4f986b).

---

## Использование

### Возвращение нескольких элементов

Используйте `Fragment` или эквивалентный синтаксис <code><>...&lt;/&gt;</code> для группировки нескольких элементов вместе. С его помощью вы можете поместить несколько элементов в любое место, где может находиться один элемент. Например, компонент может вернуть только один элемент, но с помощью фрагмента вы можете сгруппировать несколько элементов вместе и затем вернуть их как группу:

```js
function Post() {
    return (
        <>
            <PostTitle />
            <PostBody />
        </>
    );
}
```

Фрагменты полезны тем, что группировка элементов с помощью фрагмента не влияет на макет или стили, в отличие от того, если бы вы обернули элементы в другой контейнер, например, DOM-элемент. Если вы посмотрите этот пример с помощью инструментов браузера, вы увидите, что все узлы DOM `<h1>` и `<article>` выглядят как родные братья и сестры без оберток вокруг них:

```js
export default function Blog() {
    return (
        <>
            <Post
                title="An update"
                body="It's been a while since I posted..."
            />
            <Post
                title="My new blog"
                body="I am starting a new blog!"
            />
        </>
    );
}

function Post({ title, body }) {
    return (
        <>
            <PostTitle title={title} />
            <PostBody body={body} />
        </>
    );
}

function PostTitle({ title }) {
    return <h1>{title}</h1>;
}

function PostBody({ body }) {
    return (
        <article>
            <p>{body}</p>
        </article>
    );
}
```

!!!note "Как написать фрагмент без специального синтаксиса?"

    Приведенный выше пример эквивалентен импорту `Fragment` из React:

    ```js
    import { Fragment } from 'react';

    function Post() {
    	return (
    		<Fragment>
    			<PostTitle />
    			<PostBody />
    		</Fragment>
    	);
    }
    ```

    Обычно это не нужно, если только вам не нужно передать ключ вашему фрагменту.

---

### Присвоение переменной нескольких элементов

Как и любой другой элемент, вы можете присваивать элементы Fragment переменным, передавать их в качестве реквизитов и так далее:

```js
function CloseDialog() {
    const buttons = (
        <>
            <OKButton />
            <CancelButton />
        </>
    );
    return (
        <AlertDialog buttons={buttons}>
            Are you sure you want to leave this page?
        </AlertDialog>
    );
}
```

---

### Группировка элементов с помощью текста

Вы можете использовать `Fragment` для группировки текста вместе с компонентами:

```js
function DateRangePicker({ start, end }) {
    return (
        <>
            From
            <DatePicker date={start} />
            to
            <DatePicker date={end} />
        </>
    );
}
```

---

### Рендеринг списка фрагментов

Вот ситуация, когда вам нужно написать `Fragment` явно вместо использования синтаксиса <code><>&lt;/&gt;</code>. Когда вы [рендерите несколько элементов в цикле](../learn/rendering-lists.md), вам нужно назначить `key` каждому элементу. Если элементы в цикле являются фрагментами, то для указания атрибута `key` необходимо использовать обычный синтаксис JSX-элементов:

```js
function Blog() {
    return posts.map((post) => (
        <Fragment key={post.id}>
            <PostTitle title={post.title} />
            <PostBody body={post.body} />
        </Fragment>
    ));
}
```

Вы можете просмотреть DOM, чтобы убедиться, что вокруг дочерних элементов фрагмента нет элементов-оберток:

```js
import { Fragment } from 'react';

const posts = [
    {
        id: 1,
        title: 'An update',
        body: "It's been a while since I posted...",
    },
    {
        id: 2,
        title: 'My new blog',
        body: 'I am starting a new blog!',
    },
];

export default function Blog() {
    return posts.map((post) => (
        <Fragment key={post.id}>
            <PostTitle title={post.title} />
            <PostBody body={post.body} />
        </Fragment>
    ));
}

function PostTitle({ title }) {
    return <h1>{title}</h1>;
}

function PostBody({ body }) {
    return (
        <article>
            <p>{body}</p>
        </article>
    );
}
```

## Ссылки

-   [https://react.dev/reference/react/Fragment](https://react.dev/reference/react/Fragment)
