---
description: use server отмечает функции стороны сервера, которые могут быть вызваны из кода стороны клиента
---

# `'use server'`

<big>`'use server'` отмечает функции стороны сервера, которые могут быть вызваны из кода стороны клиента.</big>

<RSC>

`'use server'` нужен при [использовании серверных компонентов React](server-components.md).

</RSC>

## Описание {#reference}

### `'use server'` {#use-server}

Добавьте `'use server'` в верхней части тела async-функции, чтобы пометить функцию как вызываемую клиентом. Такие функции называют [_серверными функциями_](server-functions.md).

```js hl_lines="2"
async function addToCart(data) {
    'use server';
    // ...
}
```

При вызове серверной функции на клиенте выполняется сетевой запрос к серверу, включающий сериализованную копию всех переданных аргументов. Если серверная функция возвращает значение, оно будет сериализовано и возвращено клиенту.

Вместо того чтобы отдельно отмечать функции директивой `'use server'`, можно добавить директиву в верхнюю часть файла. Тогда все экспорты этого файла станут серверными функциями и их можно использовать где угодно, в том числе импортировать в клиентский код.

#### Замечания {#caveats}

-   Директивы `'use server'` должны находиться в самом начале своей функции или модуля; выше любого другого кода, включая импорт (комментарии над директивами - это нормально). Они должны быть написаны с одинарными или двойными кавычками, а не с обратными знаками.
-   Директива `'use server'` может быть использована только в файлах серверной части. Получившиеся серверные функции можно передавать клиентским компонентам через пропсы. Смотрите поддерживаемые [типы для сериализации](#serializable-parameters-and-return-values).
-   Чтобы импортировать серверную функцию из [кода клиента](./use-client.md), необходимо использовать директиву на уровне модуля.
-   Поскольку базовые сетевые вызовы всегда асинхронны, `'use server'` можно использовать только в асинхронных функциях.
-   Всегда рассматривайте аргументы серверных функций как недоверенный ввод и авторизуйте любые мутации. Смотрите [соображения безопасности](#security).
-   Серверные функции нужно вызывать в [переходе](../react/useTransition.md). Серверные функции, переданные в [`<form action>`](../react-dom/components/form.md#props) или [`formAction`](../react-dom/components/input.md#props), вызываются в переходе автоматически.
-   Серверные функции предназначены для мутаций, которые обновляют состояние на стороне сервера; их не рекомендуется использовать для получения данных. Соответственно, фреймворки, реализующие серверные функции, обычно обрабатывают одно действие за раз и не кэшируют возвращаемое значение.

### Соображения безопасности {#security}

Аргументы серверных функций полностью контролируются клиентом. В целях безопасности всегда рассматривайте их как недоверенный ввод и обязательно проверяйте и экранируйте аргументы.

В любой серверной функции обязательно проверяйте, что вошедшему в систему пользователю разрешено выполнять это действие.

!!!warning "В разработке"

    Чтобы предотвратить отправку конфиденциальных данных из серверной функции, существуют экспериментальные API для предотвращения передачи уникальных значений и объектов в клиентский код.

    См. [`experimental_taintUniqueValue`](../react/experimental_taintUniqueValue.md) и [`experimental_taintObjectReference`](../react/experimental_taintObjectReference.md).

### Сериализуемые аргументы и возвращаемые значения {#serializable-parameters-and-return-values}

Поскольку клиентский код вызывает серверную функцию по сети, любые передаваемые аргументы должны быть сериализуемыми.

Здесь перечислены поддерживаемые типы аргументов серверной функции:

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
-   Функции, являющиеся серверными функциями
-   [Promises](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Примечательно, что не поддерживаются:

-   React-элементы или [JSX](https://react.dev/learn/writing-markup-with-jsx)
-   Функции, включая функции компонентов или любые другие функции, которые не являются действиями сервера
-   [Classes](https://developer.mozilla.org/docs/Learn/JavaScript/Objects/Classes_in_JavaScript)
-   Объекты, являющиеся экземплярами любого класса (кроме упомянутых встроенных) или объекты с [нулевым прототипом](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)
-   Символы, не зарегистрированные глобально, например, `Symbol('mySymbol')`.
-   События из обработчиков событий

Поддерживаемые сериализуемые возвращаемые значения такие же, как [сериализуемые реквизиты](./use-client.md#passing-props-from-server-to-client-components) для граничного клиентского компонента.

## Использование {#usage}

<a id="server-actions-in-forms"></a>

### Серверные функции в формах {#server-functions-in-forms}

Чаще всего серверные функции вызывают, чтобы изменить данные. В браузере традиционный способ отправить мутацию — [элемент HTML-формы](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form). В React Server Components у серверных функций есть первоклассная поддержка как у действий в [формах](../react-dom/components/form.md).

Вот форма, в которой пользователь может запросить имя пользователя.

```js hl_lines="3"
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

В этом примере `requestUsername` — серверная функция, переданная в `<form>`. Когда пользователь отправляет форму, уходит сетевой запрос к серверной функции `requestUsername`. При вызове серверной функции из формы React передаёт [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) формы первым аргументом серверной функции.

Если передать серверную функцию в `action` формы, React может [прогрессивно улучшить](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement) форму. Это значит, что форму можно отправить ещё до загрузки пакета JavaScript.

#### Обработка возвращаемых значений в формах {#handling-return-values}

В форме запроса имени имя может оказаться занятым. `requestUsername` должна сообщить, удался запрос или нет.

Чтобы обновить интерфейс по результату серверной функции и при этом сохранить прогрессивное улучшение, используйте [`useActionState`](../react/useActionState.md).

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

```js hl_lines="4 8"
// UsernameForm.js
'use client';

import { useActionState } from 'react';
import requestUsername from './requestUsername';

function UsernameForm() {
  const [state, action] = useActionState(requestUsername, null, 'n/a');

  return (
    <>
      <form action={action}>
        <input type="text" name="username" />
        <button type="submit">Request</button>
      </form>
      <p>Last submission request returned: {state}</p>
    </>
  );
}
```

Как и большинство хуков, `useActionState` можно вызывать только в [клиентском коде](use-client.md).

<a id="calling-a-server-action-outside-of-form"></a>

### Вызов серверной функции вне `<form>` {#calling-a-server-function-outside-of-form}

Серверные функции — это открытые конечные точки сервера, и их можно вызвать из любого клиентского кода.

Если серверная функция используется вне [формы](../react-dom/components/form.md), вызывайте её в [переходе](../react/useTransition.md): так можно показать индикатор загрузки, [оптимистичные обновления состояния](../react/useOptimistic.md) и обработать неожиданные ошибки. Формы автоматически оборачивают серверные функции в переходы.

```js hl_lines="9-14"
import incrementLike from './actions';
import { useState, useTransition } from 'react';

function LikeButton() {
  const [isPending, startTransition] = useTransition();
  const [likeCount, setLikeCount] = useState(0);

  const onClick = () => {
    startTransition(async () => {
      const currentCount = await incrementLike();
      startTransition(() => {
        setLikeCount(currentCount);
      });
    });
  };

  return (
    <>
      <p>Total Likes: {likeCount}</p>
      <button onClick={onClick} disabled={isPending}>Like</button>;
    </>
  );
}
```

```js
// actions.js
'use server';

let likeCount = 0;
export default async function incrementLike() {
  likeCount++;
  return likeCount;
}
```

Чтобы прочитать возвращаемое значение серверной функции, нужно сделать `await` у возвращённого промиса.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/rsc/use-server](https://react.dev/reference/rsc/use-server)</small>
