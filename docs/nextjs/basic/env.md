# Переменные среды окружения

Next.js имеет встроенную поддержку переменных среды окружения, что позволяет делать следующее:

- использовать `.env.local` для загрузки переменных
- экстраполировать переменные в браузер с помощью префикса `NEXT_PUBLIC_`

Предположим, что у нас имеется такой файл `.env.local`:

```
DB_HOST=localhost
DB_USER=myuser
DB_PASS=mypassword
```

Это приведет к автоматической загрузке `process.env.DB_HOST`, `process.env.DB_USER` и `process.env.DB_PASS` в среду выполнения Node.js, позволяя использовать их в методах получения данных и интерфейсе маршрутизации:

```js
// pages/index.js
export async function getStaticProps() {
  const db = await myDB.connect({
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
  });

  // ...
}
```

Next.js позволяет использовать переменные внутри файлов `.env`:

```
HOSTNAME=localhost
PORT=8080
HOST=http://$HOSTNAME:$PORT
```

Для того, чтобы передать переменную среды окружения в браузер к ней нужно добавить префикс `NEXT_PUBLIC_`:

```
NEXT_PUBLIC_ANALYTICS_ID=abcdefghijk
```

```js
// pages/index.js
import setupAnalyticsService from '../lib/my-analytics-service';

setupAnalyticsService(process.env.NEXT_PUBLIC_ANALYTICS_ID);

function HomePage() {
  return <h1>Привет, народ!</h1>;
}

export default HomePage;
```

В дополнение к `.env.local` можно создавать файлы `.env` (для обоих режимов), `.env.development` (для режима разработки) и `.env.production` (для производственного режима). Обратите внимание: `.env.local` всегда имеет приоритет над другими файлами, содержащими переменные среды окружения.
