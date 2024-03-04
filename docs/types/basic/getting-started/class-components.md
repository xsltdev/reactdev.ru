---
description: В TypeScript React.Component является общим типом (он же React.Component&lt;PropType, StateType&gt;), поэтому вы можете предоставить ему (необязательные) параметры типа prop и state
---

# Классовые компоненты

В TypeScript `React.Component` является общим типом (он же `React.Component<PropType, StateType>`), поэтому вы можете предоставить ему (необязательные) параметры типа `prop` и `state`:

```ts
type MyProps = {
    // использование `interface` также нормально
    message: string;
};
type MyState = {
    count: number; // как это
};
class App extends React.Component<MyProps, MyState> {
    state: MyState = {
        // необязательная вторая аннотация для более
        // точного определения типа
        count: 0,
    };
    render() {
        return (
            <div>
                {this.props.message} {this.state.count}
            </div>
        );
    }
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCmATzCTgFlqAFHMAZzgF44BvCuHAD0QuAFd2wAHYBzOAANpMJFEzok8uME4oANuwhwIAawFwQSduxQykALjjsYUaTIDcFAL4fyNOo2oAZRgUZW4+MzQIMSkYBykxEAAjFTdhUV1gY3oYAAttLx80XRQrOABBMDA4JAAPZSkAE05kdBgAOgBhXEgpJFiAHiZWCA4AGgDg0KQAPgjyQSdphyYpsJ5+BcF0ozAYYAgpPUckKKa4FCkpCBD9w7hMaDgUmGUoOD96aUwVfrQkMyCKIxOJwAAMZm8ZiITRUAAoAJTzbZwIgwMRQKRwOGA7YDRrAABuM1xKN4eW07TAbHY7QsVhsSE8fAptKWynawNinlJcAGQgJxNxCJ8gh55E8QA)

Не забывайте, что вы можете экспортировать/импортировать/расширять эти типы/интерфейсы для повторного использования.

!!!note "Зачем дважды аннотировать `state`?"

    Аннотировать свойство класса `state` не обязательно, но это позволяет лучше определять тип при обращении к `this.state`, а также при инициализации состояния.

    Это происходит потому, что они работают по-разному: 2-й параметр общего типа позволит `this.setState()` работать корректно, потому что этот метод исходит от базового класса, но инициализация `state` внутри компонента переопределяет базовую реализацию, поэтому вам нужно убедиться, что вы сообщите компилятору, что на самом деле вы не делаете ничего другого.

    [См. комментарий @ferdaber здесь](https://github.com/typescript-cheatsheets/react/issues/57).

!!!note "Нет необходимости в `readonly`"

    Вы часто видите примеры кода, включающие `readonly`, чтобы пометить свойства и состояние неизменяемыми:

    ```ts
    type MyProps = {
    	readonly message: string;
    };
    type MyState = {
    	readonly count: number;
    };
    ```

    В этом нет необходимости, поскольку `React.Component<P,S>` уже помечает их как неизменяемые. ([См. PR и обсуждение!](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/26813))

**Методы классов**: Делайте все как обычно, но помните, что любые аргументы для ваших функций также должны быть типизированы:

```ts
class App extends React.Component<
    { message: string },
    { count: number }
> {
    state = { count: 0 };
    render() {
        return (
            <div onClick={() => this.increment(1)}>
                {this.props.message} {this.state.count}
            </div>
        );
    }
    increment = (amt: number) => {
        // like this
        this.setState((state) => ({
            count: state.count + amt,
        }));
    };
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCtAGxQGc64BBMMOJADxiQDsATRsnQwAdAGFckHrxgAeAN5wQSBigDmSAFxw6MKMB5q4AXwA0cRWggBXHjG09rIAEZIoJgHwWKcHTBTccAC8FnBWtvZwAAwmANw+cET8bgAUAJTe5L6+RDDWUDxwKQnZcLJ8wABucBA8YtTAaADWQfLpwV4wABbAdCIGaETKdikAjGnGHiWlFt29ImA4YH3KqhrGsz19ugFIIuF2xtO+sgD0FZVTWdlp8ddH1wNDMsFFKCCRji5uGUFe8tNTqc4A0mkg4HM6NNISI6EgYABlfzcFI7QJ-IoA66lA6RNF7XFwADUcHeMGmxjStwSxjuxiAA)

**Свойства класса**: Если вам нужно объявить свойства класса для последующего использования, просто объявите их как `state`, но без присваивания:

```ts
class App extends React.Component<{
    message: string;
}> {
    pointer: number; // like this
    componentDidMount() {
        this.pointer = 3;
    }
    render() {
        return (
            <div>
                {this.props.message} and {this.pointer}
            </div>
        );
    }
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCtAGxQGc64BBMMOJADxiQDsATRsnQwAdAGFckHrxgAeAN4U4cEEgYoA5kgBccOjCjAeGgNwUAvgD44i8sshHuUXTwCuIAEZIoJuAHo-OGpgAGskOBgAC2A6JTg0SQhpHhgAEWA+AFkIVxSACgBKGzjlKJiRBxTvOABeOABmMzs4cziifm9C4ublIhhXKB44PJLlOFk+YAA3S1GxmzK6CpwwJdV1LXM4FH4F6KXKp1aesdk-SZnRgqblY-MgA)

## Типизация `getDerivedStateFromProps`

Прежде чем начать использовать `getDerivedStateFromProps`, ознакомьтесь с [документацией](https://reactjs.org/docs/react-component.html#static-getderivedstatefromprops) и [Возможно, вам не нужны производные состояния](https://reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html). Производное состояние может быть реализовано с помощью хуков, которые также могут помочь в настройке мемоизации.

Вот несколько способов, которыми вы можете аннотировать `getDerivedStateFromProps`.

1.  Если вы явно типизировали свое производное состояние и хотите убедиться, что возвращаемое значение из `getDerivedStateFromProps` соответствует ему.

    ```ts
    class Comp extends React.Component<Props, State> {
        static getDerivedStateFromProps(
            props: Props,
            state: State
        ): Partial<State> | null {
            //
        }
    }
    ```

2.  Когда вы хотите, чтобы возвращаемое значение функции определяло ваше состояние.

    ```ts
    class Comp extends React.Component<
        Props,
        ReturnType<typeof Comp['getDerivedStateFromProps']>
    > {
        static getDerivedStateFromProps(props: Props) {}
    }
    ```

3.  Если вам нужно производное состояние с другими полями состояния и мемоизацией

    ```ts
    type CustomValue = any;
    interface Props {
        propA: CustomValue;
    }
    interface DefinedState {
        otherStateField: string;
    }
    type State = DefinedState &
        ReturnType<typeof transformPropsToState>;
    function transformPropsToState(props: Props) {
        return {
            savedPropA: props.propA, // save for memoization
            derivedState: props.propA,
        };
    }
    class Comp extends React.PureComponent<Props, State> {
        constructor(props: Props) {
            super(props);
            this.state = {
                otherStateField: '123',
                ...transformPropsToState(props),
            };
        }
        static getDerivedStateFromProps(
            props: Props,
            state: State
        ) {
            if (isEqual(props.propA, state.savedPropA))
                return null;
            return transformPropsToState(props);
        }
    }
    ```

[посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoUSWOYAZwFEBHAVxQBs5tcD2IATFHQAWAOnpJWHMuQowAnmCRwAwizoxcANQ4tlAXjgoAdvIDcFYMZhIomdMoAKOMHTgBvCnDhgXAQQAuVXVNEB12PQtyAF9La1t7NGUAESRMKyR+AGUYFBsPLzgIGGFbHLykADFgJHZ+II0oKwBzKNjyBSU4cvzDVPTjTJ7lADJEJBgWKGMAFUUkAB5OpAhMOBgoEzpMaBBnCFcZiGGAPijMFmMMYAhjdc3jbd39w+PcmwAKXwO6IJe6ACUBXI3iIk2mwO83joKAAbpkXoEfC46KJvmA-AAaOAAehxcBh8K40DgICQIAgwAAXnkbsZCt5+LZgPDsu8kEF0aj0X5CtE2hQ0OwhG4VLgwHAkAAPGzGfhuZDoGCiRxTJBi8C3JDWBb-bGnSFwNC3RosDDQL4ov4ooGeEFQugsJRQS0-AFRKHrYT0UQaCpwQx2z3eYqlKDDaq1epwABEAEYAEwAZhjmIZUNEmY2Wx2UD2KKOw1drgB6f5fMKfpgwDQcGaE1STVZEZw+Z+xd+cD1BPZQWGtvTwDWH3ozDY7A7aP82KrSF9cIR-gBQLBUzuxhY7HYHqhq4h2ceubbryLXPdFZiQA)

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/class_components></small>
