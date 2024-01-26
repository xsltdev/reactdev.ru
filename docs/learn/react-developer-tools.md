---
description: Используйте React Developer Tools для проверки React components, редактирования props и state и выявления проблем производительности
---

# React Developer Tools

<big>Используйте React Developer Tools для проверки React [компонент](your-first-component.md), редактирования [свойств](passing-props-to-a-component.md) и [состояния](state-a-components-memory.md) и выявления проблем производительности.</big>

!!!tip "Вы узнаете"

    -   Как установить React Developer Tools

## Расширение для браузера {#browser-extension}

Самый простой способ отладки веб-сайтов, созданных с помощью React, - установить расширение для браузера React Developer Tools. Оно доступно для нескольких популярных браузеров:

-   [Установить для **Chrome**](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en)
-   [Установить для **Firefox**](https://addons.mozilla.org/ru/firefox/addon/react-devtools/)
-   [Установить для **Edge**](https://microsoftedge.microsoft.com/addons/detail/react-developer-tools/gpphkfbcpidddadnkolkpfckpihlkkil)

Теперь, если вы посетите сайт, **построенный с помощью React,** вы увидите панели _Components_ и _Profiler_.

![Расширение React Developer Tools](react-devtools-extension.png)

### Safari и другие браузеры {#safari-and-other-browsers}

Для других браузеров (например, Safari) установите пакет npm [`react-devtools`](https://www.npmjs.com/package/react-devtools):

```bash linenums="0"
# Yarn
yarn global add react-devtools

# Npm
npm install -g react-devtools
```

Затем откройте инструменты разработчика из терминала:

```bash linenums="0"
react-devtools
```

Затем подключите свой сайт, добавив следующий тег `<script>` в начало `<head>` вашего сайта:

```html
<html>
    <head>
        <script src="http://localhost:8097"></script>
    </head>
</html>
```

Перезагрузите свой сайт в браузере, чтобы просмотреть его в инструментах разработчика.

![React Developer Tools standalone](react-devtools-standalone.png)

## Мобильные устройства (React Native) {#mobile-react-native}

React Developer Tools можно использовать и для проверки приложений, созданных с помощью [React Native](https://reactnativedev.ru/).

Самый простой способ использовать React Developer Tools - установить его глобально:

```bash linenums="0"
# Yarn
yarn global add react-devtools

# Npm
npm install -g react-devtools
```

Затем откройте инструменты разработчика из терминала.

```bash linenums="0"
react-devtools
```

Он должен подключиться к любому локальному запущенному приложению React Native.

!!!note "Решение проблем"

    Попробуйте перезагрузить приложение, если инструменты разработчика не подключаются через несколько секунд.

    [Подробнее об отладке React Native.](https://reactnative.dev/docs/debugging)

:material-information-outline: Источник &mdash; [https://react.dev/learn/react-developer-tools](https://react.dev/learn/react-developer-tools)
