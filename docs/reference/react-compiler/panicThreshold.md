---
description: Параметр panicThreshold управляет тем, как React Compiler обрабатывает ошибки во время компиляции
---

# panicThreshold

<big>

Параметр `panicThreshold` управляет тем, как React Compiler обрабатывает ошибки во время компиляции.

</big>

```js
{
  panicThreshold: 'none' // Recommended
}
```

## Описание {#reference}

### `panicThreshold` {#panicthreshold}

Определяет, должны ли ошибки компиляции прерывать сборку или пропускать оптимизацию.

#### Тип {#type}

```
'none' | 'critical_errors' | 'all_errors'
```

#### Значение по умолчанию {#default-value}

`'none'`

#### Варианты {#options}

- **`'none'`** (по умолчанию, рекомендуется): пропускать компоненты, которые нельзя скомпилировать, и продолжать сборку
- **`'critical_errors'`**: прерывать сборку только при критических ошибках компилятора
- **`'all_errors'`**: прерывать сборку при любой диагностике компилятора

#### Предупреждения {#caveats}

- В продакшен-сборках всегда следует использовать `'none'`
- Сбой сборки не даёт собрать приложение
- При `'none'` компилятор автоматически обнаруживает проблемный код и пропускает его
- Более строгие пороги полезны только во время разработки для отладки

## Использование {#usage}

### Конфигурация для продакшена (рекомендуется) {#production-configuration}

Для продакшен-сборок всегда используйте `'none'`. Это значение по умолчанию:

```js
{
  panicThreshold: 'none'
}
```

Это гарантирует:

- Сборка никогда не падает из-за проблем компилятора
- Компоненты, которые нельзя оптимизировать, работают как обычно
- Оптимизируется максимум компонентов
- Стабильные продакшен-развёртывания

### Отладка во время разработки {#development-debugging}

Временно используйте более строгие пороги, чтобы найти проблемы:

```js
const isDevelopment = process.env.NODE_ENV === 'development';

{
  panicThreshold: isDevelopment ? 'critical_errors' : 'none',
  logger: {
    logEvent(filename, event) {
      if (isDevelopment && event.kind === 'CompileError') {
        // ...
      }
    }
  }
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/panicThreshold](https://react.dev/reference/react-compiler/panicThreshold)</small>
