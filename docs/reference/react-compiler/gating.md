---
description: Параметр gating включает условную компиляцию и позволяет управлять тем, когда оптимизированный код используется во время выполнения
---

# gating

<big>

Параметр `gating` включает условную компиляцию и позволяет управлять тем, когда оптимизированный код используется во время выполнения.

</big>

```js
{
  gating: {
    source: 'my-feature-flags',
    importSpecifierName: 'shouldUseCompiler'
  }
}
```

## Описание {#reference}

### `gating` {#gating}

Настраивает включение скомпилированных функций через функциональный флаг во время выполнения.

#### Тип {#type}

```
{
  source: string;
  importSpecifierName: string;
} | null
```

#### Значение по умолчанию {#default-value}

`null`

#### Свойства {#properties}

- **`source`**: путь к модулю, из которого импортируется функциональный флаг
- **`importSpecifierName`**: имя экспортируемой функции, которую нужно импортировать

#### Предупреждения {#caveats}

- Функция `gating` должна возвращать логическое значение
- И скомпилированная, и исходная версии увеличивают размер бандла
- Импорт добавляется в каждый файл со скомпилированными функциями

## Использование {#usage}

### Базовая настройка функционального флага {#basic-setup}

1. Создайте модуль функционального флага:

```js
// src/utils/feature-flags.js
export function shouldUseCompiler() {
  // your logic here
  return getFeatureFlag('react-compiler-enabled');
}
```

2. Настройте компилятор:

```js
{
  gating: {
    source: './src/utils/feature-flags',
    importSpecifierName: 'shouldUseCompiler'
  }
}
```

3. Компилятор генерирует код с условием:

```js
// Input
function Button(props) {
  return <button>{props.label}</button>;
}

// Output (simplified)
import { shouldUseCompiler } from './src/utils/feature-flags';

const Button = shouldUseCompiler()
  ? function Button_optimized(props) { /* compiled version */ }
  : function Button_original(props) { /* original version */ };
```

Функция `gating` вычисляется один раз при загрузке модуля, поэтому после разбора и выполнения бандла JavaScript выбор компонента остаётся неизменным до конца сессии браузера.

## Устранение неполадок {#troubleshooting}

### Функциональный флаг не работает {#flag-not-working}

Убедитесь, что модуль флага экспортирует нужную функцию:

```js
// ❌ Wrong: Default export
export default function shouldUseCompiler() {
  return true;
}

// ✅ Correct: Named export matching importSpecifierName
export function shouldUseCompiler() {
  return true;
}
```

### Ошибки импорта {#import-errors}

Убедитесь, что путь `source` указан верно:

```js
// ❌ Wrong: Relative to babel.config.js
{
  source: './src/flags',
  importSpecifierName: 'flag'
}

// ✅ Correct: Module resolution path
{
  source: '@myapp/feature-flags',
  importSpecifierName: 'flag'
}

// ✅ Also correct: Absolute path from project root
{
  source: './src/utils/flags',
  importSpecifierName: 'flag'
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/gating](https://react.dev/reference/react-compiler/gating)</small>
