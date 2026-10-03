---
description: Проверяет чистоту компонентов и хуков по тому, что они не вызывают заведомо нечистые функции
---

# purity

<big>

Проверяет, что [компоненты и хуки чистые](../../rules/components-and-hooks-must-be-pure.md), по тому, что они не вызывают заведомо нечистые функции.

</big>

## Подробности правила {#rule-details}

Компоненты React должны быть чистыми функциями: при одних и тех же пропсах они всегда должны возвращать один и тот же JSX. Если во время рендера компонент вызывает функции вроде `Math.random()` или `Date.now()`, на каждом рендере получается разный результат. Это ломает допущения React и приводит к ошибкам: несовпадениям при гидратации, неверной мемоизации и непредсказуемому поведению.

## Типичные нарушения {#common-violations}

В общем случае это правило нарушает любой API, который при одних и тех же входных данных возвращает разное значение. Обычные примеры:

- `Math.random()`
- `Date.now()` / `new Date()`
- `crypto.randomUUID()`
- `performance.now()`

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Math.random() in render
function Component() {
  const id = Math.random(); // Different every render
  return <div key={id}>Content</div>;
}

// ❌ Date.now() for values
function Component() {
  const timestamp = Date.now(); // Changes every render
  return <div>Created at: {timestamp}</div>;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Stable IDs from initial state
function Component() {
  const [id] = useState(() => crypto.randomUUID());
  return <div key={id}>Content</div>;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно показать текущее время {#current-time}

Вызов `Date.now()` во время рендера делает компонент нечистым:

```js hl_lines="3"
// ❌ Wrong: Time changes every render
function Clock() {
  return <div>Current time: {Date.now()}</div>;
}
```

Вместо этого [вынесите нечистую функцию за пределы рендера](../../rules/components-and-hooks-must-be-pure.md#components-and-hooks-must-be-idempotent):

```js
function Clock() {
  const [time, setTime] = useState(() => Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(Date.now());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div>Current time: {time}</div>;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/purity](https://react.dev/reference/eslint-plugin-react-hooks/lints/purity)</small>
