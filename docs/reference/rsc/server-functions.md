---
description: Серверные функции позволяют клиентским компонентам вызывать асинхронные функции, которые выполняются на сервере
---

# Серверные функции

<big>

Серверные функции позволяют клиентским компонентам вызывать асинхронные функции, которые выполняются на сервере.

</big>

<RSC>

Серверные функции предназначены для [серверных компонентов React](server-components.md).

**Примечание:** до сентября 2024 года все серверные функции назывались «Server Actions». Если серверная функция передана в проп `action` или вызвана изнутри действия, это серверное действие (Server Action), но не все серверные функции являются серверными действиями. Названия в этой документации обновлены: серверные функции можно использовать для разных задач.

</RSC>

!!!note "Как обеспечить поддержку серверных функций?"

    Хотя серверные функции в React 19 стабильны и не будут ломаться между минорными версиями, базовые API, которыми бандлер или фреймворк React Server Components реализует серверные функции, не следуют semver и могут ломаться между минорными версиями React 19.x.

    Чтобы поддерживать серверные функции в бандлере или фреймворке, рекомендуем зафиксировать конкретную версию React или использовать релиз Canary. Мы продолжим работать с авторами бандлеров и фреймворков, чтобы в будущем стабилизировать API для реализации серверных функций.

Когда серверная функция объявлена с директивой [`"use server"`](use-server.md), фреймворк автоматически создаст ссылку на серверную функцию и передаст эту ссылку клиентскому компоненту. Когда функцию вызовут на клиенте, React отправит запрос на сервер, чтобы выполнить функцию, и вернёт результат.

Серверные функции можно создавать в серверных компонентах и передавать пропсами клиентским компонентам, либо импортировать и использовать в клиентских компонентах.

## Использование {#usage}

### Создание серверной функции в серверном компоненте {#creating-a-server-function-from-a-server-component}

Серверные компоненты могут объявлять серверные функции директивой `"use server"`:

```js hl_lines="7 5 12"
// Server Component
import Button from './Button';

function EmptyNote () {
  async function createNoteAction() {
    // Server Function
    'use server';

    await db.notes.create();
  }

  return <Button onClick={createNoteAction}/>;
}
```

Когда React рендерит серверный компонент `EmptyNote`, он создаёт ссылку на функцию `createNoteAction` и передаёт эту ссылку клиентскому компоненту `Button`. Когда кнопку нажмут, React отправит запрос на сервер, чтобы выполнить функцию `createNoteAction` по переданной ссылке:

```js hl_lines="5"
"use client";

export default function Button({onClick}) {
  console.log(onClick);
  // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNoteAction'}
  return <button onClick={() => onClick()}>Create Empty Note</button>
}
```

Подробнее см. документацию по [`"use server"`](use-server.md).

### Импорт серверных функций из клиентских компонентов {#importing-server-functions-from-client-components}

Клиентские компоненты могут импортировать серверные функции из файлов с директивой `"use server"`:

```js hl_lines="3"
"use server";

export async function createNote() {
  await db.notes.create();
}

```

Когда бандлер собирает клиентский компонент `EmptyNote`, он создаёт в бандле ссылку на функцию `createNote`. Когда нажмут `button`, React отправит запрос на сервер, чтобы выполнить функцию `createNote` по переданной ссылке:

```js hl_lines="2 5 7"
"use client";
import {createNote} from './actions';

function EmptyNote() {
  console.log(createNote);
  // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNote'}
  <button onClick={() => createNote()} />
}
```

Подробнее см. документацию по [`"use server"`](use-server.md).

### Серверные функции с действиями {#server-functions-with-actions}

Серверные функции можно вызывать из действий на клиенте:

```js hl_lines="3"
"use server";

export async function updateName(name) {
  if (!name) {
    return {error: 'Name is required'};
  }
  await db.users.updateName(name);
}
```

```js hl_lines="3 13 11 25"
"use client";

import {updateName} from './actions';

function UpdateName() {
  const [name, setName] = useState('');
  const [error, setError] = useState(null);

  const [isPending, startTransition] = useTransition();

  const submitAction = async () => {
    startTransition(async () => {
      const {error} = await updateName(name);
      startTransition(() => {
        if (error) {
          setError(error);
        } else {
          setName('');
        }
      });
    })
  }

  return (
    <form action={submitAction}>
      <input type="text" name="name" disabled={isPending}/>
      {error && <span>Failed: {error}</span>}
    </form>
  )
}
```

Так можно получить состояние `isPending` серверной функции, обернув её в действие на клиенте.

Подробнее см. документацию [Вызов серверной функции вне `<form>`](use-server.md#calling-a-server-function-outside-of-form)

### Серверные функции с действиями формы {#using-server-functions-with-form-actions}

Серверные функции работают с новыми возможностями форм в React 19.

Серверную функцию можно передать форме, чтобы форма автоматически отправлялась на сервер:

```js hl_lines="3 7"
"use client";

import {updateName} from './actions';

function UpdateName() {
  return (
    <form action={updateName}>
      <input type="text" name="name" />
    </form>
  )
}
```

Если отправка формы прошла успешно, React автоматически сбросит форму. Добавьте `useActionState`, чтобы получить состояние ожидания, последний ответ или поддержать прогрессивное улучшение.

Подробнее см. документацию [Серверные функции в формах](use-server.md#server-functions-in-forms).

### Серверные функции с `useActionState` {#server-functions-with-use-action-state}

Серверные функции можно вызывать через `useActionState` в типичном случае, когда нужны только состояние ожидания действия и последний возвращённый ответ:

```js hl_lines="3 6 9"
"use client";

import {updateName} from './actions';

function UpdateName() {
  const [state, submitAction, isPending] = useActionState(updateName, {error: null});

  return (
    <form action={submitAction}>
      <input type="text" name="name" disabled={isPending}/>
      {state.error && <span>Failed: {state.error}</span>}
    </form>
  );
}
```

Если `useActionState` используется вместе с серверными функциями, React также автоматически повторит отправки формы, сделанные до окончания гидратации. Пользователи смогут взаимодействовать с приложением ещё до того, как оно гидратируется.

Подробнее см. документацию [`useActionState`](../react/useActionState.md).

### Прогрессивное улучшение с `useActionState` {#progressive-enhancement-with-useactionstate}

Серверные функции также поддерживают прогрессивное улучшение через третий аргумент `useActionState`.

```js hl_lines="3 6 9"
"use client";

import {updateName} from './actions';

function UpdateName() {
  const [, submitAction] = useActionState(updateName, null, `/name/update`);

  return (
    <form action={submitAction}>
      ...
    </form>
  );
}
```

Если в `useActionState` передана постоянная ссылка, React перенаправит на указанный URL, когда форма отправлена до загрузки бандла JavaScript.

Подробнее см. документацию [`useActionState`](../react/useActionState.md).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/rsc/server-functions](https://react.dev/reference/rsc/server-functions)</small>
