---
status: experimental
description: preload позволяет вам заранее получить ресурс, такой как таблица стилей, шрифт или внешний скрипт, который вы ожидаете использовать
---

# preload

!!!example "Canary"

    Функция `preload` в настоящее время доступна только в каналах React Canary и experimental. Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

!!!note ""

    [Фреймворки на основе React](../../learn/start-a-new-react-project.md) часто обрабатывают загрузку ресурсов за вас, поэтому вы можете не вызывать этот API самостоятельно. За подробностями обращайтесь к документации вашего фреймворка.

<big>**`preload`** позволяет вам заранее получить ресурс, такой как таблица стилей, шрифт или внешний скрипт, который вы ожидаете использовать.</big>

```js
preload('https://example.com/font.woff2', { as: 'font' });
```

## Описание {#reference}

### `preload(href, options)` {#preload}

Чтобы предварительно загрузить ресурс, вызовите функцию `preload` из `react-dom`.

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('https://example.com/font.woff2', {
        as: 'font',
    });
    // ...
}
```

Функция `preload` дает браузеру подсказку о том, что ему следует начать загрузку данного ресурса, что позволяет сэкономить время.

**Параметры**

-   `href`: строка. URL-адрес ресурса, который вы хотите загрузить.
-   `options`: объект. Он содержит следующие свойства:
    -   `as`: обязательная строка. Тип ресурса. Его [возможные значения](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#as): `audio`, `document`, `embed`, `fetch`, `font`, `image`, `object`, `script`, `style`, `track`, `video`, `worker`.
    -   `crossOrigin`: строка. Политика [CORS](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin), которую следует использовать. Возможные значения: `anonymous` и `use-credentials`. Требуется, если для `as` установлено значение `"fetch"`.
    -   `referrerPolicy`: строка. Заголовок [Referrer header](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#referrerpolicy), который следует отправлять при выборке. Возможные значения: `no-referrer-when-downgrade` (по умолчанию), `no-referrer`, `origin`, `origin-when-cross-origin`, и `unsafe-url`.
    -   `integrity`: строка. Криптографический хэш ресурса для [проверки его подлинности](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
    -   `type`: строка. MIME-тип ресурса.
    -   `nonce`: строка. Криптографический [nonce для разрешения ресурса](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) при использовании строгой политики безопасности содержимого.
    -   `fetchPriority`: строка. Предлагает относительный приоритет для получения ресурса. Возможные значения: `auto` (по умолчанию), `high` и `low`.
    -   `imageSrcSet`: строка. Используется только с `as: "image"`. Указывает [исходный набор изображения](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).
    -   `imageSizes`: строка. Используется только с `as: "image"`. Указывает [размеры изображения](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

**Возвращаемое значение**

`preload` ничего не возвращает.

**Ограничения**

-   Несколько эквивалентных вызовов `preload` имеют тот же эффект, что и один вызов. Вызовы `preload` считаются эквивалентными в соответствии со следующими правилами:
    -   Два вызова эквивалентны, если у них одинаковый `href`, за исключением:
    -   Если `as` имеет значение `image`, то два вызова эквивалентны, если у них одинаковые `href`, `imageSrcSet` и `imageSizes`.
-   В браузере вы можете вызвать `preload` в любой ситуации: при рендеринге компонента, в эффекте, в обработчике событий и так далее.
-   При рендеринге на стороне сервера или при рендеринге серверных компонентов `preload` имеет эффект только в том случае, если вы вызываете его во время рендеринга компонента или в асинхронном контексте, возникающем при рендеринге компонента. Любые другие вызовы будут проигнорированы.

## Использование {#usage}

### Предварительная загрузка при рендеринге {#preloading-when-rendering}

Вызовите `preload` при рендеринге компонента, если вы знаете, что он или его дочерние компоненты будут использовать определенный ресурс.

### Примеры предварительной загрузки

**1. Предварительная загрузка внешнего скрипта**

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('https://example.com/script.js', {
        as: 'script',
    });
    return /* ... */;
}
```

Если вы хотите, чтобы браузер начал выполнять скрипт немедленно (а не просто загрузил его), используйте [`preinit`](./preinit.md). Если вы хотите загрузить модуль ESM, используйте [`preloadModule`](./preloadModule.md).

**2. Предварительная загрузка таблицы стилей**

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('https://example.com/style.css', {
        as: 'style',
    });
    return /* ... */;
}
```

Если вы хотите, чтобы таблица стилей была вставлена в документ немедленно (это означает, что браузер начнет разбирать ее сразу, а не просто загрузит), используйте [`preinit`](./preinit.md) вместо этого.

**3. Предварительная загрузка шрифта**

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('https://example.com/style.css', {
        as: 'style',
    });
    preload('https://example.com/font.woff2', {
        as: 'font',
    });
    return /* ... */;
}
```

Если вы предварительно загружаете таблицу стилей, разумно также предварительно загрузить все шрифты, на которые ссылается таблица стилей. Таким образом, браузер сможет начать загрузку шрифта до того, как загрузит и разберет таблицу стилей.

**4. Предварительная загрузка изображения**

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('/banner.png', {
        as: 'image',
        imageSrcSet:
            '/banner512.png 512w, /banner1024.png 1024w',
        imageSizes: '(max-width: 512px) 512px, 1024px',
    });
    return /* ... */;
}
```

При предварительной загрузке изображения параметры `imageSrcSet` и `imageSizes` помогают браузеру [получить изображение правильного размера в соответствии с размерами экрана](https://developer.mozilla.org/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

### Предварительная загрузка в обработчике события {#preloading-in-an-event-handler}

Вызовите `preload` в обработчике события перед переходом на страницу или в состояние, где потребуются внешние ресурсы. Это позволит запустить процесс раньше, чем если бы вы вызвали его во время рендеринга новой страницы или состояния.

```js
import { preload } from 'react-dom';

function CallToAction() {
    const onClick = () => {
        preload('https://example.com/wizardStyles.css', {
            as: 'style',
        });
        startWizard();
    };
    return <button onClick={onClick}>Start Wizard</button>;
}
```

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/preload></small>
