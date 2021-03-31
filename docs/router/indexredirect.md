# IndexRedirect

Предположим, вам хочется, чтобы пользователь при заходе на сайт, попадал сразу на отображение компонента `<List />` и корректного url-адреса соответственно.

Для этого удалите упоминания об IndexRoute'е и используйте IndexRedirect.

Привожу полный код:

_src/routes.js_

```js
import React from 'react'
import { Route, IndexRedirect } from 'react-router'

import App from './containers/App'
import Admin from './components/Admin'
import List from './components/List'
import Genre from './components/Genre'
import Release from './components/Release'
import NotFound from './components/NotFound'

export const routes = (
  <div>
    <Route path="/" component={App}>
      <IndexRedirect to="list" /> {/* INDEX REDIRECT */}
      <Route path="/admin" component={Admin} />
      <Route path="/genre/:genre" component={Genre}>
        <Route
          path="/genre/:genre/:release"
          component={Release}
        />
      </Route>
      <Route path="/list" component={List} />
    </Route>
    <Route path="*" component={NotFound} />
  </div>
)
```

Введите в браузере `http://localhost:3000/` и нажмите enter.

Откроется `http://localhost:3000/list`

Что и требовалось доказать. Результаты сохранять не нужно, вернитесь к предыдущей версии файла. Напомню, пользователям git - это можно сделать с помощью:

```
git checkout src/routes.js
```

P.S. для нетерпеливых: если интересно, как происходит redirect - используется "хук" на событие `onEnter`. Мы об этом еще не говорили, но вы можете прочитать несколько абзацев на EN [здесь](https://github.com/reactjs/react-router/blob/latest/docs/guides/IndexRoutes.md#index-redirects).

P.P.S. буквально одной строкой: если вы хотите использовать редирект не "главной страницы", то используйте следующий синтаксис:

```js
...
<Redirect from='/profile/photos' to='/new_all_photos_page'
/>
...
<Route path='new_all_photos_page' component={NewAllPhotosComponent} />
...
```
