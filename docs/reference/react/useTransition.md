---
description: useTransition - это хук React, который позволяет обновлять состояние без блокировки пользовательского интерфейса
---

# useTransition

<big>**`useTransition`** - это хук React, который позволяет обновлять состояние без блокировки пользовательского интерфейса.</big>

```js
const [isPending, startTransition] = useTransition();
```

## Описание {#reference}

### `useTransition()` {#usetransition}

Вызовите `useTransition` на верхнем уровне вашего компонента, чтобы пометить некоторые обновления состояния как переходы.

```js
import { useTransition } from 'react';

function TabContainer() {
    const [isPending, startTransition] = useTransition();
    // ...
}
```

#### Параметры {#parameters}

`useTransition` не принимает никаких параметров.

#### Возвращаемое значение {#returns}

`useTransition` возвращает массив, содержащий ровно два элемента:

1.  Флаг `isPending`, который сообщает, есть ли ожидающий переход.
2.  Функция `startTransition`, позволяющая пометить обновление состояния как переход.

### Функция `startTransition` {#starttransition}

Функция `startTransition`, возвращаемая `useTransition`, позволяет пометить обновление состояния как переход.

```js hl_lines="6 8"
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

<a id="functions-called-in-starttransition-are-called-actions"></a>

!!!note "Функции, вызываемые в `startTransition`, называются действиями"

    Функция, переданная в `startTransition`, называется «действием». По соглашению любой колбэк, который вызывают внутри `startTransition` (например, колбэк в пропсах), стоит называть `action` или добавлять суффикс `Action`:

    ```js hl_lines="1 9"
    function SubmitButton({ submitAction }) {
      const [isPending, startTransition] = useTransition();

      return (
        <button
          disabled={isPending}
          onClick={() => {
            startTransition(async () => {
              await submitAction();
            });
          }}
        >
          Submit
        </button>
      );
    }

    ```

#### Параметры {#starttransition-parameters}

-   `scope`: Функция, которая обновляет некоторое состояние, вызывая одну или несколько функций [`set`](useState.md). React немедленно вызывает `scope` без параметров и помечает все обновления состояния, запланированные синхронно во время вызова функции `scope`, как переходы. Они будут неблокирующими и не будут отображать нежелательные индикаторы загрузки.

#### Возвращаемое значение {#starttransition-returns}

`startTransition` ничего не возвращает.

#### Ограничения {#starttransition-caveats}

-   `useTransition` - это хук, поэтому его можно вызывать только внутри компонентов или пользовательских хуков. Если вам нужно запустить переход в другом месте (например, из библиотеки данных), вызовите вместо этого отдельный [`startTransition`](startTransition.md).

-   Вы можете обернуть обновление в переход, только если у вас есть доступ к функции `set` этого состояния. Если вы хотите запустить переход в ответ на какой-то пропс или пользовательское значение Hook, попробуйте вместо этого использовать [`useDeferredValue`](useDeferredValue.md).

-   Функция, которую вы передаете в `startTransition`, должна быть синхронной. React немедленно выполняет эту функцию, помечая все обновления состояния, которые происходят во время ее выполнения, как переходы. Если вы попытаетесь выполнить дополнительные обновления состояния позже (например, во время таймаута), они не будут помечены как переходы.

-   Обновление состояния, помеченное как переход, будет прерываться другими обновлениями состояния. Например, если вы обновите компонент графика внутри перехода, а затем начнете вводить текст в поле ввода, когда график находится в середине повторного рендеринга, React перезапустит работу по рендерингу компонента графика после обработки обновления ввода.

-   Обновления переходов нельзя использовать для управления текстовыми вводами.

-   При наличии нескольких текущих переходов React в настоящее время собирает их вместе. Это ограничение, которое, вероятно, будет устранено в будущем выпуске.

## Использование {#usage}

### Неблокирующие обновления с помощью действий {#perform-non-blocking-updates-with-actions}

Вызовите `useTransition` в начале компонента, чтобы создавать действия и читать состояние ожидания:

```js hl_lines="4"
import {useState, useTransition} from 'react';

function CheckoutForm() {
  const [isPending, startTransition] = useTransition();
  // ...
}
```

`useTransition` возвращает массив ровно из двух элементов:

1. Флаг `isPending`, который сообщает, есть ли ожидающий переход.
2. Функция `startTransition`, которая позволяет создать действие.

Чтобы начать переход, передайте функцию в `startTransition` так:

```js
import {useState, useTransition} from 'react';
import {updateQuantity} from './api';

function CheckoutForm() {
  const [isPending, startTransition] = useTransition();
  const [quantity, setQuantity] = useState(1);

  function onSubmit(newQuantity) {
    startTransition(async function () {
      const savedQuantity = await updateQuantity(newQuantity);
      startTransition(() => {
        setQuantity(savedQuantity);
      });
    });
  }
  // ...
}
```

Функция, переданная в `startTransition`, называется «действием» (Action). Внутри действия можно обновлять состояние и (необязательно) выполнять побочные эффекты, и эта работа пойдёт в фоне, не блокируя действия пользователя на странице. В переход может входить несколько действий, и пока переход идёт, интерфейс остаётся отзывчивым. Например, если пользователь нажал вкладку, а потом передумал и нажал другую, второй клик обработается сразу, не дожидаясь окончания первого обновления.

Чтобы показать пользователю, что переход ещё идёт, состояние `isPending` становится `true` при первом вызове `startTransition` и остаётся `true`, пока не завершатся все действия и пользователю не покажут итоговое состояние. Переходы дожидаются побочных эффектов в действиях, чтобы [не показывать нежелательные индикаторы загрузки](#preventing-unwanted-loading-indicators), а немедленную обратную связь во время перехода можно дать через `useOptimistic`.

## Примеры {#recipes}

#### Обновление количества в действии {#updating-the-quantity-in-an-action}

В этом примере функция `updateQuantity` имитирует запрос к серверу, чтобы обновить количество товара в корзине. Функция *искусственно замедлена*, чтобы запрос занимал не меньше секунды.

Быстро измените количество несколько раз. Обратите внимание: состояние ожидания у «Total» видно, пока идут любые запросы, а «Total» обновляется только после последнего запроса. Поскольку обновление внутри действия, «quantity» можно продолжать менять, пока запрос ещё выполняется.

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "beta",
        "react-dom": "beta"
      },
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test --env=jsdom",
        "eject": "react-scripts eject"
      }
    }
    ```

=== "App.js"

    ```js

    import { useState, useTransition } from "react";
    import { updateQuantity } from "./api";
    import Item from "./Item";
    import Total from "./Total";

    export default function App({}) {
        const [quantity, setQuantity] = useState(1);
        const [isPending, startTransition] = useTransition();

        const updateQuantityAction = async newQuantity => {
            // To access the pending state of a transition,
            // call startTransition again.
            startTransition(async () => {
                const savedQuantity = await updateQuantity(newQuantity);
                startTransition(() => {
                    setQuantity(savedQuantity);
                });
            });
        };

        return (
            <div>
                <h1>Checkout</h1>
                <Item action={updateQuantityAction}/>
                <hr />
                <Total quantity={quantity} isPending={isPending} />
            </div>
        );
    }
    ```

=== "Item.js"

    ```js

    import { startTransition } from "react";

    export default function Item({action}) {
        function handleChange(event) {
            // To expose an action prop, await the callback in startTransition.
            startTransition(async () => {
                await action(event.target.value);
            })
        }
        return (
            <div className="item">
                <span>Eras Tour Tickets</span>
                <label htmlFor="name">Quantity: </label>
                <input
                    type="number"
                    onChange={handleChange}
                    defaultValue={1}
                    min={1}
                />
            </div>
        )
    }
    ```

=== "Total.js"

    ```js

    const intl = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="total">
                <span>Total:</span>
                <span>
                    {isPending ? "🌀 Updating..." : `${intl.format(quantity * 9999)}`}
                </span>
            </div>
        )
    }
    ```

=== "api.js"

    ```js

    export async function updateQuantity(newQuantity) {
        return new Promise((resolve, reject) => {
            // Simulate a slow network request.
            setTimeout(() => {
                resolve(newQuantity);
            }, 2000);
        });
    }
    ```

=== "styles.css"

    ```css

    .item {
      display: flex;
      align-items: center;
      justify-content: start;
    }

    .item label {
      flex: 1;
      text-align: right;
    }

    .item input {
      margin-left: 4px;
      width: 60px;
      padding: 4px;
    }

    .total {
      height: 50px;
      line-height: 25px;
      display: flex;
      align-content: center;
      justify-content: space-between;
    }
    ```

Это базовый пример того, как работают действия, но он не обрабатывает запросы, которые завершаются не по порядку. Если быстро менять количество несколько раз, предыдущие запросы могут закончиться после более поздних, и количество обновится не в том порядке. Это известное ограничение, которое исправят в будущем (см. [Устранение неполадок](#my-state-updates-in-transitions-are-out-of-order) ниже).

Для обычных случаев React даёт готовые абстракции:
- [`useActionState`](useActionState.md)
- [действия `<form>`](../react-dom/components/form.md)
- [серверные функции](../rsc/server-functions.md)

Они сами следят за порядком запросов. Если на переходах вы строите свои хуки или библиотеки для асинхронных переходов состояния, контроля больше, но порядок нужно обрабатывать самим.

??? success "Решение"

    В этом примере `updateQuantity` тоже имитирует запрос к серверу, чтобы обновить количество товара в корзине. Функция *искусственно замедлена*, чтобы запрос занимал не меньше секунды.

    Быстро измените количество несколько раз. Обратите внимание: состояние ожидания у «Total» видно, пока идёт любой запрос, но «Total» обновляется несколько раз — по одному на каждый клик по «quantity»:

    === "package.js"

        ```json

        {
          "dependencies": {
            "react": "beta",
            "react-dom": "beta"
          },
          "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test --env=jsdom",
            "eject": "react-scripts eject"
          }
        }
        ```

    === "App.js"

        ```js

        import { useState } from "react";
        import { updateQuantity } from "./api";
        import Item from "./Item";
        import Total from "./Total";

        export default function App({}) {
            const [quantity, setQuantity] = useState(1);
            const [isPending, setIsPending] = useState(false);

            const onUpdateQuantity = async newQuantity => {
                // Manually set the isPending State.
                setIsPending(true);
                const savedQuantity = await updateQuantity(newQuantity);
                setIsPending(false);
                setQuantity(savedQuantity);
            };

            return (
                <div>
                    <h1>Checkout</h1>
                    <Item onUpdateQuantity={onUpdateQuantity}/>
                    <hr />
                    <Total quantity={quantity} isPending={isPending} />
                </div>
            );
        }

        ```

    === "Item.js"

        ```js

        export default function Item({onUpdateQuantity}) {
            function handleChange(event) {
                onUpdateQuantity(event.target.value);
            }
            return (
                <div className="item">
                    <span>Eras Tour Tickets</span>
                    <label htmlFor="name">Quantity: </label>
                    <input
                        type="number"
                        onChange={handleChange}
                        defaultValue={1}
                        min={1}
                    />
                </div>
            )
        }
        ```

    === "Total.js"

        ```js

        const intl = new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD"
        });

        export default function Total({quantity, isPending}) {
            return (
                <div className="total">
                    <span>Total:</span>
                    <span>
                        {isPending ? "🌀 Updating..." : `${intl.format(quantity * 9999)}`}
                    </span>
                </div>
            )
        }
        ```

    === "api.js"

        ```js

        export async function updateQuantity(newQuantity) {
            return new Promise((resolve, reject) => {
                // Simulate a slow network request.
                setTimeout(() => {
                    resolve(newQuantity);
                }, 2000);
            });
        }
        ```

    === "styles.css"

        ```css

        .item {
          display: flex;
          align-items: center;
          justify-content: start;
        }

        .item label {
          flex: 1;
          text-align: right;
        }

        .item input {
          margin-left: 4px;
          width: 60px;
          padding: 4px;
        }

        .total {
          height: 50px;
          line-height: 25px;
          display: flex;
          align-content: center;
          justify-content: space-between;
        }
        ```

    Обычное решение этой проблемы — не давать пользователю менять значение, пока количество обновляется:

    === "package.js"

        ```json

        {
          "dependencies": {
            "react": "beta",
            "react-dom": "beta"
          },
          "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test --env=jsdom",
            "eject": "react-scripts eject"
          }
        }
        ```

    === "App.js"

        ```js

        import { useState, useTransition } from "react";
        import { updateQuantity } from "./api";
        import Item from "./Item";
        import Total from "./Total";

        export default function App({}) {
            const [quantity, setQuantity] = useState(1);
            const [isPending, setIsPending] = useState(false);

            const onUpdateQuantity = async event => {
                const newQuantity = event.target.value;
                // Manually set the isPending state.
                setIsPending(true);
                const savedQuantity = await updateQuantity(newQuantity);
                setIsPending(false);
                setQuantity(savedQuantity);
            };

            return (
                <div>
                    <h1>Checkout</h1>
                    <Item isPending={isPending} onUpdateQuantity={onUpdateQuantity}/>
                    <hr />
                    <Total quantity={quantity} isPending={isPending} />
                </div>
            );
        }

        ```

    === "Item.js"

        ```js

        export default function Item({isPending, onUpdateQuantity}) {
            return (
                <div className="item">
                    <span>Eras Tour Tickets</span>
                    <label htmlFor="name">Quantity: </label>
                    <input
                        type="number"
                        disabled={isPending}
                        onChange={onUpdateQuantity}
                        defaultValue={1}
                        min={1}
                    />
                </div>
            )
        }
        ```

    === "Total.js"

        ```js

        const intl = new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD"
        });

        export default function Total({quantity, isPending}) {
            return (
                <div className="total">
                    <span>Total:</span>
                    <span>
                        {isPending ? "🌀 Updating..." : `${intl.format(quantity * 9999)}`}
                    </span>
                </div>
            )
        }
        ```

    === "api.js"

        ```js

        export async function updateQuantity(newQuantity) {
            return new Promise((resolve, reject) => {
                // Simulate a slow network request.
                setTimeout(() => {
                    resolve(newQuantity);
                }, 2000);
            });
        }
        ```

    === "styles.css"

        ```css

        .item {
          display: flex;
          align-items: center;
          justify-content: start;
        }

        .item label {
          flex: 1;
          text-align: right;
        }

        .item input {
          margin-left: 4px;
          width: 60px;
          padding: 4px;
        }

        .total {
          height: 50px;
          line-height: 25px;
          display: flex;
          align-content: center;
          justify-content: space-between;
        }
        ```

    Так приложение кажется медленным: пользователю приходится ждать при каждом изменении количества. Более сложную обработку можно написать вручную, чтобы интерфейс оставался отзывчивым, но действия закрывают этот случай простым встроенным API.

    ??? success "Решение"

### Проп `action` у компонентов {#exposing-action-props-from-components}

Компонент может отдать наружу проп `action`, чтобы родитель вызвал действие.

Например, этот `TabButton` оборачивает логику `onClick` в проп `action`:

```js hl_lines="8-12"
export default function TabButton({ action, children, isActive }) {
  const [isPending, startTransition] = useTransition();
  if (isActive) {
    return <b>{children}</b>
  }
  return (
    <button onClick={() => {
      startTransition(async () => {
        // await the action that's passed in.
        // This allows it to be either sync or async.
        await action();
      });
    }}>
      {children}
    </button>
  );
}
```

Поскольку родитель обновляет своё состояние внутри `action`, это обновление помечается как переход. Можно нажать «Posts», а сразу затем «Contact», и это не заблокирует действия пользователя:

=== "js"

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
                    action={() => setTab('about')}
                >
                    About
                </TabButton>
                <TabButton
                    isActive={tab === 'posts'}
                    action={() => setTab('posts')}
                >
                    Posts (slow)
                </TabButton>
                <TabButton
                    isActive={tab === 'contact'}
                    action={() => setTab('contact')}
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

    export default function TabButton({ action, children, isActive }) {
        const [isPending, startTransition] = useTransition();
        if (isActive) {
            return <b>{children}</b>
        }
        if (isPending) {
            return <b className="pending">{children}</b>;
        }
        return (
            <button onClick={async () => {
                startTransition(async () => {
                    // await the action that's passed in.
                    // This allows it to be either sync or async.
                    await action();
                });
            }}>
                {children}
            </button>
        );
    }
    ```

=== "AboutTab.js"

    ```js

    export default function AboutTab() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "PostsTab.js"

    ```js hl_lines="19 20"

    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
        // Log once. The actual slowdown is inside SlowPost.
        console.log('[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />');

        let items = [];
        for (let i = 0; i < 500; i++) {
            items.push(<SlowPost key={i} index={i} />);
        }
        return (
            <ul className="items">
                {items}
            </ul>
        );
    });

    function SlowPost({ index }) {
        let startTime = performance.now();
        while (performance.now() - startTime < 1) {
            // Do nothing for 1 ms per item to emulate extremely slow code
        }

        return (
            <li className="item">
                Post #{index + 1}
            </li>
        );
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js

    export default function ContactTab() {
        return (
            <>
                <p>
                    You can find me online here:
                </p>
                <ul>
                    <li>admin@mysite.com</li>
                    <li>+123456789</li>
                </ul>
            </>
        );
    }
    ```

=== "styles.css"

    ```css

    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    .items {
      max-height: 300px;
      overflow: auto;
    }
    ```

!!!note "Примечание"

    Если компонент отдаёт наружу проп `action`, его нужно `await`-ить внутри перехода.

    Тогда колбэк `action` может быть и синхронным, и асинхронным, и не нужен ещё один `startTransition`, чтобы обернуть `await` в действии.

### Отображение визуального состояния ожидания {#displaying-a-pending-visual-state}

Булево значение `isPending`, которое возвращает `useTransition`, показывает пользователю, что переход ещё идёт. Например, у кнопки вкладки может быть особое визуальное состояние «pending»:

```js hl_lines="4-6"
function TabButton({ action, children, isActive }) {
  const [isPending, startTransition] = useTransition();
  // ...
  if (isPending) {
    return <b className="pending">{children}</b>;
  }
  // ...
```

Обратите внимание: клик по «Posts» теперь ощущается отзывчивее, потому что сама кнопка вкладки обновляется сразу:

=== "js"

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
                    action={() => setTab('about')}
                >
                    About
                </TabButton>
                <TabButton
                    isActive={tab === 'posts'}
                    action={() => setTab('posts')}
                >
                    Posts (slow)
                </TabButton>
                <TabButton
                    isActive={tab === 'contact'}
                    action={() => setTab('contact')}
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

    export default function TabButton({ action, children, isActive }) {
        const [isPending, startTransition] = useTransition();
        if (isActive) {
            return <b>{children}</b>
        }
        if (isPending) {
            return <b className="pending">{children}</b>;
        }
        return (
            <button onClick={() => {
                startTransition(async () => {
                    await action();
                });
            }}>
                {children}
            </button>
        );
    }
    ```

=== "AboutTab.js"

    ```js

    export default function AboutTab() {
        return (
            <p>Welcome to my profile!</p>
        );
    }
    ```

=== "PostsTab.js"

    ```js hl_lines="19 20"

    import { memo } from 'react';

    const PostsTab = memo(function PostsTab() {
        // Log once. The actual slowdown is inside SlowPost.
        console.log('[ARTIFICIALLY SLOW] Rendering 500 <SlowPost />');

        let items = [];
        for (let i = 0; i < 500; i++) {
            items.push(<SlowPost key={i} index={i} />);
        }
        return (
            <ul className="items">
                {items}
            </ul>
        );
    });

    function SlowPost({ index }) {
        let startTime = performance.now();
        while (performance.now() - startTime < 1) {
            // Do nothing for 1 ms per item to emulate extremely slow code
        }

        return (
            <li className="item">
                Post #{index + 1}
            </li>
        );
    }

    export default PostsTab;
    ```

=== "ContactTab.js"

    ```js

    export default function ContactTab() {
        return (
            <>
                <p>
                    You can find me online here:
                </p>
                <ul>
                    <li>admin@mysite.com</li>
                    <li>+123456789</li>
                </ul>
            </>
        );
    }
    ```

=== "styles.css"

    ```css

    button { margin-right: 10px }
    b { display: inline-block; margin-right: 10px; }
    .pending { color: #777; }
    .items {
      max-height: 300px;
      overflow: auto;
    }
    ```


### Пометка обновления состояния как неблокирующего перехода {#marking-a-state-update-as-a-non-blocking-transition}

Вызовите `useTransition` на верхнем уровне вашего компонента, чтобы пометить обновление состояния как неблокирующий _переход_.

```js
import { useState, useTransition } from 'react';

function TabContainer() {
    const [isPending, startTransition] = useTransition();
    // ...
}
```

`useTransition` возвращает массив, содержащий ровно два элемента:

1.  Флаг `isPending`, который сообщает, есть ли ожидающий переход.
2.  `startTransition` функция, которая позволяет отметить обновление состояния как переход.

Вы можете пометить обновление состояния как переход следующим образом:

```js hl_lines="6 8"
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

Переходы позволяют сохранить отзывчивость обновлений пользовательского интерфейса даже на медленных устройствах.

С помощью перехода пользовательский интерфейс остается отзывчивым в середине повторного рендеринга. Например, если пользователь нажал на вкладку, но затем передумал и нажал на другую вкладку, он может сделать это, не дожидаясь окончания первого повторного рендеринга.

### Разница между useTransition и обычным обновлением состояния {#examples}

**1. Обновление текущей вкладки в переходе**

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/tkyfgs?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Обновление текущей вкладки без перехода**

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/pjdrgh?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обновление родительского компонента в переходе {#updating-the-parent-component-in-a-transition}

Вы можете обновить состояние родительского компонента и из вызова `useTransition`. Например, этот компонент `TabButton` обернул свою логику `onClick` в переход:

```js hl_lines="13-15"
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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/ydhhyk?view=Editor+%2B+Preview&module=%2Fsrc%2FTabButton.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Отображение ожидающего визуального состояния во время перехода {#displaying-a-pending-visual-state-during-the-transition}

Вы можете использовать булево значение `isPending`, возвращаемое `useTransition`, чтобы указать пользователю, что переход находится в процессе. Например, кнопка табуляции может иметь специальное визуальное состояние "в ожидании":

```js hl_lines="4-6"
function TabButton({ children, isActive, onClick }) {
    const [isPending, startTransition] = useTransition();
    // ...
    if (isPending) {
        return <b className="pending">{children}</b>;
    }
    // ...
}
```

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gf96wh?view=Editor+%2B+Preview&module=%2Fsrc%2FTabButton.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Предотвращение нежелательных индикаторов загрузки {#preventing-unwanted-loading-indicators}

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/cd5twq?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/hrxdqt?view=Editor+%2B+Preview&module=%2Fsrc%2FTabButton.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Подробнее об [использовании переходов в Suspense](Suspense.md).

!!!note "Ожидание переходов"

    Переходы будут "ждать" только достаточно долго, чтобы избежать скрытия _уже раскрытого_ содержимого (например, контейнера вкладки). Если вкладка Posts имеет [вложенную границу `<Suspense>`](Suspense.md), переход не будет "ждать" ее.

### Создание маршрутизатора с поддержкой `Suspense` {#building-a-suspense-enabled-router}

Если вы создаете фреймворк React или маршрутизатор, мы рекомендуем помечать переходы по страницам как переходы.

```js hl_lines="3 6 8"
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

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/z82ntv?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="silent-grass-z82ntv" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!note ""

    [Suspense-enabled](Suspense.md) ожидается, что маршрутизаторы по умолчанию будут оборачивать обновления навигации в переходы.

### Отображение ошибки для пользователей с границей ошибки {#displaying-an-error-to-users-with-error-boundary}

Если функция, переданная в `startTransition`, выкидывает ошибку, вы можете отобразить ее пользователю с помощью [границы ошибки](Component.md#catching-rendering-errors-with-an-error-boundary). Чтобы использовать границу ошибки, оберните компонент, в котором вызывается `useTransition`, в границу ошибки. После того как функция, переданная в `startTransition`, ошибется, будет отображена обратная связь для границы ошибки.

=== "AddCommentContainer.js"

    ```js
    import { useTransition } from 'react';
    import { ErrorBoundary } from 'react-error-boundary';

    export function AddCommentContainer() {
    	return (
    		<ErrorBoundary
    			fallback={<p>⚠️Something went wrong</p>}
    		>
    			<AddCommentButton />
    		</ErrorBoundary>
    	);
    }

    function addComment(comment) {
    	// For demonstration purposes to show Error Boundary
    	if (comment == null) {
    		throw new Error(
    			'Example Error: An error thrown to trigger error boundary'
    		);
    	}
    }

    function AddCommentButton() {
    	const [pending, startTransition] = useTransition();

    	return (
    		<button
    			disabled={pending}
    			onClick={() => {
    				startTransition(() => {
    					// Intentionally not passing a comment
    					// so error gets thrown
    					addComment();
    				});
    			}}
    		>
    			Add comment
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/mt4t4f?view=Editor+%2B+Preview&module=%2Fsrc%2FAddCommentContainer.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="epic-night-mt4t4f" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Устранение неполадок {#troubleshooting}

### Обновление входа в переходе не работает {#updating-an-input-in-a-transition-doesnt-work}

Вы не можете использовать переход для переменной состояния, которая управляет входом:

```js hl_lines="4 10"
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

Это связано с тем, что переходы являются неблокирующими, но обновление ввода в ответ на событие изменения должно происходить синхронно. Если вы хотите запустить переход в ответ на ввод текста, у вас есть два варианта:

1.  Вы можете объявить две отдельные переменные состояния: одну для состояния ввода (которая всегда обновляется синхронно) и одну, которую вы будете обновлять в переходе. Это позволит вам управлять вводом, используя синхронное состояние, и передать переменную состояния перехода (которая будет "отставать" от ввода) остальной части вашей логики рендеринга.
2.  В качестве альтернативы вы можете иметь одну переменную состояния и добавить [`useDeferredValue`](useDeferredValue.md), которая будет "отставать" от реального значения. Это вызовет неблокирующие повторные рендеринги, чтобы автоматически "догнать" новое значение.

### React не рассматривает обновление моего состояния как переход {#react-doesnt-treat-my-state-update-as-a-transition}

Когда вы оборачиваете обновление состояния в переход, убедитесь, что оно происходит _во время_ вызова `startTransition`:

```js
startTransition(() => {
    // ✅ Setting state *during* startTransition call
    setPage('/about');
});
```

Функция, которую вы передаете в `startTransition`, должна быть синхронной.

Вы не можете пометить обновление как переход таким образом:

```js
startTransition(() => {
    // ❌ Setting state *after* startTransition call
    setTimeout(() => {
        setPage('/about');
    }, 1000);
});
```

Вместо этого вы можете сделать следующее:

```js
setTimeout(() => {
    startTransition(() => {
        // ✅ Setting state *during* startTransition call
        setPage('/about');
    });
}, 1000);
```

Точно так же вы не можете пометить обновление как переход:

```js
startTransition(async () => {
    await someAsyncFunction();
    // ❌ Setting state *after* startTransition call
    setPage('/about');
});
```

Однако это работает вместо этого:

```js
await someAsyncFunction();
startTransition(() => {
    // ✅ Setting state *during* startTransition call
    setPage('/about');
});
```

### React не считает обновление состояния после `await` переходом {#react-doesnt-treat-my-state-update-after-await-as-a-transition}

Если внутри функции `startTransition` есть `await`, обновления состояния после `await` не помечаются как переходы. Каждое обновление состояния после `await` нужно обернуть в вызов `startTransition`:

```js
startTransition(async () => {
  await someAsyncFunction();
  // ❌ Not using startTransition after await
  setPage('/about');
});
```

А вот так это работает:

```js
startTransition(async () => {
  await someAsyncFunction();
  // ✅ Using startTransition *after* await
  startTransition(() => {
    setPage('/about');
  });
});
```

Это ограничение JavaScript: React теряет область асинхронного контекста. В будущем, когда появится [AsyncContext](https://github.com/tc39/proposal-async-context), ограничение уберут.

### Я хочу вызвать `useTransition` извне компонента {#i-want-to-call-usetransition-from-outside-a-component}

Вы не можете вызвать `useTransition` вне компонента, потому что это Hook. В этом случае вместо него используйте отдельный метод [`startTransition`](startTransition.md). Он работает так же, но не предоставляет индикатор `isPending`.

### Функция, которую я передаю в `startTransition`, выполняется немедленно {#the-function-i-pass-to-starttransition-executes-immediately}

Если вы запустите этот код, он выведет 1, 2, 3:

```js hl_lines="1 3 6"
console.log(1);
startTransition(() => {
    console.log(2);
    setPage('/about');
});
console.log(3);
```

**Ожидается, что будет выведено 1, 2, 3.** Функция, которую вы передаете в `startTransition`, не задерживается. В отличие от браузера `setTimeout`, он не запускает обратный вызов позже. React выполняет вашу функцию немедленно, но все обновления состояния, запланированные _пока она выполняется_, помечаются как переходы. Вы можете представить, что это работает следующим образом:

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

### Обновления состояния в переходах идут не по порядку {#my-state-updates-in-transitions-are-out-of-order}

Если сделать `await` внутри `startTransition`, обновления могут прийти не по порядку.

В этом примере `updateQuantity` имитирует запрос к серверу, чтобы обновить количество товара в корзине. Функция *искусственно возвращает каждый второй запрос позже предыдущего*, чтобы смоделировать гонки сетевых запросов.

Попробуйте обновить количество один раз, а затем быстро несколько раз. Можно увидеть неверную сумму:

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "beta",
        "react-dom": "beta"
      },
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test --env=jsdom",
        "eject": "react-scripts eject"
      }
    }
    ```

=== "App.js"

    ```js

    import { useState, useTransition } from "react";
    import { updateQuantity } from "./api";
    import Item from "./Item";
    import Total from "./Total";

    export default function App({}) {
        const [quantity, setQuantity] = useState(1);
        const [isPending, startTransition] = useTransition();
        // Store the actual quantity in separate state to show the mismatch.
        const [clientQuantity, setClientQuantity] = useState(1);

        const updateQuantityAction = newQuantity => {
            setClientQuantity(newQuantity);

            // Access the pending state of the transition,
            // by wrapping in startTransition again.
            startTransition(async () => {
                const savedQuantity = await updateQuantity(newQuantity);
                startTransition(() => {
                    setQuantity(savedQuantity);
                });
            });
        };

        return (
            <div>
                <h1>Checkout</h1>
                <Item action={updateQuantityAction}/>
                <hr />
                <Total clientQuantity={clientQuantity} savedQuantity={quantity} isPending={isPending} />
            </div>
        );
    }

    ```

=== "Item.js"

    ```js

    import {startTransition} from 'react';

    export default function Item({action}) {
        function handleChange(e) {
            // Update the quantity in an Action.
            startTransition(async () => {
                await action(e.target.value);
            });
        }
        return (
            <div className="item">
                <span>Eras Tour Tickets</span>
                <label htmlFor="name">Quantity: </label>
                <input
                    type="number"
                    onChange={handleChange}
                    defaultValue={1}
                    min={1}
                />
            </div>
        )
    }
    ```

=== "Total.js"

    ```js

    const intl = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
    });

    export default function Total({ clientQuantity, savedQuantity, isPending }) {
        return (
            <div className="total">
                <span>Total:</span>
                <div>
                    <div>
                        {isPending
                            ? "🌀 Updating..."
                            : `${intl.format(savedQuantity * 9999)}`}
                    </div>
                    <div className="error">
                        {!isPending &&
                            clientQuantity !== savedQuantity &&
                            `Wrong total, expected: ${intl.format(clientQuantity * 9999)}`}
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    let firstRequest = true;
    export async function updateQuantity(newName) {
        return new Promise((resolve, reject) => {
            if (firstRequest === true) {
                firstRequest = false;
                setTimeout(() => {
                    firstRequest = true;
                    resolve(newName);
                    // Simulate every other request being slower
                }, 1000);
            } else {
                setTimeout(() => {
                    resolve(newName);
                }, 50);
            }
        });
    }
    ```

=== "styles.css"

    ```css

    .item {
      display: flex;
      align-items: center;
      justify-content: start;
    }

    .item label {
      flex: 1;
      text-align: right;
    }

    .item input {
      margin-left: 4px;
      width: 60px;
      padding: 4px;
    }

    .total {
      height: 50px;
      line-height: 25px;
      display: flex;
      align-content: center;
      justify-content: space-between;
    }

    .total div {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }

    .error {
      color: red;
    }
    ```

Если кликать несколько раз, предыдущие запросы могут закончиться после более поздних. Сейчас React не знает, какой порядок был задуман. Обновления планируются асинхронно, и за асинхронной границей React теряет контекст порядка.

Так и задумано: действия внутри перехода не гарантируют порядок выполнения. Для обычных случаев React даёт абстракции уровнем выше, например [`useActionState`](useActionState.md) и [действия `<form>`](../react-dom/components/form.md), которые следят за порядком. В сложных случаях свою очередь и отмену нужно реализовать самим.

Пример того, как `useActionState` сохраняет порядок выполнения:

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "beta",
        "react-dom": "beta"
      },
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test --env=jsdom",
        "eject": "react-scripts eject"
      }
    }
    ```

=== "App.js"

    ```js

    import { useState, useActionState } from "react";
    import { updateQuantity } from "./api";
    import Item from "./Item";
    import Total from "./Total";

    export default function App({}) {
        // Store the actual quantity in separate state to show the mismatch.
        const [clientQuantity, setClientQuantity] = useState(1);
        const [quantity, updateQuantityAction, isPending] = useActionState(
            async (prevState, payload) => {
                setClientQuantity(payload);
                const savedQuantity = await updateQuantity(payload);
                return savedQuantity; // Return the new quantity to update the state
            },
            1 // Initial quantity
        );

        return (
            <div>
                <h1>Checkout</h1>
                <Item action={updateQuantityAction}/>
                <hr />
                <Total clientQuantity={clientQuantity} savedQuantity={quantity} isPending={isPending} />
            </div>
        );
    }

    ```

=== "Item.js"

    ```js

    import {startTransition} from 'react';

    export default function Item({action}) {
        function handleChange(e) {
            // Update the quantity in an Action.
            startTransition(() => {
                action(e.target.value);
            });
        }
        return (
            <div className="item">
                <span>Eras Tour Tickets</span>
                <label htmlFor="name">Quantity: </label>
                <input
                    type="number"
                    onChange={handleChange}
                    defaultValue={1}
                    min={1}
                />
            </div>
        )
    }
    ```

=== "Total.js"

    ```js

    const intl = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
    });

    export default function Total({ clientQuantity, savedQuantity, isPending }) {
        return (
            <div className="total">
                <span>Total:</span>
                <div>
                    <div>
                        {isPending
                            ? "🌀 Updating..."
                            : `${intl.format(savedQuantity * 9999)}`}
                    </div>
                    <div className="error">
                        {!isPending &&
                            clientQuantity !== savedQuantity &&
                            `Wrong total, expected: ${intl.format(clientQuantity * 9999)}`}
                    </div>
                </div>
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    let firstRequest = true;
    export async function updateQuantity(newName) {
        return new Promise((resolve, reject) => {
            if (firstRequest === true) {
                firstRequest = false;
                setTimeout(() => {
                    firstRequest = true;
                    resolve(newName);
                    // Simulate every other request being slower
                }, 1000);
            } else {
                setTimeout(() => {
                    resolve(newName);
                }, 50);
            }
        });
    }
    ```

=== "styles.css"

    ```css

    .item {
      display: flex;
      align-items: center;
      justify-content: start;
    }

    .item label {
      flex: 1;
      text-align: right;
    }

    .item input {
      margin-left: 4px;
      width: 60px;
      padding: 4px;
    }

    .total {
      height: 50px;
      line-height: 25px;
      display: flex;
      align-content: center;
      justify-content: space-between;
    }

    .total div {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }

    .error {
      color: red;
    }
    ```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useTransition](https://react.dev/reference/react/useTransition)</small>
