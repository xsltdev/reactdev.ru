# Точка входа

Подтянем Redux и `react-redux` в наш проект:

```
npm i redux react-redux --save
```

Точка входа в наше приложение - `src/index.js`

Обновим его содержимое:

_src/index.js_

```js
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import App from './App';

import registerServiceWorker from './registerServiceWorker';

import './index.css';

const store = createStore(() => {}, {}); // [1]

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
registerServiceWorker();
```

Итак, первый компонент из мира Redux - `<Provider />`.

Благодаря этому компоненту, мы сможем получать необходимые данные из `store` нашего приложения, если воспользуемся вспомогательной функцией `connect`, речь о которой пойдет далее. Сейчас нам и получать нечего, так как `store` у нас - пустой объект.

Давайте подробнее посмотрим на строку 1:

```js
const store = createStore(() => {}, {});
```

Во-первых, если вам трудно читать ES2015 код, то переводите его в привычный ES5, с помощью [babel-playground](https://babeljs.io/repl/).

На скриншоте ниже: слева - современный код, справа - старый ES5 код, после преобразования.

![babel создание store](create-store-babel.jpg)

Во-вторых, давайте взглянем на документацию метода [createStore](https://redux.js.org/api/createstore): принимает один обязательный аргумент (функцию `reducer`) и парочку не обязательных (начальное состояние и "усилители").

Теперь переведем то, что мы написали, когда присваивали `store`:

> Возьми пустую анонимную функцию в качестве редьюсера и пустой объект в качестве начального состояния. Если коротко: возьми ничего и "ничего" не делай.

Предлагаю вынести создание `store` в отдельный файл, так как в нем мы добавим позже несколько строк кода, в том числе, добавим усилителей (`enhancers`).

_src/store/configureStore.js_

```js
import { createStore } from 'redux';

export const store = createStore(() => {}, {});
```

Поправить импорт в индексе:

_src/index.js_

```js
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { store } from './store/configureStore'; // исправлено
import App from './App';

import registerServiceWorker from './registerServiceWorker';

import './index.css';

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
registerServiceWorker();
```

Усилители - это middleware функции. Если читатель знаком с [express.js](http://expressjs.com/), то он знаком с усилителями в redux. Для остальных: типичный усилитель - логгер (`logger`), который просто пишет в консоль все что происходит с наблюдаемым объектом.

Давайте так же исправим `App.js`, чтобы обозначить чем мы тут с вами занимаемся:

```js
import React, { Component } from 'react';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Мой топ фото</h1>
        </header>
        <p className="App-intro">
          Здесь будут мои самые залайканые фото
        </p>
      </div>
    );
  }
}

export default App;
```

![Консоль с Provider](app-inside-provider.jpg)

Итого: мы настроили точку входа для redux-приложения (`src/index.js`), в которой обернули все в `<Provider />`. Так же вынесли для будущего удобства настройку `store` в отдельный файл.

[Исходный код](https://github.com/maxfarseer/redux-course-ru-v2/tree/chp3-entry-point)
