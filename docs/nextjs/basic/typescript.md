# TypeScript

Next.js поддерживает TypeScript из коробки:

```bash
yarn create next-app --typescript app-name
# или
yarn create next-app --ts app-name
```

Для `getStaticProps`, `getStaticPaths` и `getServerSideProps` существуют специальные типы `GetStaticProps`, `GetStaticPaths` и `GetServerSideProps`:

```ts
import {
  GetStaticProps,
  GetStaticPaths,
  GetServerSideProps,
} from 'next';

export const getStaticProps: GetStaticProps = async (
  context
) => {
  // ...
};

export const getStaticPaths: GetStaticPaths = async () => {
  // ...
};

export const getServerSideProps: GetServerSideProps = async (
  context
) => {
  // ...
};
```

Пример использования встроенных типов для интерфейса маршрутизации (API Routes):

```ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default (
  req: NextApiRequest,
  res: NextApiResponse
) => {
  res.status(200).json({ message: 'Привет!' });
};
```

Ничто не мешает нам типизировать данные, содержащиеся в ответе:

```ts
import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
  name: string;
};

export default (
  req: NextApiRequest,
  res: NextApiResponse<Data>
) => {
  res.status(200).json({ message: 'Пока!' });
};
```

Для кастомного приложения существует специальный тип `AppProps`:

```ts
// import App from 'next/app'
import type { AppProps /*, AppContext */ } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

// Данный метод следует использовать только в случае, когда все страницы приложения
// должны предварительно рендериться на сервере
MyApp.getInitialProps = async (context: AppContext) => {
  // вызывает функцию `getInitialProps`, определенную на странице
  // и заполняет `appProps.pageProps`
  const props = await App.getInitialProps(context);

  return { ...props };
};
```

Next.js поддерживает настройки `paths` и `baseUrl`, определяемые в `tsconfig.json`.
