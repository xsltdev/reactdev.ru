# Подключаем redux

```
npm i --save redux react-redux
npm i --save-dev redux-logger redux-thunk
```

(вы всегда можете проверить версии в `package.json`, если что-то вдруг перестало работать. "Мир реакт" активно развивается)

Нам необходимо подговиться для решения следующей задачи:

Пользователь кликает на "Админка".

- Если пользователь залогинен - пропускаем его на страницу
- Если пользователь не залогинен - отправлям его на страницу логина

При чем здесь `redux`? Разве такую задачу мы уже не решили с помощью хука на `onEnter`?

Это отличный вопрос! Делайте так, как необходимо для приложения, а не просто тащите в проект все модные технологии. Тем не менее, у нашей задачи есть свои цели:

- во время логина мы сделаем задержку (как будто ждем ответ от сервера), и лишь когда пришел ответ - перенаправим браузер пользователя на `/admin`
- роутинг будет выполняться посредством `store.dispatch`

В итоге, решив данную задачу, у вас будет четкое понимание как сделать любой подобный запрос с редиректом, ведь по факту все сводится к одному и тому же: когда получен ответ - сделай редирект.

(код ниже выполнять не обязательно, так как можно взять исходный код в конце раздела.)

Для начала работы с нашим приложением, необходимо внести множество изменений. Для тех, кто знаком с redux - ничего нового. Тезисно и частично с кодом привожу здесь, так как, возможно вы читаете в формате книги вдали от ПК и хотите повторить какие-то моменты связанные с подключением redux в проект:

Обернем `<Router />` в `<Provider />`

_src/index.js_

```js
...
import { Provider } from 'react-redux'
import configureStore from './store/configureStore'
...

const store = configureStore()

render(
  <Provider store={store}>
    <Router history={browserHistory} routes={routes} />
  </Provider>,
  document.getElementById('root')
)
```

создаем константы для пользователя

_src/constants/User.js_

```js
export const LOGIN_REQUEST = 'LOGIN_REQUEST'
export const LOGIN_FAIL = 'LOGIN_FAIL'
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
export const LOGOUT_SUCCES = 'LOGOUT_SUCCESS'
```

создаем actions для пользователя

_src/actions/UserActions.js_

```js
/* eslint-disable no-unused-vars */

import {
  LOGIN_REQUEST,
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  LOGOUT_SUCCESS,
} from '../constants/User'

export function login(payload) {
  // TODO
  return {
    type: LOGIN_REQUEST,
  }
}

export function logout() {
  return {
    type: LOGOUT_SUCCESS,
  }
}

/* eslint-enable no-unused-vars */
```

создаем reducer для пользователя

_src/reducers/user.js_

```js
import {
  LOGIN_REQUEST,
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  LOGOUT_SUCCESS,
} from '../constants/User'

const initialState =
  JSON.parse(window.localStorage.getItem('rr_user')) || {}

export default function userstate(
  state = initialState,
  action
) {
  switch (action.type) {
    case LOGIN_REQUEST:
      // TODO
      return {}

    case LOGIN_SUCCESS:
      // TODO
      return {}

    case LOGIN_FAIL:
      // TODO
      return {}

    case LOGOUT_SUCCESS:
      // TODO
      return {}

    default:
      return state
  }
}
```

Сразу создадим файл с главным редьюсером, где в будущем сможем "скомбинировать" больше редьюсеров (на данный момент у нас только один)

_src/reducers/index.js_

```js
import { combineReducers } from 'redux'
import user from './user'
import popup from './popup'

export const rootReducer = combineReducers({
  user,
  popup,
})
```

конфигурируем store и добавляем несколько middleware (logger - для логов и thunk - для асинхронных запросов)

_src/sotre/configureStore_

```js
import {
  createStore,
  applyMiddleware,
  compose,
} from 'redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import { rootReducer } from '../reducers'

export default function configureStore() {
  const store = compose(
    applyMiddleware(thunkMiddleware),
    applyMiddleware(createLogger())
  )(createStore)(rootReducer)

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('../reducers', () => {
      const nextRootReducer = require('../reducers')
        .rootReducer
      store.replaceReducer(nextRootReducer)
    })
  }

  return store
}
```

превратим "тупой компонет" `<Login />` в "умный компонент" `<LoginPage />` (то есть подключим его (`connect`))

_src/containers/LoginPage/index.js_

```js
import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as UserActions from '../../actions/UserActions'

export class LoginPage extends Component {
  handleSubmit(e) {
    e.preventDefault()
    this.props.actions.login({
      name: e.target.elements[0].value,
    })
  }
  render() {
    return (
      <div className="row">
        <div className="col-md-12">
          <form
            className="form-inline"
            onSubmit={::this.handleSubmit}
          >
            <input
              className="form-control"
              type="text"
              placeholder="login"
            />{' '}
            <button
              className="btn btn-primary"
              type="submit"
            >
              Войти
            </button>
          </form>
        </div>
      </div>
    )
  }
}

function mapStateToProps() {
  return {}
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(UserActions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginPage)
```

Обратите внимание, что мы стали передавать объект `user`

```js
{
  name: логин
}
```

До этого момента, мы передавали строку с именем. Так же немного изменилось оформление компонента.

В `routes.js` изменили подключение `<Login />` на `<LoginPage />`

В будущем вы сможете добавить юзерам роль в проекте и так далее.

На всякий случай, напоминаю, что:

```js
;::this.handleSubmit
```

Эквивалентно

```js
this.handleSubmit.bind(this)
```

Итого: мы подключили redux, создав необходимый каркас для дальнейшей деятельности.

Исходный код на текущий момент. Не забудьте скачать новые зависимости:

```
npm install
```

и очистить `localStorage`

```
localStorage.clear() //выполняется из консоли хрома, например
```
