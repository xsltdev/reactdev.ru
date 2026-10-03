---
description: Suspense позволяет отображать фалбэк до тех пор, пока его дочерние элементы не закончат загрузку
---

# Suspense

<big>`<Suspense>` позволяет отображать фалбэк до тех пор, пока его дочерние элементы не закончат загрузку.</big>

```js
<Suspense fallback={<Loading />}>
    <SomeComponent />
</Suspense>
```

## Описание {#reference}

### `<Suspense>` {#suspense}

#### Свойства {#props}

-   `children`: Фактический пользовательский интерфейс, который вы собираетесь рендерить. Если `children` приостановится во время рендеринга, граница Suspense переключится на рендеринг `fallback`.
-   `fallback`: Альтернативный пользовательский интерфейс, который будет отображаться вместо реального пользовательского интерфейса, если он не закончил загрузку. Принимается любой допустимый узел React, хотя на практике запасной вариант - это легковесное представление-заполнитель, например, загрузочный спиннер или скелет. Приостановка будет автоматически переключаться на `fallback`, когда `children` приостанавливает работу, и обратно на `children`, когда данные будут готовы. Если `fallback` приостанавливает работу во время рендеринга, он активирует ближайшую родительскую границу Suspense.

#### Ограничения {#caveats}

-   React не сохраняет состояние для рендеров, которые были приостановлены до того, как они смогли смонтироваться в первый раз. Когда компонент загрузится, React повторит попытку рендеринга приостановленного дерева с нуля.
-   Если `Suspense` отображал содержимое для дерева, но затем снова приостановился, то `откат` будет показан снова, если только обновление, вызвавшее его, не было вызвано [`startTransition`](startTransition.md) или [`useDeferredValue`](useDeferredValue.md).
-   Если React необходимо скрыть уже видимый контент из-за повторного приостановления, он очистит [layout Effects](useLayoutEffect.md) в дереве контента. Когда контент снова будет готов к показу, React снова запустит Эффекты компоновки. Это гарантирует, что Эффекты, измеряющие макет DOM, не попытаются сделать это, пока содержимое скрыто.
-   React включает в себя такие "подкапотные" оптимизации, как _Streaming Server Rendering_ и _Selective Hydration_, которые интегрированы в `Suspense`. Чтобы узнать больше, прочитайте [архитектурный обзор](https://github.com/reactwg/react-18/discussions/37) и посмотрите [технический доклад](https://www.youtube.com/watch?v=pj5N-Khihgc).

### Что активирует границу Suspense {#what-activates-a-suspense-boundary}

Граница Suspense ждёт, пока содержимое будет готово, и только потом показывает его. Граница не раскрывает содержимое, пока происходит что-то из этого списка:

-   Ленивая загрузка кода компонента через [`lazy`](lazy.md).
-   Чтение промиса через [`use`](use.md), включая данные, которые приходят потоком из [серверных компонентов](../rsc/server-components.md) или загружаются через [фреймворк с поддержкой Suspense](#suspense-enabled-frameworks).
-   Загрузка таблицы стилей, отрисованной через [`<link rel="stylesheet">` с пропом `precedence`](../react-dom/components/link.md#special-rendering-behavior). React удерживает границу, пока таблица стилей не загрузится, но не дольше тайм-аута. [Пример ниже.](#waiting-for-a-stylesheet-to-load)
-   Ожидание HTML большой границы при потоковом серверном рендеринге. Передача HTML занимает время, поэтому граница с достаточным объёмом содержимого активируется, даже если внутри ничего не приостанавливается. React показывает содержимое по мере поступления HTML.
-   Загрузка шрифтов. По умолчанию Suspense не ждёт шрифты, но обновление [`<ViewTransition>`](ViewTransition.md) ждёт загрузки новых шрифтов до тайм-аута, чтобы текст не мигал запасным шрифтом. [Пример ниже.](#waiting-for-a-font-to-load)
-   Загрузка изображений. По умолчанию Suspense не ждёт изображения, но во время обновления [`<ViewTransition>`](ViewTransition.md) React удерживает границу, пока изображение не загрузится, до тайм-аута. Обработчик `onLoad` исключает конкретное изображение из этого ожидания. [Пример ниже.](#waiting-for-an-image-to-load)
-   Вычисления, которые занимают процессор, внутри границы [`<Suspense defer>`](#props).

<a id="suspense-enabled-frameworks"></a>

!!!note "Фреймворки с поддержкой Suspense"

    _Фреймворк с поддержкой Suspense_ даёт способ читать данные в компоненте так, чтобы активировалась ближайшая граница Suspense. Точный способ загрузки зависит от фреймворка и описан в его документации. Под капотом такой фреймворк хранит кэш промисов и вызывает [`use`](use.md), чтобы приостановиться на промисе.

    Без фреймворка промис можно читать через `use` напрямую, если промис [закэширован и один и тот же экземпляр переиспользуется между рендерами.](use.md#caching-promises-for-client-components)

## Использование {#usage}

### Отображение фолбэка во время загрузки контента {#displaying-a-fallback-while-content-is-loading}

Вы можете обернуть любую часть вашего приложения границей `Suspense`:

```js
<Suspense fallback={<Loading />}>
    <Albums />
</Suspense>
```

React будет отображать ваш loading fallback до тех пор, пока весь код и данные, необходимые потомкам не будут загружены.

В приведенном ниже примере компонент `Albums` _приостанавливается_ на время получения списка альбомов. Пока он не готов к рендерингу, React переключает ближайшую границу Suspense выше, чтобы показать отступающий компонент - ваш компонент `Loading`. Затем, когда данные загружаются, React скрывает компонент `Loading` и отображает компонент `Albums` с данными.

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Suspense fallback={<Loading />}>
    				<Albums artistId={artist.id} />
    			</Suspense>
    		</>
    	);
    }

    function Loading() {
    	return <h2>🌀 Loading...</h2>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/7hzg5z?view=Editor+%2B+Preview&module=%2Fsrc%2FArtistPage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="restless-waterfall-7hzg5z" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Поддержка Suspense"

    **Только источники данных с поддержкой Suspense активируют компонент Suspense.** К ним относятся:

    -   Получение данных с помощью фреймворков с поддержкой Suspense, таких как [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) и [Next.js](https://nextjs.org/docs/getting-started/react-essentials).
    -   Ленивая загрузка кода компонента с помощью [`lazy`](lazy.md).
    -   Считывание значения промиса с использованием [`use`](use.md)

    Suspense **не** обнаруживает, когда данные извлекаются внутри Effect или обработчика события.

    Точный способ загрузки данных в компонент `Albums`, описанный выше, зависит от вашего фреймворка. Если вы используете фреймворк с поддержкой Suspense, вы найдете подробности в документации по получению данных.

    Получение данных с поддержкой Suspense без использования мнений фреймворка пока не поддерживается. Требования к реализации источника данных с поддержкой Suspense нестабильны и не документированы. Официальный API для интеграции источников данных с Suspense будет выпущен в одной из будущих версий React.

### Раскрытие содержимого сразу {#revealing-content-together-at-once}

По умолчанию все дерево внутри Suspense рассматривается как единое целое. Например, даже если _только один_ из этих компонентов приостановится в ожидании каких-то данных, _все_ они вместе будут заменены индикатором загрузки:

```js hl_lines="2-5"
<Suspense fallback={<Loading />}>
    <Biography />
    <Panel>
        <Albums />
    </Panel>
</Suspense>
```

Затем, когда все они будут готовы к отображению, они появятся все вместе одновременно.

В приведенном ниже примере и `Biography`, и `Albums` получают некоторые данные. Однако, поскольку они сгруппированы под одной границей Suspense, эти компоненты всегда "всплывают" вместе в одно и то же время.

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';
    import Biography from './Biography.js';
    import Panel from './Panel.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Suspense fallback={<Loading />}>
    				<Biography artistId={artist.id} />
    				<Panel>
    					<Albums artistId={artist.id} />
    				</Panel>
    			</Suspense>
    		</>
    	);
    }

    function Loading() {
    	return <h2>🌀 Loading...</h2>;
    }
    ```

=== "Panel.js"

    ```js
    export default function Panel({ children }) {
    	return <section className="panel">{children}</section>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6j7nnj?view=Editor+%2B+Preview&module=%2Fsrc%2FArtistPage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="strange-black-6j7nnj" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Компоненты, загружающие данные, не обязательно должны быть прямыми дочерними компонентами границы Suspense. Например, вы можете переместить `Biography` и `Albums` в новый компонент `Details`. Это не изменит поведение. `Biography` и `Albums` имеют одну и ту же ближайшую родительскую границу Suspense, поэтому их раскрытие координируется вместе.

```js hl_lines="2 8-11"
<Suspense fallback={<Loading />}>
    <Details artistId={artist.id} />
</Suspense>;

function Details({ artistId }) {
    return (
        <>
            <Biography artistId={artistId} />
            <Panel>
                <Albums artistId={artistId} />
            </Panel>
        </>
    );
}
```

### Раскрытие вложенного содержимого по мере загрузки {#revealing-nested-content-as-it-loads}

Когда компонент приостанавливается, ближайший родительский Suspense-компонент показывает запасной вариант. Это позволяет вложить несколько компонентов Suspense для создания последовательности загрузки. Падение каждой границы Suspense будет заполняться по мере того, как становится доступным содержимое следующего уровня. Например, вы можете дать списку альбомов свой собственный откат:

```js hl_lines="3 7"
<Suspense fallback={<BigSpinner />}>
    <Biography />
    <Suspense fallback={<AlbumsGlimmer />}>
        <Panel>
            <Albums />
        </Panel>
    </Suspense>
</Suspense>
```

С этим изменением отображение `Biography` не должно "ждать" загрузки `Albums`.

Последовательность будет следующей:

1.  Если `Biography` еще не загрузилась, `BigSpinner` отображается вместо всей области содержимого.
2.  Как только `Biography` завершает загрузку, `BigSpinner` заменяется содержимым.
3.  Если `Albums` еще не загрузились, `AlbumsGlimmer` отображается вместо `Albums` и его родительской `Panel`.
4.  Наконец, когда `Albums` завершает загрузку, он заменяет `AlbumsGlimmer`.

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';
    import Biography from './Biography.js';
    import Panel from './Panel.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Suspense fallback={<BigSpinner />}>
    				<Biography artistId={artist.id} />
    				<Suspense fallback={<AlbumsGlimmer />}>
    					<Panel>
    						<Albums artistId={artist.id} />
    					</Panel>
    				</Suspense>
    			</Suspense>
    		</>
    	);
    }

    function BigSpinner() {
    	return <h2>🌀 Loading...</h2>;
    }

    function AlbumsGlimmer() {
    	return (
    		<div className="glimmer-panel">
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    		</div>
    	);
    }
    ```

=== "Panel.js"

    ```js
    export default function Panel({ children }) {
    	return <section className="panel">{children}</section>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/4sp9wt?view=Editor+%2B+Preview&module=%2Fsrc%2FArtistPage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="red-architecture-4sp9wt" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Приостановочные границы позволяют вам координировать, какие части пользовательского интерфейса должны всегда "всплывать" одновременно, а какие - постепенно раскрывать больше содержимого в последовательности состояний загрузки. Вы можете добавлять, перемещать или удалять Suspense-границы в любом месте дерева, не влияя на поведение остального приложения.

Не ставьте приостанавливающую границу вокруг каждого компонента. Границы приостановки не должны быть более детализированными, чем последовательность загрузки, которую вы хотите, чтобы испытал пользователь. Если вы работаете с дизайнером, спросите его, где должны располагаться состояния загрузки - скорее всего, они уже включили их в свои эскизы.

### Показ устаревшего контента во время загрузки свежего {#showing-stale-content-while-fresh-content-is-loading}

В этом примере компонент `SearchResults` приостанавливается на время получения результатов поиска. Введите `"a"`, дождитесь результатов, а затем измените его на `"ab"`. Результаты для `"a"` будут заменены загрузочным фалбэком.

=== "App.js"

    ```js
    import { Suspense, useState } from 'react';
    import SearchResults from './SearchResults.js';

    export default function App() {
    	const [query, setQuery] = useState('');
    	return (
    		<>
    			<label>
    				Search albums:
    				<input
    					value={query}
    					onChange={(e) =>
    						setQuery(e.target.value)
    					}
    				/>
    			</label>
    			<Suspense fallback={<h2>Loading...</h2>}>
    				<SearchResults query={query} />
    			</Suspense>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/mm976s?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="wild-framework-mm976s" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Распространенным альтернативным шаблоном пользовательского интерфейса является _отложенное_ обновление списка и отображение предыдущих результатов до тех пор, пока не будут готовы новые результаты. Хук [`useDeferredValue`](useDeferredValue.md) позволяет вам передать отложенную версию запроса вниз:

```js hl_lines="3 16"
export default function App() {
    const [query, setQuery] = useState('');
    const deferredQuery = useDeferredValue(query);
    return (
        <>
            <label>
                Search albums:
                <input
                    value={query}
                    onChange={(e) =>
                        setQuery(e.target.value)
                    }
                />
            </label>
            <Suspense fallback={<h2>Loading...</h2>}>
                <SearchResults query={deferredQuery} />
            </Suspense>
        </>
    );
}
```

Запрос `query` будет обновлен немедленно, поэтому на входе будет отображаться новое значение. Однако `deferredQuery` сохранит свое предыдущее значение до тех пор, пока данные не загрузятся, поэтому `SearchResults` будет отображать устаревшие результаты некоторое время.

Чтобы сделать это более очевидным для пользователя, вы можете добавить визуальную индикацию, когда отображается список несвежих результатов:

```js hl_lines="3"
<div
    style={{
        opacity: query !== deferredQuery ? 0.5 : 1,
    }}
>
    <SearchResults query={deferredQuery} />
</div>
```

Введите `"a"` в примере ниже, дождитесь загрузки результатов, а затем измените ввод на `"ab"`. Обратите внимание, что вместо отката на приостановку вы теперь видите затемненный список несвежих результатов, пока не загрузятся новые результаты:

=== "App.js"

    ```js
    import {
    	Suspense,
    	useState,
    	useDeferredValue,
    } from 'react';
    import SearchResults from './SearchResults.js';

    export default function App() {
    	const [query, setQuery] = useState('');
    	const deferredQuery = useDeferredValue(query);
    	const isStale = query !== deferredQuery;
    	return (
    		<>
    			<label>
    				Search albums:
    				<input
    					value={query}
    					onChange={(e) =>
    						setQuery(e.target.value)
    					}
    				/>
    			</label>
    			<Suspense fallback={<h2>Loading...</h2>}>
    				<div style={{ opacity: isStale ? 0.5 : 1 }}>
    					<SearchResults query={deferredQuery} />
    				</div>
    			</Suspense>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/k78jlv?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="nervous-dirac-k78jlv" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note ""

    И отложенные значения, и transitions позволяют вам избежать отображения Suspense fallback в пользу встроенных индикаторов. Переходы помечают все обновление как несрочное, поэтому они обычно используются фреймворками и библиотеками маршрутизаторов для навигации. Отложенные значения, с другой стороны, в основном полезны в коде приложений, где вы хотите пометить часть пользовательского интерфейса как несрочную и позволить ей "отстать" от остальной части пользовательского интерфейса.

### Предотвращение скрытия уже раскрытого содержимого {#preventing-already-revealed-content-from-hiding}

Когда компонент приостанавливается, ближайшая родительская граница приостановки переключается на отображение резервного копирования. Это может привести к искажению пользовательского опыта, если уже отображалось какое-то содержимое. Попробуйте нажать эту кнопку:

=== "App.js"

    ```js
    import { Suspense, useState } from 'react';
    import IndexPage from './IndexPage.js';
    import ArtistPage from './ArtistPage.js';
    import Layout from './Layout.js';

    export default function App() {
    	return (
    		<Suspense fallback={<BigSpinner />}>
    			<Router />
    		</Suspense>
    	);
    }

    function Router() {
    	const [page, setPage] = useState('/');

    	function navigate(url) {
    		setPage(url);
    	}

    	let content;
    	if (page === '/') {
    		content = <IndexPage navigate={navigate} />;
    	} else if (page === '/the-beatles') {
    		content = (
    			<ArtistPage
    				artist={{
    					id: 'the-beatles',
    					name: 'The Beatles',
    				}}
    			/>
    		);
    	}
    	return <Layout>{content}</Layout>;
    }

    function BigSpinner() {
    	return <h2>🌀 Loading...</h2>;
    }
    ```

=== "Layout.js"

    ```js
    export default function Layout({ children }) {
    	return (
    		<div className="layout">
    			<section className="header">
    				Music Browser
    			</section>
    			<main>{children}</main>
    		</div>
    	);
    }
    ```

=== "IndexPage.js"

    ```js
    export default function IndexPage({ navigate }) {
    	return (
    		<button onClick={() => navigate('/the-beatles')}>
    			Open The Beatles artist page
    		</button>
    	);
    }
    ```

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';
    import Biography from './Biography.js';
    import Panel from './Panel.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Biography artistId={artist.id} />
    			<Suspense fallback={<AlbumsGlimmer />}>
    				<Panel>
    					<Albums artistId={artist.id} />
    				</Panel>
    			</Suspense>
    		</>
    	);
    }

    function AlbumsGlimmer() {
    	return (
    		<div className="glimmer-panel">
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6mr49s?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="thirsty-wildflower-6mr49s" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

При нажатии кнопки компонент `Router` отображал `ArtistPage` вместо `IndexPage`. Компонент внутри `ArtistPage` приостанавливался, поэтому ближайшая граница Suspense начинала показывать откат. Ближайшая Suspense-граница находилась рядом с корнем, поэтому весь макет сайта заменялся на `BigSpinner`.

Чтобы предотвратить это, вы можете пометить обновление состояния навигации как _переход_ с помощью [`startTransition`:](startTransition.md)

```js hl_lines="5 7"
function Router() {
    const [page, setPage] = useState('/');

    function navigate(url) {
        startTransition(() => {
            setPage(url);
        });
    }
    // ...
}
```

Это говорит React, что переход состояния не является срочным, и лучше продолжать показывать предыдущую страницу вместо того, чтобы скрывать уже открытое содержимое. Теперь нажатие на кнопку "ждет" загрузки `Биографии`:

=== "App.js"

    ```js
    import { Suspense, startTransition, useState } from 'react';
    import IndexPage from './IndexPage.js';
    import ArtistPage from './ArtistPage.js';
    import Layout from './Layout.js';

    export default function App() {
    	return (
    		<Suspense fallback={<BigSpinner />}>
    			<Router />
    		</Suspense>
    	);
    }

    function Router() {
    	const [page, setPage] = useState('/');

    	function navigate(url) {
    		startTransition(() => {
    			setPage(url);
    		});
    	}

    	let content;
    	if (page === '/') {
    		content = <IndexPage navigate={navigate} />;
    	} else if (page === '/the-beatles') {
    		content = (
    			<ArtistPage
    				artist={{
    					id: 'the-beatles',
    					name: 'The Beatles',
    				}}
    			/>
    		);
    	}
    	return <Layout>{content}</Layout>;
    }

    function BigSpinner() {
    	return <h2>🌀 Loading...</h2>;
    }
    ```

=== "Layout.js"

    ```js
    export default function Layout({ children }) {
    	return (
    		<div className="layout">
    			<section className="header">
    				Music Browser
    			</section>
    			<main>{children}</main>
    		</div>
    	);
    }
    ```

=== "IndexPage.js"

    ```js
    export default function IndexPage({ navigate }) {
    	return (
    		<button onClick={() => navigate('/the-beatles')}>
    			Open The Beatles artist page
    		</button>
    	);
    }
    ```

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';
    import Biography from './Biography.js';
    import Panel from './Panel.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Biography artistId={artist.id} />
    			<Suspense fallback={<AlbumsGlimmer />}>
    				<Panel>
    					<Albums artistId={artist.id} />
    				</Panel>
    			</Suspense>
    		</>
    	);
    }

    function AlbumsGlimmer() {
    	return (
    		<div className="glimmer-panel">
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xcmgz2?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="hidden-dust-xcmgz2" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Переход не ждет, пока загрузится _все_ содержимое. Он ждет только достаточно долго, чтобы не скрыть уже открытое содержимое. Например, сайт `Layout` уже был показан, поэтому было бы плохо скрывать его за загружающимся волчком. Однако вложенная граница `Suspense` вокруг `Albums` является новой, поэтому переход не ждет ее.

!!!note ""

    Ожидается, что маршрутизаторы с поддержкой Suspense по умолчанию будут оборачивать обновления навигации в переходы.

### Индикация того, что переход происходит {#indicating-that-a-transition-is-happening}

В приведенном выше примере после нажатия на кнопку нет визуальной индикации того, что происходит переход. Чтобы добавить индикатор, вы можете заменить [`startTransition`](startTransition.md) на [`useTransition`](useTransition.md), что даст вам булево значение `isPending`. В примере ниже это используется для изменения стиля заголовка сайта во время перехода:

=== "App.js"

    ```js
    import { Suspense, useState, useTransition } from 'react';
    import IndexPage from './IndexPage.js';
    import ArtistPage from './ArtistPage.js';
    import Layout from './Layout.js';

    export default function App() {
    	return (
    		<Suspense fallback={<BigSpinner />}>
    			<Router />
    		</Suspense>
    	);
    }

    function Router() {
    	const [page, setPage] = useState('/');
    	const [isPending, startTransition] = useTransition();

    	function navigate(url) {
    		startTransition(() => {
    			setPage(url);
    		});
    	}

    	let content;
    	if (page === '/') {
    		content = <IndexPage navigate={navigate} />;
    	} else if (page === '/the-beatles') {
    		content = (
    			<ArtistPage
    				artist={{
    					id: 'the-beatles',
    					name: 'The Beatles',
    				}}
    			/>
    		);
    	}
    	return <Layout isPending={isPending}>{content}</Layout>;
    }

    function BigSpinner() {
    	return <h2>🌀 Loading...</h2>;
    }
    ```

=== "Layout.js"

    ```js
    export default function Layout({ children, isPending }) {
    	return (
    		<div className="layout">
    			<section
    				className="header"
    				style={{
    					opacity: isPending ? 0.7 : 1,
    				}}
    			>
    				Music Browser
    			</section>
    			<main>{children}</main>
    		</div>
    	);
    }
    ```

=== "IndexPage.js"

    ```js
    export default function IndexPage({ navigate }) {
    	return (
    		<button onClick={() => navigate('/the-beatles')}>
    			Open The Beatles artist page
    		</button>
    	);
    }
    ```

=== "ArtistPage.js"

    ```js
    import { Suspense } from 'react';
    import Albums from './Albums.js';
    import Biography from './Biography.js';
    import Panel from './Panel.js';

    export default function ArtistPage({ artist }) {
    	return (
    		<>
    			<h1>{artist.name}</h1>
    			<Biography artistId={artist.id} />
    			<Suspense fallback={<AlbumsGlimmer />}>
    				<Panel>
    					<Albums artistId={artist.id} />
    				</Panel>
    			</Suspense>
    		</>
    	);
    }

    function AlbumsGlimmer() {
    	return (
    		<div className="glimmer-panel">
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    			<div className="glimmer-line" />
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5gfq94?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="brave-worker-5gfq94" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Сброс границ приостановки при навигации {#resetting-suspense-boundaries-on-navigation}

Во время перехода React будет избегать скрытия уже показанного содержимого. Однако, если вы переходите на маршрут с другими параметрами, вы можете захотеть сказать React, что это _другой_ контент. Вы можете выразить это с помощью `key`:

```js
<ProfilePage key={queryParams.id} />
```

Представьте, что вы перемещаетесь по странице профиля пользователя, и что-то приостанавливается. Если это обновление завернуто в переход, оно не вызовет откат для уже видимого содержимого. Это ожидаемое поведение.

Однако теперь представьте, что вы перемещаетесь между двумя разными профилями пользователей. В этом случае имеет смысл показать откат. Например, временная шкала одного пользователя представляет собой _различное содержимое_, чем временная шкала другого пользователя. Указывая `ключ`, вы гарантируете, что React рассматривает профили разных пользователей как разные компоненты и сбрасывает границы Suspense во время навигации. Маршрутизаторы, интегрированные в Suspense, должны делать это автоматически.

### Предоставление обратного хода для ошибок сервера и контента только для сервера {#providing-a-fallback-for-server-errors-and-client-only-content}

Если вы используете один из [API потокового серверного рендеринга](../react-dom/server/index.md) (или фреймворк, который полагается на них), React также будет использовать ваши границы `<Suspense>` для обработки ошибок на сервере. Если компонент выдает ошибку на сервере, React не будет прерывать серверный рендеринг. Вместо этого он найдет ближайший компонент `<Suspense>` над ним и включит его фалбэк (например, спиннер) в сгенерированный серверный HTML. Пользователь сначала увидит спиннер.

На клиенте React попытается отрисовать тот же компонент еще раз. Если и на клиенте произойдет ошибка, React выдаст ошибку и отобразит ближайшую [границу ошибки](Component.md). Однако, если ошибка не произойдет на клиенте, React не будет отображать ошибку пользователю, так как содержимое в итоге было отображено успешно.

Вы можете использовать это, чтобы исключить некоторые компоненты из рендеринга на сервере. Для этого бросьте ошибку в серверное окружение, а затем оберните их в границу `<Suspense>`, чтобы заменить их HTML фалбэками:

```js
<Suspense fallback={<Loading />}>
    <Chat />
</Suspense>;

function Chat() {
    if (typeof window === 'undefined') {
        throw Error(
            'Chat should only render on the client.'
        );
    }
    // ...
}
```

HTML сервера будет включать индикатор загрузки. На клиенте он будет заменен компонентом `Chat`.

### Фолбэк для содержимого только в браузере {#providing-a-fallback-for-browser-only-content}

Граница приостановки может показать фолбэк для компонента, который нужен только в браузере. Оберните компонент в `<Suspense>` и вызовите внутри [`use(browser())`](use.md#use-browser).

Нажмите **Reload**, чтобы увидеть фолбэк загрузки в исходном HTML. После гидратации React показывает черновик, загруженный из `localStorage`.

=== "App.js"

    ```js

    import { Suspense, use, useState } from 'react';
    import { browser } from 'react-dom';

    function SavedDraft() {
        use(browser('The draft is stored in localStorage.'));
        const [draft, setDraft] = useState(
            () => localStorage.getItem('draft') ?? ''
        );

        function handleChange(event) {
            const nextDraft = event.target.value;
            setDraft(nextDraft);
            localStorage.setItem('draft', nextDraft);
        }

        return (
            <label>
                Draft:
                <textarea
                    value={draft}
                    onChange={handleChange}
                    rows={4}
                    cols={30}
                />
            </label>
        );
    }

    export default function App() {
        return (
            <>
                <h1>Saved draft</h1>
                <Suspense fallback={<p>Loading draft...</p>}>
                    <SavedDraft />
                </Suspense>
            </>
        );
    }
    ```

=== "Document.js"

    ```js

    import App from './App.js';

    export default function Document() {
        return (
            <html lang="en">
                <head>
                    <title>Saved draft</title>
                    <style>{`
                        h1 { font-size: 24px; margin-top: 0; }
                        label, textarea { display: block; }
                        textarea { margin-top: 5px; }
                    `}</style>
                </head>
                <body>
                    <App />
                </body>
            </html>
        );
    }
    ```

=== "demo-helpers.js"

    ```js

    export async function flushReadableStreamToFrame(readable, frame) {
        const doc = frame.contentWindow.document;
        const decoder = new TextDecoder();
        const reader = readable.getReader();

        while (true) {
            const {done, value} = await reader.read();
            if (done) {
                break;
            }
            doc.write(decoder.decode(value, {stream: true}));
        }

        doc.write(decoder.decode());
        doc.close();
    }
    ```

=== "styles.css"

    ```css

    iframe {
      width: 100%;
      height: 160px;
      border: 0;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      },
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test --env=jsdom",
        "eject": "react-scripts eject"
      }
    }
    ```

Во время серверного рендеринга React включает фолбэк границы приостановки в HTML. В браузере React заменяет фолбэк сохранённым черновиком.

### Ожидание загрузки таблицы стилей {#waiting-for-a-stylesheet-to-load}

Таблица стилей, отрендеренная через [`<link rel="stylesheet">` и проп `precedence`](../react-dom/components/link.md#special-rendering-behavior), блокирует границу приостановки, пока таблица стилей не загрузится, но не дольше таймаута, чтобы содержимое не появилось без стилей.

В примере ниже компонент `Card` рендерит таблицу стилей с `precedence`. Нажмите «Show card»: React показывает фолбэк, пока таблица стилей не загрузится, а затем раскрывает карточку уже со стилями.

Для сравнения вторая кнопка выполняет то же обновление без React, в отдельном документе. Ничто не ждёт таблицу стилей, поэтому текст карточки сначала появляется запасным шрифтом, а потом переключается:

=== "js"

    ```js

    import { Suspense, useState, startTransition } from 'react';
    import { freshStylesheetUrl } from './styles.js';
    import VanillaCard from './VanillaCard.js';

    function Card({ href }) {
        return (
            <>
                <link rel="stylesheet" href={href} precedence="default" />
                <div className="fancy-card">This card uses a font from the stylesheet.</div>
            </>
        );
    }

    export default function App() {
        const [href, setHref] = useState(null);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setHref(freshStylesheetUrl());
                        });
                    }}>
                    Show card
                </button>
                {href && (
                    <Suspense fallback={<p>⌛ Loading styles...</p>}>
                        <Card href={href} />
                    </Suspense>
                )}
                <hr />
                <VanillaCard />
            </>
        );
    }
    ```

=== "VanillaCard.js"

    ```js

    import { useRef } from 'react';
    import { freshStylesheetUrl } from './styles.js';

    export default function VanillaCard() {
        const ref = useRef(null);
        function show() {
            const doc = ref.current.contentWindow.document;
            doc.open();
            doc.write(`
                <style>
                    body { margin: 0; }
                    .fancy-card {
                        padding: 20px;
                        border-radius: 8px;
                        color: white;
                        font-family: 'Caveat', sans-serif;
                        font-size: 24px;
                        background: linear-gradient(135deg, #087ea4, #2b3491);
                    }
                </style>
                <div class="fancy-card">This card uses a font from the stylesheet.</div>
                <link rel="stylesheet" href="${freshStylesheetUrl()}">
            `);
            doc.close();
        }
        return (
            <>
                <button onClick={show}>Show card (without React)</button>
                <iframe ref={ref} title="Vanilla card" className="vanilla-frame" />
            </>
        );
    }
    ```

=== "styles.js"

    ```js

    // Add a unique parameter so the stylesheet isn't cached,
    // and every run shows the loading state.
    export function freshStylesheetUrl() {
        return (
            'https://fonts.googleapis.com/css2?family=Caveat&display=swap' +
            '&t=' +
            Date.now()
        );
    }
    ```

=== "styles.css"

    ```css

    #root {
      min-height: 300px;
    }
    button {
      margin-right: 8px;
    }
    hr {
      margin: 16px 0;
    }
    .fancy-card {
      margin-top: 1em;
      padding: 20px;
      border-radius: 8px;
      color: white;
      font-family: 'Caveat', sans-serif;
      font-size: 24px;
      background: linear-gradient(135deg, #087ea4, #2b3491);
    }
    .vanilla-frame {
      display: block;
      margin-top: 1em;
      border: none;
      width: 100%;
      height: 90px;
    }
    ```

### Анимация от содержимого Suspense {#animating-from-suspense-content}

Suspense сочетается с [`<ViewTransition>`](ViewTransition.md), чтобы анимировать смену фолбэка на содержимое. Оберните границу в `<ViewTransition>`, и React воспримет эту смену как обновление и по умолчанию сделает перекрёстное затухание между фолбэком и содержимым:

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

!!!note "Примечание"

    От того, где `<ViewTransition>` стоит относительно границы, зависит, будет ли фолбэк и содержимое перекрёстно затухать как одно обновление или анимироваться как отдельные анимации выхода и входа. Анимацию также можно [настроить](ViewTransition.md#customizing-animations) классами View Transition.

    [Подробнее об анимации от содержимого Suspense.](ViewTransition.md#animating-from-suspense-content)

### Ожидание загрузки шрифта {#waiting-for-a-font-to-load}

Когда [`<ViewTransition>`](ViewTransition.md) анимирует раскрытие границы приостановки, React ждёт новые шрифты, которые вводит содержимое, но не дольше таймаута, чтобы текст не мигал запасным шрифтом. Это происходит только во время обновления `<ViewTransition>`.

В примере ниже граница приостановки обёрнута в `<ViewTransition>`, а компонент `Quote` приостанавливается, пока загружаются его данные. Рендер цитаты запускает загрузку шрифта. React держит фолбэк видимым, пока шрифт не загрузится, поэтому цитата появляется уже своим шрифтом.

Для сравнения вторая кнопка выполняет то же обновление без React. Ничто не ждёт шрифт, поэтому текст сначала появляется запасным шрифтом, а потом переключается:

=== "js"

    ```js

    import { ViewTransition, Suspense, use, useState, startTransition } from 'react';
    import { fetchQuote } from './data.js';
    import { freshFontUrl } from './font.js';
    import VanillaQuote from './VanillaQuote.js';

    function Quote({ fontSrc }) {
        const quote = use(fetchQuote());
        return (
            <>
                <style href={fontSrc} precedence="default">
                    {`@font-face {
                        font-family: 'Fancy';
                        src: url(${fontSrc}) format('truetype');
                        font-display: swap;
                    }`}
                </style>
                <p className="quote fancy">{quote}</p>
            </>
        );
    }

    export default function App() {
        const [fontSrc, setFontSrc] = useState(null);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setFontSrc(freshFontUrl());
                        });
                    }}>
                    Show quote
                </button>
                {fontSrc && (
                    <ViewTransition>
                        <Suspense fallback={<p className="quote">⌛ Loading quote...</p>}>
                            <Quote fontSrc={fontSrc} />
                        </Suspense>
                    </ViewTransition>
                )}
                <hr />
                <VanillaQuote />
            </>
        );
    }
    ```

=== "VanillaQuote.js"

    ```js

    import { useRef } from 'react';
    import { freshFontUrl } from './font.js';

    export default function VanillaQuote() {
        const ref = useRef(null);
        function show() {
            const style = document.createElement('style');
            style.textContent = `@font-face {
                font-family: 'VanillaFancy';
                src: url(${freshFontUrl()}) format('truetype');
                font-display: swap;
            }`;
            document.head.appendChild(style);
            ref.current.innerHTML = `<p class="quote vanilla-fancy">The best way to predict the future is to invent it.</p>`;
        }
        return (
            <>
                <button onClick={show}>Show quote (without React)</button>
                <div ref={ref} />
            </>
        );
    }
    ```

=== "font.js"

    ```js

    // Add a unique parameter so the font isn't cached,
    // and every run shows the loading state.
    export function freshFontUrl() {
        return (
            'https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%5Bwght%5D.ttf' +
            '?t=' +
            Date.now()
        );
    }
    ```

=== "data.js"

    ```js

    // Note: the way you would do data fetching depends on
    // the framework that you use together with Suspense.
    // Normally, the caching logic would be inside a framework.

    let cache = null;

    export function fetchQuote() {
        if (!cache) {
            cache = new Promise((resolve) => {
                // Add a fake delay to make waiting noticeable.
                setTimeout(() => {
                    resolve(
                        'The best way to predict the future is to invent it.'
                    );
                }, 500);
            });
        }
        return cache;
    }
    ```

=== "styles.css"

    ```css

    #root {
      min-height: 260px;
    }
    .quote {
      font-size: 20px;
      margin-top: 1em;
    }
    .fancy {
      font-family: 'Fancy', sans-serif;
    }
    .vanilla-fancy {
      font-family: 'VanillaFancy', sans-serif;
    }
    hr {
      margin: 16px 0;
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

### Ожидание загрузки изображения {#waiting-for-an-image-to-load}

Когда [`<ViewTransition>`](ViewTransition.md) анимирует раскрытие границы приостановки, React ждёт загрузки видимых изображений, но не дольше таймаута, чтобы анимация не началась с наполовину загруженной картинки. Это происходит только во время обновления `<ViewTransition>`. Обработчик `onLoad` исключает конкретное изображение из ожидания, даже внутри `<ViewTransition>`.

В примере ниже граница приостановки обёрнута в `<ViewTransition>` и показывает скелет профиля, пока не загрузится портрет.

Для сравнения вторая кнопка выполняет то же обновление без React. Ничто не ждёт изображение, поэтому карточка появляется сразу, а картинка всплывает, когда загрузится:

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
                <button onClick={show}>Show profile (without React)</button>
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
        "react": "19.3.0-canary-f1f7ed2a-20260904",
        "react-dom": "19.3.0-canary-f1f7ed2a-20260904",
        "react-scripts": "latest"
      }
    }
    ```

### Согласование шрифтов, изображений и таблиц стилей {#coordinating-fonts-images-and-stylesheets}

Граница приостановки может одновременно ждать данные, таблицы стилей, шрифты и изображения. Ожидание шрифтов и изображений бывает только во время обновления [`<ViewTransition>`](ViewTransition.md). В примере ниже компонент `ProfileCard` приостанавливается, пока загружаются его данные, и рендерит таблицу стилей с `precedence`, текст новым шрифтом и портрет. React держит скелет видимым, пока загружаются данные и таблица стилей. Затем раскрытие `<ViewTransition>` ждёт шрифт и изображение, чтобы карточка появилась целиком.

Для сравнения версия без React загружает те же данные и показывает, как каждый ресурс приходит по своему расписанию:

=== "js"

    ```js

    import { ViewTransition, Suspense, use, useState, startTransition } from 'react';
    import { fetchQuote } from './data.js';
    import { freshStylesheetUrl, freshImageUrl } from './resources.js';
    import VanillaProfileCard from './VanillaProfileCard.js';

    function ProfileCard({ resources }) {
        const quote = use(resources.quotePromise);
        return (
            <>
                <link rel="stylesheet" href={resources.stylesheet} precedence="default" />
                <div className="profile-card">
                    <img src={resources.image} alt="Jack Pope" width={80} height={80} />
                    <div>
                        <p className="name">Jack Pope</p>
                        <p className="bio">{quote}</p>
                    </div>
                </div>
            </>
        );
    }

    function ProfileCardPlaceholder() {
        return (
            <div className="profile-card">
                <div className="avatar-placeholder" />
                <div>
                    <p className="name name-placeholder">&nbsp;</p>
                    <p className="bio bio-placeholder">&nbsp;</p>
                </div>
            </div>
        );
    }

    export default function App() {
        const [resources, setResources] = useState(null);
        return (
            <>
                <button
                    onClick={() => {
                        startTransition(() => {
                            setResources({
                                quotePromise: fetchQuote(),
                                stylesheet: freshStylesheetUrl(),
                                image: freshImageUrl(),
                            });
                        });
                    }}>
                    Show profile
                </button>
                {resources && (
                    <ViewTransition>
                        <Suspense fallback={<ProfileCardPlaceholder />}>
                            <ProfileCard resources={resources} />
                        </Suspense>
                    </ViewTransition>
                )}
                <hr />
                <VanillaProfileCard />
            </>
        );
    }
    ```

=== "VanillaProfileCard.js"

    ```js

    import { useRef } from 'react';
    import { fetchQuote } from './data.js';
    import { freshStylesheetUrl, freshImageUrl } from './resources.js';

    export default function VanillaProfileCard() {
        const ref = useRef(null);
        async function show() {
            const quote = await fetchQuote();
            const doc = ref.current.contentWindow.document;
            doc.open();
            doc.write(`
                <style>
                    body { margin: 0; font-family: sans-serif; }
                    .profile-card { display: flex; gap: 12px; align-items: center; }
                    .profile-card img { border-radius: 50%; background: #dfe3e9; }
                    .name { margin: 0 0 4px; font-family: 'Caveat', sans-serif; font-size: 22px; line-height: 28px; font-weight: bold; }
                    .bio { margin: 0; font-family: 'Caveat', sans-serif; font-size: 20px; line-height: 26px; }
                </style>
                <div class="profile-card">
                    <img src="${freshImageUrl()}" alt="Jack Pope" width="80" height="80" />
                    <div>
                        <p class="name">Jack Pope</p>
                        <p class="bio">${quote}</p>
                    </div>
                </div>
                <link rel="stylesheet" href="${freshStylesheetUrl()}">
            `);
            doc.close();
        }
        return (
            <>
                <button onClick={show}>Show profile (without React)</button>
                <iframe ref={ref} title="Vanilla profile card" className="vanilla-frame" />
            </>
        );
    }
    ```

=== "resources.js"

    ```js

    // Add a unique parameter so the resources aren't cached,
    // and every run shows the loading state.
    export function freshStylesheetUrl() {
        return (
            'https://fonts.googleapis.com/css2?family=Caveat&display=swap' +
            '&t=' +
            Date.now()
        );
    }

    export function freshImageUrl() {
        return 'https://react.dev/images/team/jack-pope.jpg?t=' + Date.now();
    }
    ```

=== "data.js"

    ```js

    // Note: the way you would do data fetching depends on
    // the framework that you use together with Suspense.

    export async function fetchQuote() {
        // Add a fake delay to make waiting noticeable.
        await new Promise((resolve) => {
            setTimeout(resolve, 1000);
        });
        return 'The best way to predict the future is to invent it.';
    }
    ```

=== "styles.css"

    ```css

    #root {
      min-height: 320px;
    }
    button {
      margin-right: 8px;
    }
    hr {
      margin: 16px 0;
    }
    .profile-card {
      display: flex;
      gap: 12px;
      align-items: center;
      margin-top: 1em;
    }
    .profile-card img {
      border-radius: 50%;
      background: #dfe3e9;
    }
    .name {
      margin: 0 0 4px;
      font-family: 'Caveat', sans-serif;
      font-size: 22px;
      line-height: 28px;
      font-weight: bold;
    }
    .bio {
      margin: 0;
      font-family: 'Caveat', sans-serif;
      font-size: 20px;
      line-height: 26px;
    }
    .profile-card img {
      display: block;
    }
    .avatar-placeholder {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: #dfe3e9;
    }
    .name-placeholder,
    .bio-placeholder {
      border-radius: 4px;
      background: #dfe3e9;
      color: transparent;
    }
    .name-placeholder {
      width: 90px;
    }
    .bio-placeholder {
      width: 220px;
    }
    .vanilla-frame {
      display: block;
      margin-top: 1em;
      border: none;
      width: 100%;
      height: 110px;
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

## Устранение неполадок {#troubleshooting}

### Как предотвратить замену пользовательского интерфейса на fallback во время обновления? {#preventing-unwanted-fallbacks}

Замена видимого пользовательского интерфейса на фалбэк приводит к резким изменениям в работе пользователя. Это может произойти, когда обновление приводит к приостановке компонента, а ближайшая граница приостановки уже показывает пользователю содержимое.

Чтобы этого не произошло, пометьте обновление как несрочное с помощью `startTransition`. Во время перехода React будет ждать, пока загрузится достаточно данных, чтобы предотвратить появление нежелательного отката:

```js hl_lines="2-3 5"
function handleNextPageClick() {
    // If this update suspends, don't hide the already displayed content
    startTransition(() => {
        setCurrentPage(currentPage + 1);
    });
}
```

Это позволит избежать скрытия существующего содержимого. Тем не менее, все новые границы `Suspense` будут немедленно отображать отступления, чтобы избежать блокировки пользовательского интерфейса и позволить пользователю видеть содержимое по мере его появления.

**React будет предотвращать нежелательные отступления только во время несрочных обновлений**. Он не будет задерживать рендеринг, если он является результатом срочного обновления. Вы должны выбрать API, например [`startTransition`](startTransition.md) или [`useDeferredValue`](useDeferredValue.md).

Если ваш маршрутизатор интегрирован с Suspense, он должен автоматически обернуть свои обновления в [`startTransition`](startTransition.md).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/Suspense](https://react.dev/reference/react/Suspense)</small>
