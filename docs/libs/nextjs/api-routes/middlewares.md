# Посредники (Middlewares)

Интерфейс маршрутизации включает следующих посредников, преобразующих входящий запрос (`req`):

- `req.cookies` — объект, содержащий куки, включенные в запрос (значением по умолчанию является `{}`)
- `req.query` — объект, содержащий строку запроса (значением по умолчанию является `{}`)
- `req.body` — объект, содержащий тело запроса, преобразованное на основе заголовка Content-Type, или `null`

## Кастомизация посредников

Каждый роут может экспортировать объект `config` с настройками для посредников:

```js
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
};
```

- `bodyParser: false` — отключает разбор ответа (возвращается сырой поток данных — `Stream`)
- `bodyParser.sizeLimit` — максимальный размер тела запроса в любом формате, поддерживаемом [bytes](https://github.com/visionmedia/bytes.js)
- `externalResolver: true` — сообщает серверу, что данный роут обрабатывается внешним резолвером, таким как `express` или `connect`

## Добавление посредников

Рассмотрим добавление промежуточного обработчика [cors](https://www.npmjs.com/package/cors).

Устанавливаем модуль:

```bash
yarn add cors
```

Добавляем `cors` в роут:

```js
import Cors from 'cors';

// инициализируем посредника
const cors = Cors({
  methods: ['GET', 'HEAD'],
});

// вспомогательная функция для ожидания успешного разрешения посредника
// перед выполнением другого кода
// или для выбрасывания исключения при возникновении ошибки в посреднике
const runMiddleware = (req, res, next) =>
  new Promise((resolve, reject) => {
    fn(req, res, (result) =>
      result instanceof Error
        ? reject(result)
        : resolve(result)
    );
  });

export default async function handler(req, res) {
  // запускаем посредника
  await runMiddleware(req, res, cors);

  // остальная логика `API`
  res.json({ message: 'Всем привет!' });
}
```
