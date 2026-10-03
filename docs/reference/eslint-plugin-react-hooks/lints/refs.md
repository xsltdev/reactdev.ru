---
description: Проверяет корректное использование рефов, их не читают и не записывают во время рендера. См. раздел «подводные камни» в использовании useRef()
---

# refs

<big>

Проверяет корректное использование рефов: их не читают и не записывают во время рендера. См. раздел «подводные камни» в [использовании `useRef()`](../../react/useRef.md#usage).

</big>

## Подробности правила {#rule-details}

Рефы хранят значения, которые не используются для рендеринга. В отличие от состояния, изменение рефа не вызывает повторный рендер. Чтение или запись `ref.current` во время рендера ломает ожидания React. К моменту чтения реф может быть ещё не инициализирован, а его значение — устаревшим или несогласованным.

## Как линт распознаёт рефы {#how-it-detects-refs}

Линт применяет эти правила только к значениям, которые он считает рефами. Значение считается рефом, если компилятор видит любой из следующих паттернов:

- Возвращено из `useRef()` или `React.createRef()`.

```js
  const scrollRef = useRef(null);
  ```

- Идентификатор с именем `ref` или с суффиксом `Ref`, который читает или записывает `.current`.

```js
  buttonRef.current = node;
  ```

- Передан через JSX-проп `ref` (например, ``).

```jsx
  <input ref={inputRef} />
  ```

Когда что-то помечено как реф, этот вывод следует за значением через присваивания, деструктуризацию и вызовы вспомогательных функций. Поэтому линт находит нарушения, даже если `ref.current` читают внутри другой функции, которой реф передали аргументом.

## Типичные нарушения {#common-violations}

- Чтение `ref.current` во время рендера
- Обновление `refs` во время рендера
- Использование `refs` для значений, которые должны быть состоянием

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Reading ref during render
function Component() {
  const ref = useRef(0);
  const value = ref.current; // Don't read during render
  return <div>{value}</div>;
}

// ❌ Modifying ref during render
function Component({value}) {
  const ref = useRef(null);
  ref.current = value; // Don't modify during render
  return <div />;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Read ref in effects/handlers
function Component() {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      console.log(ref.current.offsetWidth); // OK in effect
    }
  });

  return <div ref={ref} />;
}

// ✅ Use state for UI values
function Component() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}

// ✅ Lazy initialization of ref value
function Component() {
  const ref = useRef(null);

  // Initialize only once on first use
  if (ref.current === null) {
    ref.current = expensiveComputation(); // OK - lazy initialization
  }

  const handleClick = () => {
    console.log(ref.current); // Use the initialized value
  };

  return <button onClick={handleClick}>Click</button>;
}
```

## Устранение неполадок {#troubleshooting}

### Линт отметил обычный объект с `.current` {#plain-object-current}

Эвристика по имени специально считает `ref.current` и `fooRef.current` настоящими рефами. Если вы моделируете собственный объект-контейнер, выберите другое имя (например, `box`) или перенесите изменяемое значение в состояние. После переименования линт замолкает: компилятор перестаёт считать значение рефом.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/refs](https://react.dev/reference/eslint-plugin-react-hooks/lints/refs)</small>
