# useMemo

**`useMemo`** - это хук React, позволяющий кэшировать результат вычисления между повторными рендерингами.

<!-- 0001.part.md -->

```js
const cachedValue = useMemo(calculateValue, dependencies);
```

## Описание

### `useMemo(calculateValue, dependencies)`

Вызовите `useMemo` на верхнем уровне вашего компонента для кэширования вычислений между повторными рендерингами:

<!-- 0003.part.md -->

```js
import { useMemo } from 'react';

function TodoList({ todos, tab }) {
    const visibleTodos = useMemo(
        () => filterTodos(todos, tab),
        [todos, tab]
    );
    // ...
}
```

#### Параметры

-   `calculateValue`: Функция, вычисляющая значение, которое вы хотите кэшировать. Она должна быть чистой, не принимать аргументов и возвращать значение любого типа. React будет вызывать вашу функцию во время начального рендера. При последующих рендерах React будет возвращать то же значение, если `зависимости` не изменились с момента последнего рендера. В противном случае он вызовет `calculateValue`, вернет результат и сохранит его, чтобы можно было использовать в дальнейшем.

-   `зависимости`: Список всех реактивных значений, на которые ссылается код `calculateValue`. Реактивные значения включают пропсы, состояние, а также все переменные и функции, объявленные непосредственно в теле вашего компонента. Если ваш линтер [настроен на React](../learn/editor-setup.md), он проверит, что каждое реактивное значение правильно указано в качестве зависимости. Список зависимостей должен иметь постоянное количество элементов и быть написан inline по типу `[dep1, dep2, dep3]`. React будет сравнивать каждую зависимость с предыдущим значением, используя сравнение [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is).

#### Возвраты

При первоначальном рендере `useMemo` возвращает результат вызова `calculateValue` без аргументов.

При последующих рендерах он либо вернет уже сохраненное значение из последнего рендера (если зависимости не изменились), либо снова вызовет `calculateValue` и вернет результат, который вернул `calculateValue`.

#### Ограничения

-   `useMemo` - это хук, поэтому вы можете вызывать его только **на верхнем уровне вашего компонента** или ваших собственных хуков. Вы не можете вызывать его внутри циклов или условий. Если вам это нужно, создайте новый компонент и переместите состояние в него.
-   В строгом режиме React будет **вызывать вашу функцию вычисления дважды**, чтобы помочь вам найти случайные примеси Это поведение только для разработки и не влияет на производство. Если ваша функция вычисления чиста (как и должно быть), это не должно повлиять на вашу логику. Результат одного из вызовов будет проигнорирован.
-   React **не будет выбрасывать кэшированное значение, если для этого нет особой причины.** Например, в разработке React выбрасывает кэш, когда вы редактируете файл вашего компонента. Как в разработке, так и в производстве, React отбрасывает кэш, если ваш компонент приостанавливается во время начального монтирования. В будущем React может добавить больше функций, которые будут использовать преимущества отбрасывания кэша - например, если React в будущем добавит встроенную поддержку виртуализированных списков, то будет иметь смысл отбрасывать кэш для элементов, которые прокручиваются из области просмотра виртуализированной таблицы. Это будет хорошо, если вы полагаетесь на useMemo исключительно как на оптимизацию производительности. В противном случае более подходящим вариантом может быть переменная состояния или ссылка.

!!!note ""

    Подобное кэширование возвращаемых значений также известно как [_мемоизация_](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%BC%D0%BE%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F), поэтому этот хук называется `useMemo`.

## Использование

### Пропуск дорогостоящих перерасчетов

Чтобы кэшировать вычисления между повторными рендерами, оберните их в вызов `useMemo` на верхнем уровне вашего компонента:

<!-- 0006.part.md -->

```js
import { useMemo } from 'react';

function TodoList({ todos, tab, theme }) {
    const visibleTodos = useMemo(
        () => filterTodos(todos, tab),
        [todos, tab]
    );
    // ...
}
```

<!-- 0007.part.md -->

Вам нужно передать две вещи в `useMemo`:

1.  функцию вычисления, которая не принимает аргументов, например `() =>`, и возвращает то, что вы хотели вычислить.
2.  список зависимостей, включающий каждое значение в вашем компоненте, которое используется в расчете.

На первом рендере значение, которое вы получите от `useMemo`, будет результатом вызова вашего вычисления.

При каждом последующем рендере React будет сравнивать зависимости с зависимостями, которые вы передали во время последнего рендера. Если ни одна из зависимостей не изменилась (по сравнению с [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), `useMemo` вернет значение, которое вы уже вычислили ранее. В противном случае React повторно выполнит расчет и вернет новое значение.

Другими словами, `useMemo` кэширует результат вычислений между повторными рендерами, пока не изменятся зависимости.

**Давайте рассмотрим пример, чтобы увидеть, когда это полезно.**

По умолчанию React будет запускать заново все тело вашего компонента при каждом повторном рендеринге. Например, если этот `TodoList` обновит свое состояние или получит новые пропсы от своего родителя, функция `filterTodos` будет запущена заново:

<!-- 0008.part.md -->

```js
function TodoList({ todos, tab, theme }) {
    const visibleTodos = filterTodos(todos, tab);
    // ...
}
```

<!-- 0009.part.md -->

Обычно это не является проблемой, поскольку большинство вычислений выполняются очень быстро. Однако, если вы фильтруете или преобразуете большой массив, или выполняете какое-то дорогостоящее вычисление, вы можете захотеть пропустить его, если данные не изменились. Если `todos` и `tab` те же, что и во время последнего рендеринга, то обернув вычисления в `useMemo`, как и ранее, вы сможете повторно использовать `visibleTodos`, который вы уже вычислили ранее.

Этот тип кэширования называется _[memoization](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%BC%D0%BE%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)_.

!!!note ""

    **Вы должны полагаться на `useMemo` только в качестве оптимизации производительности.** Если ваш код не работает без него, найдите основную проблему и сначала устраните ее. Затем вы можете добавить `useMemo` для улучшения производительности.

!!!note "Как определить, является ли вычисление дорогим?"

    В общем, если вы не создаете тысячи объектов или не перебираете их в цикле, то, скорее всего, это не дорого. Если вы хотите получить больше уверенности, вы можете добавить консольный журнал, чтобы измерить время, затраченное на часть кода:

    <!-- 0010.part.md -->

    ```js
    console.time('filter array');
    const visibleTodos = filterTodos(todos, tab);
    console.timeEnd('filter array');
    ```

    <!-- 0011.part.md -->

    Выполните измеряемое действие (например, введите текст в input). После этого вы увидите в консоли журналы типа `фильтр массива: 0.15ms` в вашей консоли. Если общее время, записанное в журнал, составляет значительную величину (скажем, `1 мс` или больше), возможно, имеет смысл запомнить этот расчет. В качестве эксперимента вы можете обернуть расчет в `useMemo`, чтобы проверить, уменьшилось ли общее время регистрации для данного взаимодействия или нет:

    <!-- 0012.part.md -->

    ```js
    console.time('filter array');
    const visibleTodos = useMemo(() => {
    	return filterTodos(todos, tab); // Skipped if todos and tab haven't changed
    }, [todos, tab]);
    console.timeEnd('filter array');
    ```

    <!-- 0013.part.md -->

    `useMemo` не сделает _первый_ рендеринг быстрее. Это только поможет вам пропустить ненужную работу над обновлениями.

    Имейте в виду, что ваша машина, вероятно, быстрее, чем у ваших пользователей, поэтому хорошей идеей будет проверить производительность с помощью искусственного замедления. Например, Chrome предлагает для этого опцию [CPU Throttling](https://developer.chrome.com/blog/new-in-devtools-61/#throttling).

    Также обратите внимание, что измерение производительности в процессе разработки не даст вам наиболее точных результатов. (Например, если включен [Строгий режим](StrictMode.md), каждый компонент будет отображаться дважды, а не один раз). Чтобы получить наиболее точные результаты, создайте приложение для производства и протестируйте его на устройстве, которое есть у ваших пользователей.

!!!note "Должны ли вы добавлять useMemo везде?"

    Если ваше приложение похоже на этот сайт, и большинство взаимодействий являются грубыми (например, замена страницы или целого раздела), мемоизация обычно не нужна. С другой стороны, если ваше приложение больше похоже на редактор рисунков, и большинство взаимодействий являются гранулированными (например, перемещение фигур), то мемоизация может оказаться очень полезной.

    Оптимизация с помощью `useMemo` полезна лишь в некоторых случаях:

    -   Вычисления, которые вы помещаете в `useMemo`, заметно медленные, и их зависимости редко меняются.
    -   Вы передаете его как prop компоненту, обернутому в [`memo`](memo.md). Вы хотите пропустить повторный рендеринг, если значение не изменилось. Мемоизация позволяет вашему компоненту перерисовываться только тогда, когда зависимости не меняются.
    -   Значение, которое вы передаете, позже будет использоваться как зависимость какого-нибудь Hook. Например, возможно, от него зависит другое значение вычисления `useMemo`. Или, может быть, вы зависите от этого значения из [`useEffect.`](useEffect.md).

    В других случаях нет никакой пользы от обертывания вычисления в `useMemo`. Вреда от этого тоже нет, поэтому некоторые команды предпочитают не думать об отдельных случаях и мемоизировать как можно больше. Недостатком такого подхода является то, что код становится менее читабельным. Кроме того, не вся мемоизация эффективна: одного значения, которое "всегда новое", достаточно, чтобы нарушить мемоизацию для всего компонента.

    **На практике вы можете сделать ненужной мемоизацию, следуя нескольким принципам:**.

    1.  Когда компонент визуально обертывает другие компоненты, позвольте ему [принимать JSX в качестве дочерних компонентов](../learn/passing-props-to-a-component.md) Таким образом, когда компонент-обертка обновляет свое собственное состояние, React знает, что его дочерние компоненты не нужно перерисовывать.
    2.  Предпочитайте локальное состояние и не [поднимайте состояние вверх](../learn/sharing-state-between-components.md) дальше, чем это необходимо. Например, не храните переходные состояния, такие как формы и то, наведен ли элемент на вершину вашего дерева, в глобальной библиотеке состояний.
    3.  Сохраняйте чистоту [логики рендеринга](../learn/keeping-components-pure.md) Если повторный рендеринг компонента вызывает проблему или приводит к заметным визуальным артефактам, это ошибка в вашем компоненте! Исправьте ошибку вместо того, чтобы добавлять мемоизацию.
    4.  Избегайте [ненужных Эффектов](../learn/you-might-not-need-an-effect.md), обновляющих состояние. Большинство проблем с производительностью в приложениях React вызвано цепочками обновлений, исходящих от Эффектов, которые заставляют ваши компоненты рендериться снова и снова.
    5.  Попробуйте [удалить ненужные зависимости из ваших Эффектов](../learn/removing-effect-dependencies.md) Например, вместо мемоизации часто проще переместить какой-то объект или функцию внутрь Эффекта или за пределы компонента.

    Если конкретное взаимодействие все еще кажется нестабильным, [используйте профилировщик React Developer Tools](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html), чтобы увидеть, какие компоненты больше всего выиграют от мемоизации, и добавьте мемоизацию там, где это необходимо. Эти принципы облегчают отладку и понимание ваших компонентов, поэтому следовать им полезно в любом случае. В долгосрочной перспективе мы изучаем [автоматическое выполнение гранулярной мемоизации](https://www.youtube.com/watch?v=lGEMwh32soc), чтобы решить эту проблему раз и навсегда.

### Разница между useMemo и вычислением значения напрямую

#### 1. Пропуск пересчета с `useMemo`

В этом примере реализация `filterTodos` **искусственно замедлена**, чтобы вы могли увидеть, что происходит, когда какая-то функция JavaScript, вызываемая вами во время рендеринга, действительно медленная. Попробуйте переключить вкладки и переключить тему.

Переключение вкладок кажется медленным, потому что это заставляет замедленный `filterTodos` повторно выполняться. Это ожидаемо, потому что `вкладка` изменилась, и поэтому все вычисления _нужно_ выполнить заново. (Если вам интересно, почему он выполняется дважды, это объясняется здесь).

Переключите тему. **Благодаря `useMemo`, это быстро, несмотря на искусственное замедление!** Медленный вызов `filterTodos` был пропущен, потому что `todos` и `tab` (которые вы передаете как зависимости `useMemo`) не изменились с момента последнего рендера.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { createTodos } from './utils.js';
    import TodoList from './TodoList.js';

    const todos = createTodos();

    export default function App() {
    	const [tab, setTab] = useState('all');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<button onClick={() => setTab('all')}>
    				All
    			</button>
    			<button onClick={() => setTab('active')}>
    				Active
    			</button>
    			<button onClick={() => setTab('completed')}>
    				Completed
    			</button>
    			<br />
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Dark mode
    			</label>
    			<hr />
    			<TodoList
    				todos={todos}
    				tab={tab}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "TodoList.js"

    ```js
    import { useMemo } from 'react';
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = useMemo(
    		() => filterTodos(todos, tab),
    		[todos, tab]
    	);
    	return (
    		<div className={theme}>
    			<p>
    				<b>
    					Note: <code>filterTodos</code> is
    					artificially slowed down!
    				</b>
    			</p>
    			<ul>
    				{visibleTodos.map((todo) => (
    					<li key={todo.id}>
    						{todo.completed ? (
    							<s>{todo.text}</s>
    						) : (
    							todo.text
    						)}
    					</li>
    				))}
    			</ul>
    		</div>
    	);
    }
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	console.log(
    		'[ARTIFICIALLY SLOW] Filtering ' +
    			todos.length +
    			' todos for "' +
    			tab +
    			'" tab.'
    	);
    	let startTime = performance.now();
    	while (performance.now() - startTime < 500) {
    		// Do nothing for 500 ms to emulate extremely slow code
    	}

    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

#### 2. Всегда пересчитывает значение

В этом примере реализация `filterTodos` также **искусственно замедлена**, чтобы вы могли увидеть, что происходит, когда какая-то функция JavaScript, которую вы вызываете во время рендеринга, действительно медленная. Попробуйте переключить вкладки и переключить тему.

В отличие от предыдущего примера, переключение темы теперь также происходит медленно! Это происходит потому, что **в этой версии отсутствует вызов `useMemo`,** поэтому искусственно замедляющий работу `filterTodos` вызывается при каждом повторном рендеринге. Он вызывается, даже если изменилась только `тема`.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { createTodos } from './utils.js';
    import TodoList from './TodoList.js';

    const todos = createTodos();

    export default function App() {
    	const [tab, setTab] = useState('all');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<button onClick={() => setTab('all')}>
    				All
    			</button>
    			<button onClick={() => setTab('active')}>
    				Active
    			</button>
    			<button onClick={() => setTab('completed')}>
    				Completed
    			</button>
    			<br />
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Dark mode
    			</label>
    			<hr />
    			<TodoList
    				todos={todos}
    				tab={tab}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "TodoList.js"

    ```js
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = filterTodos(todos, tab);
    	return (
    		<div className={theme}>
    			<ul>
    				<p>
    					<b>
    						Note: <code>filterTodos</code> is
    						artificially slowed down!
    					</b>
    				</p>
    				{visibleTodos.map((todo) => (
    					<li key={todo.id}>
    						{todo.completed ? (
    							<s>{todo.text}</s>
    						) : (
    							todo.text
    						)}
    					</li>
    				))}
    			</ul>
    		</div>
    	);
    }
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	console.log(
    		'[ARTIFICIALLY SLOW] Filtering ' +
    			todos.length +
    			' todos for "' +
    			tab +
    			'" tab.'
    	);
    	let startTime = performance.now();
    	while (performance.now() - startTime < 500) {
    		// Do nothing for 500 ms to emulate extremely slow code
    	}

    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

Однако, вот тот же код **с искусственным замедлением.** Отсутствие `useMemo` ощутимо или нет?

=== "App.js"

```js
import { useState } from 'react';
import { createTodos } from './utils.js';
import TodoList from './TodoList.js';

const todos = createTodos();

export default function App() {
    const [tab, setTab] = useState('all');
    const [isDark, setIsDark] = useState(false);
    return (
        <>
            <button onClick={() => setTab('all')}>
                All
            </button>
            <button onClick={() => setTab('active')}>
                Active
            </button>
            <button onClick={() => setTab('completed')}>
                Completed
            </button>
            <br />
            <label>
                <input
                    type="checkbox"
                    checked={isDark}
                    onChange={(e) =>
                        setIsDark(e.target.checked)
                    }
                />
                Dark mode
            </label>
            <hr />
            <TodoList
                todos={todos}
                tab={tab}
                theme={isDark ? 'dark' : 'light'}
            />
        </>
    );
}
```

=== "TodoList.js"

    ```js
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = filterTodos(todos, tab);
    	return (
    		<div className={theme}>
    			<ul>
    				{visibleTodos.map((todo) => (
    					<li key={todo.id}>
    						{todo.completed ? (
    							<s>{todo.text}</s>
    						) : (
    							todo.text
    						)}
    					</li>
    				))}
    			</ul>
    		</div>
    	);
    }
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	console.log(
    		'Filtering ' +
    			todos.length +
    			' todos for "' +
    			tab +
    			'" tab.'
    	);

    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

Довольно часто код без мемоизации работает нормально. Если ваши взаимодействия достаточно быстрые, то мемоизация может и не понадобиться.

Вы можете попробовать увеличить количество элементов todo в `utils.js` и посмотреть, как изменится поведение. Этот конкретный расчет был не очень дорогим изначально, но если количество todos значительно вырастет, то большая часть накладных расходов будет приходиться на повторное отображение, а не на фильтрацию. Читайте ниже, чтобы узнать, как можно оптимизировать повторный просмотр с помощью `useMemo`.

### Пропуск повторного рендеринга компонентов

В некоторых случаях `useMemo` также может помочь вам оптимизировать производительность повторного рендеринга дочерних компонентов. Чтобы проиллюстрировать это, допустим, компонент `TodoList` передает `visibleTodos` в качестве параметра дочернему компоненту `List`:

<!-- 0039.part.md -->

```js
export default function TodoList({ todos, tab, theme }) {
    // ...
    return (
        <div className={theme}>
            <List items={visibleTodos} />
        </div>
    );
}
```

<!-- 0040.part.md -->

Вы заметили, что при переключении пропса `theme` приложение на мгновение замирает, но если убрать `<List />` из JSX, то все работает быстро. Это говорит о том, что стоит попробовать оптимизировать компонент `List`.

**По умолчанию, когда компонент рендерится, React рекурсивно рендерит все его дочерние элементы.** Вот почему, когда `TodoList` рендерится с другой `темой`, компонент `List` _также_ рендерится. Это хорошо для компонентов, которым не требуется много вычислений для повторного рендеринга. Но если вы убедились, что повторный рендеринг медленный, вы можете сказать `List` пропустить повторный рендеринг, когда его пропсы такие же, как и при последнем рендере, обернув его в [`memo`:](memo.md)

<!-- 0041.part.md -->

```js
import { memo } from 'react';

const List = memo(function List({ items }) {
    // ...
});
```

<!-- 0042.part.md -->

**После этого изменения `List` будет пропускать повторный рендеринг, если все его пропсы _те же_, что и при последнем рендеринге.** Вот где кэширование вычислений становится важным! Представьте, что вы вычислили `visibleTodos` без `useMemo`:

<!-- 0043.part.md -->

```js
export default function TodoList({ todos, tab, theme }) {
    // Every time the theme changes, this will be a different array...
    const visibleTodos = filterTodos(todos, tab);
    return (
        <div className={theme}>
            {/* ... so List's props will never be the same, and it will re-render every time */}
            <List items={visibleTodos} />
        </div>
    );
}
```

<!-- 0044.part.md -->

**В приведенном выше примере функция `filterTodos` всегда создает _разный_ массив,** подобно тому, как объектный литерал `{}` всегда создает новый объект. Обычно это не является проблемой, но это означает, что пропс `List` никогда не будет одинаковым, и ваша оптимизация [`memo`](memo.md) не будет работать. Вот здесь-то и пригодится `useMemo`:

<!-- 0045.part.md -->

```js
export default function TodoList({ todos, tab, theme }) {
    // Tell React to cache your calculation between re-renders...
    const visibleTodos = useMemo(
        () => filterTodos(todos, tab),
        [todos, tab] // ...so as long as these dependencies don't change...
    );
    return (
        <div className={theme}>
            {/* ...List will receive the same props and can skip re-rendering */}
            <List items={visibleTodos} />
        </div>
    );
}
```

<!-- 0046.part.md -->

**Вернув расчет `visibleTodos` в `useMemo`, вы гарантируете, что он будет иметь _одно и то же_ значение между повторными рендерингами** (пока не изменятся зависимости). Вы не обязаны _обертывать_ вычисления в `useMemo`, если только вы не делаете это по какой-то конкретной причине. В данном примере причина в том, что вы передаете его компоненту, обернутому в [`memo`](memo.md), и это позволяет ему пропустить повторный рендеринг. Есть еще несколько причин добавить `useMemo`, которые описаны далее на этой странице.

!!!note "Мемоизация отдельных узлов JSX"

    Вместо того чтобы обертывать `List` в [`memo`](memo.md), можно обернуть сам JSX-узел `<List />` в `useMemo`:

    <!-- 0047.part.md -->

    ```js
    export default function TodoList({ todos, tab, theme }) {
    	const visibleTodos = useMemo(
    		() => filterTodos(todos, tab),
    		[todos, tab]
    	);
    	const children = useMemo(
    		() => <List items={visibleTodos} />,
    		[visibleTodos]
    	);
    	return <div className={theme}>{children}</div>;
    }
    ```

    <!-- 0048.part.md -->

    Поведение будет таким же. Если `visibleTodos` не изменился, `List` не будет перерендерирован.

    Узел JSX типа `<List items={visibleTodos} />` - это объект типа `{ type: List, props: { items: visibleTodos } }`. Создание этого объекта очень дешево, но React не знает, совпадает ли его содержимое с прошлым разом или нет. Поэтому по умолчанию React перерендерит компонент `List`.

    Однако, если React видит тот же самый JSX, что и во время предыдущего рендеринга, он не будет пытаться перерендерить ваш компонент. Это происходит потому, что узлы JSX являются [неизменяемыми](https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82). Объект узла JSX не мог измениться с течением времени, поэтому React знает, что можно пропустить повторный рендеринг. Однако, чтобы это сработало, узел должен _фактически быть тем же объектом_, а не просто выглядеть одинаково в коде. Именно это и делает `useMemo` в данном примере.

    Ручное обертывание JSX-узлов в `useMemo` не очень удобно. Например, вы не можете сделать это условно. Обычно поэтому вместо обертывания JSX-узлов вы оборачиваете компоненты с помощью [`memo`](memo.md).

### Разница между пропуском рендеринга и постоянным рендерингом

#### 1. Пропуск повторного рендеринга с `useMemo` и `memo`

В этом примере компонент `List` **искусственно замедлен**, чтобы вы могли увидеть, что происходит, когда рендеринг компонента React действительно медленный. Попробуйте переключить вкладки и переключить тему.

Переключение вкладок кажется медленным, потому что это заставляет замедленный `List` повторно рендериться. Это ожидаемо, потому что `вкладка` изменилась, и вам нужно отразить новый выбор пользователя на экране.

Далее попробуйте переключить тему. **Благодаря `useMemo` вместе с [`memo`](memo.md) это происходит быстро, несмотря на искусственное замедление!** Список `List` пропустил повторный рендеринг, потому что массив `visibleItems` не изменился с момента последнего рендеринга. Массив `visibleItems` не изменился, потому что `todos` и `tab` (которые вы передаете в качестве зависимостей в `useMemo`) не изменились с момента последнего рендеринга.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { createTodos } from './utils.js';
    import TodoList from './TodoList.js';

    const todos = createTodos();

    export default function App() {
    	const [tab, setTab] = useState('all');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<button onClick={() => setTab('all')}>
    				All
    			</button>
    			<button onClick={() => setTab('active')}>
    				Active
    			</button>
    			<button onClick={() => setTab('completed')}>
    				Completed
    			</button>
    			<br />
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Dark mode
    			</label>
    			<hr />
    			<TodoList
    				todos={todos}
    				tab={tab}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "TodoList.js"

    ```js
    import { useMemo } from 'react';
    import List from './List.js';
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = useMemo(
    		() => filterTodos(todos, tab),
    		[todos, tab]
    	);
    	return (
    		<div className={theme}>
    			<p>
    				<b>
    					Note: <code>List</code> is artificially
    					slowed down!
    				</b>
    			</p>
    			<List items={visibleTodos} />
    		</div>
    	);
    }
    ```

=== "List.js"

    ```js
    import { memo } from 'react';

    const List = memo(function List({ items }) {
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering <List /> with ' +
    			items.length +
    			' items'
    	);
    	let startTime = performance.now();
    	while (performance.now() - startTime < 500) {
    		// Do nothing for 500 ms to emulate extremely slow code
    	}

    	return (
    		<ul>
    			{items.map((item) => (
    				<li key={item.id}>
    					{item.completed ? (
    						<s>{item.text}</s>
    					) : (
    						item.text
    					)}
    				</li>
    			))}
    		</ul>
    	);
    });

    export default List;
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

#### 2. Всегда перерендеринг компонента

В этом примере реализация `List` также **искусственно замедлена**, чтобы вы могли увидеть, что происходит, когда какой-либо компонент React, который вы рендерите, действительно медленный. Попробуйте переключить вкладки и переключить тему.

В отличие от предыдущего примера, переключение темы теперь также происходит медленно! Это происходит потому, что **в этой версии нет вызова `useMemo`,** поэтому `visibleTodos` - это всегда другой массив, и замедленный компонент `List` не может пропустить повторный рендеринг.

=== "App.js"

    ```js
    import { useState } from 'react';
    import { createTodos } from './utils.js';
    import TodoList from './TodoList.js';

    const todos = createTodos();

    export default function App() {
    	const [tab, setTab] = useState('all');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<button onClick={() => setTab('all')}>
    				All
    			</button>
    			<button onClick={() => setTab('active')}>
    				Active
    			</button>
    			<button onClick={() => setTab('completed')}>
    				Completed
    			</button>
    			<br />
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Dark mode
    			</label>
    			<hr />
    			<TodoList
    				todos={todos}
    				tab={tab}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "TodoList.js"

    ```js
    import List from './List.js';
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = filterTodos(todos, tab);
    	return (
    		<div className={theme}>
    			<p>
    				<b>
    					Note: <code>List</code> is artificially
    					slowed down!
    				</b>
    			</p>
    			<List items={visibleTodos} />
    		</div>
    	);
    }
    ```

=== "List.js"

    ```js
    import { memo } from 'react';

    const List = memo(function List({ items }) {
    	console.log(
    		'[ARTIFICIALLY SLOW] Rendering <List /> with ' +
    			items.length +
    			' items'
    	);
    	let startTime = performance.now();
    	while (performance.now() - startTime < 500) {
    		// Do nothing for 500 ms to emulate extremely slow code
    	}

    	return (
    		<ul>
    			{items.map((item) => (
    				<li key={item.id}>
    					{item.completed ? (
    						<s>{item.text}</s>
    					) : (
    						item.text
    					)}
    				</li>
    			))}
    		</ul>
    	);
    });

    export default List;
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

Однако, вот тот же код **с искусственным замедлением.** Отсутствие `useMemo` ощутимо или нет?

=== "App.js"

    ```js
    import { useState } from 'react';
    import { createTodos } from './utils.js';
    import TodoList from './TodoList.js';

    const todos = createTodos();

    export default function App() {
    	const [tab, setTab] = useState('all');
    	const [isDark, setIsDark] = useState(false);
    	return (
    		<>
    			<button onClick={() => setTab('all')}>
    				All
    			</button>
    			<button onClick={() => setTab('active')}>
    				Active
    			</button>
    			<button onClick={() => setTab('completed')}>
    				Completed
    			</button>
    			<br />
    			<label>
    				<input
    					type="checkbox"
    					checked={isDark}
    					onChange={(e) =>
    						setIsDark(e.target.checked)
    					}
    				/>
    				Dark mode
    			</label>
    			<hr />
    			<TodoList
    				todos={todos}
    				tab={tab}
    				theme={isDark ? 'dark' : 'light'}
    			/>
    		</>
    	);
    }
    ```

=== "TodoList.js"

    ```js
    import List from './List.js';
    import { filterTodos } from './utils.js';

    export default function TodoList({ todos, theme, tab }) {
    	const visibleTodos = filterTodos(todos, tab);
    	return (
    		<div className={theme}>
    			<List items={visibleTodos} />
    		</div>
    	);
    }
    ```

=== "List.js"

    ```js
    import { memo } from 'react';

    function List({ items }) {
    	return (
    		<ul>
    			{items.map((item) => (
    				<li key={item.id}>
    					{item.completed ? (
    						<s>{item.text}</s>
    					) : (
    						item.text
    					)}
    				</li>
    			))}
    		</ul>
    	);
    }

    export default memo(List);
    ```

=== "utils.js"

    ```js
    export function createTodos() {
    	const todos = [];
    	for (let i = 0; i < 50; i++) {
    		todos.push({
    			id: i,
    			text: 'Todo ' + (i + 1),
    			completed: Math.random() > 0.5,
    		});
    	}
    	return todos;
    }

    export function filterTodos(todos, tab) {
    	return todos.filter((todo) => {
    		if (tab === 'all') {
    			return true;
    		} else if (tab === 'active') {
    			return !todo.completed;
    		} else if (tab === 'completed') {
    			return todo.completed;
    		}
    	});
    }
    ```

Довольно часто код без мемоизации работает нормально. Если ваши взаимодействия достаточно быстрые, мемоизация не нужна.

Помните, что вам нужно запустить React в производственном режиме, отключить [React Developer Tools](../learn/react-developer-tools.md) и использовать устройства, похожие на те, которые есть у пользователей вашего приложения, чтобы получить реальное представление о том, что на самом деле замедляет работу вашего приложения.

### Мемоизация зависимости от другого хука

Предположим, у вас есть вычисление, которое зависит от объекта, созданного непосредственно в теле компонента:

<!-- 0079.part.md -->

```js
function Dropdown({ allItems, text }) {
    const searchOptions = { matchMode: 'whole-word', text };

    const visibleItems = useMemo(() => {
        return searchItems(allItems, searchOptions);
    }, [allItems, searchOptions]); // 🚩 Caution: Dependency on an object created in the component body
    // ...
}
```

<!-- 0080.part.md -->

Такая зависимость от объекта сводит на нет смысл мемоизации. При повторном рендеринге компонента весь код, находящийся непосредственно в теле компонента, запускается снова. Так как `searchOptions` является зависимостью вашего вызова `useMemo`, и каждый раз она разная, React знает, что зависимости разные, и каждый раз пересчитывает `searchItems`.

Чтобы исправить это, вы можете мемоизировать объект `searchOptions` _самостоятельно_ перед передачей его в качестве зависимости:

<!-- 0081.part.md -->

```js
function Dropdown({ allItems, text }) {
    const searchOptions = useMemo(() => {
        return { matchMode: 'whole-word', text };
    }, [text]); // ✅ Only changes when text changes

    const visibleItems = useMemo(() => {
        return searchItems(allItems, searchOptions);
    }, [allItems, searchOptions]);
    // ✅ Only changes when allItems or searchOptions changes
    // ...
}
```

<!-- 0082.part.md -->

В приведенном выше примере, если `text` не изменился, объект `searchOptions` также не изменится. Однако еще лучшим решением является перемещение объявления объекта `searchOptions` _внутрь_ функции вычисления `useMemo`:

<!-- 0083.part.md -->

```js
function Dropdown({ allItems, text }) {
    const visibleItems = useMemo(() => {
        const searchOptions = {
            matchMode: 'whole-word',
            text,
        };
        return searchItems(allItems, searchOptions);
    }, [allItems, text]); // ✅ Only changes when allItems or text changes
    // ...
}
```

<!-- 0084.part.md -->

Теперь ваш расчет зависит непосредственно от `text` (который является строкой и не может "случайно" стать другим).

### Мемоизация функции

Предположим, что компонент `Form` обернут в [`memo`.](memo.md) Вы хотите передать ему функцию в качестве пропса:

<!-- 0085.part.md -->

```js
export default function ProductPage({
    productId,
    referrer,
}) {
    function handleSubmit(orderDetails) {
        post('/product/' + productId + '/buy', {
            referrer,
            orderDetails,
        });
    }

    return <Form onSubmit={handleSubmit} />;
}
```

<!-- 0086.part.md -->

Подобно тому, как `{}` создает другой объект, объявления функций типа `function() {}` и выражения типа `() => {}` создают _разную_ функцию при каждом повторном рендеринге. Само по себе создание новой функции не является проблемой. Это не то, чего нужно избегать! Однако, если компонент `Form` мемоизирован, предположительно вы хотите пропустить его повторное отображение, когда ни один пропс не изменился. Пропс, который _всегда_ меняется, уничтожит смысл мемоизации.

Чтобы мемоизировать функцию с помощью `useMemo`, ваша вычислительная функция должна возвращать другую функцию:

<!-- 0087.part.md -->

```js
export default function Page({ productId, referrer }) {
    const handleSubmit = useMemo(() => {
        return (orderDetails) => {
            post('/product/' + productId + '/buy', {
                referrer,
                orderDetails,
            });
        };
    }, [productId, referrer]);

    return <Form onSubmit={handleSubmit} />;
}
```

<!-- 0088.part.md -->

Это выглядит неуклюже! **Мемоизация функций достаточно распространена, поэтому в React есть встроенный хук специально для этого. Оберните ваши функции в [`useCallback`](useCallback.md) вместо `useMemo`**, чтобы избежать необходимости писать дополнительную вложенную функцию:

<!-- 0089.part.md -->

```js
export default function Page({ productId, referrer }) {
    const handleSubmit = useCallback(
        (orderDetails) => {
            post('/product/' + productId + '/buy', {
                referrer,
                orderDetails,
            });
        },
        [productId, referrer]
    );

    return <Form onSubmit={handleSubmit} />;
}
```

<!-- 0090.part.md -->

Два приведенных выше примера полностью эквивалентны. Единственное преимущество `useCallback` в том, что он позволяет вам избежать написания дополнительной вложенной функции внутри. Больше она ничего не делает. [Подробнее об `useCallback`](useCallback.md).

## Устранение неполадок

### Мой расчет выполняется дважды при каждом рендере

В [Строгом режиме](StrictMode.md) React будет вызывать некоторые из ваших функций дважды вместо одного раза:

<!-- 0091.part.md -->

```js
function TodoList({ todos, tab }) {
    // This component function will run twice for every render.

    const visibleTodos = useMemo(() => {
        // This calculation will run twice if any of the dependencies change.
        return filterTodos(todos, tab);
    }, [todos, tab]);

    // ...
}
```

<!-- 0092.part.md -->

Это ожидаемо и не должно нарушать ваш код.

Это **поведение только для разработчиков** помогает вам [поддерживать чистоту компонентов](../learn/keeping-components-pure.md). React использует результат одного из вызовов и игнорирует результат другого вызова. Пока ваш компонент и функции вычисления чисты, это не должно влиять на вашу логику. Однако если они случайно оказались нечистыми, это поможет вам заметить и исправить ошибку.

Например, эта нечистая функция вычисления мутирует массив, который вы получили в качестве пропса:

<!-- 0093.part.md -->

```js
const visibleTodos = useMemo(() => {
    // 🚩 Mistake: mutating a prop
    todos.push({ id: 'last', text: 'Go for a walk!' });
    const filtered = filterTodos(todos, tab);
    return filtered;
}, [todos, tab]);
```

<!-- 0094.part.md -->

React вызывает вашу функцию дважды, поэтому вы заметите, что todo добавляется дважды. Ваш расчет не должен изменять существующие объекты, но можно изменять любые _новые_ объекты, созданные вами во время расчета. Например, если функция `filterTodos` всегда возвращает _другой_ массив, вы можете изменить _этот_ массив:

<!-- 0095.part.md -->

```js
const visibleTodos = useMemo(() => {
    const filtered = filterTodos(todos, tab);
    // ✅ Correct: mutating an object you created during the calculation
    filtered.push({ id: 'last', text: 'Go for a walk!' });
    return filtered;
}, [todos, tab]);
```

<!-- 0096.part.md -->

Прочитайте [keeping components pure](../learn/keeping-components-pure.md), чтобы узнать больше о чистоте.

Также ознакомьтесь с руководствами по [обновлению объектов](../learn/updating-objects-in-state.md) и [обновлению массивов](../learn/updating-arrays-in-state.md) без мутации.

### Мой вызов `useMemo` должен вернуть объект, но возвращает `undefined`

Этот код не работает:

<!-- 0097.part.md -->

```
  // 🔴 You can't return an object from an arrow function with () => {
  const searchOptions = useMemo(() => {
    matchMode: 'whole-word',
    text: text,
  }, [text]);
```

<!-- 0098.part.md -->

В JavaScript `() => {` начинает тело функции стрелки, поэтому скобка `{` не является частью вашего объекта. Именно поэтому она не возвращает объект и приводит к ошибкам. Вы можете исправить это, добавив скобки типа `({` и `})`:

<!-- 0099.part.md -->

```js
// This works, but is easy for someone to break again
const searchOptions = useMemo(
    () => ({
        matchMode: 'whole-word',
        text: text,
    }),
    [text]
);
```

<!-- 0100.part.md -->

Однако это все еще запутанно и слишком легко для того, чтобы кто-то мог нарушить его, убрав круглые скобки.

Чтобы избежать этой ошибки, пишите оператор `return` в явном виде:

<!-- 0101.part.md -->

```js
// ✅ This works and is explicit
const searchOptions = useMemo(() => {
    return {
        matchMode: 'whole-word',
        text: text,
    };
}, [text]);
```

### Каждый раз, когда мой компонент рендерится, вычисления в `useMemo` запускаются заново

Убедитесь, что вы указали массив зависимостей в качестве второго аргумента!

Если вы забудете массив зависимостей, `useMemo` будет каждый раз запускать расчет заново:

<!-- 0103.part.md -->

```js
function TodoList({ todos, tab }) {
    // 🔴 Recalculates every time: no dependency array
    const visibleTodos = useMemo(() =>
        filterTodos(todos, tab)
    );
    // ...
}
```

<!-- 0104.part.md -->

Это исправленная версия, передающая массив зависимостей в качестве второго аргумента:

<!-- 0105.part.md -->

```js
function TodoList({ todos, tab }) {
    // ✅ Does not recalculate unnecessarily
    const visibleTodos = useMemo(
        () => filterTodos(todos, tab),
        [todos, tab]
    );
    // ...
}
```

<!-- 0106.part.md -->

Если это не помогло, то проблема в том, что по крайней мере одна из ваших зависимостей отличается от предыдущего рендера. Вы можете отладить эту проблему, вручную записав логи зависимостей в консоль:

<!-- 0107.part.md -->

```js
const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
);
console.log([todos, tab]);
```

<!-- 0108.part.md -->

Затем вы можете щелкнуть правой кнопкой мыши на массивах из разных рендеров в консоли и выбрать "Store as a global variable" для обоих. Предположив, что первый массив был сохранен как `temp1`, а второй - как `temp2`, вы можете использовать консоль браузера, чтобы проверить, является ли каждая зависимость в обоих массивах одинаковой:

<!-- 0109.part.md -->

```js
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?
Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?
Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

<!-- 0110.part.md -->

Когда вы обнаружите, какая зависимость нарушает мемоизацию, либо найдите способ удалить ее, либо мемоизируйте и ее.

---

### Мне нужно вызвать `useMemo` для каждого элемента списка в цикле, но это не разрешено

Предположим, что компонент `Chart` обернут в [`memo`](memo.md). Вы хотите пропустить повторное отображение каждого `Chart` в списке при повторном отображении компонента `ReportList`. Однако вы не можете вызвать `useMemo` в цикле:

<!-- 0111.part.md -->

```js
function ReportList({ items }) {
    return (
        <article>
            {items.map((item) => {
                // 🔴 You can't call useMemo in a loop like this:
                const data = useMemo(
                    () => calculateReport(item),
                    [item]
                );
                return (
                    <figure key={item.id}>
                        <Chart data={data} />
                    </figure>
                );
            })}
        </article>
    );
}
```

<!-- 0112.part.md -->

Вместо этого извлеките компонент для каждого элемента и мемоизируйте данные для отдельных элементов:

<!-- 0113.part.md -->

```js
function ReportList({ items }) {
    return (
        <article>
            {items.map((item) => (
                <Report key={item.id} item={item} />
            ))}
        </article>
    );
}

function Report({ item }) {
    // ✅ Call useMemo at the top level:
    const data = useMemo(() => calculateReport(item), [
        item,
    ]);
    return (
        <figure>
            <Chart data={data} />
        </figure>
    );
}
```

<!-- 0114.part.md -->

В качестве альтернативы можно убрать `useMemo` и вместо этого обернуть сам `Report` в [`memo`](memo.md). Если параметр `item` не меняется, `Report` пропускает повторное отображение, поэтому `Chart` тоже пропускает повторное отображение:

<!-- 0115.part.md -->

```js
function ReportList({ items }) {
    // ...
}

const Report = memo(function Report({ item }) {
    const data = calculateReport(item);
    return (
        <figure>
            <Chart data={data} />
        </figure>
    );
});
```

## Ссылки

-   [https://react.dev/reference/react/useMemo](https://react.dev/reference/react/useMemo)
