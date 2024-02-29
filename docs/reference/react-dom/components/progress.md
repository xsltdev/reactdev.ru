---
description: Встроенный компонент браузера progress позволяет выводить индикатор прогресса
---

# &lt;progress&gt;

<big>Встроенный компонент браузера [`<progress>`](https://hcdev.ru/html/progress/) позволяет выводить индикатор прогресса.</big>

```js
<progress value={0.5} />
```

## Описание {#reference}

### `<progress>` {#progress}

Чтобы отобразить индикатор прогресса, создайте компонент [встроенный в браузер `<progress>`](https://hcdev.ru/html/progress/).

```js
<progress value={0.5} />
```

**Пропсы**

`<progress>` поддерживает все [общие пропсы элементов](./common.md#props).

Дополнительно, `<progress>` поддерживает эти пропсы:

-   [`max`](https://hcdev.ru/html/progress/#_3): Число. Определяет максимальное `value`. По умолчанию `1`.
-   [`value`](https://hcdev.ru/html/progress/#_3): Число от `0` до `max`, или `null` для неопределенного прогресса. Указывает, сколько было сделано.

## Использование {#usage}

### Управление индикатором прогресса {#controlling-a-progress-indicator}

Чтобы отобразить индикатор прогресса, создайте компонент `<progress>`. Вы можете передать число `value` между `0` и `max` значением, которое вы укажете. Если вы не передадите значение `max`, то по умолчанию оно будет равно `1`.

Если операция не выполняется, передайте `value={null}`, чтобы перевести индикатор прогресса в неопределенное состояние.

=== "App.js"

    ```js
    export default function App() {
    	return (
    		<>
    			<progress value={0} />
    			<progress value={0.5} />
    			<progress value={0.7} />
    			<progress value={75} max={100} />
    			<progress value={1} />
    			<progress value={null} />
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/p2wmww?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/progress](https://react.dev/reference/react-dom/components/progress)</small>
