---
description: Глобалы, изображения и другие файлы, не относящиеся к TS
---

# Глобалы, изображения и другие файлы, не относящиеся к TS

Используйте [объединение деклараций](https://www.typescriptlang.org/docs/handbook/declaration-merging.html).

Если, скажем, вы используете сторонний JS-скрипт, который подключается к глобалу `window`, вы можете расширить `Window`:

```ts
declare global {
    interface Window {
        MyVendorThing: MyVendorType;
    }
}
```

Аналогично, если вы хотите "импортировать" изображение или другой файл, не относящийся к TS/TSX:

```ts
// declaration.d.ts
// anywhere in your project, NOT the same name as any of your .ts/tsx files
declare module '*.png';

// importing in a tsx file
import * as logo from './logo.png';
```

Обратите внимание, что `tsc` не может упаковать эти файлы за вас, вам придется использовать Webpack или Parcel.

[Связанный вопрос](https://github.com/Microsoft/TypeScript-React-Starter/issues/12) и [StackOverflow](https://stackoverflow.com/a/49715468/4216035)

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/troubleshooting/non_ts_files></small>
