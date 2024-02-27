---
description: На этой странице перечислены все хуки из пакета react-dom
---

# Встроенные хуки React DOM

<big>Пакет `react-dom` содержит хуки, которые поддерживаются только для веб-приложений (которые работают в среде DOM браузера). Эти хуки не поддерживаются в небраузерных средах, таких как приложения для iOS, Android или Windows. Если вы ищете хуки, которые поддерживаются в веб-браузерах _и других средах_, смотрите [страницу React Хуки](../../react/hooks.md). На этой странице перечислены все хуки из пакета `react-dom`.</big>

## Хуки формы {#form-hooks}

!!!example "Canary"

    В настоящее время хуки форм доступны только в канале React canary и экспериментальном канале. Подробнее о [каналах выпуска React здесь](https://react.dev/community/versioning-policy#all-release-channels).

Формы позволяют создавать интерактивные элементы управления для отправки информации. Для управления формами в ваших компонентах используйте один из этих хуков:

-   [`useFormStatus`](./useFormStatus.md) позволяет вносить обновления в пользовательский интерфейс на основе статуса формы.
-   [`useFormState`](./useFormState.md) позволяет управлять состоянием внутри формы.

```js
function Form({ action }) {
    async function increment(n) {
        return n + 1;
    }
    const [count, incrementFormAction] = useFormState(
        increment,
        0
    );
    return (
        <form action={action}>
            <button formAction={incrementFormAction}>
                Count: {count}
            </button>
            <Button />
        </form>
    );
}

function Button() {
    const { pending } = useFormStatus();
    return (
        <button disabled={pending} type="submit">
            Submit
        </button>
    );
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/hooks](https://react.dev/reference/react-dom/hooks)</small>
