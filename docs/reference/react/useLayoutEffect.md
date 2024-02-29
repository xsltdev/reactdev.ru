---
description: useLayoutEffect - это версия useEffect, которая срабатывает перед тем, как браузер перерисовывает экран
---

# useLayoutEffect

!!!danger "Производительность"

    `useLayoutEffect` может снизить производительность. Предпочитайте [`useEffect`](useEffect.md), когда это возможно.

<big>**`useLayoutEffect`** - это версия [`useEffect`](useEffect.md), которая срабатывает перед тем, как браузер перерисовывает экран.</big>

```js
useLayoutEffect(setup, dependencies?)
```

## Описание {#reference}

### `useLayoutEffect(setup, dependencies?)` {#useinsertioneffect}

Вызывает `useLayoutEffect` для выполнения измерений макета перед тем, как браузер перерисовывает экран:

```js
import { useState, useRef, useLayoutEffect } from 'react';

function Tooltip() {
    const ref = useRef(null);
    const [tooltipHeight, setTooltipHeight] = useState(0);

    useLayoutEffect(() => {
        const {
            height,
        } = ref.current.getBoundingClientRect();
        setTooltipHeight(height);
    }, []);
    // ...
}
```

#### Параметры {#parameters}

-   `setup`: Функция с логикой вашего Эффекта. Ваша функция настройки может также возвращать функцию _cleanup_. Прежде чем ваш компонент будет добавлен в DOM, React запустит вашу функцию настройки. После каждого повторного рендеринга с измененными зависимостями React будет сначала запускать функцию очистки (если вы ее предоставили) со старыми значениями, а затем запускать вашу функцию настройки с новыми значениями. Прежде чем ваш компонент будет удален из DOM, React запустит вашу функцию очистки.
-   **опционально** `dependencies`: Список всех реактивных значений, на которые ссылается код `setup`. Реактивные значения включают `props`, `state`, а также все переменные и функции, объявленные непосредственно в теле вашего компонента. Если ваш линтер [настроен на React](../../learn/editor-setup.md#linting), он проверит, что каждое реактивное значение правильно указано в качестве зависимости. Список зависимостей должен иметь постоянное количество элементов и быть написан inline по типу `[dep1, dep2, dep3]`. React будет сравнивать каждую зависимость с предыдущим значением, используя сравнение [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Если вы опустите этот аргумент, ваш Effect будет запускаться заново после каждого повторного рендеринга компонента.

#### Возвращает {#returns}

`useLayoutEffect` возвращает `undefined`.

#### Ограничения {#caveats}

-   `useLayoutEffect` является хуком, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, извлеките компонент и переместите эффект туда.
-   Когда включен строгий режим, React будет **запускать один дополнительный цикл настройки+очистки** перед первой реальной настройкой. Это стресс-тест, который гарантирует, что ваша логика очистки "отражает" вашу логику настройки и что она останавливает или отменяет все, что делает настройка. Если это вызывает проблему, [реализуйте функцию очистки](../../learn/synchronizing-with-effects.md#how-to-handle-the-effect-firing-twice-in-development).
-   Если некоторые из ваших зависимостей являются объектами или функциями, определенными внутри компонента, есть риск, что они **приведут к тому, что Эффект будет перезапускаться чаще, чем нужно.** Чтобы исправить это, удалите ненужные зависимости `object` и `function`. Вы также можете извлекать обновления состояния и нереактивную логику наружу вашего Эффекта.
-   Эффекты **работают только на клиенте.** Они не работают во время рендеринга на сервере.
-   Код внутри `useLayoutEffect` и все запланированные обновления состояния **блокируют браузер от перерисовки экрана.** При чрезмерном использовании это делает ваше приложение медленным. Когда это возможно, предпочитайте [`useEffect`](useEffect.md).

## Использование {#usage}

### Измерение макета до того, как браузер перерисует экран {#measuring-layout-before-the-browser-repaints-the-screen}

Большинству компонентов не нужно знать свое положение и размер на экране, чтобы решить, что отображать. Они только возвращают некоторый JSX. Затем браузер вычисляет их _разметку_ (положение и размер) и перерисовывает экран.

Иногда этого недостаточно. Представьте себе всплывающую подсказку, которая появляется рядом с каким-то элементом при наведении. Если места достаточно, всплывающая подсказка должна появиться над элементом, но если она не помещается, то должна появиться под ним. Чтобы отобразить всплывающую подсказку в правильном конечном положении, необходимо знать ее высоту (т.е. поместится ли она сверху).

Для этого необходимо выполнить рендеринг в два прохода:

1.  Отрисовать всплывающую подсказку в любом месте (даже при неправильном положении).
2.  Измерьте его высоту и решите, где разместить всплывающую подсказку.
3.  Снова отобразите всплывающую подсказку _в правильном месте_.

**Все это должно произойти до того, как браузер перерисует экран.** Вы не хотите, чтобы пользователь видел, что всплывающая подсказка перемещается. Вызовите `useLayoutEffect`, чтобы выполнить измерения макета до того, как браузер перерисует экран:

```js hl_lines="7-13"
function Tooltip() {
    const ref = useRef(null);

    // You don't know real height yet
    const [tooltipHeight, setTooltipHeight] = useState(0);

    useLayoutEffect(() => {
        const {
            height,
        } = ref.current.getBoundingClientRect();
        // Re-render now that you know the real height
        setTooltipHeight(height);
    }, []);

    // ...use tooltipHeight in the rendering logic below...
}
```

Вот как это работает шаг за шагом:

1.  `Tooltip` рендерится с начальным `tooltipHeight = 0` (поэтому всплывающая подсказка может быть неправильно позиционирована).
2.  React помещает ее в DOM и запускает код в `useLayoutEffect`.
3.  ержимого всплывающей подсказки и вызывает немедленный повторный рендеринг.
4.  `Tooltip` рендерится снова с реальным `tooltipHeight` (чтобы всплывающая подсказка была правильно расположена).
5.  React обновляет его в DOM, и браузер наконец отображает всплывающую подсказку.

=== "App.js"

    ```js
    import ButtonWithTooltip from './ButtonWithTooltip.js';

    export default function App() {
    	return (
    		<div>
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip does not fit above the
    						button.
    						<br />
    						This is why it's displayed below
    						instead!
    					</div>
    				}
    			>
    				Hover over me (tooltip above)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    		</div>
    	);
    }
    ```

=== "ButtonWithTooltip.js"

    ```js
    import { useState, useRef } from 'react';
    import Tooltip from './Tooltip.js';

    export default function ButtonWithTooltip({
    	tooltipContent,
    	...rest
    }) {
    	const [targetRect, setTargetRect] = useState(null);
    	const buttonRef = useRef(null);
    	return (
    		<>
    			<button
    				{...rest}
    				ref={buttonRef}
    				onPointerEnter={() => {
    					const rect = buttonRef.current.getBoundingClientRect();
    					setTargetRect({
    						left: rect.left,
    						top: rect.top,
    						right: rect.right,
    						bottom: rect.bottom,
    					});
    				}}
    				onPointerLeave={() => {
    					setTargetRect(null);
    				}}
    			/>
    			{targetRect !== null && (
    				<Tooltip targetRect={targetRect}>
    					{tooltipContent}
    				</Tooltip>
    			)}
    		</>
    	);
    }
    ```

=== "Tooltip.js"

    ```js
    import { useRef, useLayoutEffect, useState } from 'react';
    import { createPortal } from 'react-dom';
    import TooltipContainer from './TooltipContainer.js';

    export default function Tooltip({ children, targetRect }) {
    	const ref = useRef(null);
    	const [tooltipHeight, setTooltipHeight] = useState(0);

    	useLayoutEffect(() => {
    		const {
    			height,
    		} = ref.current.getBoundingClientRect();
    		setTooltipHeight(height);
    		console.log('Measured tooltip height: ' + height);
    	}, []);

    	let tooltipX = 0;
    	let tooltipY = 0;
    	if (targetRect !== null) {
    		tooltipX = targetRect.left;
    		tooltipY = targetRect.top - tooltipHeight;
    		if (tooltipY < 0) {
    			// It doesn't fit above, so place below.
    			tooltipY = targetRect.bottom;
    		}
    	}

    	return createPortal(
    		<TooltipContainer
    			x={tooltipX}
    			y={tooltipY}
    			contentRef={ref}
    		>
    			{children}
    		</TooltipContainer>,
    		document.body
    	);
    }
    ```

=== "TooltipContainer.js"

    ```js
    export default function TooltipContainer({
    	children,
    	x,
    	y,
    	contentRef,
    }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				pointerEvents: 'none',
    				left: 0,
    				top: 0,
    				transform: `translate3d(${x}px, ${y}px, 0)`,
    			}}
    		>
    			<div ref={contentRef} className="tooltip">
    				{children}
    			</div>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/nwmw4p?view=Editor+%2B+Preview&module=%2Fsrc%2FTooltip.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что хотя компонент `Tooltip` должен быть отрисован в два прохода (сначала с `tooltipHeight`, инициализированным в `0`, а затем с реальной измеренной высотой), вы видите только конечный результат. Вот почему для этого примера вам нужен `useLayoutEffect` вместо [`useEffect`](useEffect.md). Давайте рассмотрим разницу в деталях ниже.

### useLayoutEffect vs useEffect {#examples}

**1. `useLayoutEffect` блокирует браузер от перерисовки**

React гарантирует, что код внутри `useLayoutEffect` и любые обновления состояния, запланированные внутри него, будут обработаны **до того, как браузер перерисует экран.** Это позволяет вам отрисовать всплывающую подсказку, измерить ее, и снова отрисовать ее так, чтобы пользователь не заметил первого дополнительного отрисовки. Другими словами, `useLayoutEffect` блокирует браузер от рисования.

=== "App.js"

    ```js
    import ButtonWithTooltip from './ButtonWithTooltip.js';

    export default function App() {
    	return (
    		<div>
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip does not fit above the
    						button.
    						<br />
    						This is why it's displayed below
    						instead!
    					</div>
    				}
    			>
    				Hover over me (tooltip above)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    		</div>
    	);
    }
    ```

=== "ButtonWithTooltip.js"

    ```js
    import { useState, useRef } from 'react';
    import Tooltip from './Tooltip.js';

    export default function ButtonWithTooltip({
    	tooltipContent,
    	...rest
    }) {
    	const [targetRect, setTargetRect] = useState(null);
    	const buttonRef = useRef(null);
    	return (
    		<>
    			<button
    				{...rest}
    				ref={buttonRef}
    				onPointerEnter={() => {
    					const rect = buttonRef.current.getBoundingClientRect();
    					setTargetRect({
    						left: rect.left,
    						top: rect.top,
    						right: rect.right,
    						bottom: rect.bottom,
    					});
    				}}
    				onPointerLeave={() => {
    					setTargetRect(null);
    				}}
    			/>
    			{targetRect !== null && (
    				<Tooltip targetRect={targetRect}>
    					{tooltipContent}
    				</Tooltip>
    			)}
    		</>
    	);
    }
    ```

=== "Tooltip.js"

    ```js
    import { useRef, useLayoutEffect, useState } from 'react';
    import { createPortal } from 'react-dom';
    import TooltipContainer from './TooltipContainer.js';

    export default function Tooltip({ children, targetRect }) {
    	const ref = useRef(null);
    	const [tooltipHeight, setTooltipHeight] = useState(0);

    	useLayoutEffect(() => {
    		const {
    			height,
    		} = ref.current.getBoundingClientRect();
    		setTooltipHeight(height);
    	}, []);

    	let tooltipX = 0;
    	let tooltipY = 0;
    	if (targetRect !== null) {
    		tooltipX = targetRect.left;
    		tooltipY = targetRect.top - tooltipHeight;
    		if (tooltipY < 0) {
    			// It doesn't fit above, so place below.
    			tooltipY = targetRect.bottom;
    		}
    	}

    	return createPortal(
    		<TooltipContainer
    			x={tooltipX}
    			y={tooltipY}
    			contentRef={ref}
    		>
    			{children}
    		</TooltipContainer>,
    		document.body
    	);
    }
    ```

=== "TooltipContainer.js"

    ```js
    export default function TooltipContainer({
    	children,
    	x,
    	y,
    	contentRef,
    }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				pointerEvents: 'none',
    				left: 0,
    				top: 0,
    				transform: `translate3d(${x}px, ${y}px, 0)`,
    			}}
    		>
    			<div ref={contentRef} className="tooltip">
    				{children}
    			</div>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/skfffd?view=Editor+%2B+Preview&module=%2Fsrc%2FTooltip.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. `useEffect` не блокирует браузер**

Вот тот же пример, но с [`useEffect`](useEffect.md) вместо `useLayoutEffect`. Если у вас медленное устройство, вы можете заметить, что иногда всплывающая подсказка "мерцает", и вы на короткое время видите ее начальное положение перед исправленным положением.

=== "App.js"

    ```js
    import ButtonWithTooltip from './ButtonWithTooltip.js';

    export default function App() {
    	return (
    		<div>
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip does not fit above the
    						button.
    						<br />
    						This is why it's displayed below
    						instead!
    					</div>
    				}
    			>
    				Hover over me (tooltip above)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    		</div>
    	);
    }
    ```

=== "ButtonWithTooltip.js"

    ```js
    import { useState, useRef } from 'react';
    import Tooltip from './Tooltip.js';

    export default function ButtonWithTooltip({
    	tooltipContent,
    	...rest
    }) {
    	const [targetRect, setTargetRect] = useState(null);
    	const buttonRef = useRef(null);
    	return (
    		<>
    			<button
    				{...rest}
    				ref={buttonRef}
    				onPointerEnter={() => {
    					const rect = buttonRef.current.getBoundingClientRect();
    					setTargetRect({
    						left: rect.left,
    						top: rect.top,
    						right: rect.right,
    						bottom: rect.bottom,
    					});
    				}}
    				onPointerLeave={() => {
    					setTargetRect(null);
    				}}
    			/>
    			{targetRect !== null && (
    				<Tooltip targetRect={targetRect}>
    					{tooltipContent}
    				</Tooltip>
    			)}
    		</>
    	);
    }
    ```

=== "Tooltip.js"

    ```js
    import { useRef, useEffect, useState } from 'react';
    import { createPortal } from 'react-dom';
    import TooltipContainer from './TooltipContainer.js';

    export default function Tooltip({ children, targetRect }) {
    	const ref = useRef(null);
    	const [tooltipHeight, setTooltipHeight] = useState(0);

    	useEffect(() => {
    		const {
    			height,
    		} = ref.current.getBoundingClientRect();
    		setTooltipHeight(height);
    	}, []);

    	let tooltipX = 0;
    	let tooltipY = 0;
    	if (targetRect !== null) {
    		tooltipX = targetRect.left;
    		tooltipY = targetRect.top - tooltipHeight;
    		if (tooltipY < 0) {
    			// It doesn't fit above, so place below.
    			tooltipY = targetRect.bottom;
    		}
    	}

    	return createPortal(
    		<TooltipContainer
    			x={tooltipX}
    			y={tooltipY}
    			contentRef={ref}
    		>
    			{children}
    		</TooltipContainer>,
    		document.body
    	);
    }
    ```

=== "TooltipContainer.js"

    ```js
    export default function TooltipContainer({
    	children,
    	x,
    	y,
    	contentRef,
    }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				pointerEvents: 'none',
    				left: 0,
    				top: 0,
    				transform: `translate3d(${x}px, ${y}px, 0)`,
    			}}
    		>
    			<div ref={contentRef} className="tooltip">
    				{children}
    			</div>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/s3yvm5?view=Editor+%2B+Preview&module=%2Fsrc%2FTooltip.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Чтобы ошибку было легче воспроизвести, в этой версии добавлена искусственная задержка во время рендеринга. React позволит браузеру закрасить экран до того, как обработает обновление состояния внутри `useEffect`. В результате всплывающая подсказка мерцает:

=== "App.js"

    ```js
    import ButtonWithTooltip from './ButtonWithTooltip.js';

    export default function App() {
    	return (
    		<div>
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip does not fit above the
    						button.
    						<br />
    						This is why it's displayed below
    						instead!
    					</div>
    				}
    			>
    				Hover over me (tooltip above)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    			<div style={{ height: 50 }} />
    			<ButtonWithTooltip
    				tooltipContent={
    					<div>
    						This tooltip fits above the button
    					</div>
    				}
    			>
    				Hover over me (tooltip below)
    			</ButtonWithTooltip>
    		</div>
    	);
    }
    ```

=== "ButtonWithTooltip.js"

    ```js
    import { useState, useRef } from 'react';
    import Tooltip from './Tooltip.js';

    export default function ButtonWithTooltip({
    	tooltipContent,
    	...rest
    }) {
    	const [targetRect, setTargetRect] = useState(null);
    	const buttonRef = useRef(null);
    	return (
    		<>
    			<button
    				{...rest}
    				ref={buttonRef}
    				onPointerEnter={() => {
    					const rect = buttonRef.current.getBoundingClientRect();
    					setTargetRect({
    						left: rect.left,
    						top: rect.top,
    						right: rect.right,
    						bottom: rect.bottom,
    					});
    				}}
    				onPointerLeave={() => {
    					setTargetRect(null);
    				}}
    			/>
    			{targetRect !== null && (
    				<Tooltip targetRect={targetRect}>
    					{tooltipContent}
    				</Tooltip>
    			)}
    		</>
    	);
    }
    ```

=== "Tooltip.js"

    ```js
    import { useRef, useEffect, useState } from 'react';
    import { createPortal } from 'react-dom';
    import TooltipContainer from './TooltipContainer.js';

    export default function Tooltip({ children, targetRect }) {
    	const ref = useRef(null);
    	const [tooltipHeight, setTooltipHeight] = useState(0);

    	// This artificially slows down rendering
    	let now = performance.now();
    	while (performance.now() - now < 100) {
    		// Do nothing for a bit...
    	}

    	useEffect(() => {
    		const {
    			height,
    		} = ref.current.getBoundingClientRect();
    		setTooltipHeight(height);
    	}, []);

    	let tooltipX = 0;
    	let tooltipY = 0;
    	if (targetRect !== null) {
    		tooltipX = targetRect.left;
    		tooltipY = targetRect.top - tooltipHeight;
    		if (tooltipY < 0) {
    			// It doesn't fit above, so place below.
    			tooltipY = targetRect.bottom;
    		}
    	}

    	return createPortal(
    		<TooltipContainer
    			x={tooltipX}
    			y={tooltipY}
    			contentRef={ref}
    		>
    			{children}
    		</TooltipContainer>,
    		document.body
    	);
    }
    ```

=== "TooltipContainer.js"

    ```js
    export default function TooltipContainer({
    	children,
    	x,
    	y,
    	contentRef,
    }) {
    	return (
    		<div
    			style={{
    				position: 'absolute',
    				pointerEvents: 'none',
    				left: 0,
    				top: 0,
    				transform: `translate3d(${x}px, ${y}px, 0)`,
    			}}
    		>
    			<div ref={contentRef} className="tooltip">
    				{children}
    			</div>
    		</div>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/l6qy78?view=Editor+%2B+Preview&module=%2Fsrc%2FTooltip.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Измените этот пример на `useLayoutEffect` и обратите внимание, что он блокирует закраску, даже если рендеринг замедлен.

!!!note "Производительность"

    Рендеринг в два прохода и блокировка браузера снижают производительность. Старайтесь избегать этого, когда можете.

## Устранение неполадок {#troubleshooting}

### Я получаю ошибку: "`useLayoutEffect` ничего не делает на сервере" {#im-getting-an-error-uselayouteffect-does-nothing-on-the-server}

Цель `useLayoutEffect` - позволить вашему компоненту использовать информацию о макете для рендеринга:

1.  Рендеринг начального содержимого.
2.  Измерить макет _до того, как браузер перерисует экран_.
3.  Отрисуйте конечный контент, используя информацию о макете, которую вы считали.

Когда вы или ваш фреймворк использует [серверный рендеринг](../react-dom/server/index.md), ваше приложение React рендерит в HTML на сервере для первоначального рендеринга. Это позволяет вам показать начальный HTML до загрузки кода JavaScript.

Проблема в том, что на сервере нет информации о макете.

В предыдущем примере вызов `useLayoutEffect` в компоненте `Tooltip` позволяет ему правильно позиционироваться (либо выше, либо ниже содержимого) в зависимости от высоты содержимого. Если бы вы попытались отобразить `Tooltip` как часть исходного серверного HTML, это было бы невозможно определить. На сервере еще нет макета! Поэтому, даже если бы вы отобразили его на сервере, его положение "перепрыгнуло" бы на клиенте после загрузки и выполнения JavaScript.

Обычно компоненты, которые полагаются на информацию о макете, не нуждаются в рендеринге на сервере. Например, вероятно, нет смысла показывать `Tooltip` во время первоначального рендеринга. Она вызывается взаимодействием с клиентом.

Однако, если вы столкнулись с этой проблемой, у вас есть несколько вариантов:

-   Замените `useLayoutEffect` на [`useEffect`](useEffect.md). Это говорит React, что можно отображать начальный результат рендеринга без блокировки закраски (потому что исходный HTML станет виден до запуска вашего Эффекта).
-   В качестве альтернативы, [пометьте свой компонент как предназначенный только для клиентов](Suspense.md#providing-a-fallback-for-server-errors-and-server-only-content) Это говорит React заменить содержимое до ближайшей границы [`<Suspense>`](Suspense.md) на фаллбэк загрузки (например, спиннер или мерцание) во время серверного рендеринга.
-   Альтернативно, вы можете рендерить компонент с `useLayoutEffect` только после гидратации. Храните состояние boolean `isMounted`, которое инициализируется в `false`, и устанавливайте его в `true` внутри вызова `useEffect`. Ваша логика рендеринга может быть такой: `return isMounted ? <RealContent /> : <FallbackContent />`. На сервере и во время гидратации пользователь увидит `FallbackContent`, который не должен вызывать `useLayoutEffect`. Затем React заменит его на `RealContent`, который работает только на клиенте и может включать вызовы `useLayoutEffect`.
-   Если вы синхронизируете свой компонент с внешним хранилищем данных и полагаетесь на `useLayoutEffect` по причинам, отличным от измерения макета, рассмотрите вместо него [`useSyncExternalStore`](useSyncExternalStore.md), который [поддерживает серверный рендеринг](useSyncExternalStore.md#adding-support-for-server-rendering).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)</small>
