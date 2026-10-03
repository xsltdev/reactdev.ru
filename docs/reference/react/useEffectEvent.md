---
description: useEffectEvent - это хук React, который позволяет отделить события от эффектов
---

# useEffectEvent

<big>**`useEffectEvent`** - это хук React, который позволяет отделить события от эффектов.</big>

```js
const onEvent = useEffectEvent(callback)
```

## Описание {#reference}

### `useEffectEvent(callback)` {#useeffectevent}

Вызовите `useEffectEvent` на верхнем уровне вашего компонента, чтобы создать событие эффекта.

```js hl_lines="4 6"
import { useEffectEvent, useEffect } from 'react';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });
}
```

События эффекта — часть логики вашего эффекта, но ведут себя скорее как обработчик события. Они всегда «видят» последние значения из рендера (например, пропсы и состояние), не пересинхронизируя ваш эффект, поэтому они исключены из зависимостей эффекта. Подробнее см. [Отделение событий от эффектов](../../learn/separating-events-from-effects.md#extracting-non-reactive-logic-out-of-effects).

[См. больше примеров ниже.](#usage)

#### Параметры {#parameters}

-   `callback`: Функция с логикой вашего события эффекта. Функция может принимать любое количество аргументов и возвращать любое значение. Когда вы вызываете возвращённую функцию события эффекта, `callback` всегда обращается к последним значениям, зафиксированным при рендере на момент вызова.

#### Возвращаемое значение {#returns}

`useEffectEvent` возвращает функцию события эффекта с той же сигнатурой типа, что и ваш `callback`.

Эту функцию можно вызывать внутри `useEffect`, `useLayoutEffect`, `useInsertionEffect` или из других событий эффекта в том же компоненте.

#### Предупреждения {#caveats}

-   `useEffectEvent` — это хук, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, извлеките новый компонент и перенесите в него событие эффекта.
-   События эффекта можно вызывать только изнутри эффектов или других событий эффекта. Не вызывайте их во время рендеринга и не передавайте их другим компонентам или хукам. Линтер [`eslint-plugin-react-hooks`](../eslint-plugin-react-hooks/index.md) проверяет это ограничение.
-   Не используйте `useEffectEvent`, чтобы избежать указания зависимостей в массиве зависимостей эффекта. Это скрывает ошибки и делает код труднее для понимания. Используйте его только для логики, которая действительно является событием, запускаемым из эффектов.
-   Функции события эффекта не имеют стабильной идентичности. Их идентичность намеренно меняется при каждом рендере.

<a id="why-are-effect-events-not-stable"></a>

??? note "Почему события эффекта нестабильны?"

    В отличие от функций `set` из `useState` или рефов, функции события эффекта не имеют стабильной идентичности. Их идентичность намеренно меняется при каждом рендере:

    ```js
    // 🔴 Wrong: including Effect Event in dependencies
    useEffect(() => {
      onSomething();
    }, [onSomething]); // ESLint will warn about this
    ```

    Это осознанный выбор дизайна. События эффекта предназначены для вызова только изнутри эффектов в том же компоненте. Поскольку вызывать их можно только локально и нельзя передавать другим компонентам или включать в массивы зависимостей, стабильная идентичность не имела бы смысла и на самом деле маскировала бы ошибки.

    Нестабильная идентичность работает как проверка во время выполнения: если ваш код ошибочно зависит от идентичности функции, вы увидите, что эффект перезапускается при каждом рендере, и ошибка станет очевидной.

    Такой дизайн подчёркивает, что события эффекта концептуально принадлежат конкретному эффекту и не являются API общего назначения, чтобы отказаться от реактивности.

## Использование {#usage}

### Использование события в эффекте {#using-an-event-in-an-effect}

Вызовите `useEffectEvent` на верхнем уровне вашего компонента, чтобы создать *событие эффекта*:

```js hl_lines="1"
const onConnected = useEffectEvent(() => {
  if (!muted) {
    showNotification('Connected!');
  }
});
```

`useEffectEvent` принимает `event callback` и возвращает событие эффекта. Событие эффекта — это функция, которую можно вызывать внутри эффектов, не переподключая эффект:

```js hl_lines="3"
useEffect(() => {
  const connection = createConnection(roomId);
  connection.on('connected', onConnected);
  connection.connect();
  return () => {
    connection.disconnect();
  }
}, [roomId]);
```

Поскольку `onConnected` — событие эффекта, `muted` и `onConnect` не входят в зависимости эффекта.

!!!warning "Не используйте события эффекта, чтобы пропускать зависимости"

    Может возникнуть соблазн использовать `useEffectEvent`, чтобы не перечислять зависимости, которые кажутся «ненужными». Однако это скрывает ошибки и делает код труднее для понимания:

    ```js
    // 🔴 Wrong: Using Effect Events to hide dependencies
    const logVisit = useEffectEvent(() => {
      log(pageUrl);
    });

    useEffect(() => {
      logVisit()
    }, []); // Missing pageUrl means you miss logs
    ```

    Если значение должно заставлять эффект выполняться заново, оставьте его зависимостью. Используйте события эффекта только для логики, которая действительно не должна заново запускать ваш эффект.

    Подробнее см. [Отделение событий от эффектов](../../learn/separating-events-from-effects.md).

### Использование таймера с последними значениями {#using-a-timer-with-latest-values}

Когда вы используете `setInterval` или `setTimeout` в эффекте, часто нужно читать последние значения из рендера, не перезапуская таймер при каждом изменении этих значений.

Этот счётчик увеличивает `count` на текущее значение `increment` каждую секунду. Событие эффекта `onTick` читает последние `count` и `increment`, не заставляя интервал перезапускаться:

=== "js"

    ```js

    import { useState, useEffect, useEffectEvent } from 'react';

    export default function Timer() {
        const [count, setCount] = useState(0);
        const [increment, setIncrement] = useState(1);

        const onTick = useEffectEvent(() => {
            setCount(count + increment);
        });

        useEffect(() => {
            const id = setInterval(() => {
                onTick();
            }, 1000);
            return () => {
                clearInterval(id);
            };
        }, []);

        return (
            <>
                <h1>
                    Counter: {count}
                    <button onClick={() => setCount(0)}>Reset</button>
                </h1>
                <hr />
                <p>
                    Every second, increment by:
                    <button disabled={increment === 0} onClick={() => {
                        setIncrement(i => i - 1);
                    }}>–</button>
                    <b>{increment}</b>
                    <button onClick={() => {
                        setIncrement(i => i + 1);
                    }}>+</button>
                </p>
            </>
        );
    }
    ```

=== "styles.css"

    ```css

    button { margin: 10px; }
    ```

Попробуйте изменить значение приращения, пока таймер работает. Счётчик сразу использует новое значение приращения, но таймер продолжает тикать ровно, без перезапуска.

### Использование слушателя событий с последними значениями {#using-an-event-listener-with-latest-values}

Когда вы настраиваете слушатель событий в эффекте, в колбэке часто нужно читать последние значения из рендера. Без `useEffectEvent` пришлось бы включить эти значения в зависимости, из-за чего слушатель удалялся бы и добавлялся заново при каждом изменении.

В этом примере точка следует за курсором, но только когда отмечено «Can move». Событие эффекта `onMove` всегда читает последнее значение `canMove`, не перезапуская эффект:

=== "js"

    ```js

    import { useState, useEffect, useEffectEvent } from 'react';

    export default function App() {
        const [position, setPosition] = useState({ x: 0, y: 0 });
        const [canMove, setCanMove] = useState(true);

        const onMove = useEffectEvent(e => {
            if (canMove) {
                setPosition({ x: e.clientX, y: e.clientY });
            }
        });

        useEffect(() => {
            window.addEventListener('pointermove', onMove);
            return () => window.removeEventListener('pointermove', onMove);
        }, []);

        return (
            <>
                <label>
                    <input
                        type="checkbox"
                        checked={canMove}
                        onChange={e => setCanMove(e.target.checked)}
                    />
                    The dot is allowed to move
                </label>
                <hr />
                <div style={{
                    position: 'absolute',
                    backgroundColor: 'pink',
                    borderRadius: '50%',
                    opacity: 0.6,
                    transform: `translate(${position.x}px, ${position.y}px)`,
                    pointerEvents: 'none',
                    left: -20,
                    top: -20,
                    width: 40,
                    height: 40,
                }} />
            </>
        );
    }
    ```

=== "styles.css"

    ```css

    body {
      height: 200px;
    }
    ```

Переключите флажок и подвигайте курсор. Точка сразу реагирует на состояние флажка, но слушатель событий настраивается только один раз при монтировании компонента.

### Как не переподключаться к внешним системам {#showing-a-notification-without-reconnecting}

Частый сценарий для `useEffectEvent` — когда вы хотите сделать что-то в ответ на эффект, но это «что-то» зависит от значения, на которое вы не хотите реагировать.

В этом примере компонент чата подключается к комнате и показывает уведомление при подключении. Пользователь может отключить уведомления флажком. Однако вы не хотите переподключаться к комнате чата каждый раз, когда пользователь меняет настройки:

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "latest",
        "react-dom": "latest",
        "react-scripts": "latest",
        "toastify-js": "1.12.0"
      },
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test --env=jsdom",
        "eject": "react-scripts eject"
      }
    }
    ```

=== "js"

    ```js

    import { useState, useEffect, useEffectEvent } from 'react';
    import { createConnection } from './chat.js';
    import { showNotification } from './notifications.js';

    function ChatRoom({ roomId, muted }) {
        const onConnected = useEffectEvent((roomId) => {
            console.log('✅ Connected to ' + roomId + ' (muted: ' + muted + ')');
            if (!muted) {
                showNotification('Connected to ' + roomId);
            }
        });

        useEffect(() => {
            const connection = createConnection(roomId);
            console.log('⏳ Connecting to ' + roomId + '...');
            connection.on('connected', () => {
                onConnected(roomId);
            });
            connection.connect();
            return () => {
                console.log('❌ Disconnected from ' + roomId);
                connection.disconnect();
            }
        }, [roomId]);

        return <h1>Welcome to the {roomId} room!</h1>;
    }

    export default function App() {
        const [roomId, setRoomId] = useState('general');
        const [muted, setMuted] = useState(false);
        return (
            <>
                <label>
                    Choose the chat room:{' '}
                    <select
                        value={roomId}
                        onChange={e => setRoomId(e.target.value)}
                    >
                        <option value="general">general</option>
                        <option value="travel">travel</option>
                        <option value="music">music</option>
                    </select>
                </label>
                <label>
                    <input
                        type="checkbox"
                        checked={muted}
                        onChange={e => setMuted(e.target.checked)}
                    />
                    Mute notifications
                </label>
                <hr />
                <ChatRoom
                    roomId={roomId}
                    muted={muted}
                />
            </>
        );
    }
    ```

=== "chat.js"

    ```js

    const serverUrl = 'https://localhost:1234';

    export function createConnection(roomId) {
        // A real implementation would actually connect to the server
        let connectedCallback;
        let timeout;
        return {
            connect() {
                timeout = setTimeout(() => {
                    if (connectedCallback) {
                        connectedCallback();
                    }
                }, 100);
            },
            on(event, callback) {
                if (connectedCallback) {
                    throw Error('Cannot add the handler twice.');
                }
                if (event !== 'connected') {
                    throw Error('Only "connected" event is supported.');
                }
                connectedCallback = callback;
            },
            disconnect() {
                clearTimeout(timeout);
            }
        };
    }
    ```

=== "notifications.js"

    ```js

    import Toastify from 'toastify-js';
    import 'toastify-js/src/toastify.css';

    export function showNotification(message, theme) {
        Toastify({
            text: message,
            duration: 2000,
            gravity: 'top',
            position: 'right',
            style: {
                background: theme === 'dark' ? 'black' : 'white',
                color: theme === 'dark' ? 'white' : 'black',
            },
        }).showToast();
    }
    ```

=== "styles.css"

    ```css

    label { display: block; margin-top: 10px; }
    ```

Попробуйте переключать комнаты. Чат переподключается и показывает уведомление. Теперь отключите уведомления. Поскольку `muted` читается внутри события эффекта, а не внутри эффекта, чат остаётся подключённым.

### Использование событий эффекта в собственных хуках {#using-effect-events-in-custom-hooks}

Вы можете использовать `useEffectEvent` внутри собственных хуков. Это позволяет создавать переиспользуемые хуки, которые инкапсулируют эффекты, оставляя некоторые значения нереактивными:

=== "js"

    ```js

    import { useState, useEffect, useEffectEvent } from 'react';

    function useInterval(callback, delay) {
        const onTick = useEffectEvent(callback);

        useEffect(() => {
            if (delay === null) {
                return;
            }
            const id = setInterval(() => {
                onTick();
            }, delay);
            return () => clearInterval(id);
        }, [delay]);
    }

    function Counter({ incrementBy }) {
        const [count, setCount] = useState(0);

        useInterval(() => {
            setCount(c => c + incrementBy);
        }, 1000);

        return (
            <div>
                <h2>Count: {count}</h2>
                <p>Incrementing by {incrementBy} every second</p>
            </div>
        );
    }

    export default function App() {
        const [incrementBy, setIncrementBy] = useState(1);

        return (
            <>
                <label>
                    Increment by:{' '}
                    <select
                        value={incrementBy}
                        onChange={(e) => setIncrementBy(Number(e.target.value))}
                    >
                        <option value={1}>1</option>
                        <option value={5}>5</option>
                        <option value={10}>10</option>
                    </select>
                </label>
                <hr />
                <Counter incrementBy={incrementBy} />
            </>
        );
    }
    ```

=== "styles.css"

    ```css

    label { display: block; margin-bottom: 8px; }
    ```

В этом примере `useInterval` — собственный хук, который настраивает интервал. Переданный ему `callback` обёрнут в событие эффекта, поэтому интервал не сбрасывается, даже если новый `callback` передаётся при каждом рендере.

## Устранение неполадок {#troubleshooting}

### Я получаю ошибку: "A function wrapped in useEffectEvent can't be called during rendering" {#cant-call-during-rendering}

Эта ошибка означает, что вы вызываете функцию события эффекта во время фазы рендеринга компонента. События эффекта можно вызывать только изнутри эффектов или других событий эффекта.

```js
function MyComponent({ data }) {
  const onLog = useEffectEvent(() => {
    console.log(data);
  });

  // 🔴 Wrong: calling during render
  onLog();

  // ✅ Correct: call from an Effect
  useEffect(() => {
    onLog();
  }, []);

  return <div>{data}</div>;
}
```

Если вам нужно выполнить логику во время рендеринга, не оборачивайте её в `useEffectEvent`. Вызовите логику напрямую или перенесите её в эффект.

### Я получаю ошибку линтера: "Functions returned from useEffectEvent must not be included in the dependency array" {#effect-event-in-deps}

Если вы видите предупреждение вроде «Functions returned from `useEffectEvent` must not be included in the dependency array», уберите событие эффекта из зависимостей:

```js
const onSomething = useEffectEvent(() => {
  // ...
});

// 🔴 Wrong: Effect Event in dependencies
useEffect(() => {
  onSomething();
}, [onSomething]);

// ✅ Correct: no Effect Event in dependencies
useEffect(() => {
  onSomething();
}, []);
```

События эффекта задуманы так, чтобы вызываться из эффектов, не будучи перечисленными как зависимости. Линтер требует этого, потому что идентичность функции [намеренно нестабильна](#why-are-effect-events-not-stable). Если включить её, эффект будет перезапускаться при каждом рендере.

### Я получаю ошибку линтера: "... is a function created with useEffectEvent, and can only be called from Effects" {#effect-event-called-outside-effect}

Если вы видите предупреждение вроде «... is a function created with React Hook `useEffectEvent`, and can only be called from Effects and Effect Events», вы вызываете функцию не из того места:

```js
const onSomething = useEffectEvent(() => {
  console.log(value);
});

// 🔴 Wrong: calling from event handler
function handleClick() {
  onSomething();
}

// 🔴 Wrong: passing to child component
return <Child onSomething={onSomething} />;

// ✅ Correct: calling from Effect
useEffect(() => {
  onSomething();
}, []);
```

События эффекта специально предназначены для использования в эффектах, локальных для компонента, в котором они определены. Если вам нужен колбэк для обработчиков событий или чтобы передать его дочерним компонентам, используйте обычную функцию или `useCallback`.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useEffectEvent](https://react.dev/reference/react/useEffectEvent)</small>
