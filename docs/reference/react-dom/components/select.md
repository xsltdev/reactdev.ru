# &lt;select&gt;

Встроенный компонент браузера [`<select>`](https://hcdev.ru/html/select/) позволяет отобразить поле выбора с опциями.

```jsx
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

## Описание

### `<select>`

Чтобы отобразить поле выбора, создайте компонент [встроенный в браузер `<select>`](https://hcdev.ru/html/select/).

```js
<select>
    <option value="someOption">Some option</option>
    <option value="otherOption">Other option</option>
</select>
```

#### Пропсы

`<select>` поддерживает все [общие пропсы элементов](components-common.md#props)

Вы можете сделать поле выбора управляемым, передав ему пропс `value`:

-   `value`: Строка (или массив строк для `multiple={true}`). Управляет тем, какая опция будет выбрана. Каждая строка значения соответствует `значению` некоторого `<option>`, вложенного внутрь `<select>`.

Когда вы передаете `value`, вы также должны передать обработчик `onChange`, который обновляет переданное значение.

Если ваш `<select>` является неуправляемым, вы можете передать пропс `defaultValue` вместо него:

-   `defaultValue`: Строка (или массив строк для `multiple={true}`). Определяет первоначально выбранный вариант.

Эти пропсы `<select>` актуальны как для неуправляемых, так и для управляемых полей выбора:

-   [`autoComplete`](https://developer.mozilla.org/docs/Web/HTML/Element/select#attr-autocomplete): Строка. Определяет один из возможных вариантов [поведения автозаполнения](https://developer.mozilla.org/docs/Web/HTML/Attributes/autocomplete#values).
-   [`autoFocus`](https://hcdev.ru/html/select/#autofocus): Булево значение. Если значение `true`, React будет фокусировать элемент на монтировании.
-   `children`: `<select>` принимает компоненты [`<option>`](https://hcdev.ru/html/option/), [`<optgroup>`](https://hcdev.ru/html/optgroup/) и [`<datalist>`](https://hcdev.ru/html/datalist/) в качестве дочерних. Вы также можете передавать собственные компоненты при условии, что они в конечном итоге отображают один из разрешенных компонентов. Если вы передаете свои собственные компоненты, которые в конечном итоге выводят теги `<option>`, каждый `<option>`, который вы выводите, должен иметь `значение`.
-   [`disabled`](https://hcdev.ru/html/select/#disabled): Булево значение. Если `true`, поле выбора не будет интерактивным и будет отображаться затемненным.
-   [`form`](https://hcdev.ru/html/select/#form): Строка. Указывает `id` формы `<form>`, к которой принадлежит это поле выбора. Если опущено, то это ближайшая родительская форма.
-   [`multiple`](https://hcdev.ru/html/select/#multiple): Булево значение. Если `true`, браузер разрешает множественный выбор.
-   [`name`](https://hcdev.ru/html/select/#name): Строка. Задает имя для этого поля выбора, которое передается вместе с формой.
-   `onChange`: Функция обработчика [`event`](components-common.md#event-handler). Требуется для управляемых полей выбора. Срабатывает немедленно, когда пользователь выбирает другой вариант. Ведет себя как событие браузера [`input`](https://developer.mozilla.org/docs/Web/API/HTMLElement/input_event).
-   `onChangeCapture`: Версия `onChange`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onInput`](https://developer.mozilla.org/docs/Web/API/HTMLElement/input_event): Функция обработчика [`event`](components-common.md#event-handler). Срабатывает немедленно, когда значение изменяется пользователем. По историческим причинам в React идиоматично использовать `onChange`, которая работает аналогично.
-   `onInputCapture`: Версия `onInput`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onInvalid`](https://developer.mozilla.org/docs/Web/API/HTMLInputElement/invalid_event): Функция обработчика [`event`](components-common.md#event-handler). Срабатывает, если ввод не прошел валидацию при отправке формы. В отличие от встроенного события `invalid`, событие React `onInvalid` вызывает всплытие.
-   `onInvalidCapture`: Версия `onInvalid`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`required`](https://hcdev.ru/html/select/#required): Булево значение. Если `true`, значение должно быть предоставлено для отправки формы.
-   [`size`](https://hcdev.ru/html/select/#size): Число. Для селектов `multiple={true}` определяет желаемое количество изначально видимых элементов.

#### Предупреждения

-   В отличие от HTML, передача атрибута `selected` в `<option>` не поддерживается. Вместо этого используйте `<select defaultValue>` для неуправляемых полей выбора и `<select value>` для управляемых полей выбора.
-   Если поле выбора получает параметр `value`, оно будет рассматриваться как управляемое.
-   Окно выбора не может быть одновременно управляемым и неуправляемым.
-   Блок выбора не может переключаться между управляемым и неуправляемым в течение своего срока службы.
-   Каждое управляемое поле выбора нуждается в обработчике события `onChange`, который синхронно обновляет его базовое значение.

## Использование

### Отображение поля выбора с опциями

Создайте `<select>` со списком компонентов `<option>` внутри для отображения поля выбора. Дайте каждому `<option>` значение `value`, представляющее данные, которые должны быть представлены в форме.

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

### Предоставление метки для поля выбора

Обычно каждый `select` помещается в тег [`<label>`](https://hcdev.ru/html/label/). Это сообщает браузеру, что данная метка связана с этим полем выбора. Когда пользователь нажимает на метку, браузер автоматически фокусирует поле выбора. Этот тег также необходим для обеспечения доступности: программа чтения с экрана будет сообщать о надписи метки, когда пользователь наведет фокус на поле выбора.

Если вы не можете вложить `select` в `<label>`, свяжите их, передав одинаковый ID в `<select id>` и [`<label htmlFor>`.](https://developer.mozilla.org/docs/Web/API/HTMLLabelElement/htmlFor) Чтобы избежать конфликтов между несколькими экземплярами одного компонента, создайте такой ID с помощью [`useId`.](useId.md)

```js
import { useId } from 'react';

export default function Form() {
    const vegetableSelectId = useId();
    return (
        <>
            <label>
                Pick a fruit:
                <select name="selectedFruit">
                    <option value="apple">Apple</option>
                    <option value="banana">Banana</option>
                    <option value="orange">Orange</option>
                </select>
            </label>
            <hr />
            <label htmlFor={vegetableSelectId}>
                Pick a vegetable:
            </label>
            <select
                id={vegetableSelectId}
                name="selectedVegetable"
            >
                <option value="cucumber">Cucumber</option>
                <option value="corn">Corn</option>
                <option value="tomato">Tomato</option>
            </select>
        </>
    );
}
```

### Предоставление первоначально выбранного варианта

По умолчанию браузер выбирает первый `<option>` в списке. Чтобы выбрать другой вариант по умолчанию, передайте `значение` этого `<option>` в качестве `defaultValue` элементу `<select>`.

```js
export default function FruitPicker() {
    return (
        <label>
            Pick a fruit:
            <select
                name="selectedFruit"
                defaultValue="orange"
            >
                <option value="apple">Apple</option>
                <option value="banana">Banana</option>
                <option value="orange">Orange</option>
            </select>
        </label>
    );
}
```

!!! note ""

    В отличие от HTML, передача атрибута `selected` отдельному `<option>` не поддерживается.

### Включение множественного выбора

Передайте `multiple={true}` в `<select>`, чтобы позволить пользователю выбрать несколько вариантов. В этом случае, если вы также указываете `defaultValue` для выбора первоначально выбранных опций, это должен быть массив.

```js
export default function FruitPicker() {
    return (
        <label>
            Pick some fruits:
            <select
                name="selectedFruit"
                defaultValue={['orange', 'banana']}
                multiple={true}
            >
                <option value="apple">Apple</option>
                <option value="banana">Banana</option>
                <option value="orange">Orange</option>
            </select>
        </label>
    );
}
```

### Чтение значения поля выбора при отправке формы

Добавьте [`<form>`](https://hcdev.ru/html/form/) вокруг вашего поля выбора с [`<button type="submit">`](https://hcdev.ru/html/button/) внутри. Это вызовет обработчик события `<form onSubmit>`. По умолчанию браузер отправит данные формы на текущий URL и обновит страницу. Вы можете отменить это поведение, вызвав `e.preventDefault()`. Считайте данные формы с помощью [`new FormData(e.target)`](https://developer.mozilla.org/docs/Web/API/FormData).

```js
export default function EditPost() {
    function handleSubmit(e) {
        // Prevent the browser from reloading the page
        e.preventDefault();
        // Read the form data
        const form = e.target;
        const formData = new FormData(form);
        // You can pass formData as a fetch body directly:
        fetch('/some-api', {
            method: form.method,
            body: formData,
        });
        // You can generate a URL out of it, as the browser does by default:
        console.log(
            new URLSearchParams(formData).toString()
        );
        // You can work with it as a plain object.
        const formJson = Object.fromEntries(
            formData.entries()
        );
        console.log(formJson); // (!) This doesn't include multiple select values
        // Or you can get an array of name-value pairs.
        console.log([...formData.entries()]);
    }

    return (
        <form method="post" onSubmit={handleSubmit}>
            <label>
                Pick your favorite fruit:
                <select
                    name="selectedFruit"
                    defaultValue="orange"
                >
                    <option value="apple">Apple</option>
                    <option value="banana">Banana</option>
                    <option value="orange">Orange</option>
                </select>
            </label>
            <label>
                Pick all your favorite vegetables:
                <select
                    name="selectedVegetables"
                    multiple={true}
                    defaultValue={['corn', 'tomato']}
                >
                    <option value="cucumber">
                        Cucumber
                    </option>
                    <option value="corn">Corn</option>
                    <option value="tomato">Tomato</option>
                </select>
            </label>
            <hr />
            <button type="reset">Reset</button>
            <button type="submit">Submit</button>
        </form>
    );
}
```

!!!note ""

    Дайте `name` вашему `<select>`, например `<select name="selectedFruit" />`. Указанное вами `name` будет использоваться в качестве ключа в данных формы, например `{ selectedFruit: "orange" }`.

    Если вы используете `<select multiple={true}>`, то [`FormData`](https://developer.mozilla.org/docs/Web/API/FormData), которые вы прочитаете из формы, будет включать каждое выбранное значение как отдельную пару имя-значение. Посмотрите внимательно на журналы консоли в примере выше.

!!!note ""

    По умолчанию _любая_ `<кнопка>` внутри `<формы>` отправит ее. Это может быть неожиданно! Если у вас есть собственный пользовательский компонент React `Button`, подумайте о возврате [`<button type="button">`](https://developer.mozilla.org/docs/Web/HTML/Element/input/button) вместо `<button>`. Затем, чтобы быть явным, используйте `<button type="submit">` для кнопок, которые _должны_ отправлять форму.

### Управление полем выбора с помощью переменной состояния

Окно выбора типа `<select />` является _неуправляемым._ Даже если вы передаете первоначально выбранное значение, например `<select defaultValue="orange" />`, ваш JSX определяет только начальное значение, а не значение в данный момент.

**Чтобы отобразить _управляемое_ поле выбора, передайте ему свойство `value`.** React заставит поле выбора всегда иметь переданное вами `value`. Обычно вы управляете полем выбора, объявляя [переменную состояния:](useState.md)

```js
function FruitPicker() {
    const [selectedFruit, setSelectedFruit] = useState(
        'orange'
    ); // Declare a state variable...
    // ...
    return (
        <select
            value={selectedFruit} // ...force the select's value to match the state variable...
            onChange={(e) =>
                setSelectedFruit(e.target.value)
            } // ... and update the state variable on any change!
        >
            <option value="apple">Apple</option>
            <option value="banana">Banana</option>
            <option value="orange">Orange</option>
        </select>
    );
}
```

Это полезно, если вы хотите заново отображать какую-то часть пользовательского интерфейса в ответ на каждый выбор.

```js
import { useState } from 'react';

export default function FruitPicker() {
    const [selectedFruit, setSelectedFruit] = useState(
        'orange'
    );
    const [selectedVegs, setSelectedVegs] = useState([
        'corn',
        'tomato',
    ]);
    return (
        <>
            <label>
                Pick a fruit:
                <select
                    value={selectedFruit}
                    onChange={(e) =>
                        setSelectedFruit(e.target.value)
                    }
                >
                    <option value="apple">Apple</option>
                    <option value="banana">Banana</option>
                    <option value="orange">Orange</option>
                </select>
            </label>
            <hr />
            <label>
                Pick all your favorite vegetables:
                <select
                    multiple={true}
                    value={selectedVegs}
                    onChange={(e) => {
                        const options = [
                            ...e.target.selectedOptions,
                        ];
                        const values = options.map(
                            (option) => option.value
                        );
                        setSelectedVegs(values);
                    }}
                >
                    <option value="cucumber">
                        Cucumber
                    </option>
                    <option value="corn">Corn</option>
                    <option value="tomato">Tomato</option>
                </select>
            </label>
            <hr />
            <p>Your favorite fruit: {selectedFruit}</p>
            <p>
                Your favorite vegetables:{' '}
                {selectedVegs.join(', ')}
            </p>
        </>
    );
}
```

!!!info ""

    **Если вы передаете `value` без `onChange`, выбор опции будет невозможен.** Когда вы управляете полем выбора, передавая ему некоторое `value`, вы _принуждаете_ его всегда иметь то значение, которое вы передали. Поэтому если вы передадите переменную состояния в качестве `значения`, но забудете синхронно обновить эту переменную состояния в обработчике события `onChange`, React будет возвращать поле выбора после каждого нажатия клавиши обратно к указанному вами `value`.

В отличие от HTML, передача атрибута `selected` отдельному `<option>` не поддерживается.
