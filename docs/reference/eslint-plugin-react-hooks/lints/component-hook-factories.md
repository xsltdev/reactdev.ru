---
description: Проверяет функции высшего порядка, которые объявляют вложенные компоненты или хуки. Компоненты и хуки нужно объявлять на уровне модуля
---

# component-hook-factories

<big>

Проверяет функции высшего порядка, которые объявляют вложенные компоненты или хуки. Компоненты и хуки нужно объявлять на уровне модуля.

</big>

## Подробности правила {#rule-details}

Если объявлять компоненты или хуки внутри других функций, при каждом вызове создаётся новый экземпляр. React считает каждый из них совершенно другим компонентом, уничтожает и заново создаёт всё дерево компонентов, теряет всё состояние и получает проблемы с производительностью.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js hl_lines="14"
// ❌ Factory function creating components
function createComponent(defaultValue) {
  return function Component() {
    // ...
  };
}

// ❌ Component defined inside component
function Parent() {
  function Child() {
    // ...
  }

  return <Child />;
}

// ❌ Hook factory function
function createCustomHook(endpoint) {
  return function useData() {
    // ...
  };
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Component defined at module level
function Component({ defaultValue }) {
  // ...
}

// ✅ Custom hook at module level
function useData(endpoint) {
  // ...
}
```

## Устранение неполадок {#troubleshooting}

### Нужно динамическое поведение компонента {#dynamic-behavior}

Может показаться, что фабрика нужна, чтобы создавать настроенные компоненты:

```js
// ❌ Wrong: Factory pattern
function makeButton(color) {
  return function Button({children}) {
    return (
      <button style={{backgroundColor: color}}>
        {children}
      </button>
    );
  };
}

const RedButton = makeButton('red');
const BlueButton = makeButton('blue');
```

Вместо этого [передавайте JSX как дочерние элементы](../../../learn/passing-props-to-a-component.md#passing-jsx-as-children):

```js
// ✅ Better: Pass JSX as children
function Button({color, children}) {
  return (
    <button style={{backgroundColor: color}}>
      {children}
    </button>
  );
}

function App() {
  return (
    <>
      <Button color="red">Red</Button>
      <Button color="blue">Blue</Button>
    </>
  );
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories](https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories)</small>
