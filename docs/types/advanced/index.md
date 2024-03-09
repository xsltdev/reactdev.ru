---
description: Эта расширенная шпаргалка помогает показать и объяснить расширенное использование общих типов для тех, кто пишет утилиты/функции/редакторные реквизиты/компоненты более высокого порядка и библиотеки TS+React
---

# Продвинутая шпаргалка

**Эта расширенная шпаргалка** помогает показать и объяснить расширенное использование общих типов для тех, кто пишет утилиты/функции/редакторные реквизиты/компоненты более высокого порядка и **библиотеки TS+React**.

-   В нем также есть различные советы и рекомендации для профессиональных пользователей.
-   Советы по внесению вклада в DefinitelyTyped
-   Цель - использовать _полные преимущества_ TypeScript.

**Создание библиотек React + TypeScript**.

Лучшим инструментом для создания библиотек React + TS на данный момент является [`tsdx`](https://github.com/palmerhq/tsdx). Запустите `npx tsdx create` и выберите опцию "react". Вы можете просмотреть [React User Guide](https://github.com/palmerhq/tsdx/issues/5), чтобы получить несколько советов по лучшим практикам создания библиотек React+TS и их оптимизации для производства.

Другой вариант - [Rollpkg](https://github.com/rafgraph/rollpkg), который использует Rollup и компилятор TypeScript (не Babel) для создания пакетов. Он включает конфигурации по умолчанию для TypeScript, Prettier, ESLint и Jest (настройка для использования с React), а также статистику пакетов Bundlephobia для каждой сборки.

-   Не забудьте также проверить [руководство `basarat`](https://basarat.gitbooks.io/typescript/content/docs/quick/library.html) для настроек tsconfig библиотеки.
-   Алек Ларсон: [Лучший конфиг Rollup для библиотек TypeScript](https://gist.github.com/aleclarson/9900ed2a9a3119d865286b218e14d226)
-   Из мира Angular [посмотрите](https://github.com/bitjson/typescript-starter).

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/advanced/></small>
