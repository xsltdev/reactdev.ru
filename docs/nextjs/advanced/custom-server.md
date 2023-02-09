# Кастомный сервер

Пример кастомного сервера:

```js
// server.js
const { createServer } = require('http');
const { parse } = require('url');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  createServer((req, res) => {
    // `true` обеспечивает разбор строки запроса
    const parseUrl = parse(req.url, true);
    const { pathname, query } = parseUrl;

    switch (pathname) {
      case '/a':
        return app.render(req, res, '/a', query);
      case '/b':
        return app.render(req, res, '/b', query);
      default:
        handle(req, res, parsedUrl);
    }
  }).listen(3000, (err) => {
    if (err) throw err;
    console.log('Запущен по адресу: http://localhost:3000');
  });
});
```

Для запуска этого сервера необходимо обновить раздел `scripts` в файле `package.json` следующим образом:

```json
"scripts": {
  "dev": "node server.js",
  "build": "next build",
  "start": "NODE_ENV=production node server.js"
}
```

Кастомный сервер использует такой импорт для подключения к Next.js-приложению:

```js
const next = require('next');
const app = next({});
```

`next` — это функция, которая принимает объект со следующими настройками:

- `dev: boolean` — запуск сервера в режиме для разработки
- `dir: string` — корневая директория проекта (по умолчанию `.`)
- `quiet: boolean` — если `true`, ошибки сервера не отображаются (по умолчанию `false`)
- `conf: object` — такой же объект, что используется в `next.config.js`

После этого `app` может использоваться для обработки входящих запросов.

По умолчанию Next.js обслуживает каждый файл в директории `pages` по пути, совпадающему с названием файла. При использовании кастомного сервера это может привести к возвращению одинакового контента для разных путей.

Для отключения маршрутизации, основанной на файлах в `pages`, используется настройка `useFileSystemPublicRoutes` в `next.config.js`:

```js
module.exports = {
  useFileSystemPublicRoutes: false,
};
```

Обратите внимание: это отключает роутинг по названиям файлов только для SSR. Маршрутизация на стороне клиента по-прежнему будет иметь доступ к этим путям.
