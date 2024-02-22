---
status: deprecated
---

# PureComponent

!!!warning ""

    Мы рекомендуем определять компоненты как функции, а не как классы.

`PureComponent` похож на [`Component`](Component.md), но он пропускает повторные рендеринги для тех же пропсов и состояний. Компоненты классов по-прежнему поддерживаются React, но мы не рекомендуем использовать их в новом коде.

<!-- 0001.part.md -->

```js
class Greeting extends PureComponent {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0002.part.md -->

## Описание

### `PureComponent`

Чтобы пропустить повторное отображение компонента класса для тех же пропсов и состояния, расширьте `PureComponent` вместо [`Component`:](Component.md)

<!-- 0003.part.md -->

```js
import { PureComponent } from 'react';

class Greeting extends PureComponent {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0004.part.md -->

`PureComponent` является подклассом `Component` и поддерживает [все API `Component`](Component.md) Расширение `PureComponent` эквивалентно определению пользовательского метода [`shouldComponentUpdate`](Component.md), который неглубоко сравнивает пропсы и состояние.

## Использование

### Пропуск ненужных рендеров для компонентов классов

Обычно React перерисовывает компонент каждый раз, когда перерисовывается его родитель. В качестве оптимизации вы можете создать компонент, который React не будет перерисовывать при перерисовке его родителя до тех пор, пока его новые пропсы и состояние будут такими же, как старые пропсы и состояние. [Класс компонентов](Component.md) может выбрать такое поведение, расширяя `PureComponent`:

<!-- 0005.part.md -->

```js
class Greeting extends PureComponent {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0006.part.md -->

Компонент React всегда должен иметь [чистую логику рендеринга](../../learn/keeping-components-pure.md) Это означает, что он должен возвращать тот же результат, если его пропсы, состояние и контекст не изменились. Используя `PureComponent`, вы сообщаете React, что ваш компонент соответствует этому требованию, поэтому React не нужно выполнять повторный рендеринг, пока его пропсы и состояние не изменились. Однако ваш компонент все равно будет перерендерирован, если контекст, который он использует, изменится.

В этом примере обратите внимание, что компонент `Greeting` перерисовывается при изменении `name` (потому что это один из его пропсов), но не при изменении `address` (потому что он не передается `Greeting` в качестве пропса):

```js
import { PureComponent, useState } from 'react';

class Greeting extends PureComponent {
    render() {
        console.log(
            'Greeting was rendered at',
            new Date().toLocaleTimeString()
        );
        return (
            <h3>
                Hello{this.props.name && ', '}
                {this.props.name}!
            </h3>
        );
    }
}

export default function MyApp() {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    return (
        <>
            <label>
                Name{': '}
                <input
                    value={name}
                    onChange={(e) =>
                        setName(e.target.value)
                    }
                />
            </label>
            <label>
                Address{': '}
                <input
                    value={address}
                    onChange={(e) =>
                        setAddress(e.target.value)
                    }
                />
            </label>
            <Greeting name={name} />
        </>
    );
}
```

## Альтернативы

### Миграция с компонента класса `PureComponent` на функцию

Мы рекомендуем использовать компоненты функций вместо [компонентов классов](Component.md) в новом коде. Если у вас есть некоторые существующие компоненты классов, использующие `PureComponent`, вот как их можно преобразовать. Это оригинальный код:

<!-- 0011.part.md -->

```js
import { PureComponent, useState } from 'react';

class Greeting extends PureComponent {
    render() {
        console.log(
            'Greeting was rendered at',
            new Date().toLocaleTimeString()
        );
        return (
            <h3>
                Hello{this.props.name && ', '}
                {this.props.name}!
            </h3>
        );
    }
}

export default function MyApp() {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    return (
        <>
            <label>
                Name{': '}
                <input
                    value={name}
                    onChange={(e) =>
                        setName(e.target.value)
                    }
                />
            </label>
            <label>
                Address{': '}
                <input
                    value={address}
                    onChange={(e) =>
                        setAddress(e.target.value)
                    }
                />
            </label>
            <Greeting name={name} />
        </>
    );
}
```

Когда вы [преобразуете этот компонент из класса в функцию,](Component.md) оберните его в [`memo`:](memo.md)

<!-- 0015.part.md -->

```js
import { memo, useState } from 'react';

const Greeting = memo(function Greeting({ name }) {
    console.log(
        'Greeting was rendered at',
        new Date().toLocaleTimeString()
    );
    return (
        <h3>
            Hello{name && ', '}
            {name}!
        </h3>
    );
});

export default function MyApp() {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    return (
        <>
            <label>
                Name{': '}
                <input
                    value={name}
                    onChange={(e) =>
                        setName(e.target.value)
                    }
                />
            </label>
            <label>
                Address{': '}
                <input
                    value={address}
                    onChange={(e) =>
                        setAddress(e.target.value)
                    }
                />
            </label>
            <Greeting name={name} />
        </>
    );
}
```

В отличие от `PureComponent`, [`memo`](memo.md) не сравнивает новое и старое состояние. В функциональных компонентах вызов функции [`set`](useState.md) с тем же состоянием [уже предотвращает повторные рендеринги по умолчанию](memo.md), даже без `memo`.

<!-- 0019.part.md -->

## Ссылки

-   [https://react.dev/reference/react/PureComponent](https://react.dev/reference/react/PureComponent)
