# Стор

В предыдущих разделах мы определили [экшены](Actions.md), которые представляют факт того, что "что-то случилось" и [редьюсеры](Reducers.md), которые обновляют состояние (state) в соответствии с этими экшенами.

**Стор** (Store) — это объект, который соединяет эти части вместе. Стор берет на себя следующие задачи:

-   Хранит состояние приложения (application state);
-   Предоставляет доступ к состоянию с помощью [`getState()`](../api/Store.md#getState);
-   Предоставляет возможность обновления состояния с помощью [`dispatch(action)`](../api/Store.md#dispatch);
-   Регистриурет слушателей с помощью функции [`subscribe(listener)`](../api/Store.md#subscribelistener);
-   Обрабатывает отмену регистрации слушателей с помощью функции, возвращаемой [`subscribe(listener)`](../api/Store.md#subscribelistener).

Важно отметить, что у вас будет только один стор в Redux-приложении. Если Вы захотите разделить логику обработки данных, то нужно будет использовать [композицию редьюсеров (reducer composition)](Reducers.md#splitting-reducers) вместо использования множества сторов (stores).

Очень легко создать стор (Store), если у Вас есть редьюсер. В [предыдущем разделе](Reducers.md) мы использовали [`combineReducers()`](../api/combineReducers.md) для комбинирования несколько редьюсеров в один глобальный редьюсер. Теперь мы их импортируем и передадим в [`createStore()`](../api/createStore.md).

```js
import { createStore } from 'redux';
import todoApp from './reducers';
let store = createStore(todoApp);
```

Вы можете объявить начальное состояние, передав его вторым аргументом в [`createStore()`](../api/createStore.md). Это полезно для пробрасывания состояния на клиент из состояния приложения Redux, работающего на сервере.

```js
const store = createStore(
    todoApp,
    window.STATE_FROM_SERVER
);
```

## Отправка экшенов

На текущий момент у нас есть созданный стор, давайте проверим, как работает наше приложение! Даже без пользовательского интерфейса мы уже можем проверить логику обновления состояния.

```js
import {
    addTodo,
    toggleTodo,
    setVisibilityFilter,
    VisibilityFilters,
} from './actions';

// Выведем в консоль начальное состояние
console.log(store.getState());

// Каждый раз при обновлении состояния - выводим его
// Отметим, что subscribe() возвращает функцию для отмены регистрации слушателя
const unsubscribe = store.subscribe(() =>
    console.log(store.getState())
);

// Отправим несколько экшенов
store.dispatch(addTodo('Learn about actions'));
store.dispatch(addTodo('Learn about reducers'));
store.dispatch(addTodo('Learn about store'));
store.dispatch(toggleTodo(0));
store.dispatch(toggleTodo(1));
store.dispatch(
    setVisibilityFilter(VisibilityFilters.SHOW_COMPLETED)
);

// Прекратим слушать обновление состояния
unsubscribe();
```

Вы можете видеть, как выполнение кода, приведенного выше, меняет состояние, содержащееся в сторе:

![Скриншот](store.png)

Мы смогли определить поведение нашего приложения даже до того, как начали создавать какой-то UI. Мы не будем делать этого в этом руководстве, но с этого момента Вы можете писать тесты для редьюсеров и генераторов экшенов (action creators). Вам не нужно будет ничего "мо́кать", потому что редьюсеры — это просто чистые функции. Вызывайте их и делайте проверки (make assertions) того, что они возвращают.

## Исходный код

_index.js_

```js
import { createStore } from 'redux';
import todoApp from './reducers';

let store = createStore(todoApp);
```

## Следующие шаги

Перед тем как создавать UI для нашего todo-приложения, мы сделаем небольшую прогулку, чтобы посмотреть, [что такое поток данных (data flows) в Redux-приложении](DataFlow.md).
