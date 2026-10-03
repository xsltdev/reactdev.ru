---
description: Проверяет, что компилятор сохраняет существующую ручную мемоизацию. Компилятор React компилирует компоненты и хуки, только если его вывод совпадает с существующей ручной мемоизацией или превосходит её
---

# preserve-manual-memoization

<big>

Проверяет, что компилятор сохраняет существующую ручную мемоизацию. Компилятор React компилирует компоненты и хуки, только если его вывод [совпадает с существующей ручной мемоизацией или превосходит её](../../../learn/react-compiler/introduction.md#what-should-i-do-about-usememo-usecallback-and-reactmemo).

</big>

## Подробности правила {#rule-details}

Компилятор React сохраняет ваши вызовы `useMemo`, `useCallback` и `React.memo`. Если вы мемоизировали что-то вручную, компилятор считает, что на это была причина, и не уберёт эту мемоизацию. Но неполный список зависимостей не даёт компилятору понять поток данных в коде и применить дальнейшие оптимизации.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Missing dependencies in useMemo
function Component({ data, filter }) {
  const filtered = useMemo(
    () => data.filter(filter),
    [data] // Missing 'filter' dependency
  );

  return <List items={filtered} />;
}

// ❌ Missing dependencies in useCallback
function Component({ onUpdate, value }) {
  const handleClick = useCallback(() => {
    onUpdate(value);
  }, [onUpdate]); // Missing 'value'

  return <button onClick={handleClick}>Update</button>;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Complete dependencies
function Component({ data, filter }) {
  const filtered = useMemo(
    () => data.filter(filter),
    [data, filter] // All dependencies included
  );

  return <List items={filtered} />;
}

// ✅ Or let the compiler handle it
function Component({ data, filter }) {
  // No manual memoization needed
  const filtered = data.filter(filter);
  return <List items={filtered} />;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно ли убирать ручную мемоизацию? {#remove-manual-memoization}

Может возникнуть вопрос, делает ли компилятор React ручную мемоизацию ненужной:

```js
// Do I still need this?
function Component({items, sortBy}) {
  const sorted = useMemo(() => {
    return [...items].sort((a, b) => {
      return a[sortBy] - b[sortBy];
    });
  }, [items, sortBy]);

  return <List items={sorted} />;
}
```

Если вы используете компилятор React, её можно спокойно убрать:

```js
// ✅ Better: Let the compiler optimize
function Component({items, sortBy}) {
  const sorted = [...items].sort((a, b) => {
    return a[sortBy] - b[sortBy];
  });

  return <List items={sorted} />;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization](https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization)</small>
