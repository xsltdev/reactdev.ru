---
description: Проверяет параметры конфигурации компилятора
---

# config

<big>

Проверяет [параметры конфигурации](../../react-compiler/configuration.md) компилятора.

</big>

## Подробности правила {#rule-details}

Компилятор React принимает разные [параметры конфигурации](../../react-compiler/configuration.md), которые управляют его поведением. Это правило проверяет, что в конфигурации верные имена параметров и типы значений, чтобы опечатки и неверные настройки не приводили к тихим сбоям.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Unknown option name
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compileMode: 'all' // Typo: should be compilationMode
    }]
  ]
};

// ❌ Invalid option value
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'everything' // Invalid: use 'all' or 'infer'
    }]
  ]
};
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Valid compiler configuration
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'infer',
      panicThreshold: 'critical_errors'
    }]
  ]
};
```

## Устранение неполадок {#troubleshooting}

### Конфигурация работает не так, как ожидалось {#config-not-working}

В конфигурации компилятора могут быть опечатки или неверные значения:

```js
// ❌ Wrong: Common configuration mistakes
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      // Typo in option name
      compilationMod: 'all',
      // Wrong value type
      panicThreshold: true,
      // Unknown option
      optimizationLevel: 'max'
    }]
  ]
};
```

Допустимые параметры смотрите в [документации по конфигурации](../../react-compiler/configuration.md):

```js
// ✅ Better: Valid configuration
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'all', // or 'infer'
      panicThreshold: 'none', // or 'critical_errors', 'all_errors'
      // Only use documented options
    }]
  ]
};
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/config](https://react.dev/reference/eslint-plugin-react-hooks/lints/config)</small>
