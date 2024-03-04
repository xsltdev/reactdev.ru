---
description: defaultProps со временем будет устаревшим, общее мнение - использовать значения объектов по умолчанию
---

# Типизация defaultProps

## Возможно, вам не нужен `defaultProps`

Согласно [этому твиту](https://twitter.com/dan_abramov/status/1133878326358171650), `defaultProps` со временем будет устаревшим. Вы можете ознакомиться с обсуждениями здесь:

-   [Оригинальный твит](https://twitter.com/hswolff/status/1133759319571345408)
-   Дополнительную информацию можно найти в [этой статье](https://medium.com/@matanbobi/react-defaultprops-is-dying-whos-the-contender-443c19d9e7f1)

Общее мнение - использовать значения объектов по умолчанию.

Компоненты функций:

```ts
type GreetProps = { age?: number };

const Greet = ({ age = 21 }: GreetProps) => // etc
```

Классовые компоненты:

```ts
type GreetProps = {
    age?: number;
};

class Greet extends React.Component<GreetProps> {
    render() {
        const { age = 21 } = this.props;
        /*...*/
    }
}

let el = <Greet age={3} />;
```

## Типизация `defaultProps`

Вывод типов для `defaultProps` значительно улучшился в [TypeScript 3.0+](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-0.html), хотя [некоторые крайние случаи все еще проблематичны](https://github.com/typescript-cheatsheets/react/issues/61).

**Функциональные компоненты**

```ts
// используя typeof как сокращение; обратите внимание,
// что это поднимает! Вы также можете объявить тип DefaultProps,
// если вы выберете, например
// https://github.com/typescript-cheatsheets/react/issues/415#issuecomment-841223219
type GreetProps = { age: number } & typeof defaultProps;

const defaultProps = {
    age: 21,
};

const Greet = (props: GreetProps) => {
    // etc
};
Greet.defaultProps = defaultProps;
```

_[Посмотреть в TS Playground](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAKjgQwM5wEoFNkGN4BmUEIcARFDvmQNwBQdMAnmFnAOKVYwAKxY6ALxwA3igDmWAFxwAdgFcQAIyxQ4AXzgAyOM1YQCcACZYCyeQBte-VPVwRZqeCbOXrEAXGEi6cCdLgAJgBGABo6dXo6e0d4TixuLzgACjAbGXjuPg9UAEovAD5RXzhKGHkoWTgAHiNgADcCkTScgDpkSTgAeiQFZVVELvVqrrrGiPpMmFaXcytsz2FZtwXbOiA)_

Для **Классовых компонентов** существует [несколько способов сделать это](https://github.com/typescript-cheatsheets/react/pull/103#issuecomment-481061483) (включая использование типа утилиты `Pick`), но рекомендация заключается в "обратном" определении реквизита:

```ts
type GreetProps = typeof Greet.defaultProps & {
    age: number;
};

class Greet extends React.Component<GreetProps> {
    static defaultProps = {
        age: 21,
    };
    /*...*/
}

// Проверка типов! Утверждения типов не нужны!
let el = <Greet age={3} />;
```

!!!info "Нюанс `React.JSX.LibraryManagedAttributes` для авторов библиотек"

    Вышеописанные реализации отлично подходят для создателей приложений, но иногда вы хотите иметь возможность экспортировать `GreetProps`, чтобы другие могли его использовать. Проблема здесь в том, что при определении `GreetProps`, `age` является обязательным свойством, когда оно не является таковым из-за `defaultProps`.

    Здесь нужно понимать, что [`GreetProps` - это _внутренний_ контракт вашего компонента, а не _внешний_, обращенный к потребителю контракт](https://github.com/typescript-cheatsheets/react/issues/66#issuecomment-453878710). Вы можете создать отдельный тип специально для экспорта или воспользоваться утилитой `React.JSX.LibraryManagedAttributes`:

    ```ts
    // внутренний контракт, не должен быть экспортирован за пределы
    type GreetProps = {
    	age: number;
    };

    class Greet extends Component<GreetProps> {
    	static defaultProps = { age: 21 };
    }

    // внешний контракт
    export type ApparentGreetProps = React.JSX.LibraryManagedAttributes<
    	typeof Greet,
    	GreetProps
    >;
    ```

    Это будет работать правильно, хотя наведение курсора на `ApparentGreetProps` может быть немного пугающим. Вы можете сократить этот шаблон с помощью утилиты `ComponentProps`, о которой мы расскажем ниже.

## Использование пропсов компонента с defaultProps

Может показаться, что компонент с `defaultProps` имеет некоторые необходимые свойства, которые на самом деле таковыми не являются.

### Постановка проблемы

Вот что вы хотите сделать:

```ts
interface IProps {
    name: string;
}
const defaultProps = {
    age: 25,
};
const GreetComponent = ({
    name,
    age,
}: IProps & typeof defaultProps) => (
    <div>{`Hello, my name is ${name}, ${age}`}</div>
);
GreetComponent.defaultProps = defaultProps;

const TestComponent = (
    props: React.ComponentProps<typeof GreetComponent>
) => {
    return <h1 />;
};

// Свойство 'age' отсутствует в типе '{ name: string; }',
// но обязательно в типе '{ age: number; }'.
const el = <TestComponent name="foo" />;
```

### Решение

Определите утилиту, которая применяет `React.JSX.LibraryManagedAttributes`:

```ts
type ComponentProps<T> = T extends
    | React.ComponentType<infer P>
    | React.Component<infer P>
    ? React.JSX.LibraryManagedAttributes<T, P>
    : never;

const TestComponent = (
    props: ComponentProps<typeof GreetComponent>
) => {
    return <h1 />;
};

// Нет ошибок
const el = <TestComponent name="foo" />;
```

[_Посмотреть в TS Playground_](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAKjgQwM5wEoFNkGN4BmUEIcARFDvmQNwBQdMAnmFnAMImQB2W3MABWJhUAHgAqAPjgBeOOLhYAHjD4ATdNjwwAdJ3ARe-cSyyjg3AlihwB0gD6Yqu-Tz4xzl67cl04cAH44ACkAZQANHQAZYAAjKGQoJgBZZG5kAHMsNQBBGBgoOIBXVTFxABofPzgALjheADdrejoLVSgCPDYASSEIETgAb2r0kCw61AKLDPoAXzpcQ0m4NSxOooAbQWF0OWH-TPG4ACYAVnK6WfpF7mWAcUosGFdDd1k4AApB+uQxysO4LM6r0dnAAGRwZisCAEFZrZCbbb9VAASlk0g+1VEamADUkgwABgAJLAbDYQSogJg-MZwYDoAAkg1GWFmlSZh1mBNmogA9Di8XQUfQHlgni8jLpVustn0BnJpQjZTsWrzeXANsh2gwbstxFhJhK3nIPmAdnUjfw5WIoVgYXBReKuK9+JI0TJpPs4JQYEUoNw4KIABYARjgvN8VwYargADkIIooMQoAslvBSe8JAbns7JTSsDIyAQIBAyOHJDQgA)

## Обсуждения и знания

!!!note "Почему `React.FC` ломает `defaultProps`?"

    Вы можете посмотреть обсуждения здесь:

    -   <https://medium.com/@martin_hotell/10-typescript-pro-tips-patterns-with-or-without-react-5799488d6680>
    -   <https://github.com/DefinitelyTyped/DefinitelyTyped/issues/30695>
    -   <https://github.com/typescript-cheatsheets/react/issues/87>

    Это только текущее состояние и может быть исправлено в будущем.

???note "TypeScript 2.9 и более ранние версии"

    Для TypeScript 2.9 и более ранних версий есть несколько способов сделать это, но это лучший совет, который мы видели:

    ```ts
    type Props = Required<typeof MyComponent.defaultProps> & {
    	/* additional props here */
    };

    export class MyComponent extends React.Component<Props> {
    	static defaultProps = {
    		foo: 'foo',
    	};
    }
    ```

    Наша прежняя рекомендация использовала функцию `Partial type` в TypeScript, которая означает, что текущий интерфейс будет выполнять частичную версию обернутого интерфейса. Таким образом, мы можем расширять defaultProps без каких-либо изменений в типах!

    ```ts
    interface IMyComponentProps {
    	firstProp?: string;
    	secondProp: IPerson[];
    }

    export class MyComponent extends React.Component<
    	IMyComponentProps
    > {
    	public static defaultProps: Partial<
    		IMyComponentProps
    	> = {
    		firstProp: 'default',
    	};
    }
    ```

    Проблема с этим подходом заключается в том, что он вызывает сложные проблемы с выводом типов при работе с `React.JSX.LibraryManagedAttributes`. По сути, это заставляет компилятор думать, что при создании JSX-выражения с этим компонентом все его реквизиты являются необязательными.

    [См. комментарии @ferdaber здесь](https://github.com/typescript-cheatsheets/react/issues/57) и [здесь](https://github.com/typescript-cheatsheets/react/issues/61).

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/default_props></small>
