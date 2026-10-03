---
description: <Activity> позволяет скрывать и восстанавливать интерфейс и внутреннее состояние дочерних элементов
---

# &lt;Activity&gt;

<big>**`<Activity>`** позволяет скрывать и восстанавливать интерфейс и внутреннее состояние дочерних элементов.</big>

```js
<Activity mode={visibility}>
  <Sidebar />
</Activity>
```

## Описание {#reference}

### `&lt;Activity&gt;` {#activity}

Activity можно использовать, чтобы скрыть часть приложения:

```js hl_lines="1 2"
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>
  <Sidebar />
</Activity>
```

Когда граница Activity скрыта, React визуально скрывает её дочерние элементы с помощью CSS-свойства `display: "none"`. Он также уничтожает их эффекты, очищая все активные подписки.

Пока граница скрыта, дочерние компоненты всё равно перерендериваются в ответ на новые пропсы, хотя и с более низким приоритетом, чем остальное содержимое.

Когда граница снова становится видимой, React показывает дочерние элементы с восстановленным прежним состоянием и заново создаёт их эффекты.

Таким образом, Activity можно считать механизмом рендеринга «фоновой активности». Вместо того чтобы полностью отбрасывать содержимое, которое, скорее всего, снова станет видимым, Activity позволяет сохранять и восстанавливать интерфейс и внутреннее состояние этого содержимого и при этом гарантировать, что у скрытого содержимого нет нежелательных побочных эффектов.

[См. больше примеров ниже.](#usage)

#### Пропсы {#props}

-   `children`: Интерфейс, который вы собираетесь показывать и скрывать.
-   `mode`: Строка со значением `'visible'` или `'hidden'`. Если проп опущен, по умолчанию используется `'visible'`.

#### Предупреждения {#caveats}

-   Если Activity отрендерен внутри [ViewTransition](ViewTransition.md) и становится видимым в результате обновления, вызванного [startTransition](startTransition.md), активируется анимация `enter` у ViewTransition. Если он становится скрытым, активируется его анимация `exit`.
-   *Скрытый* Activity, который рендерит только текст, не выводит ничего: скрытый текст тоже не появляется, потому что нет соответствующего DOM-элемента, к которому можно применить изменение видимости. Например, `<Activity mode="hidden"><ComponentThatJustReturnsText /></Activity>` не создаст никакого вывода в DOM для `const ComponentThatJustReturnsText = () => "Hello, World!"`. `<Activity mode="visible"><ComponentThatJustReturnsText /></Activity>` отрендерит видимый текст.

## Использование {#usage}

### Восстановление состояния скрытых компонентов {#restoring-the-state-of-hidden-components}

В React, когда нужно условно показать или скрыть компонент, его обычно монтируют или размонтируют в зависимости от этого условия:

```jsx
{isShowingSidebar && (
  <Sidebar />
)}
```

Но размонтирование компонента уничтожает его внутреннее состояние, а это нужно не всегда.

Когда вместо этого вы скрываете компонент границей Activity, React «сохранит» его состояние на потом:

```jsx
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>
  <Sidebar />
</Activity>
```

Так можно скрыть компоненты, а затем восстановить их в том состоянии, в котором они были раньше.

В следующем примере есть боковая панель с раскрывающимся разделом. Можно нажать «Overview», чтобы показать три пункта под ним. В основной области приложения тоже есть кнопка, которая скрывает и показывает боковую панель.

Попробуйте раскрыть раздел Overview, а затем закрыть и снова открыть боковую панель:

=== "App.js"

    ```js

    import { useState } from 'react';
    import Sidebar from './Sidebar.js';

    export default function App() {
        const [isShowingSidebar, setIsShowingSidebar] = useState(true);

        return (
            <>
                {isShowingSidebar && (
                    <Sidebar />
                )}

                <main>
                    <button onClick={() => setIsShowingSidebar(!isShowingSidebar)}>
                        Toggle sidebar
                    </button>
                    <h1>Main content</h1>
                </main>
            </>
        );
    }
    ```

=== "Sidebar.js"

    ```js

    import { useState } from 'react';

    export default function Sidebar() {
        const [isExpanded, setIsExpanded] = useState(false)

        return (
            <nav>
                <button onClick={() => setIsExpanded(!isExpanded)}>
                    Overview
                    <span className={`indicator ${isExpanded ? 'down' : 'right'}`}>
                        &#9650;
                    </span>
                </button>

                {isExpanded && (
                    <ul>
                        <li>Section 1</li>
                        <li>Section 2</li>
                        <li>Section 3</li>
                    </ul>
                )}
            </nav>
        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; margin: 0; }
    #root {
      display: flex;
      gap: 10px;
      height: 100%;
    }
    nav {
      padding: 10px;
      background: #eee;
      font-size: 14px;
      height: 100%;
    }
    main {
      padding: 10px;
    }
    p {
      margin: 0;
    }
    h1 {
      margin-top: 10px;
    }
    .indicator {
      margin-left: 4px;
      display: inline-block;
      rotate: 90deg;
    }
    .indicator.down {
      rotate: 180deg;
    }
    ```

Раздел Overview всегда начинается свёрнутым. Поскольку мы размонтируем боковую панель, когда `isShowingSidebar` становится `false`, всё её внутреннее состояние теряется.

Это отличный случай для Activity. Мы можем сохранить внутреннее состояние боковой панели, даже когда визуально её скрываем.

Заменим условный рендеринг боковой панели границей Activity:

```jsx hl_lines="7 9"
// Before
{isShowingSidebar && (
  <Sidebar />
)}

// After
<Activity mode={isShowingSidebar ? 'visible' : 'hidden'}>
  <Sidebar />
</Activity>
```

и посмотрите на новое поведение:

=== "App.js"

    ```js

    import { Activity, useState } from 'react';

    import Sidebar from './Sidebar.js';

    export default function App() {
        const [isShowingSidebar, setIsShowingSidebar] = useState(true);

        return (
            <>
                <Activity mode={isShowingSidebar ? 'visible' : 'hidden'}>
                    <Sidebar />
                </Activity>

                <main>
                    <button onClick={() => setIsShowingSidebar(!isShowingSidebar)}>
                        Toggle sidebar
                    </button>
                    <h1>Main content</h1>
                </main>
            </>
        );
    }
    ```

=== "Sidebar.js"

    ```js

    import { useState } from 'react';

    export default function Sidebar() {
        const [isExpanded, setIsExpanded] = useState(false)

        return (
            <nav>
                <button onClick={() => setIsExpanded(!isExpanded)}>
                    Overview
                    <span className={`indicator ${isExpanded ? 'down' : 'right'}`}>
                        &#9650;
                    </span>
                </button>

                {isExpanded && (
                    <ul>
                        <li>Section 1</li>
                        <li>Section 2</li>
                        <li>Section 3</li>
                    </ul>
                )}
            </nav>
        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; margin: 0; }
    #root {
      display: flex;
      gap: 10px;
      height: 100%;
    }
    nav {
      padding: 10px;
      background: #eee;
      font-size: 14px;
      height: 100%;
    }
    main {
      padding: 10px;
    }
    p {
      margin: 0;
    }
    h1 {
      margin-top: 10px;
    }
    .indicator {
      margin-left: 4px;
      display: inline-block;
      rotate: 90deg;
    }
    .indicator.down {
      rotate: 180deg;
    }
    ```

Внутреннее состояние боковой панели теперь восстанавливается, без каких-либо изменений в её реализации.

### Восстановление DOM скрытых компонентов {#restoring-the-dom-of-hidden-components}

Поскольку границы Activity скрывают дочерние элементы с помощью `display: none`, DOM дочерних элементов тоже сохраняется, пока они скрыты. Это удобно, чтобы удерживать временное состояние в тех частях интерфейса, с которыми пользователь, скорее всего, снова будет взаимодействовать.

В этом примере на вкладке Contact есть `<textarea>`, куда пользователь может ввести сообщение. Если ввести текст, перейти на вкладку Home, а затем вернуться на вкладку Contact, черновик сообщения пропадёт:

=== "App.js"

    ```js

    import { useState } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Contact from './Contact.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('contact');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'contact'}
                    onClick={() => setActiveTab('contact')}
                >
                    Contact
                </TabButton>

                <hr />

                {activeTab === 'home' && <Home />}
                {activeTab === 'contact' && <Contact />}
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Contact.js"

    ```js

    export default function Contact() {
        return (
            <div>
                <p>Send me a message!</p>

                <textarea />

                <p>You can find me online here:</p>
                <ul>
                    <li>admin@mysite.com</li>
                    <li>+123456789</li>
                </ul>
            </div>
        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    ```

Так происходит потому, что мы полностью размонтируем `Contact` в `App`. Когда вкладка Contact размонтируется, внутреннее состояние DOM элемента `<textarea>` теряется.

Если вместо этого использовать границу Activity, чтобы показывать и скрывать активную вкладку, можно сохранить состояние DOM каждой вкладки. Попробуйте снова ввести текст и переключить вкладки: черновик сообщения больше не сбрасывается:

=== "App.js"

    ```js

    import { Activity, useState } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Contact from './Contact.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('contact');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'contact'}
                    onClick={() => setActiveTab('contact')}
                >
                    Contact
                </TabButton>

                <hr />

                <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
                    <Home />
                </Activity>
                <Activity mode={activeTab === 'contact' ? 'visible' : 'hidden'}>
                    <Contact />
                </Activity>
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Contact.js"

    ```js

    export default function Contact() {
        return (
            <div>
                <p>Send me a message!</p>

                <textarea />

                <p>You can find me online here:</p>
                <ul>
                    <li>admin@mysite.com</li>
                    <li>+123456789</li>
                </ul>
            </div>
        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    ```

И снова граница Activity позволила сохранить внутреннее состояние вкладки Contact, не меняя её реализацию.

### Предварительный рендеринг содержимого, которое, скорее всего, станет видимым {#pre-rendering-content-thats-likely-to-become-visible}

До сих пор мы видели, как Activity может скрывать содержимое, с которым пользователь уже взаимодействовал, не отбрасывая временное состояние этого содержимого.

Но границы Activity можно использовать и чтобы _подготовить_ содержимое, которое пользователь ещё не видел:

```jsx hl_lines="1"
<Activity mode="hidden">
  <SlowComponent />
</Activity>
```

Когда граница Activity скрыта во время первоначального рендеринга, её дочерние элементы не будут видны на странице — но они _всё равно будут отрендерены_, хотя и с более низким приоритетом, чем видимое содержимое, и без монтирования их эффектов.

Такой _предварительный рендеринг_ позволяет дочерним элементам заранее загрузить нужные код или данные, чтобы позже, когда граница Activity станет видимой, дочерние элементы появлялись быстрее и с меньшим временем загрузки.

Рассмотрим пример.

В этой демонстрации вкладка Posts загружает некоторые данные. Если нажать на неё, вы увидите фолбэк Suspense, пока данные загружаются:

=== "App.js"

    ```js

    import { useState, Suspense } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Posts from './Posts.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('home');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'posts'}
                    onClick={() => setActiveTab('posts')}
                >
                    Posts
                </TabButton>

                <hr />

                <Suspense fallback={<h1>🌀 Loading...</h1>}>
                    {activeTab === 'home' && <Home />}
                    {activeTab === 'posts' && <Posts />}
                </Suspense>
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Posts.js"

    ```js

    import { use } from 'react';
    import { fetchData } from './data.js';

    export default function Posts() {
        const posts = use(fetchData('/posts'));

        return (
            <ul className="items">
                {posts.map(post =>
                    <li className="item" key={post.id}>
                        {post.title}
                    </li>
                )}
            </ul>
        );
    }
    ```

=== "data.js"

    ```js

    // Note: the way you would do data fetching depends on
    // the framework that you use together with Suspense.
    // Normally, the caching logic would be inside a framework.

    let cache = new Map();

    export function fetchData(url) {
        if (!cache.has(url)) {
            cache.set(url, getData(url));
        }
        return cache.get(url);
    }

    async function getData(url) {
        if (url.startsWith('/posts')) {
            return await getPosts();
        } else {
            throw Error('Not implemented');
        }
    }

    async function getPosts() {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });
        let posts = [];
        for (let i = 0; i < 10; i++) {
            posts.push({
                id: i,
                title: 'Post #' + (i + 1)
            });
        }
        return posts;
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    video { width: 300px; margin-top: 10px; aspect-ratio: 16/9; }
    ```

Так происходит потому, что `App` не монтирует `Posts`, пока его вкладка не активна.

Если обновить `App`, чтобы показывать и скрывать активную вкладку границей Activity, `Posts` будет предварительно отрендерен при первой загрузке приложения и сможет загрузить свои данные до того, как станет видимым.

Попробуйте теперь нажать на вкладку Posts:

=== "App.js"

    ```js

    import { Activity, useState, Suspense } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Posts from './Posts.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('home');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'posts'}
                    onClick={() => setActiveTab('posts')}
                >
                    Posts
                </TabButton>

                <hr />

                <Suspense fallback={<h1>🌀 Loading...</h1>}>
                    <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
                        <Home />
                    </Activity>
                    <Activity mode={activeTab === 'posts' ? 'visible' : 'hidden'}>
                        <Posts />
                    </Activity>
                </Suspense>
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Posts.js"

    ```js

    import { use } from 'react';
    import { fetchData } from './data.js';

    export default function Posts() {
        const posts = use(fetchData('/posts'));

        return (
            <ul className="items">
                {posts.map(post =>
                    <li className="item" key={post.id}>
                        {post.title}
                    </li>
                )}
            </ul>
        );
    }
    ```

=== "data.js"

    ```js

    // Note: the way you would do data fetching depends on
    // the framework that you use together with Suspense.
    // Normally, the caching logic would be inside a framework.

    let cache = new Map();

    export function fetchData(url) {
        if (!cache.has(url)) {
            cache.set(url, getData(url));
        }
        return cache.get(url);
    }

    async function getData(url) {
        if (url.startsWith('/posts')) {
            return await getPosts();
        } else {
            throw Error('Not implemented');
        }
    }

    async function getPosts() {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });
        let posts = [];
        for (let i = 0; i < 10; i++) {
            posts.push({
                id: i,
                title: 'Post #' + (i + 1)
            });
        }
        return posts;
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    video { width: 300px; margin-top: 10px; aspect-ratio: 16/9; }
    ```

`Posts` смог подготовиться к более быстрому рендерингу благодаря скрытой границе Activity.

Предварительный рендеринг компонентов скрытыми границами Activity — мощный способ сократить время загрузки тех частей интерфейса, с которыми пользователь, скорее всего, взаимодействует следующими.

!!!note "Примечание"

    Во время предварительного рендеринга загружаются только данные, прочитанные из источника, который [активирует границу Suspense](Suspense.md#what-activates-a-suspense-boundary), например промис, прочитанный с помощью [`use`](use.md). Activity не обнаруживает данные, полученные внутри эффекта.

### Ускорение взаимодействий во время загрузки страницы {#speeding-up-interactions-during-page-load}

В React есть внутренняя оптимизация производительности под названием Selective Hydration. Она гидратирует исходный HTML приложения _частями_, позволяя некоторым компонентам стать интерактивными, даже если другие компоненты на странице ещё не загрузили свой код или данные.

Границы Suspense участвуют в Selective Hydration, потому что естественным образом делят дерево компонентов на независимые друг от друга единицы:

```jsx
function Page() {
  return (
    <>
      <MessageComposer />

      <Suspense fallback="Loading chats...">
        <Chats />
      </Suspense>
    </>
  )
}
```

Здесь `MessageComposer` может быть полностью гидратирован во время первоначального рендеринга страницы, ещё до того, как `Chats` будет смонтирован и начнёт загружать свои данные.

Разбивая дерево компонентов на отдельные единицы, Suspense позволяет React гидратировать отрендеренный на сервере HTML частями, чтобы части приложения становились интерактивными как можно быстрее.

А как быть со страницами, которые не используют Suspense?

Возьмём такой пример с вкладками:

```jsx
function Page() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <>
      <TabButton onClick={() => setActiveTab('home')}>
        Home
      </TabButton>
      <TabButton onClick={() => setActiveTab('video')}>
        Video
      </TabButton>

      {activeTab === 'home' && (
        <Home />
      )}
      {activeTab === 'video' && (
        <Video />
      )}
    </>
  )
}
```

Здесь React должен гидратировать всю страницу за один раз. Если `Home` или `Video` рендерятся медленнее, кнопки вкладок могут казаться неотзывчивыми во время гидратации.

Добавление Suspense вокруг активной вкладки решило бы это:

```jsx hl_lines="13 20"
function Page() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <>
      <TabButton onClick={() => setActiveTab('home')}>
        Home
      </TabButton>
      <TabButton onClick={() => setActiveTab('video')}>
        Video
      </TabButton>

      <Suspense fallback={<Placeholder />}>
        {activeTab === 'home' && (
          <Home />
        )}
        {activeTab === 'video' && (
          <Video />
        )}
      </Suspense>
    </>
  )
}
```

...но это также изменит интерфейс, потому что фолбэк `Placeholder` будет показан при первоначальном рендеринге.

Вместо этого можно использовать Activity. Поскольку границы Activity показывают и скрывают свои дочерние элементы, они уже естественным образом делят дерево компонентов на независимые единицы. И так же, как Suspense, эта возможность позволяет им участвовать в Selective Hydration.

Обновим пример и обернём активную вкладку границами Activity:

```jsx hl_lines="13-18"
function Page() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <>
      <TabButton onClick={() => setActiveTab('home')}>
        Home
      </TabButton>
      <TabButton onClick={() => setActiveTab('video')}>
        Video
      </TabButton>

      <Activity mode={activeTab === "home" ? "visible" : "hidden"}>
        <Home />
      </Activity>
      <Activity mode={activeTab === "video" ? "visible" : "hidden"}>
        <Video />
      </Activity>
    </>
  )
}
```

Теперь исходный HTML, отрендеренный на сервере, выглядит так же, как в первоначальной версии, но благодаря Activity React может сначала гидратировать кнопки вкладок, ещё до того, как смонтирует `Home` или `Video`.

Таким образом, помимо скрытия и показа содержимого, границы Activity улучшают производительность приложения во время гидратации: React узнаёт, какие части страницы могут стать интерактивными по отдельности.

И даже если страница никогда не скрывает часть своего содержимого, можно добавить всегда видимые границы Activity, чтобы улучшить производительность гидратации:

```jsx
function Page() {
  return (
    <>
      <Post />

      <Activity>
        <Comments />
      </Activity>
    </>
  );
}
```

## Устранение неполадок {#troubleshooting}

### У скрытых компонентов есть нежелательные побочные эффекты {#my-hidden-components-have-unwanted-side-effects}

Граница Activity скрывает своё содержимое, устанавливая `display: none` у дочерних элементов и очищая все их эффекты. Поэтому большинство корректных компонентов React, которые правильно очищают свои побочные эффекты, уже устойчивы к скрытию через Activity.

Но _бывают_ ситуации, когда скрытый компонент ведёт себя иначе, чем размонтированный. Главное отличие: DOM скрытого компонента не уничтожается, поэтому любые побочные эффекты этого DOM сохраняются и после того, как компонент скрыт.

В качестве примера рассмотрим тег `<video>`. Обычно ему не нужна очистка, потому что даже если видео воспроизводится, размонтирование тега останавливает видео и звук в браузере. Попробуйте воспроизвести видео, а затем нажать Home в этой демонстрации:

=== "App.js"

    ```js

    import { useState } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Video from './Video.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('video');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'video'}
                    onClick={() => setActiveTab('video')}
                >
                    Video
                </TabButton>

                <hr />

                {activeTab === 'home' && <Home />}
                {activeTab === 'video' && <Video />}
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Video.js"

    ```js

    export default function Video() {
        return (
            <video
                // 'Big Buck Bunny' licensed under CC 3.0 by the Blender foundation. Hosted by archive.org
                src="https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4"
                controls
                playsInline
            />

        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    video { width: 300px; margin-top: 10px; aspect-ratio: 16/9; }
    ```

Видео останавливается, как и ожидалось.

Теперь допустим, мы хотим сохранить таймкод, на котором пользователь остановился, чтобы при возврате на вкладку видео не начиналось сначала.

Это отличный случай для Activity!

Обновим `App`, чтобы скрывать неактивную вкладку скрытой границей Activity вместо размонтирования, и посмотрим, как демонстрация ведёт себя теперь:

=== "App.js"

    ```js

    import { Activity, useState } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Video from './Video.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('video');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'video'}
                    onClick={() => setActiveTab('video')}
                >
                    Video
                </TabButton>

                <hr />

                <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
                    <Home />
                </Activity>
                <Activity mode={activeTab === 'video' ? 'visible' : 'hidden'}>
                    <Video />
                </Activity>
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Video.js"

    ```js

    export default function Video() {
        return (
            <video
                controls
                playsInline
                // 'Big Buck Bunny' licensed under CC 3.0 by the Blender foundation. Hosted by archive.org
                src="https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4"
            />

        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    video { width: 300px; margin-top: 10px; aspect-ratio: 16/9; }
    ```

Ой! Видео и звук продолжают воспроизводиться даже после скрытия, потому что элемент `<video>` вкладки всё ещё находится в DOM.

Чтобы это исправить, можно добавить эффект с функцией очистки, которая ставит видео на паузу:

```jsx hl_lines="2 4-10 14"
export default function VideoTab() {
  const ref = useRef();

  useLayoutEffect(() => {
    const videoRef = ref.current;

    return () => {
      videoRef.pause()
    }
  }, []);

  return (
    <video
      ref={ref}
      controls
      playsInline
      src="..."
    />

  );
}
```

Мы вызываем `useLayoutEffect` вместо `useEffect`, потому что концептуально код очистки связан с визуальным скрытием интерфейса компонента. Если использовать обычный эффект, код может задержаться, например, из-за повторной приостановки границы Suspense или View Transition.

Посмотрим на новое поведение. Попробуйте воспроизвести видео, переключиться на вкладку Home, а затем вернуться на вкладку Video:

=== "App.js"

    ```js

    import { Activity, useState } from 'react';
    import TabButton from './TabButton.js';
    import Home from './Home.js';
    import Video from './Video.js';

    export default function App() {
        const [activeTab, setActiveTab] = useState('video');

        return (
            <>
                <TabButton
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                >
                    Home
                </TabButton>
                <TabButton
                    isActive={activeTab === 'video'}
                    onClick={() => setActiveTab('video')}
                >
                    Video
                </TabButton>

                <hr />

                <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
                    <Home />
                </Activity>
                <Activity mode={activeTab === 'video' ? 'visible' : 'hidden'}>
                    <Video />
                </Activity>
            </>
        );
    }
    ```

=== "TabButton.js"

    ```js

    export default function TabButton({ onClick, children, isActive }) {
        if (isActive) {
            return <b>{children}</b>
        }

        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "Home.js"

    ```js

    export default function Home() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "Video.js"

    ```js

    import { useRef, useLayoutEffect } from 'react';

    export default function Video() {
        const ref = useRef();

        useLayoutEffect(() => {
            const videoRef = ref.current

            return () => {
                videoRef.pause()
            };
        }, [])

        return (
            <video
                ref={ref}
                controls
                playsInline
                // 'Big Buck Bunny' licensed under CC 3.0 by the Blender foundation. Hosted by archive.org
                src="https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4"
            />

        );
    }
    ```

=== "styles.css"

    ```css

    body { height: 275px; }
    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    video { width: 300px; margin-top: 10px; aspect-ratio: 16/9; }
    ```

Отлично работает! Функция очистки гарантирует, что видео остановится, если его когда-либо скроет граница Activity, и, что ещё лучше, поскольку тег `<video>` никогда не уничтожается, таймкод сохраняется, а само видео не нужно заново инициализировать или скачивать, когда пользователь возвращается, чтобы продолжить просмотр.

Это хороший пример того, как Activity сохраняет временное состояние DOM для частей интерфейса, которые становятся скрытыми, но с которыми пользователь, скорее всего, скоро снова будет взаимодействовать.

Пример показывает, что для некоторых тегов, таких как `<video>`, размонтирование и скрытие ведут себя по-разному. Если компонент рендерит DOM с побочным эффектом и вы хотите предотвратить этот побочный эффект, когда граница Activity его скрывает, добавьте эффект с возвращаемой функцией очистки.

Чаще всего это касается следующих тегов:

  - `<video>`
  - `<audio>`
  - `<iframe>`

Впрочем, большинство ваших компонентов React уже должны быть устойчивы к скрытию границей Activity. И концептуально о «скрытых» Activity стоит думать как о размонтированных.

Чтобы заранее обнаружить другие эффекты без правильной очистки — это важно не только для границ Activity, но и для многих других поведений React — мы рекомендуем использовать [`<StrictMode>`](StrictMode.md).

### У скрытых компонентов есть эффекты, которые не выполняются {#my-hidden-components-have-effects-that-arent-running}

Когда `<Activity>` «скрыт», все эффекты его дочерних элементов очищаются. Концептуально дочерние элементы размонтированы, но React сохраняет их состояние на потом. Это возможность Activity: подписки не будут активны для скрытых частей интерфейса, и работы для скрытого содержимого потребуется меньше.

Если вы полагаетесь на то, что монтирование эффекта очистит побочные эффекты компонента, переделайте эффект так, чтобы эта работа выполнялась в возвращаемой функции очистки.

Чтобы заранее находить проблемные эффекты, мы рекомендуем добавить [`<StrictMode>`](StrictMode.md): он заранее выполняет размонтирования и монтирования Activity, чтобы поймать неожиданные побочные эффекты.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/Activity](https://react.dev/reference/react/Activity)</small>
