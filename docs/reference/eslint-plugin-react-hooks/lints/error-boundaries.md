---
description: Проверяет, что для ошибок в дочерних компонентах используются границы ошибок, а не try/catch
---

# error-boundaries

<big>

Проверяет, что для ошибок в дочерних компонентах используются границы ошибок, а не try/catch.

</big>

## Подробности правила {#rule-details}

Блоки try/catch не ловят ошибки, которые возникают в процессе рендеринга React. Ошибки, выброшенные в методах рендера или хуках, всплывают по дереву компонентов. Поймать их могут только [границы ошибок](../../react/Component.md#catching-rendering-errors-with-an-error-boundary).

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js hl_lines="4"
// ❌ Try/catch won't catch render errors
function Parent() {
  try {
    return <ChildComponent />; // If this throws, catch won't help
  } catch (error) {
    return <div>Error occurred</div>;
  }
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Using error boundary
function Parent() {
  return (
    <ErrorBoundary>
      <ChildComponent />
    </ErrorBoundary>
  );
}
```

## Устранение неполадок {#troubleshooting}

### Почему линт запрещает оборачивать `use` в `try`/`catch`? {#why-is-the-linter-telling-me-not-to-wrap-use-in-trycatch}

Хук `use` не выбрасывает ошибки в обычном смысле: он приостанавливает выполнение компонента. Когда `use` встречает ещё не завершённый промис, он приостанавливает компонент и позволяет React показать фолбэк. Такие случаи обрабатывают только Suspense и границы ошибок. Линт предупреждает о `try`/`catch` вокруг `use`, чтобы не было путаницы: блок `catch` никогда не выполнится.

```js hl_lines="5"
// ❌ Try/catch around `use` hook
function Component({promise}) {
  try {
    const data = use(promise); // Won't catch - `use` suspends, not throws
    return <div>{data}</div>;
  } catch (error) {
    return <div>Failed to load</div>; // Unreachable
  }
}

// ✅ Error boundary catches `use` errors
function App() {
  return (
    <ErrorBoundary fallback={<div>Failed to load</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <DataComponent promise={fetchData()} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries](https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries)</small>
