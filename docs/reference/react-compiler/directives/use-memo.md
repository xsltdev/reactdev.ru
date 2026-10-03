---
description: '"use memo" помечает функцию для оптимизации React Compiler'
---

# use memo

<big>

`"use memo"` помечает функцию для оптимизации React Compiler.

</big>

!!!note "Примечание"

    В большинстве случаев `"use memo"` не нужна. Она нужна прежде всего в режиме `annotation`, где функции для оптимизации нужно помечать явно. В режиме `infer` компилятор автоматически определяет компоненты и хуки по шаблону имени (PascalCase для компонентов, префикс `use` для хуков). Если компонент или хук не компилируется в режиме `infer`, исправьте соглашение об именовании, а не принуждайте компиляцию с помощью `"use memo"`.

## Описание {#reference}

### `"use memo"` {#use-memo}

Добавьте `"use memo"` в начало функции, чтобы пометить её для оптимизации React Compiler.

```js hl_lines="1"
function MyComponent() {
  "use memo";
  // ...
}
```

Если функция содержит `"use memo"`, React Compiler проанализирует и оптимизирует её во время сборки. Компилятор автоматически мемоизирует значения и компоненты, чтобы избежать ненужных повторных вычислений и повторных рендеров.

#### Предупреждения {#caveats}

* `"use memo"` должна стоять в самом начале тела функции, до любых импортов и другого кода (комментарии допустимы).
* Директиву нужно записывать в двойных или одинарных кавычках, а не в обратных.
* Директива должна точно совпадать с `"use memo"`.
* Обрабатывается только первая директива в функции; остальные игнорируются.
* Эффект директивы зависит от параметра [`compilationMode`](../compilationMode.md).

### Как `"use memo"` помечает функции для оптимизации {#how-use-memo-marks}

В приложении React, которое использует React Compiler, функции анализируются во время сборки, чтобы определить, можно ли их оптимизировать. По умолчанию компилятор автоматически выводит, какие компоненты мемоизировать, но это может зависеть от параметра [`compilationMode`](../compilationMode.md), если вы его задали.

`"use memo"` явно помечает функцию для оптимизации и переопределяет поведение по умолчанию:

* В режиме `annotation`: оптимизируются только функции с `"use memo"`
* В режиме `infer`: компилятор использует эвристики, но `"use memo"` принудительно включает оптимизацию
* В режиме `all`: по умолчанию оптимизируется всё, поэтому `"use memo"` избыточна

Директива создаёт в кодовой базе явную границу между оптимизированным и неоптимизированным кодом и даёт точечный контроль над процессом компиляции.

### Когда использовать `"use memo"` {#when-to-use}

`"use memo"` стоит рассмотреть в таких случаях:

#### Вы используете режим annotation {#annotation-mode-use}
В `compilationMode: 'annotation'` директива обязательна для любой функции, которую вы хотите оптимизировать:

```js
// ✅ This component will be optimized
function OptimizedList() {
  "use memo";
  // ...
}

// ❌ This component won't be optimized
function SimpleWrapper() {
  // ...
}
```

#### Вы постепенно внедряете React Compiler {#gradual-adoption}
Начните с режима `annotation` и выборочно оптимизируйте стабильные компоненты:

```js
// Start by optimizing leaf components
function Button({ onClick, children }) {
  "use memo";
  // ...
}

// Gradually move up the tree as you verify behavior
function ButtonGroup({ buttons }) {
  "use memo";
  // ...
}
```

## Использование {#usage}

### Работа с разными режимами компиляции {#compilation-modes}

Поведение `"use memo"` зависит от конфигурации компилятора:

```js
// babel.config.js
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'annotation' // or 'infer' or 'all'
    }]
  ]
};
```

#### Режим annotation {#annotation-mode-example}
```js
// ✅ Optimized with "use memo"
function ProductCard({ product }) {
  "use memo";
  // ...
}

// ❌ Not optimized (no directive)
function ProductList({ products }) {
  // ...
}
```

#### Режим infer (по умолчанию) {#infer-mode-example}
```js
// Automatically memoized because this is named like a Component
function ComplexDashboard({ data }) {
  // ...
}

// Skipped: Is not named like a Component
function simpleDisplay({ text }) {
  // ...
}
```

В режиме `infer` компилятор автоматически определяет компоненты и хуки по шаблону имени (PascalCase для компонентов, префикс `use` для хуков). Если компонент или хук не компилируется в режиме `infer`, исправьте соглашение об именовании, а не принуждайте компиляцию с помощью `"use memo"`.

## Устранение неполадок {#troubleshooting}

### Проверка оптимизации {#verifying-optimization}

Чтобы убедиться, что компонент оптимизируется:

1. Проверьте скомпилированный результат в сборке
2. В React DevTools найдите значок Memo ✨

### См. также {#see-also}

* [`"use no memo"`](use-no-memo.md) - исключение из компиляции
* [`compilationMode`](../compilationMode.md) - настройка поведения компиляции
* [React Compiler](../../../learn/react-compiler/index.md) - руководство по началу работы

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/directives/use-memo](https://react.dev/reference/react-compiler/directives/use-memo)</small>
