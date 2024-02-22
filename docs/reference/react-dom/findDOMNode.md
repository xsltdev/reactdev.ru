# findDOMNode

!!!danger "Устарело"

    Этот API будет удален в одной из будущих основных версий React.

`findDOMNode` находит узел DOM браузера для экземпляра React [class component](Component.md).

```js
const domNode = findDOMNode(componentInstance);
```

## Описание

### `findDOMNode(componentInstance)`

Вызывает `findDOMNode` для поиска узла DOM браузера для данного экземпляра React [class component](Component.md).

```js
import { findDOMNode } from 'react-dom';

const domNode = findDOMNode(componentInstance);
```

#### Параметры

-   `componentInstance`: Экземпляр подкласса [`Component`](Component.md). Например, `this` внутри компонента класса.

#### Возвращает

`findDOMNode` возвращает первый ближайший DOM-узел браузера в пределах заданного `componentInstance`. Если компонент отображается на `null`, или отображается `false`, `findDOMNode` возвращает `null`. Если компонент отображается в строку, `findDOMNode` возвращает текстовый узел DOM, содержащий это значение.

#### Ограничения

-   Компонент может возвращать массив или [фрагмент](Fragment.md) с несколькими дочерними элементами. В этом случае `findDOMNode` вернет узел DOM, соответствующий первому непустому дочернему компоненту.
-   `findDOMNode` работает только для смонтированных компонентов (то есть компонентов, которые были помещены в DOM). Если вы попытаетесь вызвать эту функцию на компоненте, который еще не смонтирован (например, вызвать `findDOMNode()` в `render()` на компоненте, который еще не создан), будет выброшено исключение.
-   `findDOMNode` возвращает результат только на момент вызова. Если дочерний компонент позже отобразит другой узел, у вас не будет возможности получить уведомление об этом изменении.
-   `findDOMNode` принимает экземпляр компонента класса, поэтому его нельзя использовать с компонентами функций.

## Использование

### Нахождение корневого DOM-узла компонента класса

Вызовите `findDOMNode` с экземпляром [class component](Component.md) (обычно `this`), чтобы найти DOM-узел, который он отобразил.

```js
class AutoselectingInput extends Component {
    componentDidMount() {
        const input = findDOMNode(this);
        input.select();
    }

    render() {
        return <input defaultValue="Hello" />;
    }
}
```

Здесь переменная `input` будет установлена на элемент DOM `<input>`. Это позволит вам сделать с ним что-нибудь. Например, при нажатии на кнопку "Показать пример" ниже монтируется ввод, [`input.select()`](https://developer.mozilla.org/docs/Web/API/HTMLInputElement/select) выделяет весь текст во вводе:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { Component } from 'react';
    import { findDOMNode } from 'react-dom';

    class AutoselectingInput extends Component {
    	componentDidMount() {
    		const input = findDOMNode(this);
    		input.select();
    	}

    	render() {
    		return <input defaultValue="Hello" />;
    	}
    }

    export default AutoselectingInput;
    ```

## Альтернативы

### Чтение собственного DOM-узла компонента из ссылки

Код, использующий `findDOMNode`, хрупок, поскольку связь между узлом JSX и кодом, манипулирующим соответствующим узлом DOM, не является явной. Например, попробуйте обернуть этот `input` в `div`:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { Component } from 'react';
    import { findDOMNode } from 'react-dom';

    class AutoselectingInput extends Component {
    	componentDidMount() {
    		const input = findDOMNode(this);
    		input.select();
    	}
    	render() {
    		return <input defaultValue="Hello" />;
    	}
    }

    export default AutoselectingInput;
    ```

Это нарушит код, поскольку теперь `findDOMNode(this)` находит DOM-узел `<div>`, но код ожидает DOM-узел `<input>`. Чтобы избежать подобных проблем, используйте [`createRef`](createRef.md) для управления конкретным узлом DOM.

В этом примере `findDOMNode` больше не используется. Вместо этого `inputRef = createRef(null)` определяется как поле экземпляра класса. Для чтения DOM-узла из него можно использовать `this.inputRef.current`. Чтобы присоединить его к JSX, вы рендерите `<input ref={this.inputRef} />`. Это соединяет код, использующий узел DOM, с его JSX:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { createRef, Component } from 'react';

    class AutoselectingInput extends Component {
    	inputRef = createRef(null);

    	componentDidMount() {
    		const input = this.inputRef.current;
    		input.select();
    	}

    	render() {
    		return (
    			<input
    				ref={this.inputRef}
    				defaultValue="Hello"
    			/>
    		);
    	}
    }

    export default AutoselectingInput;
    ```

В современном React без компонентов классов эквивалентный код будет вызывать [`useRef`](useRef.md) вместо этого:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { useRef, useEffect } from 'react';

    export default function AutoselectingInput() {
    	const inputRef = useRef(null);

    	useEffect(() => {
    		const input = inputRef.current;
    		input.select();
    	}, []);

    	return <input ref={inputRef} defaultValue="Hello" />;
    }
    ```

[Подробнее о манипулировании DOM с помощью ссылок](../../learn/manipulating-the-dom-with-refs.md)

### Чтение узла DOM дочернего компонента из переадресованной ссылки

В этом примере `findDOMNode(this)` находит узел DOM, принадлежащий другому компоненту. Компонент `AutoselectingInput` отображает `MyInput`, который является вашим собственным компонентом, отображающим браузерный `<input>`.

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { Component } from 'react';
    import { findDOMNode } from 'react-dom';
    import MyInput from './MyInput.js';

    class AutoselectingInput extends Component {
    	componentDidMount() {
    		const input = findDOMNode(this);
    		input.select();
    	}
    	render() {
    		return <MyInput />;
    	}
    }

    export default AutoselectingInput;
    ```

=== "MyInput.js"

    ```js
    export default function MyInput() {
    	return <input defaultValue="Hello" />;
    }
    ```

Обратите внимание, что вызов `findDOMNode(this)` внутри `AutoselectingInput` все еще дает вам DOM `input` - несмотря на то, что JSX для этого `input` скрыт внутри компонента `MyInput`. Это кажется удобным для приведенного выше примера, но это приводит к хрупкому коду. Представьте, что вы захотите отредактировать `MyInput` позже и добавить обертку `div` вокруг него. Это нарушит код `AutoselectingInput` (который ожидает найти `<input>`).

Чтобы заменить `findDOMNode` в этом примере, необходимо согласовать два компонента:

**1.** `AutoSelectingInput` должен объявить ref, как в предыдущем примере, и передать его в `<MyInput>`.

**2.** `MyInput` должен быть объявлен с [`forwardRef`](forwardRef.md), чтобы принять эту ссылку и передать ее узлу `<input>`.

Эта версия делает это, поэтому больше не требуется `findDOMNode`:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { createRef, Component } from 'react';
    import MyInput from './MyInput.js';

    class AutoselectingInput extends Component {
    	inputRef = createRef(null);

    	componentDidMount() {
    		const input = this.inputRef.current;
    		input.select();
    	}

    	render() {
    		return <MyInput ref={this.inputRef} />;
    	}
    }

    export default AutoselectingInput;
    ```

=== "MyInput.js"

    ```js
    import { forwardRef } from 'react';

    const MyInput = forwardRef(function MyInput(props, ref) {
    	return <input ref={ref} defaultValue="Hello" />;
    });

    export default MyInput;
    ```

Вот как выглядел бы этот код с компонентами функций вместо классов:

=== "App.js"

    ```js
    import { useState } from 'react';
    import AutoselectingInput from './AutoselectingInput.js';

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(true)}>
    				Show example
    			</button>
    			<hr />
    			{show && <AutoselectingInput />}
    		</>
    	);
    }
    ```

=== "AutoselectingInput.js"

    ```js
    import { useRef, useEffect } from 'react';
    import MyInput from './MyInput.js';

    export default function AutoselectingInput() {
    	const inputRef = useRef(null);

    	useEffect(() => {
    		const input = inputRef.current;
    		input.select();
    	}, []);

    	return <MyInput ref={inputRef} defaultValue="Hello" />;
    }
    ```

=== "MyInput.js"

    ```js
    import { forwardRef } from 'react';

    const MyInput = forwardRef(function MyInput(props, ref) {
    	return <input ref={ref} defaultValue="Hello" />;
    });

    export default MyInput;
    ```

### Добавление элемента-обертки `<div>`

Иногда компоненту необходимо знать положение и размер своих дочерних элементов. Это делает заманчивым найти дочерние элементы с помощью `findDOMNode(this)`, а затем использовать методы DOM, такие как [`getBoundingClientRect`](https://developer.mozilla.org/docs/Web/API/Element/getBoundingClientRect) для измерений.

В настоящее время не существует прямого эквивалента для этого случая использования, поэтому `findDOMNode` устарел, но еще не полностью удален из React. Тем временем, в качестве обходного пути вы можете попробовать отобразить узел-обертку `<div>` вокруг содержимого и получить ссылку на этот узел. Однако дополнительные обертки могут нарушить стилизацию.

```js
<div ref={someRef}>{children}</div>
```

Это также относится к фокусировке и прокрутке к произвольным дочерним элементам.
