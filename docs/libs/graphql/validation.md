# Валидация

При использовании системы типов, можно предварительно проверить, является ли запрос GraphQL валидным или нет. Это позволяет серверам и клиентам эффективно информировать разработчиков, когда создается некорректный запрос, без необходимости полагаться на проверки при запуске.

В нашем примере с Star Wars файл `starWarsValidation-test.js` содержит запросы, демонстрирующие различные ошибки, и является тестовым файлом, который может быть запущен для осуществления контроля валидатора имплементации.

Для начала, давайте возьмем полностью валидный запрос. Это вложенный запрос, похожий на пример из предыдущей секции, но с продублированными полями, вынесенными в фрагмент:

=== "Request"

    ```graphql
    {
      hero {
        ...NameAndAppearances
        friends {
          ...NameAndAppearances
          friends {
            ...NameAndAppearances
          }
        }
      }
    }
    ```

=== "Response"

    ```graphql
    fragment NameAndAppearances on Character {
      name
      appearsIn
    }

    {
      "data": {
        "hero": {
          "name": "R2-D2",
          "appearsIn": [
            "NEWHOPE",
            "EMPIRE",
            "JEDI"
          ],
          "friends": [
            {
              "name": "Luke Skywalker",
              "appearsIn": [
                "NEWHOPE",
                "EMPIRE",
                "JEDI"
              ],
              "friends": [
                {
                  "name": "Han Solo",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "Leia Organa",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "C-3PO",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "R2-D2",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                }
              ]
            },
            {
              "name": "Han Solo",
              "appearsIn": [
                "NEWHOPE",
                "EMPIRE",
                "JEDI"
              ],
              "friends": [
                {
                  "name": "Luke Skywalker",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "Leia Organa",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "R2-D2",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                }
              ]
            },
            {
              "name": "Leia Organa",
              "appearsIn": [
                "NEWHOPE",
                "EMPIRE",
                "JEDI"
              ],
              "friends": [
                {
                  "name": "Luke Skywalker",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "Han Solo",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "C-3PO",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                },
                {
                  "name": "R2-D2",
                  "appearsIn": [
                    "NEWHOPE",
                    "EMPIRE",
                    "JEDI"
                  ]
                }
              ]
            }
          ]
        }
      }
    }
    ```

Этот запрос - валиден. Давайте взгянем на невалидные запросы.

Фрагмент не может ссылаться на самого себя или создавать цикл, так как это может вызвать бесконечный ответ! Ниже приведен тот же запрос, но без явных трех уровней вложенности:

=== "Request"

    ```graphql
    {
      hero {
        ...NameAndAppearancesAndFriends
      }
    }

    fragment NameAndAppearancesAndFriends on Character {
      name
      appearsIn
      friends {
        ...NameAndAppearancesAndFriends
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "errors": [
        {
          "message": "Cannot spread fragment \"NameAndAppearancesAndFriends\" within itself.",
          "locations": [
            {
              "line": 11,
              "column": 5
            }
          ]
        }
      ]
    }
    ```

Когда мы запрашиваем поля, мы должны запросить поле данного типа. Поэтому т. к. `hero` позвращает `Character`, мы должны запросить поле типа `Character`. Этот тип не имеет поле `favoriteSpaceship`, так что данный запрос неверен:

=== "Request"

    ```graphql
    # INVALID: favoriteSpaceship does not exist on Character
    {
      hero {
        favoriteSpaceship
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "errors": [
        {
          "message": "Cannot query field \"favoriteSpaceship\" on type \"Character\".",
          "locations": [
            {
              "line": 4,
              "column": 5
            }
          ]
        }
      ]
    }
    ```

Каждый раз, когда мы запрашиваем поле и он возвращает что-то, отличное от scalar или enum, мы должны уточнить, какие данные мы хотим получить обратно из поля. `Hero` возвращает `Character`, и мы запрашивали поля `name` и `appearsIn` в нем; если мы это упустим, запрос не будет валидным:

=== "Request"

    ```graphql
    # INVALID: hero is not a scalar, so fields are needed
    {
      hero
    }
    ```

=== "Result"

    ```graphql
    {
      "errors": [
        {
          "message": "Field \"hero\" of type \"Character\" must have a selection of subfields. Did you mean \"hero { ... }    \"?",
          "locations": [
            {
              "line": 3,
              "column": 3
            }
          ]
        }
      ]
    }
    ```

Аналогично, если поле имеет тип scalar, не имеет смысла запрашивать дополнительные поля в нем, это вызовет ошибку:

=== "Request"

    ```graphql
    # INVALID: name is a scalar, so fields are not permitted
    {
      hero {
        name {
          firstCharacterOfName
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "errors": [
        {
          "message": "Field \"name\" must not have a selection since type \"String!\" has no subfields.",
          "locations": [
            {
              "line": 4,
              "column": 10
            }
          ]
        }
      ]
    }
    ```

Ранее, было отмечено, что запрос может запрашивать поля того же типа, что и в запросе; когда мы запрашиваем `hero`, который возвращает `Character`, мы можем запрашивать только поля, которые существуют в `Character`. Что произойдет, если запросим основную функцию R2-D2?

=== "Request"

    ```graphql
    # INVALID: primaryFunction does not exist on Character
    {
      hero {
        name
        primaryFunction
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "errors": [
        {
          "message": "Cannot query field \"primaryFunction\" on type \"Character\". Did you mean to use an inline     fragment on \"Droid\"?",
          "locations": [
            {
              "line": 5,
              "column": 5
            }
          ]
        }
      ]
    }
    ```

Этот запрос ошибочен, т. к. `primaryFunction` не являетя полем типа `Character`. Нам нужен способ показать, что мы хотим получить `primaryFunction` типа `Character` если `Character` - `Droid`, и игнорировать это поле в ином случае. Мы можем использовать фрагменты, о которых мы говорили ранее. Используя фрагмент от `Droid` и включив его, мы страхуемся, что можем запросить `primaryFunction`, только если он определен.

=== "Request"

    ```graphql
    {
      hero {
        name
        ...DroidFields
      }
    }

    fragment DroidFields on Droid {
      primaryFunction
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "hero": {
          "name": "R2-D2",
          "primaryFunction": "Astromech"
        }
      }
    }
    ```

Этот запрос правильный, но большой; именованные фрагменты были удобны, когда мы использовали их несколько раз, но в данном случае он используется только один раз. Вместо того, чтобы использовать именованный фрагмент, мы можем использовать внутристрочный фрагмент; это так же позволяет нам указать тип, который мы запрашиваем, но без именования отдельного фрагмента:

=== "Request"

    ```graphql
    {
      hero {
        name
        ... on Droid {
          primaryFunction
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "hero": {
          "name": "R2-D2",
          "primaryFunction": "Astromech"
        }
      }
    }
    ```

Мы только затронули систему валидации; есть множество правил проверки, направленных на то, чтобы убедиться, что запрос GraphQL семантически полноценный. Спецификация немного углубляется в секцию "Validation", а директория `validation` в GraphQL.js содержит код, осуществляющий валидацию, совместимый со спецификацией GraphQL.
