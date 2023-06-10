# Компоненты React DOM

React поддерживает все встроенные в браузеры компоненты [HTML](https://hcdev.ru/html/) и [SVG](https://developer.mozilla.org/docs/Web/SVG/Element).

## Общие компоненты

Все встроенные компоненты браузера поддерживают некоторые реквизиты и события.

-   [Общие компоненты (например, `div`)](components-common.md)

Сюда входят специфические для React реквизиты, такие как `ref` и `dangerouslySetInnerHTML`.

## Компоненты формы

Эти встроенные компоненты браузера принимают пользовательский ввод:

-   [`<input>`](components-input.md)
-   [`<select>`](components-select.md)
-   [`<textarea>`](components-textarea.md)

Они особенные в React, потому что передача им свойства `value` делает их _[управляемыми.](components-input.md#controlling-an-input-with-a-state-variable)_.

## Все компоненты HTML

React поддерживает все встроенные HTML-компоненты браузера.

!!!note ""

    Подобно стандарту [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model), React использует соглашение `camelCase` для имен реквизитов. Например, вы будете писать `tabIndex` вместо `tabindex`. Вы можете преобразовать существующий HTML в JSX с помощью [онлайн-конвертера](https://transform.tools/html-to-jsx).

### Пользовательские HTML-элементы

Если вы отображаете тег с тире, например `<my-element>`, React будет считать, что вы хотите отобразить [пользовательский элемент HTML](https://developer.mozilla.org/docs/Web/Web_Components/Using_custom_elements). В React рендеринг пользовательских элементов работает иначе, чем рендеринг встроенных тегов браузера:

-   Все реквизиты пользовательских элементов сериализуются в строки и всегда задаются с помощью атрибутов.
-   Пользовательские элементы принимают `class`, а не `className`, и `for`, а не `htmlFor`.

Если вы отображаете встроенный HTML-элемент браузера с атрибутом [`is`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/is), он также будет рассматриваться как пользовательский элемент.

!!!note ""

    [Будущая версия React будет включать более полную поддержку пользовательских элементов](https://github.com/facebook/react/issues/11347#issuecomment-1122275286).

    Вы можете попробовать это, обновив пакеты React до последней экспериментальной версии:

    -   `react@experimental`
    -   `react-dom@experimental`.

    Экспериментальные версии React могут содержать ошибки. Не используйте их в производстве.

## Все компоненты SVG

React поддерживает все встроенные в браузер SVG-компоненты.

!!!note ""

    Подобно стандарту [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model), React использует соглашение `camelCase` для имен реквизитов. Например, вы будете писать `tabIndex` вместо `tabindex`. Вы можете преобразовать существующий SVG в JSX с помощью [онлайн-конвертера](https://transform.tools/).

    Атрибуты с именами также должны быть написаны без двоеточия:

    -   `xlink:actuate` становится `xlinkActuate`.
    -   `xlink:arcrole` становится `xlinkArcrole`.
    -   `xlink:href` становится `xlinkHref`.
    -   `xlink:role` становится `xlinkRole`.
    -   `xlink:show` становится `xlinkShow`.
    -   `xlink:title` становится `xlinkTitle`.
    -   `xlink:type` становится `xlinkType`.
    -   `xml:base` становится `xmlBase`.
    -   `xml:lang` становится `xmlLang`.
    -   `xml:space` становится `xmlSpace`.
    -   `xmlns:xlink` становится `xmlnsXlink`.

## Ссылки

-   [https://react.dev/reference/react-dom/components](https://react.dev/reference/react-dom/components)
