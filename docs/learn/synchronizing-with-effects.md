---
description: Эффекты позволяют выполнить некоторый код после рендеринга, чтобы вы могли синхронизировать свой компонент с какой-либо системой вне React
---

# Синхронизация с эффектами

<big>Некоторые компоненты нуждаются в синхронизации с внешними системами. Например, вы можете захотеть управлять компонентом, не относящимся к React, на основе состояния React, установить соединение с сервером или отправлять журнал аналитики, когда компонент появляется на экране. **Эффекты** позволяют выполнить некоторый код после рендеринга, чтобы вы могли синхронизировать свой компонент с какой-либо системой вне React.</big>

!!!tip "Вы узнаете"

    -   Что такое эффекты
    -   Чем эффекты отличаются от событий
    -   Как объявить эффект в своем компоненте
    -   Как избежать повторного запуска эффекта без необходимости
    -   Почему эффекты запускаются дважды в процессе разработки и как это исправить

## Что такое эффекты и чем они отличаются от событий? {#what-are-effects-and-how-are-they-different-from-events}

Прежде чем перейти к эффектам, вам необходимо ознакомиться с двумя типами логики внутри компонентов React:

-   **Код рендеринга** (представленный в [Разработка интерфейса](describing-the-ui.md)) находится на верхнем уровне вашего компонента. Именно здесь вы берете пропсы и состояние, преобразуете их и возвращаете JSX, который вы хотите видеть на экране. [Код рендеринга должен быть чистым](keeping-components-pure.md). Подобно математической формуле, он должен только _вычислять_ результат, но не делать ничего другого.

-   **Обработчики событий** (введенные в [Добавление интерактивности](adding-interactivity.md)) - это вложенные функции внутри ваших компонентов, которые _делают_ вещи, а не просто вычисляют их. Обработчик события может обновить поле ввода, отправить HTTP POST-запрос для покупки товара или перевести пользователя на другой экран. Обработчики событий содержат ["побочные эффекты"](https://en.wikipedia.org/wiki/Side_effect) (они изменяют состояние программы), вызванные определенным действием пользователя (например, нажатием кнопки или набором текста).

Иногда этого недостаточно. Рассмотрим компонент `ChatRoom`, который должен подключаться к серверу чата всякий раз, когда он появляется на экране. Подключение к серверу не является чистым вычислением (это побочный эффект), поэтому оно не может происходить во время рендеринга. Однако не существует какого-то конкретного события, например, щелчка мыши, которое вызывает отображение `ChatRoom`.

**_Эффекты_ позволяют указать побочные эффекты, которые вызваны самим рендерингом, а не конкретным событием.** Отправка сообщения в чат - это _событие_, потому что оно непосредственно вызвано нажатием пользователем определенной кнопки. Однако установка соединения с сервером - это _эффект_, потому что он должен произойти независимо от того, какое взаимодействие вызвало появление компонента. Эффекты запускаются в конце [фазы коммита](render-and-commit.md) после обновления экрана. Это подходящее время для синхронизации компонентов React с какой-либо внешней системой (например, сетью или сторонней библиотекой).

!!!note ""

    Здесь и далее в этом тексте "Эффект" с заглавной буквы относится к специфическому для React определению, приведенному выше, т.е. побочный эффект, вызванный рендерингом. Для обозначения более широкого понятия программирования мы будем говорить "побочный эффект".

## Возможно, вам не нужен эффект {#you-might-not-need-an-effect}

**Не спешите добавлять эффекты в свои компоненты.** Помните, что эффекты обычно используются для того, чтобы "выйти" из кода React и синхронизироваться с какой-либо внешней системой. Сюда входят API браузера, сторонние виджеты, сеть и так далее. Если ваш эффект только корректирует одно состояние на основе другого состояния, возможно, [вам не нужен эффект](you-might-not-need-an-effect.md).

## Как написать эффект {#how-to-write-an-effect}

Чтобы написать эффект, выполните следующие три шага:

1.  **Объявите эффект.** По умолчанию ваш эффект будет запускаться после каждого рендеринга.
2.  **Укажите зависимости эффекта.** Большинство эффектов должны запускаться только _по мере необходимости_, а не после каждого рендера. Например, анимация затухания должна запускаться только при появлении компонента. Подключение и отключение к чату должно происходить только при появлении и исчезновении компонента или при изменении чата. Вы узнаете, как управлять этим, указывая _зависимости_.
3.  **Добавьте очистку при необходимости.** Некоторым эффектам необходимо указать, как остановить, отменить или очистить то, что они делали. Например, "connect" требует "disconnect", "subscribe" требует "unsubscribe", а "fetch" требует либо "cancel", либо "ignore". Вы узнаете, как это сделать, вернув функцию _cleanup function_.

Давайте рассмотрим каждый из этих шагов подробно.

### Шаг 1: Объявление эффекта {#step-1-declare-an-effect}

Чтобы объявить эффект в своем компоненте, импортируйте [`useEffect` Hook](../reference/react/useEffect.md) из React:

```js
import { useEffect } from 'react';
```

Затем вызовите его на верхнем уровне вашего компонента и поместите некоторый код внутри Effect:

```js hl_lines="2-4"
function MyComponent() {
    useEffect(() => {
        // Code here will run after *every* render
    });
    return <div />;
}
```

Каждый раз при рендеринге вашего компонента React будет обновлять экран _а затем_ запускать код внутри `useEffect`. Другими словами, **`useEffect` "откладывает" выполнение части кода до тех пор, пока рендеринг не будет отражен на экране.**.

Давайте посмотрим, как можно использовать эффект для синхронизации с внешней системой. Рассмотрим компонент `<VideoPlayer>` React. Было бы неплохо контролировать, играет ли он или приостановлен, передавая ему параметр `isPlaying`:

```js
<VideoPlayer isPlaying={isPlaying} />
```

Ваш пользовательский компонент `VideoPlayer` отображает встроенный тег браузера [`<video>`](https://developer.mozilla.org/docs/Web/HTML/Element/video):

```js
function VideoPlayer({ src, isPlaying }) {
    // TODO: do something with isPlaying
    return <video src={src} />;
}
```

Однако тег браузера `<video>` не имеет свойства `isPlaying`. Единственный способ управлять им - вручную вызвать методы [`play()`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/play) и [`pause()`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/pause) на элементе DOM. **Вам нужно синхронизировать значение параметра `isPlaying`, который говорит о том, должно ли видео _в данный момент_ проигрываться, с вызовами `play()` и `pause()`.**

Сначала нам нужно [получить ссылку](manipulating-the-dom-with-refs.md) на DOM-узел `<video>`.

У вас может возникнуть соблазн попытаться вызвать `play()` или `pause()` во время рендеринга, но это неправильно:

=== "App.js"

    ```js
    import { useState, useRef, useEffect } from 'react';

    function VideoPlayer({ src, isPlaying }) {
    	const ref = useRef(null);

    	if (isPlaying) {
    		ref.current.play(); // Calling these while rendering isn't allowed.
    	} else {
    		ref.current.pause(); // Also, this crashes.
    	}

    	return <video ref={ref} src={src} loop playsInline />;
    }

    export default function App() {
    	const [isPlaying, setIsPlaying] = useState(false);
    	return (
    		<>
    			<button
    				onClick={() => setIsPlaying(!isPlaying)}
    			>
    				{isPlaying ? 'Pause' : 'Play'}
    			</button>
    			<VideoPlayer
    				isPlaying={isPlaying}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/48skyx?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Причина некорректности этого кода в том, что он пытается что-то сделать с узлом DOM во время рендеринга. В React, [рендеринг должен быть чистым вычислением](keeping-components-pure.md) JSX и не должен содержать побочных эффектов, таких как изменение DOM.

Более того, когда `VideoPlayer` вызывается в первый раз, его DOM еще не существует! Еще нет узла DOM для вызова `play()` или `pause()`, потому что React не знает, какой DOM создавать, пока вы не вернете JSX.

Решением здесь является **обернуть побочный эффект с помощью `useEffect`, чтобы переместить его из расчета рендеринга:**

```js hl_lines="6 12"
import { useEffect, useRef } from 'react';

function VideoPlayer({ src, isPlaying }) {
    const ref = useRef(null);

    useEffect(() => {
        if (isPlaying) {
            ref.current.play();
        } else {
            ref.current.pause();
        }
    });

    return <video ref={ref} src={src} loop playsInline />;
}
```

Обернув обновление DOM в Эффект, вы позволяете React сначала обновить экран. Затем запускается ваш Эффект.

Когда ваш компонент `VideoPlayer` отобразится (в первый раз или при повторном рендеринге), произойдет несколько вещей. Во-первых, React обновит экран, убедившись, что тег `<video>` находится в DOM с нужными пропсами. Затем React запустит ваш Эффект. Наконец, ваш Эффект вызовет `play()` или `pause()` в зависимости от значения `isPlaying`.

Нажмите Play/Pause несколько раз и посмотрите, как видеоплеер синхронизируется со значением `isPlaying`:

=== "App.js"

    ```js
    import { useState, useRef, useEffect } from 'react';

    function VideoPlayer({ src, isPlaying }) {
    	const ref = useRef(null);

    	useEffect(() => {
    		if (isPlaying) {
    			ref.current.play();
    		} else {
    			ref.current.pause();
    		}
    	});

    	return <video ref={ref} src={src} loop playsInline />;
    }

    export default function App() {
    	const [isPlaying, setIsPlaying] = useState(false);
    	return (
    		<>
    			<button
    				onClick={() => setIsPlaying(!isPlaying)}
    			>
    				{isPlaying ? 'Pause' : 'Play'}
    			</button>
    			<VideoPlayer
    				isPlaying={isPlaying}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/lgq8k9?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В этом примере "внешней системой", которую вы синхронизировали с состоянием React, был медиа API браузера. Вы можете использовать аналогичный подход, чтобы обернуть унаследованный не-React код (например, плагины jQuery) в декларативные компоненты React.

Обратите внимание, что управление видеоплеером на практике гораздо сложнее. Вызов `play()` может не сработать, пользователь может включить или приостановить воспроизведение, используя встроенные элементы управления браузера, и так далее. Этот пример является очень упрощенным и неполным.

!!!warning "Внимание"

    По умолчанию Effects запускаются после _каждого_ рендера. Вот почему код, подобный этому, **произведет бесконечный цикл:**.

    ```js
    const [count, setCount] = useState(0);
    useEffect(() => {
    	setCount(count + 1);
    });
    ```

    Эффекты запускаются как _результат_ рендеринга. Установка состояния _триггерирует_ рендеринг. Установить состояние сразу в Эффекте - это все равно что включить розетку в розетку. Эффект запускается, он устанавливает состояние, что вызывает повторный рендеринг, который заставляет Эффект запуститься, он снова устанавливает состояние, что вызывает еще один повторный рендеринг, и так далее.

    Эффекты обычно должны синхронизировать ваши компоненты с _внешней_ системой. Если внешней системы нет, и вы хотите только корректировать одно состояние на основе другого состояния, [возможно, вам не нужен Эффект](you-might-not-need-an-effect.md).

### Шаг 2: Укажите зависимости Эффекта {#step-2-specify-the-effect-dependencies}

По умолчанию эффекты запускаются после _каждого_ рендера. Часто это **не то, что вам нужно:**.

-   Иногда это медленно. Синхронизация с внешней системой не всегда происходит мгновенно, поэтому вы можете не делать этого, если это не необходимо. Например, вы не хотите переподключаться к серверу чата при каждом нажатии клавиши.
-   Иногда это неправильно. Например, вы не хотите запускать анимацию затухания компонента при каждом нажатии клавиши. Анимация должна срабатывать только один раз, когда компонент появляется впервые.

Чтобы продемонстрировать проблему, вот предыдущий пример с несколькими вызовами `console.log` и текстовым вводом, который обновляет состояние родительского компонента. Обратите внимание, как ввод текста приводит к повторному запуску эффекта:

=== "App.js"

    ```js
    import { useState, useRef, useEffect } from 'react';

    function VideoPlayer({ src, isPlaying }) {
    	const ref = useRef(null);

    	useEffect(() => {
    		if (isPlaying) {
    			console.log('Calling video.play()');
    			ref.current.play();
    		} else {
    			console.log('Calling video.pause()');
    			ref.current.pause();
    		}
    	});

    	return <video ref={ref} src={src} loop playsInline />;
    }

    export default function App() {
    	const [isPlaying, setIsPlaying] = useState(false);
    	const [text, setText] = useState('');
    	return (
    		<>
    			<input
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button
    				onClick={() => setIsPlaying(!isPlaying)}
    			>
    				{isPlaying ? 'Pause' : 'Play'}
    			</button>
    			<VideoPlayer
    				isPlaying={isPlaying}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/x6qj7f?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Вы можете попросить React **пропустить ненужный повторный запуск эффекта**, указав массив _зависимостей_ в качестве второго аргумента вызова `useEffect`. Начните с добавления пустого массива `[]` в приведенный выше пример:

```js hl_lines="3"
useEffect(() => {
    // ...
}, []);
```

Вы должны увидеть ошибку `React Hook useEffect has a missing dependency: 'isPlaying'`:

=== "App.js"

    ```js
    import { useState, useRef, useEffect } from 'react';

    function VideoPlayer({ src, isPlaying }) {
    	const ref = useRef(null);

    	useEffect(() => {
    		if (isPlaying) {
    			console.log('Calling video.play()');
    			ref.current.play();
    		} else {
    			console.log('Calling video.pause()');
    			ref.current.pause();
    		}
    	}, []); // This causes an error

    	return <video ref={ref} src={src} loop playsInline />;
    }

    export default function App() {
    	const [isPlaying, setIsPlaying] = useState(false);
    	const [text, setText] = useState('');
    	return (
    		<>
    			<input
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button
    				onClick={() => setIsPlaying(!isPlaying)}
    			>
    				{isPlaying ? 'Pause' : 'Play'}
    			</button>
    			<VideoPlayer
    				isPlaying={isPlaying}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/ldkkcy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Проблема в том, что код внутри вашего Effect _зависит_ от пропса `isPlaying`, чтобы решить, что делать, но эта зависимость не была явно объявлена. Чтобы решить эту проблему, добавьте `isPlaying` в массив зависимостей:

```js hl_lines="2 8"
useEffect(() => {
    if (isPlaying) {
        // It's used here...
        // ...
    } else {
        // ...
    }
}, [isPlaying]); // ...so it must be declared here!
```

Теперь все зависимости объявлены, поэтому ошибки нет. Указание `[isPlaying]` в качестве массива зависимостей говорит React, что он должен пропустить повторный запуск вашего Эффекта, если `isPlaying` будет таким же, как и во время предыдущего рендеринга. С этим изменением ввод текста в поле ввода не приводит к повторному запуску эффекта, но нажатие кнопки Play/Pause приводит к повторному запуску:

=== "App.js"

    ```js
    import { useState, useRef, useEffect } from 'react';

    function VideoPlayer({ src, isPlaying }) {
    	const ref = useRef(null);

    	useEffect(() => {
    		if (isPlaying) {
    			console.log('Calling video.play()');
    			ref.current.play();
    		} else {
    			console.log('Calling video.pause()');
    			ref.current.pause();
    		}
    	}, [isPlaying]);

    	return <video ref={ref} src={src} loop playsInline />;
    }

    export default function App() {
    	const [isPlaying, setIsPlaying] = useState(false);
    	const [text, setText] = useState('');
    	return (
    		<>
    			<input
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button
    				onClick={() => setIsPlaying(!isPlaying)}
    			>
    				{isPlaying ? 'Pause' : 'Play'}
    			</button>
    			<VideoPlayer
    				isPlaying={isPlaying}
    				src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    			/>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/ymdqrc?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Массив зависимостей может содержать несколько зависимостей. React пропустит повторное выполнение Эффекта только в том случае, если _все_ указанные вами зависимости имеют точно такие же значения, как и во время предыдущего рендеринга. React сравнивает значения зависимостей, используя сравнение [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Подробности смотрите в справке [`useEffect`](../reference/react/useEffect.md).

**Обратите внимание, что вы не можете "выбирать" свои зависимости.** Вы получите ошибку lint, если указанные вами зависимости не соответствуют тому, что ожидает React на основе кода внутри вашего Effect. Это поможет отловить множество ошибок в вашем коде. Если вы не хотите, чтобы какой-то код выполнялся повторно, [_отредактируйте код самого Эффекта_, чтобы он не нуждался в этой зависимости](lifecycle-of-reactive-effects.md).

!!!warning ""

    Поведение без массива зависимостей и с _пустым_ массивом зависимостей `[]` отличается:

    ```js hl_lines="3 7 12"
    useEffect(() => {
    	// This runs after every render
    });

    useEffect(() => {
    	// This runs only on mount (when the component appears)
    }, []);

    useEffect(() => {
    	// This runs on mount *and also*
    	// if either a or b have changed since the last render
    }, [a, b]);
    ```

    Мы подробно рассмотрим, что означает "mount" в следующем шаге.

!!!note "Почему ссылка была исключена из массива зависимостей?"

    Этот Эффект использует и `ref`, и `isPlaying`, но только `isPlaying` объявлен как зависимость:

    ```js hl_lines="9"
    function VideoPlayer({ src, isPlaying }) {
    const ref = useRef(null);
    useEffect(() => {
    	if (isPlaying) {
    	ref.current.play();
    	} else {
    	ref.current.pause();
    	}
    }, [isPlaying]);
    ```

    Это происходит потому, что объект `ref` имеет _стабильную идентичность:_ React гарантирует [вы всегда будете получать один и тот же объект](../reference/react/useRef.md) от одного и того же вызова `useRef` при каждом рендере. Он никогда не меняется, поэтому сам по себе никогда не вызовет повторного запуска Эффекта. Поэтому не имеет значения, включаете вы его или нет. Включение тоже не имеет значения:

    ```js hl_lines="9"
    function VideoPlayer({ src, isPlaying }) {
    const ref = useRef(null);
    useEffect(() => {
    	if (isPlaying) {
    	ref.current.play();
    	} else {
    	ref.current.pause();
    	}
    }, [isPlaying, ref]);
    ```

    Функции [`set`](../reference/react/useState.md), возвращаемые `useState`, также имеют стабильную идентичность, поэтому их часто можно увидеть опущенными из зависимостей. Если линтер позволяет вам опустить зависимость без ошибок, это безопасно.

    Опускание всегда стабильных зависимостей работает только тогда, когда линтер "видит", что объект стабилен. Например, если `ref` передается от родительского компонента, вам придется указать его в массиве зависимостей. Однако, это хорошо, потому что вы не можете знать, всегда ли родительский компонент передает один и тот же ref, или передает один из нескольких ref условно. Таким образом, ваш Effect _будет_ зависеть от того, какая ссылка передается.

### Шаг 3: Добавьте очистку при необходимости {#step-3-add-cleanup-if-needed}

Рассмотрим другой пример. Вы пишете компонент `ChatRoom`, который должен подключаться к серверу чата при его появлении. Вам предоставлен API `createConnection()`, который возвращает объект с методами `connect()` и `disconnect()`. Как сохранить компонент подключенным, пока он отображается пользователю?

Начните с написания логики Effect:

```js
useEffect(() => {
    const connection = createConnection();
    connection.connect();
});
```

Было бы медленно подключаться к чату после каждого повторного рендеринга, поэтому вы добавляете массив зависимостей:

```js hl_lines="4"
useEffect(() => {
    const connection = createConnection();
    connection.connect();
}, []);
```

**Код внутри Effect не использует никаких props или state, поэтому ваш массив зависимостей будет `[]` (пустой). Это говорит React запускать этот код только тогда, когда компонент "монтируется", т.е. появляется на экране в первый раз**.

Давайте попробуем запустить этот код:

=== "App.js"

    ```js
    import { useEffect } from 'react';
    import { createConnection } from './chat.js';

    export default function ChatRoom() {
    	useEffect(() => {
    		const connection = createConnection();
    		connection.connect();
    	}, []);
    	return <h1>Welcome to the chat!</h1>;
    }
    ```

=== "chat.js"

    ```js
    export function createConnection() {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log('✅ Connecting...');
    		},
    		disconnect() {
    			console.log('❌ Disconnected.');
    		},
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/qx7jkr?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Этот Эффект выполняется только при монтировании, поэтому можно ожидать, что `✅ Connecting...` будет выведен в консоль один раз. Однако, если проверить консоль, то `✅ Connecting...` выводится дважды. Почему так происходит?

Представьте, что компонент `ChatRoom` является частью большого приложения с множеством различных экранов. Пользователь начинает свое путешествие со страницы `ChatRoom`. Компонент монтируется и вызывает `connection.connect()`. Затем представьте, что пользователь переходит на другой экран - например, на страницу настроек. Компонент `ChatRoom` размонтируется. Наконец, пользователь нажимает кнопку Back, и `ChatRoom` снова монтируется. Это установит второе соединение - но первое соединение никогда не было разрушено! По мере того как пользователь перемещается по приложению, соединения продолжают накапливаться.

Подобные ошибки легко пропустить без тщательного ручного тестирования. Чтобы помочь вам быстро обнаружить их, в процессе разработки React перемонтирует каждый компонент один раз сразу после его первоначального монтирования.

Дважды увидев журнал `"✅ Connecting..."`, вы сможете заметить реальную проблему: ваш код не закрывает соединение, когда компонент размонтируется.

Чтобы решить эту проблему, верните функцию _cleanup_ из вашего Effect:

```js hl_lines="4-6"
useEffect(() => {
    const connection = createConnection();
    connection.connect();
    return () => {
        connection.disconnect();
    };
}, []);
```

React будет вызывать вашу функцию очистки каждый раз перед повторным запуском Effect и последний раз, когда компонент размонтируется (удаляется). Давайте посмотрим, что произойдет, когда функция очистки будет реализована:

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { createConnection } from './chat.js';

    export default function ChatRoom() {
    	useEffect(() => {
    		const connection = createConnection();
    		connection.connect();
    		return () => connection.disconnect();
    	}, []);
    	return <h1>Welcome to the chat!</h1>;
    }
    ```

=== "chat.js"

    ```js
    export function createConnection() {
    	// A real implementation would actually connect to the server
    	return {
    		connect() {
    			console.log('✅ Connecting...');
    		},
    		disconnect() {
    			console.log('❌ Disconnected.');
    		},
    	};
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dg4vhl?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Теперь в процессе разработки вы получите три консольных журнала:

1.  "✅ Connecting..."
2.  "❌ Disconnected."
3.  "✅ Connecting..."

**Это правильное поведение при разработке.** Перемонтируя ваш компонент, React проверяет, что навигация в сторону и обратно не нарушит ваш код. Отсоединение, а затем повторное присоединение - это именно то, что должно произойти! При хорошей реализации очистки не должно быть никакой видимой пользователю разницы между запуском Эффекта один раз и запуском, очисткой и повторным запуском. Есть дополнительная пара вызовов connect/disconnect, потому что React проверяет ваш код на наличие ошибок в процессе разработки. Это нормально - не пытайтесь заставить его исчезнуть!

**В производстве вы увидите `✅ Connecting...` только один раз.** Перемонтирование компонентов происходит только в процессе разработки, чтобы помочь вам найти эффекты, требующие очистки. Вы можете отключить [Строгий режим](../reference/react/StrictMode.md), чтобы отказаться от такого поведения при разработке, но мы рекомендуем оставить его включенным. Это позволит вам найти множество ошибок, подобных приведенной выше.

## Как обрабатывать эффект, срабатывающий дважды в разработке? {#how-to-handle-the-effect-firing-twice-in-development}

React намеренно перемонтирует ваши компоненты в процессе разработки, чтобы найти ошибки, как в последнем примере. **Правильный вопрос не "как запустить Эффект один раз", а "как исправить мой Эффект, чтобы он работал после перемонтирования "**.

Обычно ответ заключается в реализации функции очистки. Функция очистки должна остановить или отменить все, что делал Эффект. Эмпирическое правило гласит, что пользователь не должен различать однократный запуск Эффекта (как в производстве) и последовательность _установка → очистка → установка_ (как в разработке).

Большинство эффектов, которые вы будете писать, будут соответствовать одному из общих шаблонов, приведенных ниже.

### Управление не-React виджетами {#controlling-non-react-widgets}

Иногда вам нужно добавить виджеты пользовательского интерфейса, которые не написаны на React. Например, допустим, вы добавляете на страницу компонент карты. У него есть метод `setZoomLevel()`, и вы хотите синхронизировать уровень масштабирования с переменной состояния `zoomLevel` в коде React. Ваш Effect будет выглядеть примерно так:

```js
useEffect(() => {
    const map = mapRef.current;
    map.setZoomLevel(zoomLevel);
}, [zoomLevel]);
```

Обратите внимание, что в этом случае не требуется никакой очистки. В процессе разработки React вызовет Effect дважды, но это не проблема, потому что вызов `setZoomLevel` дважды с одним и тем же значением ничего не делает. Это может быть немного медленнее, но это не имеет значения, потому что в продакшене он не будет перемонтироваться без необходимости.

Некоторые API не позволяют вызывать их дважды подряд. Например, метод [`showModal`](https://developer.mozilla.org/docs/Web/API/HTMLDialogElement/showModal) встроенного элемента [`<dialog>`](https://hcdev.ru/html/dialog/) бросается, если вызвать его дважды. Реализуйте функцию очистки и заставьте ее закрыть диалог:

```js hl_lines="4"
useEffect(() => {
    const dialog = dialogRef.current;
    dialog.showModal();
    return () => dialog.close();
}, []);
```

В процессе разработки ваш Effect будет вызывать `showModal()`, затем сразу же `close()`, а затем `showModal()` снова. Это имеет такое же видимое пользователю поведение, как и однократный вызов `showModal()`, как вы увидите в продакшене.

### Подписка на события {#subscribing-to-events}

Если ваш Effect подписался на что-то, функция очистки должна отменить подписку:

```js hl_lines="6-8"
useEffect(() => {
    function handleScroll(e) {
        console.log(window.scrollX, window.scrollY);
    }
    window.addEventListener('scroll', handleScroll);
    return () =>
        window.removeEventListener('scroll', handleScroll);
}, []);
```

При разработке ваш Effect будет вызывать `addEventListener()`, затем сразу же `removeEventListener()`, а затем `addEventListener()` снова с тем же обработчиком. Таким образом, одновременно будет только одна активная подписка. Это имеет такое же видимое пользователю поведение, как и вызов `addEventListener()` один раз, как в продакшене.

### Запуск анимации {#triggering-animations}

Если ваш Эффект что-то анимирует, функция очистки должна сбросить анимацию к начальным значениям:

```js hl_lines="4-6"
useEffect(() => {
    const node = ref.current;
    node.style.opacity = 1; // Trigger the animation
    return () => {
        node.style.opacity = 0; // Reset to the initial value
    };
}, []);
```

В процессе разработки непрозрачность будет установлена на `1`, затем на `0`, а затем снова на `1`. Это должно иметь такое же видимое для пользователя поведение, как и установка значения `1` напрямую, что и будет происходить на производстве. Если вы используете стороннюю библиотеку анимации с поддержкой tweening, ваша функция очистки должна вернуть временную шкалу в исходное состояние.

### Получение данных {#fetching-data}

Если ваш Effect выполняет выборку данных, функция очистки должна либо [прервать выборку](https://developer.mozilla.org/docs/Web/API/AbortController), либо игнорировать ее результат:

```js hl_lines="2 6 13-15"
useEffect(() => {
    let ignore = false;

    async function startFetching() {
        const json = await fetchTodos(userId);
        if (!ignore) {
            setTodos(json);
        }
    }

    startFetching();

    return () => {
        ignore = true;
    };
}, [userId]);
```

Вы не можете "отменить" сетевой запрос, который уже произошел, но ваша функция очистки должна гарантировать, что выборка, которая уже _не актуальна_, не будет продолжать влиять на ваше приложение. Если `userId` меняется с `Alice` на `Bob`, очистка гарантирует, что ответ `Alice` будет проигнорирован, даже если он придет после ответа `Bob`.

**В процессе разработки вы увидите две выборки на вкладке Network.** В этом нет ничего плохого. При вышеописанном подходе первый Effect будет немедленно очищен, поэтому его копия переменной `ignore` будет установлена в `true`. Таким образом, даже если есть дополнительный запрос, он не повлияет на состояние благодаря проверке `if (!ignore)`.

**В производстве будет только один запрос.** Если второй запрос в разработке беспокоит вас, лучше всего использовать решение, которое дедуплицирует запросы и кэширует их ответы между компонентами:

```js
function TodoList() {
    const todos = useSomeDataLibrary(
        `/api/user/${userId}/todos`
    );
    // ...
}
```

Это не только улучшит опыт разработки, но и сделает ваше приложение более быстрым. Например, пользователю, нажавшему кнопку "Назад", не придется ждать, пока некоторые данные снова загрузятся, потому что они будут кэшированы. Вы можете либо создать такой кэш самостоятельно, либо использовать одну из многочисленных альтернатив ручной выборки данных в Effects.

!!!note "Какие существуют альтернативы ручной выборке данных в Effects?"

    Написание вызовов `fetch` внутри Effects является [популярным способом получения данных](https://www.robinwieruch.de/react-hooks-fetch-data/), особенно в полностью клиентских приложениях. Однако это очень ручной подход, и у него есть существенные недостатки:

    -   **Эффекты не запускаются на сервере.** Это означает, что первоначальный HTML, отрисованный на сервере, будет содержать только состояние загрузки без каких-либо данных. Клиентский компьютер должен будет загрузить весь JavaScript и отобразить ваше приложение только для того, чтобы обнаружить, что теперь ему нужно загрузить данные. Это не очень эффективно.
    -   **Получение данных непосредственно в Effects позволяет легко создавать "сетевые водопады".** Вы рендерите родительский компонент, он получает некоторые данные, рендерит дочерние компоненты, а затем они начинают получать свои данные. Если сеть не очень быстрая, это значительно медленнее, чем параллельная выборка всех данных.
    -   Например, если компонент размонтируется, а затем снова монтируется, ему придется снова получать данные.
    -   **Это не очень эргономично.** Существует довольно много кода, связанного с написанием вызовов `fetch` таким образом, чтобы не страдать от ошибок типа [race conditions.](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect)

    Этот список недостатков не является специфическим для React. Он применим к выборке данных при подключении с помощью любой библиотеки. Как и в случае с маршрутизацией, выборка данных не является тривиальной задачей, поэтому мы рекомендуем следующие подходы:

    -   **Если вы используете [фреймворк](start-a-new-react-project.md), используйте его встроенный механизм выборки данных.** Современные фреймворки React имеют встроенные механизмы выборки данных, которые эффективны и не страдают от описанных выше подводных камней.
    -   В противном случае, рассмотрите возможность использования или создания кэша на стороне клиента. Популярные решения с открытым исходным кодом включают [React Query](https://tanstack.com/query/latest), [useSWR](https://swr.vercel.app/) и [React Router 6.4+.](https://beta.reactrouter.com/en/main/start/overview) Вы также можете создать собственное решение, в этом случае вы будете использовать Effects под капотом, но добавите логику для дедупликации запросов, кэширования ответов и избежания сетевых водопадов (путем предварительной загрузки данных или поднятия требований к данным в маршрутах).

    Вы можете продолжать получать данные непосредственно в Effects, если ни один из этих подходов вам не подходит.

### Отправка аналитики {#sending-analytics}

Рассмотрим этот код, который отправляет событие аналитики при посещении страницы:

```js
useEffect(() => {
    logVisit(url); // Sends a POST request
}, [url]);
```

В процессе разработки `logVisit` будет вызываться дважды для каждого URL, поэтому у вас может возникнуть соблазн попытаться исправить это. **Мы рекомендуем оставить этот код как есть.** Как и в предыдущих примерах, нет никакой _видимой пользователю_ разницы в поведении между однократным и двукратным запуском. С практической точки зрения, `logVisit` не должен ничего делать в разработке, потому что вы не хотите, чтобы журналы с машин разработки искажали производственные метрики. Ваш компонент перемонтируется каждый раз, когда вы сохраняете его файл, поэтому в любом случае он регистрирует лишние посещения в разработке.

**В производстве не будет дублирующих журналов посещений.**.

Для отладки событий аналитики, которые вы отправляете, вы можете развернуть свое приложение в среде staging (которая работает в режиме production) или временно отказаться от [Strict Mode](../reference/react/StrictMode.md) и его проверок ремонтирования только для разработки. Вы также можете отправлять аналитику из обработчиков событий изменения маршрута вместо Effects. Для более точной аналитики, [наблюдатели пересечений](https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API) могут помочь отследить, какие компоненты находятся в области просмотра и как долго они остаются видимыми.

### Не эффект: инициализация приложения {#not-an-effect-initializing-the-application}

Некоторая логика должна выполняться только один раз при запуске приложения. Вы можете поместить ее за пределы ваших компонентов:

```js hl_lines="3-4"
if (typeof window !== 'undefined') {
    // Check if we're running in the browser.
    checkAuthToken();
    loadDataFromLocalStorage();
}

function App() {
    // ...
}
```

Это гарантирует, что такая логика выполняется только один раз после загрузки страницы браузером.

### Не эффект: покупка товара {#not-an-effect-buying-a-product}

Иногда, даже если вы напишите функцию очистки, нет способа предотвратить видимые пользователю последствия запуска эффекта дважды. Например, возможно, ваш Эффект отправляет POST-запрос типа "Покупка товара":

```js hl_lines="2-3"
useEffect(() => {
    // 🔴 Wrong: This Effect fires twice in development, exposing a problem in the code.
    fetch('/api/buy', { method: 'POST' });
}, []);
```

Вы не захотите покупать продукт дважды. Однако именно поэтому вы не должны помещать эту логику в Effect. Что если пользователь перейдет на другую страницу, а затем нажмет Back? Ваш эффект запустится снова. Вы не хотите покупать товар, когда пользователь _посещает_ страницу; вы хотите купить его, когда пользователь _нажимает_ кнопку "Купить".

Покупка не вызвана рендерингом; она вызвана определенным взаимодействием. Он должен запускаться только тогда, когда пользователь нажимает на кнопку. **Удалите эффект и перенесите запрос `/api/buy` в обработчик события кнопки "Купить":**

```js hl_lines="2-3"
function handleClick() {
    // ✅ Buying is an event because it is caused by a particular interaction.
    fetch('/api/buy', { method: 'POST' });
}
```

**Это иллюстрирует, что если перемонтирование нарушает логику вашего приложения, то обычно это позволяет обнаружить существующие ошибки.** С точки зрения пользователя, посещение страницы не должно отличаться от ее посещения, щелчка по ссылке и нажатия кнопки Back. React проверяет, соблюдают ли ваши компоненты этот принцип, перемонтируя их один раз в процессе разработки.

## Собираем все вместе {#putting-it-all-together}

Эта игровая площадка поможет вам "почувствовать", как Эффекты работают на практике.

В этом примере используется [`setTimeout`](https://developer.mozilla.org/docs/Web/API/setTimeout), чтобы запланировать появление консольного журнала с введенным текстом через три секунды после запуска Эффекта. Функция очистки отменяет ожидающий таймаут. Начните с нажатия кнопки "Смонтировать компонент":

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';

    function Playground() {
    	const [text, setText] = useState('a');

    	useEffect(() => {
    		function onTimeout() {
    			console.log('⏰ ' + text);
    		}

    		console.log('🔵 Schedule "' + text + '" log');
    		const timeoutId = setTimeout(onTimeout, 3000);

    		return () => {
    			console.log('🟡 Cancel "' + text + '" log');
    			clearTimeout(timeoutId);
    		};
    	}, [text]);

    	return (
    		<>
    			<label>
    				What to log:{' '}
    				<input
    					value={text}
    					onChange={(e) =>
    						setText(e.target.value)
    					}
    				/>
    			</label>
    			<h1>{text}</h1>
    		</>
    	);
    }

    export default function App() {
    	const [show, setShow] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShow(!show)}>
    				{show ? 'Unmount' : 'Mount'} the component
    			</button>
    			{show && <hr />}
    			{show && <Playground />}
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/6kh88t?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Сначала вы увидите три журнала: `Schedule "a" log`, `Cancel "a" log`, и `Schedule "a" log` снова. Через три секунды появится также журнал с надписью `a`. Как вы узнали ранее, дополнительная пара schedule/cancel нужна потому, что React перемонтирует компонент один раз в процессе разработки, чтобы убедиться, что вы хорошо реализовали очистку.

Теперь отредактируйте входные данные так, чтобы они говорили `abc`. Если вы сделаете это достаточно быстро, вы увидите `Schedule "ab" log`, за которым сразу же последуют `Cancel "ab" log` и `Schedule "abc" log`. **React всегда очищает эффект предыдущего рендера перед эффектом следующего рендера.** Вот почему, даже если вы быстро вводите данные, за один раз будет запланирован только один тайм-аут. Отредактируйте ввод несколько раз и посмотрите на консоль, чтобы понять, как очищаются эффекты.

Введите что-нибудь в поле ввода, а затем сразу же нажмите "Размонтировать компонент". Обратите внимание, как размонтирование очищает Эффект последнего рендера. Здесь он очищает последний таймаут, прежде чем у него появится шанс сработать.

Наконец, отредактируйте компонент выше и закомментируйте функцию очистки, чтобы таймауты не отменялись. Попробуйте быстро набрать `abcde`. Что, по вашему мнению, произойдет через три секунды? Будет ли `console.log(text)` внутри тайм-аута печатать _последний_ `текст` и выдавать пять логов `abcde`? Попробуйте, чтобы проверить свою интуицию!

Через три секунды вы должны увидеть последовательность логов (`a`, `ab`, `abc`, `abcd` и `abcde`), а не пять логов `abcde`. **Каждый Эффект "захватывает" значение `text` из соответствующего рендера.** Не имеет значения, что состояние `text` изменилось: Эффект из рендера с `text = 'ab'` всегда будет видеть `'ab'`. Другими словами, эффекты из каждого рендера изолированы друг от друга. Если вам интересно, как это работает, вы можете прочитать о [closures](https://developer.mozilla.org/docs/Web/JavaScript/Closures).

!!!note "Каждый рендер имеет свои собственные Эффекты"

    Вы можете думать об `useEffect` как о "прикреплении" части поведения к выводу рендера. Рассмотрим этот Эффект:

    ```js
    export default function ChatRoom({ roomId }) {
    	useEffect(() => {
    		const connection = createConnection(roomId);
    		connection.connect();
    		return () => connection.disconnect();
    	}, [roomId]);

    	return <h1>Welcome to {roomId}!</h1>;
    }
    ```

    Давайте посмотрим, что именно происходит, когда пользователь перемещается по приложению.

    **Первоначальный рендер**

    Пользователь посещает `<ChatRoom roomId="general" />`. Давайте [мысленно заменим](state-as-a-snapshot.md) `roomId` на `'general'`:

    ```js
    // JSX for the first render (roomId = "general")
    return <h1>Welcome to general!</h1>;
    ```

    **Эффект также является частью вывода рендеринга.** Эффект первого рендеринга становится:

    ```js
    // Effect for the first render (roomId = "general")
    () => {
    	const connection = createConnection('general');
    	connection.connect();
    	return () => connection.disconnect();
    },
    	// Dependencies for the first render (roomId = "general")
    	['general'];
    ```

    React запускает этот Эффект, который подключается к чату `'general'`.

    **Повторный рендеринг с теми же зависимостями**

    Допустим, `<ChatRoom roomId="general" />` повторно рендерится. Вывод JSX будет таким же:

    ```js
    // JSX for the second render (roomId = "general")
    return <h1>Welcome to general!</h1>;
    ```

    React видит, что вывод рендера не изменился, поэтому он не обновляет DOM.

    Эффект от второго рендеринга выглядит следующим образом:

    ```js
    // Effect for the second render (roomId = "general")
    () => {
    	const connection = createConnection('general');
    	connection.connect();
    	return () => connection.disconnect();
    },
    	// Dependencies for the second render (roomId = "general")
    	['general'];
    ```

    React сравнивает `['general']` из второго рендера с `['general']` из первого рендера. **Поскольку все зависимости одинаковы, React _игнорирует_ Effect из второго рендера.** Он никогда не будет вызван.

    **Повторный рендеринг с различными зависимостями**

    Затем пользователь посещает `<ChatRoom roomId="travel" />`. На этот раз компонент возвращает другой JSX:

    ```js
    // JSX for the third render (roomId = "travel")
    return <h1>Welcome to travel!</h1>;
    ```

    React обновляет DOM, чтобы изменить `"Welcome to general"` на `"Welcome to travel"`.

    Эффект от третьего рендера выглядит следующим образом:

    ```js
    // Effect for the third render (roomId = "travel")
    () => {
    	const connection = createConnection('travel');
    	connection.connect();
    	return () => connection.disconnect();
    },
    	// Dependencies for the third render (roomId = "travel")
    	['travel'];
    ```

    React сравнивает `['travel']` из третьего рендера с `['general']` из второго рендера. Одна зависимость отличается: `Object.is('travel', 'general')` - `false`. Эффект не может быть пропущен.

    **Прежде чем React сможет применить эффект из третьего рендера, ему нужно очистить последний эффект, который _уже_ был запущен.** Эффект второго рендера был пропущен, поэтому React нужно очистить эффект первого рендера. Если вы прокрутите страницу до первого рендера, то увидите, что его очистка вызывает `disconnect()` для соединения, которое было создано с помощью `createConnection('general')`. Это отключает приложение от чата `'general'`.

    После этого React запускает третий эффект рендеринга. Он подключается к чату `'travel'`.

    **Размонтирование**

    Наконец, допустим, пользователь переходит в другое место, и компонент `ChatRoom` размонтируется. React запускает функцию очистки последнего эффекта. Последний Эффект был создан на третьем рендере. Очистка третьего рендера уничтожает соединение `createConnection('travel')`. Поэтому приложение отсоединяется от комнаты `'travel'`.

    **Поведение только для разработчиков**

    Когда включен [Строгий режим](../reference/react/StrictMode.md), React перемонтирует каждый компонент один раз после монтирования (состояние и DOM сохраняются). Это помогает найти эффекты, которые нуждаются в очистке, и выявляет ошибки, такие как условия гонки, на ранней стадии. Кроме того, React будет перемонтировать эффекты всякий раз, когда вы сохраняете файл в процессе разработки. Оба эти поведения предназначены только для разработки.

!!!note "Итоги"

    -   В отличие от событий, эффекты вызываются самим рендерингом, а не конкретным взаимодействием.
    -   Эффекты позволяют синхронизировать компонент с какой-либо внешней системой (сторонний API, сеть и т.д.).
    -   По умолчанию эффекты запускаются после каждого рендеринга (включая начальный).
    -   React пропустит эффект, если все его зависимости имеют те же значения, что и во время последнего рендера.
    -   Вы не можете "выбрать" свои зависимости. Они определяются кодом внутри Эффекта.
    -   Пустой массив зависимостей (`[]`) соответствует "монтированию" компонента, то есть его добавлению на экран.
    -   В строгом режиме React монтирует компоненты дважды (только в разработке\!) для стресс-тестирования ваших Эффектов.
    -   Если ваш Эффект сломается из-за повторного монтирования, вам необходимо реализовать функцию очистки.
    -   React будет вызывать вашу функцию очистки перед следующим запуском Эффекта и во время повторного монтирования.

## Задачи {#challenges}

### 1. Фокусировка на поле после монтирования {#focus-a-field-on-mount}

В этом примере форма отображает компонент `<MyInput />`.

Используйте метод [`focus()`](https://developer.mozilla.org/docs/Web/API/HTMLElement/focus) input'а, чтобы заставить `MyInput` автоматически фокусироваться, когда он появляется на экране. Уже есть закомментированная реализация, но она не совсем работает. Разберитесь, почему он не работает, и исправьте это. (Если вы знакомы с атрибутом `autoFocus`, представьте, что его не существует: мы реализуем ту же функциональность с нуля).

=== "MyInput.js"

    ```js
    import { useEffect, useRef } from 'react';

    export default function MyInput({ value, onChange }) {
    	const ref = useRef(null);

    	// TODO: This doesn't quite work. Fix it.
    	// ref.current.focus()

    	return (
    		<input
    			ref={ref}
    			value={value}
    			onChange={onChange}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/f7zsz4?view=Editor+%2B+Preview&module=%2Fsrc%2FMyInput.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Чтобы убедиться, что ваше решение работает, нажмите "Показать форму" и убедитесь, что ввод получает фокус (становится выделенным и курсор помещается внутрь). Нажмите "Скрыть форму" и снова "Показать форму". Убедитесь, что вход снова выделен.

`MyInput` должен фокусироваться только _при монтаже_, а не после каждого рендера. Чтобы убедиться в правильности поведения, нажмите "Показать форму", а затем несколько раз нажмите на флажок "Сделать прописными". Нажатие на флажок не должно _не_ фокусировать ввод над ним.

???success "Показать решение"

    Вызов `ref.current.focus()` во время рендеринга является неправильным, потому что это _побочный эффект_. Побочные эффекты должны быть либо помещены в обработчик событий, либо объявлены с `useEffect`. В данном случае побочный эффект _вызван_ появлением компонента, а не каким-либо конкретным взаимодействием, поэтому имеет смысл поместить его в Effect.

    Чтобы исправить ошибку, оберните вызов `ref.current.focus()` в объявление Effect. Затем, чтобы этот Эффект запускался только при монтировании, а не после каждого рендера, добавьте к нему пустые зависимости `[]`.

    === "MyInput.js"

    	```js
    	import { useEffect, useRef } from 'react';

    	export default function MyInput({ value, onChange }) {
    		const ref = useRef(null);

    		useEffect(() => {
    			ref.current.focus();
    		}, []);

    		return (
    			<input
    				ref={ref}
    				value={value}
    				onChange={onChange}
    			/>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/hyps49?view=Editor+%2B+Preview&module=%2Fsrc%2FMyInput.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 2. Фокусировка поля условно {#focus-a-field-conditionally}

Эта форма отображает два компонента `<MyInput />`.

Нажмите "Показать форму" и обратите внимание, что второе поле автоматически фокусируется. Это происходит потому, что оба компонента `<MyInput />` пытаются сфокусировать поле внутри. Когда вы вызываете `focus()` для двух полей ввода подряд, последнее всегда "побеждает".

Допустим, вы хотите сфокусировать первое поле. Первый компонент `MyInput` теперь получает булево свойство `shouldFocus`, установленное в `true`. Измените логику так, чтобы `focus()` вызывалась только в том случае, если пропс `shouldFocus`, полученный `MyInput`, равен `true`.

=== "App.js"

    ```js
    import { useEffect, useRef } from 'react';

    export default function MyInput({
    	shouldFocus,
    	value,
    	onChange,
    }) {
    	const ref = useRef(null);

    	// TODO: call focus() only if shouldFocus is true.
    	useEffect(() => {
    		ref.current.focus();
    	}, []);

    	return (
    		<input
    			ref={ref}
    			value={value}
    			onChange={onChange}
    		/>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/cggf6d?view=Editor+%2B+Preview&module=%2Fsrc%2FMyInput.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Чтобы проверить ваше решение, нажмите "Показать форму" и "Скрыть форму" несколько раз. Когда форма появится, только _первый_ вход должен быть сфокусирован. Это происходит потому, что родительский компонент отображает первый вход с `shouldFocus={true}`, а второй вход с `shouldFocus={false}`. Также проверьте, что оба ввода по-прежнему работают и вы можете вводить текст в оба из них.

???tip "Показать подсказку"

    Вы не можете объявить эффект условно, но ваш эффект может включать условную логику.

???success "Показать решение"

    Поместите условную логику внутрь Эффекта. Вам нужно будет указать `shouldFocus` как зависимость, потому что вы используете его внутри Эффекта. (Это означает, что если `shouldFocus` какого-либо ввода изменится с `false` на `true`, он сфокусируется после монтирования).

    === "MyInput.js"

    	```js
    	import { useEffect, useRef } from 'react';

    	export default function MyInput({
    		shouldFocus,
    		value,
    		onChange,
    	}) {
    		const ref = useRef(null);

    		useEffect(() => {
    			if (shouldFocus) {
    				ref.current.focus();
    			}
    		}, [shouldFocus]);

    		return (
    			<input
    				ref={ref}
    				value={value}
    				onChange={onChange}
    			/>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/f4pn55?view=Editor+%2B+Preview&module=%2Fsrc%2FMyInput.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### 3. Исправьте интервал, который срабатывает дважды {#fix-an-interval-that-fires-twice}

Этот компонент `Counter` отображает счетчик, который должен увеличиваться каждую секунду. При монтировании он вызывает [`setInterval`.](https://developer.mozilla.org/docs/Web/API/setInterval) Это заставляет функцию `onTick` выполняться каждую секунду. Функция `onTick` увеличивает счетчик.

Однако вместо того, чтобы увеличиваться один раз в секунду, она увеличивается дважды. Почему так происходит? Найдите причину ошибки и исправьте ее.

=== "Counter.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function Counter() {
    	const [count, setCount] = useState(0);

    	useEffect(() => {
    		function onTick() {
    			setCount((c) => c + 1);
    		}

    		setInterval(onTick, 1000);
    	}, []);

    	return <h1>{count}</h1>;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/8nhxmd?view=Editor+%2B+Preview&module=%2Fsrc%2FCounter.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???tip "Показать подсказку"

    Помните, что `setInterval` возвращает ID интервала, который вы можете передать в [`clearInterval`](https://developer.mozilla.org/docs/Web/API/clearInterval), чтобы остановить интервал.

???success "Показать решение"

    Когда включен [Строгий режим](../reference/react/StrictMode.md) (как в песочницах на этом сайте), React перемонтирует каждый компонент один раз в процессе разработки. Это приводит к тому, что интервал устанавливается дважды, и поэтому каждую секунду счетчик увеличивается дважды.

    Однако поведение React не является _причиной_ ошибки: ошибка уже существует в коде. Поведение React делает ошибку более заметной. Настоящая причина в том, что этот Эффект запускает процесс, но не предоставляет способа его очистки.

    Чтобы исправить этот код, сохраните идентификатор интервала, возвращаемый `setInterval`, и реализуйте функцию очистки с помощью [`clearInterval`](https://developer.mozilla.org/docs/Web/API/clearInterval):

    === "Counter.js"

    ```js
    import { useState, useEffect } from 'react';

    export default function Counter() {
    	const [count, setCount] = useState(0);

    	useEffect(() => {
    		function onTick() {
    			setCount((c) => c + 1);
    		}

    		const intervalId = setInterval(onTick, 1000);
    		return () => clearInterval(intervalId);
    	}, []);

    	return <h1>{count}</h1>;
    }
    ```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/fcnn3z?view=Editor+%2B+Preview&module=%2Fsrc%2FCounter.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    В процессе разработки React все равно перемонтирует ваш компонент один раз, чтобы убедиться, что вы хорошо реализовали очистку. Поэтому будет вызван вызов `setInterval`, за которым сразу же последует `clearInterval`, и снова `setInterval`. В продакшене будет только один вызов `setInterval`. Видимое пользователю поведение в обоих случаях одинаково: счетчик увеличивается раз в секунду.

### 4. Исправление выборки внутри эффекта {#fix-fetching-inside-an-effect}

Этот компонент показывает биографию для выбранного человека. Он загружает биографию, вызывая асинхронную функцию `fetchBio(person)` при монтировании и при каждом изменении `person`. Эта асинхронная функция возвращает [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise), который в конечном итоге разрешается в строку. Когда выборка завершена, вызывается `setBio` для отображения этой строки в поле выбора.

=== "App.js"

    ```js
    import { useState, useEffect } from 'react';
    import { fetchBio } from './api.js';

    export default function Page() {
    	const [person, setPerson] = useState('Alice');
    	const [bio, setBio] = useState(null);

    	useEffect(() => {
    		setBio(null);
    		fetchBio(person).then((result) => {
    			setBio(result);
    		});
    	}, [person]);

    	return (
    		<>
    			<select
    				value={person}
    				onChange={(e) => {
    					setPerson(e.target.value);
    				}}
    			>
    				<option value="Alice">Alice</option>
    				<option value="Bob">Bob</option>
    				<option value="Taylor">Taylor</option>
    			</select>
    			<hr />
    			<p>
    				<i>{bio ?? 'Loading...'}</i>
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/c9vdv7?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

В этом коде есть ошибка. Начните с выбора "Алисы". Затем выберите "Боб" и сразу после этого выберите "Тейлор". Если вы сделаете это достаточно быстро, вы заметите эту ошибку: Тейлор выбран, но в абзаце ниже написано "Это биография Боба".

Почему так происходит? Исправьте ошибку внутри этого Эффекта.

???tip "Показать подсказку"

    Если Эффект получает что-то асинхронно, он обычно нуждается в очистке.

???success "Показать решение"

    Чтобы запустить ошибку, все должно произойти в таком порядке:

    -   Выбор `'Bob'` вызывает `fetchBio('Bob')`.
    -   Выбор `Тейлора` вызывает `fetchBio('Taylor')`
    -   **Выборка `Тейлора` завершается _перед_ выборкой `Боба`**.
    -   Эффект от рендеринга `Тейлора` вызывает `setBio('Это биография Тейлора')`.
    -   Получение `Боба` завершается
    -   Эффект от рендера `'Bob'` вызывает `setBio('Это биография Боба')`.

    Вот почему вы видите биографию Боба, даже если выбран Тейлор. Подобные ошибки называются [состояние гонки](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B5_%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8), потому что две асинхронные операции "гоняются" друг с другом, и они могут выполняться в неожиданном порядке.

    Чтобы исправить это состояние гонки, добавьте функцию очистки:

    === "App.js"

    	```js
    	import { useState, useEffect } from 'react';
    	import { fetchBio } from './api.js';

    	export default function Page() {
    		const [person, setPerson] = useState('Alice');
    		const [bio, setBio] = useState(null);
    		useEffect(() => {
    			let ignore = false;
    			setBio(null);
    			fetchBio(person).then((result) => {
    				if (!ignore) {
    					setBio(result);
    				}
    			});
    			return () => {
    				ignore = true;
    			};
    		}, [person]);

    		return (
    			<>
    				<select
    					value={person}
    					onChange={(e) => {
    						setPerson(e.target.value);
    					}}
    				>
    					<option value="Alice">Alice</option>
    					<option value="Bob">Bob</option>
    					<option value="Taylor">Taylor</option>
    				</select>
    				<hr />
    				<p>
    					<i>{bio ?? 'Loading...'}</i>
    				</p>
    			</>
    		);
    	}
    	```

    === "CodeSandbox"

    	<iframe src="https://codesandbox.io/embed/zwx37k?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

    Каждый Эффект рендера имеет свою собственную переменную `ignore`. Изначально переменная `ignore` имеет значение `false`. Однако, если Эффект очищается (например, когда вы выбираете другого человека), его переменная `ignore` становится `true`. Таким образом, теперь не имеет значения, в каком порядке выполняются запросы. Только у Эффекта последнего человека `ignore` будет установлена в `false`, поэтому он вызовет `setBio(result)`. Прошлые Эффекты были очищены, поэтому проверка `if (!ignore)` не позволит им вызвать `setBio`:

    -   Выбор `'Bob'` вызывает `fetchBio('Bob')`.
    -   Выборка `'Taylor'` вызывает `fetchBio('Taylor')` **и очищает предыдущий эффект (эффект Боба)**.
    -   Выборка `Тейлора` завершается _до_ выборки `Боба`.
    -   Эффект из рендера `'Taylor'` вызывает `setBio('This is Taylor's bio')`.
    -   Получение `Боба` завершается
    -   Эффект из рендера `'Bob'` **ничего не делает, потому что его флаг `ignore` был установлен в `true`**.

    Помимо игнорирования результата устаревшего вызова API, вы также можете использовать [`AbortController`](https://developer.mozilla.org/docs/Web/API/AbortController) для отмены запросов, которые больше не нужны. Однако одного этого недостаточно для защиты от условий гонки. После выборки может быть выполнено больше асинхронных шагов, поэтому использование явного флага типа `ignore` является наиболее надежным способом устранения проблем такого типа.

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/synchronizing-with-effects](https://react.dev/learn/synchronizing-with-effects)</small>
