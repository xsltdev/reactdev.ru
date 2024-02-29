---
status: experimental
title: taintObjectReference
description: Функция taintObjectReference позволяет предотвратить передачу определенного экземпляра объекта клиентскому компоненту, например, объекта user
---

# experimental_taintObjectReference

!!!warning "В разработке"

    **Этот API является экспериментальным и пока не доступен в стабильной версии React.**

    Вы можете попробовать его, обновив пакеты React до последней экспериментальной версии:

    -   `react@experimental`
    -   `react-dom@experimental`
    -   `eslint-plugin-react-hooks@experimental`.

    Экспериментальные версии React могут содержать ошибки. Не используйте их в продакшене.

    Этот API доступен только в компонентах React Server.

<big>Функция `taintObjectReference` позволяет предотвратить передачу определенного экземпляра объекта клиентскому компоненту, например, объекта `user`.</big>

```js
experimental_taintObjectReference(message, object);
```

Чтобы не передавать ключ, хэш или токен, смотрите [`taintUniqueValue`](./experimental_taintUniqueValue.md).

## Описание {#reference}

### `taintObjectReference(message, object)` {#taintobjectreference}

Вызовите `taintObjectReference` с объектом, чтобы зарегистрировать его в React как нечто, что не должно быть передано клиенту как есть:

```js
import { experimental_taintObjectReference } from 'react';

experimental_taintObjectReference(
    'Do not pass ALL environment variables to the client.',
    process.env
);
```

**Параметры**

-   `message`: Сообщение, которое вы хотите отобразить, если объект будет передан клиентскому компоненту. Это сообщение будет отображено как часть ошибки, которая будет выброшена, если объект будет передан клиентскому компоненту.

-   `object`: Объект, который будет запятнан. Функции и экземпляры классов могут быть переданы в `taintObjectReference` как `object`. Функции и классы уже заблокированы от передачи клиентским компонентам, но стандартное сообщение об ошибке React будет заменено на то, которое вы определили в `message`. Когда конкретный экземпляр типизированного массива передается в `taintObjectReference` как `object`, все остальные экземпляры типизированного массива не будут затронуты.

**Возвращает**

`experimental_taintObjectReference` возвращает `undefined`.

**Замечания**

-   При воссоздании или клонировании запятнанного объекта создается новый незапятнанный объект, который может содержать конфиденциальные данные. Например, если у вас есть запятнанный объект `user`, `const userInfo = {name: user.name, ssn: user.ssn}` или `{...user}` создаст новые объекты, которые не будут запятнаны. `taintObjectReference` защищает только от простых ошибок, когда объект передается клиентскому компоненту без изменений.

!!!warning "Не полагайтесь на то, что безопасность обеспечивается только путем запятнания"

    Запятнание объекта не предотвращает утечку всех возможных производных значений. Например, клон запятнанного объекта создаст новый незапятнанный объект. Использование данных из запятнанного объекта (например, `{secret: taintedObj.secret}`) приведет к созданию нового значения или объекта, который не является запятнанным. Запятнанность - это уровень защиты; безопасное приложение будет иметь несколько уровней защиты, хорошо продуманные API и шаблоны изоляции.

## Использование {#usage}

### Предотвращение непреднамеренного попадания пользовательских данных к клиенту {#prevent-user-data-from-unintentionally-reaching-the-client}

Клиентский компонент никогда не должен принимать объекты, содержащие конфиденциальные данные. В идеале, функции получения данных не должны открывать данные, к которым текущий пользователь не должен иметь доступа. Иногда во время рефакторинга случаются ошибки. Чтобы защититься от таких ошибок в дальнейшем, мы можем "запятнать" объект пользователя в нашем API данных.

```js
import { experimental_taintObjectReference } from 'react';

export async function getUser(id) {
    const user = await db`SELECT * FROM users WHERE id = ${id}`;
    experimental_taintObjectReference(
        'Do not pass the entire user object to the client. ' +
            'Instead, pick off the specific properties you ' +
            'need for this use case.',
        user
    );
    return user;
}
```

Теперь, когда кто-то попытается передать этот объект клиентскому компоненту, вместо него будет выдана ошибка с переданным сообщением об ошибке.

#### Защита от утечек при получении данных {#protecting-against-leaks-in-data-fetching}

Если вы используете среду Server Components, которая имеет доступ к конфиденциальным данным, вам нужно быть осторожным, чтобы не передавать объекты напрямую:

```js
// api.js
export async function getUser(id) {
    const user = await db`SELECT * FROM users WHERE id = ${id}`;
    return user;
}
```

---

```js
import { getUser } from 'api.js';
import { InfoCard } from 'components.js';

export async function Profile(props) {
    const user = await getUser(props.userId);
    // DO NOT DO THIS
    return <InfoCard user={user} />;
}
```

---

```js
// components.js
'use client';

export async function InfoCard({ user }) {
    return <div>{user.name}</div>;
}
```

В идеале функция `getUser` не должна раскрывать данные, к которым текущий пользователь не должен иметь доступа. Чтобы предотвратить передачу объекта `user` клиентскому компоненту в дальнейшем, мы можем "испортить" объект пользователя:

```js
// api.js
import { experimental_taintObjectReference } from 'react';

export async function getUser(id) {
    const user = await db`SELECT * FROM users WHERE id = ${id}`;
    experimental_taintObjectReference(
        'Do not pass the entire user object to the client. ' +
            'Instead, pick off the specific properties you ' +
            'need for this use case.',
        user
    );
    return user;
}
```

Теперь, если кто-то попытается передать объект `user` клиентскому компоненту, будет выдана ошибка с переданным сообщением об ошибке.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/experimental_taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference)</small>
