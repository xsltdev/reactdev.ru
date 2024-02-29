---
description: Компонент встроенный в браузер option позволяет отобразить опцию внутри поля select
---

# &lt;option&gt;

<big>Компонент [встроенный в браузер `<option>`](https://hcdev.ru/html/option/) позволяет отобразить опцию внутри поля [`<select>`](./select.md).</big>

```js
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

## Описание {#reference}

### `<option>` {#option}

Компонент [встроенный в браузер `option`](https://hcdev.ru/html/option/) позволяет отобразить опцию внутри поля [`select`](./select.md).

```js
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

**Пропсы**

`<option>` поддерживает все [общие пропсы элементов](./common.md#props).

Дополнительно, `<option>` поддерживает эти пропсы:

-   [`disabled`](https://hcdev.ru/html/option/#disabled): Булево значение. Если `true`, опция не будет доступна для выбора и будет отображаться затемненной.
-   [`label`](https://hcdev.ru/html/option/#label): Строка. Определяет значение опции. Если не указана, используется текст внутри опции.
-   [`value`](https://hcdev.ru/html/option/#value): Значение, которое будет использоваться [при отправке родительского `<select>` в форме](./select.md#reading-the-select-box-value-when-submitting-a-form), если выбран этот параметр.

**Ограничения**

-   React не поддерживает атрибут `selected` для `<option>`. Вместо этого передайте `value` этой опции родителю [`<select defaultValue>`](./select.md#providing-an-initially-selected-option) для неуправляемого блока выбора или [`<select value>`](./select.md#controlling-a-select-box-with-a-state-variable) для управляемого блока выбора.

## Использование {#usage}

### Отображение поля выбора с опциями {#displaying-a-select-box-with-options}

Для отображения поля выбора создайте `<select>` со списком компонентов `<option>` внутри. Задайте каждому `<option>` значение `value`, представляющее данные, которые должны быть представлены в форме.

Подробнее об [отображении `<select>` со списком компонентов `<option>`.](./select.md)

=== "App.js"

    ```js
    export default function FruitPicker() {
    	return (
    		<label>
    			Pick a fruit:
    			<select name="selectedFruit">
    				<option value="apple">Apple</option>
    				<option value="banana">Banana</option>
    				<option value="orange">Orange</option>
    			</select>
    		</label>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/2f64v2?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/option](https://react.dev/reference/react-dom/components/option)</small>
