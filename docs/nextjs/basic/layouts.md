# Макеты (Layouts)

Разработка React-приложения предполагает разделение страницы на отдельные компоненты. Многие компоненты используются на нескольких страницах. Предположим, что на каждой странице используется панель навигации и подвал:

```js
// components/layout.js
import Navbar from './navbar';
import Footer from './footer';

export default function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  );
}
```

## Примеры

### Единственный макет

Если в приложении используется только один макет, мы можем создать кастомное приложение (custom app) и обернуть приложение в макет. Поскольку компонент-макет будет переиспользоваться при изменении страниц, его состояние (например, значения инпутов) будет сохраняться:

```js
// pages/_app.js
import Layout from '../components/layout';

export default function App({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}
```

### Макеты на уровне страниц

Свойство `getLayout` страницы позволяет возвращать компонент для макета. Это позволяет определять макеты на уровне страниц. Возвращаемая функция позволяет конструировать вложенные макеты:

```js
// pages/index.js
import Layout from '../components/layout';
import Nested from '../components/nested';

export default function Page() {
  return {
    // ...
  };
}

Page.getLayout = (page) => (
  <Layout>
    <Nested>{page}</Nested>
  </Layout>
);
```

```js
// pages/_app.js
export default function App({ Component, pageProps }) {
  // использовать макет, определенный на уровне страницы, при наличии такового
  const getLayout = Component.getLayout || ((page) => page);

  return getLayout(<Component {...pageProps} />);
}
```

При переключении страниц состояние каждой из них (значения инпутов, позиция прокрутки и т. п.) будет сохраняться.

### Использование с TypeScript

При использовании TypeScript сначала создается новый тип для страницы, включающей `getLayout`. Затем следует создать новый тип для `AppProps`, который перезаписывает свойство `Component` для обеспечения возможности использования созданного ранее типа:

```ts
// pages/index.tsx
import type { ReactElement } from 'react';
import Layout from '../components/layout';
import Nested from '../components/nested';

export default function Page() {
  return {
    // ...
  };
}

Page.getLayout = (page: ReactElement) => (
  <Layout>
    <Nested>{page}</Nested>
  </Layout>
);
```

```ts
// pages/_app.tsx
import type { ReactElement, ReactNode } from 'react';
import type { NextPage } from 'next';
import type { AppProps } from 'next/app';

type NextPageWithLayout = NextPage & {
  getLayout?: (page: ReactElement) => ReactNode;
};

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
};

export default function App({
  Component,
  pageProps,
}: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((page) => page);

  return getLayout(<Component {...pageProps} />);
}
```

### Получение данных

Данные в макете можно получать на стороне клиента с помощью `useEffect` или утилит вроде `SWR`. Поскольку макет — это не страница, в нем в настоящее время нельзя использовать `getStaticProps` или `getServerSideProps`:

```js
import useSWR from 'swr';
import Navbar from './navbar';
import Footer from './footer';

export default function Layout({ children }) {
  const { data, error } = useSWR('/data', fetcher);

  if (error) return <div>Ошибка</div>;
  if (!data) return <div>Загрузка...</div>;

  return (
    <>
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  );
}
```
