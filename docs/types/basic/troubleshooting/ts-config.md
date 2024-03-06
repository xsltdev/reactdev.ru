---
description: В новой документации по TS также есть аннотации по каждому флагу, что каждый из них делает
---

# `tsconfig.json`

Вы можете найти [все опции компилятора в документации по TypeScript](https://www.typescriptlang.org/docs/handbook/compiler-options.html). [В новой документации по TS также есть аннотации по каждому флагу, что каждый из них делает](https://www.typescriptlang.org/tsconfig#allowSyntheticDefaultImports). Я использую эту настройку для APPS (не для библиотек - для библиотек вы можете посмотреть настройки, которые мы используем в `tsdx`):

```json
{
    "compilerOptions": {
        "incremental": true,
        "outDir": "build/lib",
        "target": "es5",
        "module": "esnext",
        "lib": ["DOM", "ESNext"],
        "sourceMap": true,
        "importHelpers": true,
        "declaration": true,
        "rootDir": "src",
        "strict": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "allowJs": false,
        "jsx": "react",
        "moduleResolution": "node",
        "baseUrl": "src",
        "forceConsistentCasingInFileNames": true,
        "esModuleInterop": true,
        "suppressImplicitAnyIndexErrors": true,
        "allowSyntheticDefaultImports": true,
        "experimentalDecorators": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "build", "scripts"]
}
```

Вы можете найти больше [рекомендуемых конфигов TS здесь](https://github.com/tsconfig/bases).

Пожалуйста, откройте вопрос и обсудите, есть ли лучшие рекомендуемые варианты для React.

Выбранные флаги и почему они нам нравятся:

-   `esModuleInterop`: отключает импорт пространств имен (`import * as foo from "foo"`) и включает импорт в стиле CJS/AMD/UMD (`import fs from "fs"`)
-   `strict`: `strictPropertyInitialization` заставляет вас инициализировать свойства класса или явно объявлять, что они могут быть неопределены. Вы можете отказаться от этого с помощью определенного утверждения присваивания.
-   `"typeRoots": ["./typings", "./node_modules/@types"]`: По умолчанию TypeScript ищет сторонние объявления типов в папках `node_modules/@types`и родительских папках. Вы можете переопределить это разрешение по умолчанию, чтобы поместить все свои глобальные объявления типов в специальную папку`typings`.

Время компиляции растет линейно с размером кодовой базы. Для больших проектов лучше использовать [Project References](https://www.typescriptlang.org/docs/handbook/project-references.html). Комментарии см. в нашей шпаргалке [ADVANCED](https://react-typescript-cheatsheet.netlify.app/docs/advanced).

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/troubleshooting/tsconfig></small>
