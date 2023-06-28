# Как работает GraphQL

GraphQL сервер принимает запросы от клиента, взаимодействует с БД и отправляет ответ клиенту. GraphQL запрос это http-запрос, но в отличие от REST у GraphQL всего 1 маршрут, например:

```
HTTP POST https://mysite.com/graphql
```

```js
// отправляем данные через get-запрос
fetch(
  'https://mysite.com/graphql?query={posts(id: 1){...}}'
)
```

```js
// отправляем данные через post-запрос
fetch('https://mysite.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: `
            {
                posts(id: 1) {
                    id
                    title
                    author {
                        firstname
                        lastname
                    }
                }
            }
            `,
  }),
})
```

GraphQL не подменяет сервер: GraphQL имеет некий слой между клиентов и сервером. GraphQL может быть не очень удобен с точки зрения реализации, но с точки зрения клиента он очень удобен.
