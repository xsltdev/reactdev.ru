# Термины

## Запрос

Запрос - в запросе мы указываем то, что мы хотим получить от сервера.

```graphql
query {
  posts(id: 1) {
    id
    title
    author {
      firstname
      lastname
    }
  }
}
```

## Тип

Тип - типы данных. Например, перед отправкой запроса на сервер, серверу нужно объяснить, что такое `post`.

`ID!` - тип данных в GraphQL.

`Author!` - составные (пользовательские) типы данных; берутся от того, кто реализует сервер. Типы в GraphQL реализуются на стороне сервера.

```graphql
type Post {
  id: ID!
  title: String!
  content: String!
  author: Author!
  status: Status!
  comments: [Comment]!
}
type Author {
  id: ID!
  firstname: String!
  lastname: String!
}
enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}
type Comment {
  id: ID!
  title: String!
  body: String!
}
```

## Изменение (Mutation)

Изменение (Mutation) - похожи на запросы, но если запрос получает данные, то изменения изменяют данные.

```graphql
mutation {
  createPost(
    input: {
      title: "Заголовок"
      content: "..."
      status: DRAFT
      author: {
        firstname: "John"
        lastname: "Smith"
        status: DRAFT
      }
    }
  )
}
```
