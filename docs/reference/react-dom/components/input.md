---
description: Встроенный компонент браузера input позволяет отображать различные виды вводимых форм
---

# &lt;input&gt;

<big>Встроенный компонент браузера [`<input>`](https://hcdev.ru/html/input/) позволяет отображать различные виды вводимых форм.</big>

```js
<input />
```

## Описание {#reference}

### `<input>` {#input}

Чтобы отобразить ввод, отобразите компонент [встроенный в браузер `<input>`](https://hcdev.ru/html/input/).

```js
<input name="myInput" />
```

### Свойства {#props}

`input` поддерживает все [общие пропсы элементов](./common.md#props).

Вы можете сделать `input` управляемым, передав один из этих пропсов:

-   [`checked`](https://hcdev.ru/html/input/#checked): Булево значение. Для входа с чекбоксом или радиокнопкой контролирует, выбран ли он.
-   [`value`](https://hcdev.ru/html/input/#value): Строка. Для текстового ввода управляет его текстом. (Для радиокнопки определяет данные формы).

При передаче любого из них вы также должны передать обработчик `onChange`, который обновляет переданное значение.

Эти пропсы `input` актуальны только для неконтролируемых входов:

-   [`defaultChecked`](https://developer.mozilla.org/docs/Web/API/HTMLInputElement#defaultChecked): Булево значение. Определяет начальное значение для входов `type="checkbox"` и `type="radio"`.
-   [`defaultValue`](https://developer.mozilla.org/docs/Web/API/HTMLInputElement#defaultValue): Строка. Определяет начальное значение для текстового ввода.

Эти пропсы `input` актуальны как для неконтролируемых, так и для контролируемых входов:

-   [`accept`](https://hcdev.ru/html/input/#accept): Строка. Определяет, какие типы файлов принимаются входом `type="file"`.
-   [`alt`](https://hcdev.ru/html/input/#alt): Строка. Определяет альтернативный текст изображения для входа `type="image"`.
-   [`capture`](https://developer.mozilla.org/docs/Web/HTML/Element/input#capture): Строка. Указывает носитель (микрофон, видео или камера), захваченный входом `type="file"`.
-   [`autoComplete`](https://hcdev.ru/html/input/#autocomplete): Строка. Определяет один из возможных вариантов [поведения автозаполнения](https://developer.mozilla.org/docs/Web/HTML/Attributes/autocomplete#values).
-   [`autoFocus`](https://hcdev.ru/html/input/#autofocus): Булево значение. Если `true`, React будет фокусировать элемент на монтировании.
-   [`dirname`](https://hcdev.ru/html/input/#dirname): Строка. Указывает имя поля формы для направленности элемента.
-   [`disabled`](https://hcdev.ru/html/input/#disabled): Булево значение. Если `true`, вход не будет интерактивным и будет отображаться затемненным.
-   `children`: `input` не принимает детей.
-   [`form`](https://hcdev.ru/html/input/#form): Строка. Указывает `id` формы, к которой принадлежит этот input. Если опущено, то это ближайшая родительская форма.
-   [`formAction`](https://hcdev.ru/html/input/#formaction): Строка. Переопределяет родительское `<form action>` для `type="submit"` и `type="image"`.
-   [`formEnctype`](https://hcdev.ru/html/input/#formenctype): Строка. Переопределяет родительский `<form enctype>` для `type="submit"` и `type="image"`.
-   [`formMethod`](https://hcdev.ru/html/input/#formmethod): Строка. Переопределяет родительский `<метод формы>` для `type="submit"` и `type="image"`.
-   [`formNoValidate`](https://hcdev.ru/html/input/#formnovalidate): Строка. Переопределяет родительскую `<form noValidate>` для `type="submit"` и `type="image"`.
-   [`formTarget`](https://hcdev.ru/html/input/#formtarget): Строка. Переопределяет родительскую `<form target>` для `type="submit"` и `type="image"`.
-   [`height`](https://developer.mozilla.org/docs/Web/HTML/Element/input#height): Строка. Определяет высоту изображения для `type="image"`.
-   [`list`](https://developer.mozilla.org/docs/Web/HTML/Element/input#list): Строка. Указывает `id` `<datalist>` с опциями автозаполнения.
-   [`max`](https://hcdev.ru/html/input/#max): Число. Определяет максимальное значение числовых данных и данных времени.
-   [`maxLength`](https://hcdev.ru/html/input/#maxlength): Число. Определяет максимальную длину текстовых и других вводов.

**Предостережения**

-   Для флажков нужно `checked` (или `defaultChecked`), а не `value` (или `defaultValue`).
-   Если текстовый ввод получает строковое значение `value`, он будет рассматриваться как управляемый.
-   Если чекбокс или радиокнопка получает булево свойство `checked`, они будут рассматриваться как управляемые.
-   Вход не может быть одновременно управляемым и неуправляемым.
-   Вход не может переключаться между управляемым и неуправляемым в течение своего существования.
-   Каждый управляемый вход нуждается в обработчике события `onChange`, который синхронно обновляет его базовое значение.

## Использование {#usage}

### Отображение входов различных типов {#displaying-inputs-of-different-types}

Чтобы отобразить ввод, создайте компонент `input`. По умолчанию это будет текстовый ввод. Вы можете передать `type="checkbox"` для флажка, `type="radio"` для радиокнопки, [или один из других типов ввода.](https://developer.mozilla.org/docs/Web/HTML/Element/input#input_types)

```js
export default function MyForm() {
    return (
        <>
            <label>
                Text input: <input name="myInput" />
            </label>
            <hr />
            <label>
                Checkbox:{' '}
                <input type="checkbox" name="myCheckbox" />
            </label>
            <hr />
            <p>
                Radio buttons:
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option1"
                    />
                    Option 1
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option2"
                    />
                    Option 2
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option3"
                    />
                    Option 3
                </label>
            </p>
        </>
    );
}
```

### Предоставление метки для ввода {#providing-a-label-for-an-input}

Обычно вы помещаете каждый `input` в тег [`label`](https://hcdev.ru/html/label/). Это сообщает браузеру, что данная метка связана с этим входом. Когда пользователь нажимает на метку, браузер автоматически фокусируется на вводе. Это также необходимо для обеспечения доступности: программа чтения с экрана объявит надпись на ярлыке, когда пользователь сфокусируется на связанном вводе.

Если вы не можете вложить `input` в `label`, свяжите их, передав одинаковый ID в `<input id>` и [`<label htmlFor>`](https://developer.mozilla.org/docs/Web/API/HTMLLabelElement/htmlFor). Чтобы избежать конфликтов между несколькими экземплярами одного компонента, создайте такой ID с помощью [`useId`](../../react/useId.md).

```js
import { useId } from 'react';

export default function Form() {
    const ageInputId = useId();
    return (
        <>
            <label>
                Your first name:
                <input name="firstName" />
            </label>
            <hr />
            <label htmlFor={ageInputId}>Your age:</label>
            <input
                id={ageInputId}
                name="age"
                type="number"
            />
        </>
    );
}
```

### Предоставление начального значения для ввода {#providing-an-initial-value-for-an-input}

Вы можете опционально указать начальное значение для любого входа. Для текстовых входов передавайте его как строку `defaultValue`. Для флажков и радиокнопок начальное значение должно задаваться булевым значением `defaultChecked`.

```js
export default function MyForm() {
    return (
        <>
            <label>
                Text input:{' '}
                <input
                    name="myInput"
                    defaultValue="Some initial value"
                />
            </label>
            <hr />
            <label>
                Checkbox:{' '}
                <input
                    type="checkbox"
                    name="myCheckbox"
                    defaultChecked={true}
                />
            </label>
            <hr />
            <p>
                Radio buttons:
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option1"
                    />
                    Option 1
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option2"
                        defaultChecked={true}
                    />
                    Option 2
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option3"
                    />
                    Option 3
                </label>
            </p>
        </>
    );
}
```

### Чтение значений ввода при отправке формы {#reading-the-input-values-when-submitting-a-form}

Добавьте [`<form>`](https://hcdev.ru/html/form/) вокруг ваших входных данных с [`<button type="submit">`](https://hcdev.ru/html/button/) внутри. Это вызовет обработчик события `<form onSubmit>`. По умолчанию браузер отправит данные формы на текущий URL и обновит страницу. Вы можете отменить это поведение, вызвав `e.preventDefault()`. Считайте данные формы с помощью [`new FormData(e.target)`](https://developer.mozilla.org/docs/Web/API/FormData).

```js
export default function MyForm() {
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

        // Or you can work with it as a plain object:
        const formJson = Object.fromEntries(
            formData.entries()
        );
        console.log(formJson);
    }

    return (
        <form method="post" onSubmit={handleSubmit}>
            <label>
                Text input:{' '}
                <input
                    name="myInput"
                    defaultValue="Some initial value"
                />
            </label>
            <hr />
            <label>
                Checkbox:{' '}
                <input
                    type="checkbox"
                    name="myCheckbox"
                    defaultChecked={true}
                />
            </label>
            <hr />
            <p>
                Radio buttons:
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option1"
                    />{' '}
                    Option 1
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option2"
                        defaultChecked={true}
                    />{' '}
                    Option 2
                </label>
                <label>
                    <input
                        type="radio"
                        name="myRadio"
                        value="option3"
                    />{' '}
                    Option 3
                </label>
            </p>
            <hr />
            <button type="reset">Reset form</button>
            <button type="submit">Submit form</button>
        </form>
    );
}
```

!!!note "Дайте `name` каждому `<input>`"

    Дайте `name` каждому `<input>`, например `<input name="firstName" defaultValue="Taylor" />`. Указанное вами `name` будет использоваться в качестве ключа в данных формы, например `{ firstName: "Taylor" }`.

!!!warning "Тип `<button>`"

    По умолчанию _любая_ `<button>` внутри `<form>` отправит ее. Это может быть неожиданно! Если у вас есть собственный пользовательский компонент React `Button`, подумайте о возврате [`<button type="button">`](https://developer.mozilla.org/docs/Web/HTML/Element/input/button) вместо `<button>`. Затем, чтобы быть однозначным, используйте `<button type="submit">` для кнопок, которые _должны_ отправлять форму.

### Управление input с помощью переменной состояния {#controlling-an-input-with-a-state-variable}

Input типа `<input />` является _неуправляемым._ Даже если вы передаете начальное значение, например `<input defaultValue="Initial text" />`, ваш JSX определяет только начальное значение. Он не контролирует, каким должно быть значение в данный момент.

**Чтобы отобразить _управляемый_ вход, передайте ему свойство `value` (или `checked` для чекбоксов и радио).** React заставит вход всегда иметь переданное вами `value`. Обычно для этого объявляется [переменная состояния](../../react/useState.md):

```js hl_lines="3 7-10"
function Form() {
    // Declare a state variable...
    const [firstName, setFirstName] = useState('');
    // ...
    return (
        <input
            // ...force the input's value to match the state variable...
            value={firstName}
            // ... and update the state variable on any edits!
            onChange={(e) => setFirstName(e.target.value)}
        />
    );
}
```

Контролируемый ввод имеет смысл, если вам все равно нужно состояние - например, для повторного отображения пользовательского интерфейса при каждом редактировании:

```js hl_lines="2 14-16"
function Form() {
    const [firstName, setFirstName] = useState('');
    return (
        <>
            <label>
                First name:
                <input
                    value={firstName}
                    onChange={(e) =>
                        setFirstName(e.target.value)
                    }
                />
            </label>
            {firstName !== '' && (
                <p>Your name is {firstName}.</p>
            )}
            ...
        </>
    );
}
```

Это также полезно, если вы хотите предложить несколько способов изменения состояния ввода (например, нажатием кнопки):

```js hl_lines="3-4 10-11 14-16"
function Form() {
    // ...
    const [age, setAge] = useState('');
    const ageAsNumber = Number(age);
    return (
        <>
            <label>
                Age:
                <input
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    type="number"
                />
                <button
                    onClick={() => setAge(ageAsNumber + 10)}
                >
                    Add 10 years
                </button>
            </label>
        </>
    );
}
```

Значение `value`, которое вы передаете управляемым компонентам, не должно быть `undefined` или `null`. Если вам нужно, чтобы начальное значение было пустым (как в случае с полем `firstName` ниже), инициализируйте переменную состояния пустой строкой (`''`).

=== "App.js"

    ```js
    import { useState } from 'react';

    export default function Form() {
    	const [firstName, setFirstName] = useState('');
    	const [age, setAge] = useState('20');
    	const ageAsNumber = Number(age);
    	return (
    		<>
    			<label>
    				First name:
    				<input
    					value={firstName}
    					onChange={(e) =>
    						setFirstName(e.target.value)
    					}
    				/>
    			</label>
    			<label>
    				Age:
    				<input
    					value={age}
    					onChange={(e) => setAge(e.target.value)}
    					type="number"
    				/>
    				<button
    					onClick={() => setAge(ageAsNumber + 10)}
    				>
    					Add 10 years
    				</button>
    			</label>
    			{firstName !== '' && (
    				<p>Your name is {firstName}.</p>
    			)}
    			{ageAsNumber > 0 && (
    				<p>Your age is {ageAsNumber}.</p>
    			)}
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/k5h8fm?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

!!!info "Если вы передадите `value` без `onChange`, то ввод будет невозможен"

    Когда вы управляете вводом, передавая ему некоторое `value`, вы _принуждаете_ его всегда иметь то значение, которое вы передали. Поэтому если вы передадите переменную состояния в качестве `value`, но забудете синхронно обновить эту переменную состояния в обработчике события `onChange`, React будет возвращать ввод после каждого нажатия клавиши к указанному вами `value`.

### Оптимизация повторного рендеринга при каждом нажатии клавиши {#optimizing-re-rendering-on-every-keystroke}

Когда вы используете управляемый ввод, вы устанавливаете состояние при каждом нажатии клавиши. Если компонент, содержащий ваше состояние, перерисовывает большое дерево, это может стать медленным. Есть несколько способов оптимизировать производительность повторного рендеринга.

Например, предположим, вы начинаете с формы, которая при каждом нажатии клавиши перерисовывает все содержимое страницы:

```js hl_lines="5-13"
function App() {
    const [firstName, setFirstName] = useState('');
    return (
        <>
            <form>
                <input
                    value={firstName}
                    onChange={(e) =>
                        setFirstName(e.target.value)
                    }
                />
            </form>
            <PageContent />
        </>
    );
}
```

Поскольку `<PageContent />` не зависит от состояния ввода, вы можете перенести состояние ввода в свой собственный компонент:

```js hl_lines="4 10-22"
function App() {
    return (
        <>
            <SignupForm />
            <PageContent />
        </>
    );
}

function SignupForm() {
    const [firstName, setFirstName] = useState('');
    return (
        <form>
            <input
                value={firstName}
                onChange={(e) =>
                    setFirstName(e.target.value)
                }
            />
        </form>
    );
}
```

Это значительно повышает производительность, поскольку теперь только `SignupForm` рендерится при каждом нажатии клавиши.

Если нет возможности избежать повторного рендеринга (например, если `PageContent` зависит от значения поискового ввода), [`useDeferredValue`](../../react/useDeferredValue.md#deferring-re-rendering-for-a-part-of-the-ui) позволяет сохранить отзывчивость управляемого ввода даже в середине большого повторного рендеринга.

## Устранение неполадок {#troubleshooting}

### Мой текстовый ввод не обновляется, когда я ввожу текст {#my-text-input-doesnt-update-when-i-type-into-it}

Если вы отображаете ввод с `value`, но без `onChange`, вы увидите ошибку в консоли:

```js
// 🔴 Bug: controlled text input with no onChange handler
<input value={something} />
```

!!!danger "Ошибка"

    Вы предоставили свойство `value` полю формы без обработчика `onChange`. Это приведет к тому, что поле будет доступно только для чтения. Если поле должно быть изменяемым, используйте `defaultValue`. В противном случае установите либо `onChange`, либо `readOnly`.

Как следует из сообщения об ошибке, если вы хотите указать только _начальное_ значение, передайте `defaultValue` вместо этого:

```js
// ✅ Good: uncontrolled input with an initial value
<input defaultValue={something} />
```

Если вы хотите управлять этим входом с помощью переменной состояния, укажите обработчик `onChange`:

```js
// ✅ Good: controlled input with onChange
<input
    value={something}
    onChange={(e) => setSomething(e.target.value)}
/>
```

Если значение намеренно предназначено только для чтения, добавьте параметр `readOnly`, чтобы подавить ошибку:

```js
// ✅ Good: readonly controlled input without on change
<input value={something} readOnly={true} />
```

### Мой флажок не обновляется, когда я нажимаю на него {#my-checkbox-doesnt-update-when-i-click-on-it}

Если вы отобразите флажок с `checked`, но без `onChange`, вы увидите ошибку в консоли:

```js
// 🔴 Bug: controlled checkbox with no onChange handler
<input type="checkbox" checked={something} />
```

!!!danger "Ошибка"

    Вы предоставили свойство `checked` полю формы без обработчика `onChange`. Это приведет к тому, что поле будет доступно только для чтения. Если поле должно быть изменяемым, используйте `defaultChecked`. В противном случае установите либо `onChange`, либо `readOnly`.

Как следует из сообщения об ошибке, если вы хотите только указать _начальное_ значение, передайте `defaultChecked` вместо этого:

```js
// ✅ Good: uncontrolled checkbox with an initial value
<input type="checkbox" defaultChecked={something} />
```

Если вы хотите управлять этим флажком с помощью переменной состояния, укажите обработчик `onChange`:

```js
// ✅ Good: controlled checkbox with onChange
<input
    type="checkbox"
    checked={something}
    onChange={(e) => setSomething(e.target.checked)}
/>
```

!!!note ""

    Для флажков нужно читать `e.target.checked`, а не `e.target.value`.

Если флажок намеренно предназначен только для чтения, добавьте параметр `readOnly`, чтобы подавить ошибку:

```js
// ✅ Good: readonly controlled input without on change
<input
    type="checkbox"
    checked={something}
    readOnly={true}
/>
```

### Мой каретка ввода перескакивает в начало при каждом нажатии клавиши {#my-input-caret-jumps-to-the-beginning-on-every-keystroke}

Если вы управляете вводом, вы должны обновить его переменную состояния до значения ввода из DOM во время `onChange`.

Вы не можете обновить ее до значения, отличного от `e.target.value` (или `e.target.checked` для флажков):

```js
function handleChange(e) {
    // 🔴 Bug: updating an input to something other than e.target.value
    setFirstName(e.target.value.toUpperCase());
}
```

Вы также не можете обновлять его асинхронно:

```js
function handleChange(e) {
    // 🔴 Bug: updating an input asynchronously
    setTimeout(() => {
        setFirstName(e.target.value);
    }, 100);
}
```

Чтобы исправить свой код, обновите его синхронно с `e.target.value`:

```js
function handleChange(e) {
    // ✅ Updating a controlled input to e.target.value synchronously
    setFirstName(e.target.value);
}
```

Если это не устраняет проблему, возможно, что ввод удаляется и добавляется из DOM при каждом нажатии клавиши. Это может произойти, если вы случайно [сбрасываете состояние](../../../learn/preserving-and-resetting-state.md) при каждом повторном рендере, например, если `input` или один из его родителей всегда получает другой атрибут `key`, или если вы вложены определения функций компонентов (что не поддерживается и приводит к тому, что "внутренний" компонент всегда считается другим деревом).

### Я получаю ошибку: "Компонент изменяет неконтролируемый вход на контролируемый" {#im-getting-an-error-a-component-is-changing-an-uncontrolled-input-to-be-controlled}

Если вы передаете компоненту `value`, оно должно оставаться строкой в течение всего времени его работы.

Вы не можете сначала передать `value={undefined}`, а затем передать `value="some string"`, потому что React не будет знать, хотите ли вы, чтобы компонент был неуправляемым или управляемым. Управляемый компонент всегда должен получать строковое `value`, а не `null` или `undefined`.

Если ваше `value` приходит из API или переменной состояния, оно может быть инициализировано в `null` или `undefined`. В этом случае либо изначально установите его в пустую строку (`''`), либо передайте `value={someValue ?? ''}`, чтобы убедиться, что `value` является строкой.

Аналогично, если вы передаете `checked` флажку, убедитесь, что это всегда булево значение.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components/input](https://react.dev/reference/react-dom/components/input)</small>
