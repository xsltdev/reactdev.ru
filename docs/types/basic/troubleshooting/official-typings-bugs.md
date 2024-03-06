---
description: Исправление ошибок в официальных типизациях
---

# Исправление ошибок в официальных типизациях

Если у вас возникнут проблемы с официальными типизациями вашей библиотеки, вы можете скопировать их локально и указать TypeScript использовать вашу локальную версию с помощью поля "paths". В вашем файле `tsconfig.json`:

```json
{
    "compilerOptions": {
        "paths": {
            "mobx-react": ["../typings/modules/mobx-react"]
        }
    }
}
```

[Спасибо @adamrackis за подсказку](https://twitter.com/AdamRackis/status/1024827730452520963).

Если вам нужно просто добавить интерфейс или добавить недостающие члены в существующий интерфейс, вам не нужно копировать весь пакет типизации. Вместо этого можно использовать [объединение деклараций](https://www.typescriptlang.org/docs/handbook/declaration-merging.html):

```ts
// my-typings.ts
declare module 'plotly.js' {
    interface PlotlyHTMLElement {
        removeAllListeners(): void;
    }
}

// MyComponent.tsx
import { PlotlyHTMLElement } from 'plotly.js';

const f = (e: PlotlyHTMLElement) => {
    e.removeAllListeners();
};
```

Вам не обязательно внедрять модуль, вы можете просто импортировать его как `any` для быстрого старта:

```ts
// my-typings.ts
declare module 'plotly.js'; // each of its imports are `any`
```

Поскольку вам не нужно явно импортировать модуль, это называется [объявление модуля окружения](https://www.typescriptlang.org/docs/handbook/namespaces-and-modules.html#pitfalls-of-namespaces-and-modules). Вы можете сделать AMD в файле `.ts` в режиме сценария (без импорта и экспорта) или в файле `.d.ts` в любом месте вашего проекта.

Вы также можете делать объявления переменных и типов ambient:

```ts
// ambient utiltity type
type ToArray<T> = T extends unknown[] ? T : T[];
// ambient variable
declare let process: {
    env: {
        NODE_ENV: 'development' | 'production';
    };
};
process = {
    env: {
        NODE_ENV: 'production',
    },
};
```

Вы можете увидеть примеры этих типов, включенных в объявления встроенных типов в поле `lib` в файле `tsconfig.json`.

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/troubleshooting/official_typings_bugs></small>
