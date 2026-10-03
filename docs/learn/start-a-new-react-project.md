---
description: Если вы хотите создать новое приложение или сайт на React, мы рекомендуем начать с фреймворка
---

# Создание приложения React

<big>

Если вы хотите создать новое приложение или сайт на React, мы рекомендуем начать с фреймворка.

</big>

Если у вашего приложения есть ограничения, которые плохо покрываются существующими фреймворками, вы предпочитаете создать собственный фреймворк или просто хотите изучить основы приложения React, вы можете [собрать приложение React с нуля](build-a-react-app-from-scratch.md).

<a id="production-grade-react-frameworks"></a>
<a id="bleeding-edge-react-frameworks"></a>

## Полностековые фреймворки {#full-stack-frameworks}

Эти рекомендуемые фреймворки поддерживают все возможности, которые нужны, чтобы развернуть приложение в производственной среде и масштабировать его. В них интегрированы новейшие возможности React, и они используют архитектуру React.

!!!note "Полностековым фреймворкам не нужен сервер."

    Все фреймворки на этой странице поддерживают клиентский рендеринг ([CSR](https://developer.mozilla.org/en-US/docs/Glossary/CSR)), одностраничные приложения ([SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA)) и генерацию статических сайтов ([SSG](https://developer.mozilla.org/en-US/docs/Glossary/SSG)). Такие приложения можно развернуть на [CDN](https://developer.mozilla.org/en-US/docs/Glossary/CDN) или сервисе статического хостинга без сервера. Кроме того, эти фреймворки позволяют добавить серверный рендеринг для отдельных маршрутов, когда это имеет смысл для вашего сценария.

    Это позволяет начать с приложения только на клиенте, а если позже потребности изменятся, вы сможете подключить серверные возможности на отдельных маршрутах, не переписывая приложение. О том, как настроить стратегию рендеринга, смотрите в документации вашего фреймворка.

### Next.js (App Router) {#nextjs-app-router}

**[App Router в Next.js](https://nextjs.org/docs) — это фреймворк React, который полностью использует архитектуру React и позволяет создавать полностековые приложения React.**

```sh linenums="0"
npx create-next-app@latest
```

Next.js поддерживается компанией [Vercel](https://vercel.com/). Вы можете [развернуть приложение Next.js](https://nextjs.org/docs/app/building-your-application/deploying) у любого хостинг-провайдера, который поддерживает Node.js или контейнеры Docker, или на собственном сервере. Next.js также поддерживает [статический экспорт](https://nextjs.org/docs/app/building-your-application/deploying/static-exports), которому не нужен сервер.

### React Router (v7) {#react-router-v7}

**[React Router](https://reactrouter.com/start/framework/installation) — самая популярная библиотека маршрутизации для React, и в паре с Vite она может стать полностековым фреймворком React**. Она опирается на стандартные веб-API и предлагает несколько [готовых к развёртыванию шаблонов](https://github.com/remix-run/react-router-templates) для разных сред выполнения JavaScript и платформ.

Чтобы создать новый проект на фреймворке React Router, выполните:

```sh linenums="0"
npx create-react-router@latest
```

React Router поддерживается компанией [Shopify](https://www.shopify.com).

### Expo (для нативных приложений) {#expo}

**[Expo](https://expo.dev/) — это фреймворк React, который позволяет создавать универсальные приложения для Android, iOS и веба с по-настоящему нативным интерфейсом.** Он предоставляет SDK для [React Native](https://reactnative.dev/), который упрощает использование нативных частей. Чтобы создать новый проект Expo, выполните:

```sh linenums="0"
npx create-expo-app@latest
```

Если вы новичок в Expo, посмотрите [учебник Expo](https://docs.expo.dev/tutorial/introduction/).

Expo поддерживается [Expo (компанией)](https://expo.dev/about). Создание приложений с помощью Expo бесплатно, и вы можете отправлять их в магазины приложений Google и Apple без ограничений. Expo дополнительно предоставляет платные облачные сервисы по желанию.

## Другие фреймворки {#other-frameworks}

Есть и другие перспективные фреймворки, которые движутся к нашему видению полностековой архитектуры React:

- [TanStack Start (Beta)](https://tanstack.com/start/): TanStack Start — полностековый фреймворк React на базе TanStack Router. Он даёт SSR всего документа, потоковую передачу, серверные функции, сборку бандла и другое с помощью таких инструментов, как Nitro и Vite.
- [RedwoodSDK](https://rwsdk.com/): Redwood — полностековый фреймворк React с большим количеством предустановленных пакетов и настроек, которые упрощают создание полностековых веб-приложений.

??? note "Какие возможности составляют видение полностековой архитектуры команды React?"

    Бандлер App Router в Next.js полностью реализует официальную [спецификацию React Server Components](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md). Это позволяет смешивать компоненты времени сборки, только серверные и интерактивные компоненты в одном дереве React.

    Например, можно написать только серверный компонент React как функцию `async`, которая читает данные из базы или из файла. Затем из него можно передать данные интерактивным компонентам:

    ```js
    // This component runs *only* on the server (or during the build).
    async function Talks({ confId }) {
      // 1. You're on the server, so you can talk to your data layer. API endpoint not required.
      const talks = await db.Talks.findAll({ confId });

      // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.
      const videos = talks.map(talk => talk.video);

      // 3. Pass the data down to the components that will run in the browser.
      return <SearchableVideoList videos={videos} />;
    }
    ```

    App Router в Next.js также объединяет [получение данных с Suspense](https://react.dev/blog/2022/03/29/react-v18#suspense-in-data-frameworks). Это позволяет задать состояние загрузки (например, скелетон-заполнитель) для разных частей интерфейса прямо в дереве React:

    ```js
    <Suspense fallback={<TalksLoading />}>
      <Talks confId={conf.id} />
    </Suspense>
    ```

    Серверные компоненты и Suspense — это возможности React, а не возможности Next.js. Однако их внедрение на уровне фреймворка требует согласия и нетривиальной реализации. На данный момент App Router в Next.js — самая полная реализация. Команда React работает с разработчиками бандлеров, чтобы эти возможности было проще реализовать в следующем поколении фреймворков.

## Начало с нуля {#start-from-scratch}

Если у вашего приложения есть ограничения, которые плохо покрываются существующими фреймворками, вы предпочитаете создать собственный фреймворк или просто хотите изучить основы приложения React, есть и другие варианты начать проект React с нуля.

Начало с нуля даёт больше гибкости, но требует, чтобы вы сами выбирали инструменты для маршрутизации, получения данных и других типичных сценариев. Это очень похоже на создание собственного фреймворка вместо использования уже существующего. У [рекомендуемых нами фреймворков](#full-stack-frameworks) есть встроенные решения этих задач.

Если вы хотите строить собственные решения, смотрите руководство [Сборка приложения React с нуля](build-a-react-app-from-scratch.md): там описано, как настроить новый проект React, начиная с инструмента сборки вроде [Vite](https://vite.dev/), [Parcel](https://parceljs.org/) или [RSbuild](https://rsbuild.dev/).

-----

_Если вы автор фреймворка и хотите, чтобы его включили на эту страницу, [дайте нам знать](https://github.com/reactjs/react.dev/issues/new?assignees=&labels=type%3A+framework&projects=&template=3-framework.yml&title=%5BFramework%5D%3A+)._

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/creating-a-react-app](https://react.dev/learn/creating-a-react-app)</small>
