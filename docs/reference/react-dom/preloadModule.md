---
status: experimental
---

# preloadModule

!!!example "Canary"

    Функция `preloadModule` в настоящее время доступна только в каналах React Canary и experimental. Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

!!!note ""

    [Фреймворки на основе React](../../learn/start-a-new-react-project.md) часто обрабатывают загрузку ресурсов за вас, поэтому вы можете не вызывать этот API самостоятельно. За подробностями обращайтесь к документации вашего фреймворка.

<big>`preloadModule` позволяет вам с нетерпением получить модуль ESM, который вы ожидаете использовать.</big>

```js
preloadModule('https://example.com/module.js', {
    as: 'script',
});
```

## Описание {#reference}

### `preloadModule(href, options)` {#preloadmodule}

Чтобы предварительно загрузить модуль ESM, вызовите функцию `preloadModule` из `react-dom`.

```js
import { preloadModule } from 'react-dom';

function AppRoot() {
    preloadModule('https://example.com/module.js', {
        as: 'script',
    });
    // ...
}
```

Функция `preloadModule` дает браузеру подсказку, что ему следует начать загрузку данного модуля, что позволяет сэкономить время.

**Параметры**

-   `href`: строка. URL-адрес модуля, который вы хотите загрузить.
-   `options`: объект. Он содержит следующие свойства:
    -   `as`: обязательная строка. Она должна быть `'script'`.
    -   `crossOrigin`: строка. Политика [CORS](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin), которую следует использовать. Возможные значения: `anonymous` и `use-credentials`.
    -   `integrity`: строка. Криптографический хэш модуля для [проверки его подлинности](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
    -   `nonce`: строка. Криптографический [nonce для разрешения модуля](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) при использовании строгой политики безопасности содержимого.

**Возвращаемое значение**

`preloadModule` ничего не возвращает.

**Ограничения**

-   Несколько вызовов `preloadModule` с одним и тем же `href` имеют тот же эффект, что и один вызов.
-   В браузере вы можете вызвать `preloadModule` в любой ситуации: при рендеринге компонента, в эффекте, в обработчике события и так далее.
-   При рендеринге на стороне сервера или при рендеринге серверных компонентов `preloadModule` имеет эффект только в том случае, если вы вызываете его во время рендеринга компонента или в асинхронном контексте, возникающем при рендеринге компонента. Любые другие вызовы будут проигнорированы.

## Использование {#usage}

### Предварительная загрузка при рендеринге {#preloading-when-rendering}

Вызовите `preloadModule` при рендеринге компонента, если вы знаете, что он или его дочерние компоненты будут использовать определенный модуль.

```js
import { preloadModule } from 'react-dom';

function AppRoot() {
  preloadModule("https://example.com/module.js", {as: "script"});
  return ...;
}
```

Если вы хотите, чтобы браузер начал выполнять модуль немедленно (а не просто загрузил его), используйте [`preinitModule`](./preinitModule.md). Если вы хотите загрузить скрипт, который не является модулем ESM, используйте [`preload`](./preload.md).

### Предварительная загрузка в обработчике события {#preloading-in-an-event-handler}

Вызовите `preloadModule` в обработчике события перед переходом на страницу или в состояние, где потребуется модуль. Это позволит запустить процесс раньше, чем если бы вы вызвали его во время рендеринга новой страницы или состояния.

```js
import { preloadModule } from 'react-dom';

function CallToAction() {
    const onClick = () => {
        preloadModule('https://example.com/module.js', {
            as: 'script',
        });
        startWizard();
    };
    return <button onClick={onClick}>Start Wizard</button>;
}
```

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/preloadModule></small>
