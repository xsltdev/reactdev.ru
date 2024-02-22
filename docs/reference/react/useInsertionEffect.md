---
description: useInsertionEffect - это версия useEffect, которая срабатывает перед любыми мутациями DOM
---

# useInsertionEffect

!!!warning "CSS-in-JS"

    `useInsertionEffect` предназначен для авторов библиотек CSS-in-JS. Если вы не работаете над библиотекой CSS-in-JS и вам нужно место для вставки стилей, вам, вероятно, лучше использовать [`useEffect`](useEffect.md) или [`useLayoutEffect`](useLayoutEffect.md).

<big>**`useInsertionEffect`** - это версия [`useEffect`](useEffect.md), которая срабатывает перед любыми мутациями DOM.</big>

```js
useInsertionEffect(setup, dependencies?)
```

## Описание {#reference}

### `useInsertionEffect(setup, dependencies?)` {#useinsertioneffect}

Вызывает `useInsertionEffect` для вставки стилей перед любыми мутациями DOM:

```js
import { useInsertionEffect } from 'react';

// Inside your CSS-in-JS library
function useCSS(rule) {
    useInsertionEffect(() => {
        // ... inject <style> tags here ...
    });
    return rule;
}
```

#### Параметры {#parameters}

-   `setup`: Функция с логикой вашего Эффекта. Ваша функция настройки может также возвращать функцию _cleanup_. Прежде чем ваш компонент будет добавлен в DOM, React запустит вашу функцию настройки. После каждого повторного рендеринга с измененными зависимостями React будет сначала запускать функцию очистки (если вы ее предоставили) со старыми значениями, а затем запускать вашу функцию настройки с новыми значениями. Прежде чем ваш компонент будет удален из DOM, React запустит вашу функцию очистки.
-   **опционально** `dependencies`: Список всех реактивных значений, на которые ссылается код `setup`. Реактивные значения включают props, state, а также все переменные и функции, объявленные непосредственно в теле вашего компонента. Если ваш линтер [настроен на React](../../learn/editor-setup.md), он проверит, что каждое реактивное значение правильно указано в качестве зависимости. Список зависимостей должен иметь постоянное количество элементов и быть написан inline по типу `[dep1, dep2, dep3]`. React будет сравнивать каждую зависимость с предыдущим значением, используя алгоритм сравнения [`Object.is`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is). Если вы не укажете зависимости вообще, ваш Effect будет запускаться заново после каждого повторного рендеринга компонента.

#### Возврат {#returns}

`useInsertionEffect` возвращает `undefined`.

#### Ограничения {#caveats}

-   Эффекты запускаются только на клиенте. Они не выполняются во время рендеринга на сервере.
-   Вы не можете обновлять состояние внутри `useInsertionEffect`.
-   К моменту запуска `useInsertionEffect`, ссылки еще не прикреплены, и DOM еще не обновлен.

## Использование {#usage}

### Вставка динамических стилей из библиотек CSS-in-JS {#injecting-dynamic-styles-from-css-in-js-libraries}

Традиционно для стилизации компонентов React используется обычный CSS.

```js
// In your JS file:
<button className="success" />

// In your CSS file:
.success { color: green; }
```

Некоторые команды предпочитают создавать стили непосредственно в коде JavaScript вместо написания файлов CSS. Для этого обычно требуется использование библиотеки CSS-in-JS или инструмента. Существует три распространенных подхода к CSS-in-JS:

1.  Статическое извлечение в CSS-файлы с помощью компилятора
2.  Встроенные стили, например, `<div style={{ opacity: 1 }}>`
3.  Инъекция тегов `<style>` во время выполнения

Если вы используете CSS-in-JS, мы рекомендуем использовать комбинацию первых двух подходов (CSS-файлы для статических стилей, инлайн-стили для динамических стилей). **Мы не рекомендуем использовать инъекцию тегов `<style>` во время выполнения по двум причинам:**

1.  Инъекция во время выполнения заставляет браузер пересчитывать стили гораздо чаще.
2.  Инъекция во время выполнения может быть очень медленной, если она происходит в неправильное время в жизненном цикле React.

Первая проблема не решаема, но `useInsertionEffect` поможет вам решить вторую проблему.

Вызовите `useInsertionEffect`, чтобы вставить стили до любых мутаций DOM:

```js hl_lines="4-15"
// Inside your CSS-in-JS library
let isInserted = new Set();
function useCSS(rule) {
    useInsertionEffect(() => {
        // As explained earlier, we don't recommend
        // runtime injection of <style> tags.
        // But if you have to do it, then it's important
        // to do in useInsertionEffect.
        if (!isInserted.has(rule)) {
            isInserted.add(rule);
            document.head.appendChild(
                getStyleForRule(rule)
            );
        }
    });
    return rule;
}

function Button() {
    const className = useCSS('...');
    return <div className={className} />;
}
```

Как и `useEffect`, `useInsertionEffect` не запускается на сервере. Если вам нужно узнать, какие правила CSS были использованы на сервере, вы можете сделать это во время рендеринга:

```js hl_lines="1 4-6"
let collectedRulesSet = new Set();

function useCSS(rule) {
    if (typeof window === 'undefined') {
        collectedRulesSet.add(rule);
    }
    useInsertionEffect(() => {
        // ...
    });
    return rule;
}
```

Подробнее об [обновлении библиотек CSS-in-JS с runtime injection до `useInsertionEffect`.](https://github.com/reactwg/react-18/discussions/110)

!!!info "Чем это лучше, чем внедрение стилей во время рендеринга или `useLayoutEffect`?"

    Если вы вставляете стили во время рендеринга, а React обрабатывает [неблокирующее обновление](useTransition.md#marking-a-state-update-as-a-non-blocking-transition), браузер будет пересчитывать стили каждый кадр при рендеринге дерева компонентов, что может быть **экстремально медленным.**.

    `useInsertionEffect` лучше, чем вставка стилей во время [`useLayoutEffect`](useLayoutEffect.md) или [`useEffect`](useEffect.md), потому что это гарантирует, что к моменту запуска других Эффектов в ваших компонентах теги `<style>` уже будут вставлены. В противном случае расчеты компоновки в обычных Эффектах были бы неверными из-за устаревших стилей.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)</small>
