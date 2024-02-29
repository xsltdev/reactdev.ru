---
description: use client необходим только в том случае, если вы используете React Server Components или создаете совместимую с ними библиотеку
status: experimental
---

# `'use client'`

!!!example "Canary"

    `'use client'` необходим только в том случае, если вы [используете React Server Components](../../learn/start-a-new-react-project.md#bleeding-edge-react-frameworks) или создаете совместимую с ними библиотеку.

<big>`'use client'` позволяет отметить, какой код выполняется на клиенте.</big>

## Справочник {#reference}

### `'use client'` {#use-client}

Добавьте `'use client'` в верхней части файла, чтобы отметить модуль и его транзитивные зависимости как клиентский код.

```js hl_lines="1"
'use client';

import { useState } from 'react';
import { formatDate } from './formatters';
import Button from './button';

export default function RichTextEditor({
    timestamp,
    text,
}) {
    const date = formatDate(timestamp);
    // ...
    const editButton = <Button />;
    // ...
}
```

Когда файл, помеченный директивой `'use client'`, импортируется из серверного компонента, [совместимые бандлеры](../../learn/start-a-new-react-project.md#bleeding-edge-react-frameworks) будут рассматривать импорт модуля как границу между кодом, выполняемым на сервере, и кодом, выполняемым на клиенте.

Будучи зависимостями `RichTextEditor`, `formatDate` и `Button` также будут оцениваться на клиенте, независимо от того, содержат ли их модули директиву `'use client'`. Обратите внимание, что один модуль может оцениваться на сервере при импорте из серверного кода и на клиенте при импорте из клиентского кода.

**Предостережения**

-   `'use client'` должно находиться в самом начале файла, выше любого импорта или другого кода (комментарии допускаются). Они должны быть написаны с одинарными или двойными кавычками, но не с обратными знаками.
-   Если модуль `'use client'` импортируется из другого клиентского модуля, директива не имеет силы.
-   Если модуль компонента содержит директиву `'use client'`, то любое использование этого компонента гарантированно является клиентским компонентом. Однако компонент может быть оценен на клиенте, даже если он не содержит директивы `'use client'`.
    -   Компонент считается клиентским, если он определен в модуле с директивой `'use client'` или является транзитивной зависимостью модуля, содержащего директиву `'use client'`. В противном случае он является серверным компонентом.
-   Код, помеченный для использования клиентом, не ограничивается компонентами. Весь код, входящий в поддерево модулей Client, отправляется клиенту и выполняется им.
-   Когда модуль, работающий с сервером, импортирует значения из модуля `'use client'`, эти значения должны быть либо компонентами React, либо поддерживаемыми сериализуемыми значениями prop для передачи в клиентский компонент. При любом другом варианте использования будет возникать исключение.

### Как `'use client'` помечает клиентский код {#how-use-client-marks-client-code}

В приложениях React компоненты часто разделяются на отдельные файлы, или [модули](../../learn/importing-and-exporting-components.md#exporting-and-importing-a-component).

Для приложений, использующих компоненты React Server Components, приложение по умолчанию рендерится на сервере. `'use client'` вводит границу сервер-клиент в [дерево зависимостей модулей](../../learn/understanding-your-ui-as-a-tree.md#the-module-dependency-tree), фактически создавая поддерево модулей Client.

Чтобы лучше проиллюстрировать это, рассмотрим следующее приложение React Server Components.

=== "App.js"

    ```js
    import FancyText from './FancyText';
    import InspirationGenerator from './InspirationGenerator';
    import Copyright from './Copyright';

    export default function App() {
    	return (
    		<>
    			<FancyText title text="Get Inspired App" />
    			<InspirationGenerator>
    				<Copyright year={2004} />
    			</InspirationGenerator>
    		</>
    	);
    }
    ```

=== "FancyText.js"

    ```js
    export default function FancyText({ title, text }) {
    	return title ? (
    		<h1 className="fancy title">{text}</h1>
    	) : (
    		<h3 className="fancy cursive">{text}</h3>
    	);
    }
    ```

=== "InspirationGenerator.js"

    ```js
    'use client';

    import { useState } from 'react';
    import inspirations from './inspirations';
    import FancyText from './FancyText';

    export default function InspirationGenerator({ children }) {
    	const [index, setIndex] = useState(0);
    	const quote = inspirations[index];
    	const next = () =>
    		setIndex((index + 1) % inspirations.length);

    	return (
    		<>
    			<p>Your inspirational quote is:</p>
    			<FancyText text={quote} />
    			<button onClick={next}>Inspire me again</button>
    			{children}
    		</>
    	);
    }
    ```

=== "Copyright.js"

    ```js
    export default function Copyright({ year }) {
    	return <p className="small">©️ {year}</p>;
    }
    ```

=== "inspirations.js"

    ```js
    export default [
    	'Don’t let yesterday take up too much of today.” — Will Rogers',
    	'Ambition is putting a ladder against the sky.',
    	"A joy that's shared is a joy made double.",
    ];
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/85dryt?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В дереве зависимостей модулей этого примера приложения директива `'use client'` в `InspirationGenerator.js` помечает этот модуль и все его транзитивные зависимости как модули Client. Поддерево, начинающееся с `InspirationGenerator.js`, теперь помечено как Client modules.

![Древовидный граф, верхний узел которого представляет модуль 'App.js'. У 'App.js' есть три дочерних модуля: 'Copyright.js', 'FancyText.js' и 'InspirationGenerator.js'. У 'InspirationGenerator.js' есть два дочерних узла: 'FancyText.js' и 'inspirations.js'. Узлы под и включая 'InspirationGenerator.js' имеют желтый цвет фона, чтобы обозначить, что этот подграф является клиентским из-за директивы 'use client' в 'InspirationGenerator.js'.](use_client_module_dependency.webp)

<small>_`'use client'` сегментирует дерево зависимостей модулей приложения React Server Components, помечая `InspirationGenerator.js` и все его зависимости как client-rendered._</small>

Во время рендеринга фреймворк отрендерит корневой компонент и продолжит движение по [дереву рендеринга](../../learn/understanding-your-ui-as-a-tree.md#the-render-tree), отказываясь от оценки любого кода, импортированного из кода, отмеченного клиентом.

Затем часть дерева рендеринга, отрендеренная сервером, отправляется клиенту. Клиент, загрузив свой клиентский код, завершает рендеринг оставшейся части дерева.

![Древовидный граф, в котором каждый узел представляет компонент, а его дочерние компоненты - дочерние компоненты. Узел верхнего уровня обозначен как 'App', и у него есть два дочерних компонента 'InspirationGenerator' и 'FancyText'. У 'InspirationGenerator' есть два дочерних компонента, 'FancyText' и 'Copyright'. И 'InspirationGenerator', и его дочерний компонент 'FancyText' помечены как клиентские.](use_client_render_tree.webp)

<small>_Дерево рендеринга для приложения React Server Components. `InspirationGenerator` и его дочерний компонент `FancyText` являются компонентами, экспортированными из клиентского кода и считаются клиентскими компонентами._</small>

Мы вводим следующие определения:

-   **Клиентские компоненты** - это компоненты в дереве рендеринга, которые отображаются на клиенте.
-   **Серверные компоненты** - это компоненты в дереве рендеринга, которые отображаются на сервере.

Работая с примером приложения, `App`, `FancyText` и `Copyright` рендерятся на сервере и считаются серверными компонентами. Поскольку `InspirationGenerator.js` и его транзитивные зависимости помечены как клиентский код, компонент `InspirationGenerator` и его дочерний компонент `FancyText` являются клиентскими компонентами.

#### Как `FancyText` является одновременно серверным и клиентским компонентом? {#how-is-fancytext-both-a-server-and-a-client-component}

Согласно приведенным выше определениям, компонент `FancyText` является одновременно серверным и клиентским компонентом, как такое может быть?

Во-первых, давайте уточним, что термин "компонент" не очень точен. Вот только два варианта понимания "компонента":

1.  "Компонент" может относиться к **определению компонента**. В большинстве случаев это будет функция.

    ```js
    // This is a definition of a component
    function MyComponent() {
        return <p>My Component</p>;
    }
    ```

2.  "Компонент" также может относиться к **компонентному использованию** его определения.

    ```js
    import MyComponent from './MyComponent';

    function App() {
        // This is a usage of a component
        return <MyComponent />;
    }
    ```

Часто неточность не имеет значения при объяснении концепций, но в данном случае она имеет значение.

Когда мы говорим о серверных или клиентских компонентах, мы имеем в виду использование компонентов.

-   Если компонент определен в модуле с директивой `'use client'`, или компонент импортируется и вызывается в клиентском компоненте, то использование компонента - это клиентский компонент.
-   В противном случае используется серверный компонент.

![Древовидный граф, в котором каждый узел представляет компонент, а его дочерние компоненты - дочерние компоненты. Узел верхнего уровня обозначен как 'App', и у него есть два дочерних компонента 'InspirationGenerator' и 'FancyText'. У 'InspirationGenerator' есть два дочерних компонента, 'FancyText' и 'Copyright'. И 'InspirationGenerator', и его дочерний компонент 'FancyText' помечены как клиентские.](use_client_render_tree.webp)

<small>_Дерево рендеринга иллюстрирует использование компонентов._</small>

Возвращаясь к вопросу о `FancyText`, мы видим, что в определении компонента _нет_ директивы `'use client'` и у него есть два варианта использования.

Использование `FancyText` в качестве дочернего компонента `App`, маркирует это использование как серверный компонент. Когда `FancyText` импортируется и вызывается в `InspirationGenerator`, это использование `FancyText` является клиентским компонентом, поскольку `InspirationGenerator` содержит директиву `'use client'`.

Это означает, что определение компонента для `FancyText` будет оцениваться на сервере, а также загружаться клиентом для отображения его использования в качестве клиентского компонента.

#### Почему `Copyright` является серверным компонентом? {#why-is-copyright-a-server-component}

Поскольку `Copyright` отображается как дочерний компонент клиентского компонента `InspirationGenerator`, вы можете быть удивлены, что он является серверным компонентом.

Вспомните, что `'use client'` определяет границу между серверным и клиентским кодом на дереве зависимостей _модуля_, а не на дереве рендеринга.

![Древовидный граф, верхний узел которого представляет модуль 'App.js'. У 'App.js' есть три дочерних модуля: 'Copyright.js', 'FancyText.js' и 'InspirationGenerator.js'. У 'InspirationGenerator.js' есть два дочерних узла: 'FancyText.js' и 'inspirations.js'. Узлы под и включая 'InspirationGenerator.js' имеют желтый цвет фона, чтобы обозначить, что этот подграф является клиентским из-за директивы 'use client' в 'InspirationGenerator.js'.](use_client_render_tree.webp)

<small>_`'use client'` определяет границу между серверным и клиентским кодом в дереве зависимостей модуля._</small>

В дереве зависимостей модулей мы видим, что `App.js` импортирует и вызывает `Copyright` из модуля `Copyright.js`. Поскольку `Copyright.js` не содержит директивы `'use client'`, использование компонента отображается на сервере. Компонент `App` отображается на сервере, так как он является корневым компонентом.

Клиентские компоненты могут рендерить серверные компоненты, потому что вы можете передавать JSX в качестве реквизита. В данном случае `InspirationGenerator` получает `Copyright` в качестве [`children`](../../learn/passing-props-to-a-component.md#passing-jsx-as-children). Однако модуль `InspirationGenerator` никогда напрямую не импортирует модуль `Copyright` и не вызывает компонент, все это делает `App`. Фактически, компонент `Copyright` полностью выполняется до того, как `InspirationGenerator` начинает рендеринг.

Отсюда следует вывод, что отношения рендеринга между компонентами типа "родитель-ребенок" не гарантируют одинакового окружения рендеринга.

### Когда использовать `'use client'` {#when-to-use-use-client}

С помощью `'use client'` вы можете определить, когда компоненты являются клиентскими компонентами. Поскольку серверные компоненты используются по умолчанию, здесь приводится краткий обзор преимуществ и ограничений серверных компонентов, чтобы определить, когда вам нужно пометить что-то как клиентское.

Для простоты мы говорим о серверных компонентах, но те же принципы применимы ко всему коду в вашем приложении, который выполняется на сервере.

#### Преимущества серверных компонентов {#advantages}

-   Серверные компоненты позволяют сократить объем кода, отправляемого и выполняемого клиентом. Только клиентские модули собираются и оцениваются клиентом.
-   Серверные компоненты выигрывают от работы на сервере. Они получают доступ к локальной файловой системе и могут работать с низкой задержкой при получении данных и сетевых запросах.

#### Ограничения серверных компонентов {#limitations}

-   Серверные компоненты не могут поддерживать взаимодействие, поскольку обработчики событий должны быть зарегистрированы и вызваны клиентом.
    -   Например, обработчики событий типа `onClick` могут быть определены только в клиентских компонентах.
-   Серверные компоненты не могут использовать большинство хуков.
    -   Когда серверные компоненты отрисовываются, их вывод - это, по сути, список компонентов для отрисовки клиентом. Серверные компоненты не сохраняются в памяти после рендеринга и не могут иметь собственного состояния.

### Сериализуемые типы, возвращаемые серверными компонентами {#serializable-types}

Как и в любом приложении React, родительские компоненты передают данные дочерним компонентам. Поскольку они отображаются в разных средах, передача данных от серверного компонента к клиентскому компоненту требует особого внимания.

Значения реквизитов, передаваемые от серверного компонента к клиентскому компоненту, должны быть сериализуемыми.

К сериализуемым реквизитам относятся:

-   Примитивы
    -   [строка](https://developer.mozilla.org/docs/Glossary/String)
    -   [число](https://developer.mozilla.org/docs/Glossary/Number)
    -   [bigint](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/BigInt)
    -   [boolean](https://developer.mozilla.org/docs/Glossary/Boolean)
    -   [undefined](https://developer.mozilla.org/docs/Glossary/Undefined)
    -   [null](https://developer.mozilla.org/docs/Glossary/Null)
    -   [symbol](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Symbol), только символы, зарегистрированные в глобальном реестре Symbol через [`Symbol.for`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Symbol/for)
-   Iterables, содержащие сериализуемые значения
    -   [String](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String)
    -   [Array](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array)
    -   [Map](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map)
    -   [Set](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Set)
    -   [TypedArray](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) и [ArrayBuffer](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)
-   [Date](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date)
-   Обычные [объекты](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object): созданные с помощью [инициализаторов объектов](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Object_initializer), с сериализуемыми свойствами
-   Функции, являющиеся [Действиями сервера](./use-server.md)
-   Элементы клиентского или серверного компонента (JSX)
-   [Promises](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Примечательно, что не поддерживаются:

-   [Функции](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Function), которые не экспортируются из модулей с клиентской разметкой или не помечены [`'use server'`](./use-server.md)
-   [Классы](https://developer.mozilla.org/docs/Learn/JavaScript/Objects/Classes_in_JavaScript)
-   Объекты, являющиеся экземплярами любого класса (кроме упомянутых встроенных) или объекты с [нулевым прототипом](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)
-   Символы, не зарегистрированные глобально, например, `Symbol('mySymbol')`.

## Использование {#usage}

### Построение с интерактивностью и состоянием {#building-with-interactivity-and-state}

=== "App.js"

    ```js
    'use client';

    import { useState } from 'react';

    export default function Counter({ initialValue = 0 }) {
    	const [countValue, setCountValue] = useState(
    		initialValue
    	);
    	const increment = () => setCountValue(countValue + 1);
    	const decrement = () => setCountValue(countValue - 1);
    	return (
    		<>
    			<h2>Count Value: {countValue}</h2>
    			<button onClick={increment}>+1</button>
    			<button onClick={decrement}>-1</button>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/w65qsc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Поскольку `Counter` требует как хук `useState`, так и обработчики событий для увеличения или уменьшения значения, этот компонент должен быть клиентским компонентом и потребует директивы `'use client'` в верхней части.

В отличие от этого, компоненту, который отображает пользовательский интерфейс без взаимодействия, не нужно быть клиентским компонентом.

```js
import { readFile } from 'node:fs/promises';
import Counter from './Counter';

export default async function CounterContainer() {
    const initialValue = await readFile(
        '/path/to/counter_value'
    );
    return <Counter initialValue={initialValue} />;
}
```

Например, родительский компонент `Counter`, `CounterContainer`, не требует `'use client'`, поскольку он не является интерактивным и не использует состояние. Кроме того, `CounterContainer` должен быть серверным компонентом, поскольку он читает из локальной файловой системы на сервере, что возможно только в серверном компоненте.

Существуют также компоненты, которые не используют никаких функций, предназначенных только для сервера или клиента, и могут быть независимы от того, где они отображаются. В нашем предыдущем примере одним из таких компонентов является `FancyText`.

```js
export default function FancyText({ title, text }) {
    return title ? (
        <h1 className="fancy title">{text}</h1>
    ) : (
        <h3 className="fancy cursive">{text}</h3>
    );
}
```

В этом случае мы не добавляем директиву `'use client'`, в результате чего при обращении к серверному компоненту в браузер отправляется вывод `FancyText` (а не его исходный код). Как было показано в предыдущем примере приложения Inspirations, `FancyText` используется как серверный или клиентский компонент, в зависимости от того, где он импортируется и используется.

Но если HTML-вывод `FancyText` велик по отношению к его исходному коду (включая зависимости), было бы эффективнее заставить его всегда быть клиентским компонентом. Компоненты, возвращающие длинную строку пути к SVG, - это один из случаев, когда может быть эффективнее заставить компонент быть клиентским компонентом.

### Использование клиентских API {#using-client-apis}

Ваше приложение React может использовать специфические клиентские API, такие как API браузера для веб-хранилища, работы с аудио и видео, аппаратного обеспечения устройства, среди [других](https://developer.mozilla.org/docs/Web/API).

В этом примере компонент использует [DOM APIs](https://developer.mozilla.org/docs/Glossary/DOM) для манипулирования элементом [`canvas`](https://developer.mozilla.org/docs/Web/HTML/Element/canvas). Поскольку эти API доступны только в браузере, он должен быть помечен как клиентский компонент.

```js
'use client';

import { useRef, useEffect } from 'react';

export default function Circle() {
    const ref = useRef(null);
    useLayoutEffect(() => {
        const canvas = ref.current;
        const context = canvas.getContext('2d');
        context.reset();
        context.beginPath();
        context.arc(100, 75, 50, 0, 2 * Math.PI);
        context.stroke();
    });
    return <canvas ref={ref} />;
}
```

### Использование сторонних библиотек {#using-third-party-libraries}

Часто в приложениях на React вы используете сторонние библиотеки для работы с общими шаблонами пользовательского интерфейса или логикой.

Эти библиотеки могут опираться на хуки компонентов или клиентские API. Сторонние компоненты, использующие любой из следующих API React, должны запускаться на клиенте:

-   [createContext](createContext.md)
-   [`react`](hooks.md) и `react-dom` Hooks, за исключением [`use`](use.md) и [`useId`](useId.md)
-   [forwardRef](forwardRef.md)
-   [memo](memo.md)
-   [startTransition](startTransition.md)
-   Если они используют клиентские API, например, вставку DOM или нативные представления платформы

Если эти библиотеки были обновлены для совместимости с React Server Components, то они уже будут содержать собственные маркеры `'use client'`, что позволит вам использовать их непосредственно из ваших серверных компонентов. Если библиотека не была обновлена, или компоненту нужны такие параметры, как обработчики событий, которые могут быть указаны только на клиенте, вам может потребоваться добавить собственный файл клиентского компонента между сторонним клиентским компонентом и вашим серверным компонентом, где вы хотите его использовать.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/use-client](https://react.dev/reference/react/use-client)</small>
