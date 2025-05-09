# createStore

```js
createStore(reducer, [preloadedState], [enhancer]);
```

Создает Redux [стор](Store.md) которое хранит полное дерево состояния вашего приложения.

Оно должно быть единственным стором в вашем приложении.

## Параметры

**`reducer`** _(Function)_
: [Функция редьюсера](../Glossary.md#reducer) которая возвращает следующее [дерево состояния](../Glossary.md#state), принимая текущее состояние и [экшен](../Glossary.md#action) к обработке.

[`preloadedState`] _(any)_
: Начальное состояние. Вы можете дополнительно указать это для гидрирования состояния с сервера в универсальных приложениях или для восстановления предыдущей сериализированной сессии пользователя. Если вы создали `редьюсер` с помощью [`combineReducers`](combineReducers.md) - это должно быть простым объектом с той же формой, как и ключи переданные ему. Иначе, вы можете передать все, что ваш `редьюсер` может понять.

[`enhancer`] _(Function)_
: Расширитель стора. Вы можете дополнительно указать это, чтобы расширить стор такими сторонними возможностями, как мидлвары (middleware), путешествия во времени, персистентность, и т.д. Единственный расширитель стора, который поставляется с Redux, это [`applyMiddleware()`](applyMiddleware.md).

## Возвращает

**[`Store`](Store.md)**
: объект, который содержит полное состояние вашего приложения. Единственный способ изменить его состояние — путем [отправки экшенов](Store.md#dispatch). Вы можете также [подписаться](Store.md#subscribe) на изменения его состояния, чтобы обновить пользовательский интерфейс.

## Пример

```js
import { createStore } from 'redux';

function todos(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            return state.concat([action.text]);
        default:
            return state;
    }
}

const store = createStore(todos, ['Use Redux']);

store.dispatch({
    type: 'ADD_TODO',
    text: 'Read the docs',
});

console.log(store.getState());
// [ 'Use Redux', 'Read the docs' ]
```

## Советы

-   Не создавайте более одного стора в приложении! Вместо этого используйте [`combineReducers`](combineReducers.md) для создания единого корневого редьюсера из нескольких.
-   Выбор формата состояния на ваше усмотрение. Можно использовать простые объекты или что-то вроде [Immutable](https://immutable-js.github.io/immutable-js/). Если вы не уверены, начните с простых объектов.
-   Если ваше состояние является простым объектом, убедитесь, что вы никогда его не изменяете! Например, вместо того, чтобы возвращать что-то вроде `Object.assign (state, newData)` из ваших редьюсеров, возвращайте `Object.assign ({}, state, newData)`. Таким образом, не переопределяется предыдущее `состояние`. Вы также можете написать `return { ...state, ...newData }` если вы включите [object spread operator proposal](../recipes/UsingObjectSpreadOperator.md).
-   Для универсальных приложений, которые выполняются на сервере, создавайте экземпляр стора с каждым запросом, так чтобы они были изолированы. Отправляйте несколько извлеченных экшенов для экземпляра стора и ждите их завершения перед рендерингом приложения на сервере.
-   Когда стор создан, Redux отправляет фиктивный экшен для вашего редьюсера, для заполнения стора с начальным состоянием. Вам не надо обрабатывать фиктивный экшен напрямую. Просто помните, что ваш редьюсер должен возвращать какое-то начальное состояние, если состояние переданное ему в качестве первого аргумента не `определено (undefined)` и все готово.
-   Чтобы использовать несколько расширителей стора вы можете использовать [`compose()`](compose.md).
