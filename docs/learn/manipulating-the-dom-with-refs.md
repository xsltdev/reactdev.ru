# Манипулирование DOM с помощью Refs

React автоматически обновляет [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model/Introduction) в соответствии с вашим выводом на экран, поэтому вашим компонентам не часто требуется манипулировать им. Однако иногда вам может понадобиться доступ к элементам DOM, управляемым React - например, для фокусировки узла, прокрутки к нему или измерения его размера и положения. Встроенного способа сделать это в React нет, поэтому вам понадобится _ref_ на узел DOM.

-   Как получить доступ к узлу DOM, управляемому React, с помощью атрибута `ref`
-   Как JSX-атрибут `ref` связан с хуком `useRef`.
-   Как получить доступ к DOM-узлу другого компонента
-   В каких случаях безопасно изменять DOM под управлением React

## Получение ссылки на узел {/_getting-a-ref-to-the-node_/}

Чтобы получить доступ к узлу DOM, управляемому React, сначала импортируйте хук `useRef`:

<!-- 0001.part.md -->

```js
import { useRef } from 'react';
```

<!-- 0002.part.md -->

Затем используйте его для объявления ссылки внутри вашего компонента:

<!-- 0003.part.md -->

```js
const myRef = useRef(null);
```

<!-- 0004.part.md -->

Наконец, передайте его узлу DOM в качестве атрибута `ref`:

<!-- 0005.part.md -->

```js
<div ref={myRef}>
```

<!-- 0006.part.md -->

The `useRef` Hook returns an object with a single property called `current`. Initially, `myRef.current` will be `null`. When React creates a DOM node for this `<div>`, React will put a reference to this node into `myRef.current`. You can then access this DOM node from your [event handlers](responding-to-events.md) and use the built-in [browser APIs](https://developer.mozilla.org/docs/Web/API/Element) defined on it.

<!-- 0007.part.md -->

```js
// You can use any browser APIs, for example:
myRef.current.scrollIntoView();
```

<!-- 0008.part.md -->

### Пример: Фокусировка текстового ввода {/_example-focusing-a-text-input_/}

В этом примере нажатие на кнопку фокусирует ввод:

<!-- 0009.part.md -->

```js
import { useRef } from 'react';

export default function Form() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <input ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

<!-- 0010.part.md -->

To implement this:

1.  Declare `inputRef` with the `useRef` Hook.
2.  Pass it as `<input ref={inputRef}>`. This tells React to **put this `<input>`’s DOM node into `inputRef.current`.**
3.  In the `handleClick` function, read the input DOM node from `inputRef.current` and call [`focus()`](https://developer.mozilla.org/docs/Web/API/HTMLElement/focus) on it with `inputRef.current.focus()`.
4.  Pass the `handleClick` event handler to `<button>` with `onClick`.

While DOM manipulation is the most common use case for refs, the `useRef` Hook can be used for storing other things outside React, like timer IDs. Similarly to state, refs remain between renders. Refs are like state variables that don’t trigger re-renders when you set them. Read about refs in [Referencing Values with Refs.](referencing-values-with-refs.md)

### Example: Scrolling to an element {/_example-scrolling-to-an-element_/}

You can have more than a single ref in a component. In this example, there is a carousel of three images. Each button centers an image by calling the browser [`scrollIntoView()`](https://developer.mozilla.org/docs/Web/API/Element/scrollIntoView) method on the corresponding DOM node:

<!-- 0011.part.md -->

```js
import { useRef } from 'react';

export default function CatFriends() {
    const firstCatRef = useRef(null);
    const secondCatRef = useRef(null);
    const thirdCatRef = useRef(null);

    function handleScrollToFirstCat() {
        firstCatRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'center',
        });
    }

    function handleScrollToSecondCat() {
        secondCatRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'center',
        });
    }

    function handleScrollToThirdCat() {
        thirdCatRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'center',
        });
    }

    return (
        <>
            <nav>
                <button onClick={handleScrollToFirstCat}>
                    Tom
                </button>
                <button onClick={handleScrollToSecondCat}>
                    Maru
                </button>
                <button onClick={handleScrollToThirdCat}>
                    Jellylorum
                </button>
            </nav>
            <div>
                <ul>
                    <li>
                        <img
                            src="https://placekitten.com/g/200/200"
                            alt="Tom"
                            ref={firstCatRef}
                        />
                    </li>
                    <li>
                        <img
                            src="https://placekitten.com/g/300/200"
                            alt="Maru"
                            ref={secondCatRef}
                        />
                    </li>
                    <li>
                        <img
                            src="https://placekitten.com/g/250/200"
                            alt="Jellylorum"
                            ref={thirdCatRef}
                        />
                    </li>
                </ul>
            </div>
        </>
    );
}
```

<!-- 0012.part.md -->

<!-- 0013.part.md -->

```css
div {
    width: 100%;
    overflow: hidden;
}

nav {
    text-align: center;
}

button {
    margin: 0.25rem;
}

ul,
li {
    list-style: none;
    white-space: nowrap;
}

li {
    display: inline;
    padding: 0.5rem;
}
```

<!-- 0014.part.md -->

#### Как управлять списком ссылок с помощью обратного вызова {/_how-to-manage-a-list-of-refs-using-a-ref-callback_/}

В приведенных выше примерах существует предопределенное количество ссылок. Однако иногда вам может понадобиться ссылка на каждый элемент списка, и вы не знаете, сколько их будет. Что-то вроде этого **не будет работать**:

<!-- 0015.part.md -->

```js
<ul>
    {items.map((item) => {
        // Doesn't work!
        const ref = useRef(null);
        return <li ref={ref} />;
    })}
</ul>
```

<!-- 0016.part.md -->

Это происходит потому, что **Крючки должны вызываться только на верхнем уровне вашего компонента.** Вы не можете вызвать `useRef` в цикле, в условии или внутри вызова `map()`.

Один из возможных способов обойти это - получить единственную ссылку на их родительский элемент, а затем использовать методы манипуляции DOM, такие как [`querySelectorAll`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll), чтобы "найти" отдельные дочерние узлы из него. Однако это хрупкий метод и может сломаться, если структура DOM изменится.

Другое решение - **передать функцию атрибуту `ref`.** Это называется [`ref` callback.](/reference/react-dom/components/common#ref-callback) React вызовет ваш ref callback с узлом DOM, когда придет время установить ref, и с `null`, когда придет время очистить его. Это позволяет вам вести свой собственный массив или [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map), и обращаться к любому ref по его индексу или какому-либо идентификатору.

В данном примере показано, как можно использовать этот подход для прокрутки к произвольному узлу в длинном списке:

<!-- 0017.part.md -->

```js
import { useRef } from 'react';

export default function CatFriends() {
    const itemsRef = useRef(null);

    function scrollToId(itemId) {
        const map = getMap();
        const node = map.get(itemId);
        node.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'center',
        });
    }

    function getMap() {
        if (!itemsRef.current) {
            // Initialize the Map on first usage.
            itemsRef.current = new Map();
        }
        return itemsRef.current;
    }

    return (
        <>
            <nav>
                <button onClick={() => scrollToId(0)}>
                    Tom
                </button>
                <button onClick={() => scrollToId(5)}>
                    Maru
                </button>
                <button onClick={() => scrollToId(9)}>
                    Jellylorum
                </button>
            </nav>
            <div>
                <ul>
                    {catList.map((cat) => (
                        <li
                            key={cat.id}
                            ref={(node) => {
                                const map = getMap();
                                if (node) {
                                    map.set(cat.id, node);
                                } else {
                                    map.delete(cat.id);
                                }
                            }}
                        >
                            <img
                                src={cat.imageUrl}
                                alt={'Cat #' + cat.id}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
}

const catList = [];
for (let i = 0; i < 10; i++) {
    catList.push({
        id: i,
        imageUrl:
            'https://placekitten.com/250/200?image=' + i,
    });
}
```

<!-- 0018.part.md -->

<!-- 0019.part.md -->

```css
div {
    width: 100%;
    overflow: hidden;
}

nav {
    text-align: center;
}

button {
    margin: 0.25rem;
}

ul,
li {
    list-style: none;
    white-space: nowrap;
}

li {
    display: inline;
    padding: 0.5rem;
}
```

<!-- 0020.part.md -->

В этом примере `itemsRef` не содержит ни одного узла DOM. Вместо этого он содержит [Map](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map) от ID элемента к узлу DOM. ([Ссылки могут содержать любые значения!](referencing-values-with-refs.md)) Обратный вызов `ref` для каждого элемента списка заботится об обновлении карты:

<!-- 0021.part.md -->

```js
<li
  key={cat.id}
  ref={node => {
    const map = getMap();
    if (node) {
      // Add to the Map
      map.set(cat.id, node);
    } else {
      // Remove from the Map
      map.delete(cat.id);
    }
  }}
>
```

<!-- 0022.part.md -->

This lets you read individual DOM nodes from the Map later.

## Accessing another component’s DOM nodes {/_accessing-another-components-dom-nodes_/}

When you put a ref on a built-in component that outputs a browser element like `<input />`, React will set that ref’s `current` property to the corresponding DOM node (such as the actual `<input />` in the browser).

However, if you try to put a ref on **your own** component, like `<MyInput />`, by default you will get `null`. Here is an example demonstrating it. Notice how clicking the button **does not** focus the input:

<!-- 0023.part.md -->

```js
import { useRef } from 'react';

function MyInput(props) {
    return <input {...props} />;
}

export default function MyForm() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <MyInput ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

<!-- 0024.part.md -->

Чтобы помочь вам заметить проблему, React также выводит ошибку в консоль:

Предупреждение: Компонентам функции нельзя давать ссылки. Попытки получить доступ к этой ссылке будут безуспешными. Вы хотели использовать React.forwardRef()?

Это происходит потому, что по умолчанию React не позволяет компоненту обращаться к узлам DOM других компонентов. Даже своим собственным детям\! Это намеренно. Ссылки - это аварийный люк, который следует использовать очень редко. Ручное манипулирование DOM-узлами _другого_ компонента делает ваш код еще более хрупким.

Вместо этого, компоненты, которые _хотят_ раскрыть свои узлы DOM, должны **оптировать** такое поведение. Компонент может указать, что он "переадресует" свою ссылку одному из своих дочерних компонентов. Вот как `MyInput` может использовать API `forwardRef`:

<!-- 0025.part.md -->

```js
const MyInput = forwardRef((props, ref) => {
    return <input {...props} ref={ref} />;
});
```

<!-- 0026.part.md -->

This is how it works:

1.  `<MyInput ref={inputRef} />` tells React to put the corresponding DOM node into `inputRef.current`. However, it’s up to the `MyInput` component to opt into that–by default, it doesn’t.
2.  The `MyInput` component is declared using `forwardRef`. **This opts it into receiving the `inputRef` from above as the second `ref` argument** which is declared after `props`.
3.  `MyInput` itself passes the `ref` it received to the `<input>` inside of it.

Now clicking the button to focus the input works:

<!-- 0027.part.md -->

```js
import { forwardRef, useRef } from 'react';

const MyInput = forwardRef((props, ref) => {
    return <input {...props} ref={ref} />;
});

export default function Form() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <MyInput ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

<!-- 0028.part.md -->

В системах проектирования обычным шаблоном для низкоуровневых компонентов, таких как кнопки, входы и т.д., является передача ссылок на их узлы DOM. С другой стороны, высокоуровневые компоненты, такие как формы, списки или разделы страницы, обычно не раскрывают свои узлы DOM, чтобы избежать случайных зависимостей от структуры DOM.

#### Раскрытие подмножества API с помощью императивного дескриптора {/_exposing-a-subset-of-the-api-with-an-imperative-handle_/}

В приведенном выше примере `MyInput` раскрывает исходный элемент ввода DOM. Это позволяет родительскому компоненту вызывать `focus()` на нем. Однако это также позволяет родительскому компоненту делать что-то еще - например, изменять стили CSS. В редких случаях вы можете захотеть ограничить открытую функциональность. Вы можете сделать это с помощью `useImperativeHandle`:

<!-- 0029.part.md -->

```js
import {
    forwardRef,
    useRef,
    useImperativeHandle,
} from 'react';

const MyInput = forwardRef((props, ref) => {
    const realInputRef = useRef(null);
    useImperativeHandle(ref, () => ({
        // Only expose focus and nothing else
        focus() {
            realInputRef.current.focus();
        },
    }));
    return <input {...props} ref={realInputRef} />;
});

export default function Form() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <MyInput ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

<!-- 0030.part.md -->

Здесь `realInputRef` внутри `MyInput` содержит фактический входной DOM-узел. Однако `useImperativeHandle` инструктирует React предоставлять ваш собственный специальный объект в качестве значения ссылки на родительский компонент. Таким образом, `inputRef.current` внутри компонента `Form` будет иметь только метод `focus`. В этом случае ref "handle" - это не узел DOM, а пользовательский объект, который вы создаете внутри вызова `useImperativeHandle`.

## Когда React присоединяет ссылки {/_when-react-attaches-the-refs_/}

В React каждое обновление делится на [две фазы](render-and-commit.md):

-   Во время **render,** React вызывает ваши компоненты, чтобы выяснить, что должно быть на экране.
-   Во время **commit,** React применяет изменения в DOM.

В общем, вы [не хотите](referencing-values-with-refs.md) обращаться к рефкам во время рендеринга. Это относится и к ссылкам, содержащим узлы DOM. Во время первого рендеринга узлы DOM еще не были созданы, поэтому `ref.current` будет `null`. А во время рендеринга обновлений, узлы DOM еще не были обновлены. Поэтому читать их еще рано.

React устанавливает `ref.current` во время фиксации. Перед обновлением DOM, React устанавливает затронутые значения `ref.current` в `null`. После обновления DOM, React немедленно устанавливает их в соответствующие узлы DOM.

**Обычно вы обращаетесь к рефкам из обработчиков событий.** Если вы хотите что-то сделать с рефкой, но нет конкретного события, в котором это можно сделать, вам может понадобиться эффект. Мы обсудим эффекты на следующих страницах.

#### Промывка обновлений состояния синхронно с помощью flushSync {/_flush-state-updates-synchronously-with-flush-sync_/}

Рассмотрим код, подобный этому, который добавляет новый todo и прокручивает экран вниз до последнего дочернего элемента списка. Обратите внимание, что по какой-то причине он всегда прокручивается к тому todo, который был _прямо перед_ последним добавленным:

<!-- 0031.part.md -->

```js
import { useState, useRef } from 'react';

export default function TodoList() {
    const listRef = useRef(null);
    const [text, setText] = useState('');
    const [todos, setTodos] = useState(initialTodos);

    function handleAdd() {
        const newTodo = { id: nextId++, text: text };
        setText('');
        setTodos([...todos, newTodo]);
        listRef.current.lastChild.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
        });
    }

    return (
        <>
            <button onClick={handleAdd}>Add</button>
            <input
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            <ul ref={listRef}>
                {todos.map((todo) => (
                    <li key={todo.id}>{todo.text}</li>
                ))}
            </ul>
        </>
    );
}

let nextId = 0;
let initialTodos = [];
for (let i = 0; i < 20; i++) {
    initialTodos.push({
        id: nextId++,
        text: 'Todo #' + (i + 1),
    });
}
```

<!-- 0032.part.md -->

Проблема заключается в этих двух линиях:

<!-- 0033.part.md -->

```js
setTodos([...todos, newTodo]);
listRef.current.lastChild.scrollIntoView();
```

<!-- 0034.part.md -->

В React [обновления состояния ставятся в очередь](queueing-a-series-of-state-updates.md). Обычно это то, что вам нужно. Однако здесь это вызывает проблему, потому что `setTodos` не обновляет DOM немедленно. Поэтому, когда вы прокручиваете список до последнего элемента, todo еще не был добавлен. Поэтому прокрутка всегда "отстает" на один элемент.

Чтобы решить эту проблему, вы можете заставить React обновлять ("промывать") DOM синхронно. Для этого импортируйте `flushSync` из `react-dom` и **оберните обновление состояния** в вызов `flushSync`:

<!-- 0035.part.md -->

```js
flushSync(() => {
    setTodos([...todos, newTodo]);
});
listRef.current.lastChild.scrollIntoView();
```

<!-- 0036.part.md -->

Это даст команду React синхронно обновить DOM сразу после выполнения кода, обернутого в `flushSync`. В результате, последний todo уже будет в DOM к тому моменту, когда вы попытаетесь перейти к нему:

<!-- 0037.part.md -->

```js
import { useState, useRef } from 'react';
import { flushSync } from 'react-dom';

export default function TodoList() {
    const listRef = useRef(null);
    const [text, setText] = useState('');
    const [todos, setTodos] = useState(initialTodos);

    function handleAdd() {
        const newTodo = { id: nextId++, text: text };
        flushSync(() => {
            setText('');
            setTodos([...todos, newTodo]);
        });
        listRef.current.lastChild.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
        });
    }

    return (
        <>
            <button onClick={handleAdd}>Add</button>
            <input
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            <ul ref={listRef}>
                {todos.map((todo) => (
                    <li key={todo.id}>{todo.text}</li>
                ))}
            </ul>
        </>
    );
}

let nextId = 0;
let initialTodos = [];
for (let i = 0; i < 20; i++) {
    initialTodos.push({
        id: nextId++,
        text: 'Todo #' + (i + 1),
    });
}
```

<!-- 0038.part.md -->

## Лучшие практики работы с DOM с помощью ссылок {/_best-practices-for-dom-manipulation-with-refs_/}

Ссылки - это аварийный люк. Вы должны использовать их только тогда, когда вам нужно "выйти за пределы React". Обычные примеры этого - управление фокусом, позицией прокрутки или вызов API браузера, которые React не раскрывает.

Если вы придерживаетесь неразрушающих действий, таких как фокусировка и прокрутка, вы не должны столкнуться с какими-либо проблемами. Однако, если вы попытаетесь **изменить** DOM вручную, вы рискуете вступить в конфликт с изменениями, которые вносит React.

Чтобы проиллюстрировать эту проблему, данный пример включает в себя приветственное сообщение и две кнопки. Первая кнопка переключает свое присутствие, используя [conditional rendering](conditional-rendering.md) и [state](state-a-components-memory.md), как вы обычно делаете в React. Вторая кнопка использует [`remove()` DOM API](https://developer.mozilla.org/docs/Web/API/Element/remove), чтобы принудительно удалить ее из DOM вне контроля React.

Попробуйте нажать "Toggle with setState" несколько раз. Сообщение должно исчезнуть и появиться снова. Затем нажмите "Удалить из DOM". Это приведет к принудительному удалению. Наконец, нажмите "Toggle with setState":

<!-- 0039.part.md -->

```js
import { useState, useRef } from 'react';

export default function Counter() {
    const [show, setShow] = useState(true);
    const ref = useRef(null);

    return (
        <div>
            <button
                onClick={() => {
                    setShow(!show);
                }}
            >
                Toggle with setState
            </button>
            <button
                onClick={() => {
                    ref.current.remove();
                }}
            >
                Remove from the DOM
            </button>
            {show && <p ref={ref}>Hello world</p>}
        </div>
    );
}
```

<!-- 0040.part.md -->

<!-- 0041.part.md -->

```css
p,
button {
    display: block;
    margin: 10px;
}
```

<!-- 0042.part.md -->

After you’ve manually removed the DOM element, trying to use `setState` to show it again will lead to a crash. This is because you’ve changed the DOM, and React doesn’t know how to continue managing it correctly.

**Avoid changing DOM nodes managed by React.** Modifying, adding children to, or removing children from elements that are managed by React can lead to inconsistent visual results or crashes like above.

However, this doesn’t mean that you can’t do it at all. It requires caution. **You can safely modify parts of the DOM that React has _no reason_ to update.** For example, if some `<div>` is always empty in the JSX, React won’t have a reason to touch its children list. Therefore, it is safe to manually add or remove elements there.

\<Recap\>

-   Refs are a generic concept, but most often you’ll use them to hold DOM elements.
-   You instruct React to put a DOM node into `myRef.current` by passing `<div ref={myRef}>`.
-   Usually, you will use refs for non-destructive actions like focusing, scrolling, or measuring DOM elements.
-   A component doesn’t expose its DOM nodes by default. You can opt into exposing a DOM node by using `forwardRef` and passing the second `ref` argument down to a specific node.
-   Avoid changing DOM nodes managed by React.
-   Если вы изменяете узлы DOM, управляемые React, изменяйте те части, которые React не имеет причин обновлять.

\</Recap\>

\<Проблемы\>

#### Воспроизведение и пауза видео {/_play-and-pause-the-video_/}

В этом примере кнопка переключает переменную состояния для перехода между воспроизведением и паузой. Однако для того, чтобы действительно воспроизвести или поставить видео на паузу, переключения состояния недостаточно. Вам также необходимо вызвать [`play()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play) и [`pause()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/pause) на элементе DOM для `<video>`. Добавьте к нему ссылку и заставьте кнопку работать.

<!-- 0043.part.md -->

```js
import { useState, useRef } from 'react';

export default function VideoPlayer() {
    const [isPlaying, setIsPlaying] = useState(false);

    function handleClick() {
        const nextIsPlaying = !isPlaying;
        setIsPlaying(nextIsPlaying);
    }

    return (
        <>
            <button onClick={handleClick}>
                {isPlaying ? 'Pause' : 'Play'}
            </button>
            <video width="250">
                <source
                    src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
                    type="video/mp4"
                />
            </video>
        </>
    );
}
```

<!-- 0044.part.md -->

<!-- 0045.part.md -->

```css
button {
    display: block;
    margin-bottom: 20px;
}
```

<!-- 0046.part.md -->

Для решения дополнительной задачи синхронизируйте кнопку "Play" с тем, воспроизводится ли видео, даже если пользователь щелкает правой кнопкой мыши на видео и воспроизводит его с помощью встроенных элементов управления мультимедиа браузера. Для этого вам может понадобиться прослушать `onPlay` и `onPause` на видео.

\<Решение\>

Объявите ссылку и поместите ее на элемент `<video>`. Затем вызовите `ref.current.play()` и `ref.current.pause()` в обработчике событий в зависимости от следующего состояния.

<!-- 0047.part.md -->

```js
import { useState, useRef } from 'react';

export default function VideoPlayer() {
    const [isPlaying, setIsPlaying] = useState(false);
    const ref = useRef(null);

    function handleClick() {
        const nextIsPlaying = !isPlaying;
        setIsPlaying(nextIsPlaying);

        if (nextIsPlaying) {
            ref.current.play();
        } else {
            ref.current.pause();
        }
    }

    return (
        <>
            <button onClick={handleClick}>
                {isPlaying ? 'Pause' : 'Play'}
            </button>
            <video
                width="250"
                ref={ref}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
            >
                <source
                    src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
                    type="video/mp4"
                />
            </video>
        </>
    );
}
```

<!-- 0048.part.md -->

<!-- 0049.part.md -->

```css
button {
    display: block;
    margin-bottom: 20px;
}
```

<!-- 0050.part.md -->

Для работы со встроенными элементами управления браузера вы можете добавить обработчики `onPlay` и `onPause` к элементу `<video>` и вызвать из них `setIsPlaying`. Таким образом, если пользователь воспроизводит видео с помощью элементов управления браузера, состояние будет соответствующим образом изменено.

\</Solution\>

#### Фокусировка поля поиска {/_focus-the-search-field_/}

Сделайте так, чтобы нажатие на кнопку "Поиск" наводило фокус на поле.

<!-- 0051.part.md -->

```js
export default function Page() {
    return (
        <>
            <nav>
                <button>Search</button>
            </nav>
            <input placeholder="Looking for something?" />
        </>
    );
}
```

<!-- 0052.part.md -->

<!-- 0053.part.md -->

```css
button {
    display: block;
    margin-bottom: 10px;
}
```

<!-- 0054.part.md -->

\<Решение\>

Добавьте ссылку на вход и вызовите `focus()` на узле DOM, чтобы сфокусировать его:

<!-- 0055.part.md -->

```js
import { useRef } from 'react';

export default function Page() {
    const inputRef = useRef(null);
    return (
        <>
            <nav>
                <button
                    onClick={() => {
                        inputRef.current.focus();
                    }}
                >
                    Search
                </button>
            </nav>
            <input
                ref={inputRef}
                placeholder="Looking for something?"
            />
        </>
    );
}
```

<!-- 0056.part.md -->

<!-- 0057.part.md -->

```css
button {
    display: block;
    margin-bottom: 10px;
}
```

<!-- 0058.part.md -->

\</Solution\>

#### Прокрутка карусели изображений {/_scrolling-an-image-carousel_/}

Эта карусель изображений имеет кнопку "Next", которая переключает активное изображение. Заставьте галерею прокручиваться горизонтально до активного изображения по щелчку. Для этого нужно вызвать [`scrollIntoView()`](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView) на DOM-узле активного изображения:

<!-- 0059.part.md -->

```js
node.scrollIntoView({
    behavior: 'smooth',
    block: 'nearest',
    inline: 'center',
});
```

<!-- 0060.part.md -->

\< Подсказка\>

Для этого упражнения не обязательно иметь ссылку на каждое изображение. Достаточно иметь ссылку на текущее активное изображение или на сам список. Используйте `flushSync` для обеспечения обновления DOM _до_ прокрутки.

\</Hint\>

<!-- 0061.part.md -->

```js
import { useState } from 'react';

export default function CatFriends() {
    const [index, setIndex] = useState(0);
    return (
        <>
            <nav>
                <button
                    onClick={() => {
                        if (index < catList.length - 1) {
                            setIndex(index + 1);
                        } else {
                            setIndex(0);
                        }
                    }}
                >
                    Next
                </button>
            </nav>
            <div>
                <ul>
                    {catList.map((cat, i) => (
                        <li key={cat.id}>
                            <img
                                className={
                                    index === i
                                        ? 'active'
                                        : ''
                                }
                                src={cat.imageUrl}
                                alt={'Cat #' + cat.id}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
}

const catList = [];
for (let i = 0; i < 10; i++) {
    catList.push({
        id: i,
        imageUrl:
            'https://placekitten.com/250/200?image=' + i,
    });
}
```

<!-- 0062.part.md -->

<!-- 0063.part.md -->

```css
div {
    width: 100%;
    overflow: hidden;
}

nav {
    text-align: center;
}

button {
    margin: 0.25rem;
}

ul,
li {
    list-style: none;
    white-space: nowrap;
}

li {
    display: inline;
    padding: 0.5rem;
}

img {
    padding: 10px;
    margin: -10px;
    transition: background 0.2s linear;
}

.active {
    background: rgba(0, 100, 150, 0.4);
}
```

<!-- 0064.part.md -->

\<Решение\>

Вы можете объявить `selectedRef`, а затем передать его условно только текущему изображению:

<!-- 0065.part.md -->

```js
<li ref={index === i ? selectedRef : null}>
```

<!-- 0066.part.md -->

Когда `index === i`, что означает, что изображение является выбранным, `<li>` получит `selectedRef`. React будет следить за тем, чтобы `selectedRef.current` всегда указывал на правильный узел DOM.

Обратите внимание, что вызов `flushSync` необходим для того, чтобы заставить React обновить DOM перед прокруткой. В противном случае `selectedRef.current` всегда будет указывать на ранее выбранный элемент.

<!-- 0067.part.md -->

```js
import { useRef, useState } from 'react';
import { flushSync } from 'react-dom';

export default function CatFriends() {
    const selectedRef = useRef(null);
    const [index, setIndex] = useState(0);

    return (
        <>
            <nav>
                <button
                    onClick={() => {
                        flushSync(() => {
                            if (
                                index <
                                catList.length - 1
                            ) {
                                setIndex(index + 1);
                            } else {
                                setIndex(0);
                            }
                        });
                        selectedRef.current.scrollIntoView({
                            behavior: 'smooth',
                            block: 'nearest',
                            inline: 'center',
                        });
                    }}
                >
                    Next
                </button>
            </nav>
            <div>
                <ul>
                    {catList.map((cat, i) => (
                        <li
                            key={cat.id}
                            ref={
                                index === i
                                    ? selectedRef
                                    : null
                            }
                        >
                            <img
                                className={
                                    index === i
                                        ? 'active'
                                        : ''
                                }
                                src={cat.imageUrl}
                                alt={'Cat #' + cat.id}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
}

const catList = [];
for (let i = 0; i < 10; i++) {
    catList.push({
        id: i,
        imageUrl:
            'https://placekitten.com/250/200?image=' + i,
    });
}
```

<!-- 0068.part.md -->

<!-- 0069.part.md -->

```css
div {
    width: 100%;
    overflow: hidden;
}

nav {
    text-align: center;
}

button {
    margin: 0.25rem;
}

ul,
li {
    list-style: none;
    white-space: nowrap;
}

li {
    display: inline;
    padding: 0.5rem;
}

img {
    padding: 10px;
    margin: -10px;
    transition: background 0.2s linear;
}

.active {
    background: rgba(0, 100, 150, 0.4);
}
```

<!-- 0070.part.md -->

\</Solution\>

#### Фокусировка поля поиска с помощью отдельных компонентов {/_focus-the-search-field-with-separate-components_/}

Сделайте так, чтобы нажатие на кнопку "Поиск" наводило фокус на поле. Обратите внимание, что каждый компонент определен в отдельном файле и не должен быть перемещен из него. Как соединить их вместе?

\<Hint\>

Вам понадобится `forwardRef`, чтобы открыть узел DOM из вашего собственного компонента, такого как `SearchInput`.

\</Hint\>

<!-- 0071.part.md -->

```js
import SearchButton from './SearchButton.js';
import SearchInput from './SearchInput.js';

export default function Page() {
    return (
        <>
            <nav>
                <SearchButton />
            </nav>
            <SearchInput />
        </>
    );
}
```

<!-- 0072.part.md -->

<!-- 0073.part.md -->

```js
export default function SearchButton() {
    return <button>Search</button>;
}
```

<!-- 0074.part.md -->

<!-- 0075.part.md -->

```js
export default function SearchInput() {
    return <input placeholder="Looking for something?" />;
}
```

<!-- 0076.part.md -->

<!-- 0077.part.md -->

```css
button {
    display: block;
    margin-bottom: 10px;
}
```

<!-- 0078.part.md -->

\<Solution\>

You’ll need to add an `onClick` prop to the `SearchButton`, and make the `SearchButton` pass it down to the browser `<button>`. You’ll also pass a ref down to `<SearchInput>`, which will forward it to the real `<input>` and populate it. Finally, in the click handler, you’ll call `focus` on the DOM node stored inside that ref.

<!-- 0079.part.md -->

```js
import { useRef } from 'react';
import SearchButton from './SearchButton.js';
import SearchInput from './SearchInput.js';

export default function Page() {
    const inputRef = useRef(null);
    return (
        <>
            <nav>
                <SearchButton
                    onClick={() => {
                        inputRef.current.focus();
                    }}
                />
            </nav>
            <SearchInput ref={inputRef} />
        </>
    );
}
```

<!-- 0080.part.md -->

<!-- 0081.part.md -->

```js
export default function SearchButton({ onClick }) {
    return <button onClick={onClick}>Search</button>;
}
```

<!-- 0082.part.md -->

<!-- 0083.part.md -->

```js
import { forwardRef } from 'react';

export default forwardRef(function SearchInput(props, ref) {
    return (
        <input
            ref={ref}
            placeholder="Looking for something?"
        />
    );
});
```

<!-- 0084.part.md -->

<!-- 0085.part.md -->

```css
button {
    display: block;
    margin-bottom: 10px;
}
```

<!-- 0086.part.md -->

\</Solution\>

\</Challenges\>

<!-- 0087.part.md -->
