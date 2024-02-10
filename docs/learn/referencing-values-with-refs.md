---
description: Когда вы хотите, чтобы компонент запомнил какую-то информацию, но не хотите, чтобы эта информация запускала новые рендеры, вы можете использовать ref
---

# Ссылка на значения с помощью Refs

<big>Когда вы хотите, чтобы компонент "запомнил" какую-то информацию, но не хотите, чтобы эта информация [запускала новые рендеры](render-and-commit.md), вы можете использовать **ref**.</big>

!!!tip "Вы узнаете"

    -   Как добавить ссылку в свой компонент
    -   Как обновить значение ссылки
    -   Чем отличаются ссылки от состояния
    -   Как безопасно использовать ссылки

## Добавление ссылки в ваш компонент {#adding-a-ref-to-your-component}

Вы можете добавить ссылку в свой компонент, импортировав хук `useRef` из React:

```js
import { useRef } from 'react';
```

Внутри вашего компонента вызовите хук `useRef` и в качестве единственного аргумента передайте начальное значение, на которое вы хотите сослаться. Например, вот ссылка на значение `0`:

```js
const ref = useRef(0);
```

`useRef` возвращает объект, подобный этому:

```js
{
    current: 0; // The value you passed to useRef
}
```

![Представление current из ref.](referencing-values-with-refs-0.png)

Вы можете получить доступ к текущему значению этой ссылки через свойство `ref.current`. Это значение намеренно мутабельно, то есть вы можете как читать, так и писать в него. Это как секретный карман вашего компонента, который React не отслеживает. (Именно это делает его "аварийным люком" из одностороннего потока данных React - подробнее об этом ниже\!)

Здесь кнопка будет увеличивать `ref.current` при каждом нажатии:

=== "App.js"

    ```js
    import { useRef } from 'react';

    export default function Counter() {
    	let ref = useRef(0);

    	function handleClick() {
    		ref.current = ref.current + 1;
    		alert('You clicked ' + ref.current + ' times!');
    	}

    	return <button onClick={handleClick}>Click me!</button>;
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/vzfntc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Ссылка указывает на число, но, как и [state](state-a-components-memory.md), вы можете указать на что угодно: строку, объект или даже функцию. В отличие от state, ref - это обычный объект JavaScript со свойством `current`, который можно читать и изменять.

Обратите внимание, что **компонент не перерисовывается при каждом увеличении.** Как и state, refs сохраняется React между перерисовками. Однако, установка состояния перерисовывает компонент. Изменение ссылки не делает этого!

## Пример: создание секундомера {#example-building-a-stopwatch}

Вы можете комбинировать ссылки и состояние в одном компоненте. Например, давайте сделаем секундомер, который пользователь может запустить или остановить нажатием кнопки. Чтобы отобразить, сколько времени прошло с момента нажатия пользователем кнопки "Start", вам нужно будет отслеживать, когда была нажата кнопка Start и каково текущее время. **Эта информация используется для рендеринга, поэтому вы будете хранить ее в состоянии:**.

```js
const [startTime, setStartTime] = useState(null);
const [now, setNow] = useState(null);
```

Когда пользователь нажмет кнопку "Start", вы будете использовать [`setInterval`](https://developer.mozilla.org/docs/Web/API/setInterval), чтобы обновлять время каждые 10 миллисекунд:

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Stopwatch() {
    	const [startTime, setStartTime] = useState(null);
    	const [now, setNow] = useState(null);

    	function handleStart() {
    		// Start counting.
    		setStartTime(Date.now());
    		setNow(Date.now());

    		setInterval(() => {
    			// Update the current time every 10ms.
    			setNow(Date.now());
    		}, 10);
    	}

    	let secondsPassed = 0;
    	if (startTime != null && now != null) {
    		secondsPassed = (now - startTime) / 1000;
    	}

    	return (
    		<>
    			<h1>Time passed: {secondsPassed.toFixed(3)}</h1>
    			<button onClick={handleStart}>Start</button>
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/jsy84p?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Когда нажата кнопка "Stop", необходимо отменить существующий интервал, чтобы он перестал обновлять переменную состояния `now`. Вы можете сделать это, вызвав [`clearInterval`](https://developer.mozilla.org/docs/Web/API/clearInterval), но вам нужно передать ему ID интервала, который ранее был возвращен вызовом `setInterval`, когда пользователь нажал кнопку Start. Вам нужно где-то сохранить ID интервала. **Поскольку ID интервала не используется для рендеринга, вы можете хранить его в ссылке:**

=== "App.js"

    ```js
    import { useState, useRef } from 'react';

    export default function Stopwatch() {
    	const [startTime, setStartTime] = useState(null);
    	const [now, setNow] = useState(null);
    	const intervalRef = useRef(null);

    	function handleStart() {
    		setStartTime(Date.now());
    		setNow(Date.now());

    		clearInterval(intervalRef.current);
    		intervalRef.current = setInterval(() => {
    			setNow(Date.now());
    		}, 10);
    	}

    	function handleStop() {
    		clearInterval(intervalRef.current);
    	}

    	let secondsPassed = 0;
    	if (startTime != null && now != null) {
    		secondsPassed = (now - startTime) / 1000;
    	}

    	return (
    		<>
    			<h1>Time passed: {secondsPassed.toFixed(3)}</h1>
    			<button onClick={handleStart}>Start</button>
    			<button onClick={handleStop}>Stop</button>
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/fk7wvx?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Если часть информации используется для рендеринга, храните ее в состоянии. Если часть информации нужна только обработчикам событий и ее изменение не требует повторного рендеринга, использование ссылки может быть более эффективным.

## Различия между refs и state {#differences-between-refs-and-state}

Возможно, вы думаете, что ссылки кажутся менее "строгими", чем `state` - например, вы можете мутировать их вместо того, чтобы всегда использовать функцию установки состояния. Но в большинстве случаев вы захотите использовать `state`. Рефы - это "аварийный люк", который вам не часто понадобится. Вот как сравниваются `state` и `refs`:

| refs                                                                                 | state                                                                                                                                                      |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `useRef(initialValue)` возвращает `{ current: initialValue }`                        | `useState(initialValue)` возвращает текущее значение переменной состояния и функцию-установщик состояния ( `[value, setValue]`)                            |
| Не запускает повторный рендеринг при изменении.                                      | Срабатывает повторный рендеринг при изменении.                                                                                                             |
| Mutable - вы можете изменять и обновлять значение `current` вне процесса рендеринга. | Immutable - вы должны использовать функцию установки состояния для изменения состояния, чтобы поставить в очередь на повторный рендеринг.                  |
| Вы не должны читать (или записывать) значение `current` во время рендеринга.         | Вы можете читать состояние в любое время. Однако каждый рендер имеет свой собственный [snapshot](state-as-a-snapshot.md) состояния, которое не изменяется. |

Вот кнопка счетчика, которая реализована с использованием состояния:

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Counter() {
    	const [count, setCount] = useState(0);

    	function handleClick() {
    		setCount(count + 1);
    	}

    	return (
    		<button onClick={handleClick}>
    			You clicked {count} times
    		</button>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/wwk4tc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Поскольку значение `count` отображается, имеет смысл использовать для него значение состояния. Когда значение счетчика устанавливается с помощью `setCount()`, React перерисовывает компонент, и экран обновляется, чтобы отразить новый счетчик.

Если бы вы попытались реализовать это с помощью ссылки, React никогда бы не перерисовал компонент, и вы бы никогда не увидели изменения счетчика! Посмотрите, как нажатие на эту кнопку **не обновляет ее текст**:

=== "App.js"

    ```js
    import { useRef } from 'react';

    export default function Counter() {
    	let countRef = useRef(0);

    	function handleClick() {
    		// This doesn't re-render the component!
    		countRef.current = countRef.current + 1;
    	}

    	return (
    		<button onClick={handleClick}>
    			You clicked {countRef.current} times
    		</button>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/2sn3k9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вот почему чтение `ref.current` во время рендеринга приводит к ненадежному коду. Если вам это нужно, используйте вместо этого state.

!!!note "Как useRef работает внутри?"

    Хотя и `useState` и `useRef` предоставляются React, в принципе `useRef` может быть реализован _поверх_ `useState`. Вы можете представить, что внутри React `useRef` реализован следующим образом:

    ```js
    // Inside of React
    function useRef(initialValue) {
    	const [ref, unused] = useState({
    		current: initialValue,
    	});
    	return ref;
    }
    ```

    Во время первого рендеринга `useRef` возвращает `{ current: initialValue }`. Этот объект хранится в памяти React, поэтому при следующем рендере будет возвращен тот же объект. Обратите внимание, что в этом примере сеттер состояния не используется. Он не нужен, потому что `useRef` всегда должен возвращать один и тот же объект!

    React предоставляет встроенную версию `useRef`, потому что это достаточно часто встречается на практике. Но вы можете думать о ней как об обычной переменной состояния без сеттера. Если вы знакомы с объектно-ориентированным программированием, refs может напомнить вам поля экземпляра, но вместо `this.something` вы напишите `somethingRef.current`.

## Когда использовать refs {#when-to-use-refs}

Как правило, вы используете refs, когда вашему компоненту нужно "выйти за пределы" React и взаимодействовать с внешними API - часто с API браузера, которые не влияют на внешний вид компонента. Вот несколько таких редких ситуаций:

-   Хранение [идентификаторов таймаута](https://developer.mozilla.org/docs/Web/API/setTimeout)
-   Хранение и манипулирование [элементами DOM](https://developer.mozilla.org/docs/Web/API/Element), о чем мы расскажем на [следующей странице](manipulating-the-dom-with-refs.md)
-   Хранение других объектов, которые не нужны для вычисления JSX.

Если вашему компоненту нужно хранить какое-то значение, но оно не влияет на логику рендеринга, выбирайте refs.

## Лучшие практики для refs {#best-practices-for-refs}

Следование этим принципам сделает ваши компоненты более предсказуемыми:

-   **Рассматривайте ссылки как аварийный люк.** Ссылки полезны, когда вы работаете с внешними системами или API браузера. Если большая часть логики вашего приложения и потока данных зависит от ссылок, возможно, вам стоит пересмотреть свой подход.
-   **Не читайте и не записывайте `ref.current` во время рендеринга.** Если какая-то информация необходима во время рендеринга, используйте [state](state-a-components-memory.md) вместо этого. Поскольку React не знает, когда изменяется `ref.current`, даже чтение его во время рендеринга делает поведение вашего компонента труднопредсказуемым. (Единственным исключением из этого является код типа `if (!ref.current) ref.current = new Thing()`, который устанавливает ссылку только один раз во время первого рендеринга).

Ограничения React state не распространяются на рефлексы. Например, состояние действует как [снимок для каждого рендера](state-as-a-snapshot.md) и [не обновляется синхронно](queueing-a-series-of-state-updates.md) Но когда вы изменяете текущее значение ссылки, оно немедленно меняется:

```js
ref.current = 5;
console.log(ref.current); // 5
```

Это происходит потому, что **ссылка сама по себе является обычным объектом JavaScript,** и поэтому ведет себя как обычный объект.

Вам также не нужно беспокоиться о [избегании мутации](updating-objects-in-state.md), когда вы работаете с ref. До тех пор, пока объект, который вы мутируете, не используется для рендеринга, React не волнует, что вы делаете с рефлексом или его содержимым.

## Ссылки и DOM {#refs-and-the-dom}

Вы можете указать ссылку на любое значение. Однако наиболее часто ссылка используется для доступа к элементу DOM. Например, это удобно, если вы хотите программно сфокусировать вход. Когда вы передаете ссылку в атрибут `ref` в JSX, например `<div ref={myRef}>`, React помещает соответствующий элемент DOM в `myRef.current`. Подробнее об этом вы можете прочитать в [Manipulating the DOM with Refs.](manipulating-the-dom-with-refs.md).

!!!tip "Итоги"

    -   Ссылки - это люк для хранения значений, которые не используются для рендеринга. Они нечасто вам понадобятся.
    -   Ссылка - это обычный объект JavaScript с единственным свойством `current`, которое вы можете прочитать или установить.
    -   Вы можете попросить React дать вам ссылку, вызвав хук `useRef`.
    -   Как и состояние, ссылки позволяют сохранять информацию между повторными рендерингами компонента.
    -   В отличие от состояния, установка `текущего` значения ссылки не вызывает повторного рендеринга.
    -   Не читайте и не записывайте `ref.current` во время рендеринга. Это сделает ваш компонент трудно предсказуемым.

## Задачи {#challenges}

### 1. Исправление неработающего входа в чат {#fix-a-broken-chat-input}

Введите сообщение и нажмите "Отправить". Вы заметите, что перед появлением сообщения "Отправлено!" произойдет трехсекундная задержка. Во время этой задержки вы увидите кнопку "Отменить". Нажмите на нее. Эта кнопка "Отменить" должна остановить появление сообщения "Отправлено!". Она делает это, вызывая [`clearTimeout`](https://developer.mozilla.org/docs/Web/API/clearTimeout) для идентификатора таймаута, сохраненного во время `handleSend`. Однако даже после нажатия кнопки "Undo" сообщение "Sent!" все равно появляется. Найдите причину неработоспособности и устраните ее.

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Chat() {
    	const [text, setText] = useState('');
    	const [isSending, setIsSending] = useState(false);
    	let timeoutID = null;

    	function handleSend() {
    		setIsSending(true);
    		timeoutID = setTimeout(() => {
    			alert('Sent!');
    			setIsSending(false);
    		}, 3000);
    	}

    	function handleUndo() {
    		setIsSending(false);
    		clearTimeout(timeoutID);
    	}

    	return (
    		<>
    			<input
    				disabled={isSending}
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button
    				disabled={isSending}
    				onClick={handleSend}
    			>
    				{isSending ? 'Sending...' : 'Send'}
    			</button>
    			{isSending && (
    				<button onClick={handleUndo}>Undo</button>
    			)}
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/x4mdcl?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Обычные переменные, такие как `let timeoutID`, не "выживают" между повторными рендерами, потому что каждый рендер запускает ваш компонент (и инициализирует его переменные) с нуля. Должны ли вы хранить идентификатор таймаута в другом месте?

???success "Показать решение"

    Всякий раз, когда ваш компонент перестраивается (например, при установке состояния), все локальные переменные инициализируются с нуля. Вот почему вы не можете сохранить идентификатор таймаута в локальной переменной типа `timeoutID`, а затем ожидать, что другой обработчик событий "увидит" его в будущем. Вместо этого сохраните его в ссылке, которую React будет сохранять между рендерами.

    === "App.js"

    	```js
    	import { useState, useRef } from 'react';

    	export default function Chat() {
    		const [text, setText] = useState('');
    		const [isSending, setIsSending] = useState(false);
    		const timeoutRef = useRef(null);

    		function handleSend() {
    			setIsSending(true);
    			timeoutRef.current = setTimeout(() => {
    				alert('Sent!');
    				setIsSending(false);
    			}, 3000);
    		}

    		function handleUndo() {
    			setIsSending(false);
    			clearTimeout(timeoutRef.current);
    		}

    		return (
    			<>
    				<input
    					disabled={isSending}
    					value={text}
    					onChange={(e) => setText(e.target.value)}
    				/>
    				<button
    					disabled={isSending}
    					onClick={handleSend}
    				>
    					{isSending ? 'Sending...' : 'Send'}
    				</button>
    				{isSending && (
    					<button onClick={handleUndo}>Undo</button>
    				)}
    			</>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/9sp2f9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 2. Исправьте компонент, который не смог перерисоваться {#fix-a-component-failing-to-re-render}

Эта кнопка должна переключаться между отображением "Вкл" и "Выкл". Однако она всегда показывает "Выключено". Что не так с этим кодом? Исправьте это.

=== "App.js"

    ```js
    import { useRef } from 'react';

    export default function Toggle() {
    	const isOnRef = useRef(false);

    	return (
    		<button
    			onClick={() => {
    				isOnRef.current = !isOnRef.current;
    			}}
    		>
    			{isOnRef.current ? 'On' : 'Off'}
    		</button>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/qgpkmc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    В этом примере текущее значение ссылки используется для расчета вывода рендеринга: `{isOnRef.current ? 'On' : 'Off'}`. Это признак того, что данная информация не должна быть в ссылке, а должна быть помещена в состояние. Чтобы исправить это, удалите ссылку и используйте вместо нее state:

    === "App.js"

    	```js
    	import { useState } from 'react';

    	export default function Toggle() {
    		const [isOn, setIsOn] = useState(false);

    		return (
    			<button
    				onClick={() => {
    					setIsOn(!isOn);
    				}}
    			>
    				{isOn ? 'On' : 'Off'}
    			</button>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/sd8nzf?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 3. Исправление debounce {#fix-debouncing}

В этом примере все обработчики нажатия на кнопку ["debounced"](https://redd.one/blog/debounce-vs-throttle). Чтобы увидеть, что это значит, нажмите на одну из кнопок. Обратите внимание, что через секунду появится сообщение. Если вы нажмете кнопку в ожидании сообщения, таймер сбросится. Таким образом, если вы будете нажимать одну и ту же кнопку много раз, сообщение появится только через секунду после того, как вы перестанете нажимать. Дебаунсинг позволяет отложить выполнение какого-либо действия до тех пор, пока пользователь не "перестанет делать что-то".

Этот пример работает, но не совсем так, как было задумано. Кнопки не являются независимыми. Чтобы увидеть проблему, нажмите на одну из кнопок, а затем сразу же нажмите на другую. Можно было бы ожидать, что после задержки вы увидите сообщения обеих кнопок. Но отображается только сообщение последней кнопки. Сообщение первой кнопки теряется.

Почему кнопки мешают друг другу? Найдите и устраните проблему.

=== "App.js"

    ```js
    let timeoutID;

    function DebouncedButton({ onClick, children }) {
    	return (
    		<button
    			onClick={() => {
    				clearTimeout(timeoutID);
    				timeoutID = setTimeout(() => {
    					onClick();
    				}, 1000);
    			}}
    		>
    			{children}
    		</button>
    	);
    }

    export default function Dashboard() {
    	return (
    		<>
    			<DebouncedButton
    				onClick={() => alert('Spaceship launched!')}
    			>
    				Launch the spaceship
    			</DebouncedButton>
    			<DebouncedButton
    				onClick={() => alert('Soup boiled!')}
    			>
    				Boil the soup
    			</DebouncedButton>
    			<DebouncedButton
    				onClick={() => alert('Lullaby sung!')}
    			>
    				Sing a lullaby
    			</DebouncedButton>
    		</>
    	);
    }
    ```

=== "Решение"

    <iframe src="https://codesandbox.io/embed/8zdcgn?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Переменная ID последнего таймаута является общей для всех компонентов `DebouncedButton`. Вот почему нажатие на одну кнопку сбрасывает таймаут другой кнопки. Можете ли вы хранить отдельный ID таймаута для каждой кнопки?

???success "Показать решение"

    Такая переменная, как `timeoutID`, является общей для всех компонентов. Вот почему нажатие на вторую кнопку сбрасывает таймаут первой кнопки. Чтобы исправить это, вы можете хранить таймаут в ссылке. Каждая кнопка получит свой собственный ref, поэтому они не будут конфликтовать друг с другом. Обратите внимание, что при быстром нажатии на две кнопки отображаются оба сообщения.

    === "App.js"

    	```js
    	import { useRef } from 'react';

    	function DebouncedButton({ onClick, children }) {
    		const timeoutRef = useRef(null);
    		return (
    			<button
    				onClick={() => {
    					clearTimeout(timeoutRef.current);
    					timeoutRef.current = setTimeout(() => {
    						onClick();
    					}, 1000);
    				}}
    			>
    				{children}
    			</button>
    		);
    	}

    	export default function Dashboard() {
    		return (
    			<>
    				<DebouncedButton
    					onClick={() => alert('Spaceship launched!')}
    				>
    					Launch the spaceship
    				</DebouncedButton>
    				<DebouncedButton
    					onClick={() => alert('Soup boiled!')}
    				>
    					Boil the soup
    				</DebouncedButton>
    				<DebouncedButton
    					onClick={() => alert('Lullaby sung!')}
    				>
    					Sing a lullaby
    				</DebouncedButton>
    			</>
    		);
    	}
    	```

    === "Решение"

    	<iframe src="https://codesandbox.io/embed/pwg2dx?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 4. Прочитать последнее состояние {#read-the-latest-state}

В этом примере после нажатия кнопки "Отправить" происходит небольшая задержка перед отображением сообщения. Введите "hello", нажмите "Отправить", а затем быстро отредактируйте ввод снова. Несмотря на ваши правки, оповещение все равно покажет "hello" (это было значение state [на момент](state-as-a-snapshot.md) нажатия кнопки).

Обычно такое поведение - это то, что вы хотите видеть в приложении. Однако иногда могут возникнуть ситуации, когда вы хотите, чтобы асинхронный код считывал _последнюю_ версию некоторого состояния. Можете ли вы придумать, как сделать так, чтобы оповещение показывало _текущий_ текст ввода, а не тот, что был в момент нажатия?

=== "App.js"

    ```js
    import { useState, useRef } from 'react';

    export default function Chat() {
    	const [text, setText] = useState('');

    	function handleSend() {
    		setTimeout(() => {
    			alert('Sending: ' + text);
    		}, 3000);
    	}

    	return (
    		<>
    			<input
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button onClick={handleSend}>Send</button>
    		</>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/hxlfx9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение"

    Состояние работает [как моментальный снимок](state-as-a-snapshot.md), поэтому вы не можете прочитать последнее состояние из асинхронной операции, такой как таймаут. Однако вы можете сохранить последний введенный текст в ссылке. Ссылка является изменяемой, поэтому вы можете прочитать свойство `current` в любое время. Поскольку текущий текст также используется для рендеринга, в этом примере вам понадобится _и_ переменная состояния (для рендеринга), _и_ ссылка (чтобы прочитать ее в таймауте). Вам нужно будет обновить текущее значение ref вручную.

    === "App.js"

    	```js
    	import { useState, useRef } from 'react';

    	export default function Chat() {
    		const [text, setText] = useState('');
    		const textRef = useRef(text);

    		function handleChange(e) {
    			setText(e.target.value);
    			textRef.current = e.target.value;
    		}

    		function handleSend() {
    			setTimeout(() => {
    				alert('Sending: ' + textRef.current);
    			}, 3000);
    		}

    		return (
    			<>
    				<input value={text} onChange={handleChange} />
    				<button onClick={handleSend}>Send</button>
    			</>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/cjk6lf?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/referencing-values-with-refs](https://react.dev/learn/referencing-values-with-refs)</small>
