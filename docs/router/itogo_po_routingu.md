# Итого по роутингу

Если вы не планируете использовать redux - на этом разделе для вас заканчивается курс по роутингу.

Подведем итоги. Мы научились:

- изменять URL-адрес и отрисовывать нужные компоненты в соответствии с этими изменениями
- использовать основные "плюшки" react-router'a: вложения (nesting) и параметры в адресе (:param)
- ограничивать доступ к странице (на примере обработки события onEnter)
- предотвращать нежелательный уход со страницы
- подкрашивать активные ссылки (заодно рассмотрели мощный прием - обертка над компонентом (wrap component))
- программно изменять роут

В качестве бонуса:

## Необязательный параметр в адресе

Перевод кода из документации:

```js
<Route path="/hello/:name">         // совпадет с /hello/michael and /hello/ryan
<Route path="/hello(/:name)">       // совпадет с /hello, /hello/michael, and /hello/ryan
<Route path="/files/*.*">           // совпадет с /files/hello.jpg and /files/hello.html
<Route path="/**/*.jpg">            // совпадет с /files/hello.jpg and /files/path/to/file.jpg
```

Кроме данного бонуса, в [официальных гайдах](https://reacttraining.com/react-router/web/guides/quick-start) (EN) еще много чего интересного.

Так же рекомендую изучить [примеры](https://reacttraining.com/react-router/web/example/basic).

Для тех, кто хочет идти дальше и использовать redux + react-router: давайте приберемся и вперед.

Приборка заключается в изменение компонента `<Home />`

_src/components/Home/index.js_

```js
import React, { Component } from 'react'

export default class Home extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-12">
          Добро пожаловать на курс по redux + react-router
        </div>
      </div>
    )
  }
}
```

P.S. приятная особенность: вы уже прошли не половину учебника, а процентов восемьдесят пять. Финал близко.
