---
description: Серверные Actions позволяют клиентским компонентам вызывать асинхронные функции, выполняемые на сервере
status: experimental
---

# Серверные Actions

<big>
Серверные Actions позволяют клиентским компонентам вызывать асинхронные функции, выполняемые на сервере.
</big>

!!!note "Как обеспечить поддержку серверных Actions?"

    Хотя серверные Actions в React 19 стабильны и не ломаются между основными версиями, базовые API, используемые для реализации серверных Actions в бандлере или фреймворке React Server Components, не соответствуют semver и могут ломаться между минимальными версиями React 19.x.

    Чтобы поддерживать серверные Actions в виде бандлера или фреймворка, мы рекомендуем привязать их к определенной версии React или использовать релиз Canary. Мы продолжим работу с бандлерами и фреймворками, чтобы стабилизировать API, используемые для реализации серверных Actions, в будущем.

Когда серверное действие определено с помощью директивы `"use server"`, ваш фреймворк автоматически создаст ссылку на серверную функцию и передаст ее клиентскому компоненту. Когда эта функция будет вызвана на клиенте, React отправит запрос на сервер для выполнения функции и вернет результат.

Серверные Actions могут быть созданы в серверных компонентах и переданы в качестве пропсов клиентским компонентам, или же они могут быть импортированы и использованы в клиентских компонентах.

## Создание серверного действия из серверного компонента {#creating-a-server-action-from-a-server-component}

Серверные компоненты могут определять серверные Actions с помощью директивы `"use server"`:

```js
// Server Component
import Button from './Button';

function EmptyNote() {
    async function createNoteAction() {
        // Server Action
        'use server';

        await db.notes.create();
    }

    return <Button onClick={createNoteAction} />;
}
```

Когда React отображает серверный компонент `EmptyNote`, он создает ссылку на функцию `createNoteAction` и передает эту ссылку клиентскому компоненту `Button`. Когда кнопка будет нажата, React отправит запрос на сервер для выполнения функции `createNoteAction` с указанной ссылкой:

```js hl_lines="5-8"
'use client';

export default function Button({ onClick }) {
    console.log(onClick);
    // {
    //   $$typeof: Symbol.for("react.server.reference"),
    //   $$id: 'createNoteAction'
    // }
    return (
        <button onClick={onClick}>Create Empty Note</button>
    );
}
```

Подробнее см. документацию по [`"use server"`](./use-server.md).

## Импорт серверных Actions из клиентских компонентов {#importing-server-actions-from-client-components}

Клиентские компоненты могут импортировать серверные Actions из файлов, использующих директиву `"use server"`:

```js
'use server';

export async function createNoteAction() {
    await db.notes.create();
}
```

При сборке клиентского компонента `EmptyNote` в сборке будет создана ссылка на функцию `createNoteAction`. Когда `button` будет нажата, React отправит запрос на сервер для выполнения функции `createNoteAction`, используя предоставленную ссылку:

```js
'use client';
import { createNoteAction } from './actions';

function EmptyNote() {
    console.log(createNoteAction);
    // {
    //   $$typeof: Symbol.for("react.server.reference"),
    //   $$id: 'createNoteAction'
    // }
    <button onClick={createNoteAction} />;
}
```

Подробнее см. документацию для [`"use server"`](./use-server.md).

## Компоновка серверных Actions с Actions {#composing-server-actions-with-actions}

Серверные Actions могут быть составлены с Actions на клиенте:

```js
'use server';

export async function updateName(name) {
    if (!name) {
        return { error: 'Name is required' };
    }
    await db.users.updateName(name);
}
```

---

```js
'use client';

import { updateName } from './actions';

function UpdateName() {
    const [name, setName] = useState('');
    const [error, setError] = useState(null);

    const [isPending, startTransition] = useTransition();

    const submitAction = async () => {
        startTransition(async () => {
            const { error } = await updateName(name);
            if (!error) {
                setError(error);
            } else {
                setName('');
            }
        });
    };

    return (
        <form action={submitAction}>
            <input
                type="text"
                name="name"
                disabled={isPending}
            />
            {state.error && (
                <span>Failed: {state.error}</span>
            )}
        </form>
    );
}
```

Это позволяет вам получить доступ к состоянию `isPending` серверного действия, обернув его в действие на клиенте.

Подробнее см. документацию по [Вызов серверного действия вне `<form>`](./use-server.md#calling-a-server-action-outside-of-form)

## Действия формы с серверными действиями {#form-actions-with-server-actions}

Серверные Actions работают с новыми функциями форм в React 19.

Вы можете передать серверное действие в форму, чтобы автоматически отправить форму на сервер:

```js
'use client';

import { updateName } from './actions';

function UpdateName() {
    return (
        <form action={updateName}>
            <input type="text" name="name" />
        </form>
    );
}
```

Когда отправка формы пройдет успешно, React автоматически сбросит форму. Вы можете добавить `useActionState` для доступа к состоянию ожидания, последнему ответу или для поддержки прогрессивного улучшения.

Подробнее см. документацию по [Серверным Actions in Forms](./use-server.md#server-actions-in-forms).

## Серверные Actions с `useActionState` {#server-actions-with-use-action-state}

Вы можете скомпоновать серверные Actions с `useActionState` для распространенного случая, когда вам нужен доступ к состоянию ожидания действия и последнему возвращенному ответу:

```js
'use client';

import { updateName } from './actions';

function UpdateName() {
    const [
        submitAction,
        state,
        isPending,
    ] = useActionState(updateName, { error: null });

    return (
        <form action={submitAction}>
            <input
                type="text"
                name="name"
                disabled={isPending}
            />
            {state.error && (
                <span>Failed: {state.error}</span>
            )}
        </form>
    );
}
```

При использовании `useActionState` с серверными Actions, React также будет автоматически воспроизводить отправленные формы до завершения гидратации. Это означает, что пользователи могут взаимодействовать с вашим приложением даже до того, как оно будет гидратировано.

Подробнее см. документацию для [`useActionState`](../react/useActionState.md).

## Прогрессивное улучшение с `useActionState` {#progressive-enhancement-with-useactionstate}

Серверные Actions также поддерживают прогрессивное улучшение с помощью третьего аргумента `useActionState`.

```js
'use client';

import { updateName } from './actions';

function UpdateName() {
    const [, submitAction] = useActionState(
        updateName,
        null,
        `/name/update`
    );

    return <form action={submitAction}>...</form>;
}
```

При указании `permalink` для `useActionState`, React перенаправит на указанный URL, если форма будет отправлена до загрузки сборки JavaScript.

Подробнее см. документацию для [`useActionState`](../react/useActionState.md).

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/rsc/server-actions></small>
