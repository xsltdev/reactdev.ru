# Устаревшие API React

Эти API экспортируются из пакета `react`, но их не рекомендуется использовать во вновь написанном коде. Предлагаемые альтернативы см. на отдельных страницах API по ссылкам.

## Устаревшие API

-   [`Children`](Children.md) позволяет манипулировать и преобразовывать JSX, полученный в качестве пропса `children`.
-   [`cloneElement`](cloneElement.md) позволяет создать элемент React, используя другой элемент в качестве отправной точки.
-   [`Component`](Component.md) позволяет определить компонент React как класс JavaScript.
-   [`createElement`](createElement.md) позволяет вам создать элемент React. Обычно вместо этого используется JSX.
-   [`createRef`](createRef.md) создает объект ref, который может содержать произвольное значение.
-   [`isValidElement`](isValidElement.md) проверяет, является ли значение элементом React. Обычно используется с [`cloneElement`.](cloneElement.md)
-   [`forwardRef`](forwardRef.md) позволяет компоненту открыть родительскому компоненту узел DOM через [реф](../../learn/manipulating-the-dom-with-refs.md).
-   [`PureComponent`](PureComponent.md) аналогичен [`Component`,](Component.md), но он пропускает повторные рендеринги с теми же пропсами.

## Удалённые API {#removed-apis}

Эти API удалены в React 19. Страницы ниже оставлены в справочнике как архив прежнего описания:

-   [`createFactory`](createFactory.md) позволял создать функцию, которая производит элементы React определенного типа. Используйте JSX.
-   Компоненты-классы: `static contextTypes`, `static childContextTypes` и `static getChildContext` заменены на [`createContext`](createContext.md).
-   Компоненты-классы: `static propTypes` заменены системой типов, например [TypeScript](https://www.typescriptlang.org/).
-   Компоненты-классы: `this.refs` заменены на [`createRef`](createRef.md).
