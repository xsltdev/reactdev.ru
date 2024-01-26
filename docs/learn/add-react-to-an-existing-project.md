---
description: Если вы хотите добавить интерактивности в существующий проект, вам не нужно переписывать его на React
---

# Добавление React в проект

<big>Если вы хотите добавить интерактивности в существующий проект, вам не нужно переписывать его на React. Добавьте React к существующему стеку и выводите интерактивные компоненты React в любом месте.</big>

!!!note "Для локальной разработки необходимо установить Node.js."

    Хотя вы можете [попробовать React](installation.md) онлайн или с помощью простой HTML-страницы, в реальности большинство инструментов JavaScript, которые вы захотите использовать для разработки, требуют Node.js.

## Использование React для целого подмаршрута существующего сайта {#using-react-for-an-entire-subroute-of-your-existing-website}

Допустим, у вас есть существующее веб-приложение по адресу `example.com`, построенное на другой серверной технологии (например, Rails), и вы хотите реализовать все маршруты, начинающиеся с `example.com/some-app/`, полностью с помощью React.

Вот как мы рекомендуем это сделать:

1.  **Создайте React-часть вашего приложения**, используя один из [React-based frameworks](start-a-new-react-project.md).
2.  **Укажите `/some-app` в качестве _базового пути_** в конфигурации вашего фреймворка (вот как: [Next.js](https://nextjs.org/docs/api-reference/next.config.js/basepath), [Gatsby](https://www.gatsbyjs.com/docs/how-to/previews-deploys-hosting/path-prefix/)).
3.  **Настройте ваш сервер или прокси** так, чтобы все запросы по адресу `/some-app/` обрабатывались вашим React-приложением.

Это гарантирует, что React-часть вашего приложения сможет [воспользоваться лучшими практиками](start-a-new-react-project.md), заложенными в эти фреймворки.

Многие фреймворки на основе React являются полнофункциональными и позволяют вашему React-приложению использовать преимущества сервера. Однако вы можете использовать тот же подход, даже если вы не можете или не хотите запускать JavaScript на сервере. В этом случае вместо этого обслуживайте экспорт HTML/CSS/JS ([`next export` output](https://nextjs.org/docs/advanced-features/static-html-export) для Next.js, по умолчанию для Gatsby) в `/some-app/`.

## Использование React для части существующей страницы {#using-react-for-a-part-of-your-existing-page}

Допустим, у вас есть существующая страница, построенная на другой технологии (либо серверной, как Rails, либо клиентской, как Backbone), и вы хотите отобразить интерактивные компоненты React где-то на этой странице. Это распространенный способ интеграции React — фактически, именно так большинство пользователей React смотрели на Meta в течение многих лет!

Вы можете сделать это в два шага:

1.  **Установите среду JavaScript**, которая позволяет вам использовать [JSX синтаксис](writing-markup-with-jsx.md), разделить ваш код на модули с помощью синтаксиса [`import`](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Statements/import) / [`export`](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Statements/export), и использовать пакеты (например, React) из реестра пакетов [npm](https://www.npmjs.com/).
2.  **Рендерите ваши компоненты React** там, где вы хотите видеть их на странице.

Точный подход зависит от существующей настройки страницы, поэтому давайте рассмотрим некоторые детали.

### Шаг 1: Создайте модульную среду JavaScript {#step-1-set-up-a-modular-javascript-environment}

Модульная среда JavaScript позволяет писать компоненты React в отдельных файлах, в отличие от написания всего кода в одном файле. Она также позволяет использовать все замечательные пакеты, опубликованные другими разработчиками в реестре [npm](https://www.npmjs.com/) — включая сам React! Как вы это сделаете, зависит от вашей существующей настройки:

-   Если ваше приложение уже разбито на файлы, использующие операторы `import`, попробуйте использовать уже имеющуюся настройку. Проверьте, не приводит ли написание `<div />` в вашем JS-коде к синтаксической ошибке. Если это приводит к синтаксической ошибке, вам может понадобиться [преобразовать ваш JavaScript код с помощью Babel](https://babeljs.io/setup), и включить [предустановку Babel React](https://babeljs.io/docs/babel-preset-react) для использования JSX.

-   Если в вашем приложении нет существующей настройки для компиляции модулей JavaScript, установите ее с помощью [Vite](https://vitejs.dev/). Сообщество Vite поддерживает [множество интеграций с бэкенд-фреймворками](https://github.com/vitejs/awesome-vite#integrations-with-backends), включая Rails, Django и Laravel. Если вашего бэкенд-фреймворка нет в списке, [следуйте этому руководству](https://vitejs.dev/guide/backend-integration.html), чтобы вручную интегрировать сборки Vite с вашим бэкендом.

Чтобы проверить, работает ли ваша настройка, выполните эту команду в папке проекта:

```sh linenums="0"
npm install react react-dom
```

Затем добавьте эти строки кода в начало вашего основного файла JavaScript (он может называться `index.js` или `main.js`):

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';

    // Clear the existing HTML content
    document.body.innerHTML = '<div id="app"></div>';

    // Render your React component instead
    const root = createRoot(document.getElementById('app'));
    root.render(<h1>Hello, world</h1>);
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/dnz4rx?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Если все содержимое вашей страницы заменить на "Привет, мир!", все заработает!

### Шаг 2: Рендеринг компонентов React в любом месте страницы {#step-2-render-react-components-anywhere-on-the-page}

В предыдущем шаге вы поместили этот код в начало вашего основного файла:

```js
import { createRoot } from 'react-dom/client';

// Clear the existing HTML content
document.body.innerHTML = '<div id="app"></div>';

// Render your React component instead
const root = createRoot(document.getElementById('app'));
root.render(<h1>Hello, world</h1>);
```

Конечно, на самом деле вы не хотите очищать существующий HTML-контент!

Удалите этот код.

Вместо этого вы, вероятно, хотите отобразить компоненты React в определенных местах HTML. Откройте вашу HTML-страницу (или шаблоны сервера, которые ее генерируют) и добавьте уникальный атрибут [`id`](https://developer.mozilla.org/ru/docs/Web/HTML/Global_attributes/id) к любому тегу, например:

```html
<!-- ... somewhere in your html ... -->
<nav id="navigation"></nav>
<!-- ... more html ... -->
```

Это позволит вам найти этот элемент HTML с помощью [`document.getElementById`](https://developer.mozilla.org/ru/docs/Web/API/Document/getElementById) и передать его в `createRoot`, чтобы вы могли создать внутри него свой собственный компонент React:

=== "index.js"

    ```js
    import { createRoot } from 'react-dom/client';

    function NavigationBar() {
    	// TODO: Actually implement a navigation bar
    	return <h1>Hello from React!</h1>;
    }

    const domNode = document.getElementById('navigation');
    const root = createRoot(domNode);
    root.render(<NavigationBar />);
    ```

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    	<head>
    		<title>My app</title>
    	</head>
    	<body>
    		<p>This paragraph is a part of HTML.</p>
    		<nav id="navigation"></nav>
    		<p>This paragraph is also a part of HTML.</p>
    	</body>
    </html>
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/vnljk3?view=Editor+%2B+Preview&module=%2Fpublic%2Findex.html" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev (forked)" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что оригинальное содержимое HTML из `index.html` сохраняется, но ваш собственный React-компонент `NavigationBar` теперь появляется внутри `<nav id="navigation">` из вашего HTML. Прочитайте документацию по использованию `createRoot`, чтобы узнать больше о рендеринге компонентов React внутри существующей HTML-страницы.

Когда вы внедряете React в существующий проект, обычно начинают с небольших интерактивных компонентов (например, кнопок), а затем постепенно продолжают "двигаться вверх", пока в конечном итоге вся ваша страница не будет построена на React. Если вы когда-нибудь достигнете этого момента, мы рекомендуем сразу после этого перейти на [фреймворк React](start-a-new-react-project.md), чтобы получить максимальную отдачу от React.

## Использование React Native в существующем нативном мобильном приложении {#using-react-native-in-an-existing-native-mobile-app}

[React Native](https://reactnative.dev/) также может быть интегрирован в существующие нативные приложения постепенно. Если у вас есть существующее нативное приложение для Android (Java или Kotlin) или iOS (Objective-C или Swift), [следуйте этому руководству](https://reactnative.dev/docs/integration-with-existing-apps), чтобы добавить в него экран React Native.

:material-information-outline: Источник &mdash; [https://react.dev/learn/add-react-to-an-existing-project](https://react.dev/learn/add-react-to-an-existing-project)
