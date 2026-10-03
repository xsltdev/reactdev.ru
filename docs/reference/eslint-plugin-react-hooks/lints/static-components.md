---
description: Проверяет, что компоненты статичны и не создаются заново при каждом рендере. Компоненты, которые создаются динамически, могут сбрасывать состояние и вызывать лишние повторные рендеры
---

# static-components

<big>

Проверяет, что компоненты статичны и не создаются заново при каждом рендере. Компоненты, которые создаются динамически, могут сбрасывать состояние и вызывать лишние повторные рендеры.

</big>

## Подробности правила {#rule-details}

Компоненты, объявленные внутри других компонентов, создаются заново на каждом рендере. React видит каждый из них как совершенно новый тип компонента: размонтирует старый, монтирует новый и при этом уничтожает всё состояние и узлы DOM.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Component defined inside component
function Parent() {
  const ChildComponent = () => { // New component every render!
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
  };

  return <ChildComponent />; // State resets every render
}

// ❌ Dynamic component creation
function Parent({type}) {
  const Component = type === 'button'
    ? () => <button>Click</button>
    : () => <div>Text</div>;

  return <Component />;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Components at module level
const ButtonComponent = () => <button>Click</button>;
const TextComponent = () => <div>Text</div>;

function Parent({type}) {
  const Component = type === 'button'
    ? ButtonComponent  // Reference existing component
    : TextComponent;

  return <Component />;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно условно рендерить разные компоненты {#conditional-components}

Компоненты иногда объявляют внутри, чтобы получить доступ к локальному состоянию:

```js hl_lines="13"
// ❌ Wrong: Inner component to access parent state
function Parent() {
  const [theme, setTheme] = useState('light');

  function ThemedButton() { // Recreated every render!
    return (
      <button className={theme}>
        Click me
      </button>
    );
  }

  return <ThemedButton />;
}
```

Вместо этого передавайте данные пропсами:

```js
// ✅ Better: Pass props to static component
function ThemedButton({theme}) {
  return (
    <button className={theme}>
      Click me
    </button>
  );
}

function Parent() {
  const [theme, setTheme] = useState('light');
  return <ThemedButton theme={theme} />;
}
```

!!!note "Примечание"

    Если хочется объявлять компоненты внутри других компонентов, чтобы достать локальные переменные, это знак, что вместо этого нужно передавать пропсы. Так компоненты проще переиспользовать и тестировать.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components](https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components)</small>
