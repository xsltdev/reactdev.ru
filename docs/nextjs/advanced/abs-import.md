# Абсолютный импорт и синонимы путей модулей

Next.js поддерживает настройки `baseUrl` и `paths` в файлах `tsconfig.json` и `jsconfig.json`.

`baseUrl` позволяет импортировать модули напрямую из корневой директории.

Пример:

```json
// `tsconfig.json` или `jsconfig.json`
{
  "compilerOptions": {
    "baseUrl": "."
  }
}
```

```js
// components/button.js
export const Button = () => <button>Click Me</button>;

// pages/index.js
import { Button } from 'components/button';

export default function Index() {
  return (
    <>
      <h1>Привет, народ!</h1>
      <Button />
    </>
  );
}
```

`paths` позволяет определять синонимы для путей модулей. Например:

```json
// `tsconfig.json` или `jsconfig.json`
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["components/*"]
    }
  }
}
```

```js
// components/button.js
export const Button = () => <button>Click Me</button>;

// pages/index.js
import { Button } from '@/button';

export default function Index() {
  return (
    <>
      <h1>Привет, народ!</h1>
      <Button />
    </>
  );
}
```
