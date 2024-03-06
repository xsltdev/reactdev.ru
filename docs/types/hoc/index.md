---
description: Этот HOC Cheatsheet собирает все доступные знания для написания компонентов высшего порядка с помощью React и TypeScript
---

# Шпаргалка по HOC

**Этот HOC Cheatsheet** собирает все доступные знания для написания компонентов высшего порядка с помощью React и TypeScript.

-   Изначально мы будем ориентироваться на [официальную документацию по HOC](https://reactjs.org/docs/higher-order-components.html).
-   Несмотря на существование хуков, многие библиотеки и кодовые базы по-прежнему нуждаются в HOC.
-   Реквизиты рендера могут быть рассмотрены в будущем
-   Цель состоит в том, чтобы писать HOC, которые обеспечивают безопасность типов и при этом не мешают.

Вот базовый пример HOC, который вы можете скопировать прямо сейчас:

```ts
type PropsAreEqual<P> = (
    prevProps: Readonly<P>,
    nextProps: Readonly<P>
) => boolean;

const withSampleHoC = <P extends {}>(
    component: {
        (props: P): Exclude<React.ReactNode, undefined>;
        displayName?: string;
    },
    propsAreEqual?: PropsAreEqual<P> | false,

    componentName = component.displayName ?? component.name
): {
    (props: P): React.JSX.Element;
    displayName: string;
} => {
    function WithSampleHoc(props: P) {
        //Do something special to justify the HoC.
        return component(props) as React.JSX.Element;
    }

    WithSampleHoc.displayName = `withSampleHoC(${componentName})`;

    let wrappedComponent =
        propsAreEqual === false
            ? WithSampleHoc
            : React.memo(WithSampleHoc, propsAreEqual);

    //copyStaticProperties(component, wrappedComponent);

    return wrappedComponent as typeof WithSampleHoc;
};
```

Этот код соответствует следующим критериям:

1.  Позволяет компоненту возвращать допустимые элементы (`string | array | boolean | null | number`), а не только `React.JSX.Element | null`.
2.  Обертывает его в мемо, если вы не откажетесь от этого.
3.  Удаляет вложенный компонент, поэтому инструменты React Dev будут показывать только один компонент.
4.  Указывает с помощью `displayName` в React Dev Tool с аннотацией, что это компонент, обернутый в два HoCs.
5.  Необязательно: Копирует статические свойства, которые могли быть определены в исходном компоненте.

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/hoc/></small>
