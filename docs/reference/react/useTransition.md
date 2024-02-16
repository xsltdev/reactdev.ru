# useTransition

**`useTransition`** - это хук React, который позволяет обновлять состояние без блокировки пользовательского интерфейса.

<!-- 0001.part.md -->

```js
const [isPending, startTransition] = useTransition();
```

## Описание

### `useTransition()`

Вызовите `useTransition` на верхнем уровне вашего компонента, чтобы пометить некоторые обновления состояния как переходы.

<!-- 0003.part.md -->

```js
import { useTransition } from 'react';

function TabContainer() {
    const [isPending, startTransition] = useTransition();
    // ...
}
```

#### Параметры

`useTransition` не принимает никаких параметров.

#### Returns

`useTransition` возвращает массив, содержащий ровно два элемента:

1.  Флаг `isPending`, который сообщает, есть ли ожидающий переход.
2.  Функция `startTransition`, позволяющая пометить обновление состояния как переход.

### Функция `startTransition`

Функция `startTransition`, возвращаемая `useTransition`, позволяет пометить обновление состояния как переход.

<!-- 0005.part.md -->

```js
function TabContainer() {
    const [isPending, startTransition] = useTransition();
    const [tab, setTab] = useState('about');

    function selectTab(nextTab) {
        startTransition(() => {
            setTab(nextTab);
        });
    }
    // ...
}
```

<!-- 0006.part.md -->

#### Параметры

-   `scope`: Функция, которая обновляет некоторое состояние, вызывая одну или несколько функций [`set`](useState.md). React немедленно вызывает `scope` без параметров и помечает все обновления состояния, запланированные синхронно во время вызова функции `scope`, как переходы. Они будут неблокирующими и не будут отображать нежелательные индикаторы загрузки.

#### Возврат

`startTransition` ничего не возвращает.

#### Ограничения

-   `useTransition` - это хук, поэтому его можно вызывать только внутри компонентов или пользовательских хуков. Если вам нужно запустить переход в другом месте (например, из библиотеки данных), вызовите вместо этого отдельный [`startTransition`](startTransition.md).

-   Вы можете обернуть обновление в переход, только если у вас есть доступ к функции `set` этого состояния. Если вы хотите запустить переход в ответ на какой-то пропс или пользовательское значение Hook, попробуйте вместо этого использовать [`useDeferredValue`](useDeferredValue.md).

-   Функция, которую вы передаете в `startTransition`, должна быть синхронной. React немедленно выполняет эту функцию, помечая все обновления состояния, которые происходят во время ее выполнения, как переходы. Если вы попытаетесь выполнить дополнительные обновления состояния позже (например, во время таймаута), они не будут помечены как переходы.

-   Обновление состояния, помеченное как переход, будет прерываться другими обновлениями состояния. Например, если вы обновите компонент графика внутри перехода, а затем начнете вводить текст в поле ввода, когда график находится в середине повторного рендеринга, React перезапустит работу по рендерингу компонента графика после обработки обновления ввода.

-   Обновления переходов нельзя использовать для управления текстовыми вводами.

-   При наличии нескольких текущих переходов React в настоящее время собирает их вместе. Это ограничение, которое, вероятно, будет устранено в будущем выпуске.

## Использование

### Пометка обновления состояния как неблокирующего перехода

Вызовите `useTransition` на верхнем уровне вашего компонента, чтобы пометить обновление состояния как неблокирующий _переход_.

<!-- 0007.part.md -->

```js
import { useState, useTransition } from 'react';

function TabContainer() {
    const [isPending, startTransition] = useTransition();
    // ...
}
```

<!-- 0008.part.md -->

`useTransition` возвращает массив, содержащий ровно два элемента:

1.  Флаг `isPending`, который сообщает, есть ли ожидающий переход.
2.  `startTransition` function, которая позволяет отметить обновление состояния как переход.

Вы можете пометить обновление состояния как переход следующим образом:

<!-- 0009.part.md -->

```js
function TabContainer() {
    const [isPending, startTransition] = useTransition();
    const [tab, setTab] = useState('about');

    function selectTab(nextTab) {
        startTransition(() => {
            setTab(nextTab);
        });
    }
    // ...
}
```

<!-- 0010.part.md -->

Переходы позволяют сохранить отзывчивость обновлений пользовательского интерфейса даже на медленных устройствах.

С помощью перехода пользовательский интерфейс остается отзывчивым в середине повторного рендеринга. Например, если пользователь нажал на вкладку, но затем передумал и нажал на другую вкладку, он может сделать это, не дожидаясь окончания первого повторного рендеринга.

### Разница между useTransition и обычным обновлением состояния

#### 1. Обновление текущей вкладки в переходе

В этом примере вкладка "Posts" **искусственно замедлена**, так что на ее отображение уходит не менее секунды.

Нажмите "Posts", а затем сразу же нажмите "Contact". Обратите внимание, что это прерывает медленное отображение "Posts". Вкладка "Контакт" отображается немедленно. Поскольку это обновление состояния отмечено как переход, медленный повторный рендеринг не привел к зависанию пользовательского интерфейса.

=== "App.js"

    ```js
    import { useState, useTransition } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [isPending, startTransition] = useTransition();
    	const [tab, setTab] = useState('about');

    	function selectTab(nextTab) {
    		startTransition(() => {
    			setTab(nextTab);
    		});
    	}

    	return (
    		<>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => selectTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => selectTab('posts')}
    			>
    				Posts (slow)
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => selectTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    import { useTransition } from 'react';

    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				onClick();
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "AboutTab.js"

    ```js
    export default function AboutTab() {
    	return <p>Welcome to my profile!</p>;
    }
    ```

=== "PostsTab.js"

    ```js
    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
    	// Log once. The actual slowdown is inside SlowPost.
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />'
    	);

    	let items = [];
    	for (let i = 0; i < 500; i++) {
    		items.push(<SlowPost key={i} index={i} />);
    	}
    	return <ul className="items">{items}</ul>;
    });

    function SlowPost({ index }) {
    	let startTime = performance.now();
    	while (performance.now() - startTime < 1) {
    		// Do nothing for 1 ms per item to emulate extremely slow code
    	}

    	return <li className="item">Post #{index + 1}</li>;
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js
    export default function ContactTab() {
    	return (
    		<>
    			<p>You can find me online here:</p>
    			<ul>
    				<li>admin@mysite.com</li>
    				<li>+123456789</li>
    			</ul>
    		</>
    	);
    }
    ```

#### 2. Обновление текущей вкладки без перехода

В этом примере вкладка "Posts" также **искусственно замедляется**, так что на ее отображение уходит не менее секунды. В отличие от предыдущего примера, это обновление состояния **не является переходом.**

Нажмите "Сообщения", а затем сразу же нажмите "Контакт". Обратите внимание, что приложение замирает во время рендеринга замедленной вкладки, а пользовательский интерфейс становится неотзывчивым. Это обновление состояния не является переходом, поэтому медленный повторный рендеринг заморозил пользовательский интерфейс.

=== "App.js"

    ```js
    import { useState } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [tab, setTab] = useState('about');

    	function selectTab(nextTab) {
    		setTab(nextTab);
    	}

    	return (
    		<>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => selectTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => selectTab('posts')}
    			>
    				Posts (slow)
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => selectTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    import { useTransition } from 'react';

    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				onClick();
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "AboutTab.js"

    ```js
    export default function AboutTab() {
    	return <p>Welcome to my profile!</p>;
    }
    ```

=== "PostsTab.js"

    ```js
    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
    	// Log once. The actual slowdown is inside SlowPost.
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />'
    	);

    	let items = [];
    	for (let i = 0; i < 500; i++) {
    		items.push(<SlowPost key={i} index={i} />);
    	}
    	return <ul className="items">{items}</ul>;
    });

    function SlowPost({ index }) {
    	let startTime = performance.now();
    	while (performance.now() - startTime < 1) {
    		// Do nothing for 1 ms per item to emulate extremely slow code
    	}

    	return <li className="item">Post #{index + 1}</li>;
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js
    export default function ContactTab() {
    	return (
    		<>
    			<p>You can find me online here:</p>
    			<ul>
    				<li>admin@mysite.com</li>
    				<li>+123456789</li>
    			</ul>
    		</>
    	);
    }
    ```

### Обновление родительского компонента в переходе

Вы можете обновить состояние родительского компонента и из вызова `useTransition`. Например, этот компонент `TabButton` обернул свою логику `onClick` в переход:

<!-- 0035.part.md -->

```js
export default function TabButton({
    children,
    isActive,
    onClick,
}) {
    const [isPending, startTransition] = useTransition();
    if (isActive) {
        return <b>{children}</b>;
    }
    return (
        <button
            onClick={() => {
                startTransition(() => {
                    onClick();
                });
            }}
        >
            {children}
        </button>
    );
}
```

<!-- 0036.part.md -->

Поскольку родительский компонент обновляет свое состояние внутри обработчика события `onClick`, это обновление состояния помечается как переход. Вот почему, как в предыдущем примере, вы можете щелкнуть на "Posts", а затем сразу же щелкнуть на "Contact". Обновление выбранной вкладки помечается как переход, поэтому оно не блокирует взаимодействие с пользователем.

=== "App.js"

    ```js
    import { useState } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [tab, setTab] = useState('about');
    	return (
    		<>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => setTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => setTab('posts')}
    			>
    				Posts (slow)
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => setTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    import { useTransition } from 'react';

    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	const [isPending, startTransition] = useTransition();
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				startTransition(() => {
    					onClick();
    				});
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "AboutTab.js"

    ```js
    export default function AboutTab() {
    	return <p>Welcome to my profile!</p>;
    }
    ```

=== "PostsTab.js"

    ```js
    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
    	// Log once. The actual slowdown is inside SlowPost.
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />'
    	);

    	let items = [];
    	for (let i = 0; i < 500; i++) {
    		items.push(<SlowPost key={i} index={i} />);
    	}
    	return <ul className="items">{items}</ul>;
    });

    function SlowPost({ index }) {
    	let startTime = performance.now();
    	while (performance.now() - startTime < 1) {
    		// Do nothing for 1 ms per item to emulate extremely slow code
    	}

    	return <li className="item">Post #{index + 1}</li>;
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js
    export default function ContactTab() {
    	return (
    		<>
    			<p>You can find me online here:</p>
    			<ul>
    				<li>admin@mysite.com</li>
    				<li>+123456789</li>
    			</ul>
    		</>
    	);
    }
    ```

### Отображение ожидающего визуального состояния во время перехода

Вы можете использовать булево значение `isPending`, возвращаемое `useTransition`, чтобы указать пользователю, что переход находится в процессе. Например, кнопка табуляции может иметь специальное визуальное состояние "в ожидании":

<!-- 0049.part.md -->

```js
function TabButton({ children, isActive, onClick }) {
    const [isPending, startTransition] = useTransition();
    // ...
    if (isPending) {
        return <b className="pending">{children}</b>;
    }
    // ...
}
```

<!-- 0050.part.md -->

Обратите внимание, что нажатие кнопки "Posts" теперь кажется более отзывчивым, потому что сама кнопка вкладки сразу же обновляется:

=== "App.js"

    ```js
    import { useState } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [tab, setTab] = useState('about');
    	return (
    		<>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => setTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => setTab('posts')}
    			>
    				Posts (slow)
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => setTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    import { useTransition } from 'react';

    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	const [isPending, startTransition] = useTransition();
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	if (isPending) {
    		return <b className="pending">{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				startTransition(() => {
    					onClick();
    				});
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "AboutTab.js"

    ```js
    export default function AboutTab() {
    	return <p>Welcome to my profile!</p>;
    }
    ```

=== "PostsTab.js"

    ```js
    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
    	// Log once. The actual slowdown is inside SlowPost.
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />'
    	);

    	let items = [];
    	for (let i = 0; i < 500; i++) {
    		items.push(<SlowPost key={i} index={i} />);
    	}
    	return <ul className="items">{items}</ul>;
    });

    function SlowPost({ index }) {
    	let startTime = performance.now();
    	while (performance.now() - startTime < 1) {
    		// Do nothing for 1 ms per item to emulate extremely slow code
    	}

    	return <li className="item">Post #{index + 1}</li>;
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js
    export default function ContactTab() {
    	return (
    		<>
    			<p>You can find me online here:</p>
    			<ul>
    				<li>admin@mysite.com</li>
    				<li>+123456789</li>
    			</ul>
    		</>
    	);
    }
    ```

### Предотвращение нежелательных индикаторов загрузки

В этом примере компонент `PostsTab` получает некоторые данные, используя источник данных [Suspense-enabled](Suspense.md). Когда вы нажимаете на вкладку "Posts", компонент `PostsTab` _приостанавливается_, вызывая появление ближайшего фалбэка загрузки:

=== "App.js"

    ```js
    import { Suspense, useState } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [tab, setTab] = useState('about');
    	return (
    		<Suspense fallback={<h1>🌀 Loading...</h1>}>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => setTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => setTab('posts')}
    			>
    				Posts
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => setTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</Suspense>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				onClick();
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

Скрытие всего контейнера вкладки для отображения индикатора загрузки приводит к искажению пользовательского опыта. Если вы добавите `useTransition` к `TabButton`, вы можете вместо этого указать отображение состояния ожидания в кнопке вкладки.

Обратите внимание, что при нажатии на кнопку "Posts" весь контейнер вкладки больше не заменяется спиннером:

=== "App.js"

    ```js
    import { Suspense, useState } from 'react';
    import TabButton from './TabButton.js';
    import AboutTab from './AboutTab.js';
    import PostsTab from './PostsTab.js';
    import ContactTab from './ContactTab.js';

    export default function TabContainer() {
    	const [tab, setTab] = useState('about');
    	return (
    		<Suspense fallback={<h1>🌀 Loading...</h1>}>
    			<TabButton
    				isActive={tab === 'about'}
    				onClick={() => setTab('about')}
    			>
    				About
    			</TabButton>
    			<TabButton
    				isActive={tab === 'posts'}
    				onClick={() => setTab('posts')}
    			>
    				Posts
    			</TabButton>
    			<TabButton
    				isActive={tab === 'contact'}
    				onClick={() => setTab('contact')}
    			>
    				Contact
    			</TabButton>
    			<hr />
    			{tab === 'about' && <AboutTab />}
    			{tab === 'posts' && <PostsTab />}
    			{tab === 'contact' && <ContactTab />}
    		</Suspense>
    	);
    }
    ```

=== "TabButton.js"

    ```js
    import { useTransition } from 'react';

    export default function TabButton({
    	children,
    	isActive,
    	onClick,
    }) {
    	const [isPending, startTransition] = useTransition();
    	if (isActive) {
    		return <b>{children}</b>;
    	}
    	if (isPending) {
    		return <b className="pending">{children}</b>;
    	}
    	return (
    		<button
    			onClick={() => {
    				startTransition(() => {
    					onClick();
    				});
    			}}
    		>
    			{children}
    		</button>
    	);
    }
    ```

[Подробнее об использовании переходов в Suspense](Suspense.md)

!!!note ""

    Переходы будут "ждать" только достаточно долго, чтобы избежать скрытия _уже раскрытого_ содержимого (например, контейнера вкладки). Если вкладка Posts имеет [вложенную границу `<Suspense>`](Suspense.md), переход не будет "ждать" ее.

### Создание маршрутизатора с поддержкой `Suspense`

Если вы создаете фреймворк React или маршрутизатор, мы рекомендуем помечать переходы по страницам как переходы.

<!-- 0091.part.md -->

```js
function Router() {
    const [page, setPage] = useState('/');
    const [isPending, startTransition] = useTransition();

    function navigate(url) {
        startTransition(() => {
            setPage(url);
        });
    }
    // ...
}
```

<!-- 0092.part.md -->

Это рекомендуется по двум причинам:

-   Переходы прерывисты, что позволяет пользователю щелкнуть мышью, не дожидаясь завершения повторного рендеринга.
-   Переходы предотвращают нежелательные индикаторы загрузки, что позволяет пользователю избежать резких скачков при навигации.

Вот небольшой упрощенный пример маршрутизатора с использованием переходов для навигации.

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

!!!note ""

    [Suspense-enabled](Suspense.md) ожидается, что маршрутизаторы по умолчанию будут оборачивать обновления навигации в переходы.

## Устранение неполадок

### Обновление входа в переходе не работает

Вы не можете использовать переход для переменной состояния, которая управляет входом:

<!-- 0113.part.md -->

```js
const [text, setText] = useState('');
// ...
function handleChange(e) {
    // ❌ Can't use transitions for controlled input state
    startTransition(() => {
        setText(e.target.value);
    });
}
// ...
return <input value={text} onChange={handleChange} />;
```

<!-- 0114.part.md -->

Это связано с тем, что переходы являются неблокирующими, но обновление ввода в ответ на событие изменения должно происходить синхронно. Если вы хотите запустить переход в ответ на ввод текста, у вас есть два варианта:

1.  Вы можете объявить две отдельные переменные состояния: одну для состояния ввода (которая всегда обновляется синхронно) и одну, которую вы будете обновлять в переходе. Это позволит вам управлять вводом, используя синхронное состояние, и передать переменную состояния перехода (которая будет "отставать" от ввода) остальной части вашей логики рендеринга.
2.  В качестве альтернативы вы можете иметь одну переменную состояния и добавить [`useDeferredValue`](useDeferredValue.md), которая будет "отставать" от реального значения. Это вызовет неблокирующие повторные рендеринги, чтобы автоматически "догнать" новое значение.

### React не рассматривает обновление моего состояния как переход

Когда вы оборачиваете обновление состояния в переход, убедитесь, что оно происходит _во время_ вызова `startTransition`:

<!-- 0115.part.md -->

```js
startTransition(() => {
    // ✅ Setting state *during* startTransition call
    setPage('/about');
});
```

<!-- 0116.part.md -->

Функция, которую вы передаете в `startTransition`, должна быть синхронной.

Вы не можете пометить обновление как переход таким образом:

<!-- 0117.part.md -->

```js
startTransition(() => {
    // ❌ Setting state *after* startTransition call
    setTimeout(() => {
        setPage('/about');
    }, 1000);
});
```

<!-- 0118.part.md -->

Вместо этого вы можете сделать следующее:

<!-- 0119.part.md -->

```js
setTimeout(() => {
    startTransition(() => {
        // ✅ Setting state *during* startTransition call
        setPage('/about');
    });
}, 1000);
```

<!-- 0120.part.md -->

Точно так же вы не можете пометить обновление как переход:

<!-- 0121.part.md -->

```js
startTransition(async () => {
    await someAsyncFunction();
    // ❌ Setting state *after* startTransition call
    setPage('/about');
});
```

<!-- 0122.part.md -->

Однако это работает вместо этого:

<!-- 0123.part.md -->

```js
await someAsyncFunction();
startTransition(() => {
    // ✅ Setting state *during* startTransition call
    setPage('/about');
});
```

### Я хочу вызвать `useTransition` извне компонента

Вы не можете вызвать `useTransition` вне компонента, потому что это Hook. В этом случае вместо него используйте отдельный метод [`startTransition`](startTransition.md). Он работает так же, но не предоставляет индикатор `isPending`.

### Функция, которую я передаю в `startTransition`, выполняется немедленно

Если вы запустите этот код, он выведет 1, 2, 3:

<!-- 0125.part.md -->

```js
console.log(1);
startTransition(() => {
    console.log(2);
    setPage('/about');
});
console.log(3);
```

<!-- 0126.part.md -->

**Ожидается, что будет выведено 1, 2, 3.** Функция, которую вы передаете в `startTransition`, не задерживается. В отличие от браузера `setTimeout`, он не запускает обратный вызов позже. React выполняет вашу функцию немедленно, но все обновления состояния, запланированные _пока она выполняется_, помечаются как переходы. Вы можете представить, что это работает следующим образом:

<!-- 0127.part.md -->

```js
// A simplified version of how React works

let isInsideTransition = false;

function startTransition(scope) {
    isInsideTransition = true;
    scope();
    isInsideTransition = false;
}

function setState() {
    if (isInsideTransition) {
        // ... schedule a transition state update ...
    } else {
        // ... schedule an urgent state update ...
    }
}
```

## Ссылки

-   [https://react.dev/reference/react/useTransition](https://react.dev/reference/react/useTransition)
