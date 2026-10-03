---
description: На этой странице перечислены все параметры конфигурации React Compiler
---

# Конфигурация

<big>

На этой странице перечислены все параметры конфигурации React Compiler.

</big>

!!!note "Примечание"

    Для большинства приложений параметры по умолчанию работают без дополнительной настройки. Если нужны особые возможности, можно использовать эти расширенные параметры.

```js
// babel.config.js
module.exports = {
  plugins: [
    [
      'babel-plugin-react-compiler', {
        // compiler options
      }
    ]
  ]
};
```

## Управление компиляцией {#compilation-control}

Эти параметры управляют тем, *что* оптимизирует компилятор и *как* он выбирает компоненты и хуки для компиляции.

* [`compilationMode`](compilationMode.md) задаёт стратегию выбора функций для компиляции (например, все функции, только аннотированные или интеллектуальное обнаружение).

```js
{
  compilationMode: 'annotation' // Only compile "use memo" functions
}
```

## Совместимость версий {#version-compatibility}

Конфигурация версии React гарантирует, что компилятор генерирует код, совместимый с вашей версией React.

[`target`](target.md) указывает, какую версию React вы используете (17, 18 или 19).

```js
// For React 18 projects
{
  target: '18' // Also requires react-compiler-runtime package
}
```

## Обработка ошибок {#error-handling}

Эти параметры управляют тем, как компилятор реагирует на код, который не следует [Правилам React](../rules/index.md).

[`panicThreshold`](panicThreshold.md) определяет, прерывать ли сборку или пропускать проблемные компоненты.

```js
// Recommended for production
{
  panicThreshold: 'none' // Skip components with errors instead of failing the build
}
```

## Отладка {#debugging}

Параметры логирования и анализа помогают понять, что делает компилятор.

[`logger`](logger.md) задаёт пользовательское логирование событий компиляции.

```js
{
  logger: {
    logEvent(filename, event) {
      if (event.kind === 'CompileSuccess') {
        console.log('Compiled:', filename);
      }
    }
  }
}
```

## Функциональные флаги {#feature-flags}

Условная компиляция позволяет управлять тем, когда используется оптимизированный код.

[`gating`](gating.md) включает функциональные флаги времени выполнения для A/B-тестирования или постепенного внедрения.

```js
{
  gating: {
    source: 'my-feature-flags',
    importSpecifierName: 'isCompilerEnabled'
  }
}
```

## Типичные шаблоны конфигурации {#common-patterns}

### Конфигурация по умолчанию {#default-configuration}

Для большинства приложений на React 19 компилятор работает без конфигурации:

```js
// babel.config.js
module.exports = {
  plugins: [
    'babel-plugin-react-compiler'
  ]
};
```

### Проекты на React 17/18 {#react-17-18}

Более старым версиям React нужны пакет runtime и конфигурация `target`:

```sh
npm install react-compiler-runtime@latest
```

```js
{
  target: '18' // or '17'
}
```

### Постепенное внедрение {#incremental-adoption}

Начните с отдельных каталогов и постепенно расширяйте охват:

```js
{
  compilationMode: 'annotation' // Only compile "use memo" functions
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/configuration](https://react.dev/reference/react-compiler/configuration)</small>
