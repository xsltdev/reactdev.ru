---
description: `<ViewTransition>` позволяет анимировать дерево компонентов с помощью переходов (Transition) и приостановки (Suspense).
---

# &lt;ViewTransition&gt;

<big>

`<ViewTransition>` позволяет анимировать дерево компонентов с помощью переходов (Transition) и приостановки (Suspense).

</big>

```js
import {ViewTransition} from 'react';

<ViewTransition>
  <div>...</div>
</ViewTransition>
```

## Описание {#reference}

### `&lt;ViewTransition&gt;` {#viewtransition}

Оберните дерево компонентов в `<ViewTransition>`, чтобы анимировать его:

```js
<ViewTransition>
  <Page />
</ViewTransition>
```

[Больше примеров ниже.](#usage)

??? note "Как работает `&lt;ViewTransition&gt;`?"

    Под капотом React применяет `view-transition-name` к инлайновым стилям ближайшего DOM-узла внутри компонента `<ViewTransition>`. Если соседних DOM-узлов несколько, как в `<ViewTransition></ViewTransition>`, React добавляет к имени суффикс, чтобы каждое было уникальным, но концептуально они остаются частью одного перехода. React не применяет их заранее, а только в тот момент, когда граница должна участвовать в анимации.

    React сам автоматически вызывает `startViewTransition` за кадром, поэтому вызывать его самостоятельно не нужно. Более того, если на странице что-то ещё уже запускает ViewTransition, React прервёт его. Поэтому такие переходы лучше координировать самим React. Если раньше вы запускали ViewTransition другими способами, рекомендуем перейти на встроенный способ.

    Если другие ViewTransition в React уже выполняются, React дождётся их завершения, прежде чем запустить следующий. При этом важно: если пока выполняется первый, происходит несколько обновлений, все они объединяются в одно. Если начат переход A->B, а тем временем приходит обновление к C, а затем к D, то после окончания первой анимации A->B следующая анимирует переход от B к D.

    Метод жизненного цикла `getSnapshotBeforeUpdate` вызывается до `startViewTransition`, и часть `view-transition-name` обновляется в тот же момент.

    Затем React вызывает `startViewTransition`. Внутри `updateCallback` React:

    - Применит свои мутации к DOM и вызовет `useInsertionEffect`.
    - Дождётся загрузки шрифтов.
    - Вызовет `componentDidMount`, `componentDidUpdate`, `useLayoutEffect` и рефы.
    - Дождётся завершения любой ожидающей навигации (Navigation).
    - Измерит изменения компоновки, чтобы определить, какие границы нужно анимировать.

    После того как промис `ready` у `startViewTransition` выполнится, React вернёт `view-transition-name` обратно. Затем React вызовет колбэки `onEnter`, `onExit`, `onUpdate` и `onShare`, чтобы можно было управлять анимациями программно вручную. Это произойдёт после того, как встроенные анимации по умолчанию уже будут вычислены.

    Если в середину этой последовательности попадёт `flushSync`, React пропустит переход (Transition): он должен завершиться синхронно.

    После того как промис `finished` у `startViewTransition` выполнится, React вызовет `useEffect`. Так эффекты не мешают производительности анимации. Это не абсолютная гарантия: если во время анимации произойдёт ещё один `setState`, React всё равно вызовет `useEffect` раньше, чтобы сохранить гарантии последовательности.

#### Пропсы {#props}

- **необязательный** `name`: Строка или объект. Имя перехода вида (View Transition) для переходов общего элемента. Если не указано, React использует уникальное имя для каждого перехода вида, чтобы избежать неожиданных анимаций.
- Пропсы [класса перехода вида](#view-transition-class).
- Пропсы [события перехода вида](#view-transition-event).

#### Предупреждения {#caveats}

- Используйте `name` только для [переходов общего элемента](#animating-a-shared-element). Для всех остальных анимаций React автоматически создаёт уникальное имя, чтобы избежать неожиданных анимаций.
- По умолчанию `setState` обновляет состояние сразу и не активирует `<ViewTransition>`. Переход вида активируют только обновления, обёрнутые в [переход](useTransition.md), [`<Suspense>`](Suspense.md) или `useDeferredValue`.
- `<ViewTransition>` создаёт изображение, которое можно перемещать, масштабировать и плавно перекрёстно затухать (cross-fade). В отличие от анимаций компоновки в React Native или Motion, это означает, что не каждый отдельный элемент внутри анимирует свою позицию. Так можно получить лучшую производительность и более непрерывную, плавную анимацию, чем при анимации каждой части по отдельности. При этом можно потерять непрерывность у того, что должно двигаться самостоятельно. Тогда дополнительные границы `<ViewTransition>` придётся добавить вручную.
- Сейчас `<ViewTransition>` работает только в DOM. Поддержка React Native и других платформ в разработке.

#### Триггеры анимации {#animation-triggers}

React сам выбирает тип анимации перехода вида:

- `enter`: срабатывает, если `ViewTransition` — первый компонент, вставленный в этом переходе.
- `exit`: срабатывает, если `ViewTransition` — первый компонент, удалённый в этом переходе.
- `update`: срабатывает, если внутри `ViewTransition` есть мутации DOM, которые выполняет React (например, изменился проп), или если сама граница `ViewTransition` меняет размер или позицию из-за непосредственного соседа. Если есть вложенные `ViewTransition`, мутация относится к ним, а не к родителю.
- `share`: если именованный `ViewTransition` находится внутри удалённого поддерева, а другой именованный `ViewTransition` с тем же именем входит во вставленное поддерево в том же переходе, они образуют переход общего элемента, и анимация идёт от удалённого к вставленному.

По умолчанию `<ViewTransition>` анимируется плавным перекрёстным затуханием (cross-fade) — это переход вида браузера по умолчанию.

Анимацию можно настроить, передав [класс перехода вида](#view-transition-class) компоненту `<ViewTransition>` для каждого вида триггера (см. [Стилизация переходов вида](#styling-view-transitions)), либо через [события ViewTransition](#view-transition-events), чтобы управлять анимацией на JavaScript с помощью [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API).

!!!note "Всегда проверяйте `prefers-reduced-motion`"

    Многие пользователи предпочитают, чтобы на странице не было анимаций. React не отключает анимации в этом случае сам.

    Рекомендуем всегда использовать медиазапрос `@media (prefers-reduced-motion)`, чтобы отключать анимации или смягчать их с учётом предпочтений пользователя.

    В будущем CSS-библиотеки могут встроить это в свои пресеты.

### Класс перехода вида {#view-transition-class}

`<ViewTransition>` даёт пропсы, которые задают, какие анимации запускать:

```js
<ViewTransition
  default="none"
  enter="slide-up"
  exit="slide-down"
/>
```

#### Пропсы {#view-transition-class-props}

- **необязательный** `enter`: `"auto"`, `"none"`, строка или объект.
- **необязательный** `exit`: `"auto"`, `"none"`, строка или объект.
- **необязательный** `update`: `"auto"`, `"none"`, строка или объект.
- **необязательный** `share`: `"auto"`, `"none"`, строка или объект.
- **необязательный** `default`: `"auto"`, `"none"`, строка или объект.

#### Предупреждения {#view-transition-class-caveats}

- Если `default` равен `"none"`, все остальные триггеры выключены, пока их явно не перечислят.

#### Значения {#view-transition-values}

Значения класса перехода вида могут быть такими:
- `auto`: значение по умолчанию. Используется анимация браузера по умолчанию.
- `none`: отключает анимации этого типа.
- `<classname>`: имя собственного CSS-класса для [настройки переходов вида](#styling-view-transitions).

Значение-объект — это объект со строковыми ключами и значением `auto`, `none` или собственным className:
- `{[type]: value}`: применяет `value`, если анимация соответствует [типу перехода](addTransitionType.md).
- `{default: value}`: значение по умолчанию, если ни один [тип перехода](addTransitionType.md) не совпал.

Например, ViewTransition можно задать так:

```js
<ViewTransition
  /* turn off any animation not defined below */
  default="none"
  enter={{
    /* apply slide-in for Transition Type `forward` */
    "forward": 'slide-in',
    /* otherwise use the browser default animation */
    "default": 'auto'
  }}
  /* use the browser default for exit animations*/
  exit="auto"
  /* apply a custom `cross-fade` class for updates */
  update="cross-fade"
>
```

О том, как задать CSS-классы для собственных анимаций, см. [Стилизация переходов вида](#styling-view-transitions).

### Событие перехода вида {#view-transition-event}

События перехода вида позволяют управлять анимацией на JavaScript через [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API):

```js
<ViewTransition
  onEnter={instance => {/* ... */}}
  onExit={instance => {/* ... */}}
/>
```

#### Пропсы {#view-transition-event-props}

- **необязательный** `onEnter`: вызывается, когда запускается анимация «enter».
- **необязательный** `onExit`: вызывается, когда запускается анимация «exit».
- **необязательный** `onShare`: вызывается, когда запускается анимация «share».
- **необязательный** `onUpdate`: вызывается, когда запускается анимация «update».

#### Предупреждения {#view-transition-event-caveats}
- На каждый `<ViewTransition>` в одном переходе срабатывает только одно событие. `onShare` имеет приоритет над `onEnter` и `onExit`.
- Каждое событие должно возвращать **функцию очистки**. Она вызывается, когда переход вида завершается, и позволяет отменить анимации или освободить связанные с ними ресурсы.

#### Аргументы {#view-transition-event-arguments}

Каждое событие получает два аргумента:

- `instance`: экземпляр перехода вида с доступом к [псевдоэлементам](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using#the_view_transition_process) перехода вида
  - `old`: псевдоэлемент `::view-transition-old`.
  - `new`: псевдоэлемент `::view-transition-new`.
  - `name`: строка `view-transition-name` этой границы.
  - `group`: псевдоэлемент `::view-transition-group`.
  - `imagePair`: псевдоэлемент `::view-transition-image-pair`.
- `types`: `Array<string>` из [типов перехода](addTransitionType.md), участвующих в анимации. Пустой массив, если типы не заданы.

Например, можно задать событие `onEnter`, которое ведёт анимацию на JavaScript:

```js
<ViewTransition
  onEnter={(instance, types) => {
    const anim = instance.new.animate([{opacity: 0}, {opacity: 1}], {
      duration: 500,
    });
    return () => anim.cancel();
  }}>
  <div>...</div>
</ViewTransition>
```

Больше примеров — в разделе [Анимация на JavaScript](#animating-with-javascript).

## Стилизация переходов вида {#styling-view-transitions}

!!!note "Примечание"

    Во многих ранних примерах View Transitions в интернете задают [`view-transition-name`](https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name) и стилизуют его селекторами `::view-transition-...(my-name)`. Для стилизации лучше использовать класс перехода вида.

Чтобы настроить анимацию `<ViewTransition>`, передайте класс перехода вида в один из пропсов активации. Класс перехода вида — это имя CSS-класса, которое React применяет к дочерним элементам, когда ViewTransition активируется.

Например, чтобы настроить анимацию «enter», передайте имя класса в проп `enter`:

```js
<ViewTransition enter="slide-in">
```

Когда `<ViewTransition>` активирует анимацию «enter», React добавит класс `slide-in`. Затем на этот класс можно ссылаться через [псевдоселекторы перехода вида](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API#pseudo-elements) и собирать переиспользуемые анимации:

```css
::view-transition-group(.slide-in) {
}
::view-transition-old(.slide-in) {
}
::view-transition-new(.slide-in) {
}
```

В будущем CSS-библиотеки могут добавить встроенные анимации на классах перехода вида, чтобы пользоваться ими было проще.

## Использование {#usage}

### Анимация элемента при входе и выходе {#animating-an-element-on-enter}

Переходы входа и выхода запускаются, когда компонент внутри перехода добавляет или удаляет `<ViewTransition>`:

```js hl_lines="3"
function Child() {
  return (
    <ViewTransition enter="auto" exit="auto" default="none">
      <div>Hi</div>
    </ViewTransition>
  );
}

function Parent() {
  const [show, setShow] = useState();
  if (show) {
    return <Child />;
  }
  return null;
}
```

Когда вызывается `setShow`, `show` становится `true`, и рендерится компонент `Child`. Если `setShow` вызван внутри `startTransition`, а `Child` рендерит `ViewTransition` раньше любых других DOM-узлов, запускается анимация `enter`.

Когда `show` снова становится `false`, запускается анимация `exit`.

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';

    function Item() {
        return (
            <ViewTransition enter="auto" exit="auto" default="none">
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>

                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

!!!warning "Анимации выхода и входа работают только у ViewTransition верхнего уровня"

    `<ViewTransition>` активирует выход и вход, только если расположен _до_ любых DOM-узлов.

    Если над `<ViewTransition>` стоит `<div>`, анимации выхода и входа не запускаются:

    ```js hl_lines="3 5"
    function Item() {
      return (
        <div> {/* 🚩<div> above <ViewTransition> breaks exit/enter */}
          <ViewTransition enter="auto" exit="auto" default="none">
            <Video video={videos[0]} />
          </ViewTransition>
        </div>
      );
    }
    ```

    Это ограничение защищает от тонких ошибок, когда анимируется слишком много или слишком мало.

### Анимация входа и выхода с помощью Activity {#animating-enter-exit-with-activity}

Если нужно анимировать появление и исчезновение компонента, сохраняя его состояние, или заранее отрендерить содержимое для анимации, используйте [`<Activity>`](Activity.md). Когда `<ViewTransition>` внутри `<Activity>` становится видимым, активируется анимация `enter`. Когда он скрывается, активируется анимация `exit`:

```js
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <ViewTransition enter="auto" exit="auto">
    <Counter />
  </ViewTransition>
</Activity>

```

В этом примере у `Counter` есть счётчик с внутренним состоянием. Увеличьте счётчик, скройте его, а затем покажите снова. Значение счётчика сохраняется, пока боковая панель анимируется при появлении и исчезновении:

=== "js"

    ```js

    import { Activity, ViewTransition, useState, startTransition } from 'react';

    export default function App() {
        const [show, setShow] = useState(true);
        return (
            <div className="layout">
                <Toggle show={show} setShow={setShow} />
                <Activity mode={show ? 'visible' : 'hidden'}>
                    <ViewTransition enter="auto" exit="auto" default="none">
                        <Counter />
                    </ViewTransition>
                </Activity>
            </div>
        );
    }
    function Toggle({show, setShow}) {
        return (
            <button
                className="toggle"
                onClick={() => {
                    startTransition(() => {
                        setShow(s => !s);
                    });
                }}>
                {show ? 'Hide' : 'Show'}
            </button>
        )
    }
    function Counter() {
        const [count, setCount] = useState(0);
        return (
            <div className="counter">
                <h2>Counter</h2>
                <p>Count: {count}</p>
                <button onClick={() => setCount(count + 1)}>
                    Increment
                </button>
            </div>
        );
    }

    ```

=== "styles.css"

    ```css

    .layout {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
      min-height: 200px;
    }
    .counter {
      padding: 15px;
      background: #f0f4f8;
      border-radius: 8px;
      width: 200px;
    }
    .counter h2 {
      margin: 0 0 10px 0;
      font-size: 16px;
    }
    .counter p {
      margin: 0 0 10px 0;
    }
    .toggle {
      padding: 8px 16px;
      border: 1px solid #ccc;
      border-radius: 6px;
      background: #f0f8ff;
      cursor: pointer;
      font-size: 14px;
    }
    .toggle:hover {
      background: #e0e8ff;
    }
    .counter button {
      padding: 4px 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
      background: white;
      cursor: pointer;
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

Без `<Activity>` счётчик сбрасывался бы в `0` каждый раз, когда боковая панель появляется снова.

### Анимация общего элемента {#animating-a-shared-element}

Обычно имя для `<ViewTransition>` лучше не задавать и позволить React назначить его автоматически. Имя нужно, чтобы анимировать переход между совершенно разными компонентами, когда одно дерево размонтируется, а другое монтируется в тот же момент, и сохранить непрерывность.

```js
<ViewTransition name={UNIQUE_NAME}>
  <Child />
</ViewTransition>
```

Когда одно дерево размонтируется, а другое монтируется, пара с одним и тем же именем в размонтируемом и монтируемом деревьях запускает анимацию «share» на обоих. Она идёт от размонтируемой стороны к монтируемой.

В отличие от анимации выхода и входа, такая пара может находиться глубоко внутри удалённого или смонтированного дерева. Если `<ViewTransition>` также подходит для выхода и входа, приоритет у анимации «share».

Если переход сначала размонтирует одну сторону, затем покажется фолбэк `<Suspense>`, и только потом смонтируется новое имя, переход общего элемента не выполняется.

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video, Thumbnail, FullscreenVideo} from './Video';
    import videos from './data';

    export default function Component() {
        const [fullscreen, setFullscreen] = useState(false);
        if (fullscreen) {
            return (
                <FullscreenVideo
                    video={videos[0]}
                    onExit={() => startTransition(() => setFullscreen(false))}
                />
            );
        }
        return (
            <Video
                video={videos[0]}
                onClick={() => startTransition(() => setFullscreen(true))}
            />
        );
    }
    ```

=== "Video.js"

    ```js

    import {ViewTransition} from 'react';

    const THUMBNAIL_NAME = 'video-thumbnail';

    export function Thumbnail({video, children}) {
        return (
            <ViewTransition name={THUMBNAIL_NAME}>
                <div
                    aria-hidden="true"
                    tabIndex={-1}
                    className={`thumbnail ${video.image}`}
                />
            </ViewTransition>
        );
    }

    export function Video({video, onClick}) {
        return (
            <div className="video">
                <div className="link" onClick={onClick}>
                    <Thumbnail video={video} />
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }

    export function FullscreenVideo({video, onExit}) {
        return (
            <div className="fullscreenLayout">
                <ViewTransition name={THUMBNAIL_NAME}>
                    <div
                        aria-hidden="true"
                        tabIndex={-1}
                        className={`thumbnail ${video.image} fullscreen`}
                    />
                    <button className="close-button" onClick={onExit}>
                        ✖
                    </button>
                </ViewTransition>
            </div>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 300px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .thumbnail.red {
      background-image: conic-gradient(at top right, #c76a15, #a6423a, #2b3491);
    }
    .thumbnail.fullscreen {
      width: 100%;
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
    }
    .fullscreenLayout {
      position: relative;
      height: 100%;
      width: 100%;
    }
    .close-button {
      position: absolute;
      top: 10px;
      right: 10px;
      color: black;
    }
    @keyframes progress-animation {
      from {
        width: 0;
      }
      to {
        width: 100%;
      }
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

!!!note "Примечание"

    Если смонтированная или размонтированная сторона пары находится за пределами области просмотра, пара не образуется. Так элемент не влетает в область просмотра и не вылетает из неё при прокрутке. Вместо этого он обрабатывается как обычный самостоятельный вход или выход.

    Этого не происходит, если один и тот же экземпляр компонента меняет позицию: тогда запускается «update». Такие анимации идут независимо от того, находится ли одна из позиций за пределами области просмотра.

    Есть известный случай: если глубоко вложенный размонтированный `<ViewTransition>` находится внутри области просмотра, а смонтированная сторона — нет, размонтированная сторона анимируется как собственная анимация «exit», даже когда она глубоко вложена, а не как часть анимации родителя.

!!!warning "Подводный камень"

    Во всём приложении одновременно может быть смонтирован только один элемент с одним и тем же именем. Поэтому для имени нужны уникальные пространства имён, чтобы избежать конфликтов. Для этого удобно завести константу в отдельном модуле и импортировать её.

    ```js
    export const MY_NAME = "my-globally-unique-name";
    import {MY_NAME} from './shared-name';
    ...
    <ViewTransition name={MY_NAME}>
    ```

### Анимация перестановки элементов списка {#animating-reorder-of-items-in-a-list}

```js
items.map((item) => <Component key={item.id} item={item} />);
```

При перестановке списка без изменения содержимого анимация «update» запускается на каждом `<ViewTransition>` в списке, если они находятся вне DOM-узла. Это похоже на анимации входа и выхода.

Значит, анимация запустится на таком `<ViewTransition>`:

```js
function Component() {
  return (
    <ViewTransition>
      <div>...</div>
    </ViewTransition>
  );
}
```

=== "Video.js"

    ```js

    function Thumbnail({video}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';

    export default function Component() {
        const [orderedVideos, setOrderedVideos] = useState(videos);
        const reorder = () => {
            startTransition(() => {
                setOrderedVideos((prev) => {
                    return [...prev.sort(() => Math.random() - 0.5)];
                });
            });
        };
        return (
            <>
                <button onClick={reorder}>🎲</button>
                <div className="listContainer">
                    {orderedVideos.map((video, i) => {
                        return (
                            <ViewTransition key={video.title}>
                                <Video video={video} />
                            </ViewTransition>
                        );
                    })}
                </div>
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
        {
            id: '2',
            title: 'Second video',
            description: 'Video description',
            image: 'red',
        },
        {
            id: '3',
            title: 'Third video',
            description: 'Video description',
            image: 'green',
        },
        {
            id: '4',
            title: 'Fourth video',
            description: 'Video description',
            image: 'purple',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 150px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .thumbnail.red {
      background-image: conic-gradient(at top right, #c76a15, #a6423a, #2b3491);
    }
    .thumbnail.green {
      background-image: conic-gradient(at top right, #c76a15, #388f7f, #2b3491);
    }
    .thumbnail.purple {
      background-image: conic-gradient(at top right, #c76a15, #575fb7, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

Однако так каждый отдельный элемент анимироваться не будет:

```js
function Component() {
  return (
    <div>
      <ViewTransition>...</ViewTransition>
    </div>
  );
}
```

Вместо этого любой родительский `<ViewTransition>` выполнит cross-fade. Если родительского `<ViewTransition>` нет, анимации в этом случае не будет.

=== "Video.js"

    ```js

    function Thumbnail({video}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';

    export default function Component() {
        const [orderedVideos, setOrderedVideos] = useState(videos);
        const reorder = () => {
            startTransition(() => {
                setOrderedVideos((prev) => {
                    return [...prev.sort(() => Math.random() - 0.5)];
                });
            });
        };
        return (
            <>
                <button onClick={reorder}>🎲</button>
                <ViewTransition>
                    <div className="listContainer">
                        {orderedVideos.map((video, i) => {
                            return <Video video={video} key={video.title} />;
                        })}
                    </div>
                </ViewTransition>
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
        {
            id: '2',
            title: 'Second video',
            description: 'Video description',
            image: 'red',
        },
        {
            id: '3',
            title: 'Third video',
            description: 'Video description',
            image: 'green',
        },
        {
            id: '4',
            title: 'Fourth video',
            description: 'Video description',
            image: 'purple',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 150px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .thumbnail.red {
      background-image: conic-gradient(at top right, #c76a15, #a6423a, #2b3491);
    }
    .thumbnail.green {
      background-image: conic-gradient(at top right, #c76a15, #388f7f, #2b3491);
    }
    .thumbnail.purple {
      background-image: conic-gradient(at top right, #c76a15, #575fb7, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

Поэтому в списках, где компонент должен сам управлять анимацией перестановки, лучше обходиться без элементов-обёрток:

```
items.map(item => <div><Component key={item.id} item={item} /></div>)
```

То же правило действует, если один из элементов обновляется и меняет размер, из-за чего соседи тоже меняют размер: соседний `<ViewTransition>` тоже анимируется, но только если это непосредственные соседи.

Значит, во время обновления с большой перекомпоновкой React не анимирует каждый `<ViewTransition>` на странице по отдельности. Иначе получилось бы много шумных анимаций, которые отвлекают от самого изменения. Поэтому React осторожнее выбирает, когда запускать отдельную анимацию.

!!!warning "Подводный камень"

    При перестановке списков важно правильно использовать ключи, чтобы сохранять идентичность. Может показаться, что для анимации перестановки подойдут «name» и переходы общего элемента, но они не запустятся, если одна сторона окажется за пределами области просмотра. При анимации перестановки часто как раз нужно показать, что элемент ушёл на позицию за пределами области просмотра.

### Анимация при появлении содержимого Suspense {#animating-from-suspense-content}

Как и любой переход, React ждёт данные и новый CSS (`<link rel="stylesheet" precedence="...">`), прежде чем запустить анимацию. Кроме того, ViewTransition ждёт до 500 мс загрузки новых шрифтов, прежде чем начать анимацию, чтобы они не мигнули позже. По той же причине изображение внутри ViewTransition дождётся загрузки этого изображения. Примеры [ожидания шрифта](Suspense.md#waiting-for-a-font-to-load) и [ожидания изображения](Suspense.md#waiting-for-an-image-to-load) есть на странице Suspense.

Если это происходит внутри нового экземпляра границы приостановки, сначала показывается фолбэк. Когда граница приостановки полностью загрузится, она запускает `<ViewTransition>`, чтобы анимировать появление содержимого.

Границы приостановки можно анимировать двумя способами в зависимости от того, куда поместить `<ViewTransition>`:

**Обновление:**

```
<ViewTransition>
  <Suspense fallback={<A />}>
    <B />
  </Suspense>
</ViewTransition>
```

В этом сценарии, когда содержимое переходит от A к B, это считается «update», и при необходимости применяется соответствующий класс. И A, и B получают одно и то же view-transition-name, поэтому по умолчанию они работают как cross-fade.

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }

    export function VideoPlaceholder() {
        const video = {image: 'loading'};
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title loading" />
                        <div className="video-description loading" />
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition, Suspense} from 'react';
    import {Video, VideoPlaceholder} from './Video';
    import {useLazyVideoData} from './data';

    function LazyVideo() {
        const video = useLazyVideoData();
        return <Video video={video} />;
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>
                {showItem ? (
                    <ViewTransition>
                        <Suspense fallback={<VideoPlaceholder />}>
                            <LazyVideo />
                        </Suspense>
                    </ViewTransition>
                ) : null}
            </>
        );
    }
    ```

=== "data.js"

    ```js

    import {use} from 'react';

    let cache = null;

    function fetchVideo() {
        if (!cache) {
            cache = new Promise((resolve) => {
                setTimeout(() => {
                    resolve({
                        id: '1',
                        title: 'First video',
                        description: 'Video description',
                        image: 'blue',
                    });
                }, 1000);
            });
        }
        return cache;
    }

    export function useLazyVideoData() {
        return use(fetchVideo());
    }
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .loading {
      background-image: linear-gradient(
        90deg,
        rgba(173, 216, 230, 0.3) 25%,
        rgba(135, 206, 250, 0.5) 50%,
        rgba(173, 216, 230, 0.3) 75%
      );
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }
    @keyframes shimmer {
      0% {
        background-position: -200% 0;
      }
      100% {
        background-position: 200% 0;
      }
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-title.loading {
      height: 20px;
      width: 80px;
      border-radius: 0.5rem;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
      border-radius: 0.5rem;
    }
    .video-description.loading {
      height: 15px;
      width: 100px;
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

**Вход и выход:**

```
<Suspense fallback={<ViewTransition><A /></ViewTransition>}>
  <ViewTransition><B /></ViewTransition>
</Suspense>
```

В этом сценарии это два отдельных экземпляра ViewTransition, у каждого свой `view-transition-name`. Это «exit» для `<A>` и «enter» для `<B>`.

Разные эффекты получаются в зависимости от того, где размещена граница `<ViewTransition>`.

### Отказ от анимации {#opting-out-of-an-animation}

Иногда вы оборачиваете большой существующий компонент, например целую страницу, и хотите анимировать отдельные обновления, такие как смена темы. При этом все обновления внутри страницы не должны сами включаться в cross-fade. Это особенно важно, когда анимации добавляются постепенно.

Чтобы отказаться от анимации, используйте класс «none». Если обернуть дочерние элементы в «none», анимации их обновлений отключаются, а родитель по-прежнему запускается.

```js
<ViewTransition>
  <div className={theme}>
    <ViewTransition update="none">{children}</ViewTransition>
  </div>
</ViewTransition>
```

Анимация произойдёт только при смене темы. Обновление одних дочерних элементов её не запустит. Дочерние элементы по-прежнему могут включиться снова через собственный `<ViewTransition>`, но это уже делается вручную.

### Настройка анимаций {#customizing-animations}

По умолчанию `<ViewTransition>` использует стандартное перекрёстное затухание (cross-fade) браузера.

Чтобы настроить анимации, передайте пропсы компоненту `<ViewTransition>` и укажите, какие анимации использовать, в зависимости от того, как активируется `<ViewTransition>`.

Например, стандартную анимацию cross-fade можно замедлить:

```js
<ViewTransition default="slow-fade">
  <Video />
</ViewTransition>
```

И задать slow-fade в CSS с помощью классов перехода вида:

```css
::view-transition-old(.slow-fade) {
  animation-duration: 500ms;
}

::view-transition-new(.slow-fade) {
  animation-duration: 500ms;
}
```

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>

                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';

    function Item() {
        return (
            <ViewTransition default="slow-fade">
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>

                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    ::view-transition-old(.slow-fade) {
      animation-duration: 500ms;
    }

    ::view-transition-new(.slow-fade) {
      animation-duration: 500ms;
    }

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

Помимо `default` можно задать настройки для анимаций `enter`, `exit`, `update` и `share`.

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>

                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';

    function Item() {
        return (
            <ViewTransition enter="slide-in" exit="slide-out">
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>

                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    ::view-transition-old(.slide-in) {
      animation-name: slideOutRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-in) {
      animation-name: slideInRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-old(.slide-out) {
      animation-name: slideOutLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-out) {
      animation-name: slideInLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    @keyframes slideOutLeft {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(-100%);
        opacity: 0;
      }
    }

    @keyframes slideInLeft {
      from {
        transform: translateX(-100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }

    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

### Настройка анимаций с помощью типов {#customizing-animations-with-types}

С помощью API [`addTransitionType`](addTransitionType.md) можно добавить имя класса дочерним элементам, когда для определённого триггера активации включается определённый тип перехода. Так анимацию можно настроить для каждого типа перехода.

Например, чтобы настроить анимацию всех переходов вперёд и назад:

```js
<ViewTransition
  default={{
    'navigation-back': 'slide-right',
    'navigation-forward': 'slide-left',
  }}>
  <div>...</div>
</ViewTransition>;

// in your router:
startTransition(() => {
  addTransitionType('navigation-' + navigationType);
});
```

Когда ViewTransition активирует анимацию «navigation-back», React добавит класс «slide-right». Когда ViewTransition активирует анимацию «navigation-forward», React добавит класс «slide-left».

В будущем маршрутизаторы и другие библиотеки могут добавить поддержку стандартных типов и стилей view-transition.

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>
                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {
        ViewTransition,
        addTransitionType,
        useState,
        startTransition,
    } from 'react';
    import {Video} from './Video';
    import videos from './data';

    function Item() {
        return (
            <ViewTransition
                enter={{
                    'add-video-back': 'slide-in-back',
                    'add-video-forward': 'slide-in-forward',
                }}
                exit={{
                    'remove-video-back': 'slide-in-forward',
                    'remove-video-forward': 'slide-in-back',
                }}>
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <div className="button-container">
                    <button
                        onClick={() => {
                            startTransition(() => {
                                if (showItem) {
                                    addTransitionType('remove-video-back');
                                } else {
                                    addTransitionType('add-video-back');
                                }
                                setShowItem((prev) => !prev);
                            });
                        }}>
                        ⬅️
                    </button>
                    <button
                        onClick={() => {
                            startTransition(() => {
                                if (showItem) {
                                    addTransitionType('remove-video-forward');
                                } else {
                                    addTransitionType('add-video-forward');
                                }
                                setShowItem((prev) => !prev);
                            });
                        }}>
                        ➡️
                    </button>
                </div>
                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    ::view-transition-old(.slide-in-back) {
      animation-name: slideOutRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-in-back) {
      animation-name: slideInRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-old(.slide-out-back) {
      animation-name: slideOutLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-out-back) {
      animation-name: slideInLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-old(.slide-in-forward) {
      animation-name: slideOutLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-in-forward) {
      animation-name: slideInLeft;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-old(.slide-out-forward) {
      animation-name: slideOutRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    ::view-transition-new(.slide-out-forward) {
      animation-name: slideInRight;
      animation-duration: 500ms;
      animation-timing-function: ease-in-out;
    }

    @keyframes slideOutLeft {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(-100%);
        opacity: 0;
      }
    }

    @keyframes slideInLeft {
      from {
        transform: translateX(-100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }

    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .button-container {
      display: flex;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

### Анимация на JavaScript {#animating-with-javascript}

[Классы перехода вида](#view-transition-class) задают анимации в CSS, но иногда нужен императивный контроль. Колбэки `onEnter`, `onExit`, `onUpdate` и `onShare` дают прямой доступ к псевдоэлементам перехода вида, чтобы анимировать их через [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API).

Каждый колбэк получает `instance` со свойствами `.old` и `.new` — это псевдоэлементы перехода вида. На них можно вызвать `.animate()` так же, как на DOM-элементе:

```js
<ViewTransition
  onEnter={(instance) => {
    const anim = instance.new.animate(
      [
        {transform: 'scale(0.8)'},
        {transform: 'scale(1)'},
      ],
      {duration: 300, easing: 'ease-out'}
    );
    return () => anim.cancel();
  }}>
  <div>...</div>
</ViewTransition>
```

Так можно сочетать анимации на CSS и анимации на JavaScript.

В следующем примере стандартный cross-fade задаётся в CSS, а анимации скольжения — на JavaScript в `onEnter` и `onExit`:

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>

                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition} from 'react';
    import {Video} from './Video';
    import videos from './data';
    import {SLIDE_IN, SLIDE_OUT} from './animations';

    function Item() {
        return (
            <ViewTransition
                default="none"
                /* CSS driven cross fade defaults */
                enter="auto"
                exit="auto"
                /* JS driven slide animations */
                onEnter={(instance) => {
                    const anim = instance.new.animate(
                        SLIDE_IN,
                        {duration: 500, easing: 'ease-out'}
                    );
                    return () => anim.cancel();
                }}
                onExit={(instance) => {
                    const anim = instance.old.animate(
                        SLIDE_OUT,
                        {duration: 300, easing: 'ease-in'}
                    );
                    return () => anim.cancel();
                }}>
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>

                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "animations.js"

    ```js

    export const SLIDE_IN = [
        {transform: 'translateY(20px)'},
        {transform: 'translateY(0)'},
    ];

    export const SLIDE_OUT = [
        {transform: 'translateY(0)'},
        {transform: 'translateY(-20px)'},
    ];
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

!!!note "Всегда очищайте события перехода вида"

    События перехода вида всегда должны возвращать функцию очистки:

    ```js hl_lines="7"
    <ViewTransition
      onEnter={(instance) => {
        const anim = instance.new.animate(
          SLIDE_IN,
          {duration: 500, easing: 'ease-out'}
        );
        return () => anim.cancel();
      }}
    >
    ```

    Так браузер может отменить анимацию, когда переход вида прерывается.

### Анимация типов перехода на JavaScript {#animating-transition-types-with-javascript}

Через `types`, которые приходят в события `ViewTransition`, можно по-разному анимировать в зависимости от того, как был запущен переход.

```js hl_lines="3"
 <ViewTransition
  onEnter={(instance, types) => {
    const duration = types.includes('fast') ? 150 : 2000;
    const anim = instance.new.animate(
      SLIDE_IN,
      {duration: duration, easing: 'ease-out'}
    );
    return () => anim.cancel();
  }}
>
```

В этом примере вызывается [`addTransitionType`](addTransitionType.md), чтобы пометить переход как «fast», а затем изменить длительность анимации:

=== "Video.js"

    ```js

    function Thumbnail({video, children}) {
        return (
            <div
                aria-hidden="true"
                tabIndex={-1}
                className={`thumbnail ${video.image}`}
            />
        );
    }

    export function Video({video}) {
        return (
            <div className="video">
                <div className="link">
                    <Thumbnail video={video}></Thumbnail>

                    <div className="info">
                        <div className="video-title">{video.title}</div>
                        <div className="video-description">{video.description}</div>
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "js"

    ```js

    import {ViewTransition, useState, startTransition, addTransitionType} from 'react';
    import {Video} from './Video';
    import videos from './data';
    import {SLIDE_IN, SLIDE_OUT} from './animations';

    function Item() {
        return (
            <ViewTransition
                onEnter={(instance, types) => {
                    const duration = types.includes('fast') ? 150 : 2000;
                    const anim = instance.new.animate(
                        SLIDE_IN,
                        {duration: duration, easing: 'ease-out'}
                    );
                    return () => anim.cancel();
                }}
                onExit={(instance, types) => {
                    const duration = types.includes('fast') ? 150 : 500;
                    const anim = instance.old.animate(
                        SLIDE_OUT,
                        {duration: duration, easing: 'ease-in'}
                    );
                    return () => anim.cancel();
                }}>
                <Video video={videos[0]} />
            </ViewTransition>
        );
    }

    export default function Component() {
        const [showItem, setShowItem] = useState(false);
        const [isFast, setIsFast] = useState(false);
        return (
            <>
                <div>
                    Fast: <input type="checkbox" onChange={() => {setIsFast(f => !f)}} value={isFast}></input>
                </div><br />
                <button
                    onClick={() => {
                        startTransition(() => {
                            if (isFast) {
                                addTransitionType('fast');
                            }
                            setShowItem((prev) => !prev);
                        });
                    }}>
                    {showItem ? '➖' : '➕'}
                </button>

                {showItem ? <Item /> : null}
            </>
        );
    }
    ```

=== "animations.js"

    ```js

    export const SLIDE_IN = [
        {opacity: 0, transform: 'translateY(20px)'},
        {opacity: 1, transform: 'translateY(0)'},
    ];

    export const SLIDE_OUT = [
        {opacity: 1, transform: 'translateY(0)'},
        {opacity: 0, transform: 'translateY(-20px)'},
    ];
    ```

=== "data.js"

    ```js

    export default [
        {
            id: '1',
            title: 'First video',
            description: 'Video description',
            image: 'blue',
        },
    ];
    ```

=== "styles.css"

    ```css

    #root {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 200px;
    }
    button {
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f8ff;
      color: white;
      font-size: 20px;
      cursor: pointer;
      transition: background-color 0.3s, border 0.3s;
    }
    button:hover {
      border: 2px solid #ccc;
      background-color: #e0e8ff;
    }
    .thumbnail {
      position: relative;
      aspect-ratio: 16 / 9;
      display: flex;
      overflow: hidden;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 0.5rem;
      outline-offset: 2px;
      width: 8rem;
      vertical-align: middle;
      background-color: #ffffff;
      background-size: cover;
      user-select: none;
    }
    .thumbnail.blue {
      background-image: conic-gradient(at top right, #c76a15, #087ea4, #2b3491);
    }
    .video {
      display: flex;
      flex-direction: row;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1em;
    }
    .video .link {
      display: flex;
      flex-direction: row;
      flex: 1 1 0;
      gap: 0.125rem;
      outline-offset: 4px;
      cursor: pointer;
    }
    .video .info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin-left: 8px;
      gap: 0.125rem;
    }
    .video .info:hover {
      text-decoration: underline;
    }
    .video-title {
      font-size: 15px;
      line-height: 1.25;
      font-weight: 700;
      color: #23272f;
    }
    .video-description {
      color: #5e687e;
      font-size: 13px;
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

### Маршрутизаторы с поддержкой перехода вида {#building-view-transition-enabled-routers}

React ждёт завершения любой ожидающей навигации (Navigation), чтобы восстановление прокрутки произошло внутри анимации. Если навигация заблокирована на React, маршрутизатор должен снять блокировку в `useLayoutEffect`: `useEffect` приведёт к взаимной блокировке.

Если `startTransition` запущен из устаревшего события popstate, например при навигации «назад», он должен завершиться синхронно, чтобы правильно восстановились прокрутка и форма. Это конфликтует с анимацией перехода вида. Поэтому React пропускает анимации из popstate, и для кнопки «Назад» они не выполняются. Исправление — обновить маршрутизатор до Navigation API.

## Устранение неполадок {#troubleshooting}

### Мой `&lt;ViewTransition&gt;` не активируется {#my-viewtransition-is-not-activating}

`<ViewTransition>` активируется, только если расположен до любого DOM-узла:

```js hl_lines="3 5"
function Component() {
  return (
    <div>
      <ViewTransition>Hi</ViewTransition>
    </div>
  );
}
```

Чтобы это исправить, `<ViewTransition>` должен идти раньше любых других DOM-узлов:

```js hl_lines="3 5"
function Component() {
  return (
    <ViewTransition>
      <div>Hi</div>
    </ViewTransition>
  );
}
```

### Ошибка «There are two `&lt;ViewTransition name=%s&gt;` components with the same name mounted at the same time.» {#two-viewtransition-with-same-name}

Эта ошибка возникает, когда одновременно смонтированы два компонента `<ViewTransition>` с одним и тем же `name`:

```js hl_lines="3"
function Item() {
  // 🚩 All items will get the same "name".
  return <ViewTransition name="item">...</ViewTransition>;
}

function ItemList({items}) {
  return (
    <>
      {items.map((item) => (
        <Item key={item.id} />
      ))}
    </>
  );
}
```

Из-за этого переход вида завершится ошибкой. В режиме разработки React обнаруживает проблему, чтобы показать её, и пишет в журнал две ошибки:

```text linenums="0"
<ConsoleLogLine level="error">

There are two `<ViewTransition name=%s>` components with the same name mounted at the same time. This is not supported and will cause View Transitions to error. Try to use a more unique name e.g. by using a namespace prefix and adding the id of an item to the name.
{' '}at Item
{' '}at ItemList

</ConsoleLogLine>

<ConsoleLogLine level="error">

The existing `<ViewTransition name=%s>` duplicate has this stack trace.
{' '}at Item
{' '}at ItemList

</ConsoleLogLine>
```

Чтобы это исправить, во всём приложении одновременно должен быть смонтирован только один `<ViewTransition>` с таким именем: сделайте `name` уникальным или добавьте к имени `id`:

```js hl_lines="3"
function Item({id}) {
  // ✅ All items will get a unique name.
  return <ViewTransition name={`item-${id}`}>...</ViewTransition>;
}

function ItemList({items}) {
  return (
    <>
      {items.map((item) => (
        <Item key={item.id} item={item} />
      ))}
    </>
  );
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/ViewTransition](https://react.dev/reference/react/ViewTransition)</small>
