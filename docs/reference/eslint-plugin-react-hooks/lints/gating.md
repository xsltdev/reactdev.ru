---
description: Проверяет конфигурацию режима gating
---

# gating

<big>

Проверяет конфигурацию [режима gating](../../react-compiler/gating.md).

</big>

## Подробности правила {#rule-details}

Режим gating позволяет постепенно внедрять компилятор React, помечая отдельные компоненты для оптимизации. Это правило проверяет, что конфигурация gating верна и компилятор знает, какие компоненты обрабатывать.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Missing required fields
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      gating: {
        importSpecifierName: '__experimental_useCompiler'
        // Missing 'source' field
      }
    }]
  ]
};

// ❌ Invalid gating type
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      gating: '__experimental_useCompiler' // Should be object
    }]
  ]
};
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Complete gating configuration
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      gating: {
        importSpecifierName: 'isCompilerEnabled', // exported function name
        source: 'featureFlags' // module name
      }
    }]
  ]
};

// featureFlags.js
export function isCompilerEnabled() {
  // ...
}

// ✅ No gating (compile everything)
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      // No gating field - compiles all components
    }]
  ]
};
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/gating](https://react.dev/reference/eslint-plugin-react-hooks/lints/gating)</small>
