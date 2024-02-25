# &lt;option&gt;

Компонент [встроенный в браузер `<option>`](https://hcdev.ru/html/option/) позволяет отобразить опцию внутри поля [`<select>`](./select.md).

```jsx
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

## Описание

### `<option>`

Компонент [встроенный в браузер `option`](https://hcdev.ru/html/option/) позволяет отобразить опцию внутри поля [`select`](./select.md).

```js
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

#### Пропсы

`<option>` поддерживает все [общие пропсы элементов](./common.md#props).

Дополнительно, `<option>` поддерживает эти пропсы:

-   [`disabled`](https://hcdev.ru/html/option/#disabled): Булево значение. Если `true`, опция не будет доступна для выбора и будет отображаться затемненной.
-   [`label`](https://hcdev.ru/html/option/#label): Строка. Определяет значение опции. Если не указана, используется текст внутри опции.
-   [`value`](https://hcdev.ru/html/option/#value): Значение, которое будет использоваться [при отправке родительского `<select>` в форме](./select.md#reading-the-select-box-value-when-submitting-a-form), если выбран этот параметр.

#### Ограничения

-   React не поддерживает атрибут `selected` для `<option>`. Вместо этого передайте `значение` этой опции родителю [`<select defaultValue>`](./select.md#providing-an-initially-selected-option) для неуправляемого блока выбора или [`<select value>`](./select.md#controlling-a-select-box-with-a-state-variable) для управляемого блока выбора.

## Использование

### Отображение поля выбора с опциями

Для отображения поля выбора создайте `<select>` со списком компонентов `<option>` внутри. Задайте каждому `<option>` значение `value`, представляющее данные, которые должны быть представлены в форме.

[Подробнее об отображении `<select>` со списком компонентов `<option>`.](./select.md)

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
