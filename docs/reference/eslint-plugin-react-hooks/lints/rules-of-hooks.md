---
description: Проверяет, что компоненты и хуки следуют Правилам хуков
---

# rules-of-hooks

<big>

Проверяет, что компоненты и хуки следуют [Правилам хуков](../../rules/rules-of-hooks.md).

</big>

## Подробности правила {#rule-details}

React опирается на порядок вызова хуков, чтобы правильно сохранять состояние между рендерами. При каждом рендере компонента React ожидает, что будут вызваны те же самые хуки и в том же самом порядке. Если хуки вызываются условно или в циклах, React теряет соответствие между состоянием и конкретным вызовом хука. Отсюда ошибки вроде несовпадения состояния и «Rendered fewer/more hooks than expected».

## Типичные нарушения {#common-violations}

Эти паттерны нарушают Правила хуков:

- **Хуки в условиях** (`if`/`else`, тернарный оператор, `&&`/`||`)
- **Хуки в циклах** (`for`, `while`, `do-while`)
- **Хуки после раннего возврата**
- **Хуки в колбэках и обработчиках событий**
- **Хуки в async-функциях**
- **Хуки в методах класса**
- **Хуки на уровне модуля**

!!!note "Хук `use`"

    Хук `use` отличается от других хуков React. Его можно вызывать условно и в циклах:

    ```js
    // ✅ `use` can be conditional
    if (shouldFetch) {
      const data = use(fetchPromise);
    }

    // ✅ `use` can be in loops
    for (const promise of promises) {
      results.push(use(promise));
    }
    ```

    При этом у `use` остаются ограничения:
    - Нельзя оборачивать в try/catch
    - Нужно вызывать внутри компонента или хука

    Подробнее: [справочник API `use`](../../react/use.md)

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Hook in condition
if (isLoggedIn) {
  const [user, setUser] = useState(null);
}

// ❌ Hook after early return
if (!data) return <Loading />;
const [processed, setProcessed] = useState(data);

// ❌ Hook in callback
<button onClick={() => {
  const [clicked, setClicked] = useState(false);
}}/>

// ❌ `use` in try/catch
try {
  const data = use(promise);
} catch (e) {
  // error handling
}

// ❌ Hook at module level
const globalState = useState(0); // Outside component
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
function Component({ isSpecial, shouldFetch, fetchPromise }) {
  // ✅ Hooks at top level
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  if (!isSpecial) {
    return null;
  }

  if (shouldFetch) {
    // ✅ `use` can be conditional
    const data = use(fetchPromise);
    return <div>{data}</div>;
  }

  return <div>{name}: {count}</div>;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно загрузить данные по условию {#conditional-data-fetching}

Вы пытаетесь вызвать useEffect условно:

```js
// ❌ Conditional hook
if (isLoggedIn) {
  useEffect(() => {
    fetchUserData();
  }, []);
}
```

Вызывайте хук безусловно, а условие проверяйте внутри:

```js
// ✅ Condition inside hook
useEffect(() => {
  if (isLoggedIn) {
    fetchUserData();
  }
}, [isLoggedIn]);
```

!!!note "Примечание"

    Загружать данные лучше не в useEffect. Для загрузки данных рассмотрите TanStack Query, useSWR или React Router 6.4+. Эти решения умеют убирать дубли запросов, кэшировать ответы и избегать каскада сетевых запросов.

    Подробнее: [Получение данных](../../../learn/synchronizing-with-effects.md#fetching-data)

### Нужно разное состояние для разных сценариев {#conditional-state-initialization}

Вы пытаетесь инициализировать состояние условно:

```js
// ❌ Conditional state
if (userType === 'admin') {
  const [permissions, setPermissions] = useState(adminPerms);
} else {
  const [permissions, setPermissions] = useState(userPerms);
}
```

Всегда вызывайте useState, а начальное значение задавайте условно:

```js
// ✅ Conditional initial value
const [permissions, setPermissions] = useState(
  userType === 'admin' ? adminPerms : userPerms
);
```

## Параметры {#options}

Пользовательские хуки-эффекты можно настроить через общие параметры ESLint (доступно в `eslint-plugin-react-hooks` 6.1.1 и новее):

```js
{
  "settings": {
    "react-hooks": {
      "additionalEffectHooks": "(useMyEffect|useCustomEffect)"
    }
  }
}
```

- `additionalEffectHooks`: регулярное выражение для пользовательских хуков, которые нужно считать эффектами. Тогда `useEffectEvent` и похожие функции событий можно вызывать из ваших пользовательских хуков-эффектов.

Эта общая настройка используется и правилом `rules-of-hooks`, и правилом `exhaustive-deps`, поэтому проверка хуков ведёт себя одинаково.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks)</small>
