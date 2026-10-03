---
description: Параметр target указывает, для какой версии React компилятор должен генерировать код
---

# target

<big>

Параметр `target` указывает, для какой версии React компилятор должен генерировать код.

</big>

```js
{
  target: '19' // or '18', '17'
}
```

## Описание {#reference}

### `target` {#target}

Задаёт совместимость скомпилированного результата с версией React.

#### Тип {#type}

```
'17' | '18' | '19'
```

#### Значение по умолчанию {#default-value}

`'19'`

#### Допустимые значения {#valid-values}

- **`'19'`**: целевая версия React 19 (по умолчанию). Дополнительный runtime не нужен.
- **`'18'`**: целевая версия React 18. Нужен пакет `react-compiler-runtime`.
- **`'17'`**: целевая версия React 17. Нужен пакет `react-compiler-runtime`.

#### Предупреждения {#caveats}

- Всегда используйте строки, а не числа (например, `'17'`, а не `17`)
- Не указывайте версии патча (например, `'18'`, а не `'18.2.0'`)
- В React 19 есть встроенные API runtime компилятора
- Для React 17 и 18 нужно установить `react-compiler-runtime@latest`

## Использование {#usage}

### Целевая версия React 19 (по умолчанию) {#targeting-react-19}

Для React 19 особая конфигурация не нужна:

```js
{
  // defaults to target: '19'
}
```

Компилятор будет использовать встроенные API runtime React 19:

```js
// Compiled output uses React 19's native APIs
import { c as _c } from 'react/compiler-runtime';
```

### Целевые версии React 17 и 18 {#targeting-react-17-or-18}

Для проектов на React 17 и React 18 нужны два шага:

1. Установите пакет runtime:

```sh
npm install react-compiler-runtime@latest
```

2. Настройте `target`:

```js
// For React 18
{
  target: '18'
}

// For React 17
{
  target: '17'
}
```

Компилятор будет использовать полифил runtime для обеих версий:

```js
// Compiled output uses the polyfill
import { c as _c } from 'react-compiler-runtime';
```

## Устранение неполадок {#troubleshooting}

### Ошибки времени выполнения из-за отсутствующего runtime компилятора {#missing-runtime}

Если вы видите ошибки вроде "Cannot find module 'react/compiler-runtime'":

1. Проверьте версию React:
```sh
   npm why react
   ```

2. Если вы используете React 17 или 18, установите runtime:
```sh
   npm install react-compiler-runtime@latest
   ```

3. Убедитесь, что `target` совпадает с вашей версией React:
```js
   {
     target: '18' // Must match your React major version
   }
   ```

### Пакет runtime не работает {#runtime-not-working}

Убедитесь, что пакет runtime:

1. Установлен в проекте (не глобально)
2. Указан в зависимостях `package.json`
3. Имеет правильную версию (тег `@latest`)
4. Не находится в `devDependencies` (он нужен во время выполнения)

### Проверка скомпилированного результата {#checking-output}

Чтобы убедиться, что используется правильный runtime, обратите внимание на разный импорт (`react/compiler-runtime` для встроенного, отдельный пакет `react-compiler-runtime` для 17/18):

```js
// For React 19 (built-in runtime)
import { c } from 'react/compiler-runtime'
//                      ^

// For React 17/18 (polyfill runtime)
import { c } from 'react-compiler-runtime'
//                      ^
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-compiler/target](https://react.dev/reference/react-compiler/target)</small>
