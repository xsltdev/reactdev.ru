# Самонаблюдение

Довольно полезно запрашивать схему GraphQL, чтобы понимать, какие запросы он поддерживает. GraphQL позволяет сделать это при помощи системы самонаблюдения!

В нашем примере с Star Wars, файл [starWarsIntrospection-test.js](https://github.com/graphql/graphql-js/blob/master/src/__tests__/starWarsIntrospection-test.js) содержит набор запросов, демонстрирующий систему самонаблюдения, и является тестовым файлом, который можно запустить для реализации системы самонаблюдения освовного внедрения.

Мы спроектированили систему типов, так что мы знаем, какие типы доступны. В ином случае, мы можем спросить GraphQL, запросив поле `__schema`, всегда доступный в корневом типе `Query`. Давайте сделаем это сейчас, и узнаем, какие типы доступны.

=== "Request"

    ```graphql
    {
      __schema {
        types {
          name
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__schema": {
          "types": [
            {
              "name": "Query"
            },
            {
              "name": "Episode"
            },
            {
              "name": "Character"
            },
            {
              "name": "ID"
            },
            {
              "name": "String"
            },
            {
              "name": "Int"
            },
            {
              "name": "FriendsConnection"
            },
            {
              "name": "FriendsEdge"
            },
            {
              "name": "PageInfo"
            },
            {
              "name": "Boolean"
            },
            {
              "name": "Review"
            },
            {
              "name": "SearchResult"
            },
            {
              "name": "Human"
            },
            {
              "name": "LengthUnit"
            },
            {
              "name": "Float"
            },
            {
              "name": "Starship"
            },
            {
              "name": "Droid"
            },
            {
              "name": "Mutation"
            },
            {
              "name": "ReviewInput"
            },
            {
              "name": "__Schema"
            },
            {
              "name": "__Type"
            },
            {
              "name": "__TypeKind"
            },
            {
              "name": "__Field"
            },
            {
              "name": "__InputValue"
            },
            {
              "name": "__EnumValue"
            },
            {
              "name": "__Directive"
            },
            {
              "name": "__DirectiveLocation"
            }
          ]
        }
      }
    }
    ```

Ух ты, здесь много типов! Что они представляют? Давайте сгруппируем их:

- `Query`, `Character`, `Human`, `Episode`, `Droid` - те, что мы определии в системе типов.
- `String`, `Boolean` - встроенные скаляры, предоставляемые системой типов.
- `__Schema`, `__Type`, `__TypeKind`, `__Field`, `__InputValue`, `__EnumValue`, `__Directive` - эти содержат приставку `__`, показывающую, что эти поля являются частью системы самонаблюдения.

Теперь, давайте выясним, с чего начать изучать, какие запросы доступны. Когда мы спроектировали нашу систему типов, мы указали, с какого типа будут начинаться все запросы; давайте спросим у системы самонаблюдения об этом!

=== "Request"

    ```graphql
    {
      __schema {
        queryType {
          name
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__schema": {
          "queryType": {
            "name": "Query"
          }
        }
      }
    }
    ```

И это совпадает с тем, что мы говорили в разделе о системе типов,- тип `Query` там, где мы стартуем! Отметим, что именование тут по договоренности; мы можем назвать наш тип `Query` по-другому, и ответ будет возвращаться с этим новым именем. Хотя назвать его `Query` - полезная договоренность.

Часто полезно разобрать один определенный тип. Давайте взглянем на тип `Droid`:

=== "Request"

    ```graphql
    {
      __type(name: "Droid") {
        name
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Droid"
        }
      }
    }
    ```

Что, если мы хотим знать больше о `Droid`? Например, является ли он интерфейсом или объектом?

=== "Request"

    ```graphql
    {
      __type(name: "Droid") {
        name
        kind
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Droid",
          "kind": "OBJECT"
        }
      }
    }
    ```

Поле `kind` возвращает `__TypeKind` вида enum, одно из этих значений - `OBJECT`. Если мы запросим `Character`, мы обнаружим, что это интерфейс:

=== "Request"

    ```graphql
    {
      __type(name: "Character") {
        name
        kind
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Character",
          "kind": "INTERFACE"
        }
      }
    }
    ```

В случае с объектом полезно знать, какие поля доступны, так что давайте спросим систему самонаблюдения о `Droid`:

=== "Request"

    ```graphql
    {
      __type(name: "Droid") {
        name
        fields {
          name
          type {
            name
            kind
          }
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Droid",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL"
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL"
              }
            },
            {
              "name": "friends",
              "type": {
                "name": null,
                "kind": "LIST"
              }
            },
            {
              "name": "friendsConnection",
              "type": {
                "name": null,
                "kind": "NON_NULL"
              }
            },
            {
              "name": "appearsIn",
              "type": {
                "name": null,
                "kind": "NON_NULL"
              }
            },
            {
              "name": "primaryFunction",
              "type": {
                "name": "String",
                "kind": "SCALAR"
              }
            }
          ]
        }
      }
    }
    ```

Это все поля, которые мы определили в `Droid`!

`id` выглядит немного странно, т. к. не содержит названия типа. Это потому, что это тип "обертки" типа `NON_NULL`. Если мы запросим `ofType` по этому типу поля, мы обнаружим здесь тип `ID`, говорящий там, что это non-null `ID`.

Так же, `friends` и `appearsIn` не имеют имени, т. к. они являются оберткой типа `LIST`. Мы можем запросить `ofType` этих типов, который скажет нам, что эти типы являются списками.

=== "Request"

    ```graphql
    {
      __type(name: "Droid") {
        name
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Droid",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "friends",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": "Character",
                  "kind": "INTERFACE"
                }
              }
            },
            {
              "name": "friendsConnection",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "FriendsConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "appearsIn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "primaryFunction",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        }
      }
    }
    ```

Давайте закончим на этом, запросив у системы документацию!

=== "Request"

    ```graphql
    {
      __type(name: "Droid") {
        name
        description
      }
    }
    ```

=== "Result"

    ```graphql
    {
      "data": {
        "__type": {
          "name": "Droid",
          "description": "An autonomous mechanical character in the Star Wars universe"
        }
      }
    }
    ```

Так мы можем получить доступ к документации о системе типов, используя самонаблюдение, и создать просмотр документации, или расширить возможности IDE.

Мы только прикоснулись к системе самонаблюдения; мы можем запросить значения enum, которые представляют внедрение типов, и даже больше. Мы даже можем наблюдать за системой самонаблюдения. Документация углубляется в детали этой темы в секции ["Introspection"](https://github.com/graphql/graphql-js/blob/master/src/type/introspection.js), а файл `GraphQL.js` содержит код, реализующий систему самонаблюдения, ориентированную на спецификации GraphQL.
