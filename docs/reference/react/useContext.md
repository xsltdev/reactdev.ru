---
description: useContext - это хук React, который позволяет вам читать и подписываться на контекст из вашего компонента
---

# useContext

<big>**`useContext`** - это хук React, который позволяет вам читать и подписываться на [контекст](../../learn/passing-data-deeply-with-context.md) из вашего компонента.</big>

```js
const value = useContext(SomeContext);
```

## Описание {#reference}

### `useContext(SomeContext)` {#usecontext}

Вызовите `useContext` на верхнем уровне вашего компонента для чтения и подписки на [контекст](../../learn/passing-data-deeply-with-context.md).

```js
import { useContext } from 'react';

function MyComponent() {
    const theme = useContext(ThemeContext);
    // ...
}
```

#### Параметры {#parameters}

-   `SomeContext`: Контекст, который вы ранее создали с помощью [`createContext`](createContext.md). Сам контекст не хранит информацию, он только представляет тип информации, которую вы можете предоставить или прочитать из компонентов.

#### Возвращает {#returns}

`useContext` возвращает значение контекста для вызывающего компонента. Оно определяется как `value`, переданное ближайшему `SomeContext.Provider` над вызывающим компонентом в дереве. Если такого провайдера нет, то возвращаемое значение будет `defaultValue`, которое вы передали в [`createContext`](createContext.md) для этого контекста. Возвращаемое значение всегда актуально. React автоматически перерисовывает компоненты, которые читают некоторый контекст, если он меняется.

#### Ограничения {#caveats}

-   Вызов `useContext()` в компоненте не влияет на провайдеров, возвращаемых из _этого же_ компонента. Соответствующий `<Context.Provider>` **должен находиться _выше_** компонента, выполняющего вызов `useContext()`.
-   React **автоматически перерисовывает** все дочерние компоненты, использующие определенный контекст, начиная с провайдера, получившего другое `value`. Предыдущее и последующее значения сравниваются с помощью сравнения [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Пропуск повторных рендеров с помощью [`memo`](memo.md) не мешает дочерним компонентам получать свежие значения контекста.
-   Если ваша система сборки выдает дубликаты модулей на выходе (что может произойти при использовании симлинков), это может нарушить контекст. Передача чего-либо через контекст работает только в том случае, если `SomeContext`, который вы используете для предоставления контекста, и `SomeContext`, который вы используете для его чтения, являются **_точно_ одним и тем же объектом**, что определяется сравнением `===`.

## Использование {#usage}

### Передача данных глубоко в дерево {#passing-data-deeply-into-the-tree}

Вызовите `useContext` на верхнем уровне вашего компонента для чтения и подписки на [контекст](../../learn/passing-data-deeply-with-context.md).

```js hl_lines="4"
import { useContext } from 'react';

function Button() {
    const theme = useContext(ThemeContext);
    // ...
}
```

`useContext` возвращает значение контекста для контекста, который вы передали. Чтобы определить значение контекста, React просматривает дерево компонентов и находит **ближайшего поставщика контекста выше** для данного контекста.

Чтобы передать контекст `Button`, оберните его или один из его родительских компонентов в соответствующий провайдер контекста:

```js hl_lines="3 5"
function MyPage() {
    return (
        <ThemeContext.Provider value="dark">
            <Form />
        </ThemeContext.Provider>
    );
}

function Form() {
    // ... renders buttons inside ...
}
```

Не имеет значения, сколько слоев компонентов находится между провайдером и `Button`. Когда `Button` _в любом месте_ внутри `Form` вызывает `useContext(ThemeContext)`, он получит `"dark"` в качестве значения.

!!!warning " Поиск ближайшего провайдера"

    `useContext()` всегда ищет ближайшего провайдера _выше_ компонента, который его вызывает. Она ищет вверх и не рассматривает провайдеров в компоненте, из которого вы вызываете `useContext()`.

=== "App.js"

    ```js
    import { createContext, useContext } from 'react';

    const ThemeContext = createContext(null);

    export default function MyApp() {
    	return (
    		<ThemeContext.Provider value="dark">
    			<Form />
    		</ThemeContext.Provider>
    	);
    }

    function Form() {
    	return (
    		<Panel title="Welcome">
    			<Button>Sign up</Button>
    			<Button>Log in</Button>
    		</Panel>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button className={className}>{children}</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/5y537n?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Обновление данных, переданных через контекст {#updating-data-passed-via-context}

Часто требуется, чтобы контекст менялся с течением времени. Чтобы обновить контекст, объедините его с [состоянием](useState.md). Объявите переменную состояния в родительском компоненте и передайте текущее состояние как значение контекста провайдеру.

```js hl_lines="2"
function MyPage() {
    const [theme, setTheme] = useState('dark');
    return (
        <ThemeContext.Provider value={theme}>
            <Form />
            <Button
                onClick={() => {
                    setTheme('light');
                }}
            >
                Switch to light theme
            </Button>
        </ThemeContext.Provider>
    );
}
```

Теперь любой `Button` внутри провайдера будет получать текущее значение `theme`. Если вы вызовете `setTheme` для обновления значения `theme`, которое вы передаете провайдеру, все компоненты `Button` будут перерисованы с новым значением `'light'`.

### Примеры обновления контекста {#examples-basic}

#### 1. Обновление значения через контекст {#updating-a-value-via-context}

В этом примере компонент `MyApp` хранит переменную состояния, которая затем передается провайдеру `ThemeContext`. Установка флажка "Темный режим" обновляет состояние. Изменение предоставленного значения пересматривает все компоненты, использующие данный контекст.

=== "App.js"

    ```js
    import { createContext, useContext, useState } from 'react';

    const ThemeContext = createContext(null);

    export default function MyApp() {
    	const [theme, setTheme] = useState('light');
    	return (
    		<ThemeContext.Provider value={theme}>
    			<Form />
    			<label>
    				<input
    					type="checkbox"
    					checked={theme === 'dark'}
    					onChange={(e) => {
    						setTheme(
    							e.target.checked
    								? 'dark'
    								: 'light'
    						);
    					}}
    				/>
    				Use dark mode
    			</label>
    		</ThemeContext.Provider>
    	);
    }

    function Form({ children }) {
    	return (
    		<Panel title="Welcome">
    			<Button>Sign up</Button>
    			<Button>Log in</Button>
    		</Panel>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button className={className}>{children}</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yfz5sy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что `value="dark"` передает строку `"dark"`, а `value={theme}` передает значение переменной JavaScript `theme` с [фигурными скобками JSX](../../learn/javascript-in-jsx-with-curly-braces.md). Фигурные скобки также позволяют передавать контекстные значения, которые не являются строками.

#### 2. Обновление объекта через контекст {#updating-an-object-via-context}

В этом примере есть переменная состояния `currentUser`, которая содержит объект. Вы объединяете `{ currentUser, setCurrentUser }` в один объект и передаете его вниз через контекст внутри `value={}`. Это позволяет любому компоненту ниже, например, `LoginButton`, читать и `currentUser`, и `setCurrentUser`, а затем вызывать `setCurrentUser`, когда это необходимо.

=== "App.js"

    ```js
    import { createContext, useContext, useState } from 'react';

    const CurrentUserContext = createContext(null);

    export default function MyApp() {
    	const [currentUser, setCurrentUser] = useState(null);
    	return (
    		<CurrentUserContext.Provider
    			value={{
    				currentUser,
    				setCurrentUser,
    			}}
    		>
    			<Form />
    		</CurrentUserContext.Provider>
    	);
    }

    function Form({ children }) {
    	return (
    		<Panel title="Welcome">
    			<LoginButton />
    		</Panel>
    	);
    }

    function LoginButton() {
    	const { currentUser, setCurrentUser } = useContext(
    		CurrentUserContext
    	);

    	if (currentUser !== null) {
    		return <p>You logged in as {currentUser.name}.</p>;
    	}

    	return (
    		<Button
    			onClick={() => {
    				setCurrentUser({ name: 'Advika' });
    			}}
    		>
    			Log in as Advika
    		</Button>
    	);
    }

    function Panel({ title, children }) {
    	return (
    		<section className="panel">
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children, onClick }) {
    	return (
    		<button className="button" onClick={onClick}>
    			{children}
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/72nnpt?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### 3. Множественные контексты {#multiple-contexts}

В этом примере есть два независимых контекста. `ThemeContext` предоставляет текущую тему, которая является строкой, а `CurrentUserContext` содержит объект, представляющий текущего пользователя.

=== "App.js"

    ```js
    import { createContext, useContext, useState } from 'react';

    const ThemeContext = createContext(null);
    const CurrentUserContext = createContext(null);

    export default function MyApp() {
    	const [theme, setTheme] = useState('light');
    	const [currentUser, setCurrentUser] = useState(null);
    	return (
    		<ThemeContext.Provider value={theme}>
    			<CurrentUserContext.Provider
    				value={{
    					currentUser,
    					setCurrentUser,
    				}}
    			>
    				<WelcomePanel />
    				<label>
    					<input
    						type="checkbox"
    						checked={theme === 'dark'}
    						onChange={(e) => {
    							setTheme(
    								e.target.checked
    									? 'dark'
    									: 'light'
    							);
    						}}
    					/>
    					Use dark mode
    				</label>
    			</CurrentUserContext.Provider>
    		</ThemeContext.Provider>
    	);
    }

    function WelcomePanel({ children }) {
    	const { currentUser } = useContext(CurrentUserContext);
    	return (
    		<Panel title="Welcome">
    			{currentUser !== null ? (
    				<Greeting />
    			) : (
    				<LoginForm />
    			)}
    		</Panel>
    	);
    }

    function Greeting() {
    	const { currentUser } = useContext(CurrentUserContext);
    	return <p>You logged in as {currentUser.name}.</p>;
    }

    function LoginForm() {
    	const { setCurrentUser } = useContext(
    		CurrentUserContext
    	);
    	const [firstName, setFirstName] = useState('');
    	const [lastName, setLastName] = useState('');
    	const canLogin = firstName !== '' && lastName !== '';
    	return (
    		<>
    			<label>
    				First name{': '}
    				<input
    					required
    					value={firstName}
    					onChange={(e) =>
    						setFirstName(e.target.value)
    					}
    				/>
    			</label>
    			<label>
    				Last name{': '}
    				<input
    					required
    					value={lastName}
    					onChange={(e) =>
    						setLastName(e.target.value)
    					}
    				/>
    			</label>
    			<Button
    				disabled={!canLogin}
    				onClick={() => {
    					setCurrentUser({
    						name: firstName + ' ' + lastName,
    					});
    				}}
    			>
    				Log in
    			</Button>
    			{!canLogin && <i>Fill in both fields.</i>}
    		</>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children, disabled, onClick }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button
    			className={className}
    			disabled={disabled}
    			onClick={onClick}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/nm2ytg?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### 4. Извлечение провайдеров в компонент {#extracting-providers-to-a-component}

По мере роста вашего приложения ожидается, что у вас будет "пирамида" контекстов ближе к корню вашего приложения. В этом нет ничего плохого. Однако, если вам эстетически не нравится вложенность, вы можете извлечь провайдеров в один компонент. В этом примере `MyProviders` скрывает "сантехнику" и отображает переданные ему дочерние элементы внутри необходимых провайдеров. Обратите внимание, что состояния `theme` и `setTheme` нужны в самом `MyApp`, поэтому `MyApp` по-прежнему владеет этой частью состояния.

=== "App.js"

    ```js
    import { createContext, useContext, useState } from 'react';

    const ThemeContext = createContext(null);
    const CurrentUserContext = createContext(null);

    export default function MyApp() {
    	const [theme, setTheme] = useState('light');
    	return (
    		<MyProviders theme={theme} setTheme={setTheme}>
    			<WelcomePanel />
    			<label>
    				<input
    					type="checkbox"
    					checked={theme === 'dark'}
    					onChange={(e) => {
    						setTheme(
    							e.target.checked
    								? 'dark'
    								: 'light'
    						);
    					}}
    				/>
    				Use dark mode
    			</label>
    		</MyProviders>
    	);
    }

    function MyProviders({ children, theme, setTheme }) {
    	const [currentUser, setCurrentUser] = useState(null);
    	return (
    		<ThemeContext.Provider value={theme}>
    			<CurrentUserContext.Provider
    				value={{
    					currentUser,
    					setCurrentUser,
    				}}
    			>
    				{children}
    			</CurrentUserContext.Provider>
    		</ThemeContext.Provider>
    	);
    }

    function WelcomePanel({ children }) {
    	const { currentUser } = useContext(CurrentUserContext);
    	return (
    		<Panel title="Welcome">
    			{currentUser !== null ? (
    				<Greeting />
    			) : (
    				<LoginForm />
    			)}
    		</Panel>
    	);
    }

    function Greeting() {
    	const { currentUser } = useContext(CurrentUserContext);
    	return <p>You logged in as {currentUser.name}.</p>;
    }

    function LoginForm() {
    	const { setCurrentUser } = useContext(
    		CurrentUserContext
    	);
    	const [firstName, setFirstName] = useState('');
    	const [lastName, setLastName] = useState('');
    	const canLogin = firstName !== '' && lastName !== '';
    	return (
    		<>
    			<label>
    				First name{': '}
    				<input
    					required
    					value={firstName}
    					onChange={(e) =>
    						setFirstName(e.target.value)
    					}
    				/>
    			</label>
    			<label>
    				Last name{': '}
    				<input
    					required
    					value={lastName}
    					onChange={(e) =>
    						setLastName(e.target.value)
    					}
    				/>
    			</label>
    			<Button
    				disabled={!canLogin}
    				onClick={() => {
    					setCurrentUser({
    						name: firstName + ' ' + lastName,
    					});
    				}}
    			>
    				Log in
    			</Button>
    			{!canLogin && <i>Fill in both fields.</i>}
    		</>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children, disabled, onClick }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button
    			className={className}
    			disabled={disabled}
    			onClick={onClick}
    		>
    			{children}
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/nn6css?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### 5. Масштабирование с помощью контекста и редуктора {#scaling-up-with-context-and-a-reducer}

В больших приложениях часто используется сочетание контекста с [редьюсером](useReducer.md) для извлечения логики, связанной с некоторым состоянием, из компонентов. В этом примере вся "проводка" спрятана в `TasksContext.js`, который содержит редуктор и два отдельных контекста.

Прочитайте [полное прохождение](../../learn/scaling-up-with-reducer-and-context.md) этого примера.

=== "App.js"

    ```js
    import AddTask from './AddTask.js';
    import TaskList from './TaskList.js';
    import { TasksProvider } from './TasksContext.js';

    export default function TaskApp() {
    	return (
    		<TasksProvider>
    			<h1>Day off in Kyoto</h1>
    			<AddTask />
    			<TaskList />
    		</TasksProvider>
    	);
    }
    ```

=== "TasksContext.js"

    ```js
    import {
    	createContext,
    	useContext,
    	useReducer,
    } from 'react';

    const TasksContext = createContext(null);

    const TasksDispatchContext = createContext(null);

    export function TasksProvider({ children }) {
    	const [tasks, dispatch] = useReducer(
    		tasksReducer,
    		initialTasks
    	);

    	return (
    		<TasksContext.Provider value={tasks}>
    			<TasksDispatchContext.Provider value={dispatch}>
    				{children}
    			</TasksDispatchContext.Provider>
    		</TasksContext.Provider>
    	);
    }

    export function useTasks() {
    	return useContext(TasksContext);
    }

    export function useTasksDispatch() {
    	return useContext(TasksDispatchContext);
    }

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

    const initialTasks = [
    	{ id: 0, text: 'Philosopher’s Path', done: true },
    	{ id: 1, text: 'Visit the temple', done: false },
    	{ id: 2, text: 'Drink matcha', done: false },
    ];
    ```

=== "AddTask.js"

    ```js
    import { useState, useContext } from 'react';
    import { useTasksDispatch } from './TasksContext.js';

    export default function AddTask() {
    	const [text, setText] = useState('');
    	const dispatch = useTasksDispatch();
    	return (
    		<>
    			<input
    				placeholder="Add task"
    				value={text}
    				onChange={(e) => setText(e.target.value)}
    			/>
    			<button
    				onClick={() => {
    					setText('');
    					dispatch({
    						type: 'added',
    						id: nextId++,
    						text: text,
    					});
    				}}
    			>
    				Add
    			</button>
    		</>
    	);
    }

    let nextId = 3;
    ```

=== "TaskList.js"

    ```js
    import { useState, useContext } from 'react';
    import {
    	useTasks,
    	useTasksDispatch,
    } from './TasksContext.js';

    export default function TaskList() {
    	const tasks = useTasks();
    	return (
    		<ul>
    			{tasks.map((task) => (
    				<li key={task.id}>
    					<Task task={task} />
    				</li>
    			))}
    		</ul>
    	);
    }

    function Task({ task }) {
    	const [isEditing, setIsEditing] = useState(false);
    	const dispatch = useTasksDispatch();
    	let taskContent;
    	if (isEditing) {
    		taskContent = (
    			<>
    				<input
    					value={task.text}
    					onChange={(e) => {
    						dispatch({
    							type: 'changed',
    							task: {
    								...task,
    								text: e.target.value,
    							},
    						});
    					}}
    				/>
    				<button onClick={() => setIsEditing(false)}>
    					Save
    				</button>
    			</>
    		);
    	} else {
    		taskContent = (
    			<>
    				{task.text}
    				<button onClick={() => setIsEditing(true)}>
    					Edit
    				</button>
    			</>
    		);
    	}
    	return (
    		<label>
    			<input
    				type="checkbox"
    				checked={task.done}
    				onChange={(e) => {
    					dispatch({
    						type: 'changed',
    						task: {
    							...task,
    							done: e.target.checked,
    						},
    					});
    				}}
    			/>
    			{taskContent}
    			<button
    				onClick={() => {
    					dispatch({
    						type: 'deleted',
    						id: task.id,
    					});
    				}}
    			>
    				Delete
    			</button>
    		</label>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/z59gng?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Указание запасного значения по умолчанию {#specifying-a-fallback-default-value}

Если React не может найти поставщиков данного контекста в родительском дереве, значение контекста, возвращаемое `useContext()`, будет равно значению по умолчанию, которое вы указали при [создании контекста](createContext.md):

```js
const ThemeContext = createContext(null);
```

Значение по умолчанию **никогда не изменяется**. Если вы хотите обновить контекст, используйте его вместе с состоянием, как описано выше.

Часто вместо `null` можно использовать какое-то более значимое значение по умолчанию, например:

```js
const ThemeContext = createContext('light');
```

Таким образом, если вы случайно отобразите какой-либо компонент без соответствующего провайдера, он не сломается. Это также поможет вашим компонентам хорошо работать в тестовой среде без установки большого количества провайдеров в тестах.

В примере ниже кнопка "Toggle theme" всегда светлая, потому что она находится **вне любого провайдера контекста темы**, а значение контекстной темы по умолчанию - `'light'`. Попробуйте изменить тему по умолчанию на `'dark'`.

=== "App.js"

    ```js
    import { createContext, useContext, useState } from 'react';

    const ThemeContext = createContext('light');

    export default function MyApp() {
    	const [theme, setTheme] = useState('light');
    	return (
    		<>
    			<ThemeContext.Provider value={theme}>
    				<Form />
    			</ThemeContext.Provider>
    			<Button
    				onClick={() => {
    					setTheme(
    						theme === 'dark' ? 'light' : 'dark'
    					);
    				}}
    			>
    				Toggle theme
    			</Button>
    		</>
    	);
    }

    function Form({ children }) {
    	return (
    		<Panel title="Welcome">
    			<Button>Sign up</Button>
    			<Button>Log in</Button>
    		</Panel>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			<h1>{title}</h1>
    			{children}
    		</section>
    	);
    }

    function Button({ children, onClick }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button className={className} onClick={onClick}>
    			{children}
    		</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/f82tfk?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Переопределение контекста для части дерева {#overriding-context-for-a-part-of-the-tree}

Вы можете переопределить контекст для части дерева, обернув эту часть в провайдер с другим значением.

```js
<ThemeContext.Provider value="dark">
    ...
    <ThemeContext.Provider value="light">
        <Footer />
    </ThemeContext.Provider>
    ...
</ThemeContext.Provider>
```

Вы можете вложить и переопределить провайдеров столько раз, сколько вам нужно.

### Примеры переопределения контекста {#examples}

#### 1. Переопределение темы {#overriding-a-theme}

Здесь кнопка внутри `Footer` получает другое значение контекста (`"light"`), чем кнопки снаружи (`"dark"`).

=== "App.js"

    ```js
    import { createContext, useContext } from 'react';

    const ThemeContext = createContext(null);

    export default function MyApp() {
    	return (
    		<ThemeContext.Provider value="dark">
    			<Form />
    		</ThemeContext.Provider>
    	);
    }

    function Form() {
    	return (
    		<Panel title="Welcome">
    			<Button>Sign up</Button>
    			<Button>Log in</Button>
    			<ThemeContext.Provider value="light">
    				<Footer />
    			</ThemeContext.Provider>
    		</Panel>
    	);
    }

    function Footer() {
    	return (
    		<footer>
    			<Button>Settings</Button>
    		</footer>
    	);
    }

    function Panel({ title, children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'panel-' + theme;
    	return (
    		<section className={className}>
    			{title && <h1>{title}</h1>}
    			{children}
    		</section>
    	);
    }

    function Button({ children }) {
    	const theme = useContext(ThemeContext);
    	const className = 'button-' + theme;
    	return (
    		<button className={className}>{children}</button>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/hpt75y?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

#### 2. Автоматически вложенные заголовки {#automatically-nested-headings}

Вы можете "накапливать" информацию при вложении провайдеров контекста. В этом примере компонент `Section` отслеживает `LevelContext`, который определяет глубину вложенности раздела. Он считывает `LevelContext` из родительской секции и предоставляет своим дочерним секциям номер `LevelContext`, увеличенный на единицу. В результате компонент `Heading` может автоматически решать, какой из тегов `<h1>`, `<h2>`, `<h3>`, ..., использовать, основываясь на том, сколько компонентов `Section` вложено в него.

Прочитайте [подробное описание](../../learn/passing-data-deeply-with-context.md) этого примера.

=== "App.js"

    ```js
    import Heading from './Heading.js';
    import Section from './Section.js';

    export default function Page() {
    	return (
    		<Section>
    			<Heading>Title</Heading>
    			<Section>
    				<Heading>Heading</Heading>
    				<Heading>Heading</Heading>
    				<Heading>Heading</Heading>
    				<Section>
    					<Heading>Sub-heading</Heading>
    					<Heading>Sub-heading</Heading>
    					<Heading>Sub-heading</Heading>
    					<Section>
    						<Heading>Sub-sub-heading</Heading>
    						<Heading>Sub-sub-heading</Heading>
    						<Heading>Sub-sub-heading</Heading>
    					</Section>
    				</Section>
    			</Section>
    		</Section>
    	);
    }
    ```

=== "Section.js"

    ```js
    import { useContext } from 'react';
    import { LevelContext } from './LevelContext.js';

    export default function Section({ children }) {
    	const level = useContext(LevelContext);
    	return (
    		<section className="section">
    			<LevelContext.Provider value={level + 1}>
    				{children}
    			</LevelContext.Provider>
    		</section>
    	);
    }
    ```

=== "Heading.js"

    ```js
    import { useContext } from 'react';
    import { LevelContext } from './LevelContext.js';

    export default function Heading({ children }) {
    	const level = useContext(LevelContext);
    	switch (level) {
    		case 0:
    			throw Error(
    				'Heading must be inside a Section!'
    			);
    		case 1:
    			return <h1>{children}</h1>;
    		case 2:
    			return <h2>{children}</h2>;
    		case 3:
    			return <h3>{children}</h3>;
    		case 4:
    			return <h4>{children}</h4>;
    		case 5:
    			return <h5>{children}</h5>;
    		case 6:
    			return <h6>{children}</h6>;
    		default:
    			throw Error('Unknown level: ' + level);
    	}
    }
    ```

=== "LevelContext.js"

    ```js
    import { createContext } from 'react';

    export const LevelContext = createContext(0);
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yz5t28?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

### Оптимизация рендеринга при передаче объектов и функций {#optimizing-re-renders-when-passing-objects-and-functions}

Вы можете передавать любые значения через контекст, включая объекты и функции.

```js hl_lines="11"
function MyApp() {
    const [currentUser, setCurrentUser] = useState(null);

    function login(response) {
        storeCredentials(response.credentials);
        setCurrentUser(response.user);
    }

    return (
        <AuthContext.Provider
            value={{ currentUser, login }}
        >
            <Page />
        </AuthContext.Provider>
    );
}
```

Здесь контекстное значение - это объект JavaScript с двумя свойствами, одно из которых - функция. Всякий раз, когда `MyApp` перерисовывается (например, при обновлении маршрута), это будет _разный_ объект, указывающий на _разную_ функцию, поэтому React также должен будет перерисовать все компоненты в глубине дерева, которые вызывают `useContext(AuthContext)`.

В небольших приложениях это не является проблемой. Однако нет необходимости перерисовывать их, если базовые данные, такие как `currentUser`, не изменились. Чтобы помочь React воспользоваться этим фактом, вы можете обернуть функцию `login` в [`useCallback`](useCallback.md) и обернуть создание объекта в [`useMemo`](useMemo.md). Это оптимизация производительности:

```js hl_lines="6 9 11 16 20"
import { useCallback, useMemo } from 'react';

function MyApp() {
    const [currentUser, setCurrentUser] = useState(null);

    const login = useCallback((response) => {
        storeCredentials(response.credentials);
        setCurrentUser(response.user);
    }, []);

    const contextValue = useMemo(
        () => ({
            currentUser,
            login,
        }),
        [currentUser, login]
    );

    return (
        <AuthContext.Provider value={contextValue}>
            <Page />
        </AuthContext.Provider>
    );
}
```

В результате этого изменения, даже если `MyApp` потребуется перерендеринг, компонентам, вызывающим `useContext(AuthContext)`, не потребуется перерендеринг, если только `currentUser` не изменился.

Подробнее о [`useMemo`](useMemo.md) и [`useCallback`](useCallback.md)

## Устранение неполадок {#troubleshooting}

### Мой компонент не видит значение от моего провайдера {#my-component-doesnt-see-the-value-from-my-provider}

Есть несколько распространенных способов, как это может произойти:

1.  Вы отображаете `<SomeContext.Provider>` в том же компоненте (или ниже), где вы вызываете `useContext()`. Переместите `<SomeContext.Provider>` _выше и вне_ компонента, вызывающего `useContext()`.
2.  Возможно, вы забыли обернуть ваш компонент `<SomeContext.Provider>`, или вы поместили его в другую часть дерева, чем думали. Проверьте правильность иерархии с помощью [React DevTools](../../learn/react-developer-tools.md).
3.  Возможно, вы столкнулись с какой-то проблемой сборки с вашим инструментарием, из-за которой `SomeContext`, как видно из предоставляющего компонента, и `SomeContext`, как видно из читающего компонента, являются двумя разными объектами. Это может произойти, например, если вы используете симлинки. Вы можете проверить это, присвоив им глобальные значения `window.SomeContext1` и `window.SomeContext2`, а затем проверив в консоли, равно ли `window.SomeContext1 === window.SomeContext2`. Если они не одинаковы, исправьте эту проблему на уровне инструмента сборки.

### Я всегда получаю `undefined` из моего контекста, хотя значение по умолчанию другое {#i-am-always-getting-undefined-from-my-context-although-the-default-value-is-different}

У вас может быть провайдер без `value` в дереве:

```js hl_lines="1-2"
// 🚩 Doesn't work: no value prop
<ThemeContext.Provider>
    <Button />
</ThemeContext.Provider>
```

Если вы забыли указать `value`, это все равно, что передать `value={undefined}`.

Вы также могли по ошибке использовать другое имя пропса:

```js hl_lines="1-2"
// 🚩 Doesn't work: prop should be called "value"
<ThemeContext.Provider theme={theme}>
    <Button />
</ThemeContext.Provider>
```

В обоих этих случаях вы должны увидеть предупреждение от React в консоли. Чтобы исправить их, вызовите свойство `value`:

```js hl_lines="1-2"
// ✅ Passing the value prop
<ThemeContext.Provider value={theme}>
    <Button />
</ThemeContext.Provider>
```

Обратите внимание, что значение по умолчанию из вашего вызова `createContext(defaultValue)` используется только **если выше вообще нет подходящего провайдера.** Если где-то в родительском дереве есть компонент `<SomeContext.Provider value={undefined}>`, компонент, вызывающий `useContext(SomeContext)` получит `undefined` в качестве значения контекста.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useContext](https://react.dev/reference/react/useContext)</small>
