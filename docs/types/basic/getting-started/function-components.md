---
description: Они могут быть написаны как обычные функции, которые принимают аргумент `props` и возвращают элемент JSX
---

# Функциональные компоненты

Они могут быть написаны как обычные функции, которые принимают аргумент `props` и возвращают элемент JSX.

```ts
// Объявление типа реквизитов - примеры см. в разделе
// "Типизация реквизитов компонентов".
type AppProps = {
    message: string;
}; /* используйте `interface` при экспорте,
      чтобы потребители могли расширять */

// Самый простой способ объявить функциональный компонент;
// тип возвращаемой функции определяется на основе предположений.
const App = ({ message }: AppProps) => <div>{message}</div>;

// вы можете выбрать аннотацию возвращаемого типа,
// чтобы при случайном возврате другого типа возникала ошибка
const App = ({ message }: AppProps): React.JSX.Element => (
    <div>{message}</div>
);

// Вы также можете вставить объявление типа; это избавляет от
// необходимости именовать типы реквизитов, но выглядит повторяющимся
const App = ({ message }: { message: string }) => (
    <div>{message}</div>
);

// В качестве альтернативы вы можете использовать React.FunctionComponent
// (или React.FC), если вам так больше нравится.
// В последних версиях React и TypeScript 5.1. это в основном
// стилистический выбор, в остальных случаях не рекомендуется.
const App: React.FunctionComponent<{ message: string }> = ({
    message,
}) => <div>{message}</div>;
```

!!!tip "Совет"

    Вы можете использовать [Расширение VS Code от Пола Шена](https://marketplace.visualstudio.com/items?itemName=paulshen.paul-typescript-toolkit) для автоматизации объявления деструктуры типа (включая [сочетание клавиш](https://twitter.com/_paulshen/status/1392915279466745857?s=20)).

!!!info "Почему `React.FC` не нужен? А как насчет `React.FunctionComponent`/`React.VoidFunctionComponent`?"

    Вы можете увидеть это во многих кодовых базах React+TypeScript:

    ```ts
    const App: React.FunctionComponent<{ message: string }> = ({
    	message,
    }) => <div>{message}</div>;
    ```

    Однако сегодня общее мнение таково, что `React.FunctionComponent` (или сокращенно `React.FC`) не нужен. Если вы все еще используете React 17 или TypeScript ниже версии 5.1, это даже [не рекомендуется](https://github.com/facebook/create-react-app/pull/8177). Это, конечно, мнение с нюансами, но если вы согласны и хотите убрать `React.FC` из своей кодовой базы, то можете воспользоваться [этим кодомодом jscodeshift](https://github.com/gndelia/codemod-replace-react-fc-typescript).

    Некоторые отличия от версии "нормальной функции":

    -   `React.FunctionComponent` явно указывает на возвращаемый тип, в то время как версия обычной функции - неявно (или нуждается в дополнительной аннотации).

    -   Она обеспечивает проверку типов и автозаполнение для статических свойств, таких как `displayName`, `propTypes` и `defaultProps`.

    	-   Обратите внимание, что есть некоторые известные проблемы с использованием `defaultProps` с `React.FunctionComponent`. Смотрите [этот выпуск для подробностей](https://github.com/typescript-cheatsheets/react/issues/87). Мы ведем отдельный раздел `defaultProps`, который вы также можете посмотреть.

    -   До [обновления типа React 18](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/56210), `React.FunctionComponent` предоставлял неявное определение `children` (см. ниже), что вызвало бурные споры и стало одной из причин [`React.FC` был удален из шаблона Create React App TypeScript](https://github.com/facebook/create-react-app/pull/8177).

    ```ts
    // before React 18 types
    const Title: React.FunctionComponent<{ title: string }> = ({
    	children,
    	title,
    }) => <div title={title}>{children}</div>;
    ```

    -   В будущем он может автоматически помечать реквизиты как `readonly`, хотя это спорный вопрос, если объект props деструктурирован в списке параметров.

    В большинстве случаев нет особой разницы, какой синтаксис используется, но вы можете предпочесть более явную природу `React.FunctionComponent`.

!!!note "(Устарело) Использование `React.VoidFunctionComponent` или `React.VFC` вместо этого"

    В [@types/react 16.9.48](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/46643) был добавлен тип `React.VoidFunctionComponent` или `React.VFC` для явного ввода `children`.
    Однако помните, что `React.VFC` и `React.VoidFunctionComponent` были [устаревшими в React 18](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/59882), поэтому это временное решение больше не нужно и не рекомендуется в React 18+.

    Вместо них используйте обычные функциональные компоненты или `React.FC`.

    ```ts
    type Props = { foo: string };

    // OK now, in future, error
    const FunctionComponent: React.FunctionComponent<Props> = ({
    	foo,
    	children,
    }: Props) => {
    	return (
    		<div>
    			{foo} {children}
    		</div>
    	); // OK
    };

    // Error now, in future, deprecated
    const VoidFunctionComponent: React.VoidFunctionComponent<Props> = ({
    	foo,
    	children,
    }) => {
    	return (
    		<div>
    			{foo}
    			{children}
    		</div>
    	);
    };
    ```

<small>:material-information-outline: Источник &mdash; [https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/function_components](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/function_components)</small>
