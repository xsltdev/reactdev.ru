---
description: Проверяет, что состояние не устанавливается во время рендера безусловно, потому что это запускает дополнительные рендеры и может привести к бесконечному циклу рендера
---

# set-state-in-render

<big>

Проверяет, что состояние не устанавливается во время рендера безусловно: это запускает дополнительные рендеры и может привести к бесконечному циклу рендера.

</big>

## Подробности правила {#rule-details}

Безусловный вызов `setState` во время рендера запускает ещё один рендер до того, как текущий завершится. Получается бесконечный цикл, и приложение падает.

## Типичные нарушения {#common-violations}

### Неверно {#invalid}

```js hl_lines="4"
// ❌ Unconditional setState directly in render
function Component({value}) {
  const [count, setCount] = useState(0);
  setCount(value); // Infinite loop!
  return <div>{count}</div>;
}
```

### Верно {#valid}

```js
// ✅ Derive during render
function Component({items}) {
  const sorted = [...items].sort(); // Just calculate it in render
  return <ul>{sorted.map(/*...*/)}</ul>;
}

// ✅ Set state in event handler
function Component() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}

// ✅ Derive from props instead of setting state
function Component({user}) {
  const name = user?.name || '';
  const email = user?.email || '';
  return <div>{name}</div>;
}

// ✅ Conditionally derive state from props and state from previous renders
function Component({ items }) {
  const [isReverse, setIsReverse] = useState(false);
  const [selection, setSelection] = useState(null);

  const [prevItems, setPrevItems] = useState(items);
  if (items !== prevItems) { // This condition makes it valid
    setPrevItems(items);
    setSelection(null);
  }
  // ...
}
```

## Устранение неполадок {#troubleshooting}

### Нужно синхронизировать состояние с пропом {#clamp-state-to-prop}

Частая проблема — попытка «поправить» состояние после рендера. Допустим, счётчик не должен превышать проп `max`:

```js
// ❌ Wrong: clamps during render
function Counter({max}) {
  const [count, setCount] = useState(0);

  if (count > max) {
    setCount(max);
  }

  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}
```

Как только `count` превысит `max`, запустится бесконечный цикл.

Чаще эту логику лучше перенести в событие — туда, где состояние устанавливается в первый раз. Например, максимум можно проверять в момент обновления состояния:

```js
// ✅ Clamp when updating
function Counter({max}) {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(current => Math.min(current + 1, max));
  };

  return <button onClick={increment}>{count}</button>;
}
```

Теперь сеттер выполняется только в ответ на клик, React нормально завершает рендер, и `count` никогда не переходит за `max`.

В редких случаях состояние нужно поправить по данным из предыдущих рендеров. Тогда следуйте [этому паттерну](https://react.dev/reference/react/useState#storing-information-from-previous-renders) условной установки состояния.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render)</small>
