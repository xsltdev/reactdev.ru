---
description: Проверяет, что во время рендера нет присваивания и изменения глобальных переменных. Это часть правила, по которому побочные эффекты должны выполняться вне рендера
---

# globals

<big>

Проверяет, что во время рендера нет присваивания и изменения глобальных переменных. Это часть правила, по которому [побочные эффекты должны выполняться вне рендера](../../rules/components-and-hooks-must-be-pure.md#side-effects-must-run-outside-of-render).

</big>

## Подробности правила {#rule-details}

Глобальные переменные живут вне контроля React. Если менять их во время рендера, ломается допущение React, что рендеринг чистый. Из-за этого компоненты могут вести себя по-разному в разработке и в продакшене, ломается Fast Refresh, а приложение нельзя оптимизировать возможностями вроде компилятора React.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Global counter
let renderCount = 0;
function Component() {
  renderCount++; // Mutating global
  return <div>Count: {renderCount}</div>;
}

// ❌ Modifying window properties
function Component({userId}) {
  window.currentUser = userId; // Global mutation
  return <div>User: {userId}</div>;
}

// ❌ Global array push
const events = [];
function Component({event}) {
  events.push(event); // Mutating global array
  return <div>Events: {events.length}</div>;
}

// ❌ Cache manipulation
const cache = {};
function Component({id}) {
  if (!cache[id]) {
    cache[id] = fetchData(id); // Modifying cache during render
  }
  return <div>{cache[id]}</div>;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Use state for counters
function Component() {
  const [clickCount, setClickCount] = useState(0);

  const handleClick = () => {
    setClickCount(c => c + 1);
  };

  return (
    <button onClick={handleClick}>
      Clicked: {clickCount} times
    </button>
  );
}

// ✅ Use context for global values
function Component() {
  const user = useContext(UserContext);
  return <div>User: {user.id}</div>;
}

// ✅ Synchronize external state with React
function Component({title}) {
  useEffect(() => {
    document.title = title; // OK in effect
  }, [title]);

  return <div>Page: {title}</div>;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/globals](https://react.dev/reference/eslint-plugin-react-hooks/lints/globals)</small>
