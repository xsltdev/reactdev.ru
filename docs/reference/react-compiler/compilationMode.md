---
description: Параметр compilationMode управляет тем, как React Compiler выбирает функции для компиляции
---

# compilationMode

<big>

Параметр `compilationMode` управляет тем, как React Compiler выбирает функции для компиляции.

</big>

```js
{
  compilationMode: 'infer' // or 'annotation', 'syntax', 'all'
}
```

## Описание {#reference}

### `compilationMode` {#compilationmode}

Управляет стратегией, по которой React Compiler определяет, какие функции оптимизировать.

#### Тип {#type}

```
'infer' | 'syntax' | 'annotation' | 'all'
```

#### Значение по умолчанию {#default-value}

`'infer'`

#### Варианты {#options}

- **`'infer'`** (по умолчанию): Компилятор использует интеллектуальные эвристики, чтобы определить компоненты и хуки React:
  - Функции, явно помеченные директивой `"use memo"`
  - Функции, названные как компоненты (PascalCase) или хуки (префикс `use`), которые при этом создают JSX и/или вызывают другие хуки

- **`'annotation'`**: Компилируются только функции, явно помеченные директивой `"use memo"`. Подходит для постепенного внедрения.

- **`'syntax'`**: Компилируются только компоненты и хуки, которые используют синтаксис Flow [component](https://flow.org/en/docs/react/component-syntax/) и [hook](https://flow.org/en/docs/react/hook-syntax/).

- **`'all'`**: Компилируются все функции верхнего уровня. Не рекомендуется, потому что могут быть скомпилированы функции, не относящиеся к React.

#### Предупреждения {#caveats}

- Режим `'infer'` требует, чтобы функции следовали соглашениям об именовании React, иначе они не будут обнаружены
- Режим `'all'` может ухудшить производительность, компилируя служебные функции
- Режим `'syntax'` требует Flow и не работает с TypeScript
- Независимо от режима, функции с директивой `"use no memo"` всегда пропускаются

## Использование {#usage}

### Режим вывода по умолчанию {#default-inference-mode}

Режим `'infer'` по умолчанию хорошо подходит для большинства кодовых баз, которые следуют соглашениям React:

```js
{
  compilationMode: 'infer'
}
```

В этом режиме будут скомпилированы такие функции:

```js
// ✅ Compiled: Named like a component + returns JSX
function Button(props) {
  return <button>{props.label}</button>;
}

// ✅ Compiled: Named like a hook + calls hooks
function useCounter() {
  const [count, setCount] = useState(0);
  return [count, setCount];
}

// ✅ Compiled: Explicit directive
function expensiveCalculation(data) {
  "use memo";
  return data.reduce(/* ... */);
}

// ❌ Not compiled: Not a component/hook pattern
function calculateTotal(items) {
  return items.reduce((a, b) => a + b, 0);
}
```

### Постепенное внедрение в режиме annotation {#incremental-adoption}

Для постепенной миграции используйте режим `'annotation'`, чтобы компилировать только помеченные функции:

```js
{
  compilationMode: 'annotation'
}
```

Затем явно пометьте функции, которые нужно скомпилировать:

```js
// Only this function will be compiled
function ExpensiveList(props) {
  "use memo";
  return (
    <ul>
      {props.items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

// This won't be compiled without the directive
function NormalComponent(props) {
  return <div>{props.content}</div>;
}
```

### Использование режима синтаксиса Flow {#flow-syntax-mode}

Если кодовая база использует Flow вместо TypeScript:

```js
{
  compilationMode: 'syntax'
}
```

Затем используйте синтаксис компонентов Flow:

```js
// Compiled: Flow component syntax
component Button(label: string) {
  return <button>{label}</button>;
}

// Compiled: Flow hook syntax
hook useCounter(initial: number) {
  const [count, setCount] = useState(initial);
  return [count, setCount];
}

// Not compiled: Regular function syntax
function helper(data) {
  return process(data);
}
```

### Исключение отдельных функций {#opting-out}

Независимо от режима компиляции, используйте `"use no memo"`, чтобы пропустить компиляцию:

```js
function ComponentWithSideEffects() {
  "use no memo"; // Prevent compilation

  // This component has side effects that shouldn't be memoized
  logToAnalytics('component_rendered');

  return <div>Content</div>;
}
```

## Устранение неполадок {#troubleshooting}

### Компонент не компилируется в режиме infer {#component-not-compiled-infer}

В режиме `'infer'` убедитесь, что компонент следует соглашениям React:

```js
// ❌ Won't be compiled: lowercase name
function button(props) {
  return <button>{props.label}</button>;
}

// ✅ Will be compiled: PascalCase name
function Button(props) {
  return <button>{props.label}</button>;
}

// ❌ Won't be compiled: doesn't create JSX or call hooks
function useData() {
  return window.localStorage.getItem('data');
}

// ✅ Will be compiled: calls a hook
function useData() {
  const [data] = useState(() => window.localStorage.getItem('data'));
  return data;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/compilationMode](https://react.dev/reference/react-compiler/compilationMode)</small>
