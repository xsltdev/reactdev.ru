---
description: captureOwnerStack читает текущий стек владельца в режиме разработки и возвращает его строкой, если он доступен
---

# captureOwnerStack

<big>**`captureOwnerStack`** читает текущий стек владельца в режиме разработки и возвращает его строкой, если он доступен.</big>

```js
const stack = captureOwnerStack();
```

## Описание {#reference}

### `captureOwnerStack()` {#captureownerstack}

Вызовите `captureOwnerStack`, чтобы получить текущий стек владельца.

```js hl_lines="5 5"
import * as React from 'react';

function Component() {
  if (process.env.NODE_ENV !== 'production') {
    const ownerStack = React.captureOwnerStack();
    console.log(ownerStack);
  }
}
```

#### Параметры {#parameters}

`captureOwnerStack` не принимает никаких параметров.

#### Возвращаемое значение {#returns}

`captureOwnerStack` возвращает `string | null`.

Стеки владельца доступны в

-   рендере компонента
-   эффектах (например, `useEffect`)
-   обработчиках событий React (например, `<button onClick={...} />`)
-   обработчиках ошибок React ([параметры корня React](../react-dom/client/createRoot.md#parameters) `onCaughtError`, `onRecoverableError` и `onUncaughtError`)

Если стек владельца недоступен, возвращается `null` (см. [Устранение неполадок: стек владельца равен `null`](#the-owner-stack-is-null)).

#### Предупреждения {#caveats}

-   Стеки владельца доступны только в режиме разработки. Вне режима разработки `captureOwnerStack` всегда возвращает `null`.

??? note "Стек владельца и стек компонента"

    Стек владельца отличается от стека компонента, доступного в обработчиках ошибок React, например [`errorInfo.componentStack` в `onUncaughtError`](../react-dom/client/hydrateRoot.md#error-logging-in-production).

    Например, рассмотрим следующий код:

    === "App.js"

        ```js

        import {Suspense} from 'react';

        function SubComponent({disabled}) {
            if (disabled) {
                throw new Error('disabled');
            }
        }

        export function Component({label}) {
            return (
                <fieldset>
                    <legend>{label}</legend>
                    <SubComponent key={label} disabled={label === 'disabled'} />
                </fieldset>
            );
        }

        function Navigation() {
            return null;
        }

        export default function App({children}) {
            return (
                <Suspense fallback="loading...">
                    <main>
                        <Navigation />
                        {children}
                    </main>
                </Suspense>
            );
        }
        ```

    === "index.js"

        ```js

        import {captureOwnerStack} from 'react';
        import {createRoot} from 'react-dom/client';
        import App, {Component} from './App.js';
        import './styles.css';

        createRoot(document.createElement('div'), {
            onUncaughtError: (error, errorInfo) => {
                // The stacks are logged instead of showing them in the UI directly to
                // highlight that browsers will apply sourcemaps to the logged stacks.
                // Note that sourcemapping is only applied in the real browser console not
                // in the fake one displayed on this page.
                // Press "fork" to be able to view the sourcemapped stack in a real console.
                console.log(errorInfo.componentStack);
                console.log(captureOwnerStack());
            },
        }).render(
            <App>
                <Component label="disabled" />
            </App>
        );
        ```

    `SubComponent` выбросит ошибку.
    Стек компонента этой ошибки будет

    ```
    at SubComponent
    at fieldset
    at Component
    at main
    at React.Suspense
    at App
    ```

    Однако стек владельца прочитает только

    ```
    at Component
    ```

    Ни `App`, ни DOM-компоненты (например, `fieldset`) не считаются владельцами в этом стеке, поскольку они не участвовали в «создании» узла, содержащего `SubComponent`. `App` и DOM-компоненты только пробросили узел дальше. `App` просто отрендерил узел `children`, в отличие от `Component`, который создал узел, содержащий `SubComponent`, через `<SubComponent />`.

    Ни `Navigation`, ни `legend` вообще нет в стеке, поскольку они лишь соседи узла, содержащего `<SubComponent />`.

    `SubComponent` опущен, потому что он уже является частью стека вызовов.

## Использование {#usage}

### Улучшение собственного оверлея ошибок {#enhance-a-custom-error-overlay}

```js hl_lines="5 7"
import { captureOwnerStack } from "react";
import { instrumentedConsoleError } from "./errorOverlay";

const originalConsoleError = console.error;
console.error = function patchedConsoleError(...args) {
  originalConsoleError.apply(console, args);
  const ownerStack = captureOwnerStack();
  onConsoleError({
    // Keep in mind that in a real application, console.error can be
    // called with multiple arguments which you should account for.
    consoleMessage: args[0],
    ownerStack,
  });
};
```

Если вы перехватываете вызовы `console.error`, чтобы подсвечивать их в оверлее ошибок, вы можете вызвать `captureOwnerStack`, чтобы включить стек владельца.

=== "styles.css"

    ```css

    * {
      box-sizing: border-box;
    }

    body {
      font-family: sans-serif;
      margin: 20px;
      padding: 0;
    }

    h1 {
      margin-top: 0;
      font-size: 22px;
    }

    h2 {
      margin-top: 0;
      font-size: 20px;
    }

    code {
      font-size: 1.2em;
    }

    ul {
      padding-inline-start: 20px;
    }

    label, button { display: block; margin-bottom: 20px; }
    html, body { min-height: 300px; }

    #error-dialog {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background-color: white;
      padding: 15px;
      opacity: 0.9;
      text-wrap: wrap;
      overflow: scroll;
    }

    .text-red {
      color: red;
    }

    .-mb-20 {
      margin-bottom: -20px;
    }

    .mb-0 {
      margin-bottom: 0;
    }

    .mb-10 {
      margin-bottom: 10px;
    }

    pre {
      text-wrap: wrap;
    }

    pre.nowrap {
      text-wrap: nowrap;
    }

    .hidden {
     display: none;
    }
    ```

=== "errorOverlay.js"

    ```js

    export function onConsoleError({ consoleMessage, ownerStack }) {
        const errorDialog = document.getElementById("error-dialog");
        const errorBody = document.getElementById("error-body");
        const errorOwnerStack = document.getElementById("error-owner-stack");

        // Display console.error() message
        errorBody.innerText = consoleMessage;

        // Display owner stack
        errorOwnerStack.innerText = ownerStack;

        // Show the dialog
        errorDialog.classList.remove("hidden");
    }
    ```

=== "index.js"

    ```js

    import { captureOwnerStack } from "react";
    import { createRoot } from "react-dom/client";
    import App from './App';
    import { onConsoleError } from "./errorOverlay";
    import './styles.css';

    const originalConsoleError = console.error;
    console.error = function patchedConsoleError(...args) {
        originalConsoleError.apply(console, args);
        const ownerStack = captureOwnerStack();
        onConsoleError({
            // Keep in mind that in a real application, console.error can be
            // called with multiple arguments which you should account for.
            consoleMessage: args[0],
            ownerStack,
        });
    };

    const container = document.getElementById("root");
    createRoot(container).render(<App />);
    ```

=== "App.js"

    ```js

    function Component() {
        return <button onClick={() => console.error('Some console error')}>Trigger console.error()</button>;
    }

    export default function App() {
        return <Component />;
    }
    ```

## Устранение неполадок {#troubleshooting}

### Стек владельца равен `null` {#the-owner-stack-is-null}

Вызов `captureOwnerStack` произошёл вне функции, контролируемой React, например в колбэке `setTimeout`, после вызова `fetch` или в собственном обработчике DOM-события. Во время рендеринга, в эффектах, обработчиках событий React и обработчиках ошибок React (например, `hydrateRoot#options.onCaughtError`) стеки владельца должны быть доступны.

В примере ниже нажатие на кнопку запишет в лог пустой стек владельца, потому что `captureOwnerStack` был вызван в собственном обработчике DOM-события. Стек владельца нужно захватить раньше, например перенеся вызов `captureOwnerStack` в тело эффекта.

```js
import {captureOwnerStack, useEffect} from 'react';

export default function App() {
    useEffect(() => {
        // Should call `captureOwnerStack` here.
        function handleEvent() {
            // Calling it in a custom DOM event handler is too late.
            // The Owner Stack will be `null` at this point.
            console.log('Owner Stack: ', captureOwnerStack());
        }

        document.addEventListener('click', handleEvent);

        return () => {
            document.removeEventListener('click', handleEvent);
        }
    })

    return <button>Click me to see that Owner Stacks are not available in custom DOM event handlers</button>;
}
```

### `captureOwnerStack` недоступен {#captureownerstack-is-not-available}

`captureOwnerStack` экспортируется только в сборках для разработки. В продакшен-сборках он будет `undefined`. Если `captureOwnerStack` используется в файлах, которые собираются и для продакшена, и для разработки, обращайтесь к нему условно из импорта пространства имён.

```js
// Don't use named imports of `captureOwnerStack` in files that are bundled for development and production.
import {captureOwnerStack} from 'react';
// Use a namespace import instead and access `captureOwnerStack` conditionally.
import * as React from 'react';

if (process.env.NODE_ENV !== 'production') {
  const ownerStack = React.captureOwnerStack();
  console.log('Owner Stack', ownerStack);
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/captureOwnerStack](https://react.dev/reference/react/captureOwnerStack)</small>
