# Программируем переходы

Давайте рассмотрим очень "выдуманный пример":

На главной странице у нас есть форма, в которой мы можем написать любой жанр. По кнопке - перейти - мы попадаем по адресу:

```
http://localhost:3000/genre/жанр_из_формы/
```

Динамический роут `/genre/:genre` - как раз позволит нам это.

Практической пользы в этом никакой, но так мы рассмотрим переходы "программно" на деле.

Реальная задача вас ждет уже в следующей главе, но мне бы хотелось, чтобы после решения данного выдуманного примера вы с легкостью решили ее самостоятельно.

Приступим:

_src/components/Home/index.js_

```js
import React, { Component } from 'react'
import { browserHistory } from 'react-router'

export default class Home extends Component {
  handleSubmit(e) {
    e.preventDefault()
    const value = e.target.elements[0].value.toLowerCase()
    browserHistory.push(`/genre/${value}`)
  }
  render() {
    return (
      <div className="row">
        <div className="col-md-12">Раздел /</div>
        <form
          className="col-md-4"
          onSubmit={this.handleSubmit}
        >
          <input type="text" placeholder="genreName" />
          <button type="submit">Перейти</button>
        </form>
      </div>
    )
  }
}
```

Все предельно прозрачно: мы использовали browserHistory API, просто "[пушнув](https://developer.mozilla.org/ru/docs/Web/API/History_API)" (pushState) новую запись в историю.

Замечание: browserHistory из `react-router`, использует библиотеку [history](https://github.com/mjackson/history), которая в свою очередь использует [возможности современных браузеров](https://developer.mozilla.org/ru/docs/Web/API/History_API).

Если мы передадим значение rock - по клику на кнопку нас "перебросит" на:

```
http://localhost:3000/genre/rock
```

Вопрос валидации здесь не важен, так как цель данного урока не в этом.

Важно отметить, что если вы передадите историю в роутер, отличную от того, что используется здесь - приложение сломается. Честно говоря, на практике я не встречался с такой проблемой, но мне нравится ее решение, которое приводится в [официальной документации](https://github.com/reactjs/react-router-tutorial/tree/master/lessons/12-navigating) (ES5 синтаксис).

Использование `this.context` для программной навигации

_src/components/Home/index.js_

```js
import React, { Component, PropTypes } from 'react'

export default class Home extends Component {
  constructor() {
    super()
    this.handleSubmit = this.handleSubmit.bind(this)
  }
  handleSubmit(e) {
    e.preventDefault()
    const value = e.target.elements[0].value.toLowerCase()
    this.context.router.push(`/genre/${value}`)
  }
  render() {
    return (
      <div className="row">
        <div className="col-md-12">Раздел /</div>
        <form
          className="col-md-4"
          onSubmit={this.handleSubmit}
        >
          <input type="text" placeholder="genreName" />
          <button type="submit">Перейти</button>
        </form>
      </div>
    )
  }
}

Home.contextTypes = {
  router: PropTypes.object.isRequired,
}
```

Так как, в будущем мы еще столкнемся с использованием `this.context.router` и так как этот вариант является пуленепробиваемым - давайте оставим его.

У меня есть парочка вопросов на знание экосистемы react'a.

Зачем используется `this.handleSubmit = this.handleSubmit.bind(this)`?

Будет ли работать `this.context.router.push` если убрать последние три строки (там где проверяются props)?

Ответы:

React с версии 0.14 (предыдущей, перед 15.0) не использует автобиндинг если используются ES2015 классы. Мы должны забиндить `this` явно.

Работать не будет, так как `this.context` можно использовать только при наличии проверки contextTypes.

Итого: мы можем программно перенаправить браузер пользователя на новый URL. Мы научились использовать `this.context` используя "классический" (от слова "класс") синтаксис ES2015.

[Исходный код](https://github.com/maxfarseer/react-router-ru-tutorial/tree/programming_url_change) на данный момент.
