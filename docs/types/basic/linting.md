---
id: linting
title: Linting
---

# Линтинг

> ⚠️Note, что [TSLint сейчас находится на техническом обслуживании, и вам следует попробовать использовать ESLint вместо него](https://medium.com/palantir/tslint-in-2019-1a144c2317a9). Если вас интересуют советы по работе с TSLint, ознакомьтесь с этим PR от [@azdanov](https://github.com/typescript-cheatsheets/react/pull/14). Остальная часть этого раздела посвящена только ESLint. [Вы можете конвертировать TSlint в ESlint с помощью этого инструмента](https://github.com/typescript-eslint/tslint-to-eslint-config).
>
> ⚠️This - это развивающаяся тема. `typescript-eslint-parser` больше не поддерживается, и [недавно началась работа над `typescript-eslint` в сообществе ESLint](https://eslint.org/blog/2019/01/future-typescript-eslint), чтобы привести ESLint к полному паритету и взаимодействию с TSLint.

Следите за документацией по TypeScript + ESLint на <https://github.com/typescript-eslint/typescript-eslint>:

```
yarn add -D @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint
```

добавьте скрипт `lint` в ваш `package.json`:

```json
  "scripts": {
    "lint": "eslint 'src/**/*.ts'"
  },
```

и подходящий `.eslintrc.js` (здесь используется `.js`, а не `.json`, чтобы мы могли добавлять комментарии):

```js
module.exports = {
    env: {
        es6: true,
        node: true,
        jest: true,
    },
    extends: 'eslint:recommended',
    parser: '@typescript-eslint/parser',
    plugins: ['@typescript-eslint'],
    parserOptions: {
        ecmaVersion: 2017,
        sourceType: 'module',
    },
    rules: {
        indent: ['error', 2],
        'linebreak-style': ['error', 'unix'],
        quotes: ['error', 'single'],
        'no-console': 'warn',
        'no-unused-vars': 'off',
        '@typescript-eslint/no-unused-vars': [
            'error',
            {
                vars: 'all',
                args: 'after-used',
                ignoreRestSiblings: false,
            },
        ],
        '@typescript-eslint/explicit-function-return-type':
            'warn', // Consider using explicit annotations for object literals and function return types even when they can be inferred.
        'no-empty': 'warn',
    },
};
```

Большая часть этого взята из [PR `tsdx`](https://github.com/palmerhq/tsdx/pull/70/files), который предназначен для **библиотек**.

Больше опций `.eslintrc.json` для рассмотрения с дополнительными опциями, которые могут понадобиться для **apps**:

```json
{
    "extends": [
        "airbnb",
        "prettier",
        "prettier/react",
        "plugin:prettier/recommended",
        "plugin:jest/recommended",
        "plugin:unicorn/recommended"
    ],
    "plugins": ["prettier", "jest", "unicorn"],
    "parserOptions": {
        "sourceType": "module",
        "ecmaFeatures": {
            "jsx": true
        }
    },
    "env": {
        "es6": true,
        "browser": true,
        "jest": true
    },
    "settings": {
        "import/resolver": {
            "node": {
                "extensions": [".js", ".jsx", ".ts", ".tsx"]
            }
        }
    },
    "overrides": [
        {
            "files": ["**/*.ts", "**/*.tsx"],
            "parser": "typescript-eslint-parser",
            "rules": {
                "no-undef": "off"
            }
        }
    ]
}
```

Еще один отличный ресурс - ["Использование ESLint и Prettier в TypeScript-проекте"](https://dev.to/robertcoopercode/using-eslint-and-prettier-in-a-typescript-project-53jb) от @robertcoopercode.

Уэс Бос также работает над [поддержкой TypeScript для его конфигурации eslint+prettier](https://github.com/wesbos/eslint-config-wesbos/issues/68).

Если вы ищете информацию о Prettier, ознакомьтесь с руководством [Prettier](https://github.com/typescript-cheatsheets/react/blob/main/docs/advanced/misc-concerns.md#prettier).

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/linting></small>
