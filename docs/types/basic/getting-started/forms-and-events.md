---
description: Если производительность не является проблемой (а обычно это не так!), инлайнить обработчики проще всего, поскольку вы можете просто использовать вывод типов и контекстную типизацию
---

# Формы и события

Если производительность не является проблемой (а обычно это не так!), инлайнить обработчики проще всего, поскольку вы можете просто использовать [вывод типов и контекстную типизацию](https://www.typescriptlang.org/docs/handbook/type-inference.html#contextual-typing):

```ts
const el = (
    <button
        onClick={(event) => {
            /* event will be correctly typed automatically! */
        }}
    />
);
```

Но если вам нужно определить обработчик события отдельно, инструменты IDE придутся как нельзя кстати, поскольку определения `@type` содержат множество вариантов ввода. Введите то, что вы ищете, и обычно автозаполнение поможет вам. Вот как это выглядит для `onChange` для события формы:

```ts
type State = {
    text: string;
};
class App extends React.Component<Props, State> {
    state = {
        text: '',
    };

    // typing on RIGHT hand side of =
    onChange = (
        e: React.FormEvent<HTMLInputElement>
    ): void => {
        this.setState({ text: e.currentTarget.value });
    };
    render() {
        return (
            <div>
                <input
                    type="text"
                    value={this.state.text}
                    onChange={this.onChange}
                />
            </div>
        );
    }
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCtAGxQGc64BBMMOJADxiQDsATRsnQwAdAGFckHrxgAeCnDgBvAL4AaBcs2KA9Drg8IcMDjB1tcblwBccOjCjAeAcwDcmlRQB8W8ovso3HAAvL6KilYwtgBE0R7ulH5wepYAnmBOznAQPIgAkgDiABIAKnAAFij8dsB8SNmYIZo5YpUu9aEAFEi2QhgiAGLQIACiAG4ysqUAsgAyeTxgAK4wI9RIIDJeAJS2YxC1IT5KFjDlwHQidEgwAMowgUidSpacUewiaEtQRDwwJSgoM4biIxihqEt6iptglFCpYXBfnUoJ1tmFwkQYN9cp0LIpZHxgGMvHjwrInMt4DB0khgtFItE4GCIbSlGcLlcHtwRJEVNkeK0qsDgmzzpcWm1gXydCSkuE4LIdITiRYYR4KCogA)

Вместо того чтобы вводить аргументы и возвращаемые значения с помощью `React.FormEvent<>` и `void`, вы можете альтернативно применить типы к самому обработчику события (_внесено @TomasHubelbauer_):

```ts
// typing on LEFT hand side of =
onChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
	this.setState({text: e.currentTarget.value})
}
```

!!!info "Зачем делать одно и то же двумя способами?"

    Первый метод использует сигнатуру инферентного метода `(e: React.FormEvent<HTMLInputElement>): void`, а второй метод принудительно использует тип делегата, предоставляемый `@types/react`. Таким образом, `React.ChangeEventHandler<>` - это просто "благословенная" типизация от `@types/react`, в то время как вы можете думать об инферированном методе как о более... _кустарно обработанным_. В любом случае, это хороший паттерн, который нужно знать. [Подробнее см. наш PR на Github](https://github.com/typescript-cheatsheets/react/pull/24).

**Типизация события onSubmit с неконтролируемыми компонентами в форме**.

Если вам не очень важен тип события, вы можете просто использовать `React.SyntheticEvent`. Если ваша целевая форма имеет пользовательские именованные входы, к которым вы хотите получить доступ, вы можете использовать утверждение типа:

```ts
<form
    ref={formRef}
    onSubmit={(e: React.SyntheticEvent) => {
        e.preventDefault();
        const target = e.target as typeof e.target & {
            email: { value: string };
            password: { value: string };
        };
        const email = target.email.value; // typechecks!
        const password = target.password.value; // typechecks!
        // etc...
    }}
>
    <div>
        <label>
            Email:
            <input type="email" name="email" />
        </label>
    </div>
    <div>
        <label>
            Password:
            <input type="password" name="password" />
        </label>
    </div>
    <div>
        <input type="submit" value="Log in" />
    </div>
</form>
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCtCAOwGctoRlM4BeRYmAOgFc6kLABQBKClVoM4AMSbs4o9gD4FFOHAA8mJmrhFMbAN7aozJJgC+u2gGVeAIxDAYRoUgBcndDxsBPGjAAFkgwwGgAogBuSAEiynCGuupI3GBE0QEAIuYovAA2MKIA3Elw1PTwMChQAOYh8ilVtfUodHAwvmBIEKyN1XXwAGQJpckgKMB5noZwkSh5vB5wDFDANDVwFiXk6rtwYK10AO7QACbTs-OLnitrG1ulDzu75VJI45PyTQPc7xN53DmCyQRTgAHowe1Okg0ME0ABrOgAQlKr3gBzoxzOX36IVShxOUFOgKuIPBkI6XVhMMRKOe6ghcBCaG4rN0Fis5CUug0p2AkW59M0eRQ9iQeUFe3U4Q+U1GmjWYF4lWhbAARH9Jmq4DQUCAkOrNXltWDJbsNGCRWKJTywXyBTz7Wb1BoreLnbsAAoEs7ueUaRXKqFddUYrFE7W6-Whn0R8Eei1um3PC1Ox38hOBlUhtV0BxOGDaoGLdUAGQgGzWJrNqYzFAtJhAgpEQA)

Конечно, если вы создаете какую-то значимую форму, [вам следует использовать Formik](https://jaredpalmer.com/formik) или [React Hook Form](https://react-hook-form.com/), которые написаны на TypeScript.

## Список типов событий

| Тип события      | Описание                                                                                                                                                                                                                                                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnimationEvent   | CSS Анимации.                                                                                                                                                                                                                                                                                                               |
| ChangeEvent      | Изменение значения элемента `<input>`, `<select>` и `<textarea>`.                                                                                                                                                                                                                                                           |
| ClipboardEvent   | Использование событий копирования, вставки и вырезания.                                                                                                                                                                                                                                                                     |
| CompositionEvent | События, которые происходят из-за непрямого ввода текста пользователем (например, в зависимости от настроек браузера и компьютера может появиться всплывающее окно с дополнительными символами, если вы, например, хотите набрать японский язык на американской клавиатуре).                                                |
| DragEvent        | Перетаскивание с помощью устройства-указателя (например, мыши).                                                                                                                                                                                                                                                             |
| FocusEvent       | Событие, которое происходит, когда элементы получают или теряют фокус.                                                                                                                                                                                                                                                      |
| FormEvent        | Событие, которое происходит всякий раз, когда форма или элемент формы получает/теряет фокус, значение элемента формы изменяется или форма отправляется.                                                                                                                                                                     |
| InvalidEvent     | Возникает, когда ограничения валидности ввода не проходят (например, `<input type="number" max="10">` и кто-то вводит число 20).                                                                                                                                                                                            |
| KeyboardEvent    | Взаимодействие пользователя с клавиатурой. Каждое событие описывает взаимодействие с одной клавишей.                                                                                                                                                                                                                        |
| MouseEvent       | События, которые происходят из-за взаимодействия пользователя с указательным устройством (например, мышью)                                                                                                                                                                                                                  |
| PointerEvent     | События, которые происходят при взаимодействии пользователя с различными указывающими устройствами, такими как мышь, перо/стилус, сенсорный экран, а также поддерживающими мультитач. Если вы не разрабатываете для старых браузеров (IE10 или Safari 12), рекомендуется использовать события указателя. Расширяет UIEvent. |
| TouchEvent       | События, которые происходят из-за взаимодействия пользователя с сенсорным устройством. Расширяет UIEvent.                                                                                                                                                                                                                   |
| TransitionEvent  | Переход CSS. Не полностью поддерживается браузером. Расширяет UIEvent.                                                                                                                                                                                                                                                      |
| UIEvent          | Базовое событие для событий мыши, касания и указателя.                                                                                                                                                                                                                                                                      |
| WheelEvent       | Прокрутка на колесике мыши или аналогичном устройстве ввода. ( Примечание: событие `wheel` не следует путать с событием `scroll`)                                                                                                                                                                                           |
| SyntheticEvent   | Базовое событие для всех вышеперечисленных событий. Следует использовать, если нет уверенности в типе события                                                                                                                                                                                                               |

!!!info "А как насчет `InputEvent`?"

    Вы, вероятно, заметили, что здесь нет `InputEvent`. Это потому, что оно не поддерживается Typescript, так как само событие не имеет полной браузерной поддержки и может вести себя по-разному в разных браузерах. Вместо этого вы можете использовать `KeyboardEvent`.

    Источники:

    -   <https://github.com/microsoft/TypeScript/issues/29441>
    -   <https://developer.mozilla.org/en-US/docs/Web/API/InputEvent>
    -   <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event>

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/forms_and_events></small>
