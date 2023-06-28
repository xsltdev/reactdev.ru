# Сервер GraphQl в node.js

## Настройка express сервера

```js
// server.js
const express = require('express')
const server = express()

server.get('/', (req, res) => {
  res.send('hello world!')
})

server.listen(3001, () => {
  console.log('test server on port 3001')
})
```

## Отдельный модуль для API

Создадим отдельный модуль для работы API и импортируем его:

```js
// api/index.js
const express = require('express')
const api = express()

api.all('/api', (req, res) => {
  res.send('send api')
})

module.exports = api
```

```js
// server.js
server.get('/', (req, res) => {
  res.send('hello world!')
})
server.use('/', api)
server.listen(3001, () => {
  console.log('test server on port 3001')
})
```

## Библиотека graphql и express-graphql

```
npm i graphql
```

Свяжем GraphQL с express сервером при помощи `express-graphql`:

```
npm i express-graphql
```

Импортируем `express-graphql` в нашем апи модуле, при этом `express-graphql` будет отвечать за обработку запросов-ответов.

```js
// api/index.js
const express = require('express')
const graphqlMiddleWare = require('express-graphql')

const api = express()

api.all(
  '/api',
  graphqlMiddleWare({
    graphiql: true,
  })
)

module.exports = api
```

## Схема

Перед тем как сервер сможет отдавать какие-либо данные клиенту ему нужно указать с какими данными придется работать. За описание данных отвечает схема.

```js
// api/index.js
const express = require('express')
const graphqlMiddleWare = require('express-graphql')
// импортируем схему
const schema = require('./schema.js')

const api = express()

api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
  })
)

module.exports = api
```

```js
// api/schema.js
const { buildSchema } = require('graphql')

// в type Query необходимо прописать запросы, которые сможет принимть сервер
// pet - запрос на сервере; String - отдаем, к примеру, тип String
module.exports = buildSchema(`
    type Query {
        pet: String
    }
`)
```

Далее при запросу на `http://localhost:3001/api` вы сможете увидеть редактор graphiql.

## Резолверы

Нам требуется научить GraphQL отдавать данные при, например, запросе на `pet`. Для этого используются резолверы - реализация запросов в свойстве `rootValue`.

```js
// api/index.js
const express = require('express')
const graphqlMiddleWare = require('express-graphql')
// импортируем схему в файле index.js
const schema = require('./schema.js')

const api = express()

api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
    rootValue: {
      // 1 - название запроса; 2 - ф-я (реализация схемы)
      pet: () => 'test',
    },
  })
)

module.exports = api
```

Теперь при запросе в graphiQL (если `graphiql: true`) на:

```graphql
query {
  pet
}
```

Ответ:

```json
{
  "data": {
    "pet": "test"
  }
}
```

```
http://localhost:3001/api?query=query%20%7B%0A%20%20pet%0A%7D
```

## Типы в схеме

Для объекта `pet` нам нужно создать тип. Для это в файле `schema.js`:

```js
// api/schema.js
module.exports = buildSchema(`
    type Step {
        title: String!,
        completed: Boolean!
    }

    type Pet {
        id: ID!,
        name: String!,
        species: String!,
        favFoods: [String],
        birthYear: Int,
        photo: String,
        steps: [Step]
    }

    type Query {
        pet: Pet!,
        pets: [Pet]
    }
`)
```

```graphql
query {
  pets {
    id
    species
    favFoods
    birthYear
    name
    steps {
      title
      completed
    }
  }
}
```

## Реализуем запрос с аргументом/ми

Воспользуемся аргументами, чтобы получить нужного питомца по `id`:

```graphql
type Query {
  pet(id: ID!): Pet!
}
```

```js
// api/index.js
api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
    rootValue: {
      pet: ({ id }) => {
        return pets.find(function (pet) {
          return pet.id == id
        })
      },
      pets: () => pets,
    },
  })
)
```

```graphql
query {
  pet(id: 2) {
    id
    species
    favFoods
    birthYear
    name
    steps {
      title
      completed
    }
  }
}
```

## Изменения (обновление)

Для изменения данных используются изменения или `mutation`. В `schema.js` добавим еще один тип - `mutation`, в нем определим функции, которые будут изменять данные.

Данные (например, пришедшие на изменение) в GraphQL называют `input`.

```
// НЕВЕРНО, так как **
// api/schema.js
type Mutation {
    createPet(input: Pet!): Pet
    updatePet(id: ID!, input: Pet!): Pet
    deletePet(id: ID!): ID
}
```

Далее необходимо описать вышеприведенные функции как резолверы.

Для входных данных (а они в GraphQL называются словом `input`) нельзя `**` использовать типы данных, которые мы определили ранее, например, `Pet` и которые мы используем в `type Query`.

В input-ах мы можем указывать значения по умолчанию.

Для каждого входного `input` нужно определить свой тип данных через ключевой слово `input`:

```js
module.exports = buildSchema(`
    type Step {
        title: String!,
        completed: Boolean!
    }

    type Pet {
        id: ID!,
        name: String!,
        species: String!,
        favFoods: [String],
        birthYear: Int,
        photo: String,
        steps: [Step]
    }

    type Query {
        pet(id: ID!): Pet!,
        pets: [Pet]
    }

    input StepInput {
        title: String!,
        completed: Boolean = false
    }

    input PetInput {
        name: String!,
        species: String!,
        birthYear: Int,
        steps: [StepInput]
    }

    type Mutation {
        createPet(input: PetInput!): Pet
        updatePet(id: ID!, input: PetInput!): Pet
        deletePet(id: ID!): ID
    }
`)
```

Реализуем функцию, которая будет срабатывать при запросе на `createPet` (`mutation`):

```js
// api/index.js
api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
    rootValue: {
      // 1 - название запроса; 2 - ф-я (реализация схемы)
      pet: ({ id }) => {
        return pets.find(function (pet) {
          return pet.id == id
        })
      },
      pets: () => pets,
      createPet: ({ input }) => {
        let pet = { ...input, id: pets.length + 1 }
        pets.push(pet)
        return pet
      },
    },
  })
)
```

Добавим задачу через интерфейс GraphiQL:

```graphql
mutation {
  createPet(
    input: {
      name: "Bobik"
      species: "dog"
      birthYear: 2019
    }
  ) {
    id
    name
  }
}
```

```json
{
  "data": {
    "createPet": {
      "id": "6",
      "name": "Bobik"
    }
  }
}
```

Код с реализацией удаления, редактирования и добавления питомцев:

```js
// api/index.js
const express = require('express')
const graphqlMiddleWare = require('express-graphql')
// импортируем схему в файле index.js
const schema = require('./schema.js')

let pets = require('./data').pets
const api = express()

// класс Pet будет отвечать за корректную инициализацию экземпляра Pet
class Pet {
  constructor({
    name,
    species = 'dog',
    steps = [],
    birthYear = 2019,
  } = {}) {
    this.name = name
    this.species = species
    this.birthYear = birthYear
    this.steps = steps
    this.id = pets.length + 1
  }
}

api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
    rootValue: {
      // 1 - название запроса; 2 - ф-я (реализация схемы)
      pet: ({ id }) => {
        return pets.find(function (pet) {
          return pet.id == id
        })
      },
      pets: () => pets,
      createPet: ({ input }) => {
        let pet = new Pet(input)
        pets.push(pet)
        return pet
      },
      updatePet: ({ id, input }) => {
        const pet = pets.find(function (pet) {
          return pet.id == id
        })
        Object.assign(pet, input)
        return pet
      },
      deletePet: ({ id }) => {
        const pet = pets.find(function (pet) {
          return pet.id == id
        })
        pets = pets.filter(function (pet) {
          return pet.id != id
        })
        return pet.id
      },
    },
  })
)

module.exports = api
```

Запросы в GrapiQL (`getPets` и `updatePet` это кастомные названия, чтобы GrapiQL мог выбрать query/mutation):

```graphql
query getPets {
  pets {
    species
    favFoods
    birthYear
    name
    id
  }
}

mutation updatePet {
  updatePet(
    id: 1
    input: {
      name: "Bobik1"
      species: "dog1"
      birthYear: 2019
      steps: [{ title: "start", completed: true }]
    }
  ) {
    id
    name
    birthYear
  }

  deletePet(id: 1)
}
```

## Добавим MongoDB

Для взаимодействия c MongoDB установим `mongoose`:

```
npm i mongoose
```

В папке `api` создадим файл `model.js`, в котором мы опишем модель для mongoose:

```js
// api/model.js
const mongoose = require('mongoose')

const Pet = new mongoose.Schema({
  //id: - за id будет отвечать MongoDB
  name: {
    type: String,
    required: true,
  },
  species: {
    type: String,
    required: true,
  },
  favFoods: [String],
  birthYear: Number,
  photo: String,
  steps: [
    {
      title: String,
      completed: Boolean,
    },
  ],
})

module.exports = mongoose.model('Pet', Pet)
```

В файле `index.js` подключим mongoose, модель `mongoose` (реализованную ранее), подключимся к MongoDB и реализуем работу с запросами и `mongoose`:

```js
// api/index.js
const express = require('express')
const graphqlMiddleWare = require('express-graphql')
// импортируем схему в файле index.js
const schema = require('./schema.js')

const mongoose = require('mongoose')
mongoose.Promise = Promise
mongoose.connect('mongodb://localhost:27017/graphql-intro')
mongoose.connection.once('open', () =>
  console.log('connect to MongoDB')
)

// импортируем модель (mongoose)
const Pet = require('./model')

const api = express()

api.all(
  '/api',
  graphqlMiddleWare({
    schema,
    graphiql: true,
    rootValue: {
      // 1 - название запроса; 2 - ф-я (реализация схемы)
      pet: ({ id }) => Pet.findById(id),
      pets: () => Pet.find({}),
      createPet: ({ input }) => {
        // метод mongoose create возвращает Promise
        return Pet.create(input)
      },
      updatePet: ({ id, input }) => {
        return Pet.findByIdAndUpdate(id, input, {
          new: true, // то есть вернуть новый объект
        })
      },
      deletePet: ({ id }) => {
        return Pet.deleteOne({ _id: id }).then(() => {
          return id
        })
      },
    },
  })
)

module.exports = api
```

Три запроса на создание, редактирование и удаление питомцев:

```graphql
mutation createPet {
  createPet(
    input: {
      name: "Bobik"
      species: "dog"
      birthYear: 2019
    }
  ) {
    id
    name
  }
}

mutation updatePet {
  updatePet(
    id: "5c55a389a45bfa12446b9fdf"
    input: {
      name: "12Bobik"
      species: "12dog"
      birthYear: 122019
    }
  ) {
    id
    name
  }
}

mutation deletePet {
  deletePet(id: "5c55a389a45bfa12446b9fdf")
}
```

## Файл схемы

На данный момент схема описана через шаблонные строки в файле `api/schema.js` при вызове метода `buildSchema`. Но схему можно поместить в специальный файл - `schema.graphql`:

```graphql
type Step {
  title: String!
  completed: Boolean!
}

type Pet {
  id: ID!
  name: String!
  species: String!
  favFoods: [String]
  birthYear: Int
  photo: String
  steps: [Step]
}

type Query {
  pet(id: ID!): Pet!
  pets: [Pet]
}

input StepInput {
  title: String!
  completed: Boolean = false
}

input PetInput {
  name: String!
  species: String!
  birthYear: Int
  steps: [StepInput]
}

type Mutation {
  createPet(input: PetInput!): Pet
  updatePet(id: ID!, input: PetInput!): Pet
  deletePet(id: ID!): ID
}
```

Подключим вместо шаблонных строк наш файл `schema.graphql`:

```js
const { buildSchema } = require('graphql')
const path = require('path')
const fs = require('fs')

const schema = fs.readFileSync(
  path.resolve(__dirname, 'schema.graphql'),
  'utf-8'
)

module.exports = buildSchema(schema)
```
