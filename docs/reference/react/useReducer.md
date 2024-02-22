---
description: useReducer - это хук React, который позволяет добавить редьюсер в ваш компонент
---

# useReducer

<big>**`useReducer`** - это хук React, который позволяет добавить [редьюсер](../../learn/extracting-state-logic-into-a-reducer.md) в ваш компонент.</big>

```js
const [state, dispatch] = useReducer(reducer, initialArg, init?)
```

## Описание {#reference}

### `useReducer(reducer, initialArg, init?)` {#usereducer}

Вызовите `useReducer` на верхнем уровне вашего компонента для управления его состоянием с помощью [редьюсера](../../learn/extracting-state-logic-into-a-reducer.md).

```js
import { useReducer } from 'react';

function reducer(state, action) {
    // ...
}

function MyComponent() {
    const [state, dispatch] = useReducer(reducer, {
        age: 42,
    });
    // ...
}
```

#### Параметры {#parameters}

-   `reducer`: Функция reducer, определяющая, как обновляется состояние. Она должна быть чистой, принимать в качестве аргументов состояние и действие и возвращать следующее состояние. Состояние и действие могут быть любого типа.
-   `initialArg`: Значение, из которого вычисляется начальное состояние. Это может быть значение любого типа. То, как из него будет вычисляться начальное состояние, зависит от следующего аргумента `init`.
-   **опционально** `init`: Функция инициализатора, которая должна вернуть начальное состояние. Если она не указана, то начальное состояние устанавливается в `initialArg`. В противном случае начальное состояние устанавливается в результат вызова `init(initialArg)`.

#### Возвращаемое значение {#returns}

`useReducer` возвращает массив, содержащий ровно два значения:

1.  Текущее состояние. Во время первого рендера оно устанавливается в `init(initialArg)` или `initialArg` (если нет `init`).
2.  Функция `dispatch`, которая позволяет обновить состояние до другого значения и вызвать повторный рендеринг.

#### Предостережения {#caveats}

-   `useReducer` - это хук, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, создайте новый компонент и переместите состояние в него.
-   В строгом режиме React будет **вызывать ваш редуктор и инициализатор дважды**, чтобы помочь вам найти случайные примеси Это поведение только для разработки и не влияет на производство. Если ваши редуктор и инициализатор чисты (как и должно быть), это не должно повлиять на вашу логику. Результат одного из вызовов игнорируется.

### `dispatch` функция {#dispatch}

Функция `dispatch`, возвращаемая `useReducer`, позволяет вам обновить состояние до другого значения и вызвать повторный рендеринг. В качестве единственного аргумента в функцию `dispatch` нужно передать действие:

```js
const [state, dispatch] = useReducer(reducer, { age: 42 });

function handleClick() {
    dispatch({ type: 'incremented_age' });
    // ...
}
```

React установит следующее состояние как результат вызова функции `reducer`, которую вы предоставили с текущим `состоянием` и действием, которое вы передали в `dispatch`.

#### Параметры {#dispatch-parameters}

-   `действие`: Действие, выполняемое пользователем. Это может быть значение любого типа. По соглашению, действие обычно представляет собой объект со свойством `type`, идентифицирующим его, и, опционально, другими свойствами с дополнительной информацией.

#### Возврат {#dispatch-returns}

Функции `dispatch` не имеют возвращаемого значения.

#### Предостережения {#setstate-caveats}

-   Функция `dispatch` **только обновляет переменную состояния для _следующего_ рендера**. Если вы прочитаете переменную состояния после вызова функции `dispatch`, вы получите старое значение, которое было на экране до вашего вызова.
-   Если новое значение, которое вы предоставили, идентично текущему `state`, что определяется сравнением [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is), React **пропустит повторное отображение компонента и его дочерних элементов.** Это оптимизация. React все еще может потребоваться вызвать ваш компонент перед игнорированием результата, но это не должно повлиять на ваш код.
-   React [batches state updates](../../learn/queueing-a-series-of-state-updates.md). Он обновляет экран **после того, как все обработчики событий запущены** и вызвали свои функции `set`. Это предотвращает множественные повторные рендеринги во время одного события. В редких случаях, когда вам нужно заставить React обновить экран раньше, например, для доступа к DOM, вы можете использовать [`flushSync`](../react-dom/flushSync.md).

## Использование {#usage}

### Добавление редуктора к компоненту {#adding-a-reducer-to-a-component}

Вызовите `useReducer` на верхнем уровне вашего компонента для управления состоянием с помощью [reducer](../../learn/extracting-state-logic-into-a-reducer.md).

```js
import { useReducer } from 'react';

function reducer(state, action) {
    // ...
}

function MyComponent() {
    const [state, dispatch] = useReducer(reducer, {
        age: 42,
    });
    // ...
}
```

`useReducer` возвращает массив, содержащий ровно два элемента:

1.  текущее состояние этой переменной состояния, первоначально установленное в начальное состояние, которое вы указали.
2.  `dispatch` функцию, которая позволяет вам изменять состояние в ответ на взаимодействие.

Чтобы обновить то, что отображается на экране, вызовите `dispatch` с объектом, представляющим действия пользователя, называемым _action_:

```js
function handleClick() {
    dispatch({ type: 'incremented_age' });
}
```

React передаст текущее состояние и действие вашей функции редуктора. Ваш редуктор вычислит и вернет следующее состояние. React будет хранить это следующее состояние, рендерить ваш компонент с ним и обновлять пользовательский интерфейс.

=== "App.js"

    ```js
    import { useReducer } from 'react';

    function reducer(state, action) {
    	if (action.type === 'incremented_age') {
    		return {
    			age: state.age + 1,
    		};
    	}
    	throw Error('Unknown action.');
    }

    export default function Counter() {
    	const [state, dispatch] = useReducer(reducer, {
    		age: 42,
    	});

    	return (
    		<>
    			<button
    				onClick={() => {
    					dispatch({ type: 'incremented_age' });
    				}}
    			>
    				Increment age
    			</button>
    			<p>Hello! You are {state.age}.</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yjlw76?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

`useReducer` очень похож на [`useState`](useState.md), но он позволяет вам перенести логику обновления состояния из обработчиков событий в одну функцию вне вашего компонента. Подробнее о [выбор между `useState` и `useReducer`](../../learn/extracting-state-logic-into-a-reducer.md)

### Написание функции редуктора {#writing-the-reducer-function}

Функция редуктора объявляется следующим образом:

```js
function reducer(state, action) {
    // ...
}
```

Затем вам нужно заполнить код, который будет вычислять и возвращать следующее состояние. По традиции, это принято записывать как оператор [`switch`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/switch). Для каждого `case` в `switch`, вычислите и верните некоторое следующее состояние.

```js hl_lines="4-7 10-13"
function reducer(state, action) {
    switch (action.type) {
        case 'incremented_age': {
            return {
                name: state.name,
                age: state.age + 1,
            };
        }
        case 'changed_name': {
            return {
                name: action.nextName,
                age: state.age,
            };
        }
    }
    throw Error('Unknown action: ' + action.type);
}
```

Действия могут иметь любую форму. По традиции принято передавать объекты со свойством `type`, идентифицирующим действие. Он должен включать минимально необходимую информацию, которая нужна редуктору для вычисления следующего состояния.

```js hl_lines="8 12-15"
function Form() {
    const [state, dispatch] = useReducer(reducer, {
        name: 'Taylor',
        age: 42,
    });

    function handleButtonClick() {
        dispatch({ type: 'incremented_age' });
    }

    function handleInputChange(e) {
        dispatch({
            type: 'changed_name',
            nextName: e.target.value,
        });
    }
    // ...
}
```

Имена типов действий являются локальными для вашего компонента. [Каждое действие описывает одно взаимодействие, даже если оно приводит к нескольким изменениям данных](../../learn/extracting-state-logic-into-a-reducer.md#writing-reducers-well). Форма состояния произвольна, но обычно это объект или массив.

Прочитайте [извлечение логики состояния в редуктор](../../learn/extracting-state-logic-into-a-reducer.md), чтобы узнать больше.

!!!warning "Обновление состояния"

    Состояние доступно только для чтения. Не изменяйте никакие объекты или массивы в состоянии:

    ```js hl_lines="4-5"
    function reducer(state, action) {
    	switch (action.type) {
    		case 'incremented_age': {
    			// 🚩 Don't mutate an object in state like this:
    			state.age = state.age + 1;
    			return state;
    		}
    	}
    }
    ```

    Вместо этого всегда возвращайте новые объекты из вашего редуктора:

    ```js hl_lines="4-8"
    function reducer(state, action) {
    	switch (action.type) {
    		case 'incremented_age': {
    			// ✅ Instead, return a new object
    			return {
    				...state,
    				age: state.age + 1
    			};
    		}
    	}
    }
    ```

    Прочитайте [обновление объектов в состоянии](../../learn/updating-objects-in-state.md) и [обновление массивов в состоянии](../../learn/updating-arrays-in-state.md), чтобы узнать больше.

### Основные примеры использованияReducer {#examples-basic}

**1. Форма (объект)**

В этом примере редуктор управляет объектом state с двумя полями: `name` и `age`.

=== "App.js"

    ```js
    import { useReducer } from 'react';

    function reducer(state, action) {
    	switch (action.type) {
    		case 'incremented_age': {
    			return {
    				name: state.name,
    				age: state.age + 1,
    			};
    		}
    		case 'changed_name': {
    			return {
    				name: action.nextName,
    				age: state.age,
    			};
    		}
    	}
    	throw Error('Unknown action: ' + action.type);
    }

    const initialState = { name: 'Taylor', age: 42 };

    export default function Form() {
    	const [state, dispatch] = useReducer(
    		reducer,
    		initialState
    	);

    	function handleButtonClick() {
    		dispatch({ type: 'incremented_age' });
    	}

    	function handleInputChange(e) {
    		dispatch({
    			type: 'changed_name',
    			nextName: e.target.value,
    		});
    	}

    	return (
    		<>
    			<input
    				value={state.name}
    				onChange={handleInputChange}
    			/>
    			<button onClick={handleButtonClick}>
    				Increment age
    			</button>
    			<p>
    				Hello, {state.name}. You are {state.age}.
    			</p>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/8r27wz?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Todo list (массив)**

В этом примере редуктор управляет массивом задач. Массив необходимо обновить [без мутации](../../learn/updating-arrays-in-state.md).

=== "App.js"

    ```js
    import { useReducer } from 'react';
    import AddTask from './AddTask.js';
    import TaskList from './TaskList.js';

    function tasksReducer(tasks, action) {
    	switch (action.type) {
    		case 'added': {
    			return [
    				...tasks,
    				{
    					id: action.id,
    					text: action.text,
    					done: false,
    				},
    			];
    		}
    		case 'changed': {
    			return tasks.map((t) => {
    				if (t.id === action.task.id) {
    					return action.task;
    				} else {
    					return t;
    				}
    			});
    		}
    		case 'deleted': {
    			return tasks.filter((t) => t.id !== action.id);
    		}
    		default: {
    			throw Error('Unknown action: ' + action.type);
    		}
    	}
    }

    export default function TaskApp() {
    	const [tasks, dispatch] = useReducer(
    		tasksReducer,
    		initialTasks
    	);

    	function handleAddTask(text) {
    		dispatch({
    			type: 'added',
    			id: nextId++,
    			text: text,
    		});
    	}

    	function handleChangeTask(task) {
    		dispatch({
    			type: 'changed',
    			task: task,
    		});
    	}

    	function handleDeleteTask(taskId) {
    		dispatch({
    			type: 'deleted',
    			id: taskId,
    		});
    	}

    	return (
    		<>
    			<h1>Prague itinerary</h1>
    			<AddTask onAddTask={handleAddTask} />
    			<TaskList
    				tasks={tasks}
    				onChangeTask={handleChangeTask}
    				onDeleteTask={handleDeleteTask}
    			/>
    		</>
    	);
    }

    let nextId = 3;
    const initialTasks = [
    	{ id: 0, text: 'Visit Kafka Museum', done: true },
    	{ id: 1, text: 'Watch a puppet show', done: false },
    	{ id: 2, text: 'Lennon Wall pic', done: false },
    ];
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/qh57kd?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**Написание краткой логики обновления с помощью Immer**

Если обновление массивов и объектов без мутации кажется утомительным, вы можете использовать библиотеку типа [Immer](https://github.com/immerjs/use-immer#useimmerreducer) для сокращения повторяющегося кода. Immer позволяет вам писать лаконичный код, как если бы вы мутировали объекты, но под капотом она выполняет неизменяемые обновления:

=== "App.js"

    ```js
    import { useImmerReducer } from 'use-immer';
    import AddTask from './AddTask.js';
    import TaskList from './TaskList.js';

    function tasksReducer(draft, action) {
    	switch (action.type) {
    		case 'added': {
    			draft.push({
    				id: action.id,
    				text: action.text,
    				done: false,
    			});
    			break;
    		}
    		case 'changed': {
    			const index = draft.findIndex(
    				(t) => t.id === action.task.id
    			);
    			draft[index] = action.task;
    			break;
    		}
    		case 'deleted': {
    			return draft.filter((t) => t.id !== action.id);
    		}
    		default: {
    			throw Error('Unknown action: ' + action.type);
    		}
    	}
    }

    export default function TaskApp() {
    	const [tasks, dispatch] = useImmerReducer(
    		tasksReducer,
    		initialTasks
    	);

    	function handleAddTask(text) {
    		dispatch({
    			type: 'added',
    			id: nextId++,
    			text: text,
    		});
    	}

    	function handleChangeTask(task) {
    		dispatch({
    			type: 'changed',
    			task: task,
    		});
    	}

    	function handleDeleteTask(taskId) {
    		dispatch({
    			type: 'deleted',
    			id: taskId,
    		});
    	}

    	return (
    		<>
    			<h1>Prague itinerary</h1>
    			<AddTask onAddTask={handleAddTask} />
    			<TaskList
    				tasks={tasks}
    				onChangeTask={handleChangeTask}
    				onDeleteTask={handleDeleteTask}
    			/>
    		</>
    	);
    }

    let nextId = 3;
    const initialTasks = [
    	{ id: 0, text: 'Visit Kafka Museum', done: true },
    	{ id: 1, text: 'Watch a puppet show', done: false },
    	{ id: 2, text: 'Lennon Wall pic', done: false },
    ];
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/4wr6gv?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="fast-butterfly-4wr6gv" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Избегание воссоздания начального состояния {#avoiding-recreating-the-initial-state}

React сохраняет начальное состояние один раз и игнорирует его при последующих рендерах.

```js
function createInitialState(username) {
    // ...
}

function TodoList({ username }) {
    const [state, dispatch] = useReducer(
        reducer,
        createInitialState(username)
    );
    // ...
}
```

Хотя результат `createInitialState(username)` используется только для начального рендеринга, вы все равно вызываете эту функцию при каждом рендеринге. Это может быть расточительно, если она создает большие массивы или выполняет дорогие вычисления.

Чтобы решить эту проблему, вы можете **передать ее в качестве _инициализатора_ функции** в `useReducer` в качестве третьего аргумента вместо этого:

```js hl_lines="6-10"
function createInitialState(username) {
    // ...
}

function TodoList({ username }) {
    const [state, dispatch] = useReducer(
        reducer,
        username,
        createInitialState
    );
    // ...
}
```

Обратите внимание, что вы передаете `createInitialState`, которая является самой _функцией_, а не `createInitialState()`, которая является результатом ее вызова. Таким образом, начальное состояние не создается заново после инициализации.

В приведенном выше примере `createInitialState` принимает аргумент `username`. Если вашему инициализатору не нужна информация для вычисления начального состояния, вы можете передать `null` в качестве второго аргумента в `useReducer`.

### Разница между передачей инициализатора и передачей начального состояния напрямую {#examples-initializer}

**1. Передача функции инициализатора**

В этом примере передается функция инициализатора, поэтому функция `createInitialState` выполняется только во время инициализации. Она не выполняется при повторном рендеринге компонента, например, когда вы вводите текст в поле ввода.

=== "TodoList.js"

    ```js
    import { useReducer } from 'react';

    function createInitialState(username) {
    	const initialTodos = [];
    	for (let i = 0; i < 50; i++) {
    		initialTodos.push({
    			id: i,
    			text: username + "'s task #" + (i + 1),
    		});
    	}
    	return {
    		draft: '',
    		todos: initialTodos,
    	};
    }

    function reducer(state, action) {
    	switch (action.type) {
    		case 'changed_draft': {
    			return {
    				draft: action.nextDraft,
    				todos: state.todos,
    			};
    		}
    		case 'added_todo': {
    			return {
    				draft: '',
    				todos: [
    					{
    						id: state.todos.length,
    						text: state.draft,
    					},
    					...state.todos,
    				],
    			};
    		}
    	}
    	throw Error('Unknown action: ' + action.type);
    }

    export default function TodoList({ username }) {
    	const [state, dispatch] = useReducer(
    		reducer,
    		username,
    		createInitialState
    	);
    	return (
    		<>
    			<input
    				value={state.draft}
    				onChange={(e) => {
    					dispatch({
    						type: 'changed_draft',
    						nextDraft: e.target.value,
    					});
    				}}
    			/>
    			<button
    				onClick={() => {
    					dispatch({ type: 'added_todo' });
    				}}
    			>
    				Add
    			</button>
    			<ul>
    				{state.todos.map((item) => (
    					<li key={item.id}>{item.text}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gyld7n?view=Editor+%2B+Preview&module=%2Fsrc%2FTodoList.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Передача начального состояния напрямую**

В этом примере не передается функция инициализатора, поэтому функция `createInitialState` запускается при каждом рендере, например, когда вы вводите текст в `input`. Разница в поведении не заметна, но этот код менее эффективен.

=== "TodoList.js"

    ```js
    import { useReducer } from 'react';

    function createInitialState(username) {
    	const initialTodos = [];
    	for (let i = 0; i < 50; i++) {
    		initialTodos.push({
    			id: i,
    			text: username + "'s task #" + (i + 1),
    		});
    	}
    	return {
    		draft: '',
    		todos: initialTodos,
    	};
    }

    function reducer(state, action) {
    	switch (action.type) {
    		case 'changed_draft': {
    			return {
    				draft: action.nextDraft,
    				todos: state.todos,
    			};
    		}
    		case 'added_todo': {
    			return {
    				draft: '',
    				todos: [
    					{
    						id: state.todos.length,
    						text: state.draft,
    					},
    					...state.todos,
    				],
    			};
    		}
    	}
    	throw Error('Unknown action: ' + action.type);
    }

    export default function TodoList({ username }) {
    	const [state, dispatch] = useReducer(
    		reducer,
    		createInitialState(username)
    	);
    	return (
    		<>
    			<input
    				value={state.draft}
    				onChange={(e) => {
    					dispatch({
    						type: 'changed_draft',
    						nextDraft: e.target.value,
    					});
    				}}
    			/>
    			<button
    				onClick={() => {
    					dispatch({ type: 'added_todo' });
    				}}
    			>
    				Add
    			</button>
    			<ul>
    				{state.todos.map((item) => (
    					<li key={item.id}>{item.text}</li>
    				))}
    			</ul>
    		</>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/gjw6zq?view=Editor+%2B+Preview&module=%2Fsrc%2FTodoList.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Устранение неполадок {#troubleshooting}

### Я диспетчеризировал действие, но логирование дает мне старое значение состояния {#ive-dispatched-an-action-but-logging-gives-me-the-old-state-value}

Вызов функции `dispatch` **не изменяет состояние в работающем коде**:

```js hl_lines="4-5 8"
function handleClick() {
    console.log(state.age); // 42

    dispatch({ type: 'incremented_age' }); // Request a re-render with 43
    console.log(state.age); // Still 42!

    setTimeout(() => {
        console.log(state.age); // Also 42!
    }, 5000);
}
```

Это происходит потому, что [состояние ведет себя как моментальный снимок](../../learn/state-as-a-snapshot.md). Обновление состояния запрашивает другой рендер с новым значением состояния, но не влияет на переменную JavaScript `state` в уже запущенном обработчике событий.

Если вам нужно узнать следующее значение состояния, вы можете вычислить его вручную, вызвав редьюсер самостоятельно:

```js
const action = { type: 'incremented_age' };
dispatch(action);

const nextState = reducer(state, action);
console.log(state); // { age: 42 }
console.log(nextState); // { age: 43 }
```

### Я запустил экшн, но экран не обновляется {#ive-dispatched-an-action-but-the-screen-doesnt-update}

React будет **игнорировать ваше обновление, если следующее состояние равно предыдущему,** что определяется сравнением [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Обычно это происходит, когда вы изменяете объект или массив в состоянии напрямую:

```js hl_lines="4-5 9-10"
function reducer(state, action) {
    switch (action.type) {
        case 'incremented_age': {
            // 🚩 Wrong: mutating existing object
            state.age++;
            return state;
        }
        case 'changed_name': {
            // 🚩 Wrong: mutating existing object
            state.name = action.nextName;
            return state;
        }
        // ...
    }
}
```

Вы изменили существующий объект `state` и вернули его, поэтому React проигнорировал обновление. Чтобы исправить это, вам нужно убедиться, что вы всегда [обновляете объекты в состоянии](../../learn/updating-objects-in-state.md) и [обновляете массивы в состоянии](../../learn/updating-arrays-in-state.md), а не мутируете их:

```js hl_lines="4-8 11-15"
function reducer(state, action) {
    switch (action.type) {
        case 'incremented_age': {
            // ✅ Correct: creating a new object
            return {
                ...state,
                age: state.age + 1,
            };
        }
        case 'changed_name': {
            // ✅ Correct: creating a new object
            return {
                ...state,
                name: action.nextName,
            };
        }
        // ...
    }
}
```

### Часть состояния моего редуктора становится неопределенной после диспетчеризации {#a-part-of-my-reducer-state-becomes-undefined-after-dispatching}

Убедитесь, что каждая ветвь `case` **копирует все существующие поля** при возврате нового состояния:

```js hl_lines="5"
function reducer(state, action) {
    switch (action.type) {
        case 'incremented_age': {
            return {
                ...state, // Don't forget this!
                age: state.age + 1,
            };
        }
        // ...
    }
}
```

Без `...state` выше, возвращаемое следующее состояние будет содержать только поле `age` и ничего больше.

### Все состояние моего редуктора становится неопределенным после диспетчеризации {#my-entire-reducer-state-becomes-undefined-after-dispatching}

Если ваше состояние неожиданно становится `undefined`, скорее всего, вы забыли `return` состояние в одном из случаев, или ваш тип действия не соответствует ни одному из утверждений `case`. Чтобы выяснить причину, выбросьте ошибку вне `switch`:

```js hl_lines="10"
function reducer(state, action) {
    switch (action.type) {
        case 'incremented_age': {
            // ...
        }
        case 'edited_name': {
            // ...
        }
    }
    throw Error('Unknown action: ' + action.type);
}
```

Вы также можете использовать статическую проверку типов, например, TypeScript, для выявления таких ошибок.

### Я получаю ошибку: "Too many re-renders" {#im-getting-an-error-too-many-re-renders}

Вы можете получить ошибку, которая гласит: `Too many re-renders. React limits the number of renders to prevent an infinite loop.` Обычно это означает, что вы безоговорочно отправляете действие _во время рендера_, поэтому ваш компонент попадает в цикл: рендер, диспетчеризация (которая вызывает рендер), рендер, диспетчеризация (которая вызывает рендер) и так далее. Очень часто причиной этого является ошибка в определении обработчика события:

```js hl_lines="1-2"
// 🚩 Wrong: calls the handler during render
return <button onClick={handleClick()}>Click me</button>;

// ✅ Correct: passes down the event handler
return <button onClick={handleClick}>Click me</button>;

// ✅ Correct: passes down an inline function
return (
    <button onClick={(e) => handleClick(e)}>
        Click me
    </button>
);
```

Если вы не можете найти причину этой ошибки, нажмите на стрелку рядом с ошибкой в консоли и просмотрите стек JavaScript, чтобы найти конкретный вызов функции `dispatch`, ответственный за ошибку.

### Моя функция редуктора или инициализатора выполняется дважды {#my-reducer-or-initializer-function-runs-twice}

В [Строгом режиме](StrictMode.md) React будет вызывать ваши функции редуктора и инициализатора дважды. Это не должно сломать ваш код.

Это **поведение только для разработчиков** помогает вам [поддерживать чистоту компонентов](../../learn/keeping-components-pure.md). React использует результат одного из вызовов и игнорирует результат другого вызова. Пока ваши функции компонента, инициализатора и редуктора чисты, это не должно влиять на вашу логику. Однако если они случайно оказались нечистыми, это поможет вам заметить ошибки.

Например, эта нечистая функция reducer мутирует массив в состоянии:

```js hl_lines="4-9"
function reducer(state, action) {
    switch (action.type) {
        case 'added_todo': {
            // 🚩 Mistake: mutating state
            state.todos.push({
                id: nextId++,
                text: action.text,
            });
            return state;
        }
        // ...
    }
}
```

Поскольку React дважды вызывает вашу функцию `reducer`, вы увидите, что `todo` был добавлен дважды, поэтому вы будете знать, что произошла ошибка. В этом примере вы можете исправить ошибку, [заменив массив вместо его мутирования](../../learn/updating-arrays-in-state.md):

```js hl_lines="4-11"
function reducer(state, action) {
    switch (action.type) {
        case 'added_todo': {
            // ✅ Correct: replacing with new state
            return {
                ...state,
                todos: [
                    ...state.todos,
                    { id: nextId++, text: action.text },
                ],
            };
        }
        // ...
    }
}
```

Теперь, когда эта функция reducer является чистой, ее повторный вызов не изменит поведение. Вот почему двойной вызов React помогает найти ошибки. **Только функции компонента, инициализатора и редуктора должны быть чистыми.** Обработчики событий не должны быть чистыми, поэтому React никогда не будет вызывать обработчики событий дважды.

Прочитайте [поддержание чистоты компонентов](../../learn/keeping-components-pure.md), чтобы узнать больше.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useReducer](https://react.dev/reference/react/useReducer)</small>
