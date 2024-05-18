---
status: experimental
description: На этой странице вы узнаете о новом экспериментальном компиляторе React Compiler и о том, как его успешно использовать
---

# React Compiler

<big>
На этой странице вы узнаете о новом экспериментальном компиляторе React Compiler и о том, как его успешно использовать.
</big>

!!!warning "Внимание"

    Эта документация все еще находится в процессе разработки. Больше документации доступно в репозитории [React Compiler Working Group repo](https://github.com/reactwg/react-compiler/discussions), и будет перенесено в эту документацию, когда она станет более стабильной.

!!!tip "Вы узнаете"

    -   Начало работы с компилятором
    -   Установка компилятора и плагина eslint
    -   Устранение неполадок

!!!note "Готовность"

    **React Compiler** - это новый экспериментальный компилятор, который мы выложили в открытый доступ, чтобы получить первые отзывы от сообщества. Он все еще имеет шероховатости и пока не полностью готов к использованию.

    Для работы React Compiler требуется React 19 Beta.

React Compiler - это новый экспериментальный компилятор, который мы выложили в открытый доступ, чтобы получить ранние отзывы от сообщества. Это инструмент, который автоматически оптимизирует ваше React-приложение только во время сборки. Он работает с обычным JavaScript и понимает [Rules of React](../reference/rules/index.md), поэтому вам не нужно переписывать код, чтобы использовать его.

В состав компилятора также входит плагин [eslint](#installing-eslint-plugin-react-compiler), который отображает анализ от компилятора прямо в вашем редакторе. Плагин работает независимо от компилятора и может быть использован, даже если вы не используете компилятор в своем приложении. Мы рекомендуем всем разработчикам React использовать этот плагин eslint для улучшения качества вашей кодовой базы.

## Что делает компилятор? {#what-does-the-compiler-do}

Компилятор понимает ваш код на глубоком уровне благодаря пониманию семантики обычного JavaScript и [Rules of React](../reference/rules/index.md). Это позволяет ему добавлять автоматические оптимизации в ваш код.

Сегодня вы можете быть знакомы с ручной мемоизацией через [`useMemo`](../reference/react/useMemo.md), [`useCallback`](../reference/react/useCallback.md) и [`React.memo`](../reference/react/memo.md). Компилятор может автоматически сделать это за вас, если ваш код следует [Rules of React](../reference/rules/index.md). Если он обнаружит нарушения правил, то автоматически пропустит только эти компоненты или хуки и продолжит безопасную компиляцию остального кода.

Если ваша кодовая база уже очень хорошо мемоизирована, вы можете не ожидать значительного повышения производительности компилятора. Тем не менее, на практике правильно указать зависимости, вызывающие проблемы с производительностью, вручную довольно сложно.

## Стоит ли мне попробовать компилятор? {#should-i-try-out-the-compiler}

Обратите внимание, что компилятор все еще является экспериментальным и имеет много неровностей. Хотя он уже используется в производстве в таких компаниях, как Meta, внедрение компилятора в производство для вашего приложения будет зависеть от состояния вашей кодовой базы и от того, насколько хорошо вы следуете [Правилам React](../reference/rules/index.md).

**Вы не должны торопиться использовать компилятор сейчас. Можно подождать до выхода стабильного релиза, прежде чем использовать его.** Однако мы будем рады, если вы попробуете его в небольших экспериментах в своих приложениях, чтобы вы могли [предоставить нам обратную связь](#reporting-issues), чтобы помочь сделать компилятор лучше.

## Начало работы {#getting-started}

В дополнение к этой документации мы рекомендуем посетить [React Compiler Working Group](https://github.com/reactwg/react-compiler) для получения дополнительной информации и обсуждения компилятора.

### Развертывание компилятора в вашей кодовой базе {#использование компилятора эффективно}

#### Существующие проекты {#existing-projects}

Компилятор предназначен для компиляции функциональных компонентов и хуков, которые следуют [Правилам React](../reference/rules/index.md). Он также может обрабатывать код, который нарушает эти правила, отбрасывая (пропуская) такие компоненты или хуки. Однако из-за гибкой природы JavaScript компилятор не может отловить все возможные нарушения и может компилировать с ложными отрицательными результатами: то есть компилятор может случайно скомпилировать компонент/хук, который нарушает правила React, что может привести к неопределенному поведению.

По этой причине для успешного внедрения компилятора в существующие проекты мы рекомендуем сначала запустить его на небольшом каталоге в коде вашего продукта. Это можно сделать, настроив компилятор на запуск только в определенном наборе директорий:

```js hl_lines="3"
const ReactCompilerConfig = {
    sources: (filename) => {
        return filename.indexOf('src/path/to/dir') !== -1;
    },
};
```

В редких случаях вы также можете настроить компилятор на работу в режиме «opt-in» с помощью опции `compilationMode: "annotation"`. В этом случае компилятор будет компилировать только компоненты и хуки, аннотированные директивой `"use memo"`. Обратите внимание, что режим `annotation` является временным, чтобы помочь ранним пользователям, и что мы не планируем использовать директиву `"use memo"` в долгосрочной перспективе.

```js hl_lines="2 7"
const ReactCompilerConfig = {
    compilationMode: 'annotation',
};

// src/app.jsx
export default function App() {
    'use memo';
    // ...
}
```

Когда вы будете более уверены в развертывании компилятора, вы сможете расширить охват и на другие каталоги и постепенно развернуть его на все приложение.

#### Новые проекты {#new-projects}

Если вы начинаете новый проект, вы можете включить компилятор для всей вашей кодовой базы, что является поведением по умолчанию.

## Установка {#installation}

### Проверка совместимости {#checking-compatibility}

Перед установкой компилятора вы можете сначала проверить, совместима ли ваша кодовая база:

```sh
npx react-compiler-healthcheck
```

Этот скрипт будет:

-   Проверить, сколько компонентов может быть успешно оптимизировано: чем больше, тем лучше
-   Проверит использование `<StrictMode>`: если он включен и соблюдается, то вероятность соблюдения [Rules of React](../reference/rules/index.md) выше.
-   Проверка использования несовместимых библиотек: известные библиотеки, которые несовместимы с компилятором

В качестве примера:

```
Successfully compiled 8 out of 9 components.
StrictMode usage not found.
Found no usage of incompatible libraries.
```

### Установка eslint-plugin-react-compiler {#installing-eslint-plugin-react-compiler}

React Compiler также поддерживает плагин eslint. Плагин eslint может использоваться **независимо** от компилятора, то есть вы можете использовать плагин eslint, даже если вы не используете компилятор.

```
npm install eslint-plugin-react-compiler
```

Затем добавьте его в конфигурацию eslint:

```js
module.exports = {
    plugins: ['eslint-plugin-react-compiler'],
    rules: {
        'react-compiler/react-compiler': 2,
    },
};
```

### Использование с Babel {#usage-with-babel}

```sh
npm install babel-plugin-react-compiler
```

Компилятор включает в себя плагин Babel, который вы можете использовать в своем конвейере сборки для запуска компилятора.

После установки добавьте его в конфигурацию Babel. Обратите внимание, что очень важно, чтобы компилятор запускался **первым** в конвейере:

```js hl_lines="7"
// babel.config.js
const ReactCompilerConfig = {
    /* ... */
};

module.exports = function () {
    return {
        plugins: [
            [
                'babel-plugin-react-compiler',
                ReactCompilerConfig,
            ], // must run first!
            // ...
        ],
    };
};
```

`babel-plugin-react-compiler` должен запускаться первым перед другими плагинами Babel, поскольку компилятору требуется исходная информация для анализа языка.

### Использование с Vite {#usage-with-vite}

Если вы используете Vite, вы можете добавить плагин в vite-plugin-react:

```js
// vite.config.js
const ReactCompilerConfig = {
    /* ... */
};

export default defineConfig(() => {
    return {
        plugins: [
            react({
                babel: {
                    plugins: [
                        [
                            'babel-plugin-react-compiler',
                            ReactCompilerConfig,
                        ],
                    ],
                },
            }),
        ],
        // ...
    };
});
```

### Использование с Next.js {#usage-with-nextjs}

Next.js позволяет использовать более медленный конвейер сборки через Babel, который может быть включен [настройкой Babel](#usage-with-babel) путем добавления файла `babel.config.js`.

### Использование с Remix {#usage-with-remix}

Установите `vite-plugin-babel` и добавьте к нему плагин компилятора Babel:

```sh
npm install vite-plugin-babel
```

---

```js
// vite.config.js
import babel from 'vite-plugin-babel';

const ReactCompilerConfig = {
    /* ... */
};

export default defineConfig({
    plugins: [
        remix({
            /* ... */
        }),
        babel({
            filter: /\.[jt]sx?$/,
            babelConfig: {
                presets: ['@babel/preset-typescript'], // if you use TypeScript
                plugins: [
                    [
                        'babel-plugin-react-compiler',
                        ReactCompilerConfig,
                    ],
                ],
            },
        }),
    ],
});
```

### Использование с Webpack {#usage-with-webpack}

Вы можете создать свой собственный загрузчик для React Compiler, например, так:

```js
const ReactCompilerConfig = {
    /* ... */
};
const BabelPluginReactCompiler = require('babel-plugin-react-compiler');

function reactCompilerLoader(sourceCode, sourceMap) {
    // ...
    const result = transformSync(sourceCode, {
        // ...
        plugins: [
            [BabelPluginReactCompiler, ReactCompilerConfig],
        ],
        // ...
    });

    if (result === null) {
        this.callback(
            Error(
                `Failed to transform "${options.filename}"`
            )
        );
        return;
    }

    this.callback(
        null,
        result.code,
        result.map === null ? undefined : result.map
    );
}

module.exports = reactCompilerLoader;
```

### Использование с Expo {#usage-with-expo}

Expo использует Babel через Metro, поэтому обратитесь к разделу [Usage with Babel](#usage-with-babel) за инструкциями по установке.

### Использование с React Native (Metro) {#usage-with-react-native-metro}

React Native использует Babel через Metro, поэтому обратитесь к разделу [Usage with Babel](#usage-with-babel) за инструкциями по установке.

## Устранение неполадок {#troubleshooting}

### Сообщение о проблемах {#reporting-issues}

Чтобы сообщить о проблемах, пожалуйста, сначала создайте минимальный реплейсер на [React Compiler Playground](https://playground.react.dev/) и включите его в ваше сообщение об ошибке.

Вы можете открыть проблемы в репо [facebook/react](https://github.com/facebook/react/issues).

Вы также можете оставить отзыв в рабочей группе React Compiler Working Group, подав заявку на вступление. Подробности о вступлении смотрите в [README](https://github.com/reactwg/react-compiler).

### Общие проблемы {#common-issues}

#### Ошибка `(0 , _c) is not a function` {#0--\_c-is-not-a-function-error}

Это происходит во время оценки модуля JavaScript, если вы не используете React 19 Beta и выше. Чтобы исправить это, сначала [обновите свое приложение до React 19 Beta](https://react.dev/blog/2024/04/25/react-19-upgrade-guide).

### Отладка {#debugging}

#### Проверка того, были ли оптимизированы компоненты {#checking-if-components-have-been-optimized}

##### React DevTools {#react-devtools}

React Devtools (v5.0+) имеет встроенную поддержку React Compiler и будет отображать значок «Memo ✨» рядом с компонентами, которые были оптимизированы компилятором.

##### Другие вопросы {#other-issues}

См. <https://github.com/reactwg/react-compiler/discussions/7>.
