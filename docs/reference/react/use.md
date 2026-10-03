---
description: use - это хук React, который позволяет вам прочитать значение ресурса, например промиса или контекста
---

# use

<big>`use` - это хук React, который позволяет вам прочитать значение ресурса, например [промиса](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекста](../../learn/passing-data-deeply-with-context.md).</big>

```js
const value = use(resource);
```

---

## Описание {#reference}

### `use(resource)` {#use}

Вызовите `use` в вашем компоненте, чтобы прочитать значение ресурса, например [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [context](../../learn/passing-data-deeply-with-context.md).

```js
import { use } from 'react';

function MessageComponent({ messagePromise }) {
    const message = use(messagePromise);
    const theme = use(ThemeContext);
    // ...
}
```

В отличие от всех остальных хуков React, `use` можно вызывать в циклах и условных операторах, таких как `if`. Как и другие хуки React, функция, вызывающая `use`, должна быть компонентом или хуком.

При вызове с `Promise` хук `use` интегрируется с [`Suspense`](Suspense.md) и [error boundaries](Component.md#catching-rendering-errors-with-an-error-boundary). Компонент, вызывающий `use`, _приостанавливается_ на время выполнения `Promise`, переданного `use`. Если компонент, вызывающий `use`, обернут в границу `Suspense`, то будет отображен `fallback`. После разрешения `Promise`, Suspense fallback заменяется рендерингом компонентов, использующих данные, возвращенные хуком `use`. Если промис, переданный в `use`, отклонен, будет отображен фаллбек ближайшей границы ошибки.

#### Параметры {#parameters}

-   `resource`: это источник данных, из которого вы хотите прочитать значение. Ресурсом может быть [промис](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекст](../../learn/passing-data-deeply-with-context.md).

#### Возвращает {#returns}

Хук `use` возвращает значение, которое было прочитано из ресурса, как разрешенное значение [промиса](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) или [контекст](../../learn/passing-data-deeply-with-context.md).

#### Замечания {#caveats}

-   Хук `use` должен быть вызван внутри компонента или хука.
-   При получении данных в [серверном компоненте](../rsc/use-server.md) отдавайте предпочтение `async` и `await`, а не `use`. `async` и `await` выполняют рендеринг с того момента, когда был вызван `await`, в то время как `use` повторно рендерит компонент после разрешения данных.
-   Предпочтительнее создавать промисы в [Компонентах сервера](../rsc/use-server.md) и передавать их в [Компоненты клиента](../rsc/use-client.md), чем создавать обещания в компонентах клиента. Обещания, созданные в клиентских компонентах, пересоздаются при каждом рендере. Обещания, переданные из серверного компонента в клиентский компонент, стабильны при каждом рендере. [См. этот пример](#streaming-data-from-server-to-client).

### `use(context)` {#use-context}

Вызовите `use` с [контекстом](../../learn/passing-data-deeply-with-context.md), чтобы прочитать его значение. В отличие от [`useContext`](useContext.md), `use` можно вызывать в циклах и условиях вроде `if`.

```js
import { use } from 'react';

function Button() {
  const theme = use(ThemeContext);
  // ...
```

[Смотрите другие примеры ниже.](#usage-context)

#### Параметры {#context-parameters}

* `context`: [контекст](../../learn/passing-data-deeply-with-context.md), созданный через [`createContext`](createContext.md).

#### Возвращаемое значение {#context-returns}

Значение контекста для переданного контекста. Его определяет ближайший провайдер контекста выше компонента, который вызвал `use`. Если провайдера нет, возвращается `defaultValue`, переданный в [`createContext`](createContext.md).

#### Предупреждения {#context-caveats}

* `use` нужно вызывать внутри компонента или хука.
* Чтение контекста через `use` не поддерживается в [серверных компонентах](../rsc/server-components.md).

### `use(promise)` {#use-promise}

Вызовите `use` с [промисом](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), чтобы прочитать его разрешённое значение. Компонент, который вызывает `use`, *приостанавливается*, пока промис ожидает. Несмотря на имя, `use` — это не хук. В отличие от хуков, его можно вызывать в циклах и условиях вроде `if`.

```js
import { use } from 'react';

function MessageComponent({ messagePromise }) {
  const message = use(messagePromise);
  // ...
```

Если компонент, вызывающий `use`, обёрнут в границу [Suspense](Suspense.md), пока промис ожидает, будет показан фолбэк. Когда промис разрешится, фолбэк Suspense заменится компонентами, которые рендерятся с данными, возвращёнными `use`. Если промис отклонён, будет показан фолбэк ближайшей [границы ошибки](Component.md#catching-rendering-errors-with-an-error-boundary).

[Смотрите другие примеры ниже.](#usage-promises)

#### Параметры {#promise-parameters}

* `promise`: [промис](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), разрешённое значение которого нужно прочитать. Промис должен быть [закэширован](#caching-promises-for-client-components), чтобы между повторными рендерами переиспользовался один и тот же экземпляр.

#### Возвращаемое значение {#promise-returns}

Разрешённое значение промиса.

#### Предупреждения {#promise-caveats}

* `use` нужно вызывать внутри компонента или хука.
* `use` нельзя вызывать внутри блока try-catch. Вместо этого оберните компонент в [границу ошибки](#displaying-an-error-with-an-error-boundary), чтобы поймать ошибку и показать фолбэк.
* Промисы, переданные в `use`, нужно кэшировать, чтобы между повторными рендерами переиспользовался один и тот же экземпляр. [Смотрите кэширование промисов ниже.](#caching-promises-for-client-components)
* Когда промис передаётся из серверного компонента в клиентский, его разрешённое значение должно быть [сериализуемым](../rsc/use-client.md#serializable-types).

### `use(browser())` {#use-browser}

Вызовите `use` со значением, которое вернул [`browser`](../react-dom/browser.md), в компоненте, который должен рендериться только в браузере:

```js
import { use } from 'react';
import { browser } from 'react-dom';

function BrowserOnly() {
  use(browser('This component requires browser APIs.'));
  return <BrowserContent />;
}
```

Во время серверного рендеринга компонент, вызывающий `use(browser())`, приостанавливается, и React включает в HTML фолбэк ближайшей границы [`<Suspense>`](Suspense.md). В браузере `use(browser())` возвращает `undefined`, и компонент рендерится как обычно.

[Смотрите пример ниже.](#rendering-a-component-only-in-the-browser)

#### Параметры {#browser-parameters}

* `browserValue`: значение, которое вернул [`browser`](../react-dom/browser.md).

#### Возвращаемое значение {#browser-returns}

В браузере `use(browser())` возвращает `undefined`.

#### Предупреждения {#browser-caveats}

* Компонент, вызывающий `use(browser())`, во время серверного рендеринга должен быть внутри границы `<Suspense>`. Без неё серверный рендеринг завершится ошибкой.
* В приложении с React Server Components `use(browser())` нужно вызывать из [клиентского компонента](../rsc/use-client.md), а не из [серверного компонента](../rsc/server-components.md).

## Использование {#usage}

## Использование (контекст) {#usage-context}

### Чтение контекста с помощью `use` {#reading-context-with-use}

Когда в `use` передается [context](../../learn/passing-data-deeply-with-context.md), он работает аналогично [`useContext`](useContext.md). В то время как `useContext` должен вызываться на верхнем уровне вашего компонента, `use` можно вызывать внутри условий типа `if` и циклов типа `for`. `use` предпочтительнее, чем `useContext`, потому что он более гибкий.

```js hl_lines="4"
import { use } from 'react';

function Button() {
    const theme = use(ThemeContext);
    // ...
}
```

`use` возвращает значение контекста для переданного вами контекста. Чтобы определить значение контекста, React просматривает дерево компонентов и находит **ближайший провайдер контекста выше** для данного контекста.

Чтобы передать контекст кнопке `Button`, оберните ее или один из ее родительских компонентов в соответствующий провайдер контекста.

```js hl_lines="3 5"
function MyPage() {
    return (
        <ThemeContext.Provider value="dark">
            <Form />
        </ThemeContext.Provider>
    );
}

function Form() {
    // ... renders buttons inside ...
}
```

Не имеет значения, сколько слоев компонентов находится между провайдером и `Button`. Когда `Button` _в любом месте_ внутри `Form` вызывает `use(ThemeContext)`, она получит `"dark"` в качестве значения.

В отличие от [`useContext`](useContext.md), `use` можно вызывать в условиях и циклах, как `if`.

```js hl_lines="2-3"
function HorizontalRule({ show }) {
    if (show) {
        const theme = use(ThemeContext);
        return <hr className={theme} />;
    }
    return false;
}
```

`use` вызывается внутри оператора `if`, позволяя вам условно считывать значения из Context.

!!!warning "Ближайший провайдер"

    Как и `useContext`, `use(context)` всегда ищет ближайшего провайдера контекста _выше_ компонента, который его вызывает. Он ищет вверх и **не** рассматривает провайдеров контекста в компоненте, из которого вы вызываете `use(context)`.

</Pitfall>

<Sandpack>

=== "App.js"

    ```js
    import { createContext, use } from 'react';

    const ThemeContext = createContext(null);

    export default function MyApp() {
    	return (
    		<ThemeContext.Provider value="dark">
    			<Form />
    		</ThemeContext.Provider>
    	);
    }

    function Form() {
    	return (
    		<Panel title="Welcome">
    			<Button show={true}>Sign up</Button>
    			<Button show={false}>Log in</Button>
    		</Panel>
    	);
    }

    function Panel({ title, children }) {
    	const theme = use(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ show, children }) {
    	if (show) {
    		const theme = use(ThemeContext);
    		const className = 'button-' + theme;
    		return (
    			<button className={className}>
    				{children}
    			</button>
    		);
    	}
    	return false;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/68ryxj?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="silly-dijkstra-68ryxj" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Чтение промиса из контекста {#reading-a-promise-from-context}

Чтобы делиться асинхронными данными без прокидывания пропсов, положите промис в значение контекста, прочитайте его через `use(context)` и разрешите через `use(promise)`:

```js
import { use } from 'react';
import { UserContext } from './UserContext';

function Profile() {
  const userPromise = use(UserContext);
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}
```

Чтобы прочитать значение, нужны два вызова `use`, потому что само значение контекста не ожидается. Прежде чем тянуться к контексту, смотрите альтернативы в разделе [Прежде чем использовать контекст](../../learn/passing-data-deeply-with-context.md#before-you-use-context).

Оберните компоненты, которые читают промис, в границу [Suspense](Suspense.md), чтобы приостановилось только это поддерево, пока промис ожидает. Подробнее о чтении промисов через `use` — в разделе [Использование (промисы)](#usage-promises) ниже.

!!!warning "Подводный камень"

    Если этот приём используется с [серверными компонентами](../rsc/server-components.md), повторная загрузка промиса требует повторного рендера серверного компонента, который кладёт промис в контекст. Не ставьте промис в контекст высоко в дереве: иначе без нужды заново отрендерится большая часть приложения.

## Использование (промисы) {#usage-promises}

### Чтение промиса с помощью `use` {#reading-a-promise-with-use}

Вызовите `use` с промисом, чтобы прочитать его разрешённое значение. Пока промис ожидает, компонент [приостановится](Suspense.md).

```js hl_lines="4"
import { use } from 'react';

function Albums({ albumsPromise }) {
  const albums = use(albumsPromise);
  return (
    <ul>
      {albums.map(album => (
        <li key={album.id}>
          {album.title} ({album.year})
        </li>
      ))}
    </ul>
  );
}
```

Оберните компонент, который вызывает `use`, в границу [Suspense](Suspense.md), чтобы React мог показать фолбэк, пока промис ожидает. Ближайшая граница Suspense выше приостановленного компонента показывает свой фолбэк. Когда промис разрешится, React прочитает значение через `use` и заменит фолбэк отрендеренным компонентом.

## Примеры {#recipes}

#### Загрузка данных с помощью `use` {#fetching-data-with-use}

В этом примере `Albums` вызывает `use` с закэшированным промисом. Пока промис ожидает, компонент приостанавливается, и React показывает ближайший фолбэк Suspense. Отклонённые промисы доходят до ближайшей [границы ошибки](Component.md#catching-rendering-errors-with-an-error-boundary).

=== "App.js"

    ```js

    import { use, Suspense } from 'react';
    import { ErrorBoundary } from 'react-error-boundary';
    import { fetchData } from './data.js';

    export default function App() {
        return (
            <ErrorBoundary fallback={<p>Could not fetch albums.</p>}>
                <Suspense fallback={<Loading />}>
                    <Albums />
                </Suspense>
            </ErrorBoundary>
        );
    }

    function Albums() {
        const albums = use(fetchData('/albums'));
        return (
            <ul>
                {albums.map(album => (
                    <li key={album.id}>
                        {album.title} ({album.year})
                    </li>
                ))}
            </ul>
        );
    }

    function Loading() {
        return <h2>Loading...</h2>;
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
        if (url === '/albums') {
            return await getAlbums();
        } else {
            throw Error('Not implemented');
        }
    }

    async function getAlbums() {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });

        return [{
            id: 13,
            title: 'Let It Be',
            year: 1970
        }, {
            id: 12,
            title: 'Abbey Road',
            year: 1969
        }, {
            id: 11,
            title: 'Yellow Submarine',
            year: 1969
        }, {
            id: 10,
            title: 'The Beatles',
            year: 1968
        }];
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.0.0",
        "react-dom": "19.0.0",
        "react-scripts": "^5.0.0",
        "react-error-boundary": "4.0.3"
      },
      "main": "/index.js"
    }
    ```

??? success "Решение"

    До `use` данные часто загружали в эффекте и обновляли состояние, когда они приходили. По сравнению с `use` так приходится вручную вести состояния загрузки и ошибки. Почему загрузку в эффекте лучше не делать, смотрите в [Вам может не понадобиться эффект](../../learn/you-might-not-need-an-effect.md#fetching-data).

    === "App.js"

        ```js

        import { useState, useEffect } from 'react';
        import { fetchAlbums } from './data.js';

        export default function App() {
            const [albums, setAlbums] = useState(null);
            const [isLoading, setIsLoading] = useState(true);
            const [error, setError] = useState(null);

            useEffect(() => {
                fetchAlbums()
                    .then(data => {
                        setAlbums(data);
                        setIsLoading(false);
                    })
                    .catch(err => {
                        setError(err);
                        setIsLoading(false);
                    });
            }, []);

            if (isLoading) {
                return <h2>Loading...</h2>;
            }

            if (error) {
                return <p>Error: {error.message}</p>;
            }

            return (
                <ul>
                    {albums.map(album => (
                        <li key={album.id}>
                            {album.title} ({album.year})
                        </li>
                    ))}
                </ul>
            );
        }
        ```

    === "data.js"

        ```js

        export async function fetchAlbums() {
            // Add a fake delay to make waiting noticeable.
            await new Promise(resolve => {
                setTimeout(resolve, 1000);
            });

            return [{
                id: 13,
                title: 'Let It Be',
                year: 1970
            }, {
                id: 12,
                title: 'Abbey Road',
                year: 1969
            }, {
                id: 11,
                title: 'Yellow Submarine',
                year: 1969
            }, {
                id: 10,
                title: 'The Beatles',
                year: 1968
            }];
        }
        ```

    ??? success "Решение"

!!!warning "Промисы, переданные в `use`, нужно кэшировать"

    Промисы, созданные во время рендера, создаются заново при каждом рендере. Из-за этого React снова и снова показывает фолбэк Suspense, и содержимое не появляется.

    ```js
    function Albums() {
      // 🔴 `fetch` creates a new Promise on every render.
      const albums = use(fetch('/albums'));
      // ...
    }
    ```

    Вместо этого передайте промис из кэша, [фреймворка с поддержкой Suspense](Suspense.md#suspense-enabled-frameworks) или серверного компонента:

    ```js
    // ✅ fetchData reads the Promise from a cache.
    const albums = use(fetchData('/albums'));
    ```

??? note "Почему промисы создаются заново при каждом рендере?"

    [React не сохраняет состояние рендеров, которые приостановились до монтирования](Suspense.md#caveats). После каждой приостановки React заново пробует рендер с нуля, поэтому любой промис, созданный во время рендера, создаётся снова.

    Промис легко нечаянно пересоздать во время рендера вот так:

    ```js
    function Albums() {
      // 🔴 `fetch` creates a new Promise on every render.
      const albums = use(fetch('/albums'));

      // 🔴 Uncached `async` function calls create a new Promise on every render.
      const albums = use((async () => {
        const res = await fetch('/albums');
        return res.json();
      })());

      // 🔴 Adding `.then` returns a new Promise on every render,
      // even if `fetchData` is cached.
      const albums = use(fetchData('/albums').then(res => res.json()));
      // ...
    }
    ```

    В идеале промисы создают до рендера: в обработчике события, загрузчике маршрута или серверном компоненте — и передают в компонент, который вызывает `use`. Ленивая загрузка во время рендера откладывает сетевые запросы и может создать водопады.

    ```js
    // ✅ fetchData reads the Promise from a cache.
    const albums = use(fetchData('/albums'));
    ```

### Кэширование промисов для клиентских компонентов {#caching-promises-for-client-components}

Промисы, переданные в `use` в клиентских компонентах, нужно кэшировать, чтобы между повторными рендерами переиспользовался один и тот же экземпляр. Если новый промис создаётся прямо в рендере, React будет показывать фолбэк Suspense при каждом повторном рендере.

```js
// ✅ Cache the Promise so the same one is reused across renders
let cache = new Map();

export function fetchData(url) {
  if (!cache.has(url)) {
    cache.set(url, getData(url));
  }
  return cache.get(url);
}
```

Функция `fetchData` возвращает один и тот же промис при каждом вызове с тем же URL. Когда `use` при повторном рендере получает тот же промис, он синхронно читает уже разрешённое значение и не приостанавливается.

!!!note "Примечание"

    Как кэшировать промисы, зависит от фреймворка, с которым вы используете Suspense. Обычно у фреймворков есть встроенное кэширование. Если фреймворка нет, подойдёт простой кэш на уровне модуля, как выше, или [источник данных с поддержкой Suspense](Suspense.md#what-activates-a-suspense-boundary).

В примере ниже клик по «Re-render» обновляет состояние в `App` и вызывает повторный рендер. Поскольку `fetchData` возвращает тот же закэшированный промис, `Albums` читает значение синхронно и не показывает фолбэк Suspense снова.

=== "App.js"

    ```js

    import { use, Suspense, useState } from 'react';
    import { fetchData } from './data.js';

    export default function App() {
        const [count, setCount] = useState(0);
        return (
            <>
                <button onClick={() => setCount(count + 1)}>
                    Re-render
                </button>
                <p>Render count: {count}</p>
                <Suspense fallback={<p>Loading...</p>}>
                    <Albums />
                </Suspense>
            </>
        );
    }

    function Albums() {
        const albums = use(fetchData('/albums'));
        return (
            <ul>
                {albums.map(album => (
                    <li key={album.id}>
                        {album.title} ({album.year})
                    </li>
                ))}
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
        if (url === '/albums') {
            return await getAlbums();
        } else {
            throw Error('Not implemented');
        }
    }

    async function getAlbums() {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });

        return [{
            id: 13,
            title: 'Let It Be',
            year: 1970
        }, {
            id: 12,
            title: 'Abbey Road',
            year: 1969
        }, {
            id: 11,
            title: 'Yellow Submarine',
            year: 1969
        }];
    }
    ```

<a id="how-to-implement-a-promise-cache"></a>

??? note "Как реализовать кэш промисов"

    Простой кэш хранит промис по ключу URL, чтобы между рендерами переиспользовался один экземпляр. Чтобы не показывать лишний фолбэк Suspense, когда данные уже есть, на промисе можно выставить поля `status` и `value` (или `reason`). React смотрит эти поля, когда вызывается `use`: если `status` равен `'fulfilled'`, он синхронно читает `value` и не приостанавливается. Если `status` равен `'rejected'`, он бросает `reason`. Если поля нет или оно равно `'pending'`, он приостанавливается.

    ```js
    let cache = new Map();

    function fetchData(url) {
      if (!cache.has(url)) {
        const promise = getData(url);
        promise.status = 'pending';
        promise.then(
          value => {
            promise.status = 'fulfilled';
            promise.value = value;
          },
          reason => {
            promise.status = 'rejected';
            promise.reason = reason;
          },
        );
        cache.set(url, promise);
      }
      return cache.get(url);
    }
    ```

    Это в первую очередь нужно авторам библиотек, которые строят слой данных, совместимый с Suspense. React сам выставит поле `status` у промисов, где его нет, но если выставить его заранее, лишний рендер не случится, когда данные уже доступны.

    Этот кэш — основа для [повторной загрузки данных](#re-fetching-data-in-client-components) (смена ключа кэша запускает новую загрузку) и [предзагрузки при наведении](#preloading-data-on-hover) (ранний вызов `fetchData` значит, что к моменту чтения через `use` промис уже может быть разрешён).

!!!warning "Не пропускайте вызов `use` из-за того, что промис уже завершился"

    В отличие от других хуков, `use` можно вызывать в условиях и циклах, но для самого промиса его нужно вызывать всегда. Никогда не читайте `promise.status` или `promise.value` напрямую, чтобы обойти `use`: всегда передавайте промис в `use` и дайте React разобраться.

    ```js
    // 🔴 Don't bypass `use` by reading promise status directly
    if (promise.status === 'fulfilled') {
      return promise.value;
    }
    const value = use(promise);
    ```

    ```js
    // ✅ Pass the promise to `use` and let React track the promise
    const value = use(promise);
    ```

    Такой обход может сломать оптимизации Suspense и возможности Suspense в React DevTools. `use(promise)` можно вызывать условно, но нельзя решать, вызывать ли `use(promise)`, по самому промису.

### Повторная загрузка данных в клиентских компонентах {#re-fetching-data-in-client-components}

Чтобы обновить данные по тому же URL (например, кнопкой «Refresh»), сбросьте запись кэша и начните новую загрузку внутри [`startTransition`](startTransition.md). Сохраните полученный промис в состоянии, чтобы вызвать повторный рендер. Пока новый промис ожидает, React продолжает показывать текущее содержимое, потому что обновление внутри перехода.

```js
function App() {
  const [albumsPromise, setAlbumsPromise] = useState(fetchData('/albums'));
  const [isPending, startTransition] = useTransition();

  function handleRefresh() {
    startTransition(() => {
      setAlbumsPromise(refetchData('/albums'));
    });
  }
  // ...
}
```

`refetchData` очищает старую запись кэша и начинает новую загрузку по тому же URL. Сохранение полученного промиса в состоянии вызывает повторный рендер внутри перехода. При повторном рендере `Albums` получает новый промис, и `use` приостанавливается на нём, а React продолжает показывать старое содержимое.

=== "App.js"

    ```js

    import { Suspense, useState, useTransition } from 'react';
    import { use } from 'react';
    import { fetchData, refetchData } from './data.js';

    export default function App() {
        const [albumsPromise, setAlbumsPromise] = useState(
            () => fetchData('/the-beatles/albums')
        );
        const [isPending, startTransition] = useTransition();

        function handleRefresh() {
            startTransition(() => {
                setAlbumsPromise(refetchData('/the-beatles/albums'));
            });
        }

        return (
            <>
                <button
                    onClick={handleRefresh}
                    disabled={isPending}
                >
                    {isPending ? 'Refreshing...' : 'Refresh'}
                </button>
                <div style={{ opacity: isPending ? 0.6 : 1 }}>
                    <Suspense fallback={<Loading />}>
                        <Albums albumsPromise={albumsPromise} />
                    </Suspense>
                </div>
            </>
        );
    }

    function Albums({ albumsPromise }) {
        const albums = use(albumsPromise);
        return (
            <ul>
                {albums.map(album => (
                    <li key={album.id}>
                        {album.title} ({album.year})
                    </li>
                ))}
            </ul>
        );
    }

    function Loading() {
        return <h2>Loading...</h2>;
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

    export function refetchData(url) {
        cache.delete(url);
        return fetchData(url);
    }

    async function getData(url) {
        if (url.startsWith('/the-beatles/albums')) {
            return await getAlbums();
        } else {
            throw Error('Not implemented');
        }
    }

    async function getAlbums() {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });

        return [{
            id: 13,
            title: 'Let It Be',
            year: 1970
        }, {
            id: 12,
            title: 'Abbey Road',
            year: 1969
        }, {
            id: 11,
            title: 'Yellow Submarine',
            year: 1969
        }, {
            id: 10,
            title: 'The Beatles',
            year: 1968
        }, {
            id: 9,
            title: 'Magical Mystery Tour',
            year: 1967
        }];
    }
    ```

=== "styles.css"

    ```css

    button { margin-bottom: 10px; }
    ```

!!!note "Примечание"

    Фреймворки с поддержкой Suspense обычно дают свои механизмы кэша и инвалидации. Свой кэш выше полезен, чтобы понять приём, но на практике лучше решение для загрузки данных вашего фреймворка.

### Предзагрузка данных при наведении {#preloading-data-on-hover}

Данные можно начать грузить до того, как они понадобятся, вызвав `fetchData` при наведении. Поскольку `fetchData` кэширует промис, к моменту клика данные уже могут быть на месте. Если к моменту чтения через `use` промис разрешился, React сразу рендерит компонент и не показывает фолбэк Suspense.

```js
<button
  onMouseEnter={() => fetchData(`/${id}/albums`)}
  onClick={() => {
    startTransition(() => {
      setArtistId(id);
    });
  }}
>
```

В этом примере наведение на кнопку исполнителя начинает в фоне грузить его альбомы. Если не наводить курсор заранее, клик показывает фолбэк загрузки. Подержите курсор на кнопке немного перед кликом и сравните.

=== "App.js"

    ```js

    import { Suspense, useState, useTransition } from 'react';
    import Albums from './Albums.js';
    import { fetchData } from './data.js';

    export default function App() {
        const [artistId, setArtistId] = useState('the-beatles');
        const [isPending, startTransition] = useTransition();

        return (
            <>
                <div>
                    {['the-beatles', 'led-zeppelin', 'pink-floyd'].map(id => (
                        <button
                            key={id}
                            onMouseEnter={() => {
                                fetchData(`/${id}/albums`);
                            }}
                            onClick={() => {
                                startTransition(() => {
                                    setArtistId(id);
                                });
                            }}
                        >
                            {id === 'the-beatles' ? 'The Beatles' :
                              id === 'led-zeppelin' ? 'Led Zeppelin' :
                              'Pink Floyd'}
                        </button>
                    ))}
                </div>
                <Suspense key={artistId} fallback={<Loading />}>
                    <Albums artistId={artistId} />
                </Suspense>
            </>
        );
    }

    function Loading() {
        return <h2>Loading...</h2>;
    }
    ```

=== "Albums.js"

    ```js

    import { use } from 'react';
    import { fetchData } from './data.js';

    export default function Albums({ artistId }) {
        const albums = use(fetchData(`/${artistId}/albums`));
        return (
            <ul>
                {albums.map(album => (
                    <li key={album.id}>
                        {album.title} ({album.year})
                    </li>
                ))}
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
            const promise = getData(url);
            // Set status fields so React can read the value
            // synchronously if the Promise resolves before
            // `use` is called (e.g. when preloading on hover).
            promise.status = 'pending';
            promise.then(
                value => {
                    promise.status = 'fulfilled';
                    promise.value = value;
                },
                reason => {
                    promise.status = 'rejected';
                    promise.reason = reason;
                },
            );
            cache.set(url, promise);
        }
        return cache.get(url);
    }

    async function getData(url) {
        if (url.startsWith('/the-beatles/albums')) {
            return await getAlbums('the-beatles');
        } else if (url.startsWith('/led-zeppelin/albums')) {
            return await getAlbums('led-zeppelin');
        } else if (url.startsWith('/pink-floyd/albums')) {
            return await getAlbums('pink-floyd');
        } else {
            throw Error('Not implemented');
        }
    }

    async function getAlbums(artistId) {
        // Add a fake delay to make waiting noticeable.
        await new Promise(resolve => {
            setTimeout(resolve, 800);
        });

        if (artistId === 'the-beatles') {
            return [{
                id: 13,
                title: 'Let It Be',
                year: 1970
            }, {
                id: 12,
                title: 'Abbey Road',
                year: 1969
            }, {
                id: 11,
                title: 'Yellow Submarine',
                year: 1969
            }];
        } else if (artistId === 'led-zeppelin') {
            return [{
                id: 10,
                title: 'Coda',
                year: 1982
            }, {
                id: 9,
                title: 'In Through the Out Door',
                year: 1979
            }, {
                id: 8,
                title: 'Presence',
                year: 1976
            }];
        } else {
            return [{
                id: 7,
                title: 'The Wall',
                year: 1979
            }, {
                id: 6,
                title: 'Animals',
                year: 1977
            }, {
                id: 5,
                title: 'Wish You Were Here',
                year: 1975
            }];
        }
    }
    ```

=== "styles.css"

    ```css

    button { margin-right: 10px; }
    ```

### Потоковая передача данных от сервера к клиенту {#streaming-data-from-server-to-client}

Данные могут передаваться от сервера к клиенту путем передачи Promise в качестве реквизита от серверного компонента к клиентскому компоненту.

```js
import { fetchMessage } from './lib.js';
import { Message } from './message.js';

export default function App() {
    const messagePromise = fetchMessage();
    return (
        <Suspense fallback={<p>waiting for message...</p>}>
            <Message messagePromise={messagePromise} />
        </Suspense>
    );
}
```

Затем клиентский компонент принимает полученное обещание в качестве реквизита и передает его хуку `use`. Это позволяет клиентскому компоненту прочитать значение из обещания, которое было первоначально создано серверным компонентом.

```js
// message.js
'use client';

import { use } from 'react';

export function Message({ messagePromise }) {
    const messageContent = use(messagePromise);
    return <p>Here is the message: {messageContent}</p>;
}
```

Поскольку `Message` обернут в [`Suspense`](Suspense.md), fallback будет отображаться до тех пор, пока Promise не будет разрешен. Когда обещание будет разрешено, значение будет считано хуком `use` и компонент `Message` заменит фаллбэк Suspense.

=== "message.js"

    ```js
    'use client';

    import { use, Suspense } from 'react';

    function Message({ messagePromise }) {
    	const messageContent = use(messagePromise);
    	return <p>Here is the message: {messageContent}</p>;
    }

    export function MessageContainer({ messagePromise }) {
    	return (
    		<Suspense
    			fallback={<p>⌛Downloading message...</p>}
    		>
    			<Message messagePromise={messagePromise} />
    		</Suspense>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/8dg646?view=Editor+%2B+Preview&module=%2Fsrc%2Fmessage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="happy-shadow-8dg646" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note "Сериализуемость значений"

    При передаче Promise от серверного компонента к клиентскому компоненту его разрешенное значение должно быть сериализуемым для передачи между сервером и клиентом. Типы данных, такие как функции, не являются сериализуемыми и не могут быть разрешенным значением такого промиса.

!!!info "Как разрешить промис в серверном или клиентском компоненте?"

    Промис можно передать из серверного компонента в клиентский компонент и разрешить его в клиентском компоненте с помощью хука `use`. Вы также можете разрешить промис в серверном компоненте с помощью `await` и передать необходимые данные клиентскому компоненту в качестве свойства.

    ```js
    export default function App() {
    	const messageContent = await fetchMessage();
    	return <Message messageContent={messageContent} />
    }
    ```

    Но использование `await` в компоненте [Server Component](components.md#server-components) заблокирует его рендеринг до завершения оператора `await`. Передача промиса от серверного компонента клиентскому компоненту не позволяет промису блокировать отрисовку серверного компонента.

### Отображение ошибки с помощью границы ошибки {#displaying-an-error-with-an-error-boundary}

Если промис, переданный в `use`, отклонён, ошибка всплывает к ближайшей [границе ошибки](Component.md#catching-rendering-errors-with-an-error-boundary). Оберните компонент, который вызывает `use`, в границу ошибки, чтобы показать фолбэк, когда промис отклонён.

В примере ниже `fetchData` отклоняется при первой попытке и успешно завершается при повторе. Граница ошибки перехватывает отказ и показывает фолбэк с кнопкой «Try again».

=== "App.js"

    ```js

    import { use, Suspense, useState, startTransition } from "react";
    import { ErrorBoundary } from "react-error-boundary";
    import { fetchData, refetchData } from "./data.js";

    export default function App() {
        const [albumsPromise, setAlbumsPromise] = useState(
            () => fetchData('/the-beatles/albums')
        );

        function handleRetry() {
            startTransition(() => {
                setAlbumsPromise(refetchData('/the-beatles/albums'));
            });
        }

        return (
            <ErrorBoundary
                resetKeys={[albumsPromise]}
                fallbackRender={() => (
                    <>
                        <p>⚠️ Something went wrong loading the albums.</p>
                        <button onClick={handleRetry}>Try again</button>
                    </>
                )}
            >
                <Suspense fallback={<p>Loading...</p>}>
                    <Albums albumsPromise={albumsPromise} />
                </Suspense>
            </ErrorBoundary>
        );
    }

    function Albums({ albumsPromise }) {
        const albums = use(albumsPromise);
        return (
            <ul>
                {albums.map(album => (
                    <li key={album.id}>
                        {album.title} ({album.year})
                    </li>
                ))}
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
    let retried = false;

    export function fetchData(url) {
        if (!cache.has(url)) {
            cache.set(url, getData(url));
        }
        return cache.get(url);
    }

    export function refetchData(url) {
        cache.delete(url);
        retried = true;
        return fetchData(url);
    }

    async function getData(url) {
        // Add a fake delay to make the loading state visible.
        await new Promise(resolve => setTimeout(resolve, 1000));
        if (url === '/the-beatles/albums') {
            // Fail the first attempt to demonstrate the Error Boundary,
            // then succeed on retry.
            if (!retried) {
                throw new Error('Example Error: Failed to fetch albums');
            }
            return [{
                id: 13,
                title: 'Let It Be',
                year: 1970
            }, {
                id: 12,
                title: 'Abbey Road',
                year: 1969
            }, {
                id: 11,
                title: 'Yellow Submarine',
                year: 1969
            }, {
                id: 10,
                title: 'The Beatles',
                year: 1968
            }];
        }
        throw new Error('Not implemented');
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.0.0",
        "react-dom": "19.0.0",
        "react-scripts": "^5.0.0",
        "react-error-boundary": "4.0.3"
      },
      "main": "/index.js"
    }
    ```

## Использование (браузер) {#usage-browser}

### Рендер компонента только в браузере {#rendering-a-component-only-in-the-browser}

Передайте в `use` значение, которое вернул [`browser`](../react-dom/browser.md), внутри компонента, который должен рендериться только в браузере.

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

Во время серверного рендеринга `use(browser())` приостанавливает компонент, и React включает в HTML фолбэк ближайшей границы приостановки. В браузере `use(browser())` возвращает `undefined`, и сохранённый черновик рендерится как обычно.

### Работа с отклоненными промисами {#dealing-with-rejected-promises}

В некоторых случаях промис, переданный в `use`, может быть отклонен. Вы можете обработать отклоненные промисы следующим образом:

1.  [Отображение ошибки для пользователей с границей ошибки](#displaying-an-error-to-users-with-error-boundary).
2.  [Предоставить альтернативное значение с помощью `Promise.catch`](#providing-an-alternative-value-with-promise-catch)

!!!warning "try-catch"

    `use` нельзя вызывать в блоке `try-catch`. Вместо блока `try-catch` [оберните ваш компонент в границу ошибки](#displaying-an-error-to-users-with-error-boundary) или [предоставьте альтернативное значение для использования в методе `.catch` промиса](#providing-an-alternative-value-with-promise-catch).

#### Отображение ошибки для пользователей с границей ошибки {#displaying-an-error-to-users-with-error-boundary}

Если вы хотите отобразить ошибку для пользователей, когда промис отклоняется, вы можете использовать [границу ошибки](Component.md#catching-rendering-errors-with-an-error-boundary). Чтобы использовать границу ошибки, оберните компонент, в котором вы вызываете хук `use`, в границу ошибки. Если промис, переданный в `use`, будет отклонен, то будет отображен обратный вариант границы ошибки.

=== "message.js"

    ```js
    'use client';

    import { use, Suspense } from 'react';
    import { ErrorBoundary } from 'react-error-boundary';

    export function MessageContainer({ messagePromise }) {
    	return (
    		<ErrorBoundary
    			fallback={<p>⚠️Something went wrong</p>}
    		>
    			<Suspense
    				fallback={<p>⌛Downloading message...</p>}
    			>
    				<Message messagePromise={messagePromise} />
    			</Suspense>
    		</ErrorBoundary>
    	);
    }

    function Message({ messagePromise }) {
    	const content = use(messagePromise);
    	return <p>Here is the message: {content}</p>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dzl7jd?view=Editor+%2B+Preview&module=%2Fsrc%2Fmessage.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="funny-cherry-dzl7jd" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### Предоставление альтернативного значения с помощью `Promise.catch` {#providing-an-alternative-value-with-promise-catch}

Если вы хотите предоставить альтернативное значение, когда промис, переданный в `use`, будет отклонен, вы можете использовать метод [`catch`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch) промиса.

```js hl_lines="8"
import { Message } from './message.js';

export default function App() {
    const messagePromise = new Promise(
        (resolve, reject) => {
            reject();
        }
    ).catch(() => {
        return 'no new message found.';
    });

    return (
        <Suspense fallback={<p>waiting for message...</p>}>
            <Message messagePromise={messagePromise} />
        </Suspense>
    );
}
```

Чтобы использовать метод `catch` промиса, вызовите `catch` на объекте промиса. `catch` принимает единственный аргумент: функцию, которая принимает в качестве аргумента сообщение об ошибке. То, что будет возвращено функцией, переданной в `catch`, будет использовано в качестве разрешенного значения промиса.

## Устранение неполадок {#troubleshooting}

### "Suspense Exception: This is not a real error!" {#suspense-exception-error}

Вы либо вызываете `use` вне компонента React или функции Hook, либо вызываете `use` в блоке try-catch. Если вы вызываете `use` внутри блока try-catch, оберните ваш компонент в границу ошибки или вызовите `catch` промиса, чтобы поймать ошибку и разрешить промис другим значением. [См. эти примеры](#dealing-with-rejected-promises).

Если вы вызываете `use` вне компонента React или функции Hook, перенесите вызов `use` в компонент React или функцию Hook.

```jsx
function MessageComponent({messagePromise}) {
  function download() {
    // ❌ the function calling `use` is not a Component or Hook
    const message = use(messagePromise);
    // ...
```

Вместо этого вызывайте `use` вне закрытий компонентов, если функция, вызывающая `use`, является компонентом или хуком.

```jsx
function MessageComponent({messagePromise}) {
  // ✅ `use` is being called from a component.
  const message = use(messagePromise);
  // ...
```

### Предупреждение: «A component was suspended by an uncached promise» {#uncached-promise-error}

Промис, переданный в `use`, не закэширован, поэтому React не может переиспользовать его между повторными рендерами.

Так часто бывает, если `fetch` или `async`-функцию вызывают прямо в рендере:

```js
function Albums() {
  // 🔴 This creates a new Promise on every render
  const albums = use(fetch('/albums'));
  // ...
}
```

Чтобы это исправить, закэшируйте промис, чтобы переиспользовался один и тот же экземпляр:

```js
// ✅ fetchData returns the same Promise for the same URL
const albums = use(fetchData('/albums'));
```

Подробнее в разделе [Кэширование промисов для клиентских компонентов](#caching-promises-for-client-components).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/use](https://react.dev/reference/react/use)</small>
