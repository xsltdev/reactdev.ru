# Константы

Константы одна из первых тем для холиваров. Как их лучше делать, где размещать и так далее. Мы возьмем такой способ: будем определять константу рядом с экшеном.

_src/actions/PageActions.js_

```js
export const SET_YEAR = 'SET_YEAR' // положили строку в константу

export function setYear(year) {
  return {
    type: SET_YEAR, // изменили строку на константу
    payload: year,
  }
}
```

Подключим константу в редьюсер `Page`

_src/reducers/page.js_

```js
import { SET_YEAR } from '../actions/PageActions'

const initialState = {
  year: 2018,
  photos: [],
}

export function pageReducer(state = initialState, action) {
  switch (action.type) {
    case SET_YEAR: // изменили строку на константу
      return { ...state, year: action.payload }

    default:
      return state
  }
}
```

В дальнейшем мы будем придерживаться такого подхода и добавлять константы для всех типов наших экшенов. Зачем мы это делаем, сказать сложно. Попробую придумать пример: вы решили, что все ваши типы теперь должны быть составными строками `module name/action type`, получается для `SET_YEAR` будет:

```js
const SET_YEAR = 'page/SET_YEAR'
```

При подходе с константами, вам потребуется изменит код лишь в одном месте (в определении константы).

Итого: превратили строковое значение в константу и познакомились с данным подходом организации типов экшенов.

[Исходный код](https://github.com/maxfarseer/redux-course-ru-v2/tree/chp8-constants).
