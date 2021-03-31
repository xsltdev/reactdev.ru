# Подключаем react-router

Продолжим разбирать страницу [официального туториала](https://github.com/reactjs/react-router/blob/latest/docs/Introduction.md).

Сейчас код компонента `<App />` не выглядит слишком сложным. Но если развивать идею роутинга, появятся другие URL-адреса, что-то вложится во что-то большее... появится больше ссылок...

Скорее всего, нас ожидает трудноподдерживаемая путаница. Поэтому `react-router` с одной стороны можно рассматривать как "высокоуровневую" абстракцию, а с другой - полезный "плагин" с массой дополнительных плюшек. Давайте установим его и перепишем наш простой пример, который как обычно, в силу своей простоты, покажется несколько раздутым из-за использования react-router'а.

```bash
npm i react-router --save
```

_src/index.js_

```js
import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import App from './containers/App'
import Admin from './components/Admin'
import Genre from './components/Genre'
import Home from './components/Home'

import {
  Router,
  Route,
  IndexRoute,
  browserHistory,
} from 'react-router'

render(
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={Home} />
      <Route path="admin" component={Admin} />
      <Route path="genre" component={Genre} />
    </Route>
  </Router>,
  document.getElementById('root')
)
```

Мы перенесли `import` компонентов в `index.js`, а ниже указали роуты. Обратите внимание, на `<IndexRoute />` - так задается роут для "корня" (то есть для `/`, еще можно сказать - `http://localhost:3000`).

Так же, здесь мы использовали одну из главных фишек react-router'a - "вложения" (nesting). Мы вложили `admin` и `genre` в `/`, поэтому чтобы компоненты были доступны по соответствующим "урлам" (URL-адресам), осталось лишь выводить их как "потомков":

_src/containers/App.js_

```js
import React, { Component } from 'react'
import { Link } from 'react-router'

export default class App extends Component {
  render() {
    return (
      <div className="container">
        <h1>App</h1>
        <ul>
          <li>
            <Link to="/admin">Admin</Link>
          </li>
          <li>
            <Link to="/genre">Genre</Link>
          </li>
        </ul>
        {/* добавили вывод потомков */}
        {this.props.children}
      </div>
    )
  }
}
```

Согласно документации, мы также заменили `<a></a>` на компонент реакт-роутера - `<Link />`.

Код реакт-роутера хорошо читается и не изобилует новыми терминами. В следующей главе - продолжим настройку.

**Итого**: мы подключили react-router, посмотрели как назначается компонент на "корень" сайта, а так же познакомились с компонентом `<Link />`.

[Исходный код](https://github.com/maxfarseer/react-router-ru-tutorial/tree/add_react-router) на данный момент.

## Задача

Если бы у нас был компонент `<BanList />`, доступный по адресу: `http://localhost:3000/admin/banlist`, как мог бы выглядеть роутер?

## Решение

```js
render(
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={Home} />
      <Route path="admin" component={Admin}>
        <Route path="banlist" component={BanList} />
      </Route>
      <Route path="genre" component={Genre} />
    </Route>
  </Router>,
  document.getElementById('root')
)
```
