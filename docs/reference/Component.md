# Component

!!!warning ""

    Мы рекомендуем определять компоненты как функции, а не как классы.

`Component` - это базовый класс для компонентов React, определенных как [классы JavaScript.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) Классовые компоненты все еще поддерживаются React, но мы не рекомендуем использовать их в новом коде.

<!-- 0001.part.md -->

```js
class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0002.part.md -->

## Описание

### `Component`

Чтобы определить компонент React как класс, расширьте встроенный класс `Component` и определите метод `render`:

<!-- 0003.part.md -->

```js
import { Component } from 'react';

class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0004.part.md -->

Только метод `render` является обязательным, остальные методы необязательны.

### `context`

[Контекст](../learn/passing-data-deeply-with-context.md) компонента класса доступен как `this.context`. Он доступен только если вы укажете _какой_ контекст вы хотите получить, используя `static contextType` (современный) или `static contextTypes` (устаревший).

Компонент класса может одновременно считывать только один контекст.

<!-- 0005.part.md -->

```js
class Button extends Component {
    static contextType = ThemeContext;

    render() {
        const theme = this.context;
        const className = 'button-' + theme;
        return (
            <button className={className}>
                {this.props.children}
            </button>
        );
    }
}
```

<!-- 0006.part.md -->

!!!note ""

    Чтение `this.context` в компонентах класса эквивалентно [`useContext`](useContext.md) в компонентах функции.

### `props`

Реквизиты, передаваемые компоненту класса, доступны как `this.props`.

<!-- 0007.part.md -->

```js
class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}

<Greeting name="Taylor" />;
```

<!-- 0008.part.md -->

!!note ""

    Чтение `this.props` в компонентах классов эквивалентно [объявлению props](../learn/passing-props-to-a-component.md) в компонентах функций.

### `refs`

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React. [Вместо него используйте `createRef`](createRef.md).

Позволяет получить доступ к [legacy string refs](https://reactjs.org/docs/refs-and-the-dom.html#legacy-api-string-refs) для этого компонента.

### `state`

Состояние компонента класса доступно как `this.state`. Поле `state` должно быть объектом. Не изменяйте состояние напрямую. Если вы хотите изменить состояние, вызовите `setState` с новым состоянием.

<!-- 0009.part.md -->

```js
class Counter extends Component {
    state = {
        age: 42,
    };

    handleAgeChange = () => {
        this.setState({
            age: this.state.age + 1,
        });
    };

    render() {
        return (
            <>
                <button onClick={this.handleAgeChange}>
                    Increment age
                </button>
                <p>You are {this.state.age}.</p>
            </>
        );
    }
}
```

<!-- 0010.part.md -->

!!!note ""

    Определение `state` в компонентах класса эквивалентно вызову [`useState`](useState.md) в компонентах функции.

### `constructor(props)`

Конструктор [constructor](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/constructor) запускается перед тем, как компонент вашего класса _монтируется_ (добавляется на экран). Как правило, конструктор используется в React только для двух целей. Он позволяет вам объявить состояние и [привязать](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_objects/Function/bind) методы вашего класса к экземпляру класса:

<!-- 0011.part.md -->

```js
class Counter extends Component {
    constructor(props) {
        super(props);
        this.state = { counter: 0 };
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        // ...
    }
}
```

<!-- 0012.part.md -->

Если вы используете современный синтаксис JavaScript, конструкторы нужны редко. Вместо этого вы можете переписать приведенный выше код, используя синтаксис [public class field syntax](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Public_class_fields), который поддерживается как современными браузерами, так и инструментами типа [Babel:](https://babeljs.io/).

<!-- 0013.part.md -->

```js
class Counter extends Component {
    state = { counter: 0 };

    handleClick = () => {
        // ...
    };
}
```

<!-- 0014.part.md -->

Конструктор не должен содержать никаких побочных эффектов или подписок.

#### Параметры

-   `props`: Начальные параметры компонента.

#### Возвращает

`constructor` не должен ничего возвращать.

#### Ограничения

-   Не запускайте в конструкторе никаких побочных эффектов или подписок. Вместо этого используйте `componentDidMount`.

-   Внутри конструктора необходимо вызывать `super(props)` перед любым другим оператором. Если этого не сделать, то `this.props` будет `неопределенным` во время работы конструктора, что может запутать и привести к ошибкам.

-   Конструктор - это единственное место, где вы можете присвоить `this.state` напрямую. Во всех остальных методах вместо этого нужно использовать `this.setState()`. Не вызывайте `setState` в конструкторе.

-   При использовании [server rendering](server.md), конструктор будет выполняться и на сервере, а за ним последует метод `render`. Однако методы жизненного цикла, такие как `componentDidMount` или `componentWillUnmount`, не будут выполняться на сервере.

-   Когда включен [Строгий режим](StrictMode.md), React будет вызывать `constructor` дважды в процессе разработки, а затем выбрасывать один из экземпляров. Это поможет вам заметить случайные побочные эффекты, которые необходимо вынести за пределы `конструктора`.

!!!note ""

    Точного эквивалента `constructor` в функциональных компонентах не существует. Чтобы объявить состояние в функциональном компоненте, вызовите [`useState`](useState.md). Чтобы избежать пересчета начального состояния, [передайте функцию `useState`](useState.md).

### `componentDidCatch(error, info)`

Если вы определите `componentDidCatch`, React будет вызывать его, когда какой-либо дочерний компонент (включая удаленные дочерние компоненты) выкинет ошибку во время рендеринга. Это позволит вам регистрировать эту ошибку на службе сообщений об ошибках в продакшене.

Обычно этот метод используется вместе с `static getDerivedStateFromError`, который позволяет обновить состояние в ответ на ошибку и вывести сообщение об ошибке пользователю. Компонент с этими методами называется _граница ошибки_.

#### Параметры

-   `error`: Ошибка, которая была выдана. На практике это обычно будет экземпляр [`Error`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Error), но это не гарантировано, поскольку JavaScript позволяет [`throw`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/throw) любое значение, включая строки или даже `null`.

-   `info`: Объект, содержащий дополнительную информацию об ошибке. Его поле `componentStack` содержит трассировку стека с компонентом, который бросил, а также имена и местоположение источников всех его родительских компонентов. В продакшене имена компонентов будут минифицированы. Если вы настроите prod

<!-- 0015.part.md -->

#### Возврат

`componentDidCatch` не должен ничего возвращать.

#### Ограничения

-   В прошлом было принято вызывать `setState` внутри `componentDidCatch`, чтобы обновить пользовательский интерфейс и отобразить сообщение об ошибке. Это устарело в пользу определения `static getDerivedStateFromError`.

-   Производственные и девелоперские сборки React немного отличаются в том, как `componentDidCatch` обрабатывает ошибки. В разработке ошибки будут всплывать в `window`, что означает, что любые `window.onerror` или `window.addEventListener('error', callback)` будут перехватывать ошибки, которые были пойманы `componentDidCatch`. В производстве, вместо этого, ошибки не будут всплывать, что означает, что любой обработчик ошибок предка будет получать только ошибки, явно не пойманные `componentDidCatch`.

!!note ""

Прямого эквивалента для `componentDidCatch` в компонентах функций пока не существует. Если вы хотите избежать создания компонентов классов, напишите один компонент `ErrorBoundary`, как описано выше, и используйте его во всем приложении. В качестве альтернативы вы можете использовать пакет [`react-error-boundary`](https://github.com/bvaughn/react-error-boundary), который сделает это за вас.

### `componentDidMount()`

Если вы определите метод `componentDidMount`, React будет вызывать его, когда ваш компонент будет добавлен _(смонтирован)_ на экран. Это обычное место для начала получения данных, установки подписок или манипулирования узлами DOM.

Если вы реализуете `componentDidMount`, вам обычно необходимо реализовать другие методы жизненного цикла, чтобы избежать ошибок. Например, если `componentDidMount` считывает некоторые состояния или реквизиты, вам также необходимо реализовать `componentDidUpdate` для обработки их изменений и `componentWillUnmount` для очистки того, что делал `componentDidMount`.

<!-- 0016.part.md -->

```js
class ChatRoom extends Component {
    state = {
        serverUrl: 'https://localhost:1234',
    };

    componentDidMount() {
        this.setupConnection();
    }

    componentDidUpdate(prevProps, prevState) {
        if (
            this.props.roomId !== prevProps.roomId ||
            this.state.serverUrl !== prevState.serverUrl
        ) {
            this.destroyConnection();
            this.setupConnection();
        }
    }

    componentWillUnmount() {
        this.destroyConnection();
    }

    // ...
}
```

#### Параметры

`componentDidMount` не принимает никаких параметров.

#### Returns

`componentDidMount` не должен ничего возвращать.

#### Caveats

-   Когда включен [Строгий режим](StrictMode.md), при разработке React будет вызывать `componentDidMount`, затем сразу же вызывать `componentWillUnmount`, и затем снова вызывать `componentDidMount`. Это поможет вам заметить, если вы забыли реализовать `componentWillUnmount` или если его логика не полностью "отражает" то, что делает `componentDidMount`.

-   Хотя вы можете вызвать `setState` непосредственно в `componentDidMount`, лучше избегать этого, когда это возможно. Это вызовет дополнительный рендеринг, но он произойдет до того, как браузер обновит экран. Это гарантирует, что даже если `render` будет вызван дважды в этом случае, пользователь не увидит промежуточного состояния. Используйте этот паттерн с осторожностью, поскольку он часто вызывает проблемы с производительностью. В большинстве случаев вы можете назначить начальное состояние в `constructor`. Тем не менее, это может быть необходимо в таких случаях, как модалы и всплывающие подсказки, когда вам нужно измерить узел DOM перед отрисовкой чего-то, что зависит от его размера или положения.

!!!note ""

    Для многих случаев использования определение `componentDidMount`, `componentDidUpdate` и `componentWillUnmount` вместе в компонентах класса эквивалентно вызову [`useEffect`](useEffect.md) в компонентах функций. В редких случаях, когда важно, чтобы код выполнялся перед закраской браузера, более подходящим вариантом является [`useLayoutEffect`](useLayoutEffect.md).

### `componentDidUpdate(prevProps, prevState, snapshot?)`

Если вы определите метод `componentDidUpdate`, React вызовет его сразу после того, как ваш компонент будет перерендерирован с обновленными реквизитами или состоянием. Этот метод не вызывается для первоначального рендеринга.

Вы можете использовать его для манипуляций с DOM после обновления. Это также обычное место для выполнения сетевых запросов, если вы сравниваете текущие реквизиты с предыдущими (например, сетевой запрос может не потребоваться, если реквизиты не изменились). Обычно вы используете его вместе с `componentDidMount` и `componentWillUnmount`:

<!-- 0018.part.md -->

```js
class ChatRoom extends Component {
    state = {
        serverUrl: 'https://localhost:1234',
    };

    componentDidMount() {
        this.setupConnection();
    }

    componentDidUpdate(prevProps, prevState) {
        if (
            this.props.roomId !== prevProps.roomId ||
            this.state.serverUrl !== prevState.serverUrl
        ) {
            this.destroyConnection();
            this.setupConnection();
        }
    }

    componentWillUnmount() {
        this.destroyConnection();
    }

    // ...
}
```

#### Параметры

-   `prevProps`: Реквизиты до обновления. Сравните `prevProps` с `this.props`, чтобы определить, что изменилось.
-   `prevState`: Состояние перед обновлением. Сравните `prevState` с `this.state`, чтобы определить, что изменилось.
-   `snapshot`: Если вы реализовали `getSnapshotBeforeUpdate`, `snapshot` будет содержать значение, которое вы вернули из этого метода. В противном случае оно будет `undefined`.

#### Возвращает

`componentDidUpdate` не должен ничего возвращать.

#### Предупреждения

-   `componentDidUpdate` не будет вызван, если `shouldComponentUpdate` определен и возвращает `false`.

-   Логика внутри `componentDidUpdate` обычно должна быть обернута в условия, сравнивающие `this.props` с `prevProps`, а `this.state` с `prevState`. В противном случае есть риск создания бесконечных циклов.

-   Хотя вы можете вызвать `setState` непосредственно в `componentDidUpdate`, лучше избегать этого, когда это возможно. Это вызовет дополнительный рендеринг, но он произойдет до того, как браузер обновит экран. Это гарантирует, что хотя `render` в этом случае будет вызван дважды, пользователь не увидит промежуточного состояния. Этот паттерн часто вызывает проблемы с производительностью, но он может быть необходим в редких случаях, таких как модалы и всплывающие подсказки, когда вам нужно измерить узел DOM перед рендерингом чего-то, что зависит от его размера или положения.

!!!note ""

    Для многих случаев использования определение `componentDidMount`, `componentDidUpdate` и `componentWillUnmount` вместе в компонентах класса эквивалентно вызову [`useEffect`](useEffect.md) в компонентах функций. В редких случаях, когда важно, чтобы код выполнялся перед закраской браузера, более подходящим вариантом является [`useLayoutEffect`](useLayoutEffect.md).

### `componentWillMount()`

!!!danger "Устарело"

    Этот API был переименован из `componentWillMount` в `UNSAFE_componentWillMount` Старое название было устаревшим. В будущей основной версии React будет работать только новое название.

    Запустите [`rename-unsafe-lifecycles` codemod](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) для автоматического обновления ваших компонентов.

### `componentWillReceiveProps(nextProps)`

!!!danger "Устарело"

    Этот API был переименован из `componentWillReceiveProps` в `UNSAFE_componentWillReceiveProps` Старое название было устаревшим. В будущей основной версии React будет работать только новое название.

    Запустите кодмод [`rename-unsafe-lifecycles`](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) для автоматического обновления.

### `componentWillUpdate(nextProps, nextState)`

!!!danger "Устарело"

    Этот API был переименован из `componentWillUpdate` в `UNSAFE_componentWillUpdate` Старое название было устаревшим. В будущей основной версии React будет работать только новое название.

    Запустите [`rename-unsafe-lifecycles` codemod](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) для автоматического обновления ваших компонентов.

---

### `componentWillUnmount()`

Если вы определите метод `componentWillUnmount`, React вызовет его перед тем, как ваш компонент будет удален _(размонтирован)_ с экрана. Это обычное место для отмены получения данных или удаления подписок.

Логика внутри `componentWillUnmount` должна "отражать" логику внутри `componentDidMount`. Например, если `componentDidMount` устанавливает подписку, `componentWillUnmount` должен очистить эту подписку. Если логика очистки в вашем `componentWillUnmount` считывает некоторые реквизиты или состояние, вам обычно также потребуется реализовать `componentDidUpdate` для очистки ресурсов (таких как подписки), соответствующих старым реквизитам и состоянию.

<!-- 0021.part.md -->

```js
class ChatRoom extends Component {
    state = {
        serverUrl: 'https://localhost:1234',
    };

    componentDidMount() {
        this.setupConnection();
    }

    componentDidUpdate(prevProps, prevState) {
        if (
            this.props.roomId !== prevProps.roomId ||
            this.state.serverUrl !== prevState.serverUrl
        ) {
            this.destroyConnection();
            this.setupConnection();
        }
    }

    componentWillUnmount() {
        this.destroyConnection();
    }

    // ...
}
```

#### Параметры

`componentWillUnmount` не принимает никаких параметров.

#### Returns

`componentWillUnmount` не должен ничего возвращать.

#### Caveats

-   Когда включен [Строгий режим](StrictMode.md), при разработке React будет вызывать `componentDidMount`, затем сразу же вызывать `componentWillUnmount`, а затем снова вызывать `componentDidMount`. Это поможет вам заметить, если вы забыли реализовать `componentWillUnmount` или если его логика не полностью "отражает" то, что делает `componentDidMount`.

!!!note ""

    Для многих случаев использования определение `componentDidMount`, `componentDidUpdate` и `componentWillUnmount` вместе в компонентах класса эквивалентно вызову [`useEffect`](useEffect.md) в компонентах функций. В редких случаях, когда важно, чтобы код выполнялся перед закраской браузера, более подходящим вариантом является [`useLayoutEffect`](useLayoutEffect.md).

### `forceUpdate(callback?)`

Принуждает компонент к повторному рендерингу.

Обычно в этом нет необходимости. Если метод `render` вашего компонента читает только из `this.props`, `this.state` или `this.context`, то он будет перерендерирован автоматически, когда вы вызовете `setState` внутри вашего компонента или одного из его родителей. Однако если метод `render` вашего компонента считывает данные непосредственно из внешнего источника данных, вам необходимо указать React обновлять пользовательский интерфейс при изменении источника данных. Именно это и позволяет сделать `forceUpdate`.

Старайтесь избегать всех случаев использования `forceUpdate` и читайте только из `this.props` и `this.state` в `render`.

#### Параметры

-   **опционально** `callback` Если указано, React вызовет указанный вами `callback` после фиксации обновления.

#### Возвраты

`forceUpdate` ничего не возвращает.

#### Предостережения

-   Если вы вызовете `forceUpdate`, React выполнит повторный рендеринг без вызова `shouldComponentUpdate`.

!!!note ""

    Чтение внешнего источника данных и принуждение компонентов класса к повторному рендерингу в ответ на его изменения с помощью `forceUpdate` было заменено на [`useSyncExternalStore`](useSyncExternalStore.md) в компонентах функций.

### `getChildContext()`

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React. [Вместо него используйте `Context.Provider`](createContext.md).

Позволяет указать значения для [унаследованного контекста](https://reactjs.org/docs/legacy-context.html), предоставляемого этим компонентом.

### `getSnapshotBeforeUpdate(prevProps, prevState)`

Если вы реализуете `getSnapshotBeforeUpdate`, React будет вызывать его непосредственно перед тем, как React обновит DOM. Это позволит вашему компоненту захватить некоторую информацию из DOM (например, позицию прокрутки) до того, как она будет потенциально изменена. Любое значение, возвращаемое этим методом жизненного цикла, будет передано в качестве параметра в `componentDidUpdate`.

<!-- 0023.part.md -->

Например, вы можете использовать его в пользовательском интерфейсе, таком как поток чата, который должен сохранять позицию прокрутки во время обновления:

<!-- 0024.part.md -->

```js
class ScrollingList extends React.Component {
    constructor(props) {
        super(props);
        this.listRef = React.createRef();
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // Are we adding new items to the list?
        // Capture the scroll position so we can adjust scroll later.
        if (
            prevProps.list.length < this.props.list.length
        ) {
            const list = this.listRef.current;
            return list.scrollHeight - list.scrollTop;
        }
        return null;
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // If we have a snapshot value, we've just added new items.
        // Adjust scroll so these new items don't push the old ones out of view.
        // (snapshot here is the value returned from getSnapshotBeforeUpdate)
        if (snapshot !== null) {
            const list = this.listRef.current;
            list.scrollTop = list.scrollHeight - snapshot;
        }
    }

    render() {
        return (
            <div ref={this.listRef}>
                {/* ...contents... */}
            </div>
        );
    }
}
```

<!-- 0025.part.md -->

В приведенном выше примере важно прочитать свойство `scrollHeight` непосредственно в `getSnapshotBeforeUpdate`. Небезопасно читать его в `render`, `UNSAFE_componentWillReceiveProps` или `UNSAFE_componentWillUpdate`, поскольку существует потенциальный разрыв во времени между вызовом этих методов и обновлением DOM в React.

#### Параметры

-   `prevProps`: Реквизиты до обновления. Сравните `prevProps` с `this.props`, чтобы определить, что изменилось.

-   `prevState`: Состояние перед обновлением. Сравните `prevState` с `this.state`, чтобы определить, что изменилось.

#### Возвраты

Вы должны вернуть значение снапшота любого типа, который вы хотите, или `null`. Возвращенное значение будет передано в качестве третьего аргумента в `componentDidUpdate`.

#### Caveats

-   `getSnapshotBeforeUpdate` не будет вызван, если определено `shouldComponentUpdate` и возвращает `false`.

!!!note ""

    На данный момент не существует эквивалента `getSnapshotBeforeUpdate` для компонентов функций. Это очень редкий случай использования, но если у вас возникнет такая необходимость, то пока вам придется написать компонент класса.

### `render()`

Метод `render` является единственным обязательным методом в компоненте класса.

Метод `render` должен определять, что вы хотите видеть на экране, например:

<!-- 0026.part.md -->

```js
import { Component } from 'react';

class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0027.part.md -->

React может вызвать `render` в любой момент, поэтому не стоит предполагать, что он выполняется в определенное время. Обычно метод `render` должен возвращать часть [JSX](../learn/writing-markup-with-jsx.md), но поддерживаются и некоторые другие типы возврата (например, строки). Для вычисления возвращаемого JSX метод `render` может читать `this.props`, `this.state` и `this.context`.

Вы должны написать метод `render` как чистую функцию, что означает, что он должен возвращать один и тот же результат, если реквизиты, состояние и контекст одинаковы. Он также не должен содержать побочных эффектов (таких как установка подписок) или взаимодействовать с API браузера. Побочные эффекты должны происходить либо в обработчиках событий, либо в методах типа `componentDidMount`.

#### Параметры

-   `prevProps`: Реквизиты до обновления. Сравните `prevProps` с `this.props`, чтобы определить, что изменилось.

-   `prevState`: Состояние перед обновлением. Сравните `prevState` с `this.state`, чтобы определить, что изменилось.

#### Возвраты

`render` может возвращать любой допустимый узел React. Сюда входят такие элементы React, как `<div />`, строки, числа, [порталы](createPortal.md), пустые узлы (`null`, `undefined`, `true` и `false`) и массивы узлов React.

#### Caveats

-   `render` должна быть написана как чистая функция props, state и context. Она не должна иметь побочных эффектов.

-   `render` не будет вызван, если определено `shouldComponentUpdate` и возвращает `false`.

-   Когда включен [Strict Mode](StrictMode.md), React будет вызывать `render` дважды в процессе разработки, а затем отбрасывать один из результатов. Это поможет вам заметить случайные побочные эффекты, которые необходимо убрать из метода `render`.

-   Между вызовом `render` и последующим вызовом `componentDidMount` или `componentDidUpdate` нет соответствия один к одному. Некоторые результаты вызова `render` могут быть отброшены React, когда это будет полезно.

### `setState(nextState, callback?)`

Вызовите `setState` для обновления состояния вашего компонента React.

<!-- 0028.part.md -->

```js
class Form extends Component {
    state = {
        name: 'Taylor',
    };

    handleNameChange = (e) => {
        const newName = e.target.value;
        this.setState({
            name: newName,
        });
    };

    render() {
        return (
            <>
                <input
                    value={this.state.name}
                    onChange={this.handleNameChange}
                />
                <p>Hello, {this.state.name}.</p>
            </>
        );
    }
}
```

<!-- 0029.part.md -->

`setState` регистрирует изменения в состоянии компонента. Он сообщает React, что этот компонент и его дочерние элементы должны быть перерисованы с новым состоянием. Это основной способ обновления пользовательского интерфейса в ответ на взаимодействие.

!!!warning ""

    Вызов `setState` **не** изменяет текущее состояние в уже выполняющемся коде:

    <!-- 0030.part.md -->

    ```js
    function handleClick() {
    	console.log(this.state.name); // "Taylor"
    	this.setState({
    		name: 'Robin',
    	});
    	console.log(this.state.name); // Still "Taylor"!
    }
    ```

    Это влияет только на то, что `this.state` будет возвращать, начиная со _следующего_ рендера.

Вы также можете передать функцию в `setState`. Это позволит вам обновить состояние на основе предыдущего состояния:

<!-- 0032.part.md -->

```js
handleIncreaseAge = () => {
    this.setState((prevState) => {
        return {
            age: prevState.age + 1,
        };
    });
};
```

<!-- 0033.part.md -->

Это не обязательно, но удобно, если вы хотите обновить состояние несколько раз во время одного и того же события.

#### Параметры

-   `nextState`: Либо объект, либо функция.
    -   Если вы передадите объект в качестве `nextState`, он будет неглубоко объединен с `this.state`.
    -   Если вы передадите функцию в качестве `nextState`, она будет рассматриваться как _функция обновления_. Она должна быть чистой, принимать в качестве аргументов состояние ожидания и реквизит, и возвращать объект, который будет неглубоко объединен в `this.state`. React поместит вашу функцию обновления в очередь и перерендерит ваш компонент. Во время следующего рендеринга React вычислит следующее состояние, применив все стоящие в очереди функции обновления к предыдущему состоянию.
-   **опциональный** `callback`: Если указано, React вызовет указанный вами `callback` после фиксации обновления.

#### Возвраты

`setState` ничего не возвращает.

#### Предостережения

-   Рассматривайте `setState` как _запрос_, а не как немедленную команду на обновление компонента. Когда несколько компонентов обновляют свое состояние в ответ на событие, React будет собирать их обновления и перерисовывать их вместе за один проход в конце события. В редких случаях, когда вам нужно заставить определенное обновление состояния применяться синхронно, вы можете обернуть его в [`flushSync`,](flushSync.md), но это может снизить производительность.

-   `setState` не обновляет `this.state` немедленно. Это делает чтение `this.state` сразу после вызова `setState` потенциально опасным. Вместо этого используйте `componentDidUpdate` или аргумент setState `callback`, любой из которых гарантированно сработает после применения обновления. Если вам нужно установить состояние на основе предыдущего состояния, вы можете передать функцию в `nextState`, как описано выше.

!!!note ""

    Вызов `setState` в компонентах классов аналогичен вызову функции [`set`](useState.md) в компонентах функций.

### `shouldComponentUpdate(nextProps, nextState, nextContext)`

Если вы определите `shouldComponentUpdate`, React будет вызывать его, чтобы определить, можно ли пропустить повторный рендеринг.

Если вы уверены, что хотите написать его вручную, вы можете сравнить `this.props` с `nextProps` и `this.state` с `nextState` и вернуть `false`, чтобы сообщить React, что обновление можно пропустить.

<!-- 0034.part.md -->

```js
class Rectangle extends Component {
    state = {
        isHovered: false,
    };

    shouldComponentUpdate(nextProps, nextState) {
        if (
            nextProps.position.x ===
                this.props.position.x &&
            nextProps.position.y ===
                this.props.position.y &&
            nextProps.size.width ===
                this.props.size.width &&
            nextProps.size.height ===
                this.props.size.height &&
            nextState.isHovered === this.state.isHovered
        ) {
            // Nothing has changed, so a re-render is unnecessary
            return false;
        }
        return true;
    }
    // ...
}
```

<!-- 0035.part.md -->

React вызывает `shouldComponentUpdate` перед рендерингом при получении новых реквизитов или состояния. По умолчанию установлено значение `true`. Этот метод не вызывается для начального рендеринга или при использовании `forceUpdate`.

#### Параметры

-   `nextProps`: Следующий реквизит, с которым компонент будет рендериться. Сравните `nextProps` с `this.props`, чтобы определить, что изменилось.
-   `nextState`: Следующее состояние, в котором компонент будет отображаться. Сравните `nextState` с `this.state`, чтобы определить, что изменилось.
-   `nextContext`: Следующий контекст, с которым компонент собирается выполнить рендеринг. Сравните `nextContext` с `this.context`, чтобы определить, что изменилось. Доступно только если вы указали `static contextType` (современный) или `static contextTypes` (унаследованный).

#### Returns

Возвращает `true`, если вы хотите, чтобы компонент был перерендерен. Это поведение по умолчанию.

Верните `false`, чтобы сообщить React, что повторный рендеринг можно пропустить.

#### Caveats

-   Этот метод _только_ существует как оптимизация производительности. Если ваш компонент ломается без него, сначала исправьте это.

-   Рассмотрите возможность использования [`PureComponent`](PureComponent.md) вместо написания `shouldComponentUpdate` вручную. `PureComponent` неглубоко сравнивает реквизиты и состояние и уменьшает вероятность того, что вы пропустите необходимое обновление.

-   Мы не рекомендуем выполнять глубокие проверки равенства или использовать `JSON.stringify` в `shouldComponentUpdate`. Это делает производительность непредсказуемой и зависимой от структуры данных каждого реквизита и состояния. В лучшем случае вы рискуете внести многосекундные задержки в ваше приложение, а в худшем - завалить его.

-   Возврат `false` не предотвращает повторный рендеринг дочерних компонентов при изменении _их_ состояния.

-   Возврат `false` не _гарантирует_, что компонент не будет повторно отображаться. React будет использовать возвращаемое значение как подсказку, но он все равно может решить перерисовать ваш компонент, если это имеет смысл сделать по другим причинам.

!!!note ""

    Оптимизация компонентов классов с помощью `shouldComponentUpdate` аналогична оптимизации компонентов функций с помощью [`memo`.](memo.md) Компоненты функций также предлагают более детальную оптимизацию с помощью [`useMemo`.](useMemo.md).

### `UNSAFE_componentWillMount()`

Если вы определите `UNSAFE_componentWillMount`, React вызовет его сразу после `constructor`. Он существует только по историческим причинам и не должен использоваться в любом новом коде. Вместо этого используйте одну из альтернатив:

-   Для инициализации состояния объявите `state` как поле класса или установите `this.state` внутри `constructor`.
-   Если вам нужно запустить побочный эффект или установить подписку, перенесите эту логику в `componentDidMount`.

<!-- 0036.part.md -->

#### Параметры

`UNSAFE_componentWillMount` не принимает никаких параметров.

#### Возвращает

`UNSAFE_componentWillMount` не должен ничего возвращать.

#### Caveats

-   `UNSAFE_componentWillMount` не будет вызван, если компонент реализует `static getDerivedStateFromProps` или `getSnapshotBeforeUpdate`.

-   Несмотря на свое название, `UNSAFE_componentWillMount` не гарантирует, что компонент _будет смонтирован_, если ваше приложение использует современные функции React, такие как [`Suspense`.](Suspense.md) Если попытка рендеринга приостановлена (например, потому что код для какого-то дочернего компонента еще не загружен), React отбросит дерево процесса и попытается построить компонент с нуля во время следующей попытки. Вот почему этот метод является "небезопасным". Код, который полагается на монтирование (например, добавление подписки), должен идти в `componentDidMount`.

-   `UNSAFE_componentWillMount` - это единственный метод жизненного цикла, который выполняется во время [рендеринга сервера.](server.md) Для всех практических целей он идентичен `constructor`, поэтому для такого типа логики следует использовать `constructor`.

!!!note ""

    Вызов `setState` внутри `UNSAFE_componentWillMount` в компоненте класса для инициализации состояния эквивалентен передаче этого состояния в качестве начального состояния в [`useState`](useState.md) в компоненте функции.

### `UNSAFE_componentWillReceiveProps(nextProps, nextContext)`

Если вы определите `UNSAFE_componentWillReceiveProps`, React будет вызывать его, когда компонент получит новые реквизиты. Оно существует только по историческим причинам и не должно использоваться в новом коде. Вместо этого используйте одну из альтернатив:

-   Если вам нужно **запустить побочный эффект** (например, получить данные, запустить анимацию или переинициализировать подписку) в ответ на изменение реквизита, перенесите эту логику в `componentDidUpdate`.
-   Если вам нужно **избежать повторного вычисления некоторых данных только при изменении реквизита,** используйте вместо этого [memoization helper](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#what-about-memoization).
-   Если вам нужно **"сбросить" некоторое состояние при изменении реквизита,** рассмотрите возможность сделать компонент [полностью управляемым](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#recommendation-fully-controlled-component) или [полностью неуправляемым с ключом](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#recommendation-fully-uncontrolled-component-with-a-key).
-   Если вам нужно "подправить" некоторое состояние при изменении реквизита, проверьте, можете ли вы вычислить всю необходимую информацию только из реквизитов во время рендеринга. Если нет, используйте вместо этого статический `getDerivedStateFromProps`.

<!-- 0037.part.md -->

[См. примеры перехода от небезопасных жизненных циклов.](https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#updating-state-based-on-props)

#### Параметры

-   `nextProps`: Следующий реквизит, который компонент собирается получить от своего родительского компонента. Сравните `nextProps` с `this.props`, чтобы определить, что изменилось.
-   `nextContext`: Следующий реквизит, который компонент собирается получить от ближайшего провайдера. Сравните `nextContext` с `this.context`, чтобы определить, что изменилось. Доступно только если вы указали `static contextType` (современный) или `static contextTypes` (унаследованный).

#### Возвращает

`UNSAFE_componentWillReceiveProps` не должен ничего возвращать.

#### Caveats

-   `UNSAFE_componentWillReceiveProps` не будет вызван, если компонент реализует `static getDerivedStateFromProps` или `getSnapshotBeforeUpdate`.

-   Несмотря на свое название, `UNSAFE_componentWillReceiveProps` не гарантирует, что компонент получит эти props, если ваше приложение использует современные функции React, такие как [`Suspense`.](Suspense.md) Если попытка рендеринга приостановлена (например, потому что код для какого-то дочернего компонента еще не загружен), React отбросит текущее дерево и попытается построить компонент с нуля во время следующей попытки. К моменту следующей попытки рендеринга реквизит может быть другим. Вот почему этот метод является "небезопасным". Код, который должен выполняться только для зафиксированных обновлений (например, сброс подписки), следует поместить в `componentDidUpdate`.

-   `UNSAFE_componentWillReceiveProps` не означает, что компонент получил _другие_ реквизиты, чем в прошлый раз. Вам нужно самостоятельно сравнить `nextProps` и `this.props`, чтобы проверить, изменилось ли что-то.

-   React не вызывает `UNSAFE_componentWillReceiveProps` с начальными реквизитами во время монтирования. Он вызывает этот метод только в том случае, если некоторые реквизиты компонента будут обновлены. Например, вызов `setState` обычно не вызывает `UNSAFE_componentWillReceiveProps` внутри того же компонента.

!!!note ""

    Вызов `setState` внутри `UNSAFE_componentWillReceiveProps` в компоненте класса для "корректировки" состояния эквивалентен [вызову функции `set` из `useState` во время рендеринга](useState.md) в компоненте функции.

---

### `UNSAFE_componentWillUpdate(nextProps, nextState)`

Если вы определите `UNSAFE_componentWillUpdate`, React будет вызывать его перед рендерингом с новыми props или state. Он существует только по историческим причинам и не должен использоваться в новом коде. Вместо этого используйте одну из альтернатив:

-   Если вам нужно запустить побочный эффект (например, получить данные, запустить анимацию или повторно инициализировать подписку) в ответ на изменение реквизита или состояния, перенесите эту логику в `componentDidUpdate`.

-   Если вам нужно прочитать какую-то информацию из DOM (например, сохранить текущую позицию прокрутки), чтобы позже использовать ее в `componentDidUpdate`, прочитайте ее внутри `getSnapshotBeforeUpdate`.

[См. примеры перехода от небезопасных жизненных циклов](https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#examples).

#### Параметры

-   `nextProps`: Следующий реквизит, с которым компонент собирается выполнить рендеринг. Сравните `nextProps` с `this.props`, чтобы определить, что изменилось.
-   `nextState`: Следующее состояние, в котором компонент будет отображаться. Сравните `nextState` с `this.state`, чтобы определить, что изменилось.

#### Возвращает

`UNSAFE_componentWillUpdate` не должен ничего возвращать.

#### Предостережения

-   `UNSAFE_componentWillUpdate` не будет вызван, если `shouldComponentUpdate` определен и возвращает `false`.

-   `UNSAFE_componentWillUpdate` не будет вызван, если компонент реализует `static getDerivedStateFromProps` или `getSnapshotBeforeUpdate`.

-   Не поддерживается вызов `setState` (или любого метода, который приводит к вызову `setState`, например, диспетчеризация действия Redux) во время `componentWillUpdate`.

-   Несмотря на свое название, `UNSAFE_componentWillUpdate` не гарантирует, что компонент _обновится_, если ваше приложение использует современные функции React, такие как [`Suspense`](Suspense.md). Если попытка рендеринга приостановлена (например, потому что код для какого-то дочернего компонента еще не загружен), React отбросит дерево процесса и попытается построить компонент с нуля во время следующей попытки. К моменту следующей попытки рендеринга реквизиты и состояние могут быть другими. Вот почему этот метод является "небезопасным". Код, который должен выполняться только для зафиксированных обновлений (например, сброс подписки), следует поместить в `componentDidUpdate`.

-   `UNSAFE_componentWillUpdate` не означает, что компонент получил _другой_ реквизит или состояние, чем в прошлый раз. Вам нужно самостоятельно сравнить `nextProps` с `this.props` и `nextState` с `this.state`, чтобы проверить, изменилось ли что-то.

-   React не вызывает `UNSAFE_componentWillUpdate` с начальными props и state во время монтирования.

!!!note ""

    Не существует прямого эквивалента `UNSAFE_componentWillUpdate` в функциональных компонентах.

### `static childContextTypes`

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React. Вместо него используйте `статический contextType`.

Позволяет указать, какой [legacy context](https://reactjs.org/docs/legacy-context.html) предоставляется этим компонентом.

### `static contextTypes`

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React. Вместо него используйте `статический contextType`.

Позволяет указать, какой [legacy context](https://reactjs.org/docs/legacy-context.html) потребляется этим компонентом.

### `static contextType`

Если вы хотите читать `this.context` из компонента вашего класса, вы должны указать, какой контекст он должен читать. Контекст, который вы указываете в качестве `static contextType`, должен быть значением, ранее созданным с помощью [`createContext`](createContext.md).

<!-- 0040.part.md -->

```js
class Button extends Component {
    static contextType = ThemeContext;

    render() {
        const theme = this.context;
        const className = 'button-' + theme;
        return (
            <button className={className}>
                {this.props.children}
            </button>
        );
    }
}
```

<!-- 0041.part.md -->

!!!note ""

    Чтение `this.context` в компонентах класса эквивалентно [`useContext`](useContext.md) в компонентах функции.

### `static defaultProps`

Вы можете определить `static defaultProps`, чтобы установить реквизиты по умолчанию для класса. Они будут использоваться для `неопределенных` и отсутствующих реквизитов, но не для реквизитов `null`.

Например, вот как определить, что реквизит `color` должен по умолчанию иметь значение `'blue'`:

<!-- 0042.part.md -->

```js
class Button extends Component {
    static defaultProps = {
        color: 'blue',
    };

    render() {
        return (
            <button className={this.props.color}>
                click me
            </button>
        );
    }
}
```

<!-- 0043.part.md -->

Если параметр `color` не указан или является `неопределенным`, он будет установлен по умолчанию в `синий`:

<!-- 0044.part.md -->

```js
<>
    {/* this.props.color is "blue" */}
    <Button />

    {/* this.props.color is "blue" */}
    <Button color={undefined} />

    {/* this.props.color is null */}
    <Button color={null} />

    {/* this.props.color is "red" */}
    <Button color="red" />
</>
```

<!-- 0045.part.md -->

!!!note ""

    Определение `defaultProps` в компонентах классов аналогично использованию [значений по умолчанию](../learn/passing-props-to-a-component.md) в компонентах функций.

### `static propTypes`

Вы можете определить `static propTypes` вместе с библиотекой [`prop-types`](https://www.npmjs.com/package/prop-types), чтобы объявить типы реквизитов, принимаемых вашим компонентом. Эти типы будут проверяться во время рендеринга и только в процессе разработки.

<!-- 0046.part.md -->

```js
import PropTypes from 'prop-types';

class Greeting extends React.Component {
    static propTypes = {
        name: PropTypes.string,
    };

    render() {
        return <h1>Hello, {this.props.name}</h1>;
    }
}
```

<!-- 0047.part.md -->

!!!note ""

    Мы рекомендуем использовать [TypeScript](https://www.typescriptlang.org/) вместо проверки типов реквизитов во время выполнения.

### `static getDerivedStateFromError(error)`

Если вы определите `static getDerivedStateFromError`, React будет вызывать его, когда дочерний компонент (включая удаленные дочерние компоненты) бросит ошибку во время рендеринга. Это позволит вам отобразить сообщение об ошибке вместо того, чтобы очищать пользовательский интерфейс.

Обычно этот метод используется вместе с `componentDidCatch`, который позволяет отправить отчет об ошибке в какой-либо аналитический сервис. Компонент с этими методами называется _граница ошибки_.

#### Параметры

-   `error`: Ошибка, которая была выдана. На практике это обычно будет экземпляр [`Error`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Error), но это не гарантировано, поскольку JavaScript позволяет [`throw`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/throw) любое значение, включая строки или даже `null`.

#### Возвращает

`static getDerivedStateFromError` должен возвращать состояние, указывающее компоненту на отображение сообщения об ошибке.

#### Caveats

-   Функция `static getDerivedStateFromError` должна быть чистой функцией. Если вы хотите выполнить побочный эффект (например, вызвать аналитический сервис), вам необходимо также реализовать `componentDidCatch`.

!!!note ""

    Прямого эквивалента для `static getDerivedStateFromError` в компонентах функций пока не существует. Если вы хотите избежать создания компонентов классов, напишите один компонент `ErrorBoundary`, как описано выше, и используйте его во всем приложении. В качестве альтернативы используйте пакет [`react-error-boundary`](https://github.com/bvaughn/react-error-boundary), который делает это.

### `static getDerivedStateFromProps(props, state)`

Если вы определите `static getDerivedStateFromProps`, React будет вызывать его непосредственно перед вызовом `render`, как при первоначальном монтаже, так и при последующих обновлениях. Он должен вернуть объект для обновления состояния, или `null`, чтобы ничего не обновлять.

Этот метод существует для [редких случаев использования](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#when-to-use-derived-state), когда состояние зависит от изменений в реквизитах с течением времени. Например, этот компонент `Form` сбрасывает состояние `email` при изменении реквизита `userID`:

<!-- 0048.part.md -->

```js
class Form extends Component {
    state = {
        email: this.props.defaultEmail,
        prevUserID: this.props.userID,
    };

    static getDerivedStateFromProps(props, state) {
        // Any time the current user changes,
        // Reset any parts of state that are tied to that user.
        // In this simple example, that's just the email.
        if (props.userID !== state.prevUserID) {
            return {
                prevUserID: props.userID,
                email: props.defaultEmail,
            };
        }
        return null;
    }

    // ...
}
```

<!-- 0049.part.md -->

Обратите внимание, что этот паттерн требует, чтобы вы хранили предыдущее значение реквизита (например, `userID`) в состоянии (например, `prevUserID`).

!!!warning ""

    Выведение состояния приводит к многословному коду и делает ваши компоненты сложными для осмысления. [Убедитесь, что вы знакомы с более простыми альтернативами:](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html)

    -   Если вам нужно **выполнить побочный эффект** (например, выборку данных или анимацию) в ответ на изменение реквизита, используйте метод `componentDidUpdate`.
    -   Если вы хотите **пересчитывать некоторые данные только при изменении реквизита,** [используйте вместо этого помощник мемоизации](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#what-about-memoization).
    -   Если вы хотите **"сбросить" некоторое состояние при изменении реквизита,** рассмотрите возможность сделать компонент [полностью управляемым](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#recommendation-fully-controlled-component) или [полностью неуправляемым с ключом](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#recommendation-fully-uncontrolled-component-with-a-key).

#### Параметры

-   `props`: Следующий реквизит, с которым компонент собирается выполнить рендеринг.
-   `state`: Следующее состояние, с которым компонент будет рендериться.

#### Возвращает

`static getDerivedStateFromProps` возвращает объект для обновления состояния, или `null` для отсутствия обновления.

#### Caveats

-   Этот метод срабатывает при _каждом_ рендере, независимо от причины. Это отличается от `UNSAFE_componentWillReceiveProps`, который срабатывает только тогда, когда родитель вызывает повторный рендеринг, а не в результате локального `setState`.

-   Этот метод не имеет доступа к экземпляру компонента. Если вы хотите, вы можете повторно использовать некоторый код между `static getDerivedStateFromProps` и другими методами класса, извлекая чистые функции реквизитов и состояния компонента за пределы определения класса.

!!!note ""

    Реализация `static getDerivedStateFromProps` в компоненте класса эквивалентна [вызову функции `set` из `useState` во время рендеринга](useState.md) в компоненте функции.

## Использование

### Определение компонента класса

Чтобы определить компонент React как класс, расширьте встроенный класс `Component` и определите метод `render`:

<!-- 0050.part.md -->

```js
import { Component } from 'react';

class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

<!-- 0051.part.md -->

React будет вызывать ваш метод `render` всякий раз, когда ему нужно будет определить, что отобразить на экране. Обычно вы будете возвращать из него некий [JSX](../learn/writing-markup-with-jsx.md). Ваш метод `render` должен быть [чистой функцией](https://ru.wikipedia.org/wiki/%D0%A7%D0%B8%D1%81%D1%82%D0%BE%D1%82%D0%B0_%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8): он должен только вычислять JSX.

Аналогично [функциональным компонентам,](../learn/your-first-component.md) компонент класса может [получать информацию по props](../learn/your-first-component.md) от своего родительского компонента. Однако синтаксис для чтения реквизитов отличается. Например, если родительский компонент отображает `<Greeting name="Taylor" />`, то вы можете прочитать реквизит `name` из `this.props`, как `this.props.name`:

<!-- 0052.part.md -->

```js
import { Component } from 'react';

class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}

export default function App() {
    return (
        <>
            <Greeting name="Sara" />
            <Greeting name="Cahal" />
            <Greeting name="Edite" />
        </>
    );
}
```

<!-- 0053.part.md -->

Обратите внимание, что хуки (функции, начинающиеся с `use`, например [`useState`](useState.md)) не поддерживаются внутри компонентов классов.

!!!warning ""

    Мы рекомендуем определять компоненты как функции, а не как классы.

### Добавление состояния в компонент класса

Чтобы добавить [state](../learn/state-a-components-memory.md) в класс, присвойте объект свойству `state`. Чтобы обновить состояние, вызовите `this.setState`.

<!-- 0054.part.md -->

```js
import { Component } from 'react';

export default class Counter extends Component {
    state = {
        name: 'Taylor',
        age: 42,
    };

    handleNameChange = (e) => {
        this.setState({
            name: e.target.value,
        });
    };

    handleAgeChange = () => {
        this.setState({
            age: this.state.age + 1,
        });
    };

    render() {
        return (
            <>
                <input
                    value={this.state.name}
                    onChange={this.handleNameChange}
                />
                <button onClick={this.handleAgeChange}>
                    Increment age
                </button>
                <p>
                    Hello, {this.state.name}. You are{' '}
                    {this.state.age}.
                </p>
            </>
        );
    }
}
```

---

### Добавление методов жизненного цикла в компонент класса

Есть несколько специальных методов, которые вы можете определить для своего класса.

Если вы определите метод `componentDidMount`, React будет вызывать его, когда ваш компонент будет добавлен _(смонтирован)_ на экран. React вызовет метод `componentDidUpdate` после того, как ваш компонент изменит рендеринг из-за изменения реквизитов или состояния. React вызовет `componentWillUnmount` после того, как ваш компонент будет удален _(размонтирован)_ с экрана.

Если вы реализуете `componentDidMount`, вам обычно нужно реализовать все три жизненных цикла, чтобы избежать ошибок. Например, если `componentDidMount` считывает некоторые состояния или реквизиты, вы также должны реализовать `componentDidUpdate` для обработки их изменений, и `componentWillUnmount` для очистки всего, что делал `componentDidMount`.

Например, этот компонент `ChatRoom` поддерживает соединение чата, синхронизированное с реквизитами и состоянием:

=== "App.js"

    <div markdown style="max-height: 400px; overflow-y: auto;">

    ```js
    import { useState } from 'react';
    import ChatRoom from './ChatRoom.js';

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Close chat' : 'Open chat'}
    			</button>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

    </div>

=== "ChatRoom.js"

    <div markdown style="max-height: 400px; overflow-y: auto;">

    ```js
    import { Component } from 'react';
    import { createConnection } from './chat.js';

    export default class ChatRoom extends Component {
    	state = {
    		serverUrl: 'https://localhost:1234',
    	};

    	componentDidMount() {
    		this.setupConnection();
    	}

    	componentDidUpdate(prevProps, prevState) {
    		if (
    			this.props.roomId !== prevProps.roomId ||
    			this.state.serverUrl !== prevState.serverUrl
    		) {
    			this.destroyConnection();
    			this.setupConnection();
    		}
    	}

    	componentWillUnmount() {
    		this.destroyConnection();
    	}

    	setupConnection() {
    		this.connection = createConnection(
    			this.state.serverUrl,
    			this.props.roomId
    		);
    		this.connection.connect();
    	}

    	destroyConnection() {
    		this.connection.disconnect();
    		this.connection = null;
    	}

    	render() {
    		return (
    			<>
    				<label>
    					Server URL:{' '}
    					<input
    						value={this.state.serverUrl}
    						onChange={(e) => {
    							this.setState({
    								serverUrl: e.target.value,
    							});
    						}}
    					/>
    				</label>
    				<h1>
    					Welcome to the {this.props.roomId} room!
    				</h1>
    			</>
    		);
    	}
    }
    ```

    </div>

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log(
    				'✅ Connecting to "' +
    					roomId +
    					'" room at ' +
    					serverUrl +
    					'...'
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    		},
    	};
    }
    ```

Обратите внимание, что при разработке, когда включен [Strict Mode](StrictMode.md), React вызовет `componentDidMount`, тут же вызовет `componentWillUnmount`, а затем снова вызовет `componentDidMount`. Это поможет вам заметить, если вы забыли реализовать `componentWillUnmount` или если его логика не полностью "зеркальна" тому, что делает `componentDidMount`.

### Ловля ошибок рендеринга с границей ошибки

По умолчанию, если ваше приложение выдаст ошибку во время рендеринга, React удалит свой UI с экрана. Чтобы предотвратить это, вы можете обернуть часть вашего пользовательского интерфейса в _границу ошибки_. Граница ошибки - это специальный компонент, который позволяет отображать некоторый резервный пользовательский интерфейс вместо той части, которая потерпела крах - например, сообщение об ошибке.

Чтобы реализовать компонент границы ошибки, вам нужно предоставить `static getDerivedStateFromError`, который позволяет обновлять состояние в ответ на ошибку и выводить пользователю сообщение об ошибке. Вы также можете реализовать `componentDidCatch` для добавления дополнительной логики, например, для регистрации ошибки в аналитическом сервисе.

<!-- 0066.part.md -->

```js
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    componentDidCatch(error, info) {
        // Example "componentStack":
        //   in ComponentThatThrows (created by App)
        //   in ErrorBoundary (created by App)
        //   in div (created by App)
        //   in App
        logErrorToMyService(error, info.componentStack);
    }

    render() {
        if (this.state.hasError) {
            // You can render any custom fallback UI
            return this.props.fallback;
        }

        return this.props.children;
    }
}
```

<!-- 0067.part.md -->

Затем вы можете обернуть им часть дерева компонентов:

<!-- 0068.part.md -->

```js
<ErrorBoundary fallback={<p>Something went wrong</p>}>
    <Profile />
</ErrorBoundary>
```

<!-- 0069.part.md -->

Если `Profile` или его дочерний компонент выбросит ошибку, `ErrorBoundary` "поймает" эту ошибку, отобразит резервный пользовательский интерфейс с сообщением об ошибке, которое вы предоставили, и отправит производственный отчет об ошибке в вашу службу сообщений об ошибках.

Вам не нужно оборачивать каждый компонент в отдельную границу ошибки. Когда вы думаете о [гранулярности границ ошибок](https://aweary.dev/fault-tolerance-react/), подумайте, где имеет смысл отображать сообщение об ошибке. Например, в приложении для обмена сообщениями имеет смысл поместить границу ошибки вокруг списка бесед. Также имеет смысл поместить ее вокруг каждого отдельного сообщения. Однако не имеет смысла размещать границу вокруг каждого аватара.

!!!note ""

    В настоящее время не существует способа написать границу ошибки как компонент функции. Однако вам не обязательно писать класс границы ошибки самостоятельно. Например, вы можете использовать [`react-error-boundary`](https://github.com/bvaughn/react-error-boundary).

## Альтернативы

### Перенос простого компонента из класса в функцию

Обычно вместо этого вы [определяете компоненты как функции](../learn/your-first-component.md).

Например, предположим, что вы преобразовываете компонент класса `Greeting` в функцию:

<!-- 0070.part.md -->

```js
import { Component } from 'react';

class Greeting extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}

export default function App() {
    return (
        <>
            <Greeting name="Sara" />
            <Greeting name="Cahal" />
            <Greeting name="Edite" />
        </>
    );
}
```

<!-- 0071.part.md -->

Определите функцию под названием `Greeting`. Именно сюда вы переместите тело вашей функции `render`.

<!-- 0072.part.md -->

```js
function Greeting() {
    // ... move the code from the render method here ...
}
```

<!-- 0073.part.md -->

Вместо `this.props.name` определите реквизит `name` [используя синтаксис деструктуризации](../learn/passing-props-to-a-component.md) и читайте его напрямую:

<!-- 0074.part.md -->

```js
function Greeting({ name }) {
    return <h1>Hello, {name}!</h1>;
}
```

<!-- 0075.part.md -->

Вот полный пример:

<!-- 0076.part.md -->

```js
function Greeting({ name }) {
    return <h1>Hello, {name}!</h1>;
}

export default function App() {
    return (
        <>
            <Greeting name="Sara" />
            <Greeting name="Cahal" />
            <Greeting name="Edite" />
        </>
    );
}
```

<!-- 0077.part.md -->

---

### Перенос компонента с состоянием из класса в функцию

Предположим, вы преобразовываете компонент класса `Counter` в функцию:

<!-- 0078.part.md -->

```js
import { Component } from 'react';

export default class Counter extends Component {
    state = {
        name: 'Taylor',
        age: 42,
    };

    handleNameChange = (e) => {
        this.setState({
            name: e.target.value,
        });
    };

    handleAgeChange = (e) => {
        this.setState({
            age: this.state.age + 1,
        });
    };

    render() {
        return (
            <>
                <input
                    value={this.state.name}
                    onChange={this.handleNameChange}
                />
                <button onClick={this.handleAgeChange}>
                    Increment age
                </button>
                <p>
                    Hello, {this.state.name}. You are{' '}
                    {this.state.age}.
                </p>
            </>
        );
    }
}
```

<!-- 0081.part.md -->

Начните с объявления функции с необходимыми [переменными состояния:](useState.md)

<!-- 0082.part.md -->

```js
import { useState } from 'react';

function Counter() {
    const [name, setName] = useState('Taylor');
    const [age, setAge] = useState(42);
    // ...
}
```

<!-- 0083.part.md -->

Затем преобразуйте обработчики событий:

<!-- 0084.part.md -->

```js
function Counter() {
    const [name, setName] = useState('Taylor');
    const [age, setAge] = useState(42);

    function handleNameChange(e) {
        setName(e.target.value);
    }

    function handleAgeChange() {
        setAge(age + 1);
    }
    // ...
}
```

<!-- 0085.part.md -->

Наконец, замените все ссылки, начинающиеся с `this`, на переменные и функции, которые вы определили в своем компоненте. Например, замените `this.state.age` на `age`, а `this.handleNameChange` на `handleNameChange`.

Вот полностью преобразованный компонент:

<!-- 0086.part.md -->

```js
import { useState } from 'react';

export default function Counter() {
    const [name, setName] = useState('Taylor');
    const [age, setAge] = useState(42);

    function handleNameChange(e) {
        setName(e.target.value);
    }

    function handleAgeChange() {
        setAge(age + 1);
    }

    return (
        <>
            <input
                value={name}
                onChange={handleNameChange}
            />
            <button onClick={handleAgeChange}>
                Increment age
            </button>
            <p>
                Hello, {name}. You are {age}.
            </p>
        </>
    );
}
```

### Перенос компонента с методами жизненного цикла из класса в функцию

Предположим, вы преобразовываете компонент класса `ChatRoom` с методами жизненного цикла в функцию:

=== "App.js"

    ```js
    import { useState } from 'react';
    import ChatRoom from './ChatRoom.js';

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Close chat' : 'Open chat'}
    			</button>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

=== "ChatRoom.js"

    ```js
    import { Component } from 'react';
    import { createConnection } from './chat.js';

    export default class ChatRoom extends Component {
    	state = {
    		serverUrl: 'https://localhost:1234',
    	};

    	componentDidMount() {
    		this.setupConnection();
    	}

    	componentDidUpdate(prevProps, prevState) {
    		if (
    			this.props.roomId !== prevProps.roomId ||
    			this.state.serverUrl !== prevState.serverUrl
    		) {
    			this.destroyConnection();
    			this.setupConnection();
    		}
    	}

    	componentWillUnmount() {
    		this.destroyConnection();
    	}

    	setupConnection() {
    		this.connection = createConnection(
    			this.state.serverUrl,
    			this.props.roomId
    		);
    		this.connection.connect();
    	}

    	destroyConnection() {
    		this.connection.disconnect();
    		this.connection = null;
    	}

    	render() {
    		return (
    			<>
    				<label>
    					Server URL:{' '}
    					<input
    						value={this.state.serverUrl}
    						onChange={(e) => {
    							this.setState({
    								serverUrl: e.target.value,
    							});
    						}}
    					/>
    				</label>
    				<h1>
    					Welcome to the {this.props.roomId} room!
    				</h1>
    			</>
    		);
    	}
    }
    ```

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log(
    				'✅ Connecting to "' +
    					roomId +
    					'" room at ' +
    					serverUrl +
    					'...'
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    		},
    	};
    }
    ```

<!-- 0097.part.md -->

Сначала убедитесь, что ваш `componentWillUnmount` делает противоположное `componentDidMount`. В приведенном выше примере это так: он разрывает соединение, которое устанавливает `componentDidMount`. Если такая логика отсутствует, сначала добавьте ее.

Далее проверьте, что ваш метод `componentDidUpdate` обрабатывает изменения всех реквизитов и состояний, которые вы используете в `componentDidMount`. В приведенном выше примере `componentDidMount` вызывает `setupConnection`, который считывает `this.state.serverUrl` и `this.props.roomId`. Именно поэтому `componentDidUpdate` проверяет, изменились ли `this.state.serverUrl` и `this.props.roomId`, и сбрасывает соединение, если изменились. Если логика вашего `componentDidUpdate` отсутствует или не обрабатывает изменения всех соответствующих реквизитов и состояния, сначала исправьте это.

В приведенном выше примере логика внутри методов жизненного цикла соединяет компонент с системой вне React (сервером чата). Чтобы подключить компонент к внешней системе, [опишите эту логику как один Эффект:](useEffect.md)

<!-- 0098.part.md -->

```js
import { useState, useEffect } from 'react';

function ChatRoom({ roomId }) {
    const [serverUrl, setServerUrl] = useState(
        'https://localhost:1234'
    );

    useEffect(() => {
        const connection = createConnection(
            serverUrl,
            roomId
        );
        connection.connect();
        return () => {
            connection.disconnect();
        };
    }, [serverUrl, roomId]);

    // ...
}
```

<!-- 0099.part.md -->

Этот вызов [`useEffect`](useEffect.md) эквивалентен логике в методах жизненного цикла, описанных выше. Если ваши методы жизненного цикла делают несколько несвязанных вещей, [разделите их на несколько независимых Эффектов](../learn/removing-effect-dependencies.md). Вот полный пример, с которым вы можете поиграть:

=== "App.js"

    ```js
    import { useState } from 'react';
    import ChatRoom from './ChatRoom.js';

    export default function App() {
    	const [roomId, setRoomId] = useState('general');
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<label>
    				Choose the chat room:{' '}
    				<select
    					value={roomId}
    					onChange={(e) =>
    						setRoomId(e.target.value)
    					}
    				>
    					<option value="general">general</option>
    					<option value="travel">travel</option>
    					<option value="music">music</option>
    				</select>
    			</label>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Close chat' : 'Open chat'}
    			</button>
    			{show && <hr />}
    			{show && <ChatRoom roomId={roomId} />}
    		</>
    	);
    }
    ```

=== "ChatRoom.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    export default function ChatRoom({ roomId }) {
    	const [serverUrl, setServerUrl] = useState(
    		'https://localhost:1234'
    	);

    	useEffect(() => {
    		const connection = createConnection(
    			serverUrl,
    			roomId
    		);
    		connection.connect();
    		return () => {
    			connection.disconnect();
    		};
    	}, [roomId, serverUrl]);

    	return (
    		<>
    			<label>
    				Server URL:{' '}
    				<input
    					value={serverUrl}
    					onChange={(e) =>
    						setServerUrl(e.target.value)
    					}
    				/>
    			</label>
    			<h1>Welcome to the {roomId} room!</h1>
    		</>
    	);
    }
    ```

=== "chat.js"

    ```js
    export function createConnection(serverUrl, roomId) {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log(
    				'✅ Connecting to "' +
    					roomId +
    					'" room at ' +
    					serverUrl +
    					'...'
    			);
    		},
    		disconnect() {
    			console.log(
    				'❌ Disconnected from "' +
    					roomId +
    					'" room at ' +
    					serverUrl
    			);
    		},
    	};
    }
    ```

!!!note ""

    Если ваш компонент не синхронизируется с внешними системами, [возможно, вам не нужен Эффект](../learn/you-might-not-need-an-effect.md).

### Перенос компонента с контекстом из класса в функцию

В этом примере компоненты классов `Panel` и `Button` считывают [context](../learn/passing-data-deeply-with-context.md) из `this.context`:

<!-- 0108.part.md -->

```js
import { createContext, Component } from 'react';

const ThemeContext = createContext(null);

class Panel extends Component {
    static contextType = ThemeContext;

    render() {
        const theme = this.context;
        const className = 'panel-' + theme;
        return (
            <section className={className}>
                <h1>{this.props.title}</h1>
                {this.props.children}
            </section>
        );
    }
}

class Button extends Component {
    static contextType = ThemeContext;

    render() {
        const theme = this.context;
        const className = 'button-' + theme;
        return (
            <button className={className}>
                {this.props.children}
            </button>
        );
    }
}

function Form() {
    return (
        <Panel title="Welcome">
            <Button>Sign up</Button>
            <Button>Log in</Button>
        </Panel>
    );
}

export default function MyApp() {
    return (
        <ThemeContext.Provider value="dark">
            <Form />
        </ThemeContext.Provider>
    );
}
```

Когда вы преобразуете их в компоненты функций, замените вызовы `this.context` на [`useContext`](useContext.md):

<!-- 0112.part.md -->

```js
import { createContext, useContext } from 'react';

const ThemeContext = createContext(null);

function Panel({ title, children }) {
    const theme = useContext(ThemeContext);
    const className = 'panel-' + theme;
    return (
        <section className={className}>
            <h1>{title}</h1>
            {children}
        </section>
    );
}

function Button({ children }) {
    const theme = useContext(ThemeContext);
    const className = 'button-' + theme;
    return (
        <button className={className}>{children}</button>
    );
}

function Form() {
    return (
        <Panel title="Welcome">
            <Button>Sign up</Button>
            <Button>Log in</Button>
        </Panel>
    );
}

export default function MyApp() {
    return (
        <ThemeContext.Provider value="dark">
            <Form />
        </ThemeContext.Provider>
    );
}
```

## Ссылки

-   [https://react.dev/reference/react/Component](https://react.dev/reference/react/Component)
