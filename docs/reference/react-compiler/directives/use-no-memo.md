---
description: '"use no memo" запрещает React Compiler оптимизировать функцию'
---

# use no memo

<big>

`"use no memo"` запрещает React Compiler оптимизировать функцию.

</big>

## Описание {#reference}

### `"use no memo"` {#use-no-memo}

Добавьте `"use no memo"` в начало функции, чтобы запретить оптимизацию React Compiler.

```js hl_lines="1"
function MyComponent() {
  "use no memo";
  // ...
}
```

Если функция содержит `"use no memo"`, React Compiler полностью пропустит её при оптимизации. Это полезно как временная лазейка при отладке или при работе с кодом, который некорректно работает с компилятором.

#### Предупреждения {#caveats}

* `"use no memo"` должна стоять в самом начале тела функции, до любых импортов и другого кода (комментарии допустимы).
* Директиву нужно записывать в двойных или одинарных кавычках, а не в обратных.
* Директива должна точно совпадать с `"use no memo"` или её псевдонимом `"use no forget"`.
* Эта директива имеет приоритет над всеми режимами компиляции и другими директивами.
* Она задумана как временный инструмент отладки, а не как постоянное решение.

### Как `"use no memo"` отключает оптимизацию {#how-use-no-memo-opts-out}

React Compiler анализирует код во время сборки, чтобы применить оптимизации. `"use no memo"` создаёт явную границу и указывает компилятору полностью пропустить функцию.

Эта директива имеет приоритет над всеми остальными настройками:

* В режиме `all`: функция пропускается, несмотря на глобальную настройку
* В режиме `infer`: функция пропускается, даже если эвристики оптимизировали бы её

Компилятор обрабатывает такие функции так, как если бы React Compiler не был включён, и оставляет их в точности как написано.

### Когда использовать `"use no memo"` {#when-to-use}

`"use no memo"` следует использовать редко и временно. Типичные случаи:

#### Отладка проблем компилятора {#debugging-compiler}
Если вы подозреваете, что проблемы вызывает компилятор, временно отключите оптимизацию, чтобы изолировать причину:

```js
function ProblematicComponent({ data }) {
  "use no memo"; // TODO: Remove after fixing issue #123

  // Rules of React violations that weren't statically detected
  // ...
}
```

#### Интеграция со сторонними библиотеками {#third-party}
При интеграции с библиотеками, которые могут быть несовместимы с компилятором:

```js
function ThirdPartyWrapper() {
  "use no memo";

  useThirdPartyHook(); // Has side effects that compiler might optimize incorrectly
  // ...
}
```

## Использование {#usage}

Директива `"use no memo"` ставится в начало тела функции, чтобы React Compiler не оптимизировал эту функцию:

```js
function MyComponent() {
  "use no memo";
  // Function body
}
```

Директиву также можно поставить в начало файла, чтобы она действовала на все функции модуля:

```js
"use no memo";

// All functions in this file will be skipped by the compiler
```

`"use no memo"` на уровне функции переопределяет директиву уровня модуля.

## Устранение неполадок {#troubleshooting}

### Директива не предотвращает компиляцию {#not-preventing}

Если `"use no memo"` не срабатывает:

```js
// ❌ Wrong - directive after code
function Component() {
  const data = getData();
  "use no memo"; // Too late!
}

// ✅ Correct - directive first
function Component() {
  "use no memo";
  const data = getData();
}
```

Также проверьте:

* Написание - должно быть в точности `"use no memo"`
* Кавычки - одинарные или двойные, не обратные

### Рекомендации {#best-practices}

**Всегда документируйте, почему** вы отключаете оптимизацию:

```js
// ✅ Good - clear explanation and tracking
function DataProcessor() {
  "use no memo"; // TODO: Remove after fixing rule of react violation
  // ...
}

// ❌ Bad - no explanation
function Mystery() {
  "use no memo";
  // ...
}
```

### См. также {#see-also}

* [`"use memo"`](use-memo.md) - включение в компиляцию
* [React Compiler](../../../learn/react-compiler/index.md) - руководство по началу работы

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/directives/use-no-memo](https://react.dev/reference/react-compiler/directives/use-no-memo)</small>
