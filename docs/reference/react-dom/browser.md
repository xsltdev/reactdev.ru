---
description: browser позволяет пометить компонент как доступный только в браузере во время серверного рендеринга
---

# browser

<big>`browser` позволяет пометить компонент как доступный только в браузере во время серверного рендеринга.</big>

```js
use(browser(reason?))
```

## Описание {#reference}

### `browser(reason?)` {#browser}

Вызовите `browser` внутри [`use`](../react/use.md), чтобы пометить компонент как доступный только в браузере во время серверного рендеринга:

```js
import { use } from 'react';
import { browser } from 'react-dom';

function BrowserOnly() {
  use(browser('This component requires browser APIs.'));
  return <BrowserContent />;
}
```

Во время серверного рендеринга `use(browser())` останавливает рендеринг компонента и оставляет на его месте фолбэк ближайшей границы [`<Suspense>`](../react/Suspense.md). В браузере `use(browser())` возвращает `undefined`, поэтому компонент рендерится как обычно.

[Больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   **опционально** `reason`: Строка или функция, которая объясняет, почему содержимое нужно рендерить в браузере. Строка или возвращаемое значение функции становится `cause` объекта `Error`, передаваемого в [`onBrowserBailout`](#reporting-browser-only-rendering-on-the-server). React вызывает функцию причины каждый раз, когда серверный рендерер встречает значение, возвращённое `browser`, но не вызывает её в браузере. Если создание причины дорого, передайте функцию, например `() => new Error(...)`.

#### Возвращаемое значение {#returns}

`browser` возвращает непрозрачное значение, которое можно передать в `use` в компоненте или использовать как причину при [прерывании серверного рендеринга](#aborting-pending-server-rendering-for-the-browser). В браузере передача этого значения в `use` возвращает `undefined`.

#### Предупреждения {#caveats}

-   `use(browser())` во время серверного рендеринга должен находиться внутри границы `<Suspense>`. Без неё серверный рендеринг завершается ошибкой.
-   `use(browser())` нужно вызывать из [клиентского компонента](../rsc/use-client.md), а не из [серверного компонента](../rsc/server-components.md).
-   Сам по себе вызов `browser()` ничего не делает. Чтобы пометить компонент как доступный только в браузере, передайте значение, возвращённое `browser`, в `use`. Не выбрасывайте его.

## Использование {#usage}

### Рендеринг содержимого только в браузере {#rendering-content-only-in-the-browser}

Вызовите `browser` внутри `use` в компоненте, который должен рендериться только в браузере.

Это можно использовать вместо проверки `typeof window`, ожидания, пока [`Эффект`](../react/useEffect.md) установит состояние «смонтирован», или опции фреймворка, которая отключает серверный рендеринг.

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

!!!note "Примечание"

    `use(browser())` нужно вызывать из клиентского компонента. Если ваш фреймворк по умолчанию использует серверные компоненты, добавьте директиву [`'use client'`](../rsc/use-client.md) в этот файл или перенесите вызов в дочерний клиентский компонент:

    ```js hl_lines="1"
    'use client';

    import { use, useState } from 'react';
    import { browser } from 'react-dom';

    export default function SavedDraft() {
      use(browser('The saved draft is stored in localStorage.'));
      const [draft] = useState(() => localStorage.getItem('draft') ?? '');
      return <DraftEditor initialDraft={draft} />;
    }
    ```

### Условный рендеринг на сервере {#conditionally-rendering-on-the-server}

Как и другие вызовы [`use`](../react/use.md), `use(browser())` можно вызывать внутри условия или после раннего возврата. Это позволяет компоненту или пользовательскому хуку отказаться от серверного рендеринга в зависимости от условия, например от значения пропса.

Например, хук `useTimeZone` принимает необязательное значение по умолчанию. Если оно передано, React рендерит значение по умолчанию в исходном HTML и в браузере. Без значения по умолчанию компонент приостанавливается во время серверного рендеринга и показывает локальный часовой пояс устройства в браузере.

Нажмите **Reload**, чтобы увидеть фолбэк загрузки до появления часового пояса пользователя.

=== "App.js"

    ```js
    import { Suspense } from 'react';
    import { useTimeZone } from './useTimeZone.js';

    function TimeZone({label, defaultTimeZone}) {
        const timeZone = useTimeZone(defaultTimeZone);
        return <p>{label}: <strong>{timeZone}</strong></p>;
    }

    export default function App() {
        return (
            <>
                <h1>Event details</h1>
                <TimeZone
                    label="Event time zone"
                    defaultTimeZone="America/New_York"
                />
                <Suspense fallback={<p>Loading your time zone...</p>}>
                    <TimeZone label="Your time zone" />
                </Suspense>
            </>
        );
    }
    ```

=== "useTimeZone.js"

    ```js
    import { use } from 'react';
    import { browser } from 'react-dom';

    export function useTimeZone(defaultTimeZone) {
        if (defaultTimeZone !== undefined) {
            return defaultTimeZone;
        }

        use(browser('No default time zone was provided.'));
        return Intl.DateTimeFormat().resolvedOptions().timeZone;
    }
    ```

=== "Document.js"

    ```js
    import App from './App.js';

    export default function Document() {
        return (
            <html lang="en">
                <head>
                    <title>Event details</title>
                    <style>{`
                        h1 { font-size: 24px; margin-top: 0; }
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
      height: 240px;
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

Похожий приём можно применить, чтобы условно избежать серверного рендеринга при использовании библиотеки получения данных с поддержкой Suspense:

```js hl_lines="3"
function useBrowserQuery(query, options) {
  if (options.initialData === undefined) {
    use(browser('useBrowserQuery: No initial data was provided.'));
  }

  return useQuery(query, options);
}

function ProductDetails({ productId, initialData }) {
  const product = useBrowserQuery(`/api/products/${productId}`, {
    initialData,
  });

  return <h1>{product.name}</h1>;
}
```

С `initialData` React рендерит компонент в HTML на сервере. Без него React оставляет в HTML фолбэк ближайшей границы [`<Suspense>`](../react/Suspense.md). В браузере `useQuery` может получить данные или прочитать их из клиентского кэша, как обычно.

### Отчёты о рендеринге только в браузере на сервере {#reporting-browser-only-rendering-on-the-server}

Передайте обратный вызов `onBrowserBailout` серверному рендереру, чтобы сообщать о рендеринге только в браузере. Когда React оставляет фолбэк Suspense для браузера, он не вызывает обратный вызов `onError` серверного рендерера и обратный вызов [`onRecoverableError` у `hydrateRoot`](client/hydrateRoot.md#error-logging-in-production). В этом примере также передаётся причина, доступная как `cause` сообщаемой ошибки:

```js
import { Suspense, use, useState } from 'react';
import { browser } from 'react-dom';
import { renderToPipeableStream } from 'react-dom/server';

function SavedDraft() {
  use(browser(() => new Error('The saved draft is stored in localStorage.')));
  const [draft] = useState(() => localStorage.getItem('draft') ?? '');
  return <DraftEditor initialDraft={draft} />;
}

function App() {
  return (
    <Suspense fallback={<p>Loading saved draft...</p>}>
      <SavedDraft />
    </Suspense>
  );
}

const { pipe } = renderToPipeableStream(<App />, {
  onShellReady() {
    pipe(response);
  },
  onBrowserBailout(error, errorInfo) {
    logBrowserBailout(error, errorInfo);
  }
});
```

`onBrowserBailout` получает два аргумента:

1. `Error`, описывающий рендеринг только в браузере. Если вы передали причину в `browser`, она доступна как `cause` ошибки.
2. Объект `errorInfo` со `componentStack`, который показывает, где произошёл рендеринг только в браузере.

Функция причины может вернуть любое значение. Верните новый `Error`, чтобы у причины был собственный стек и при этом `Error` не создавался в браузере. React не сериализует причину в HTML.

Если нет границы Suspense, которая могла бы дать фолбэк, серверный рендеринг завершается ошибкой. React сообщает о сбое через обычные обратные вызовы ошибок рендерера, а не через `onBrowserBailout`.

### Прерывание незавершённого серверного рендеринга в пользу браузера {#aborting-pending-server-rendering-for-the-browser}

Если вы вызываете API серверного рендеринга напрямую, можно перестать ждать незавершённое содержимое и позволить браузеру дорендерить его. Передайте значение, возвращённое `browser`, как причину при прерывании серверного рендеринга. Тогда React оставляет ожидающие границы Suspense в состоянии фолбэка и рендерит их содержимое в браузере:

```js hl_lines="1 8"
import { browser } from 'react-dom';
import { renderToPipeableStream } from 'react-dom/server';

const { pipe, abort } = renderToPipeableStream(<App />, {
  onShellReady() {
    pipe(response);
    setTimeout(() => {
      abort(browser('The server render timed out.'));
    }, 10000);
  }
});
```

Причина прерывания `browser` не вызывает обратный вызов `onError` серверного рендерера и обратный вызов `onRecoverableError` у `hydrateRoot`. Вместо этого серверный рендерер сообщает о каждой восстановленной границе Suspense в `onBrowserBailout`.

Для API серверного рендеринга, которые принимают [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), передайте `browser()` как причину в [`AbortController.abort`](https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/browser](https://react.dev/reference/react-dom/browser)</small>
