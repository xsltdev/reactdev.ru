# Неуправляемые компоненты

В большинстве случаев при работе с формами мы рекомендуем использовать [управляемые компоненты](forms.md). В управляемом компоненте, данные формы обрабатываются React-компонентом. В качестве альтернативы можно использовать неуправляемые компоненты. Они хранят данные формы прямо в DOM.

Вместо того, чтобы писать обработчик события для каждого обновления состояния, вы можете использовать неуправляемый компонент и читать значения из DOM через [реф](refs-and-the-dom.md).

Вот так, к примеру, обработчик неуправляемого компонента может получить имя от элемента `input`:

```javascript
class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.input = React.createRef();
  }

  handleSubmit(event) {
    alert('Отправленное имя: ' + this.input.current.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Имя:
          <input type="text" ref={this.input} />
        </label>
        <input type="submit" value="Отправить" />
      </form>
    );
  }
}
```

[**Посмотреть на CodePen**](https://codepen.io/gaearon/pen/WooRWa?editors=0010)

Неуправляемые компоненты опираются на DOM в качестве источника данных и могут быть удобны при интеграции React с кодом, не связанным с React. Количество кода может уменьшиться, правда, за счёт потери в его чистоте. Поэтому в обычных ситуациях мы рекомендуем использовать управляемые компоненты.

Если всё ещё остаётся неясным, какой тип компонента лучше использовать в конкретной ситуации, то, возможно, [статья про сравнение управляемых и неуправляемых полях ввода](https://goshakkk.name/controlled-vs-uncontrolled-inputs-react/) окажется полезной.

## Значения по умолчанию {#default-values}

На этапе рендеринга атрибут `value` полей ввода переопределяет значение в DOM. С неуправляемым компонентом зачастую нужно, чтобы React определил первоначальное значение, но впоследствии ничего не делал с ним. В этом случае необходимо определить атрибут `defaultValue` вместо `value`.

```javascript
render() {
  return (
    <form onSubmit={this.handleSubmit}>
      <label>
        Имя:
        <input
          defaultValue="Боб"
          type="text"
          ref={this.input} />
      </label>
      <input type="submit" value="Отправить" />
    </form>
  );
}
```

Аналогично, `<input type="checkbox">` и `<input type="radio">` используют `defaultChecked`, а `<select>` и `<textarea>` — `defaultValue`.

## Тег поля загрузки файла {#the-file-input-tag}

HTML-тег `<input type="file">` позволяет пользователю выбрать один или несколько файлов из дискового устройства, чтобы загрузить их на сервер, либо управлять ими с помощью JavaScript через [File API](https://developer.mozilla.org/ru/docs/Web/API/File/Using_files_from_web_applications).

```html
<input type="file" />
```

В React `<input type="file">` всегда является неуправляемым компонентом, потому что его значение может быть установлено только пользователем, а не программным путём.

Для взаимодействия с файлами следует использовать File API. В следующем примере показано, как создать [реф на DOM-узел](refs-and-the-dom.md), чтобы затем получить доступ к файлам в обработчике отправки формы:

```js
class FileInput extends React.Component {
  constructor(props) {
    // highlight-range{3}
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
  }
  handleSubmit(event) {
    // highlight-range{3}
    event.preventDefault();
    alert(
      `Selected file - ${this.fileInput.current.files[0].name}`
    );
  }

  render() {
    // highlight-range{5}
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Upload file:
          <input type="file" ref={this.fileInput} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    );
  }
}

ReactDOM.render(
  <FileInput />,
  document.getElementById('root')
);
```
