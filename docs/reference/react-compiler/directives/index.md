---
description: Директивы React Compiler - это специальные строковые литералы, которые управляют тем, компилируются ли отдельные функции
---

# Директивы

<big>

Директивы React Compiler - это специальные строковые литералы, которые управляют тем, компилируются ли отдельные функции.

</big>

```js
function MyComponent() {
  "use memo"; // Opt this component into compilation
  return <div>{/* ... */}</div>;
}
```

## Обзор {#overview}

Директивы React Compiler дают точечный контроль над тем, какие функции оптимизирует компилятор. Это строковые литералы, которые ставятся в начало тела функции или в начало модуля.

### Доступные директивы {#available-directives}

* **[`"use memo"`](use-memo.md)** - включает функцию в компиляцию
* **[`"use no memo"`](use-no-memo.md)** - исключает функцию из компиляции

### Краткое сравнение {#quick-comparison}

| Директива | Назначение | Когда использовать |
|-----------|---------|-------------|
| [`"use memo"`](use-memo.md) | Принудительная компиляция | В режиме `annotation` или чтобы переопределить эвристики режима `infer` |
| [`"use no memo"`](use-no-memo.md) | Запрет компиляции | Отладка проблем или работа с несовместимым кодом |

## Использование {#usage}

### Директивы на уровне функции {#function-level}

Поставьте директиву в начало функции, чтобы управлять её компиляцией:

```js
// Opt into compilation
function OptimizedComponent() {
  "use memo";
  return <div>This will be optimized</div>;
}

// Opt out of compilation
function UnoptimizedComponent() {
  "use no memo";
  return <div>This won't be optimized</div>;
}
```

### Директивы на уровне модуля {#module-level}

Поставьте директиву в начало файла, чтобы она действовала на все функции модуля:

```js
// At the very top of the file
"use memo";

// All functions in this file will be compiled
function Component1() {
  return <div>Compiled</div>;
}

function Component2() {
  return <div>Also compiled</div>;
}

// Can be overridden at function level
function Component3() {
  "use no memo"; // This overrides the module directive
  return <div>Not compiled</div>;
}
```

### Взаимодействие с режимами компиляции {#compilation-modes}

Директивы ведут себя по-разному в зависимости от [`compilationMode`](../compilationMode.md):

* **Режим `annotation`**: компилируются только функции с `"use memo"`
* **Режим `infer`**: компилятор сам решает, что компилировать, а директивы переопределяют его решения
* **Режим `all`**: компилируется всё, а `"use no memo"` может исключить отдельные функции

## Рекомендации {#best-practices}

### Используйте директивы умеренно {#use-sparingly}

Директивы - это лазейки. Предпочитайте настраивать компилятор на уровне проекта:

```js
// ✅ Good - project-wide configuration
{
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'infer'
    }]
  ]
}

// ⚠️ Use directives only when needed
function SpecialCase() {
  "use no memo"; // Document why this is needed
  // ...
}
```

### Документируйте использование директив {#document-usage}

Всегда объясняйте, зачем используется директива:

```js
// ✅ Good - clear explanation
function DataGrid() {
  "use no memo"; // TODO: Remove after fixing issue with dynamic row heights (JIRA-123)
  // Complex grid implementation
}

// ❌ Bad - no explanation
function Mystery() {
  "use no memo";
  // ...
}
```

### Планируйте удаление {#plan-removal}

Директивы исключения должны быть временными:

1. Добавьте директиву с комментарием TODO
2. Создайте задачу для отслеживания
3. Исправьте исходную проблему
4. Удалите директиву

```js
function TemporaryWorkaround() {
  "use no memo"; // TODO: Remove after upgrading ThirdPartyLib to v2.0
  return <ThirdPartyComponent />;
}
```

## Распространённые шаблоны {#common-patterns}

### Постепенное внедрение {#gradual-adoption}

При внедрении React Compiler в большую кодовую базу:

```js
// Start with annotation mode
{
  compilationMode: 'annotation'
}

// Opt in stable components
function StableComponent() {
  "use memo";
  // Well-tested component
}

// Later, switch to infer mode and opt out problematic ones
function ProblematicComponent() {
  "use no memo"; // Fix issues before removing
  // ...
}
```

## Устранение неполадок {#troubleshooting}

По конкретным проблемам с директивами смотрите разделы устранения неполадок:

* [Устранение неполадок `"use memo"`](use-memo.md#troubleshooting)
* [Устранение неполадок `"use no memo"`](use-no-memo.md#troubleshooting)

### Типичные проблемы {#common-issues}

1. **Директива игнорируется**: проверьте расположение (должна быть первой) и написание
2. **Компиляция всё равно происходит**: проверьте параметр `ignoreUseNoForget`
3. **Директива модуля не работает**: убедитесь, что она стоит перед всеми импортами

## См. также {#see-also}

* [`compilationMode`](../compilationMode.md) - как компилятор выбирает, что оптимизировать
* [`Конфигурация`](../configuration.md) - все параметры конфигурации компилятора
* [Документация React Compiler](../../../learn/react-compiler/index.md) - руководство по началу работы

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/directives](https://react.dev/reference/react-compiler/directives)</small>
