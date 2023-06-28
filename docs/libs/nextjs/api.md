# API

## Next CLI

Next CLI позволяет запускать, собирать и экспортировать приложение.

Команда для получения списка доступных команд:

```bash
npx next -h
```

Пример передачи аргументов:

```
NODE_OPTIONS='--throw-deprecation' next
NODE_OPTIONS='-r esm' next
NODE_OPTIONS='--inspect' next
```

### Сборка

Команда `next build` создает оптимизированную производственную сборку приложения. Для каждого роута отображается:

- размер (size) — количество ресурсов, загружаемых при запросе страницы на стороне клиента
- первоначально загружаемый (first load) JS — количество ресурсов, загружаемых при получении страницы от сервера

Флаг `--profile` позволяет включить производственный профайлинг:

```sh
next build --profile
```

Флаг `--verbose` позволяет получить более подробный вывод:

```sh
next build --verbose
```

### Разработка

Команда `next dev` запускает приложение в режиме разработки с быстрой перезагрузкой кода, отчетами об ошибках и т. д.

По умолчанию приложение запускается по адресу `http://localhost:3000`. Порт может быть изменен с помощью флага `-p`:

```sh
npx next dev -p 4000
```

Для этого также можно использовать переменную `PORT`:

```sh
PORT=4000 npx next dev
```

Дефолтный хост (`0.0.0.0`) можно изменить с помощью флага `-H`:

```sh
npx next dev -H 192.168.1.2
```

### Продакшн

Команда `next start` запускает приложение в производственном режиме. Перед этим приложение должно быть скомпилировано с помощью `next build`.

### Линтер

Команда `next lint` запускает ESLint для всех файлов в директориях `pages`, `components` и `lib`. Дополнительные директории для проверки могут быть определены с помощью флага `--dir`:

```sh
next lint --dir utils
```

## Create Next App

CLI `create-next-app` — это простейший способ создать болванку Next-проекта.

```sh
npx create-next-app [app-name]
# or
yarn create next-app [app-name]
```

Или, если вам требуется поддержка TypeScript:

```sh
npx create-next-app [app-name] --typescript
# or
yarn create next-app [app-name] --ts
```

### Настройки

- `--ts`, `--typescript` — инициализация TS-проекта
- `-e`, `--example [example-name][github-url]` — инициализация проекта на основе примера. В URL может быть указана любая ветка и/или поддиректория
- `--example-path [path-to-example]`
- `--use-npm`

### next/router

#### useRouter

Хук `useRouter` позволяет получить доступ к объекту `router` в любом функциональном компоненте:

```js
import { useRouter } from 'next/router';

export const ActiveLink = ({ children, href }) => {
  const router = useRouter();

  const style = {
    marginRight: 10,
    color: router.asPath === href ? 'green' : 'blue',
  };

  const handleClick = (e) => {
    e.preventDefault();
    router.push(href);
  };

  return (
    <a href={href} onClick={handleClick} style={style}>
      {children}
    </a>
  );
};
```

#### Объект router

Объект `router` возвращается `useRouter` и `withRouter` и содержит следующие свойства:

- `pathname: string` — текущий роут, путь страницы из `/pages` без `basePath` или `locale`
- `query: object` — строка запроса, разобранная в объект. По умолчанию имеет значение `{}`
- `asPath: string` — путь (включая строку запроса), отображаемый в браузере, без `basePath` или `locale`
- `isFallback: boolean` — находится ли текущая страница в резервном режиме?
- `basePath: string` — активный базовый путь
- `locale: string` — активная локаль
- `locales: string[]` — поддерживаемые локали
- `defaultLocale: string` — дефолтная локаль
- `domainsLocales: Array<{ domain, defaultLocalem locales }>` — локали для доменов
- `isReady: boolean` — готовы ли поля роутера к использованию? Может использоваться только в `useEffect`
- `isPreview: boolean` — находится ли приложение в режиме предварительного просмотра?

#### router.push

Метод `router.push` предназначен для случаев, когда `next/link` оказывается недостаточно.

```js
router.push(url, as, options);
```

- `url: string | object` — путь для навигации
- `as: string | object` — опциональный декоратор для адреса страницы при отображении в браузере
- `options` — опциональный объект со следующими свойствами:
  - `scroll: boolean` — выполнять ли прокрутку в верхнюю часть области просмотра при переключении страницы? По умолчанию имеет значение `true`
  - `shallow: boolean` — позволяет обновлять путь текущей страницы без использования `getStaticProps`, getServerSideProps или `getInitialProps`. По умолчанию имеет значение `false`
  - `locale: string` — локаль новой страницы

Использование. Переключение на страницу `pages/about.js`:

```js
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  return (
    <button
      className="link"
      onClick={() => router.push('/about')}
    >
      О нас
    </button>
  );
}
```

Переключение на страницу `pages/post/[pid].js`:

```js
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  return (
    <button
      className="link"
      onClick={() => router.push('/post/abc')}
    >
      Подробнее
    </button>
  );
}
```

Перенаправление пользователя на страницу `pages/login.js` (может использоваться для реализации защищенных страниц):

```js
import { useEffect } from 'react';
import { useRouter } from 'next/router';

// Получаем данные пользователя
const useUser = () => ({ user: null, loading: false });

export default function Page() {
  const { user, loading } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading]);

  return user ? (
    <p>Привет, {user.name}!</p>
  ) : (
    <p>Загрузка...</p>
  );
}
```

Пример использования объекта вместо строки:

```js
import { useRouter } from 'next/router';

export default function ReadMore({ post }) {
  const router = useRouter();

  return (
    <button
      className="link"
      onClick={() => {
        router.push({
          pathname: '/post/[pid]',
          query: { pid: post.id },
        });
      }}
    >
      Подробнее
    </button>
  );
}
```

#### router.replace

Метод `router.replace` обновляет путь текущей страницы без добавления URL в стек `history`.

```js
router.replace(url, as, options);
```

Использование

```js
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  return (
    <button
      className="link"
      onClick={() => router.replace('/home')}
    >
      Главная
    </button>
  );
}
```

#### router.prefetch

Метод `router.prefetch` позволяет выполнять предварительную загрузку страниц для ускорения навигации. Обратите внимание: `next/link` выполняет предварительную загрузку страниц автоматически.

```js
router.prefetch(url, as);
```

Использование. Предположим, что после авторизации мы перенаправляем пользователя на страницу профиля. Для ускорения навигации мы можем предварительно загрузить страницу профиля:

```js
import { useCallback, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Login() {
  const router = useRouter();

  const handleSubmit = useCallback((e) => {
    e.preventDefault();

    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        /* Данные пользователя */
      }),
    }).then((res) => {
      // Выполняем перенаправление на предварительно загруженную страницу профиля
      if (res.ok) router.push('/dashboard');
    });
  }, []);

  useEffect(() => {
    // Предварительно загружаем страницу профиля
    router.prefetch('/dashboard');
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      {/* Поля формы */}
      <button type="submit">Войти</button>
    </form>
  );
}
```

#### router.beforePopState

Метод `router.beforePopState` позволяет реагировать на событие `popstate` перед обработкой пути роутером.

```js
router.beforePopState(cb);
```

`cb` — это функция, которая запускается при возникновении события `popstate`. Данная функция получает объект события со следующими свойствами:

- `url: string` — путь для нового состояния (как правило, название страницы)
- `as: string` — URL, который будет отображен в браузере
- `options: object` — дополнительные настройки из `router.push`

Использование. `beforePopState` может использоваться для модификации запроса или принудительного обновления SSR, как в следующем примере:

```js
import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  useEffect(() => {
    router.beforePopState(({ url, as, options }) => {
      // Разрешены только указанные пути
      if (as !== '/' && as !== '/other') {
        // Заставляем `SSR` рендерить страницу 404
        window.location.href = as;
        return false;
      }

      return true;
    });
  }, []);

  return <p>Добро пожаловать!</p>;
}
```

#### router.back

Данный метод позволяет вернуться к предыдущей странице. При его использовании выполняется `window.history.back()`:

```js
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  return (
    <button className="link" onClick={() => router.back()}>
      Назад
    </button>
  );
}
```

#### router.reload

Данный метод перезагружает текущий URL. При его использовании выполняется `window.location.reload()`:

```js
import { useRouter } from 'next/router';

export default function Page() {
  const router = useRouter();

  return (
    <button
      className="link"
      onClick={() => router.reload()}
    >
      Обновить
    </button>
  );
}
```

#### router.events

Использование роутера приводит к возникновению следующих событий:

- `routeChangeStart(url, { shallow })` — возникает в начале обновления роута
- `routeChangeComplete(url, { shallow })` — возникает в конце обновления роута
- `routeChangeError(err, url, { shallow })` — возникает при провале или отмене обновления роута
- `beforeHistoryChange(url, { shallow })` — возникает перед изменением истории браузера
- `hashChangeStart(url, { shallow })` — возникает в начале изменения хеш-части URL (но не самого URL)
- `hashChangeComplete(url, { shallow })` — возникает в конце изменения хеш-части URL (но не самого URL)

Обратите внимание: здесь `url` — это адрес страницы, отображаемый в браузере, включая `basePath`.

Использование

```js
// pages/_app.js
import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url, { shallow }) => {
      console.log(
        `Выполняется переключение на страницу ${url} ${
          shallow ? 'с' : 'без'
        } поверхностной маршрутизации`
      );
    };

    router.events.on('routeChangeStart', handleRouteChange);

    // При размонтировании компонента
    // отписываемся от события с помощью метода `off`
    return () => {
      router.events.off(
        'routeChangeStart',
        handleRouteChange
      );
    };
  }, []);

  return <Component {...pageProps} />;
}
```

#### withRouter

Вместо `useRouter` может использоваться `withRouter`:

```js
import { withRouter } from 'next/router';

function Page({ router }) {
  return <p>{router.pathname}</p>;
}

export default withRouter(Page);
```

#### TypeScript

```js
import React from 'react';
import { withRouter, NextRouter } from 'next/router';

interface WithRouterProps {
  router: NextRouter;
}

interface MyComponentProps extends WithRouterProps {}

class MyComponent extends React.Component<MyComponentProps> {
  render() {
    return <p>{this.props.router.pathname}</p>;
  }
}

export default withRouter(MyComponent);
```

### next/link

Компонент `Link`, экспортируемый из `next/link`, позволяет переключаться между страницами на стороне клиента.

Предположим, что в директории pages содержатся следующие файлы:

```
pages/index.js
pages/about.js
pages/blog/[slug].js
```

Пример навигации по этим страницам:

```js
import Link from 'next/link';

export default function Home() {
  return (
    <ul>
      <li>
        <Link href="/">
          <a>Главная</a>
        </Link>
      </li>
      <li>
        <Link href="/about">
          <a>О нас</a>
        </Link>
      </li>
      <li>
        <Link href="/blog/hello-world">
          <a>Пост</a>
        </Link>
      </li>
    </ul>
  );
}
```

`Link` принимает следующие пропы:

- `href` — путь или URL для навигации. Единственный обязательный проп
- `as` — опциональный декоратор пути, отображаемый в адресной строке браузера
- `passHref` — указывает `Link` передать проп `href` дочернему компоненту. По умолчанию имеет значение `false`
- `prefetch` — предварительная загрузка страницы в фоновом режиме. По умолчанию — `true`. Предварительная загрузка страницы выполняется для любого `Link`, находящегося в области просмотра (изначально или при прокрутке). Предварительная загрузка может быть отключена с помощью `prefetch={false}`. Однако даже в этом случае предварительная загрузка выполняется при наведении курсора на ссылку. Для страниц со статической генерацией загружается JSON-файл для более быстрого переключения страницы. Предварительная загрузка выполняется только в производственном режиме
- `replace` — заменяет текущее состояние истории вместо добавления нового URL в стек. По умолчанию — `false`
- `scroll` — выполнение прокрутки в верхнюю часть области просмотра. По умолчанию — `true`
- `shallow` — обновление пути текущей страницы без перезапуска `getStaticProps`, `getServerSideProps` или `getInitialProps`. По умолчанию — `false`
- `locale` — по умолчанию к пути добавляется активная локаль. `locale` позволяет определить другую локаль. Когда имеет значение `false`, проп `href` должен включать локаль

#### Роут с динамическими сегментами

Пример динамического роута для `pages/blog/[slug].js`:

```js
import Link from 'next/link';

export default function Posts({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link
            href={`/blog/${encodeURIComponent(post.slug)}`}
          >
            <a>{post.title}</a>
          </Link>
        </li>
      ))}
    </ul>
  );
}
```

#### Кастомный компонент — обертка для тега a

Если дочерним компонентом `Link` является кастомный компонент, оборачивающий `a`, `Link` должен иметь проп `passHref`. Это необходимо при использовании таких библиотек как styled-components. Без этого тег `a` не получит атрибут `href`, что негативно скажется на доступности и SEO.

```js
import Link from 'next/link';
import styled from 'styled-components';

// Создаем кастомный компонент, оборачивающий `a`
const RedLink = styled.a`
  color: red;
`;

export default function NavLink({ href, name }) {
  // Добавляем `passHref`
  return (
    <Link href={href} passHref>
      <RedLink>{name}</RedLink>
    </Link>
  );
}
```

#### Функциональный компонент

Если дочерним компонентом `Link` является функция, то кроме `passHref`, необходимо обернуть ее в `React.forwardRef`:

```js
import Link from 'next/link';
import { forwardRef } from 'react';

// `onClick`, `href` и `ref` должны быть переданы DOM-элементу
const MyButton = forwardRef(({ onClick, href }, ref) => {
  return (
    <a href={href} onClick={onClick} ref={ref}>
      Кликни
    </a>
  );
});

export default function Home() {
  return (
    <Link href="/about" passHref>
      <MyButton />
    </Link>
  );
}
```

#### Объект URL

`Link` также принимает объект URL. Данный объект автоматически преобразуется в строку:

```js
import Link from 'next/link';

export default function Home() {
  return (
    <ul>
      <li>
        <Link
          href={{
            pathname: '/about',
            query: { name: 'test' },
          }}
        >
          <a>О нас</a>
        </Link>
      </li>
      <li>
        <Link
          href={{
            pathname: '/blog/[slug]',
            query: { slug: 'my-post' },
          }}
        >
          <a>Пост</a>
        </Link>
      </li>
    </ul>
  );
}
```

В приведенном примере у нас имеются ссылки на:

- предопределенный роут: `/about?name=test`
- динамический роут: `/blog/my-post`

#### Замена URL

```jsx
<Link href="/about" replace>
  <a>О нас</a>
</Link>
```

#### Отключение прокрутки

```jsx
<Link href="/?page=2" scroll={false}>
  <a>Загрузить еще</a>
</Link>
```

### next/image

#### Обязательные пропы

Компонент `Image` принимает следующие обязательные пропы:

- `src` — статически импортированный файл или строка, которая может быть абсолютной ссылкой или относительным путем в зависимости от пропа `loader` или настроек загрузки. При использовании ссылок на внешние ресурсы, эти ресурсы должны быть указаны в разделе `domains` файла `next.config.js`
- `width` — ширина изображения в пикселях: целое число без единицы измерения
- `height` — высота изображения в пикселях: целое число без единицы измерения

#### Опциональные пропы

- `layout` — `intrinsic | fixed | responsive | fill`. Значением по умолчанию является `intrinsic`
- `loader` — кастомная функция для разрешения URL. Установка этого пропа перезаписывает настройки из раздела `images` в `next.config.js`. `loader` принимает параметры `src`, `width` и `quality`

```js
import Image from 'next/image';

const myLoader = ({ src, width, quality }) =>
  `https://example.com/${src}?w=${width}&q=${
    quality || 75
  }`;

const MyImage = (props) => (
  <Image
    loader={myLoader}
    src="me.png"
    alt=""
    role="presentation"
    width={500}
    height={500}
  />
);
```

- `sizes` — строка, содержащая информацию о ширине изображения на различных контрольных точках. По умолчанию имеет значение `100vw` при использовании `layout="responsive"` или `layout="fill"`
- `quality` — качество оптимизированного изображения: целое число от 1 до 100, где 100 — лучшее качество. Значением по умолчанию является 75
- `priority` — если `true`, изображение будет считаться приоритетным и загружаться предварительно. Ленивая загрузка для такого изображения будет отключена
- `placeholder` — заменитель изображения. Возможными значениями являются `blur` и `empty`. Значением по умолчанию является `empty`. Когда значением является `blur`, в качестве заменителя используется значение пропа `blurDataURL`. Если значением `src` является объект из статического импорта и импортированное изображение имеет формат JPG, PNG, WebP или AVIF, `blurDataURL` заполняется автоматически

#### Пропы для продвинутого использования

- `objectFit` — определяет, как изображение заполняет родительский контейнер при использовании `layout="fill"`
- `objectPosition` — определяет, как изображение позиционируется внутри родительского контейнера при использовании `layout="fill"`
- `onLoadingComplete` — функция, которая вызывается после полной загрузки изображения и удаления заменителя
- `lazyBoundary` — строка, определяющая ограничительную рамку для определения пересечения области просмотра с изображением для запуска его ленивой загрузки. По умолчанию имеет значение `200px`
- `unoptimized` — если `true`, источник изображения будет использоваться как есть, без изменения качества, размера или формата. Значением по умолчанию является `false`

#### Другие пропы

Любые другие пропы компонента `Image` передаются дочернему элементу `img`, кроме следующих:

- `style` — для стилизации изображения следует использовать `className`
- `srcSet` — следует использовать размеры устройства
- `ref` — следует использовать onLoadingComplete
- `decoding` — всегда `async`

#### Настройки

Настройки для обработки изображений определяются в файле `next.config.js`.

**Домены**. Настройка доменов для провайдеров изображений позволяет защитить приложение от атак, связанных с внедрением в изображение вредоносного кода.

```js
module.exports = {
  images: {
    domains: ['assets.acme.com'],
  },
};
```

**Размеры устройств**. Настройка `deviceSizes` позволяет определить список контрольных точек для ширины устройств потенциальных пользователей. Эти контрольные точки предназначены для предоставления подходящего изображения при использовании `layout="responsive"` или `layout="fill"`.

```js
// настройки по умолчанию
module.exports = {
  images: {
    deviceSizes: [
      640,
      750,
      828,
      1080,
      1200,
      1920,
      2048,
      3840,
    ],
  },
};
```

**Размеры изображений**. Настройка `imageSizes` позволяет определить размеры изображений в виде списка. Этот список объединяется с массивом размеров устройств для формирования полного перечня размеров для генерации набора источников (`srcset`) изображения.

```js
module.exports = {
  images: {
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

### next/head

Компонент `Head` позволяет добавлять элементы в [`head`](https://hcdev.ru/html/head/) страницы:

```js
import Head from 'next/head';

export default function IndexPage() {
  return (
    <div>
      <Head>
        <title>Заголовок страницы</title>
        <meta
          name="viewport"
          content="initial-scale=1.0, width=device-width"
        />
      </Head>
      <p>Привет, народ!</p>
    </div>
  );
}
```

Проп `key` позволяет дедуплицировать теги:

```js
import Head from 'next/head';

export default function IndexPage() {
  return (
    <div>
      <Head>
        <title>Заголовок страницы</title>
        <meta
          property="og:title"
          content="Заголовок страницы"
          key="title"
        />
      </Head>
      <Head>
        <meta
          property="og:title"
          content="Новый заголовок страницы"
          key="title"
        />
      </Head>
      <p>Привет, народ!</p>
    </div>
  );
}
```

В данном случае будет отрендерен только `<meta property="og:title" content="Новый заголовок страницы" key="title" />`.

Контент `head` удаляется при размонтировании компонента.

`title`, `meta` и другие элементы должны быть прямыми потомками `Head`. Они могут быть обернуты в один `<React.Fragment>` или рендериться из массива.

### next/server

Посредники создаются с помощью функции `middleware`, находящейся в файле `_middleware`. Интерфейс посредников основан на нативных объектах `FetchEvent`, `Response` и `Request`.

Эти нативные объекты расширены для предоставления большего контроля над формированием ответов на основе входящих запросов.

Сигнатура функции:

```js
import type {
  NextRequest,
  NextFetchEvent,
} from 'next/server';

export type Middleware = (
  request: NextRequest,
  event: NextFetchEvent
) => Promise<Response | undefined> | Response | undefined;
```

Функция не обязательно должна называться `middleware`. Это всего лишь соглашение. Функция также не обязательно должна быть асинхронной.

#### NextRequest

Объект `NextRequest` расширяет нативный интерфейс `Request` следующими методами и свойствами:

- `cookies` — куки запроса
- `nextUrl` — расширенный, разобранный объект URL, предоставляющий доступ к таким свойствам, как `pathname`, `basePath`, `trailingSlash` и `i18n`
- `geo` — геоинформация о запросе
- `country` — код страны
- `region` — код региона
- `city` — город
- `latitude` — долгота
- `longitude` — широта
- `ip` — IP-адрес запроса
- `ua` — агент пользователя

`NextRequest` может использоваться вместо `Request`.

```js
import type { NextRequest } from 'next/server';
```

#### NextFetchEvent

`NextFetchEvent` расширяет объект `FetchEvent` методом `waitUntil`.

Данный метод позволяет продолжить выполнение функции после отправки ответа.

Например, `waitUntil` может использоваться для интеграции с такими системами мониторинга ошибок, как `Sentry`.

```js
import type { NextFetchEvent } from 'next/server';
```

#### NextResponse

`NextResponse` расширяет `Response` следующими методами и свойствами:

- `cookies` — куки ответа
- `redirect()` — возвращает `NextResponse` с набором перенаправлений (`redirects`)
- `rewrite()` — возвращает `NextResponse` с набором перезаписей (`rewrites`)
- `next()` — возвращает `NextResponse`, который является частью цепочки посредников

```js
import { NextResponse } from 'next/server';
```
