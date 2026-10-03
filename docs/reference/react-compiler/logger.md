---
description: Параметр logger задаёт пользовательское логирование событий React Compiler во время компиляции
---

# logger

<big>

Параметр `logger` задаёт пользовательское логирование событий React Compiler во время компиляции.

</big>

```js
{
  logger: {
    logEvent(filename, event) {
      console.log(`[Compiler] ${event.kind}: ${filename}`);
    }
  }
}
```

## Описание {#reference}

### `logger` {#logger}

Настраивает пользовательское логирование, чтобы отслеживать поведение компилятора и отлаживать проблемы.

#### Тип {#type}

```
{
  logEvent: (filename: string | null, event: LoggerEvent) => void;
} | null
```

#### Значение по умолчанию {#default-value}

`null`

#### Методы {#methods}

- **`logEvent`**: вызывается для каждого события компилятора и получает имя файла и сведения о событии

#### Типы событий {#event-types}

- **`CompileSuccess`**: функция успешно скомпилирована
- **`CompileError`**: функция пропущена из-за ошибок
- **`CompileDiagnostic`**: нефатальная диагностическая информация
- **`CompileSkip`**: функция пропущена по другим причинам
- **`PipelineError`**: неожиданная ошибка компиляции
- **`Timing`**: сведения о времени выполнения

#### Предупреждения {#caveats}

- Структура событий может меняться между версиями
- Большие кодовые базы порождают много записей в журнале

## Использование {#usage}

### Базовое логирование {#basic-logging}

Отслеживайте успешную компиляцию и сбои:

```js
{
  logger: {
    logEvent(filename, event) {
      switch (event.kind) {
        case 'CompileSuccess': {
          console.log(`✅ Compiled: ${filename}`);
          break;
        }
        case 'CompileError': {
          console.log(`❌ Skipped: ${filename}`);
          break;
        }
        default: {}
      }
    }
  }
}
```

### Подробное логирование ошибок {#detailed-error-logging}

Получайте конкретные сведения о сбоях компиляции:

```js
{
  logger: {
    logEvent(filename, event) {
      if (event.kind === 'CompileError') {
        console.error(`\nCompilation failed: ${filename}`);
        console.error(`Reason: ${event.detail.reason}`);

        if (event.detail.description) {
          console.error(`Details: ${event.detail.description}`);
        }

        if (event.detail.loc) {
          const { line, column } = event.detail.loc.start;
          console.error(`Location: Line ${line}, Column ${column}`);
        }

        if (event.detail.suggestions) {
          console.error('Suggestions:', event.detail.suggestions);
        }
      }
    }
  }
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/logger](https://react.dev/reference/react-compiler/logger)</small>
