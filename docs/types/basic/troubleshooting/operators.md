---
description: Операторы
---

# Операторы

-   `typeof` и `instanceof`: запрос типа, используемый для уточнения.
-   `keyof`: получение ключей объекта. `keyof T` - оператор, указывающий, какие значения `k` могут быть использованы для `obj[k]`.
    -   [Некоторые заблуждения здесь](https://twitter.com/SeaRyanC/status/1418678670739218438?s=20).
-   `O[K]`: поиск свойств
-   `[K в O]`: сопоставленные типы
-   `+` или `-` или `readonly` или `?`: сложение и вычитание, модификаторы readonly и optional
-   `x ? Y : Z`: Условные типы для общих типов, псевдонимы типов, типы параметров функций
-   `!`: Утверждение nonnull для nullable типов
-   `=`: Параметр общего типа по умолчанию для общих типов
-   `as`: утверждение типа
-   `is`: защита типа для типов с возвратом функции

Условные типы - сложная тема для изучения, поэтому вот несколько дополнительных ресурсов:

-   [полное объяснение](https://artsy.github.io/blog/2018/11/21/conditional-types-in-typescript/)
-   [Отступление и другие продвинутые темы](https://github.com/sw-yx/ts-spec/blob/master/conditional-types.md)
-   [Видео Басарата](https://www.youtube.com/watch?v=SbVgPQDealg&list=PLYvdvJlnTOjF6aJsWWAt7kZRJvzw-en8B&index=2&t=0s)
-   [Дженерики, условные типы и сопоставленные типы](https://www.youtube.com/watch?v=PJjeHzvi_VQ&feature=youtu.be)

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/troubleshooting/operators></small>
