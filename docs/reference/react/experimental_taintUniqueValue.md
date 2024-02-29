---
status: experimental
title: taintUniqueValue
---

# experimental_taintUniqueValue

!!!warning "В разработке"

    **Этот API является экспериментальным и пока не доступен в стабильной версии React.**

    Вы можете попробовать его, обновив пакеты React до последней экспериментальной версии:

    -   `react@experimental`
    -   `react-dom@experimental`
    -   `eslint-plugin-react-hooks@experimental`.

    Экспериментальные версии React могут содержать ошибки. Не используйте их в продакшене.

    Этот API доступен только внутри [React Server Components](./use-client.md).

<big>`taintUniqueValue` позволяет предотвратить передачу уникальных значений клиентским компонентам, таких как пароли, ключи или токены.</big>

```js
taintUniqueValue(errMessage, lifetime, value);
```

Чтобы предотвратить передачу объекта, содержащего конфиденциальные данные, смотрите [`taintObjectReference`](./experimental_taintObjectReference.md).

## Описание {#reference}

### `taintUniqueValue(message, lifetime, value)` {#taintuniquevalue}

Вызовите `taintUniqueValue` с паролем, токеном, ключом или хэшем, чтобы зарегистрировать его в React как нечто, что не должно быть передано клиенту как есть:

```js
import { experimental_taintUniqueValue } from 'react';

experimental_taintUniqueValue(
    'Do not pass secret keys to the client.',
    process,
    process.env.SECRET_KEY
);
```

**Параметры**

-   `message`: Сообщение, которое вы хотите отобразить, если `value` будет передано клиентскому компоненту. Это сообщение будет отображаться как часть ошибки, которая будет выброшена, если `value` будет передано клиентскому компоненту.

-   `lifetime`: Любой объект, указывающий, как долго `value` должно быть запятнано. Пока этот объект существует, `value` будет заблокирован от передачи любому клиентскому компоненту. Например, передача `globalThis` блокирует значение на время жизни приложения. `lifetime` обычно представляет собой объект, свойства которого содержат `value`.

-   `value`: Строка, bigint или TypedArray. `value` должно быть уникальной последовательностью символов или байтов с высокой энтропией, например, криптографическим токеном, закрытым ключом, хэшем или длинным паролем. Значение `value` будет заблокировано от отправки любому клиентскому компоненту.

**Возвращает**

`experimental_taintUniqueValue` возвращает `undefined`.

**Замечания**

-   Получение новых значений из запятнанных значений может нарушить защиту от запятнанности. Новые значения, созданные путем перевода запятнанных значений в верхний регистр, конкатенации запятнанных строковых значений в большую строку, преобразования запятнанных значений в base64, подстроки запятнанных значений и других подобных преобразований, не будут запятнаны, если вы явно не вызовете `taintUniqueValue` для этих вновь созданных значений.
-   Не используйте `taintUniqueValue` для защиты значений с низкой энтропией, таких как PIN-коды или номера телефонов. Если любое значение в запросе контролируется злоумышленником, он может определить, какое значение испорчено, перечислив все возможные значения секрета.

## Использование {#usage}

### Предотвращение передачи токена клиентским компонентам {#prevent-a-token-from-being-passed-to-client-components}

Чтобы гарантировать, что конфиденциальная информация, такая как пароли, токены сессий или другие уникальные значения, не будут случайно переданы клиентским компонентам, функция `taintUniqueValue` обеспечивает уровень защиты. Если значение запятнано, любая попытка передать его клиентскому компоненту приведет к ошибке.

Аргумент `lifetime` определяет срок, в течение которого значение остается запятнанным. Для значений, которые должны оставаться запятнанными неограниченно долго, в качестве аргумента `lifetime` могут выступать объекты типа [`globalThis`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis) или `process`. Эти объекты имеют срок жизни, который охватывает все время выполнения вашего приложения.

```js
import { experimental_taintUniqueValue } from 'react';

experimental_taintUniqueValue(
    'Do not pass a user password to the client.',
    globalThis,
    process.env.SECRET_KEY
);
```

Если время жизни запятнанного значения привязано к объекту, то `lifetime` должен быть объектом, который инкапсулирует значение. Это гарантирует, что запятнанное значение останется защищенным в течение всего срока жизни инкапсулирующего объекта.

```js
import { experimental_taintUniqueValue } from 'react';

export async function getUser(id) {
    const user = await db`SELECT * FROM users WHERE id = ${id}`;
    experimental_taintUniqueValue(
        'Do not pass a user session token to the client.',
        user,
        user.session.token
    );
    return user;
}
```

В этом примере в качестве аргумента `lifetime` выступает объект `user`. Если этот объект попадет в глобальный кэш или будет доступен по другому запросу, маркер сессии останется испорченным.

<Pitfall>

!!!warning "Не полагайтесь только на запятнанность для обеспечения безопасности"

    Запятнанность значения не блокирует все возможные производные значения. Например, создание нового значения путем выделения верхним регистром запятнанной строки не приведет к запятнанию нового значения.

    ```js
    import { experimental_taintUniqueValue } from 'react';

    const password = 'correct horse battery staple';

    experimental_taintUniqueValue(
    	'Do not pass the password to the client.',
    	globalThis,
    	password
    );

    // `uppercasePassword` is not tainted
    const uppercasePassword = password.toUpperCase();
    ```

    В этом примере запятнана константа `password`. Затем `password` используется для создания нового значения `uppercasePassword` путем вызова метода `toUpperCase` для `password`. Вновь созданное значение `uppercasePassword` не запятнано.

    Другие подобные способы получения новых значений из запятнанных значений, такие как конкатенация в большую строку, преобразование в base64 или возврат подстроки, создают незапятнанные значения.

    Tainting защищает только от простых ошибок, таких как явная передача секретных значений клиенту. Ошибки при вызове `taintUniqueValue`, например, использование глобального хранилища вне React, без соответствующего объекта `lifetime`, могут привести к тому, что запятнанное значение станет незапятнанным. Запятнанное значение - это уровень защиты; безопасное приложение будет иметь несколько уровней защиты, хорошо разработанные API и шаблоны изоляции.

#### Использование `server-only` и `taintUniqueValue` для предотвращения утечки секретов {#using-server-only-and-taintuniquevalue-to-prevent-leaking-secrets}

Если вы используете среду серверных компонентов, которая имеет доступ к закрытым ключам или паролям, таким как пароли баз данных, вы должны быть осторожны, чтобы не передать их клиентскому компоненту.

```js
export async function Dashboard(props) {
    // DO NOT DO THIS
    return <Overview password={process.env.API_PASSWORD} />;
}
```

---

```js
"use client";

import {useEffect} from '...'

export async function Overview({ password }) {
  useEffect(() => {
    const headers = { Authorization: password };
    fetch(url, { headers }).then(...);
  }, [password]);
  ...
}
```

В этом примере секретный API-токен будет передан клиенту. Если этот API-токен может быть использован для доступа к данным, к которым этот конкретный пользователь не должен иметь доступа, это может привести к утечке данных.

В идеале подобные секреты абстрагируются в один файл-помощник, который может быть импортирован только доверенными утилитами данных на сервере. Этот помощник можно даже пометить [`server-only`](https://www.npmjs.com/package/server-only), чтобы гарантировать, что этот файл не будет импортирован на клиенте.

```js
import 'server-only';

export function fetchAPI(url) {
    const headers = {
        Authorization: process.env.API_PASSWORD,
    };
    return fetch(url, { headers });
}
```

Иногда во время рефакторинга случаются ошибки, и не все ваши коллеги могут знать об этом. Чтобы защитить себя от таких ошибок, мы можем "испортить" настоящий пароль:

```js
import "server-only";
import {experimental_taintUniqueValue} from 'react';

experimental_taintUniqueValue(
  'Do not pass the API token password to the client. ' +
    'Instead do all fetches on the server.'
  process,
  process.env.API_PASSWORD
);
```

Теперь при попытке передать этот пароль клиентскому компоненту или отправить пароль клиентскому компоненту с помощью серверного действия будет возникать ошибка с сообщением, которое вы определили при вызове `taintUniqueValue`.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/experimental_taintUniqueValue](https://react.dev/reference/react/experimental_taintUniqueValue)</small>
