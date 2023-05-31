# useEffectEvent

!!!warning "Этот API является экспериментальным и пока не доступен в стабильной версии React."

    Вы можете попробовать его, обновив пакеты React до последней экспериментальной версии:

    - `react@experimental`
    - `react-dom@experimental`
    - `eslint-plugin-react-hooks@experimental`.

    Экспериментальные версии React могут содержать ошибки. Не используйте их в производстве.

`useEffectEvent` - это хук React, который позволяет вам извлекать нереактивную логику в [событие эффекта](../learn/separating-events-from-effects.md).

```js
const onSomething = useEffectEvent(callback);
```

## Ссылки

-   [https://react.dev/reference/react/experimental_useEffectEvent](https://react.dev/reference/react/experimental_useEffectEvent)
