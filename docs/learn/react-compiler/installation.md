---
description: Это руководство поможет установить и настроить React Compiler в приложении React
---

# Установка

<big>

Это руководство поможет установить и настроить React Compiler в приложении React.

</big>

!!!tip "Вы узнаете"

    * Как установить React Compiler
    * Базовая конфигурация для разных инструментов сборки
    * Как проверить, что настройка работает

## Требования {#prerequisites}

React Compiler лучше всего работает с React 19, но также поддерживает React 17 и 18. Подробнее о [совместимости версий React](../../reference/react-compiler/target.md).

## Установка {#installation}

Установите React Compiler как `devDependency`:

```sh linenums="0"
npm install -D babel-plugin-react-compiler@latest
```

Или с помощью Yarn:

```sh linenums="0"
yarn add -D babel-plugin-react-compiler@latest
```

Или с помощью pnpm:

```sh linenums="0"
pnpm install -D babel-plugin-react-compiler@latest
```

## Базовая настройка {#basic-setup}

React Compiler по умолчанию рассчитан на работу без какой-либо конфигурации. Если настроить его всё же нужно в особых случаях (например, чтобы ориентироваться на версии React ниже 19), смотрите [справочник параметров компилятора](../../reference/react-compiler/configuration.md).

Процесс настройки зависит от инструмента сборки. В React Compiler есть плагин Babel, который встраивается в конвейер сборки.

!!!warning "Ловушка"

    React Compiler должен выполняться **первым** в конвейере плагинов Babel. Компилятору нужна исходная информация о коде для правильного анализа, поэтому он должен обработать код раньше других преобразований.

### Babel {#babel}

Создайте или обновите `babel.config.js`:

```js hl_lines="3"
module.exports = {
  plugins: [
    'babel-plugin-react-compiler', // must run first!
    // ... other plugins
  ],
  // ... other config
};
```

### Vite {#vite}

Если вы используете Vite с версией 6.0.0 или новее пакета `@vitejs/plugin-react`, можно использовать `reactCompilerPreset`:

```sh linenums="0"
npm install -D @rolldown/plugin-babel
```

```js hl_lines="3-4 9-11"
// vite.config.js
import { defineConfig } from 'vite';
import react, { reactCompilerPreset } from '@vitejs/plugin-react';
import babel from '@rolldown/plugin-babel';

export default defineConfig({
  plugins: [
    react(),
    babel({
      presets: [reactCompilerPreset()]
    }),
  ],
});
```

!!!note "Примечание"

    В `@vitejs/plugin-react@6.0.0` встроенный параметр Babel убрали. Если вы используете более старую версию, можно сделать так:

    ```js
    // vite.config.js
    import { defineConfig } from 'vite';
    import react from '@vitejs/plugin-react';

    export default defineConfig({
      plugins: [
        react({
          babel: {
            plugins: ['babel-plugin-react-compiler'],
          },
        }),
      ],
    });
    ```

Другой вариант: использовать плагин Babel напрямую вместе с `@rolldown/plugin-babel`:

```js hl_lines="3 9"
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import babel from '@rolldown/plugin-babel';

export default defineConfig({
  plugins: [
    react(),
    babel({
      plugins: ['babel-plugin-react-compiler'],
    }),
  ],
});
```

### Next.js {#usage-with-nextjs}

Подробности смотрите в [документации Next.js](https://nextjs.org/docs/app/api-reference/next-config-js/reactCompiler).

### React Router {#usage-with-react-router}
Установите `vite-plugin-babel` и добавьте в него плагин Babel компилятора:

```sh linenums="0"
npm install vite-plugin-babel
```

```js hl_lines="3-4 16"
// vite.config.js
import { defineConfig } from "vite";
import babel from "vite-plugin-babel";
import { reactRouter } from "@react-router/dev/vite";

const ReactCompilerConfig = { /* ... */ };

export default defineConfig({
  plugins: [
    reactRouter(),
    babel({
      filter: /\.[jt]sx?$/,
      babelConfig: {
        presets: ["@babel/preset-typescript"], // if you use TypeScript
        plugins: [
          ["babel-plugin-react-compiler", ReactCompilerConfig],
        ],
      },
    }),
  ],
});
```

### Webpack {#usage-with-webpack}

Загрузчик webpack от сообщества [теперь доступен здесь](https://github.com/SukkaW/react-compiler-webpack).

### Expo {#usage-with-expo}

Чтобы включить и использовать React Compiler в приложениях Expo, смотрите [документацию Expo](https://docs.expo.dev/guides/react-compiler/).

### Metro (React Native) {#usage-with-react-native-metro}

React Native использует Babel через Metro, поэтому инструкции по установке смотрите в разделе [Использование с Babel](#babel).

### Rspack {#usage-with-rspack}

Чтобы включить и использовать React Compiler в приложениях Rspack, смотрите [документацию Rspack](https://rspack.dev/guide/tech/react#react-compiler).

### Rsbuild {#usage-with-rsbuild}

Чтобы включить и использовать React Compiler в приложениях Rsbuild, смотрите [документацию Rsbuild](https://rsbuild.dev/guide/framework/react#react-compiler).

## Интеграция с ESLint {#eslint-integration}

В React Compiler есть правило ESLint, которое помогает находить код, который нельзя оптимизировать. Если правило ESLint сообщает об ошибке, это значит, что компилятор пропустит оптимизацию этого конкретного компонента или хука. Это безопасно: компилятор продолжит оптимизировать остальные части кодовой базы. Не обязательно исправлять все нарушения сразу. Разбирайтесь с ними в своём темпе, чтобы постепенно увеличивать число оптимизированных компонентов.

Установите плагин ESLint:

```sh linenums="0"
npm install -D eslint-plugin-react-hooks@latest
```

Если вы ещё не настроили eslint-plugin-react-hooks, следуйте [инструкциям по установке в readme](https://github.com/react/react/blob/main/packages/eslint-plugin-react-hooks/README.md#installation). Правила компилятора доступны в пресете `recommended-latest`.

Правило ESLint будет:
- Находить нарушения [Правил React](../../reference/rules/index.md)
- Показывать, какие компоненты нельзя оптимизировать
- Давать полезные сообщения об ошибках, чтобы исправить проблемы

## Проверьте настройку {#verify-your-setup}

После установки проверьте, что React Compiler работает правильно.

### Проверка React DevTools {#check-react-devtools}

Компоненты, оптимизированные React Compiler, показывают значок «Memo ✨» в React DevTools:

1. Установите расширение браузера [React Developer Tools](../react-developer-tools.md)
2. Откройте приложение в режиме разработки
3. Откройте React DevTools
4. Найдите эмодзи ✨ рядом с именами компонентов

Если компилятор работает:
- У компонентов в React DevTools будет значок «Memo ✨»
- Дорогие вычисления будут мемоизироваться автоматически
- Ручной `useMemo` не нужен

### Проверка результата сборки {#check-build-output}

Убедиться, что компилятор работает, можно и по результату сборки. В скомпилированном коде появится логика автоматической мемоизации, которую компилятор добавляет сам.

```js
import { c as _c } from "react/compiler-runtime";
export default function MyApp() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <div>Hello World</div>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}

```

## Устранение неполадок {#troubleshooting}

### Исключение отдельных компонентов {#opting-out-specific-components}

Если после компиляции компонент вызывает проблемы, его можно временно исключить директивой `"use no memo"`:

```js
function ProblematicComponent() {
  "use no memo";
  // Component code here
}
```

Это говорит компилятору пропустить оптимизацию этого конкретного компонента. Нужно исправить исходную проблему и убрать директиву, когда она будет решена.

Дополнительная помощь по неполадкам — в [руководстве по отладке](debugging.md).

## Следующие шаги {#next-steps}

Теперь, когда React Compiler установлен, узнайте больше о следующем:

- [Совместимость версий React](../../reference/react-compiler/target.md) для React 17 и 18
- [Параметры конфигурации](../../reference/react-compiler/configuration.md), чтобы настроить компилятор
- [Стратегии постепенного внедрения](incremental-adoption.md) для существующих кодовых баз
- [Приёмы отладки](debugging.md), чтобы разбирать проблемы
- [Руководство по компиляции библиотек](../../reference/react-compiler/compiling-libraries.md), чтобы скомпилировать библиотеку React

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/react-compiler/installation](https://react.dev/learn/react-compiler/installation)</small>
