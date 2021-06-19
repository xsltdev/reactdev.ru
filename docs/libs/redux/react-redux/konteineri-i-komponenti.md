# Контейнеры и компоненты

Прежде чем мы разобьем `App.js` на компоненты `<User />` и `<Page />` хотелось бы отметить про способ разделения на "компоненты" и "контейнеры", иначе называемый: деление на "глупые" и "умные" компоненты, "Presentational" и "Container" и быть может как-то еще.

Позволю себе в очередной раз прибегнуть к офф.документации и перевести таблицу различий, которая отлично и кратко отражает суть.

|                       | Компонент (глупый)                 | Контейнер (умный)                                         |
| --------------------- | ---------------------------------- | --------------------------------------------------------- |
| Цель                  | Как это выглядит (разметка, стили) | Как это работает (получение данных, обновление состояния) |
| Осведомлен о Redux    | Нет                                | Да                                                        |
| Для считывания данных | Читает данные из props             | Подписан на Redux state (состояние)                       |
| Для изменения данных  | Вызывает callback из props         | Отправляет (dispatch) Redux действие (actions)            |
| Пишутся               | Вручную                            | Обычно, генерируются Redux                                |

Магия таблиц обычно проявляется не сразу. Если переписать наше приложение, а потом взглянуть сюда еще раз - многое станет гораздо яснее. Предлагаю так и поступить. Поехали!

Установим `prop-types` и создадим компоненты.

```
npm install --save prop-types
```

_src/components/User.js_

```js
import React from 'react';
import PropTypes from 'prop-types';

export class User extends React.Component {
  render() {
    const { name } = this.props;
    return (
      <div>
        <p>Привет, {name}!</p>
      </div>
    );
  }
}

User.propTypes = {
  name: PropTypes.string.isRequired,
};
```

_src/components/Page.js_

```js
import React from 'react';
import PropTypes from 'prop-types';

export class Page extends React.Component {
  render() {
    const { year, photos } = this.props;
    return (
      <div>
        <p>
          У тебя {photos.length} фото за {year} год
        </p>
      </div>
    );
  }
}

Page.propTypes = {
  year: PropTypes.number.isRequired,
  photos: PropTypes.array.isRequired,
};
```

Наш файл `App.js` - это контейнер (так как подключен к redux). Изменим-с...

_src/containers/App.js_

```js
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { User } from '../components/User';
import { Page } from '../components/Page';

import './App.css';

class App extends Component {
  render() {
    const { user, page } = this.props;
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Мой топ фото</h1>
        </header>
        <User name={user.name} />
        <Page photos={page.photos} year={page.year} />
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return {
    user: store.user,
    page: store.page,
  };
};

export default connect(mapStateToProps)(App);
```

Не забудьте так же перенести `App.css` в `src/containers` и поменять подключение `<App />` в `index.js`:

```js
import App from './containers/App'; // изменили путь
```

Так же удалите файл с тестом - `App.test.js`, так как тесты в данный момент не входят в нашу программу, но возможно, будут добавлены в конце в раздел рецептов.

Итого: изучили на практике деление на компоненты и контейнеры.

[Исходный код](https://github.com/maxfarseer/redux-course-ru-v2/tree/chp6-conteiners-and-components)
