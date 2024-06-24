---
description: 'Описание типизации Redux в React с использованием TypeScript, включая создание глобальных типов хранилища, таких как RootState и RootAction, для улучшения безопасности типов.'
---

# Redux

## Конфигурация стора

### Создание глобальных типов хранилища

#### `RootState` - тип, представляющий корневое дерево состояний.

Может быть импортирован в подключаемые компоненты для обеспечения безопасности типов для функции Redux `connect`.

#### `RootAction` - тип, представляющий тип объединения всех объектов действия.

Может быть импортирован в различные слои, принимающие или отправляющие действия Redux, такие как: reducers, sagas или redux-observables epics

```ts
import { StateType, ActionType } from 'typesafe-actions';

declare module 'MyTypes' {
    export type Store = StateType<
        typeof import('./store').default
    >;
    export type RootAction = ActionType<
        typeof import('./root-action').default
    >;
    export type RootState = StateType<
        ReturnType<typeof import('./root-reducer').default>
    >;
}

declare module 'typesafe-actions' {
    interface Types {
        RootAction: ActionType<
            typeof import('./root-action').default
        >;
    }
}
```

### Создать стор

При создании экземпляра стора нам не нужно предоставлять никаких дополнительных типов. Он создаст **безопасный с точки зрения типов экземпляр Store**, используя вывод типов.

> Результирующие методы экземпляра стора, такие как `getState` или `dispatch`, будут проверены на тип и покажут все ошибки типа.

```ts
import { RootAction, RootState, Services } from 'MyTypes';
import { applyMiddleware, createStore } from 'redux';
import { createEpicMiddleware } from 'redux-observable';

import services from '../services';
import { routerMiddleware } from './redux-router';
import rootEpic from './root-epic';
import rootReducer from './root-reducer';
import { composeEnhancers } from './utils';

const epicMiddleware = createEpicMiddleware<
    RootAction,
    RootAction,
    RootState,
    Services
>({
    dependencies: services,
});

// configure middlewares
const middlewares = [epicMiddleware, routerMiddleware];
// compose enhancers
const enhancer = composeEnhancers(
    applyMiddleware(...middlewares)
);

// rehydrate state on app start
const initialState = {};

// create store
const store = createStore(
    rootReducer,
    initialState,
    enhancer
);

epicMiddleware.run(rootEpic);

// export store singleton instance
export default store;
```

## Создатели действий 🌟

> Мы будем использовать проверенную в боях библиотеку-помощник [`typesafe-actions`](https://github.com/piotrwitek/typesafe-actions#typesafe-actions) [![Latest Stable Version](https://img.shields.io/npm/v/typesafe-actions.svg)](https://www.npmjs.com/package/typesafe-actions) [![NPM Downloads](https://img.shields.io/npm/dt/typesafe-actions.svg)](https://www.npmjs.com/package/typesafe-actions), которая создана для того, чтобы сделать работу с **Redux** в **TypeScript** простой и увлекательной.
> Чтобы узнать больше, ознакомьтесь с этим подробным руководством: [Typesafe-Actions - Tutorial](https://github.com/piotrwitek/typesafe-actions#tutorial)!

Ниже представлено решение с использованием простой функции-фабрики для автоматизации создания безопасных для типов действий создателей. Цель состоит в том, чтобы уменьшить усилия по обслуживанию и сократить повторение кода аннотаций типов для действий и создателей. В результате получаются полностью безопасные для типов создатели действий и их действия.

```ts
/* eslint-disable */
import { action } from 'typesafe-actions';

import { ADD, INCREMENT } from './constants';

/* SIMPLE API */

export const increment = () => action(INCREMENT);
export const add = (amount: number) => action(ADD, amount);

/* ADVANCED API */

// More flexible allowing to create complex actions more easily
// use can use "action-creator" instance in place of "type constant"
// e.g. case getType(increment): return action.payload;
// This will allow to completely eliminate need for "constants" in your application, more info here:
// https://github.com/piotrwitek/typesafe-actions#constants

import { createAction } from 'typesafe-actions';
import { Todo } from '../todos/models';

export const emptyAction = createAction(INCREMENT)<void>();
export const payloadAction = createAction(ADD)<number>();
export const payloadMetaAction = createAction(ADD)<
    number,
    string
>();

export const payloadCreatorAction = createAction(
    'TOGGLE_TODO',
    (todo: Todo) => todo.id
)<string>();
```

```ts
import { store } from '../../store/';
import { countersActions as counter } from '../counters';

// store.dispatch(counter.increment(1)); // Error: Expected 0 arguments, but got 1.
store.dispatch(counter.increment()); // OK

// store.dispatch(counter.add()); // Error: Expected 1 arguments, but got 0.
store.dispatch(counter.add(1)); // OK
```

## Редукторы

### Состояние с неизменяемостью на уровне типа

Объявите тип редуктора `State` с модификатором `readonly`, чтобы получить неизменяемость во время компиляции

```ts
export type State = {
    readonly counter: number;
    readonly todos: ReadonlyArray<string>;
};
```

Модификатор Readonly позволяет инициализировать, но не позволяет переназначать, выделяя ошибки компилятора

```ts
export const initialState: State = {
    counter: 0,
}; // OK

initialState.counter = 3; // TS Error: cannot be mutated
```

Это отлично подходит для **массивов в JS**, потому что он будет ошибаться при использовании мутаторных методов, таких как (`push`, `pop`, `splice`, ...), но при этом позволит использовать неизменяемые методы, такие как (`concat`, `map`, `lice`, ...).

```ts
state.todos.push('Learn about tagged union types'); // TS Error: Property 'push' does not exist on type 'ReadonlyArray<string>'
const newTodos = state.todos.concat(
    'Learn about tagged union types'
); // OK
```

#### Caveat - `Readonly` не является рекурсивным.

Это означает, что модификатор `readonly` не распространяет неизменяемость вниз по вложенной структуре объектов. Вам придется явно помечать каждое свойство на каждом уровне.

> **TIP:** используйте `Readonly` или `ReadonlyArray` [Mapped types](https://www.typescriptlang.org/docs/handbook/advanced-types.html)

```ts
export type State = Readonly<{
    counterPairs: ReadonlyArray<
        Readonly<{
            immutableCounter1: number;
            immutableCounter2: number;
        }>
    >;
}>;

state.counterPairs[0] = {
    immutableCounter1: 1,
    immutableCounter2: 1,
}; // TS Error: cannot be mutated
state.counterPairs[0].immutableCounter1 = 1; // TS Error: cannot be mutated
state.counterPairs[0].immutableCounter2 = 1; // TS Error: cannot be mutated
```

#### Решение - рекурсивный `Readonly` называется `DeepReadonly`.

Чтобы исправить это, мы можем использовать тип [`DeepReadonly`](https://github.com/piotrwitek/utility-types#deepreadonlyt) (доступен из `utility-types`).

```ts
import { DeepReadonly } from 'utility-types';

export type State = DeepReadonly<{
    containerObject: {
        innerValue: number;
        numbers: number[];
    };
}>;

state.containerObject = { innerValue: 1 }; // TS Error: cannot be mutated
state.containerObject.innerValue = 1; // TS Error: cannot be mutated
state.containerObject.numbers.push(1); // TS Error: cannot use mutator methods
```

### Typing reducer

> для понимания следующего раздела обязательно изучите [Type Inference](https://www.typescriptlang.org/docs/handbook/type-inference.html), [Control flow analysis](https://github.com/Microsoft/TypeScript/wiki/What%27s-new-in-TypeScript#control-flow-based-type-analysis) и [Tagged union types](https://github.com/Microsoft/TypeScript/wiki/What%27s-new-in-TypeScript#tagged-union-types)

```ts
import { combineReducers } from 'redux';
import { ActionType } from 'typesafe-actions';

import { Todo, TodosFilter } from './models';
import * as actions from './actions';
import { ADD, CHANGE_FILTER, TOGGLE } from './constants';

export type TodosAction = ActionType<typeof actions>;

export type TodosState = Readonly<{
    todos: Todo[];
    todosFilter: TodosFilter;
}>;
const initialState: TodosState = {
    todos: [],
    todosFilter: TodosFilter.All,
};

export default combineReducers<TodosState, TodosAction>({
    todos: (state = initialState.todos, action) => {
        switch (action.type) {
            case ADD:
                return [...state, action.payload];

            case TOGGLE:
                return state.map((item) =>
                    item.id === action.payload
                        ? {
                              ...item,
                              completed: !item.completed,
                          }
                        : item
                );

            default:
                return state;
        }
    },
    todosFilter: (
        state = initialState.todosFilter,
        action
    ) => {
        switch (action.type) {
            case CHANGE_FILTER:
                return action.payload;

            default:
                return state;
        }
    },
});
```

### Typing reducer с `typesafe-actions`

> Обратите внимание, что от нас не требуется использовать какой-либо параметр общего типа в API. Попробуйте сравнить его с обычным reducer, поскольку они эквивалентны.

```ts
import { combineReducers } from 'redux';
import { createReducer } from 'typesafe-actions';

import { Todo, TodosFilter } from './models';
import { ADD, CHANGE_FILTER, TOGGLE } from './constants';

export type TodosState = Readonly<{
    todos: Todo[];
    todosFilter: TodosFilter;
}>;
const initialState: TodosState = {
    todos: [],
    todosFilter: TodosFilter.All,
};

const todos = createReducer(initialState.todos)
    .handleType(ADD, (state, action) => [
        ...state,
        action.payload,
    ])
    .handleType(TOGGLE, (state, action) =>
        state.map((item) =>
            item.id === action.payload
                ? { ...item, completed: !item.completed }
                : item
        )
    );

const todosFilter = createReducer(
    initialState.todosFilter
).handleType(
    CHANGE_FILTER,
    (state, action) => action.payload
);

export default combineReducers({
    todos,
    todosFilter,
});
```

### Тестирование редуктора

```ts
import {
    todosReducer as reducer,
    todosActions as actions,
} from './';
import { TodosState } from './reducer';

/**
 * FIXTURES
 */
const getInitialState = (initial?: Partial<TodosState>) =>
    reducer(initial as TodosState, {} as any);

/**
 * STORIES
 */
describe('Todos Stories', () => {
    describe('initial state', () => {
        it('should match a snapshot', () => {
            const initialState = getInitialState();
            expect(initialState).toMatchSnapshot();
        });
    });

    describe('adding todos', () => {
        it('should add a new todo as the first element', () => {
            const initialState = getInitialState();
            expect(initialState.todos).toHaveLength(0);
            const state = reducer(
                initialState,
                actions.add('new todo')
            );
            expect(state.todos).toHaveLength(1);
            expect(state.todos[0].title).toEqual(
                'new todo'
            );
        });
    });

    describe('toggling completion state', () => {
        it('should mark active todo as complete', () => {
            const activeTodo = {
                id: '1',
                completed: false,
                title: 'active todo',
            };
            const initialState = getInitialState({
                todos: [activeTodo],
            });
            expect(
                initialState.todos[0].completed
            ).toBeFalsy();
            const state1 = reducer(
                initialState,
                actions.toggle(activeTodo.id)
            );
            expect(state1.todos[0].completed).toBeTruthy();
        });
    });
});
```

## Подключенные компоненты Redux

### Счетчик подключенных компонентов Redux

```ts
import Types from 'MyTypes';
import { connect } from 'react-redux';

import {
    countersActions,
    countersSelectors,
} from '../features/counters';
import { FCCounter } from '../components';

const mapStateToProps = (state: Types.RootState) => ({
    count: countersSelectors.getReduxCounter(
        state.counters
    ),
});

const dispatchProps = {
    onIncrement: countersActions.increment,
};

export const FCCounterConnected = connect(
    mapStateToProps,
    dispatchProps
)(FCCounter);
```

```ts
import * as React from 'react';

import { FCCounterConnected } from '.';

export default () => (
    <FCCounterConnected label={'FCCounterConnected'} />
);
```

### Подключенный счетчик Redux с собственными реквизитами

```ts
import Types from 'MyTypes';
import { connect } from 'react-redux';

import {
    countersActions,
    countersSelectors,
} from '../features/counters';
import { FCCounter } from '../components';

type OwnProps = {
    initialCount?: number;
};

const mapStateToProps = (
    state: Types.RootState,
    ownProps: OwnProps
) => ({
    count:
        countersSelectors.getReduxCounter(state.counters) +
        (ownProps.initialCount || 0),
});

const dispatchProps = {
    onIncrement: countersActions.increment,
};

export const FCCounterConnectedOwnProps = connect(
    mapStateToProps,
    dispatchProps
)(FCCounter);
```

```ts
import * as React from 'react';

import { FCCounterConnectedOwnProps } from '.';

export default () => (
    <FCCounterConnectedOwnProps
        label={'FCCounterConnectedOwnProps'}
        initialCount={10}
    />
);
```

### Подключенный счетчик Redux с помощью хуков

```ts
import * as React from 'react';
import { FCCounter } from '../components';
import { increment } from '../features/counters/actions';
import { useSelector, useDispatch } from '../store/hooks';

const FCCounterConnectedHooksUsage: React.FC = () => {
    const counter = useSelector(
        (state) => state.counters.reduxCounter
    );
    const dispatch = useDispatch();
    return (
        <FCCounter
            label="Use selector"
            count={counter}
            onIncrement={() => dispatch(increment())}
        />
    );
};

export default FCCounterConnectedHooksUsage;
```

### Счетчик подключений в Redux с интеграцией `redux-thunk`

```ts
import Types from 'MyTypes';
import { bindActionCreators, Dispatch } from 'redux';
import { connect } from 'react-redux';
import * as React from 'react';

import { countersActions } from '../features/counters';

// Thunk Action
const incrementWithDelay = () => async (
    dispatch: Dispatch
): Promise<void> => {
    setTimeout(
        () => dispatch(countersActions.increment()),
        1000
    );
};

const mapStateToProps = (state: Types.RootState) => ({
    count: state.counters.reduxCounter,
});

const mapDispatchToProps = (
    dispatch: Dispatch<Types.RootAction>
) =>
    bindActionCreators(
        {
            onIncrement: incrementWithDelay,
        },
        dispatch
    );

type Props = ReturnType<typeof mapStateToProps> &
    ReturnType<typeof mapDispatchToProps> & {
        label: string;
    };

export const FCCounter: React.FC<Props> = (props) => {
    const { label, count, onIncrement } = props;

    const handleIncrement = () => {
        // Thunk action is correctly typed as promise
        onIncrement().then(() => {
            // ...
        });
    };

    return (
        <div>
            <span>
                {label}: {count}
            </span>
            <button type="button" onClick={handleIncrement}>
                {`Increment`}
            </button>
        </div>
    );
};

export const FCCounterConnectedBindActionCreators = connect(
    mapStateToProps,
    mapDispatchToProps
)(FCCounter);
```

```ts
import * as React from 'react';

import { FCCounterConnectedBindActionCreators } from '.';

export default () => (
    <FCCounterConnectedBindActionCreators
        label={'FCCounterConnectedBindActionCreators'}
    />
);
```

## Async Flow с `redux-observable`

### Эпики типизации

```ts
import { RootAction, RootState, Services } from 'MyTypes';
import { Epic } from 'redux-observable';
import {
    tap,
    ignoreElements,
    filter,
} from 'rxjs/operators';
import { isOfType } from 'typesafe-actions';

import { todosConstants } from '../todos';

// contrived example!!!
export const logAddAction: Epic<
    RootAction,
    RootAction,
    RootState,
    Services
> = (action$, state$, { logger }) =>
    action$.pipe(
        filter(isOfType(todosConstants.ADD)), // action is narrowed to: { type: "ADD_TODO"; payload: string; }
        tap((action) => {
            logger.log(
                `action type must be equal: ${todosConstants.ADD} === ${action.type}`
            );
        }),
        ignoreElements()
    );
```

### Испытание Эпиком

```ts
import {
    StateObservable,
    ActionsObservable,
} from 'redux-observable';
import { RootState, RootAction } from 'MyTypes';
import { Subject } from 'rxjs';

import { add } from './actions';
import { logAddAction } from './epics';

// Simple typesafe mock of all the services, you dont't need to mock anything else
// It is decoupled and reusable for all your tests, just put it in a separate file
const services = {
    logger: {
        log: jest.fn(),
    },
    localStorage: {
        loadState: jest.fn(),
        saveState: jest.fn(),
    },
};

describe('Todos Epics', () => {
    let state$: StateObservable<RootState>;

    beforeEach(() => {
        state$ = new StateObservable<RootState>(
            new Subject<RootState>(),
            undefined as any
        );
    });

    describe('logging todos actions', () => {
        beforeEach(() => {
            services.logger.log.mockClear();
        });

        it('should call the logger service when adding a new todo', (done) => {
            const addTodoAction = add('new todo');
            const action$ = ActionsObservable.of(
                addTodoAction
            );

            logAddAction(action$, state$, services)
                .toPromise()
                .then((outputAction: RootAction) => {
                    expect(
                        services.logger.log
                    ).toHaveBeenCalledTimes(1);
                    expect(
                        services.logger.log
                    ).toHaveBeenCalledWith(
                        'action type must be equal: todos/ADD === todos/ADD'
                    );
                    // expect output undefined because we're using "ignoreElements" in epic
                    expect(outputAction).toEqual(undefined);
                    done();
                });
        });
    });
});
```

## Селекторы с `reselect`

```ts
import { createSelector } from 'reselect';

import { TodosState } from './reducer';

export const getTodos = (state: TodosState) => state.todos;

export const getTodosFilter = (state: TodosState) =>
    state.todosFilter;

export const getFilteredTodos = createSelector(
    getTodos,
    getTodosFilter,
    (todos, todosFilter) => {
        switch (todosFilter) {
            case 'completed':
                return todos.filter((t) => t.completed);
            case 'active':
                return todos.filter((t) => !t.completed);

            default:
                return todos;
        }
    }
);
```

## Подключение с помощью `react-redux`

### Типизация подключенного компонента

**ПРИМЕЧАНИЕ**: Ниже вы найдете краткое объяснение концепций использования `connect` в TypeScript. За более подробными примерами обращайтесь к разделу Подключаемые компоненты Redux.

```ts
import MyTypes from 'MyTypes';

import {
    bindActionCreators,
    Dispatch,
    ActionCreatorsMapObject,
} from 'redux';
import { connect } from 'react-redux';

import { countersActions } from '../features/counters';
import { FCCounter } from '../components';

// Type annotation for "state" argument is mandatory to check
// the correct shape of state object and injected props you can also
// extend connected component Props interface by annotating `ownProps` argument
const mapStateToProps = (
    state: MyTypes.RootState,
    ownProps: FCCounterProps
) => ({
    count: state.counters.reduxCounter,
});

// "dispatch" argument needs an annotation to check the correct shape
//  of an action object when using dispatch function
const mapDispatchToProps = (
    dispatch: Dispatch<MyTypes.RootAction>
) =>
    bindActionCreators(
        {
            onIncrement: countersActions.increment,
        },
        dispatch
    );

// shorter alternative is to use an object instead of mapDispatchToProps function
const dispatchToProps = {
    onIncrement: countersActions.increment,
};

// Notice we don't need to pass any generic type parameters to neither
// the connect function below nor map functions declared above
// because type inference will infer types from arguments annotations automatically
// This is much cleaner and idiomatic approach
export const FCCounterConnected = connect(
    mapStateToProps,
    mapDispatchToProps
)(FCCounter);

// You can add extra layer of validation of your action creators
// by using bindActionCreators generic type parameter and RootAction type
const mapDispatchToProps = (
    dispatch: Dispatch<MyTypes.RootAction>
) =>
    bindActionCreators<
        ActionCreatorsMapObject<Types.RootAction>
    >(
        {
            invalidActionCreator: () => 1, // Error: Type 'number' is not assignable to type '{ type: "todos/ADD"; payload: Todo; } | { ... }
        },
        dispatch
    );
```

### Типизация `useSelector` и `useDispatch`

```ts
import { Dispatch } from 'redux';
import {
    TypedUseSelectorHook,
    useSelector as useGenericSelector,
    useDispatch as useGenericDispatch,
} from 'react-redux';
import { RootState, RootAction } from 'MyTypes';

export const useSelector: TypedUseSelectorHook<RootState> = useGenericSelector;

export const useDispatch: () => Dispatch<
    RootAction
> = useGenericDispatch;
```

### Типизация связанного компонента с интеграцией `redux-thunk`

**ПРИМЕЧАНИЕ**: При использовании создателей действий thunk необходимо использовать `bindActionCreators`. Только так вы сможете получить исправленную подпись типа реквизита диспетчеризации, как показано ниже.

```ts
const thunkAsyncAction = () => async (
    dispatch: Dispatch
): Promise<void> => {
    // dispatch actions, return Promise, etc.
};

const mapDispatchToProps = (
    dispatch: Dispatch<Types.RootAction>
) =>
    bindActionCreators(
        {
            thunkAsyncAction,
        },
        dispatch
    );

type DispatchProps = ReturnType<typeof mapDispatchToProps>;
// { thunkAsyncAction: () => Promise<void>; }

/* Without "bindActionCreators" fix signature will be the same as the original "unbound" thunk function: */
// { thunkAsyncAction: () => (dispatch: Dispatch<AnyAction>) => Promise<void>; }
```

<small>:material-information-outline: Источник &mdash; <https://github.com/piotrwitek/react-redux-typescript-guide?tab=readme-ov-file#redux></small>
