# Язык GraphQL

Для практики будем использовать [API GitHub](https://developer.github.com/v4/explorer/)

GraphQL не работает с одинарными кавычками.

## Ошибки в ответе

В отличие от REST в GraphQL не используются ответы с кодами в случае возникновения ошибок (404 etc.). Для описания ошибки используется свойство `errors`.

```graphql
{
  "errors": [
    {
      "type": "MISSING_PAGINATION_BOUNDADRIES",
      "path": [
        "viewer",
        "gists"
      ],
      "locations": [
        {
          "line": 4,
          "column": 5
        }
      ],
      "message": "You must provide a `first` or `last` value to properly paginate the `gists` connection."
    }
  ]
}
```

## Редактор GraphiQL

Мы будем работать с GraphQL посредством редактора GraphiQL.

GraphiQL 'понимает' какие поля доступны для запроса - нажмите ctrl + space.

## Запрос через GraphiQL

В запросе ключевое слово `query` необязательно, если запрос один.

```graphql
query {
  viewer {
    login
  }
}
```

эквивалентно

```graphql
{
  viewer {
    login
  }
}
```

Результат:

```json
{
  "data": {
    "viewer": {
      "login": "userName"
    }
  }
}
```

## Вложенные запросы

Вложенные свойства указываются как вложенные свойства в JSON-объекте.

```graphql
{
  viewer {
    login
    gists {
      totalCount
    }
  }
}
```

## Вложенный запрос с аргументом и его значением

У свойств могут быть аргументы - они указываются в скобках как пара (ключ: значение).

```graphql
{
  viewer {
    login
    gists(first: 10) {
      totalCount
      nodes {
        id
        name
      }
    }
  }
}
```

```graphql
{
  repository(name: "graphql", owner: "facebook") {
    name
  }
}
```

Результат

```json
{
  "data": {
    "repository": {
      "name": "graphql"
    }
  }
}
```

## Алиасы

GraphQL позволяет в одном запросе вызывать несколько 'запросов':

```graphql
// ЭТО НЕВЕРНО
query {
    repository(name: "graphql", owner: "facebook") {
        name
    }

    repository(name: "react", owner: "facebook") {
        name
    }
}
```

Но в JSON свойства должны быть уникальны в рамках одного объекта (то есть в данном ожидается, что вернется 2 одинаковых свойства - `repository`).

Данную проблему решают алиасы. Например, в нашем примере `test` это свойство, которое придет в ответе при запросе на `test: repository(...`.

```graphql
query {
  test: repository(name: "graphql", owner: "facebook") {
    name
  }

  repository(name: "react", owner: "facebook") {
    name
  }
}
```

Ответ:

```json
{
  "data": {
    "test": {
      "name": "graphql"
    },
    "repository": {
      "name": "react"
    }
  }
}
```

## Фрагменты

Чтобы не дублировать однотипные структуры в запросах (см. пример ниже) в GraphQL есть фрагменты.

```graphql
query {
  graphql: repository(name: "graphql", owner: "facebook") {
    name
    description
    createdAt
    forks(first: 1) {
      edges {
        node {
          id
        }
      }
    }
  }

  react: repository(name: "react", owner: "facebook") {
    name
    description
    createdAt
    forks(first: 1) {
      edges {
        node {
          id
        }
      }
    }
  }
}
```

Фрагмент указывается через ключевое слово `fragment` далее идет `название фрагмента`, затем идет `тип фрагмента (on тип-данных)`.

```graphql
query {
  graphql: repository(name: "graphql", owner: "facebook") {
    ...repoDetails
  }

  react: repository(name: "react", owner: "facebook") {
    ...repoDetails
  }
}

fragment repoDetails on Repository {
  name
  description
  createdAt
  forks(first: 1) {
    edges {
      node {
        id
      }
    }
  }
}
```

## Названия запросов

Запросу можно указать название. Для обозначения наименования запроса после ключевого слова `query` ставится имя запроса. Это удобно для отладки на стороне сервера.

```graphql
query getRepository {
  graphql: repository(name: "graphql", owner: "facebook") {
    ...repoDetails
  }

  react: repository(name: "react", owner: "facebook") {
    ...repoDetails
  }
}
```

## Переменные

Запросы в GraphQL могут принимать аргументы (по аналогии с обычными функциями javascript), и за это в GraphQL отвечают переменные. Для определения переменных используется знак `$`.

Через `:` указывается тип данных переменной.

`!` указывает, что переменная обязательна.

В редакторе GrapihQL внизу есть окошко (`QUERY VARIABLES`), где указываются значения для переменных. При этом переменные указываются в JSON-формате.

```graphql
query getRepository($name: String!, $owner: String!) {
  graphql: repository(name: $name, owner: $owner) {
    name
    description
    createdAt
    forks(first: 1) {
      edges {
        node {
          id
        }
      }
    }
  }
}
```

Ответ:

```json
{
  "name": "react",
  "owner": "facebook"
}
```

В post-запросе:

```js
var dice = 3
var sides = 6
var query = `query RollDice($dice: Int!, $sides: Int) {
    rollDice(numDice: $dice, numSides: $sides)
}`

fetch('/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  body: JSON.stringify({
    query,
    variables: { dice, sides },
  }),
})
  .then((r) => r.json())
  .then((data) => console.log('data returned:', data))
```

Еще один пример:

```js
$('button').click(function () {
  event.preventDefault()
  var entry = $('#entry').val()

  $.ajax({
    method: 'POST',
    url: 'https://api.github.com/graphql',
    contentType: 'application/json',
    headers: {
      Authorization: 'bearer ***********',
    },
    data: JSON.stringify({
      query: `query ($entry: String!) {repository(name: $entry,
            owner: "*******") { pullRequests(last: 100) {
                nodes {
                state
                headRepository {
                    owner {
                    login
                    }
                }
                }
            }
            }
        }`,
      variables: {
        entry: entry,
      },
    }),
  })
})
```

get-запрос:

```
GET /graphql?query=query%20aTest(%24arg1%3A%20String!)%20%7B%20test(who%3A%20%24arg1)%20%7D&operationName=aTest&variables=me

// decode
/graphql?query=query aTest($arg1: String!) { test(who: $arg1) }&operationName=aTest&variables=me
```

## Директивы

Директива используется в GraphQL в двух случаях:

1. Хотим ли мы возвращать некоторое значение или нет по условию (`@include`).
2. Для того чтобы пропустить какое-либо значение (`@skip`).

Например, объявим переменную `includeForks`, которая будет отвечать за то, следует ли включать свойство `forks` в запрос или нет. И применим ее в директиве `@include`:

```graphql
query getRepository(
  $name: String!
  $owner: String!
  $includeForks: Boolean!
) {
  graphql: repository(name: $name, owner: $owner) {
    name
    description
    createdAt
    forks(first: 2) @include(if: $includeForks) {
      edges {
        node {
          createdAt
          id
        }
      }
    }
  }
}
```

## Документация схемы

Документация схемы - в редакторе GrapiQL есть вкладка `Docs`, в которой прописаны типы, которые мы можем использовать.

При клике на `Query` мы увидим все доступные запросы с описанием всех типов, доступных переменных и т. д. которые используются в запросе.

При этом документация генерируется автоматически.
