---
status: experimental
description: use server отмечает функции стороны сервера, которые могут быть вызваны из кода стороны клиента
---

# `'use server'`

!!!example "Canary"

    `'use server'` необходимо только в том случае, если вы [используете React Server Components](../../learn/start-a-new-react-project.md#bleeding-edge-react-frameworks) или собираете совместимую с ними библиотеку.

<big>`'use server'` отмечает функции стороны сервера, которые могут быть вызваны из кода стороны клиента.</big>

## Описание {#reference}

### `'use server'` {#use-server}

Добавьте `'use server'` в верхней части тела async-функции, чтобы пометить функцию как вызываемую клиентом. Мы называем эти функции _серверными действиями_.

```js hl_lines="2"
async function addToCart(data) {
    'use server';
    // ...
}
```

При вызове действия сервера на клиенте выполняется сетевой запрос к серверу, включающий сериализованную копию всех переданных аргументов. Если действие сервера возвращает значение, оно будет сериализовано и возвращено клиенту.

Вместо того чтобы отдельно отмечать функции с `использовать сервер`, вы можете добавить директиву в верхнюю часть файла, чтобы отметить все экспортируемые функции в этом файле как Server Actions, которые могут быть использованы где угодно, включая импортированные в клиентский код.

#### Замечания {#caveats}

-   Директивы `'use server'` должны находиться в самом начале своей функции или модуля; выше любого другого кода, включая импорт (комментарии над директивами - это нормально). Они должны быть написаны с одинарными или двойными кавычками, а не с обратными знаками.
-   Директива `'use server'` может быть использована только в файлах серверной части. Результирующие действия сервера могут быть переданы клиентским компонентам через реквизиты. Смотрите поддерживаемые [типы для сериализации](#serializable-parameters-and-return-values).
-   Чтобы импортировать действие сервера из [кода клиента](./use-client.md), необходимо использовать директиву на уровне модуля.
-   Поскольку базовые сетевые вызовы всегда асинхронны, `'use server'` можно использовать только в асинхронных функциях.
-   Всегда рассматривайте аргументы к действиям сервера как недоверенный ввод и авторизуйте любые мутации. Смотрите [соображения безопасности](#security).
-   Действия сервера должны вызываться в [transition](./useTransition.md). Действия сервера, переданные в [`<form action>`](../react-dom/components/form.md#props) или [`formAction`](../react-dom/components/input.md#props), будут автоматически вызваны в переходе.
-   Server Actions предназначены для мутаций, которые обновляют состояние на стороне сервера; их не рекомендуется использовать для получения данных. Соответственно, фреймворки, реализующие Server Actions, обычно обрабатывают одно действие за раз и не имеют возможности кэшировать возвращаемое значение.

### Соображения безопасности {#security}

Аргументы действий сервера полностью контролируются клиентом. В целях безопасности всегда рассматривайте их как недоверенный ввод и обязательно проверяйте и экранируйте аргументы.

В любом действии сервера обязательно проверяйте, что вошедшему в систему пользователю разрешено выполнять это действие.

!!!warning "В разработке"

    Чтобы предотвратить отправку конфиденциальных данных из серверного действия, существуют экспериментальные API для предотвращения передачи уникальных значений и объектов в клиентский код.

    См. [`experimental_taintUniqueValue`](./experimental_taintUniqueValue.md) и [`experimental_taintObjectReference`](./experimental_taintObjectReference.md).

### Сериализуемые аргументы и возвращаемые значения {#serializable-parameters-and-return-values}

Поскольку клиентский код вызывает действие сервера по сети, любые передаваемые аргументы должны быть сериализуемыми.

Здесь перечислены поддерживаемые типы аргументов серверного действия:

-   Примитивы
    -   [строка](https://developer.mozilla.org/docs/Glossary/String)
    -   [число](https://developer.mozilla.org/docs/Glossary/Number)
    -   [bigint](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/BigInt)
    -   [boolean](https://developer.mozilla.org/docs/Glossary/Boolean)
    -   [undefined](https://developer.mozilla.org/docs/Glossary/Undefined)
    -   [null](https://developer.mozilla.org/docs/Glossary/Null)
    -   [symbol](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Symbol), только символы, зарегистрированные в глобальном реестре Symbol через [`Symbol.for`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Symbol/for)
-   Iterables, содержащие сериализуемые значения
    -   [String](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String)
    -   [Array](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array)
    -   [Map](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map)
    -   [Set](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Set)
    -   [TypedArray](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) и [ArrayBuffer](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)
-   [Date](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date)
-   [FormData](https://developer.mozilla.org/docs/Web/API/FormData) экземпляры
-   Обычные [объекты](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object): созданные с помощью [инициализаторов объектов](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Object_initializer), с сериализуемыми свойствами
-   Функции, являющиеся действиями сервера
-   [Promises](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Примечательно, что не поддерживаются:

-   React-элементы или [JSX](https://react.dev/learn/writing-markup-with-jsx)
-   Функции, включая функции компонентов или любые другие функции, которые не являются действиями сервера
-   [Classes](https://developer.mozilla.org/docs/Learn/JavaScript/Objects/Classes_in_JavaScript)
-   Объекты, являющиеся экземплярами любого класса (кроме упомянутых встроенных) или объекты с [нулевым прототипом](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)
-   Символы, не зарегистрированные глобально, например, `Symbol('mySymbol')`.

Поддерживаемые сериализуемые возвращаемые значения такие же, как [сериализуемые реквизиты](./use-client.md#passing-props-from-server-to-client-components) для граничного клиентского компонента.

## Использование {#usage}

### Действия сервера в формах {#server-actions-in-forms}

Наиболее распространенным вариантом использования Server Actions будет вызов серверных функций, которые изменяют данные. В браузере традиционным способом отправки мутации является [элемент HTML-формы](https://developer.mozilla.org/docs/Web/HTML/Element/form). В React Server Components React представляет первоклассную поддержку Server Actions в [forms](../react-dom/components/form.md).

Здесь представлена форма, позволяющая пользователю запросить имя пользователя.

```js
// App.js

async function requestUsername(formData) {
    'use server';
    const username = formData.get('username');
    // ...
}

export default function App() {
    return (
        <form action={requestUsername}>
            <input type="text" name="username" />
            <button type="submit">Request</button>
        </form>
    );
}
```

В этом примере `requestUsername` - это действие сервера, переданное в `<form>`. Когда пользователь отправляет эту форму, происходит сетевой запрос к серверной функции `requestUsername`. При вызове серверного действия в форме React передает [`FormData`](https://developer.mozilla.org/docs/Web/API/FormData) в качестве первого аргумента серверному действию.

Передавая серверное действие форме `action`, React может [постепенно улучшать](https://developer.mozilla.org/docs/Glossary/Progressive_Enhancement) форму. Это означает, что формы могут быть отправлены до загрузки пакета JavaScript.

#### Обработка возвращаемых значений в формах {#handling-return-values}

В форме запроса имени пользователя может возникнуть ситуация, когда имя пользователя недоступно. Функция `requestUsername` должна сообщать нам о том, не удалось выполнить запрос или нет.

Чтобы обновить пользовательский интерфейс на основе результата действия сервера, поддерживая прогрессивное улучшение, используйте [`useFormState`](../react-dom/hooks/useFormState.md).

```js
// requestUsername.js
'use server';

export default async function requestUsername(formData) {
    const username = formData.get('username');
    if (canRequest(username)) {
        // ...
        return 'successful';
    }
    return 'failed';
}
```

---

```js hl_lines="4 8-11"
// UsernameForm.js
'use client';

import { useFormState } from 'react-dom';
import requestUsername from './requestUsername';

function UsernameForm() {
    const [returnValue, action] = useFormState(
        requestUsername,
        'n/a'
    );

    return (
        <>
            <form action={action}>
                <input type="text" name="username" />
                <button type="submit">Request</button>
            </form>
            <p>
                Last submission request returned:{' '}
                {returnValue}
            </p>
        </>
    );
}
```

Обратите внимание, что, как и большинство хуков, `useFormState` может быть вызван только в [клиентском коде](./use-client.md).

### Вызов серверного действия вне `<form>` {#calling-a-server-action-outside-of-form}

Действия сервера являются открытыми конечными точками сервера и могут быть вызваны в любом месте клиентского кода.

При использовании действия сервера вне [формы](../react-dom/components/form.md) вызывайте его в [переходе](./useTransition.md), что позволит вам отображать индикатор загрузки, показывать [оптимистичные обновления состояния](./useOptimistic.md) и обрабатывать неожиданные ошибки. Формы автоматически оборачивают действия сервера в переходы.

```js hl_lines="9-12"
import incrementLike from './actions';
import { useState, useTransition } from 'react';

function LikeButton() {
    const [isPending, startTransition] = useTransition();
    const [likeCount, setLikeCount] = useState(0);

    const onClick = () => {
        startTransition(async () => {
            const currentCount = await incrementLike();
            setLikeCount(currentCount);
        });
    };

    return (
        <>
            <p>Total Likes: {likeCount}</p>
            <button onClick={onClick} disabled={isPending}>
                Like
            </button>;
        </>
    );
}
```

---

```js
// actions.js
'use server';

let likeCount = 0;
export default async function incrementLike() {
    likeCount++;
    return likeCount;
}
```

Чтобы прочитать возвращаемое значение действия сервера, вам нужно `await` возвращаемого обещания.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/use-server](https://react.dev/reference/react/use-server)</small>
