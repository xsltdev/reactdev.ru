---
description: React поддерживает все встроенные в браузеры компоненты HTML и SVG
---

# Компоненты React DOM

React поддерживает все встроенные в браузеры компоненты [HTML](https://developer.mozilla.org/docs/Web/HTML/Element) и [SVG](https://developer.mozilla.org/docs/Web/SVG/Element).

## Общие компоненты {#common-components}

Все встроенные компоненты браузера поддерживают некоторые параметры и события.

-   [Общие компоненты (например, `<div>`)](./common.md)

Сюда входят специфические для React пропсы, такие как `ref` и `dangerouslySetInnerHTML`.

## Компоненты форм {#form-components}

Эти встроенные компоненты браузера принимают пользовательский ввод:

-   [`<input>`](./input.md)
-   [`<select>`](./select.md)
-   [`<textarea>`](./textarea.md)

Они особенные в React, потому что передача им свойства `value` делает их _[управляемыми](./input.md#controlling-an-input-with-a-state-variable)_.

## Компоненты ресурсов и метаданных {#resource-and-metadata-components}

Эти компоненты браузера позволяют загружать внешние ресурсы или аннотировать документ метаданными:

-   [`<link>`](./link.md)
-   [`<meta>`](./meta.md)
-   [`<script>`](./script.md)
-   [`<style>`](./style.md)
-   [`<title>`](./title.md)

Они особенные в React, потому что React может выводить их в шапку документа, приостанавливать загрузку ресурсов и выполнять другие действия, которые описаны на справочной странице для каждого конкретного компонента.

## Все HTML-компоненты {#all-html-components}

React поддерживает все встроенные в браузер HTML-компоненты. К ним относятся:

-   [`<aside>`](https://hcdev.ru/html/aside)
-   [`<audio>`](https://hcdev.ru/html/audio)
-   [`<b>`](https://hcdev.ru/html/b)
-   [`<base>`](https://hcdev.ru/html/base)
-   [`<bdi>`](https://hcdev.ru/html/bdi)
-   [`<bdo>`](https://hcdev.ru/html/bdo)
-   [`<blockquote>`](https://hcdev.ru/html/blockquote)
-   [`<body>`](https://hcdev.ru/html/body)
-   [`<br>`](https://hcdev.ru/html/br)
-   [`<button>`](https://hcdev.ru/html/button)
-   [`<canvas>`](https://hcdev.ru/html/canvas)
-   [`<caption>`](https://hcdev.ru/html/caption)
-   [`<cite>`](https://hcdev.ru/html/cite)
-   [`<code>`](https://hcdev.ru/html/code)
-   [`<col>`](https://hcdev.ru/html/col)
-   [`<colgroup>`](https://hcdev.ru/html/colgroup)
-   [`<data>`](https://hcdev.ru/html/data)
-   [`<datalist>`](https://hcdev.ru/html/datalist)
-   [`<dd>`](https://hcdev.ru/html/dd)
-   [`<del>`](https://hcdev.ru/html/del)
-   [`<details>`](https://hcdev.ru/html/details)
-   [`<dfn>`](https://hcdev.ru/html/dfn)
-   [`<dialog>`](https://hcdev.ru/html/dialog)
-   [`<div>`](https://hcdev.ru/html/div)
-   [`<dl>`](https://hcdev.ru/html/dl)
-   [`<dt>`](https://hcdev.ru/html/dt)
-   [`<em>`](https://hcdev.ru/html/em)
-   [`<embed>`](https://hcdev.ru/html/embed)
-   [`<fieldset>`](https://hcdev.ru/html/fieldset)
-   [`<figcaption>`](https://hcdev.ru/html/figcaption)
-   [`<figure>`](https://hcdev.ru/html/figure)
-   [`<footer>`](https://hcdev.ru/html/footer)
-   [`<form>`](https://hcdev.ru/html/form)
-   [`<h1>`](https://hcdev.ru/html/h1)
-   [`<head>`](https://hcdev.ru/html/head)
-   [`<header>`](https://hcdev.ru/html/header)
-   [`<hgroup>`](https://hcdev.ru/html/hgroup)
-   [`<hr>`](https://hcdev.ru/html/hr)
-   [`<html>`](https://hcdev.ru/html/html)
-   [`<i>`](https://hcdev.ru/html/i)
-   [`<iframe>`](https://hcdev.ru/html/iframe)
-   [`<img>`](https://hcdev.ru/html/img)
-   [`<input>`](./input.md)
-   [`<ins>`](https://hcdev.ru/html/ins)
-   [`<kbd>`](https://hcdev.ru/html/kbd)
-   [`<label>`](https://hcdev.ru/html/label)
-   [`<legend>`](https://hcdev.ru/html/legend)
-   [`<li>`](https://hcdev.ru/html/li)
-   [`<link>`](https://hcdev.ru/html/link)
-   [`<main>`](https://hcdev.ru/html/main)
-   [`<map>`](https://hcdev.ru/html/map)
-   [`<mark>`](https://hcdev.ru/html/mark)
-   [`<menu>`](https://hcdev.ru/html/menu)
-   [`<meta>`](https://hcdev.ru/html/meta)
-   [`<meter>`](https://hcdev.ru/html/meter)
-   [`<nav>`](https://hcdev.ru/html/nav)
-   [`<noscript>`](https://hcdev.ru/html/noscript)
-   [`<object>`](https://hcdev.ru/html/object)
-   [`<ol>`](https://hcdev.ru/html/ol)
-   [`<optgroup>`](https://hcdev.ru/html/optgroup)
-   [`<option>`](./option.md)
-   [`<output>`](https://hcdev.ru/html/output)
-   [`<p>`](https://hcdev.ru/html/p)
-   [`<picture>`](https://hcdev.ru/html/picture)
-   [`<pre>`](https://hcdev.ru/html/pre)
-   [`<progress>`](./progress.md)
-   [`<q>`](https://hcdev.ru/html/q)
-   [`<rp>`](https://hcdev.ru/html/rp)
-   [`<rt>`](https://hcdev.ru/html/rt)
-   [`<ruby>`](https://hcdev.ru/html/ruby)
-   [`<s>`](https://hcdev.ru/html/s)
-   [`<samp>`](https://hcdev.ru/html/samp)
-   [`<script>`](https://hcdev.ru/html/script)
-   [`<section>`](https://hcdev.ru/html/section)
-   [`<select>`](./select.md)
-   [`<slot>`](https://hcdev.ru/html/slot)
-   [`<small>`](https://hcdev.ru/html/small)
-   [`<source>`](https://hcdev.ru/html/source)
-   [`<span>`](https://hcdev.ru/html/span)
-   [`<strong>`](https://hcdev.ru/html/strong)
-   [`<style>`](https://hcdev.ru/html/style)
-   [`<sub>`](https://hcdev.ru/html/sub)
-   [`<summary>`](https://hcdev.ru/html/summary)
-   [`<sup>`](https://hcdev.ru/html/sup)
-   [`<table>`](https://hcdev.ru/html/table)
-   [`<tbody>`](https://hcdev.ru/html/tbody)
-   [`<td>`](https://hcdev.ru/html/td)
-   [`<template>`](https://hcdev.ru/html/template)
-   [`<textarea>`](./textarea.md)
-   [`<tfoot>`](https://hcdev.ru/html/tfoot)
-   [`<th>`](https://hcdev.ru/html/th)
-   [`<thead>`](https://hcdev.ru/html/thead)
-   [`<time>`](https://hcdev.ru/html/time)
-   [`<title>`](https://hcdev.ru/html/title)
-   [`<tr>`](https://hcdev.ru/html/tr)
-   [`<track>`](https://hcdev.ru/html/track)
-   [`<u>`](https://hcdev.ru/html/u)
-   [`<ul>`](https://hcdev.ru/html/ul)
-   [`<var>`](https://hcdev.ru/html/var)
-   [`<video>`](https://hcdev.ru/html/video)
-   [`<wbr>`](https://hcdev.ru/html/wbr)

!!!note "camelCase для имен свойств"

    По аналогии со стандартом [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model) React использует соглашение `camelCase` для имен свойств. Например, вы будете писать `tabIndex` вместо `tabindex`. Вы можете преобразовать существующий HTML в JSX с помощью [онлайн-конвертера](https://transform.tools/html-to-jsx).

### Пользовательские HTML-элементы {#custom-html-elements}

Если вы отображаете тег с тире, например `<my-element>`, React предположит, что вы хотите отобразить [пользовательский HTML-элемент.](https://developer.mozilla.org/docs/Web/Web_Components/Using_custom_elements) В React отрисовка пользовательских элементов работает иначе, чем отрисовка встроенных тегов браузера:

-   Все параметры пользовательских элементов сериализуются в строки и всегда задаются с помощью атрибутов.
-   Пользовательские элементы принимают `class`, а не `className`, и `for`, а не `htmlFor`.

Если вы отображаете встроенный HTML-элемент браузера с атрибутом [`is`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/is), он также будет рассматриваться как пользовательский элемент.

!!!note "Пользовательские элементы в React"

    [Будущая версия React будет включать более полную поддержку пользовательских элементов](https://github.com/facebook/react/issues/11347#issuecomment-1122275286).

    Вы можете попробовать это, обновив пакеты React до последней экспериментальной версии:

    -   `react@experimental`
    -   `react-dom@experimental`

    Экспериментальные версии React могут содержать ошибки. Не используйте их в производстве.

## Все компоненты SVG {#all-svg-components}

React поддерживает все встроенные в браузер SVG-компоненты. К ним относятся:

-   [`<a>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/a)
-   [`<animate>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate)
-   [`<animateMotion>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animateMotion)
-   [`<animateTransform>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animateTransform)
-   [`<circle>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/circle)
-   [`<clipPath>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/clipPath)
-   [`<defs>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/defs)
-   [`<desc>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/desc)
-   [`<discard>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/discard)
-   [`<ellipse>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/ellipse)
-   [`<feBlend>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feBlend)
-   [`<feColorMatrix>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feColorMatrix)
-   [`<feComponentTransfer>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feComponentTransfer)
-   [`<feComposite>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feComposite)
-   [`<feConvolveMatrix>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feConvolveMatrix)
-   [`<feDiffuseLighting>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDiffuseLighting)
-   [`<feDisplacementMap>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDisplacementMap)
-   [`<feDistantLight>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDistantLight)
-   [`<feDropShadow>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDropShadow)
-   [`<feFlood>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFlood)
-   [`<feFuncA>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncA)
-   [`<feFuncB>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncB)
-   [`<feFuncG>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncG)
-   [`<feFuncR>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncR)
-   [`<feGaussianBlur>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feGaussianBlur)
-   [`<feImage>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feImage)
-   [`<feMerge>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMerge)
-   [`<feMergeNode>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMergeNode)
-   [`<feMorphology>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMorphology)
-   [`<feOffset>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feOffset)
-   [`<fePointLight>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/fePointLight)
-   [`<feSpecularLighting>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feSpecularLighting)
-   [`<feSpotLight>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feSpotLight)
-   [`<feTile>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTile)
-   [`<feTurbulence>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTurbulence)
-   [`<filter>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/filter)
-   [`<foreignObject>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/foreignObject)
-   [`<g>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/g)
-   `<hatch>`
-   `<hatchpath>`
-   [`<image>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/image)
-   [`<line>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/line)
-   [`<linearGradient>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/linearGradient)
-   [`<marker>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker)
-   [`<mask>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mask)
-   [`<metadata>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/metadata)
-   [`<mpath>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mpath)
-   [`<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/path)
-   [`<pattern>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/pattern)
-   [`<polygon>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polygon)
-   [`<polyline>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polyline)
-   [`<radialGradient>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/radialGradient)
-   [`<rect>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect)
-   [`<script>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/script)
-   [`<set>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/set)
-   [`<stop>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/stop)
-   [`<style>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/style)
-   [`<svg>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/svg)
-   [`<switch>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/switch)
-   [`<symbol>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/symbol)
-   [`<text>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text)
-   [`<textPath>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath)
-   [`<title>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title)
-   [`<tspan>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/tspan)
-   [`<use>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/use)
-   [`<view>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/view)

!!!note "camelCase для имен свойств"

    По аналогии со стандартом [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) React использует соглашение `camelCase` для имен свойств. Например, вы будете писать `tabIndex` вместо `tabindex`. Вы можете преобразовать существующий SVG в JSX с помощью [онлайн-конвертера.](https://transform.tools/)

    Атрибуты с пространством имен также должны быть написаны без двоеточия:

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

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react-dom/components](https://react.dev/reference/react-dom/components)</small>
