---
status: experimental
---

# preinitModule

!!!example "Canary"

    Функция `preinitModule` в настоящее время доступна только в каналах React Canary и experimental. Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

!!!note ""

    [Фреймворки на основе React](../../learn/start-a-new-react-project.md) часто обрабатывают загрузку ресурсов за вас, поэтому вы можете не вызывать этот API самостоятельно. За подробностями обращайтесь к документации вашего фреймворка.

<big>`preinitModule` позволяет вам нетерпеливо получить и оценить модуль ESM.</big>

```js
preinitModule('https://example.com/module.js', {
    as: 'script',
});
```

## Описание {#reference}

### `preinitModule(href, options)` {#preinitmodule}

Чтобы предварительно инициировать модуль ESM, вызовите функцию `preinitModule` из `react-dom`.

```js
import { preinitModule } from 'react-dom';

function AppRoot() {
    preinitModule('https://example.com/module.js', {
        as: 'script',
    });
    // ...
}
```

Функция `preinitModule` дает браузеру подсказку, что он должен начать загрузку и выполнение данного модуля, что позволяет сэкономить время. Модули, которые вы `preinit`, выполняются после завершения их загрузки.

**Параметры**

-   `href`: строка. URL-адрес модуля, который вы хотите загрузить и использовать.
-   `options`: объект. Он содержит следующие свойства:
    -   `as`: обязательная строка. Она должна быть `'script'`.
    -   `crossOrigin`: строка. Политика [CORS](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin), которую следует использовать. Возможные значения: `anonymous` и `use-credentials`.
    -   `integrity`: строка. Криптографический хэш модуля для [проверки его подлинности](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
    -   `nonce`: строка. Криптографический [nonce для разрешения модуля](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) при использовании строгой политики безопасности содержимого.

**Возвращаемое значение**

`preinitModule` ничего не возвращает.

**Ограничения**

-   Несколько вызовов `preinitModule` с одним и тем же `href` имеют тот же эффект, что и один вызов.
-   В браузере вы можете вызвать `preinitModule` в любой ситуации: при рендеринге компонента, в эффекте, в обработчике события и так далее.
-   При рендеринге на стороне сервера или при рендеринге серверных компонентов `preinitModule` имеет эффект только в том случае, если вы вызываете его во время рендеринга компонента или в асинхронном контексте, возникающем при рендеринге компонента. Любые другие вызовы будут проигнорированы.

## Использование {#usage}

### Предварительная загрузка при рендеринге {#preloading-when-rendering}

Вызовите `preinitModule` при рендеринге компонента, если вы знаете, что он или его дочерние компоненты будут использовать определенный модуль, и вы не против того, чтобы этот модуль был оценен и вступил в силу сразу после загрузки.

```js
import { preinitModule } from 'react-dom';

function AppRoot() {
    preinitModule('https://example.com/module.js', {
        as: 'script',
    });
    return /* ... */;
}
```

Если вы хотите, чтобы браузер загрузил модуль, но не выполнял его сразу, используйте [`preloadModule`](./preloadModule.md). Если вы хотите предварительно запустить скрипт, который не является модулем ESM, используйте [`preinit`](./preinit.md).

### Предварительная загрузка в обработчике события {#preloading-in-an-event-handler}

Вызовите `preinitModule` в обработчике события перед переходом на страницу или в состояние, где потребуется модуль. Это позволит запустить процесс раньше, чем если бы вы вызвали его во время рендеринга новой страницы или состояния.

```js
import { preinitModule } from 'react-dom';

function CallToAction() {
    const onClick = () => {
        preinitModule('https://example.com/module.js', {
            as: 'script',
        });
        startWizard();
    };
    return <button onClick={onClick}>Start Wizard</button>;
}
```

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/react-dom/preinitModule></small>
