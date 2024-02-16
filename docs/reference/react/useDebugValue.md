# useDebugValue

**`useDebugValue`** - это хук React, который позволяет добавить метку к пользовательскому хуку в [React DevTools](../learn/react-developer-tools.md).

```js
useDebugValue(value, format?)
```

## Описание

### `useDebugValue(value, format?)`

Вызывает `useDebugValue` на верхнем уровне вашего [пользовательского хука](../learn/reusing-logic-with-custom-hooks.md) для отображения читаемого отладочного значения:

```js
import { useDebugValue } from 'react';

function useOnlineStatus() {
    // ...
    useDebugValue(isOnline ? 'Online' : 'Offline');
    // ...
}
```

#### Параметры

-   `value`: Значение, которое вы хотите отобразить в React DevTools. Оно может иметь любой тип.
-   **опционально** `format`: Функция форматирования. При осмотре компонента React DevTools вызовет функцию форматирования с `value` в качестве аргумента, а затем отобразит возвращенное форматированное значение (которое может иметь любой тип). Если вы не укажете функцию форматирования, будет отображено исходное `value`.

#### Возвращает

`useDebugValue` ничего не возвращает.

## Использование

### Добавление метки к пользовательскому крючку

Вызовите `useDebugValue` на верхнем уровне вашего [custom Hook](../learn/reusing-logic-with-custom-hooks.md), чтобы отобразить читаемое отладочное значение для [React DevTools](../learn/react-developer-tools.md).

```js
import { useDebugValue } from 'react';

function useOnlineStatus() {
    // ...
    useDebugValue(isOnline ? 'Online' : 'Offline');
    // ...
}
```

Это дает компонентам, вызывающим `useOnlineStatus`, метку типа `OnlineStatus: "Online"` при их осмотре:

![Скриншот React DevTools, показывающий отладочное значение](react-devtools-usedebugvalue.png)

Без вызова `useDebugValue` отображались бы только базовые данные (в данном примере `true`).

=== "App.js"

    ```js
    import { useOnlineStatus } from './useOnlineStatus.js';

    function StatusBar() {
    	const isOnline = useOnlineStatus();
    	return (
    		<h1>
    			{isOnline ? '✅ Online' : '❌ Disconnected'}
    		</h1>
    	);
    }

    export default function App() {
    	return <StatusBar />;
    }
    ```

=== "useOnlineStatus.js"

    ```js
    import { useSyncExternalStore, useDebugValue } from 'react';

    export function useOnlineStatus() {
    	const isOnline = useSyncExternalStore(
    		subscribe,
    		() => navigator.onLine,
    		() => true
    	);
    	useDebugValue(isOnline ? 'Online' : 'Offline');
    	return isOnline;
    }

    function subscribe(callback) {
    	window.addEventListener('online', callback);
    	window.addEventListener('offline', callback);
    	return () => {
    		window.removeEventListener('online', callback);
    		window.removeEventListener('offline', callback);
    	};
    }
    ```

!!!note ""

    Не добавляйте значения отладки в каждый пользовательский хук. Это наиболее ценно для пользовательских хуков, которые являются частью общих библиотек и имеют сложную внутреннюю структуру данных, которую трудно проверить.

### Откладывание форматирования отладочного значения

Вы также можете передать функцию форматирования в качестве второго аргумента в `useDebugValue`:

```js
useDebugValue(date, (date) => date.toDateString());
```

Ваша функция форматирования получит отладочное значение в качестве параметра и должна вернуть форматированное отображаемое значение. Когда ваш компонент будет проверен, React DevTools вызовет эту функцию и отобразит ее результат.

Это позволяет вам избежать выполнения потенциально дорогостоящей логики форматирования, пока компонент не будет проверен. Например, если `date` является значением Date, это позволяет избежать вызова `toDateString()` для него при каждом рендере.

## Ссылки

-   [https://react.dev/reference/react/useDebugValue](https://react.dev/reference/react/useDebugValue)
