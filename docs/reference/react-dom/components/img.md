---
description: Встроенный компонент браузера img позволяет встроить изображение
---

# &lt;img&gt;

<big>Встроенный [компонент браузера `<img>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img) позволяет встроить изображение.</big>

```js
<img src="photo.jpg" alt="A person walking through a park" />
```

## Описание {#reference}

### `&lt;img&gt;` {#img}

Чтобы показать изображение, отрендерите [встроенный компонент браузера `<img>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img).

```js
<img src="photo.jpg" alt="A person walking through a park" />
```

[Больше примеров ниже.](#usage)

#### Пропсы {#props}

`<img>` поддерживает все [общие пропсы элементов.](common.md#props)

-   `alt`: строка. Задаёт альтернативный текст изображения. Для чисто декоративного изображения используйте пустую строку.
-   `crossOrigin`: строка. Задаёт [политику CORS](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin), которую нужно использовать при загрузке изображения. Возможные значения: `anonymous` и `use-credentials`.
-   `decoding`: строка. Подсказывает, должен ли браузер дождаться декодирования изображения, прежде чем показывать остальное содержимое. Возможные значения: `async`, `sync` и `auto` (по умолчанию).
-   `fetchPriority`: строка. Предлагает относительный приоритет загрузки изображения. Возможные значения: `high`, `low` и `auto` (по умолчанию). Во время серверного рендеринга `fetchPriority="low"` также не даёт React [автоматически предварительно загружать изображение.](#controlling-image-preloading-during-server-rendering)
-   `height`: число или строка. Задаёт отображаемую высоту изображения.
-   `loading`: строка. Указывает, должен ли браузер отложить загрузку изображения, пока оно не окажется рядом с областью просмотра. Возможные значения: `eager` (по умолчанию) и `lazy`. Значение `loading="lazy"` не даёт React [автоматически предварительно загружать изображение.](#controlling-image-preloading-during-server-rendering)
-   `onError`: функция-[обработчик события](common.md#event-handler). Срабатывает, когда изображение не загрузилось.
-   `onLoad`: функция-[обработчик события](common.md#event-handler). Срабатывает, когда изображение закончило загружаться. Передача `onLoad` не даёт React [ждать изображение во время клиентского обновления View Transition.](#waiting-for-an-image-during-a-view-transition)
-   `referrerPolicy`: строка. Задаёт [информацию о реферере](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#referrerpolicy), которую нужно отправлять при загрузке изображения.
-   `sizes`: строка. Задаёт размеры изображения для разных раскладок страницы. Используется вместе с `srcSet`.
-   `src`: строка. Задаёт URL изображения.
-   `srcSet`: строка. Задаёт один или несколько вариантов источника изображения, из которых браузер может выбрать.
-   `useMap`: строка. Связывает изображение с [клиентской картой изображения](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/map).
-   `width`: число или строка. Задаёт отображаемую ширину изображения.

#### Предупреждения {#caveats}

-   Не передавайте в `src` пустую строку. Из-за этого браузер может снова запросить текущую страницу. В режиме разработки React предупреждает и опускает атрибут. Чтобы не рендерить изображение, не выводите `<img>` или передайте в `src` значение `null`.
-   `<img>` не может иметь дочерние элементы и не может использовать `dangerouslySetInnerHTML`. React выбросит ошибку, если передать то или другое.
-   `fetchPriority="low"` не мешает React ждать загрузки и декодирования изображения во время клиентского обновления View Transition. Чтобы отказаться от этого поведения, используйте `loading="lazy"` или обработчик `onLoad`.

## Использование {#usage}

### Отображение изображения {#displaying-an-image}

Передайте URL изображения в `src` и текстовое описание в `alt`:

=== "js"

    ```js
    export default function Profile() {
        return (
            <img
                src="https://react.dev/images/docs/scientists/yXOvdOSs.jpg"
                alt="Hedy Lamarr"
                width={100}
                height={100}
            />
        );
    }
    ```

=== "styles.css"

    ```css
    img {
      border-radius: 50%;
      object-fit: cover;
    }
    ```

Укажите `width` и `height`, если знаете размеры изображения, чтобы браузер зарезервировал место до его загрузки. Для декоративного изображения передайте `alt=""`, чтобы программы чтения с экрана его проигнорировали.

### Управление предварительной загрузкой изображения во время серверного рендеринга {#controlling-image-preloading-during-server-rendering}

Во время серверного рендеринга React по умолчанию автоматически создаёт подсказку предварительной загрузки для `<img>`. Благодаря этому браузер может начать загрузку изображения до того, как встретит `<img>` в отрендеренном HTML.

Добавьте `loading="lazy"` или `fetchPriority="low"` изображению, которое не должно получать эту подсказку:

```js
function ProductPage() {
  return (
    <>
      <img src="hero.jpg" alt="Featured product" />
      <img src="thumbnail.jpg" alt="Related product" loading="lazy" />
      <img src="secondary.jpg" alt="Another product" fetchPriority="low" />
    </>
  );
}
```

В этом примере React создаёт подсказку предварительной загрузки только для `hero.jpg`. В зависимости от серверного API или фреймворка React может отрендерить эквивалент такого элемента:

```html
<link rel="preload" as="image" href="hero.jpg" />
```

React может вместо этого передать ту же подсказку в заголовке ответа `Link`. У двух других изображений пропсы `loading` и `fetchPriority` сохраняются в отрендеренном HTML, но React не создаёт для них подсказки предварительной загрузки. Проп `loading="lazy"` просит браузер отложить загрузку изображения, пока оно не приблизится к области просмотра. Проп `fetchPriority="low"` позволяет загрузить изображение сразу, но говорит браузеру получать его с меньшим приоритетом.

React также не создаёт автоматическую предварительную загрузку, если изображение находится внутри элемента `<picture>` или `<noscript>` либо если его `src` или `srcSet` — это data URL.

Если вы рендерите изображение через фреймворк или библиотеку компонентов, смотрите в её документации поведение по умолчанию. React решает, создавать ли автоматическую предварительную загрузку, по пропсам нижележащего `<img>`. Например, компонент изображения может по умолчанию добавлять `loading="lazy"` и давать отдельную опцию, чтобы явно предварительно загружать выбранные изображения.

Чтобы создать явную подсказку предварительной загрузки, вызовите [`preload`](../preload.md).

### Ожидание изображения во время View Transition {#waiting-for-an-image-during-a-view-transition}

Во время клиентского обновления [`<ViewTransition>`](../../react/ViewTransition.md) React может дождаться загрузки и декодирования изображения, прежде чем начать анимацию. Это происходит, когда рендерится новый `<img>` с непустым `src` или когда у существующего изображения меняется `src` или `srcSet`. Изображение должно находиться внутри поддерева `<ViewTransition>` и не должно иметь `loading="lazy"` или обработчик `onLoad`. Во время синхронных обновлений React не ждёт изображения.

Когда граница Suspense раскрывает потоковое содержимое внутри `<ViewTransition>`, React также может ждать видимые изображения с непустым `src`, у которых нет `loading="lazy"`. React перестаёт ждать после таймаута, чтобы медленное изображение не блокировало обновление бесконечно.

В этом примере граница Suspense обёрнута в `<ViewTransition>` и показывает скелетон профиля, пока портрет не загрузится.

Для сравнения вторая кнопка вставляет ту же карточку прямо в DOM. Карточка появляется сразу, а браузер показывает изображение после загрузки:

=== "js"

    ```js
    import { ViewTransition, Suspense, useState, startTransition } from 'react';
    import { freshImageUrl } from './image.js';
    import VanillaProfile from './VanillaProfile.js';

    function Profile({ src }) {
        return (
            <div className="card">
                <img src={src} alt="Jack Pope" width={80} height={80} />
                <p>Jack Pope</p>
            </div>
        );
    }

    function ProfilePlaceholder() {
        return (
            <div className="card">
                <div className="avatar-placeholder" />
                <p className="name-placeholder">&nbsp;</p>
            </div>
        );
    }

    export default function App() {
        const [src, setSrc] = useState(null);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setSrc(freshImageUrl());
                        });
                    }}>
                    Show profile
                </button>
                {src && (
                    <ViewTransition>
                        <Suspense fallback={<ProfilePlaceholder />}>
                            <Profile src={src} />
                        </Suspense>
                    </ViewTransition>
                )}
                <hr />
                <VanillaProfile />
            </>
        );
    }
    ```

=== "VanillaProfile.js"

    ```js
    import { useRef } from 'react';
    import { freshImageUrl } from './image.js';

    export default function VanillaProfile() {
        const ref = useRef(null);
        function show() {
            ref.current.innerHTML = `<div class="card">
                <img src="${freshImageUrl()}" alt="Jack Pope" width="80" height="80" />
                <p>Jack Pope</p>
            </div>`;
        }
        return (
            <>
                <button onClick={show}>Show profile (direct DOM update)</button>
                <div ref={ref} />
            </>
        );
    }
    ```

=== "image.js"

    ```js
    // Add a unique parameter so the image isn't cached,
    // and every run shows the loading state.
    export function freshImageUrl() {
        return 'https://react.dev/images/team/jack-pope.jpg?t=' + Date.now();
    }
    ```

=== "styles.css"

    ```css
    #root {
      min-height: 390px;
    }
    .card {
      margin-top: 1em;
    }
    .card img {
      display: block;
      border-radius: 50%;
      background: #dfe3e9;
    }
    .card p {
      font-weight: bold;
    }
    .avatar-placeholder {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: #dfe3e9;
    }
    .name-placeholder {
      width: 90px;
      border-radius: 4px;
      background: #dfe3e9;
    }
    hr {
      margin: 16px 0;
    }
    ```

=== "package.js"

    ```json
    {
      "dependencies": {
        "react": "19.3.0",
        "react-dom": "19.3.0",
        "react-scripts": "latest"
      }
    }
    ```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/img](https://react.dev/reference/react-dom/components/img)</small>
