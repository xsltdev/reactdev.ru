# Встроенная поддержка CSS

## Импорт глобальных стилей

Для добавления глобальных стилей соответствующую таблицу следует импортировать в файл `pages/_app.js` (обратите внимание на нижнее подчеркивание):

```js
// pages/_app.js
import './style.css';

// Данный экспорт по умолчанию является обязательным
export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
```

Такие стили будут применяться ко всем страницам и компонентам в приложении. Обратите внимание: во избежание конфликтов глобальные стили могут импортироваться только в `pages/_app.js`.

При сборке приложения все стили объединяются в один минифицированный CSS-файл.

## Импорт стилей из директории node_modules

Стили могут импортироваться из `node_modules`.

Пример импорта глобальных стилей:

```js
// pages/_app.js
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
```

Пример импорта стилей для стороннего компонента:

```js
// components/Dialog.js
import { useState } from 'react';
import { Dialog } from '@reach/dialog';
import VisuallyHidden from '@reach/visually-hidden';
import '@reach/dialog/styles.css';

export function MyDialog(props) {
  const [show, setShow] = useState(false);
  const open = () => setShow(true);
  const close = () => setShow(false);

  return (
    <div>
      <button onClick={open} className="btn-open">
        Открыть
      </button>
      <Dialog>
        <button onClick={close} className="btn-close">
          <VisuallyHidden>Закрыть</VisuallyHidden>
          <span>X</span>
        </button>
        <p>Привет!</p>
      </Dialog>
    </div>
  );
}
```

## Добавление стилей на уровне компонента

Next.js из коробки поддерживает CSS-модули. CSS-модули должны иметь название `[name].module.css`. Они создают локальную область видимости для соответствующих стилей, что позволяет использовать одинаковые названия классов без риска возникновения коллизий. CSS-модуль импортируется как объект (обычно, именуемый `styles`), ключами которого являются названия соответствующих классов.

Пример использования CSS-модулей:

```css
/* components/Button/Button.module.css */
.danger {
  background-color: red;
  color: white;
}
```

```js
// components/Button/Button.js
import styles from './Button.module.css';

export const Button = () => (
  <button className={styles.danger}>Удалить</button>
);
```

При сборке CSS-модули конкатенируются и разделяются на отдельные минифицированные CSS-файлы, что позволяет загружать только необходимые стили.

## Поддержка SASS

Next.js поддерживает файлы с расширением `.scss` и `.sass`. SASS также может использоваться на уровне компонентов (`.module.scss` и `.module.sass`). Для компиляции SASS в CSS необходимо установить sass:

```sh
yarn add sass
```

Поведение компилятора SASS может быть кастомизировано в файле `next.config.js`, например:

```js
const path = require('path');

module.exports = {
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
};
```

## CSS-в-JS

В Next.js можно использовать любое решение CSS-в-JS. Простейшим примером является использование встроенных стилей:

```js
export const Hi = ({ name }) => (
  <p style={{ color: 'green' }}>Привет, {name}!</p>
);
```

Next.js также имеет встроенную поддержку styled-jsx:

```js
export const Bye = ({ name }) => (
  <div>
    <p>Пока, {name}. Скоро увидимся!</p>
    <style jsx>{`
      div {
        background-color: #3c3c3c;
      }
      p {
        color: #f0f0f0;
      }
      @media (max-width: 768px) {
        div {
          backround-color: #f0f0f0;
        }
        p {
          color: #3c3c3c;
        }
      }
    `}</style>
    <style global jsx>{`
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
      }
    `}</style>
  </div>
);
```
