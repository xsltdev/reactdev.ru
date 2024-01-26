---
description: React, как и многие другие библиотеки пользовательского интерфейса, моделирует пользовательский интерфейс в виде дерева. Представление о вашем приложении как о дереве полезно для понимания взаимосвязи между компонентами
---

# Понимание своего UI как дерева

<big>Ваше приложение React приобретает форму, в нем много компонентов, вложенных друг в друга. Как React отслеживает структуру компонентов вашего приложения?

React, как и многие другие библиотеки пользовательского интерфейса, моделирует пользовательский интерфейс в виде дерева. Представление о вашем приложении как о дереве полезно для понимания взаимосвязи между компонентами. Это понимание поможет вам отладить такие будущие концепции, как производительность и управление состояниями.</big>

!!!tip "Вы узнаете"

    -   Как React "видит" структуры компонентов
    -   Что такое дерево рендеринга и для чего оно нужно
    -   Что такое дерево зависимостей модулей и чем оно полезно

## Ваш UI в виде дерева {#your-ui-as-a-tree}

Деревья - это модель отношений между элементами, и пользовательский интерфейс часто представляют с помощью древовидных структур. Например, браузеры используют древовидные структуры для моделирования HTML ([DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model/Introduction)) и CSS ([CSSOM](https://developer.mozilla.org/docs/Web/API/CSS_Object_Model)). Мобильные платформы также используют деревья для представления иерархии представлений.

![Диаграмма с тремя секциями, расположенными горизонтально. В первой секции расположены три прямоугольника, сложенные вертикально, с надписями 'Component A', 'Component B' и 'Component C'. Переход к следующей панели представляет собой стрелку с логотипом React на вершине и надписью 'React'. Средняя секция содержит дерево компонентов, корень которого обозначен 'A', а два дочерних компонента - 'B' и 'C'. Переход к следующей секции снова осуществляется с помощью стрелки с логотипом React сверху и надписью 'React DOM'. Третья и последняя секция представляет собой каркас браузера, содержащий дерево из 8 узлов, у которого выделено только подмножество (указывающее на поддерево из средней секции).](preserving_state_dom_tree.webp)

_React создает дерево пользовательского интерфейса из ваших компонентов. В этом примере дерево пользовательского интерфейса используется для рендеринга в DOM._

Подобно браузерам и мобильным платформам, React также использует древовидные структуры для управления и моделирования отношений между компонентами в приложении React. Эти деревья являются полезными инструментами для понимания того, как данные проходят через приложение React и как оптимизировать рендеринг и размер приложения.

## Дерево рендеринга {#the-render-tree}

Важной особенностью компонентов является возможность компоновать компоненты из других компонентов. По мере [вложения компонентов](./your-first-component.md#nesting-and-organizing-components) у нас появляется концепция родительских и дочерних компонентов, где каждый родительский компонент может быть дочерним по отношению к другому компоненту.

Когда мы рендерим React-приложение, мы можем смоделировать эти отношения в дереве, известном как дерево рендеринга.

Здесь представлено приложение React, которое отображает вдохновляющие цитаты.

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
    import * as React from 'react';
    import quotes from './quotes';
    import FancyText from './FancyText';

    export default function InspirationGenerator({ children }) {
    	const [index, setIndex] = React.useState(0);
    	const quote = quotes[index];
    	const next = () =>
    		setIndex((index + 1) % quotes.length);

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

=== "quotes.js"

    ```js
    export default [
    	'Don’t let yesterday take up too much of today.” — Will Rogers',
    	'Ambition is putting a ladder against the sky.',
    	"A joy that's shared is a joy made double.",
    ];
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/m725yh?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

![Древовидный граф с пятью узлами. Каждый узел представляет компонент. Корнем дерева является App, от него отходят две стрелки к 'InspirationGenerator' и 'FancyText'. Стрелки помечены словом 'renders'. Узел 'InspirationGenerator' также имеет две стрелки, указывающие на узлы 'FancyText' и 'Copyright'.](render_tree.webp)

_React создает дерево рендеринга, дерево пользовательского интерфейса, состоящее из рендеренных компонентов._

Из примера приложения мы можем построить дерево рендеринга.

Дерево состоит из узлов, каждый из которых представляет компонент. `App`, `FancyText`, `Copyright` и другие являются узлами в нашем дереве.

Корневым узлом в дереве рендеринга React является [корневой компонент](./importing-and-exporting-components.md#the-root-component-file) приложения. В данном случае корневым компонентом является `App`, и это первый компонент, который рендерит React. Каждая стрелка в дереве указывает от родительского компонента к дочернему.

!!!note "Где находятся HTML-теги в дереве рендеринга?"

    Вы можете заметить, что в приведенном выше дереве рендеринга нет упоминания о HTML-тегах, которые отображает каждый компонент. Это потому, что дерево рендеринга состоит только из [компонентов React](./your-first-component.md#components-ui-building-blocks).

    React, как фреймворк пользовательского интерфейса, не зависит от платформы. На react.dev мы показываем примеры, которые выводятся в веб, где в качестве примитивов пользовательского интерфейса используется HTML-разметка. Но приложение React с такой же вероятностью может быть создано для мобильной или настольной платформы, которая может использовать другие примитивы пользовательского интерфейса, такие как [UIView](https://developer.apple.com/documentation/uikit/uiview) или [FrameworkElement](https://learn.microsoft.com/en-us/dotnet/api/system.windows.frameworkelement?view=windowsdesktop-7.0).

    Эти платформенные примитивы пользовательского интерфейса не являются частью React. Деревья рендеринга React могут дать представление о нашем приложении React независимо от того, на какую платформу рендерится ваше приложение.

Дерево рендеринга представляет собой один проход рендеринга в приложении React. С помощью [условного рендеринга](./conditional-rendering.md) родительский компонент может рендерить разные дочерние компоненты в зависимости от переданных данных.

Мы можем обновить приложение, чтобы оно условно отображало либо вдохновляющую цитату, либо цвет.

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

=== "Color.js"

    ```js
    export default function Color({ value }) {
    	return (
    		<div
    			className="colorbox"
    			style={{ backgroundColor: value }}
    		/>
    	);
    }
    ```

=== "InspirationGenerator.js"

    ```js
    import * as React from 'react';
    import inspirations from './inspirations';
    import FancyText from './FancyText';
    import Color from './Color';

    export default function InspirationGenerator({ children }) {
    	const [index, setIndex] = React.useState(0);
    	const inspiration = inspirations[index];
    	const next = () =>
    		setIndex((index + 1) % inspirations.length);

    	return (
    		<>
    			<p>Your inspirational {inspiration.type} is:</p>
    			{inspiration.type === 'quote' ? (
    				<FancyText text={inspiration.value} />
    			) : (
    				<Color value={inspiration.value} />
    			)}

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
    	{
    		type: 'quote',
    		value:
    			'Don’t let yesterday take up too much of today.” — Will Rogers',
    	},
    	{ type: 'color', value: '#B73636' },
    	{
    		type: 'quote',
    		value:
    			'Ambition is putting a ladder against the sky.',
    	},
    	{ type: 'color', value: '#256266' },
    	{
    		type: 'quote',
    		value: "A joy that's shared is a joy made double.",
    	},
    	{ type: 'color', value: '#F9F2B4' },
    ];
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dw3zjl?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

</Sandpack>

![Древовидный граф с шестью узлами. Верхний узел дерева обозначен как "App", а две стрелки ведут к узлам, обозначенным как "InspirationGenerator" и "FancyText". Стрелки представляют собой сплошные линии и помечены словом 'renders'. Узел 'InspirationGenerator' также имеет три стрелки. Стрелки к узлам 'FancyText' и 'Color' - пунктирные и помечены словом 'renders?'. Последняя стрелка указывает на узел с надписью 'Copyright', она сплошная и помечена надписью 'renders'.](conditional_render_tree.webp)

_При условном рендеринге в разных рендерах дерево рендеринга может отображать разные компоненты._

В этом примере, в зависимости от типа `inspiration.type`, мы можем отобразить `<FancyText>` или `<Color>`. Дерево рендеринга может быть разным для каждого прохода рендеринга.

Хотя деревья рендеринга могут отличаться в разных проходах рендеринга, эти деревья в целом полезны для определения того, какими являются _верхнеуровневые_ и _листовые_ компоненты в приложении React. Компоненты верхнего уровня - это ближайшие к корневому компоненту компоненты, которые влияют на производительность рендеринга всех расположенных под ними компонентов и часто содержат наибольшую сложность. Листовые компоненты находятся в нижней части дерева, не имеют дочерних компонентов и часто перерисовываются.

Определение этих категорий компонентов полезно для понимания потока данных и производительности вашего приложения.

## Дерево зависимостей модулей {#the-module-dependency-tree}

Еще одна связь в приложении React, которую можно смоделировать с помощью дерева, - это зависимости модулей приложения. Когда мы [разбиваем наши компоненты](./importing-and-exporting-components.md#exporting-and-importing-a-component) и логику на отдельные файлы, мы создаем [JS-модули](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Modules), куда мы можем экспортировать компоненты, функции или константы.

Каждый узел в дереве зависимостей модуля - это модуль, а каждая ветвь представляет собой оператор `импорта` в этом модуле.

Если мы возьмем предыдущее приложение Inspirations, то сможем построить дерево зависимостей модулей, или дерево зависимостей для краткости.

![Древовидный граф с семью узлами. Каждый узел помечен именем модуля. Узел верхнего уровня дерева обозначен как 'App.js'. Три стрелки указывают на модули 'InspirationGenerator.js', 'FancyText.js' и 'Copyright.js', а сами стрелки помечены как 'imports'. От узла 'InspirationGenerator.js' идут три стрелки к трем модулям: 'FancyText.js', 'Color.js' и 'inspirations.js'. Стрелки помечены символом 'imports'.](module_dependency_tree.webp)

_Дерево зависимостей модулей для приложения Inspirations._

Корневым узлом дерева является корневой модуль, также известный как файл начальной точки. Часто именно этот модуль содержит корневой компонент.

При сравнении с деревом рендеринга того же приложения можно заметить схожие структуры, но есть и заметные отличия:

-   Узлы, составляющие дерево, представляют модули, а не компоненты.
-   Некомпонентные модули, такие как `inspirations.js`, также представлены в этом дереве. Дерево рендеринга содержит только компоненты.
-   `Copyright.js` отображается под `App.js`, но в дереве рендеринга компонент `Copyright` отображается как дочерний компонент `InspirationGenerator`. Это происходит потому, что `InspirationGenerator` принимает JSX как [children props](./passing-props-to-a-component.md#passing-jsx-as-children), поэтому он рендерит `Copyright` как дочерний компонент, но не импортирует модуль.

Деревья зависимостей полезны для определения того, какие модули необходимы для работы вашего React-приложения. При создании React-приложения для производства обычно выполняется этап сборки, на котором собирается весь необходимый JavaScript для отправки клиенту. Инструмент, отвечающий за это, называется [bundler](https://developer.mozilla.org/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Overview#the_modern_tooling_ecosystem), и для определения того, какие модули должны быть включены, bundlers использует дерево зависимостей.

По мере роста вашего приложения часто увеличивается и размер пакета. Большие размеры пакета требуют от клиента больших затрат на загрузку и запуск. Большие размеры пакета могут задерживать время отрисовки пользовательского интерфейса. Понимание дерева зависимостей вашего приложения может помочь в отладке этих проблем.

!!!note "Итого"

    -   Деревья - распространенный способ представления отношений между сущностями. Они часто используются для моделирования пользовательского интерфейса.
    -   Деревья рендеринга представляют вложенные отношения между компонентами React в течение одного рендера.
    -   При условном рендеринге дерево рендеринга может меняться при разных рендерах. При использовании различных значений prop компоненты могут рендерить различные дочерние компоненты.
    -   Деревья рендеринга помогают определить, что является компонентами верхнего уровня и листьями. Компоненты верхнего уровня влияют на производительность рендеринга всех компонентов, расположенных под ними, а листовые компоненты часто перерисовываются. Их идентификация полезна для понимания и отладки производительности рендеринга.
    -   Деревья зависимостей представляют собой зависимости модулей в приложении React.
    -   Деревья зависимостей используются инструментами сборки для компоновки кода, необходимого для поставки приложения.
    -   Деревья зависимостей полезны для отладки больших размеров пакетов, которые замедляют время отрисовки, и открывают возможности для оптимизации кода в пакете.

:material-information-outline: Источник &mdash; [https://react.dev/learn/understanding-your-ui-as-a-tree](https://react.dev/learn/understanding-your-ui-as-a-tree)
