---
description: useOptimistic - это React хук, позволяющий оптимистично обновлять пользовательский интерфейс.
---

# useOptimistic

<big>`useOptimistic` - это React хук, позволяющий оптимистично обновлять пользовательский интерфейс.</big>

```js
const [optimisticState, setOptimistic] = useOptimistic(value, reducer?);
```

## Описание {#reference}

### `useOptimistic(value, reducer?)` {#useoptimistic}

Вызовите `useOptimistic` на верхнем уровне компонента, чтобы создать оптимистичное состояние для значения.

```js
import { useOptimistic } from 'react';

function MyComponent({name, todos}) {
    const [optimisticAge, setOptimisticAge] = useOptimistic(28);
    const [optimisticName, setOptimisticName] = useOptimistic(name);
    const [optimisticTodos, setOptimisticTodos] = useOptimistic(todos, todoReducer);
    // ...
}
```

[Смотрите примеры ниже.](#usage)

#### Параметры {#parameters}

-   `value`: значение, которое возвращается, когда нет ожидающих действий.
-   **необязательно** `reducer(currentState, action)`: функция-редюсер, которая задаёт, как обновляется оптимистичное состояние. Она должна быть чистой, принимать текущее состояние и аргумент действия редюсера и возвращать следующее оптимистичное состояние.

#### Возвращаемое значение {#returns}

`useOptimistic` возвращает массив ровно из двух значений:

1.  `optimisticState`: текущее оптимистичное состояние. Оно равно `value`, если действие не ожидается. Если действие ожидается, оно равно состоянию, которое вернул `reducer`, или значению, переданному в функцию `set`, если `reducer` не передавали.
2.  [Функция `set`](#setoptimistic), которой можно обновить оптимистичное состояние на другое значение внутри действия.

### Функции `set`, например `setOptimistic(optimisticState)` {#setoptimistic}

Функция `set`, которую возвращает `useOptimistic`, позволяет обновлять состояние на время [действия](useTransition.md#functions-called-in-starttransition-are-called-actions). Можно передать следующее состояние напрямую или функцию, которая вычислит его из предыдущего:

```js
const [optimisticLike, setOptimisticLike] = useOptimistic(false);
const [optimisticSubs, setOptimisticSubs] = useOptimistic(subs);

function handleClick() {
  startTransition(async () => {
    setOptimisticLike(true);
    setOptimisticSubs(a => a + 1);
    await saveChanges();
  });
}
```

#### Параметры {#setoptimistic-parameters}

* `optimisticState`: значение, которое оптимистичное состояние должно иметь во время [действия](useTransition.md#functions-called-in-starttransition-are-called-actions). Если в `useOptimistic` передан `reducer`, это значение уйдёт вторым аргументом в редюсер. Тип может быть любым.
    * Если в `optimisticState` передать функцию, она будет считаться *функцией обновления*. Она должна быть чистой, принимать ожидающее состояние единственным аргументом и возвращать следующее оптимистичное состояние. React поставит функцию обновления в очередь и перерендерит компонент. При следующем рендере React вычислит следующее состояние, применив очередь обновлений к предыдущему состоянию, как у [обновлений `useState`](useState.md#setstate-parameters).

#### Возвращаемое значение {#setoptimistic-returns}

У функций `set` нет возвращаемого значения.

#### Предупреждения {#setoptimistic-caveats}

* Функцию `set` нужно вызывать внутри [действия](useTransition.md#functions-called-in-starttransition-are-called-actions). Если вызвать сеттер вне действия, [React покажет предупреждение](#an-optimistic-state-update-occurred-outside-a-transition-or-action), и оптимистичное состояние на мгновение отрендерится.

<a id="how-optimistic-state-works"></a>

??? note "Как работает оптимистичное состояние"

    `useOptimistic` позволяет показать временное значение, пока действие ещё выполняется:

    ```js
    const [value, setValue] = useState('a');
    const [optimistic, setOptimistic] = useOptimistic(value);

    startTransition(async () => {
      setOptimistic('b');
      const newValue = await saveChanges('b');
      setValue(newValue);
    });
    ```

    Когда сеттер вызывают внутри действия, `useOptimistic` запускает повторный рендер, чтобы показать это состояние, пока действие идёт. Иначе возвращается `value`, переданное в `useOptimistic`.

    Это состояние называют «оптимистичным», потому что им сразу показывают пользователю результат действия, хотя само действие ещё занимает время.

    **Как проходит обновление**

    1. **Обновление сразу**: когда вызывается `setOptimistic('b')`, React сразу рендерит `'b'`.

    2. **(Необязательно) await в действии**: если в действии есть await, React продолжает показывать `'b'`.

    3. **Запланирован переход**: `setValue(newValue)` планирует обновление настоящего состояния.

    4. **(Необязательно) ожидание Suspense**: если `newValue` приостанавливается, React продолжает показывать `'b'`.

    5. **Один коммит рендера**: в конце `newValue` коммитится и для `value`, и для `optimistic`.

    Лишнего рендера, чтобы «сбросить» оптимистичное состояние, нет. Оптимистичное и настоящее состояние сходятся в одном рендере, когда переход завершается.

    !!!note "Оптимистичное состояние временно"

        Оптимистичное состояние рендерится только пока действие выполняется, иначе рендерится `value`.

        Если `saveChanges` вернула `'c'`, то и `value`, и `optimistic` будут `'c'`, а не `'b'`.

    **Как определяется итоговое состояние**

    Аргумент `value` у `useOptimistic` определяет, что показывается после завершения действия. Как это работает, зависит от приёма:

    - **Зашитые значения** вроде `useOptimistic(false)`: после действия `state` по-прежнему `false`, поэтому интерфейс показывает `false`. Это удобно для состояний ожидания, которые всегда начинаются с `false`.

    - **Переданные пропсы или состояние** вроде `useOptimistic(isLiked)`: если родитель обновляет `isLiked` во время действия, после завершения используется новое значение. Так интерфейс отражает результат действия.

    - **Паттерн редюсера** вроде `useOptimistic(items, fn)`: если `items` меняется, пока действие ожидает, React заново запускает `reducer` с новыми `items` и пересчитывает состояние. Оптимистичные добавления остаются поверх свежих данных.

    **Что происходит, если действие завершается ошибкой**

    Если действие бросает ошибку, переход всё равно заканчивается, и React рендерит то, чем `value` является сейчас. Обычно родитель обновляет `value` только при успехе, поэтому при ошибке `value` не меняется, и интерфейс возвращается к тому, что было до оптимистичного обновления. Ошибку можно поймать и показать сообщение пользователю.

## Использование {#usage}

### Оптимистичное состояние в компоненте {#adding-optimistic-state-to-a-component}

Вызовите `useOptimistic` на верхнем уровне компонента, чтобы объявить одно или несколько оптимистичных состояний.

```js hl_lines="4 5 6"
import { useOptimistic } from 'react';

function MyComponent({age, name, todos}) {
  const [optimisticAge, setOptimisticAge] = useOptimistic(age);
  const [optimisticName, setOptimisticName] = useOptimistic(name);
  const [optimisticTodos, setOptimisticTodos] = useOptimistic(todos, reducer);
  // ...
```

`useOptimistic` возвращает массив ровно из двух элементов:

1. Оптимистичное состояние. Сначала оно равно переданному значению.
2. Функция `set`, которая на время [действия](useTransition.md#functions-called-in-starttransition-are-called-actions) временно меняет состояние.
   * Если передан редюсер, он выполнится перед возвратом оптимистичного состояния.

Чтобы использовать оптимистичное состояние, вызовите функцию `set` внутри действия.

Действия — это функции, которые вызывают внутри `startTransition`:

```js hl_lines="3"
function onAgeChange(e) {
  startTransition(async () => {
    setOptimisticAge(42);
    const newAge = await postAge(42);
    setAge(newAge);
  });
}
```

Сначала React отрендерит оптимистичное состояние `42`, а `age` останется текущим возрастом. Действие дождётся POST, а затем отрендерит `newAge` и для `age`, и для `optimisticAge`.

Подробный разбор — в разделе [Как работает оптимистичное состояние](#how-optimistic-state-works).

!!!note "Примечание"

    С [пропами-действиями](useTransition.md#exposing-action-props-from-components) функцию `set` можно вызывать без `startTransition`:

    ```js hl_lines="2"
    async function submitAction() {
      setOptimisticName('Taylor');
      await updateName('Taylor');
    }
    ```

    Это работает, потому что пропы-действия и так вызываются внутри `startTransition`.

    Пример: [Оптимистичное состояние в пропах-действиях](#using-optimistic-state-in-action-props).

### Оптимистичное состояние в пропах-действиях {#using-optimistic-state-in-action-props}

В [пропе-действии](useTransition.md#exposing-action-props-from-components) оптимистичный сеттер можно вызвать напрямую, без `startTransition`.

В этом примере оптимистичное состояние выставляется внутри пропа `submitAction` у `<form>`:

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import EditName from './EditName';

    export default function App() {
        const [name, setName] = useState('Alice');

        return <EditName name={name} action={setName} />;
    }
    ```

=== "EditName.js"

    ```js

    import { useOptimistic, startTransition } from 'react';
    import { updateName } from './actions.js';

    export default function EditName({ name, action }) {
        const [optimisticName, setOptimisticName] = useOptimistic(name);

        async function submitAction(formData) {
            const newName = formData.get('name');
            setOptimisticName(newName);

            const updatedName = await updateName(newName);
            startTransition(() => {
                action(updatedName);
            })
        }

        return (
            <form action={submitAction}>
                <p>Your name is: {optimisticName}</p>
                <p>
                    <label>Change it: </label>
                    <input
                        type="text"
                        name="name"
                        disabled={name !== optimisticName}
                    />
                </p>
            </form>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function updateName(name) {
        await new Promise((res) => setTimeout(res, 1000));
        return name;
    }
    ```

Когда пользователь отправляет форму, `optimisticName` сразу показывает `newName`, пока запрос к серверу ещё идёт. Когда запрос завершается, `name` и `optimisticName` рендерятся с настоящим `updatedName` из ответа.

??? note "Почему здесь не нужен `startTransition`?"

    По соглашению пропы, которые вызывают внутри `startTransition`, называют со словом «Action».

    Раз `submitAction` назван со словом «Action», он уже вызывается внутри `startTransition`.

    Паттерн пропа `action` описан в разделе [Проп `action` у компонентов](useTransition.md#exposing-action-props-from-components).

### Оптимистичное состояние в пропах-действиях компонента {#adding-optimistic-state-to-action-props}

Когда вы создаёте [проп-действие](useTransition.md#exposing-action-props-from-components), можно добавить `useOptimistic`, чтобы сразу дать обратную связь.

Вот кнопка, которая показывает «Submitting...», пока `action` ожидает:

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import Button from './Button';
    import { submitForm } from './actions.js';

    export default function App() {
        const [count, setCount] = useState(0);
        return (
            <div>
                <Button action={async () => {
                    await submitForm();
                    startTransition(() => {
                        setCount(c => c + 1);
                    });
                }}>Increment</Button>
                {count > 0 && <p>Submitted {count}!</p>}
            </div>
        );
    }
    ```

=== "Button.js"

    ```js

    import { useOptimistic, startTransition } from 'react';

    export default function Button({ action, children }) {
        const [isPending, setIsPending] = useOptimistic(false);

        return (
            <button
                disabled={isPending}
                onClick={() => {
                    startTransition(async () => {
                        setIsPending(true);
                        await action();
                    });
                }}
            >
                {isPending ? 'Submitting...' : children}
            </button>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function submitForm() {
        await new Promise((res) => setTimeout(res, 1000));
    }
    ```

Когда кнопку нажимают, `setIsPending(true)` через оптимистичное состояние сразу показывает «Submitting...» и отключает кнопку. Когда действие заканчивается, `isPending` автоматически рендерится как `false`.

Так состояние ожидания показывается само, как бы проп `action` ни использовали вместе с `Button`:

```js
// Show pending state for a state update
<Button action={() => { setState(c => c + 1) }} />

// Show pending state for a navigation
<Button action={() => { navigate('/done') }} />

// Show pending state for a POST
<Button action={async () => { await fetch(/* ... */) }} />

// Show pending state for any combination
<Button action={async () => {
  setState(c => c + 1);
  await fetch(/* ... */);
  navigate('/done');
}} />
```

Состояние ожидания будет видно, пока не закончится всё, что есть в пропе `action`.

!!!note "Примечание"

    Состояние ожидания можно получить и через [`useTransition`](useTransition.md), по флагу `isPending`.

    Разница в том, что `useTransition` даёт функцию `startTransition`, а `useOptimistic` работает с любым переходом. Берите то, что лучше подходит компоненту.

### Оптимистичное обновление пропсов или состояния {#updating-props-or-state-optimistically}

Пропсы или состояние можно обернуть в `useOptimistic`, чтобы обновить их сразу, пока действие ещё выполняется.

В этом примере `LikeButton` получает `isLiked` пропом и сразу переключает его по клику:

=== "App.js"

    ```js

    import { useState, useOptimistic, startTransition } from 'react';
    import { toggleLike } from './actions.js';

    export default function App() {
        const [isLiked, setIsLiked] = useState(false);
        const [optimisticIsLiked, setOptimisticIsLiked] = useOptimistic(isLiked);

        function handleClick() {
            startTransition(async () => {
                const newValue = !optimisticIsLiked
                console.log('⏳ setting optimistic state: ' + newValue);

                setOptimisticIsLiked(newValue);
                const updatedValue = await toggleLike(newValue);

                startTransition(() => {
                    console.log('⏳ setting real state: ' + updatedValue );
                    setIsLiked(updatedValue);
                });
            });
        }

        if (optimisticIsLiked !== isLiked) {
            console.log('✅ rendering optimistic state: ' + optimisticIsLiked);
        } else {
            console.log('✅ rendering real value: ' + optimisticIsLiked);
        }

        return (
            <button onClick={handleClick}>
                {optimisticIsLiked ? '❤️ Unlike' : '🤍 Like'}
            </button>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function toggleLike(value) {
        return await new Promise((res) => setTimeout(() => res(value), 1000));
        // In a real app, this would update the server
    }
    ```

Когда кнопку нажимают, `setOptimisticIsLiked` сразу меняет показанное состояние, и сердце выглядит нажатым. Тем временем в фоне выполняется `await toggleLike`. Когда `await` завершается, родительский `setIsLiked` обновляет «настоящее» состояние `isLiked`, и оптимистичное состояние рендерится в соответствии с этим новым значением.

!!!note "Примечание"

    В примере следующее значение считается из `optimisticIsLiked`. Это работает, если базовое состояние не изменится. Если базовое состояние может измениться, пока действие ожидает, лучше функция обновления или редюсер.

    Пример есть в разделе [Обновление состояния на основе текущего состояния](#updating-state-based-on-current-state).

### Обновление нескольких значений вместе {#updating-multiple-values-together}

Если оптимистичное обновление затрагивает несколько связанных значений, обновляйте их вместе через редюсер. Тогда интерфейс остаётся согласованным.

Вот кнопка подписки, которая обновляет и состояние подписки, и число подписчиков:

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import { followUser, unfollowUser } from './actions.js';
    import FollowButton from './FollowButton';

    export default function App() {
        const [user, setUser] = useState({
            name: 'React',
            isFollowing: false,
            followerCount: 10500
        });

        async function followAction(shouldFollow) {
            if (shouldFollow) {
                await followUser(user.name);
            } else {
                await unfollowUser(user.name);
            }
            startTransition(() => {
                setUser(current => ({
                    ...current,
                    isFollowing: shouldFollow,
                    followerCount: current.followerCount + (shouldFollow ? 1 : -1)
                }));
            });
        }

        return <FollowButton user={user} followAction={followAction} />;
    }
    ```

=== "FollowButton.js"

    ```js

    import { useOptimistic, startTransition } from 'react';

    export default function FollowButton({ user, followAction }) {
        const [optimisticState, updateOptimistic] = useOptimistic(
            { isFollowing: user.isFollowing, followerCount: user.followerCount },
            (current, isFollowing) => ({
                isFollowing,
                followerCount: current.followerCount + (isFollowing ? 1 : -1)
            })
        );

        function handleClick() {
            const newFollowState = !optimisticState.isFollowing;
            startTransition(async () => {
                updateOptimistic(newFollowState);
                await followAction(newFollowState);
            });
        }

        return (
            <div>
                <p><strong>{user.name}</strong></p>
                <p>{optimisticState.followerCount} followers</p>
                <button onClick={handleClick}>
                    {optimisticState.isFollowing ? 'Unfollow' : 'Follow'}
                </button>
            </div>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function followUser(name) {
        await new Promise((res) => setTimeout(res, 1000));
    }

    export async function unfollowUser(name) {
        await new Promise((res) => setTimeout(res, 1000));
    }
    ```

Редюсер получает новое значение `isFollowing` и за одно обновление считает и новое состояние подписки, и новое число подписчиков. Текст кнопки и счётчик всегда остаются согласованными.

??? note "Как выбрать между функциями обновления и редюсерами"

    У `useOptimistic` два приёма, чтобы считать состояние от текущего:

    **Функции обновления** работают как [обновления useState](useState.md#updating-state-based-on-the-previous-state). Передайте функцию в сеттер:

    ```js
    const [optimistic, setOptimistic] = useOptimistic(value);
    setOptimistic(current => !current);
    ```

    **Редюсеры** отделяют логику обновления от вызова сеттера:

    ```js
    const [optimistic, dispatch] = useOptimistic(value, (current, action) => {
      // Calculate next state based on current and action
    });
    dispatch(action);
    ```

    **Берите функции обновления**, если вызов сеттера сам по себе описывает обновление. Это похоже на `setState(prev => ...)` у `useState`.

    **Берите редюсеры**, если в обновление нужно передать данные (например, какой элемент добавить) или если один хук обрабатывает несколько типов обновлений.

    **Зачем редюсер?**

    Редюсеры нужны, когда базовое состояние может измениться, пока переход ожидает. Если `todos` изменится, пока добавление ещё ожидает (например, другой пользователь добавил задачу), React заново запустит редюсер с новыми `todos` и пересчитает, что показать. Новая задача добавится к свежему списку, а не к устаревшей копии.

    Функция обновления вроде `setOptimistic(prev => [...prev, newItem])` увидит только состояние на момент старта перехода и пропустит обновления, которые случились за время асинхронной работы.

### Оптимистичное добавление в список {#optimistically-adding-to-a-list}

Чтобы оптимистично добавлять элементы в список, используйте `reducer`:

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import { addTodo } from './actions.js';
    import TodoList from './TodoList';

    export default function App() {
        const [todos, setTodos] = useState([
            { id: 1, text: 'Learn React' }
        ]);

        async function addTodoAction(newTodo) {
            const savedTodo = await addTodo(newTodo);
            startTransition(() => {
                setTodos(todos => [...todos, savedTodo]);
            });
        }

        return <TodoList todos={todos} addTodoAction={addTodoAction} />;
    }
    ```

=== "TodoList.js"

    ```js

    import { useOptimistic, startTransition } from 'react';

    export default function TodoList({ todos, addTodoAction }) {
        const [optimisticTodos, addOptimisticTodo] = useOptimistic(
            todos,
            (currentTodos, newTodo) => [
                ...currentTodos,
                { id: newTodo.id, text: newTodo.text, pending: true }
            ]
        );

        function handleAddTodo(text) {
            const newTodo = { id: crypto.randomUUID(), text: text };
            startTransition(async () => {
                addOptimisticTodo(newTodo);
                await addTodoAction(newTodo);
            });
        }

        return (
            <div>
                <button onClick={() => handleAddTodo('New todo')}>Add Todo</button>
                <ul>
                    {optimisticTodos.map(todo => (
                        <li key={todo.id}>
                            {todo.text} {todo.pending && "(Adding...)"}
                        </li>
                    ))}
                </ul>
            </div>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function addTodo(todo) {
        await new Promise((res) => setTimeout(res, 1000));
        // In a real app, this would save to the server
        return { ...todo, pending: false };
    }
    ```

`reducer` получает текущий список задач и новую задачу. Это важно: если проп `todos` изменится, пока добавление ожидает (например, другой пользователь добавил задачу), React обновит оптимистичное состояние, заново запустив редюсер с обновлённым списком. Новая задача добавится к свежему списку, а не к устаревшей копии.

!!!note "Примечание"

    У каждого оптимистичного элемента есть флаг `pending: true`, чтобы показать загрузку у отдельных элементов. Когда сервер ответит и родитель обновит канонический список `todos` сохранённым элементом, оптимистичное состояние сменится на подтверждённый элемент без флага ожидания.

### Несколько типов `action` {#handling-multiple-action-types}

Если нужно несколько видов оптимистичных обновлений (например, добавление и удаление), используйте редюсер с объектами `action`.

В этом примере корзины один редюсер обрабатывает добавление и удаление:

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import { addToCart, removeFromCart, updateQuantity } from './actions.js';
    import ShoppingCart from './ShoppingCart';

    export default function App() {
        const [cart, setCart] = useState([]);

        const cartActions = {
            async add(item) {
                await addToCart(item);
                startTransition(() => {
                    setCart(current => {
                        const exists = current.find(i => i.id === item.id);
                        if (exists) {
                            return current.map(i =>
                                i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
                            );
                        }
                        return [...current, { ...item, quantity: 1 }];
                    });
                });
            },
            async remove(id) {
                await removeFromCart(id);
                startTransition(() => {
                    setCart(current => current.filter(item => item.id !== id));
                });
            },
            async updateQuantity(id, quantity) {
                await updateQuantity(id, quantity);
                startTransition(() => {
                    setCart(current =>
                        current.map(item =>
                            item.id === id ? { ...item, quantity } : item
                        )
                    );
                });
            }
        };

        return <ShoppingCart cart={cart} cartActions={cartActions} />;
    }
    ```

=== "ShoppingCart.js"

    ```js

    import { useOptimistic, startTransition } from 'react';

    export default function ShoppingCart({ cart, cartActions }) {
        const [optimisticCart, dispatch] = useOptimistic(
            cart,
            (currentCart, action) => {
                switch (action.type) {
                    case 'add':
                        const exists = currentCart.find(item => item.id === action.item.id);
                        if (exists) {
                            return currentCart.map(item =>
                                item.id === action.item.id
                                    ? { ...item, quantity: item.quantity + 1, pending: true }
                                    : item
                            );
                        }
                        return [...currentCart, { ...action.item, quantity: 1, pending: true }];
                    case 'remove':
                        return currentCart.filter(item => item.id !== action.id);
                    case 'update_quantity':
                        return currentCart.map(item =>
                            item.id === action.id
                                ? { ...item, quantity: action.quantity, pending: true }
                                : item
                        );
                    default:
                        return currentCart;
                }
            }
        );

        function handleAdd(item) {
            startTransition(async () => {
                dispatch({ type: 'add', item });
                await cartActions.add(item);
            });
        }

        function handleRemove(id) {
            startTransition(async () => {
                dispatch({ type: 'remove', id });
                await cartActions.remove(id);
            });
        }

        function handleUpdateQuantity(id, quantity) {
            startTransition(async () => {
                dispatch({ type: 'update_quantity', id, quantity });
                await cartActions.updateQuantity(id, quantity);
            });
        }

        const total = optimisticCart.reduce(
            (sum, item) => sum + item.price * item.quantity,
            0
        );

        return (
            <div>
                <h2>Shopping Cart</h2>
                <div style={{ marginBottom: 16 }}>
                    <button onClick={() => handleAdd({
                        id: 1, name: 'T-Shirt', price: 25
                    })}>
                        Add T-Shirt ($25)
                    </button>{' '}
                    <button onClick={() => handleAdd({
                        id: 2, name: 'Mug', price: 15
                    })}>
                        Add Mug ($15)
                    </button>
                </div>
                {optimisticCart.length === 0 ? (
                    <p>Your cart is empty</p>
                ) : (
                    <ul>
                        {optimisticCart.map(item => (
                            <li key={item.id}>
                                {item.name} - ${item.price} ×
                                {item.quantity}
                                {' '}= ${item.price * item.quantity}
                                <button
                                    onClick={() => handleRemove(item.id)}
                                    style={{ marginLeft: 8 }}
                                >
                                    Remove
                                </button>
                                {item.pending && ' ...'}
                            </li>
                        ))}
                    </ul>
                )}
                <p><strong>Total: ${total}</strong></p>
            </div>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function addToCart(item) {
        await new Promise((res) => setTimeout(res, 800));
    }

    export async function removeFromCart(id) {
        await new Promise((res) => setTimeout(res, 800));
    }

    export async function updateQuantity(id, quantity) {
        await new Promise((res) => setTimeout(res, 800));
    }
    ```

Редюсер обрабатывает три типа `action` (`add`, `remove`, `update_quantity`) и для каждого возвращает новое оптимистичное состояние. Каждое `action` ставит флаг `pending: true`, чтобы показать обратную связь, пока выполняется [серверная функция](../rsc/server-functions.md).

### Оптимистичное удаление с восстановлением после ошибки {#optimistic-delete-with-error-recovery}

При оптимистичном удалении нужно обработать случай, когда действие завершается ошибкой.

В примере показано, как вывести сообщение об ошибке, если удаление не удалось: интерфейс сам откатывается и снова показывает элемент.

=== "App.js"

    ```js

    import { useState, startTransition } from 'react';
    import { deleteItem } from './actions.js';
    import ItemList from './ItemList';

    export default function App() {
        const [items, setItems] = useState([
            { id: 1, name: 'Learn React' },
            { id: 2, name: 'Build an app' },
            { id: 3, name: 'Deploy to production' },
        ]);

        async function deleteAction(id) {
            await deleteItem(id);
            startTransition(() => {
                setItems(current => current.filter(item => item.id !== id));
            });
        }

        return <ItemList items={items} deleteAction={deleteAction} />;
    }
    ```

=== "ItemList.js"

    ```js

    import { useState, useOptimistic, startTransition } from 'react';

    export default function ItemList({ items, deleteAction }) {
        const [error, setError] = useState(null);
        const [optimisticItems, removeItem] = useOptimistic(
            items,
            (currentItems, idToRemove) =>
                currentItems.map(item =>
                    item.id === idToRemove
                        ? { ...item, deleting: true }
                        : item
                )
        );

        function handleDelete(id) {
            setError(null);
            startTransition(async () => {
                removeItem(id);
                try {
                    await deleteAction(id);
                } catch (e) {
                    setError(e.message);
                }
            });
        }

        return (
            <div>
                <h2>Your Items</h2>
                <ul>
                    {optimisticItems.map(item => (
                        <li
                            key={item.id}
                            style={{
                                opacity: item.deleting ? 0.5 : 1,
                                textDecoration: item.deleting ? 'line-through' : 'none',
                                transition: 'opacity 0.2s'
                            }}
                        >
                            {item.name}
                            <button
                                onClick={() => handleDelete(item.id)}
                                disabled={item.deleting}
                                style={{ marginLeft: 8 }}
                            >
                                {item.deleting ? 'Deleting...' : 'Delete'}
                            </button>
                        </li>
                    ))}
                </ul>
                {error && (
                    <p style={{ color: 'red', padding: 8, background: '#fee' }}>
                        {error}
                    </p>
                )}
            </div>
        );
    }
    ```

=== "actions.js"

    ```js

    export async function deleteItem(id) {
        await new Promise((res) => setTimeout(res, 1000));
        // Item 3 always fails to demonstrate error recovery
        if (id === 3) {
            throw new Error('Cannot delete. Permission denied.');
        }
    }
    ```

Попробуйте удалить «Deploy to production». Когда удаление не удастся, элемент сам появится в списке снова.


### Оптимистическое обновление форм {#optimistically-updating-with-forms}

Хук `useOptimistic` предоставляет возможность оптимистично обновлять пользовательский интерфейс до завершения фоновой операции, например, сетевого запроса. В контексте форм эта техника помогает сделать приложения более отзывчивыми. Когда пользователь отправляет форму, вместо того чтобы ждать, пока ответ сервера отразит изменения, интерфейс сразу же обновляется с ожидаемым результатом.

Например, когда пользователь вводит сообщение в форму и нажимает кнопку "Отправить", хук `useOptimistic` позволяет сообщению сразу же появиться в списке с надписью "Отправка...", еще до того, как оно будет отправлено на сервер. Такой "оптимистичный" подход создает впечатление скорости и оперативности. Затем форма пытается действительно отправить сообщение в фоновом режиме. Как только сервер подтверждает, что сообщение получено, метка "Отправка..." удаляется.

=== "App.js"

    ```js
    import { useOptimistic, useState, useRef } from 'react';
    import { deliverMessage } from './actions.js';

    function Thread({ messages, sendMessage }) {
    	const formRef = useRef();
    	async function formAction(formData) {
    		addOptimisticMessage(formData.get('message'));
    		formRef.current.reset();
    		await sendMessage(formData);
    	}
    	const [
    		optimisticMessages,
    		addOptimisticMessage,
    	] = useOptimistic(messages, (state, newMessage) => [
    		...state,
    		{
    			text: newMessage,
    			sending: true,
    		},
    	]);

    	return (
    		<>
    			{optimisticMessages.map((message, index) => (
    				<div key={index}>
    					{message.text}
    					{!!message.sending && (
    						<small> (Sending...)</small>
    					)}
    				</div>
    			))}
    			<form action={formAction} ref={formRef}>
    				<input
    					type="text"
    					name="message"
    					placeholder="Hello!"
    				/>
    				<button type="submit">Send</button>
    			</form>
    		</>
    	);
    }

    export default function App() {
    	const [messages, setMessages] = useState([
    		{ text: 'Hello there!', sending: false, key: 1 },
    	]);
    	async function sendMessage(formData) {
    		const sentMessage = await deliverMessage(
    			formData.get('message')
    		);
    		setMessages((messages) => [
    			...messages,
    			{ text: sentMessage },
    		]);
    	}
    	return (
    		<Thread
    			messages={messages}
    			sendMessage={sendMessage}
    		/>
    	);
    }
    ```

=== "actions.js"

    ```js
    export async function deliverMessage(message) {
    	await new Promise((res) => setTimeout(res, 1000));
    	return message;
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/hsvs2d?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="nostalgic-cdn-hsvs2d" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Устранение неполадок {#troubleshooting}

### Ошибка: «An optimistic state update occurred outside a Transition or Action» {#an-optimistic-state-update-occurred-outside-a-transition-or-action}

Вы можете увидеть такую ошибку:

```text linenums="0"
<ConsoleLogLine level="error">

An optimistic state update occurred outside a Transition or Action. To fix, move the update to an Action, or wrap with `startTransition`.

</ConsoleLogLine>
```

Оптимистичный сеттер нужно вызывать внутри `startTransition`:

```js
// 🚩 Incorrect: outside a Transition
function handleClick() {
  setOptimistic(newValue);  // Warning!
  // ...
}

// ✅ Correct: inside a Transition
function handleClick() {
  startTransition(async () => {
    setOptimistic(newValue);
    // ...
  });
}

// ✅ Also correct: inside an Action prop
function submitAction(formData) {
  setOptimistic(newValue);
  // ...
}
```

Если вызвать сеттер вне действия, оптимистичное состояние на мгновение появится и сразу вернётся к исходному значению. Так происходит, потому что нет перехода, который «удержал» бы оптимистичное состояние, пока выполняется действие.

### Ошибка: «Cannot update optimistic state while rendering» {#cannot-update-optimistic-state-while-rendering}

Вы можете увидеть такую ошибку:

```text linenums="0"
<ConsoleLogLine level="error">

Cannot update optimistic state while rendering.

</ConsoleLogLine>
```

Эта ошибка возникает, если оптимистичный сеттер вызывают во время фазы рендера компонента. Его можно вызывать только из обработчиков событий, эффектов или других колбэков:

```js
// 🚩 Incorrect: calling during render
function MyComponent({ items }) {
  const [isPending, setPending] = useOptimistic(false);

  // This runs during render - not allowed!
  setPending(true);

  // ...
}

// ✅ Correct: calling inside startTransition
function MyComponent({ items }) {
  const [isPending, setPending] = useOptimistic(false);

  function handleClick() {
    startTransition(() => {
      setPending(true);
      // ...
    });
  }

  // ...
}

// ✅ Also correct: calling from an Action
function MyComponent({ items }) {
  const [isPending, setPending] = useOptimistic(false);

  function action() {
    setPending(true);
    // ...
  }

  // ...
}
```

### Оптимистичные обновления показывают устаревшие значения {#my-optimistic-updates-show-stale-values}

Если оптимистичное состояние как будто считается от старых данных, используйте функцию обновления или редюсер, чтобы считать его относительно текущего состояния.

```js
// May show stale data if state changes during Action
const [optimistic, setOptimistic] = useOptimistic(count);
setOptimistic(5);  // Always sets to 5, even if count changed

// Better: relative updates handle state changes correctly
const [optimistic, adjust] = useOptimistic(count, (current, delta) => current + delta);
adjust(1);  // Always adds 1 to whatever the current count is
```

Подробности в разделе [Обновление состояния на основе текущего состояния](#updating-state-based-on-current-state).

### Непонятно, ожидает ли оптимистичное обновление {#i-dont-know-if-my-optimistic-update-is-pending}

Чтобы узнать, ожидает ли `useOptimistic`, есть три варианта:

1. **Проверить `optimisticValue === value`**

```js
const [optimistic, setOptimistic] = useOptimistic(value);
const isPending = optimistic !== value;
```

Если значения не равны, переход ещё идёт.

2. **Добавить `useTransition`**

```js
const [isPending, startTransition] = useTransition();
const [optimistic, setOptimistic] = useOptimistic(value);

//...
startTransition(() => {
  setOptimistic(state);
})
```

Поскольку `useTransition` под капотом использует `useOptimistic` для `isPending`, это то же самое, что вариант 1.

3. **Добавить флаг `pending` в редюсер**

```js
const [optimistic, addOptimistic] = useOptimistic(
  items,
  (state, newItem) => [...state, { ...newItem, isPending: true }]
);
```

У каждого оптимистичного элемента свой флаг, поэтому состояние загрузки можно показать у отдельных элементов.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useOptimistic](https://react.dev/reference/react/useOptimistic)</small>
