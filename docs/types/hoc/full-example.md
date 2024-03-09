---
description: Контекст отлично подходит для этого, но тогда значения из контекста могут быть использованы только в вашей функции render. HoC будет предоставлять эти значения в качестве пропсов
---

# Пример с полным HOC

> Это пример HOC, который вы можете скопировать и вставить. Если некоторые фрагменты не имеют для вас смысла, перейдите по ссылке [React HOC Docs intro](https://react-typescript-cheatsheet.netlify.app/docs/hoc/react_hoc_docs/), чтобы получить подробное описание через полный перевод документации по React на TypeScript.

Иногда вам нужен простой способ инжектировать пропсы из другого места (либо глобального хранилища, либо провайдера), и вы не хотите постоянно передавать пропсы для этого. Контекст отлично подходит для этого, но тогда значения из контекста могут быть использованы только в вашей функции `render`. HoC будет предоставлять эти значения в качестве пропсов.

**Инжектируемые пропсы**

```ts
interface WithThemeProps {
    primaryColor: string;
}
```

**Использование в компоненте**.

Цель состоит в том, чтобы пропсы были доступны в интерфейсе компонента, но вычитались для потребителей компонента при обертывании в HoC.

```ts
interface Props extends WithThemeProps {
    children?: React.ReactNode;
}

class MyButton extends React.Component<Props> {
    public render() {
        // Render an the element using the theme and other props.
    }

    private someInternalMethod() {
        // The theme values are also available as props here.
    }
}

export default withTheme(MyButton);
```

**Потребление компонента**

Теперь при потреблении компонента вы можете опустить параметр `primaryColor` или переопределить тот, который предоставляется через контекст.

```ts
<MyButton>Hello button</MyButton> // Valid
<MyButton primaryColor="#333">Hello Button</MyButton> // Also valid
```

**Объявление HoC**

Фактический HoC.

```ts
export function withTheme<
    T extends WithThemeProps = WithThemeProps
>(WrappedComponent: React.ComponentType<T>) {
    // Try to create a nice displayName for React Dev Tools.
    const displayName =
        WrappedComponent.displayName ||
        WrappedComponent.name ||
        'Component';

    // Creating the inner component. The calculated Props type here is the where the magic happens.
    const ComponentWithTheme = (
        props: Omit<T, keyof WithThemeProps>
    ) => {
        // Fetch the props you want to inject. This could be done with context instead.
        const themeProps = useTheme();

        // props comes afterwards so the can override the default ones.
        return (
            <WrappedComponent
                {...themeProps}
                {...(props as T)}
            />
        );
    };

    ComponentWithTheme.displayName = `withTheme(${displayName})`;

    return ComponentWithTheme;
}
```

Обратите внимание, что утверждение `{...(props as T)}` необходимо из-за текущей ошибки в TS 3.2 <https://github.com/Microsoft/TypeScript/issues/28938#issuecomment-450636046>.

Вот более продвинутый пример динамического компонента высшего порядка, который основывает некоторые свои параметры на пропсах передаваемого компонента:

```ts
// inject static values to a component so that they're always provided
export function inject<
    TProps,
    TInjectedKeys extends keyof TProps
>(
    Component: React.JSXElementConstructor<TProps>,
    injector: Pick<TProps, TInjectedKeys>
) {
    return function Injected(
        props: Omit<TProps, TInjectedKeys>
    ) {
        return (
            <Component
                {...(props as TProps)}
                {...injector}
            />
        );
    };
}
```

## Использование `forwardRef`

Для "настоящего" многократного использования вам также следует подумать об открытии реферера для вашего HOC. Вы можете использовать `React.forwardRef<Ref, Props>`, как описано в [базовой шпаргалке](https://github.com/typescript-cheatsheets/react/blob/main/README.md#forwardrefcreateref), но нас интересуют более реальные примеры. [Вот хороший пример на практике](https://gist.github.com/OliverJAsh/d2f462b03b3e6c24f5588ca7915d010e) от @OliverJAsh (обратите внимание - он все еще имеет некоторые неровности, нам нужна помощь, чтобы проверить это/документировать это).

## Поддержка `defaultProps` обернутого компонента

Если вам это нужно, пожалуйста, посмотрите [устаревшее обсуждение](https://github.com/typescript-cheatsheets/react/issues/86) и напишите в комментариях свои требования. При необходимости мы поднимем эту тему снова.

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/hoc/full_example></small>
