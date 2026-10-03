---
description: Fragment позволяет группировать элементы без узла-обертки
---

# Fragment

<big>`<Fragment>`, часто используемый через синтаксис <code><>...&lt;/&gt;</code>, позволяет группировать элементы без узла-обертки.</big>

```js
<>
    <OneChild />
    <AnotherChild />
</>
```

## Описание {#reference}

### `<Fragment>` {#fragment}

Оберните элементы в `<Fragment>`, чтобы сгруппировать их вместе в ситуациях, когда вам нужен один элемент. Группировка элементов в `Fragment` не влияет на результирующий DOM; он такой же, как если бы элементы не были сгруппированы. Пустой JSX-тег <code>&lt;>&lt;/&gt;</code> в большинстве случаев является сокращением для `<Fragment></Fragment>`.

#### Параметры {#props}

-   **опционально** `key`: Фрагменты, объявленные с явным синтаксисом `<Fragment>`, могут иметь [ключи](../../learn/rendering-lists.md).

#### Предупреждения {#caveats}

-   Если вы хотите передать `key` фрагменту, вы не можете использовать синтаксис <code>&lt;>...&lt;/&gt;</code>. Вы должны явно импортировать `Fragment` из `'react'` и передать `<Fragment key={yourKey}>...</Fragment>`.

-   React не [сбрасывает состояние](../../learn/preserving-and-resetting-state.md), когда вы переходите от рендеринга <code>&lt;>&lt;Child /&gt;&lt;/&gt;</code> к `[<Child />]` или обратно, или когда вы переходите от рендеринга <code>&lt;>&lt;Child /&gt;&lt;/&gt;</code> к `<Child />` и обратно. Это работает только на одном уровне в глубину: например, переход от <code>&lt;>&lt;>&lt;Child /&gt;&lt;/&gt;&lt;/&gt;</code> к `<Child />` сбрасывает состояние. Точную семантику можно посмотреть [здесь](https://gist.github.com/clemmy/b3ef00f9507909429d8aa0d3ee4f986b).

### `FragmentInstance` {#fragmentinstance}

Когда во фрагмент передают `ref`, React даёт объект `FragmentInstance`. У него есть методы для работы с DOM-потомками первого уровня, которые обёрнуты фрагментом.

* [`addEventListener`](#addeventlistener) и [`removeEventListener`](#removeeventlistener) управляют слушателями событий на всех DOM-потомках первого уровня.
* [`dispatchEvent`](#dispatchevent) отправляет событие на фрагменте, и оно может всплыть к родительскому DOM-узлу.
* [`focus`](#focus), [`focusLast`](#focuslast) и [`blur`](#blur) управляют фокусом по всем вложенным потомкам в порядке обхода в глубину.
* [`observeUsing`](#observeusing) и [`unobserveUsing`](#unobserveusing) подключают и отключают экземпляры `IntersectionObserver` или `ResizeObserver`.
* [`getClientRects`](#getclientrects) возвращает ограничивающие прямоугольники всех DOM-потомков первого уровня.
* [`getRootNode`](#getrootnode) возвращает корневой узел родителя фрагмента.
* [`compareDocumentPosition`](#comparedocumentposition) сравнивает позицию фрагмента с другим узлом.
* [`scrollIntoView`](#scrollintoview) прокручивает потомков фрагмента в область видимости.

#### `addEventListener(type, listener, options?)` {#addeventlistener}

Добавляет слушатель события ко всем DOM-потомкам фрагмента первого уровня.

```js
fragmentRef.current.addEventListener('click', handleClick);
```

##### Параметры {#addeventlistener-parameters}

* `type`: строка с типом события (например, `'click'`, `'focus'`).
* `listener`: функция-обработчик события.
* **необязательно** `options`: объект параметров или булево значение для захвата, как в [DOM API `addEventListener`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener).

##### Возвращаемое значение {#addeventlistener-returns}

`addEventListener` ничего не возвращает (`undefined`).

#### `removeEventListener(type, listener, options?)` {#removeeventlistener}

Удаляет слушатель события со всех DOM-потомков фрагмента первого уровня.

```js
fragmentRef.current.removeEventListener('click', handleClick);
```

##### Параметры {#removeeventlistener-parameters}

* `type`: строка с типом события.
* `listener`: функция-обработчик, которую нужно удалить.
* **необязательно** `options`: объект параметров или булево значение, как в [DOM API `removeEventListener`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener).

##### Возвращаемое значение {#removeeventlistener-returns}

`removeEventListener` ничего не возвращает (`undefined`).

#### `dispatchEvent(event)` {#dispatchevent}

Отправляет событие на фрагменте. Вызываются добавленные слушатели, и событие может всплыть к родительскому DOM-узлу фрагмента.

```js
fragmentRef.current.dispatchEvent(new Event('custom', { bubbles: true }));
```

##### Параметры {#dispatchevent-parameters}

* `event`: объект [`Event`](https://developer.mozilla.org/en-US/docs/Web/API/Event), который нужно отправить. Если `bubbles` равен `true`, событие всплывает к родительскому DOM-узлу фрагмента.

##### Возвращаемое значение {#dispatchevent-returns}

`true`, если событие не отменено, и `false`, если вызван `preventDefault()`.

#### `focus(options?)` {#focus}

Переводит фокус на первый фокусируемый DOM-узел внутри фрагмента. В отличие от `element.focus()` на DOM-элементе, этот метод ищет *всех* вложенных потомков в глубину, пока не найдёт фокусируемый элемент, а не только сам элемент или его прямых потомков.

```js
fragmentRef.current.focus();
```

##### Параметры {#focus-parameters}

* **необязательно** `options`: объект [`FocusOptions`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus#options) (например, `{ preventScroll: true }`).

##### Возвращаемое значение {#focus-returns}

`focus` ничего не возвращает (`undefined`).

#### `focusLast(options?)` {#focuslast}

Переводит фокус на последний фокусируемый DOM-узел внутри фрагмента. Ищет вложенных потомков в глубину, а затем идёт в обратном порядке.

```js
fragmentRef.current.focusLast();
```

##### Параметры {#focuslast-parameters}

* **необязательно** `options`: объект [`FocusOptions`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus#options).

##### Возвращаемое значение {#focuslast-returns}

`focusLast` ничего не возвращает (`undefined`).

#### `blur()` {#blur}

Снимает фокус с активного элемента, если он находится внутри фрагмента. Если `document.activeElement` не внутри фрагмента, `blur` ничего не делает.

```js
fragmentRef.current.blur();
```

##### Возвращаемое значение {#blur-returns}

`blur` ничего не возвращает (`undefined`).

#### `observeUsing(observer)` {#observeusing}

Начинает наблюдение за всеми DOM-потомками фрагмента первого уровня переданным наблюдателем.

```js
const observer = new IntersectionObserver(callback, options);
fragmentRef.current.observeUsing(observer);
```

##### Параметры {#observeusing-parameters}

* `observer`: экземпляр [`IntersectionObserver`](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver) или [`ResizeObserver`](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver).

##### Возвращаемое значение {#observeusing-returns}

`observeUsing` ничего не возвращает (`undefined`).

#### `unobserveUsing(observer)` {#unobserveusing}

Прекращает наблюдение за DOM-потомками фрагмента указанным наблюдателем.

```js
fragmentRef.current.unobserveUsing(observer);
```

##### Параметры {#unobserveusing-parameters}

* `observer`: тот же экземпляр `IntersectionObserver` или `ResizeObserver`, который раньше передали в [`observeUsing`](#observeusing).

##### Возвращаемое значение {#unobserveusing-returns}

`unobserveUsing` ничего не возвращает (`undefined`).

#### `getClientRects()` {#getclientrects}

Возвращает плоский массив объектов [`DOMRect`](https://developer.mozilla.org/en-US/docs/Web/API/DOMRect) с ограничивающими прямоугольниками всех DOM-потомков первого уровня.

```js
const rects = fragmentRef.current.getClientRects();
```

##### Возвращаемое значение {#getclientrects-returns}

`Array<DOMRect>` с ограничивающими прямоугольниками всех потомков.

#### `getRootNode(options?)` {#getrootnode}

Возвращает корневой узел, в котором находится родительский DOM-узел фрагмента, как [`Node.getRootNode()`](https://developer.mozilla.org/en-US/docs/Web/API/Node/getRootNode).

```js
const root = fragmentRef.current.getRootNode();
```

##### Параметры {#getrootnode-parameters}

* **необязательно** `options`: объект с булевым свойством `composed`, как в [DOM API `getRootNode`](https://developer.mozilla.org/en-US/docs/Web/API/Node/getRootNode#options).

##### Возвращаемое значение {#getrootnode-returns}

`Document`, `ShadowRoot` или сам `FragmentInstance`, если родительского DOM-узла нет.

#### `compareDocumentPosition(otherNode)` {#comparedocumentposition}

Сравнивает позицию фрагмента в документе с другим узлом и возвращает битовую маску, как [`Node.compareDocumentPosition()`](https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition).

```js
const position = fragmentRef.current.compareDocumentPosition(otherElement);
```

##### Параметры {#comparedocumentposition-parameters}

* `otherNode`: DOM-узел, с которым нужно сравнить.

##### Возвращаемое значение {#comparedocumentposition-returns}

Битовая маска [флагов позиции](https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition#return_value). Пустые фрагменты и фрагменты, чьи потомки отрендерены через [портал](../react-dom/createPortal.md), включают в результат `Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC`.

#### `scrollIntoView(alignToTop?)` {#scrollintoview}

Прокручивает потомков фрагмента в область видимости. Если `alignToTop` равен `true` или опущен, прокрутка выравнивает первого потомка по верху прокручиваемого предка. Если `alignToTop` равен `false`, прокрутка выравнивает последнего потомка по низу.

```js
fragmentRef.current.scrollIntoView();
```

##### Параметры {#scrollintoview-parameters}

* **необязательно** `alignToTop`: булево значение. Если `true` (по умолчанию), первый потомок прокручивается к верху прокручиваемой области. Если `false`, последний потомок прокручивается к низу. В отличие от [`Element.scrollIntoView()`](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView), этот метод не принимает объект `ScrollIntoViewOptions`.

##### Возвращаемое значение {#scrollintoview-returns}

`scrollIntoView` ничего не возвращает (`undefined`).

##### Предупреждения {#scrollintoview-caveats}

* `scrollIntoView` не принимает объект параметров. Если его передать, будет ошибка. Используйте булево значение `alignToTop`.
* Если у фрагмента нет потомков, `scrollIntoView` в качестве фолбэка прокручивает в область видимости ближайшего соседа или родителя.

#### Предупреждения `FragmentInstance` {#fragmentinstance-caveats}

* Методы, которые работают с потомками (`addEventListener`, `observeUsing`, `getClientRects`), действуют на *хост-потомков (DOM) первого уровня* фрагмента. Они не нацелены напрямую на потомков, вложенных в другой DOM-элемент.
* `focus` и `focusLast` ищут фокусируемые элементы среди вложенных потомков в глубину, в отличие от методов событий и наблюдателей, которые затрагивают только хост-потомков первого уровня.
* `observeUsing` не работает с текстовыми узлами. В разработке React пишет предупреждение, если фрагмент содержит только текстовых потомков.
* React не вешает слушатели, добавленные через `addEventListener`, на скрытые деревья [`<Activity>`](Activity.md). Когда граница `Activity` переключается со скрытой на видимую, слушатели применяются автоматически.
* Каждый DOM-потомок первого уровня фрагмента с `ref` получает свойство `reactFragments` — `Set<FragmentInstance>` со всеми экземплярами фрагмента, которым принадлежит элемент. Это позволяет [кэшировать общий наблюдатель](#caching-global-intersection-observer) для нескольких фрагментов.

## Использование {#usage}

### Возвращение нескольких элементов {#returning-multiple-elements}

Используйте `Fragment` или эквивалентный синтаксис <code>&lt;>...&lt;/&gt;</code> для группировки нескольких элементов вместе. С его помощью вы можете поместить несколько элементов в любое место, где может находиться один элемент. Например, компонент может вернуть только один элемент, но с помощью фрагмента вы можете сгруппировать несколько элементов вместе и затем вернуть их как группу:

```js hl_lines="3 6"
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

=== "App.js"

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dkf6wt?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Как написать фрагмент без специального синтаксиса?"

    Приведенный выше пример эквивалентен импорту `Fragment` из React:

    ```js hl_lines="1 5 8"
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

### Присвоение переменной нескольких элементов {#assigning-multiple-elements-to-a-variable}

Как и любой другой элемент, вы можете присваивать элементы Fragment переменным, передавать их в качестве пропсов и так далее:

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

### Группировка элементов с помощью текста {#grouping-elements-with-text}

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

### Рендеринг списка фрагментов {#rendering-a-list-of-fragments}

Вот ситуация, когда вам нужно написать `Fragment` явно вместо использования синтаксиса <code><>&lt;/&gt;</code>. Когда вы [рендерите несколько элементов в цикле](../../learn/rendering-lists.md), вам нужно назначить `key` каждому элементу. Если элементы в цикле являются фрагментами, то для указания атрибута `key` необходимо использовать обычный синтаксис JSX-элементов:

```js hl_lines="3 6"
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

=== "App.js"

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5wvtmh?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Слушатели событий без элемента-обёртки {#adding-event-listeners-without-wrapper}

Рефы фрагмента позволяют добавить слушатели событий к группе элементов, не добавляя DOM-узел-обёртку. Чтобы подключить и очистить слушатели, используйте [ref-колбэк](../react-dom/components/common.md#ref-callback):

=== "js"

    ```js

    import { Fragment, useState, useRef, useEffect } from 'react';

    function ClickableFragment({ children, onClick }) {
        const fragmentRef = useRef(null);
        useEffect(() => {
            const fragmentInstance = fragmentRef.current;
            if (fragmentInstance === null) {
                return;
            }
            fragmentInstance.addEventListener('click', onClick);
            return () => {
                fragmentInstance.removeEventListener(
                    'click',
                    onClick
                );
            };
        }, [onClick])
        return (
            <Fragment ref={fragmentRef}>
                {children}
            </Fragment>
        );
    }

    export default function App() {
        const [clicks, setClicks] = useState(0);

        return (
            <>
                <p>Total clicks: {clicks}</p>
                <ClickableFragment onClick={() => {
                    setClicks(c => c + 1);
                }}>
                    <button>Button A</button>
                    <button>Button B</button>
                    <button>Button C</button>
                </ClickableFragment>
            </>
        );
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

Вызов `addEventListener` вешает слушатель на каждого DOM-потомка фрагмента первого уровня. Когда потомков динамически добавляют или удаляют, `FragmentInstance` сам добавляет или снимает слушатель.

??? note "Каких потомков затрагивает реф фрагмента?"

    `FragmentInstance` нацелен на **хост-потомков (DOM) первого уровня** фрагмента. Рассмотрим такое дерево:

    ```js
    <Fragment ref={ref}>
      <div id="A" />
      <Wrapper>
        <div id="B">
          <div id="C" />
        </div>
      </Wrapper>
      <div id="D" />
    </Fragment>
    ```

    `Wrapper` — это компонент React, поэтому `FragmentInstance` смотрит сквозь него в поисках DOM-узлов. Целевые потомки — `A`, `B` и `D`. `C` не входит в них, потому что вложен в DOM-элемент `B`.

    Методы вроде `addEventListener`, `observeUsing` и `getClientRects` работают с этими DOM-потомками первого уровня. `focus` и `focusLast` устроены иначе: они ищут *всех* вложенных потомков в глубину, чтобы найти фокусируемые элементы.

### Фокус на группе элементов {#managing-focus-across-elements}

Рефы фрагмента дают методы `focus`, `focusLast` и `blur`, которые работают со всеми DOM-узлами внутри фрагмента:

=== "js"

    ```js

    import { Fragment, useRef } from 'react';

    function FormFields({ children }) {
        const fragmentRef = useRef(null);

        return (
            <>
                <div className="buttons">
                    <button onClick={() => {
                        fragmentRef.current.focus();
                    }}>
                        Focus first
                    </button>
                    <button onClick={() => {
                        fragmentRef.current.focusLast();
                    }}>
                        Focus last
                    </button>
                    <button onClick={() => {
                        fragmentRef.current.blur();
                    }}>
                        Blur
                    </button>
                </div>
                <Fragment ref={fragmentRef}>
                    {children}
                </Fragment>
            </>
        );
    }

    // Even though the inputs are deeply nested,
    // focus() searches depth-first to find them.
    export default function App() {
        return (
            <FormFields>
                <fieldset>
                    <legend>Shipping</legend>
                    <label>
                        Street: <input name="street" />
                    </label>
                    <label>
                        City: <input name="city" />
                    </label>
                </fieldset>
            </FormFields>
        );
    }
    ```

=== "styles.css"

    ```css

    .buttons {
      display: flex;
      gap: 8px;
      margin-bottom: 10px;
    }

    label {
      display: inline-block;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

Вызов `focus()` фокусирует поле `street`, хотя оно вложено в `<fieldset>` и `<label>`. `focus()` ищет в глубину всех вложенных потомков, а не только прямых потомков фрагмента. `focusLast()` делает то же самое в обратном порядке, а `blur()` снимает фокус, если сейчас сфокусирован элемент внутри фрагмента.

### Прокрутка группы элементов в область видимости {#scrolling-group-into-view}

`scrollIntoView` прокручивает потомков фрагмента в область видимости без элемента-обёртки. Передайте `true` (или опустите аргумент), чтобы прокрутить первого потомка к верху. Передайте `false`, чтобы прокрутить последнего потомка к низу:

=== "js"

    ```js

    import { Fragment, useRef } from 'react';

    function ScrollableSection({ children }) {
        const fragmentRef = useRef(null);

        return (
            <>
                <div className="buttons">
                    <button onClick={() => {
                        fragmentRef.current.scrollIntoView();
                    }}>
                        Scroll to top
                    </button>
                    <button onClick={() => {
                        fragmentRef.current.scrollIntoView(false);
                    }}>
                        Scroll to bottom
                    </button>
                </div>
                <div className="container">
                    <Fragment ref={fragmentRef}>
                        {children}
                    </Fragment>
                </div>
            </>
        );
    }

    const items = [];
    for (let i = 1; i <= 25; i++) {
        items.push('Item ' + i);
    }

    export default function App() {
        return (
            <ScrollableSection>
                <h3>Section Start</h3>
                {items.map((item) => (
                    <p key={item}>{item}</p>
                ))}
                <h3>Section End</h3>
            </ScrollableSection>
        );
    }
    ```

=== "styles.css"

    ```css

    .buttons {
      display: flex;
      gap: 8px;
      margin-bottom: 10px;
    }

    .container {
      height: 200px;
      overflow-y: auto;
      border: 2px solid #c4c4c4;
      border-radius: 4px;
      padding: 10px;
    }

    h3 {
      margin: 4px 0;
      /* Padding to handle offset of global sticky nav when scrolling for example */
      padding-top: 4em;
      color: #1a73e8;
    }

    p {
      margin: 4px 0;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

### Наблюдение за видимостью без элемента-обёртки {#observing-visibility-without-wrapper}

`observeUsing` подключает `IntersectionObserver` ко всем DOM-потомкам фрагмента первого уровня. Так можно следить за видимостью, не заставляя дочерние компоненты отдавать `ref` и не добавляя элемент-обёртку:

=== "js"

    ```js

    import {
        Fragment,
        useRef,
        useLayoutEffect,
        useState,
    } from 'react';
    import Card from './Card';

    function VisibleGroup({ onVisibilityChange, children }) {
        const fragmentRef = useRef(null);

        useLayoutEffect(() => {
            const visibleElements = new Set();
            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach(e => {
                        if (e.isIntersecting) {
                            visibleElements.add(e.target);
                        } else {
                            visibleElements.delete(e.target);
                        }
                    });
                    onVisibilityChange(visibleElements.size > 0);
                }
            );
            const fragmentInstance = fragmentRef.current;
            fragmentInstance.observeUsing(observer);
            return () => {
                fragmentInstance.unobserveUsing(observer);
            };
        }, [onVisibilityChange]);

        return (
            <Fragment ref={fragmentRef}>
                {children}
            </Fragment>
        );
    }

    export default function App() {
        const [isVisible, setIsVisible] = useState(true);

        return (
            <div className={isVisible ? 'page visible' : 'page'}>
                <div className="filler">Scroll down</div>
                <VisibleGroup onVisibilityChange={setIsVisible}>
                    <Card title="First section" />
                    <Card title="Second section" />
                </VisibleGroup>
                <div className="filler">Scroll up</div>
            </div>
        );
    }
    ```

=== "styles.css"

    ```css

    .page {
      transition: background 0.3s;
    }

    .page.visible {
      background: #d4edda;
    }

    .filler {
      height: 500px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #aaa;
      font-size: 14px;
    }

    .card {
      padding: 16px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      margin: 8px 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      font-weight: 600;
      font-size: 14px;
    }
    ```

=== "Card.js"

    ```js

    export default function Card({ title }) {
        return <div className="card">{title}</div>;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

### Кэширование общего IntersectionObserver {#caching-global-intersection-observer}

Частая оптимизация для страниц со множеством наблюдателей — один `IntersectionObserver` на конфигурацию и маршрутизация его записей в нужные колбэки по тому, какой элемент пересёкся. Рефы фрагмента поддерживают тот же приём через свойство `reactFragments`.

У каждого DOM-потомка первого уровня фрагмента с `ref` есть свойство `reactFragments`: `Set` объектов `FragmentInstance`, которые содержат этот элемент. Когда срабатывает общий наблюдатель, по этому свойству можно найти, какому `FragmentInstance` принадлежит пересекающийся элемент, и вызвать нужные колбэки.

=== "App.js"

    ```js

    import { useState, useCallback } from 'react';
    import ObservedGroup from './ObservedGroup';
    import Card from './Card';

    export default function App() {
        const [bgColor, setBgColor] = useState(null);

        const onGreen = useCallback((entry) => {
            if (entry.isIntersecting) {
                setBgColor('#d4edda');
            }
        }, []);

        const onBlue = useCallback((entry) => {
            if (entry.isIntersecting) {
                setBgColor('#cce5ff');
            }
        }, []);

        return (
            <div className="page" style={{
                background: bgColor || 'white',
            }}>
                <div className="filler">Scroll down</div>
                <ObservedGroup onIntersection={onGreen}>
                    <Card title="Green section" className="green" />
                </ObservedGroup>
                <div className="filler" />
                <ObservedGroup onIntersection={onBlue}>
                    <Card title="Blue section" className="blue" />
                </ObservedGroup>
                <div className="filler">Scroll up</div>
            </div>
        );
    }
    ```

=== "ObservedGroup.js"

    ```js

    import {
        Fragment,
        useRef,
        useLayoutEffect,
    } from 'react';

    const callbackMap = new WeakMap();
    const observerCache = new Map();

    function getOptionsKey(options) {
        const root = options?.root ?? null;
        const rootMargin = options?.rootMargin ?? '0px';
        const threshold = options?.threshold ?? 0;
        return `${rootMargin}|${threshold}`;
    }

    function getSharedObserver(
        fragmentInstance,
        onIntersection,
        options,
    ) {
        // Register this callback for the
        // fragment instance.
        const existing =
            callbackMap.get(fragmentInstance);
        callbackMap.set(
            fragmentInstance,
            existing
                ? [...existing, onIntersection]
                : [onIntersection],
        );

        const key = getOptionsKey(options);
        if (observerCache.has(key)) {
            return observerCache.get(key);
        }

        const observer = new IntersectionObserver(
            (entries) => {
                for (const entry of entries) {
                    // Look up which FragmentInstances own
                    // this element.
                    const fragmentInstances =
                        entry.target.reactFragments;
                    if (fragmentInstances) {
                        for (const inst of fragmentInstances) {
                            const callbacks =
                                callbackMap.get(inst) || [];
                            callbacks.forEach(cb => cb(entry));
                        }
                    }
                }
            },
            options,
        );

        observerCache.set(key, observer);
        return observer;
    }

    export default function ObservedGroup({
        onIntersection,
        options,
        children,
    }) {
        const fragmentRef = useRef(null);

        useLayoutEffect(() => {
            const fragmentInstance = fragmentRef.current;
            const observer = getSharedObserver(
                fragmentInstance,
                onIntersection,
                options,
            );
            fragmentInstance.observeUsing(observer);
            return () => {
                fragmentInstance.unobserveUsing(observer);
                callbackMap.delete(fragmentInstance);
            };
        }, [onIntersection, options]);

        return (
            <Fragment ref={fragmentRef}>
                {children}
            </Fragment>
        );
    }
    ```

=== "styles.css"

    ```css

    .page {
      transition: background 0.3s;
    }

    .filler {
      height: 500px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #aaa;
      font-size: 14px;
    }

    .card {
      padding: 16px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      margin: 0 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      font-weight: 600;
      font-size: 14px;
    }

    .card.green {
      border-left: 3px solid #28a745;
    }

    .card.blue {
      border-left: 3px solid #007bff;
    }
    ```

=== "Card.js"

    ```js

    export default function Card({ title, className }) {
        return <div className={'card' + (className ? ' ' + className : '')}>{title}</div>;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

Несколько компонентов `ObservedGroup` с одинаковыми параметрами переиспользуют один `IntersectionObserver`. Когда любая из секций прокручивается в область видимости, общий наблюдатель срабатывает и через `reactFragments` направляет запись в нужный колбэк.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/Fragment](https://react.dev/reference/react/Fragment)</small>
