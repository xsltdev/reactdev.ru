# Получение данных (Data Fetching)

Существует 3 функции для получения данных, необходимых для предварительного рендеринга:

- `getStaticProps` (SSG): получение данных во время сборки
- `getStaticPaths` (SSG): определение динамических роутов для предварительного рендеринга страниц на основе данных
- `getServerSideProps` (SSR): получение данных при каждом запросе

## getStaticProps

Страница, на которой экспортируется асинхронная функция `getStaticProps`, предварительно рендерится с помощью возвращаемых этой функцией пропсов.

```js
export async function getStaticProps(context) {
  return {
    props: {},
  };
}
```

`context` — это объект со следующими свойствами:

- `params` — параметры роута для страниц с динамической маршрутизацией. Например, если названием страницы является `[id].js`, params будет иметь вид `{ id: ... }`
- `preview` — имеет значение true, если страница находится в режиме предварительного просмотра
- `previewData` — набор данных, установленный с помощью `setPreviewData`
- `locale` — текущая локаль (если включено)
- `locales` — поддерживаемые локали (если включено)
- `defaultLocale` — дефолтная локаль (если включено)

`getStaticProps` возвращает объект со следующими свойствами:

- `props` — опциональный объект с пропами для страницы
- `revalidate` — опциональное количество секунд, по истечении которых происходит повторная генерация страницы. По умолчанию имеет значение `false` — повторная генерация выполняется только при следующей сборке
- `notFound` — опциональное логическое значение, позволяющее вернуть статус 404 и соответствующую страницу, например:

```js
export async function getStaticProps(context) {
  const res = await fetch('/data');
  const data = await res.json();

  if (!data) {
    return {
      notFound: true,
    };
  }

  return {
    props: {
      data,
    },
  };
}
```

!!! info "Обратите внимание"

    `notFound` не требуется в режиме `fallback: false`, поскольку в этом режиме предварительно рендерятся только пути, возвращаемые `getStaticPaths`.

    Также обратите внимание, что `notFound: true` означает возврат 404 даже в случае, если предыдущая страница была успешно сгенерирована. Это рассчитано на поддержку случаев удаления пользовательского контента.

- `redirect` — опциональный объект, позволяющий выполнять перенаправления на внутренние и внешние ресурсы, который должен иметь форму `{ destination: string, permanent: boolean }`:

```js
export async function getStaticProps(context) {
  const res = await fetch('/data');
  const data = await res.json();

  if (!data) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
      },
    };
  }

  return {
    props: {
      data,
    },
  };
}
```

!!! warning ""

    Замечание 1: в настоящее время перенаправления во время сборки не разрешаются. Такие перенаправления должны быть добавлены в `next.config.js`.

    Замечание 2: модули, импортируемые на верхнем уровне для использования в `getStaticProps`, не включаются в клиентскую сборку. Это означает, что серверный код, включая операции чтения из файловой системы или из базы данных, можно писать прямо в `getStaticProps`.

    Замечание 3: `fetch()` в `getStaticProps` следует использовать только при получении ресурсов из внешних источников.

Случаи использования:

- данные для рендеринга доступны во время сборки и не зависят от запроса пользователя
- данные приходят из безголовой (headless) CMS
- данные могут быть кешированы в открытом виде (не предназначены для конкретного пользователя)
- страница должна быть предварительно отрендерена (для SEO) и при этом должна быть очень быстрой — `getStaticProps` генерирует HTML и JSON файлы, которые могут быть кешированы с помощью CDN

Использование с TypeScript

```ts
import { GetStaticProps } from 'next';

export const getStaticProps: GetStaticProps = async (
  context
) => {};
```

Для получения предполагаемых типов для пропов следует использовать `InferGetStaticPropsType<typeof getStaticProps>`:

```ts
import { InferGetStaticPropsType } from 'next';

type Post = {
  author: string;
  content: string;
};

export const getStaticProps = async () => {
  const res = await fetch('/posts');
  const posts: Post[] = await res.json();

  return {
    props: {
      posts,
    },
  };
};

export default function Blog({
  posts,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  // посты будут иметь тип `Post[]`
}
```

### Инкрементальная статическая регенерация

Статические страницы можно обновлять после сборки приложения. Инкрементальная статическая регенерация позволяет использовать статическую генерацию на уровне отдельных страниц без необходимости повторной сборки всего проекта.

Пример:

```js
const Blog = ({ posts }) => (
  <ul>
    {posts.map((post) => (
      <li>{post.title}</li>
    ))}
  </ul>
);

// Данная функция вызывается во время сборки на сервере.
// Она может вызываться повторно как бессерверная функция
// при включенной инвалидации и поступлении нового запроса
export async function getStaticProps() {
  const res = await fetch('/posts');
  const posts = await res.json();

  return {
    props: {
      posts,
    },
    // `Next.js` попытается регенерировать страницу:
    // - при поступлении нового запроса
    // - как минимум, один раз каждые 10 секунд
    revalidate: 10, // в секундах
  };
}

// Данная функция вызывается во время сборки на сервере.
// Она может вызываться повторно как бессерверная функция
// если путь не был сгенерирован предварительно
export async function getStaticPaths() {
  const res = await fetch('/posts');
  const posts = await res.json();

  // Получаем пути для предварительного рендеринга на основе постов
  const paths = posts.map((post) => ({
    params: { id: post.id },
  }));

  // Только эти пути будут предварительно отрендерены во время сборки
  // `{ fallback: 'blocking' }` будет рендерить страницы на сервере
  // при отсутствии соответствующего пути
  return { paths, fallback: 'blocking' };
}

export default Blog;
```

При запросе страницы, которая была предварительно отрендерена во время сборки, отображается кешированная страница.

- Ответ на любой запрос к такой странице до истечения 10 секунд также мгновенно возвращается из кеша
- По истечении 10 секунд следующий запрос также получает в ответ кешированную версию страницы
- После этого в фоновом режиме запускается регенерация страницы
- После успешной регенерации кеш инвалидируется и отображается новая страница. При провале регенерации старая страница остается неизменной

### Чтение файлов

Для получения абсолютного пути к текущей рабочей директории следует использовать `process.cwd()`:

```js
import { promises as fs } from 'fs';
import { join } from 'path';

const Blog = ({ posts }) => (
  <ul>
    {posts.map((post) => (
      <li key={post.id}>
        <h3>{post.filename}</h3>
        <p>{post.content}</p>
      </li>
    ))}
  </ul>
);

// Данная функция вызывается на сервере, так что
// в ней можно напрямую обращаться к БД
export async function getStaticProps() {
  const postsDir = join(process.cwd(), 'posts');
  const filenames = await fs.readdir(postsDir);

  const posts = filenames.map(async (filename) => {
    const filePath = join(postsDir, filename);
    const fileContent = await fs.readFile(
      filePath,
      'utf-8'
    );

    // Обычно, здесь выполняется преобразование контента,
    // например, разбор `markdown` в `HTML`

    return {
      filename,
      content: fileContent,
    };
  });

  return {
    props: {
      posts: await Promise.all(posts),
    },
  };
}
export default Blog;
```

### Технические подробности

- Поскольку `getStaticProps` запускается во время сборки, она не может использовать данные из запроса, такие как параметры строки запроса (query params) или HTTP-заголовки (headers)
- `getStaticProps` запускается только на сервере, поэтому ее нельзя использовать для обращения к внутренним роутам
- при использовании `getStaticProps` генерируется не только HTML, но и файл в формате JSON. Данный файл содержит результаты выполнения `getStaticProps` и используется механизмом маршрутизации на стороне клиента для передачи пропов компонентам
- `getStaticProps` может использовать только в компоненте-странице. Это объясняется тем, что все данные, необходимые для рендеринга страницы, должны быть доступными
- в режиме для разработки `getStaticProps` вызывается при каждом запросе
- режим предварительного просмотра (preview mode) используется для рендеринга страницы при каждом запросе

## getStaticPaths

Страницы с динамической маршрутизацией, из которых экспортируется асинхронная функция `getStaticPaths`, будут предварительно сгенерированы для всех путей, возвращаемых этой функцией.

```js
export async function getStaticPaths() {
  return {
    paths: [(params: {})],
    fallback: true | false | 'blocking',
  };
}
```

### Ключ paths

`paths` определяет, какие пути будут предварительно отрендерены. Например, если у нас имеется страница с динамической маршрутизацией, которая называется `pages/posts/[id].js`, и экспортируемая на этой странице `getStaticPaths` возвращает такой `paths`:

```js
return {
  paths: [{ params: { id: '1' } }, { params: { id: '2' } }],
};
```

Тогда будут статически сгенерированы страницы `posts/1` и `posts/2` на основе компонента `pages/posts/[id].js`.

Обратите внимание, что название каждого `params` должно совпадать с параметрами, используемыми на странице:

- если названием страницы является `pages/posts/[postId]/[commentId]`, тогда `params` должен содержать `postId` и `commentId`
- если на странице используется перехватчик роутов, например, `pages/[...slug]`, `params` должен содержать `slug` в виде массива. Например, если такой массив будет выглядеть как `['foo', 'bar']`, то будет сгенерирована страница `/foo/bar`
- если на странице используется опциональный перехватчик роутов, применение `null`, `[]`, `undefined` или `false`, приведет к рендерингу роута верхнего уровня. Например, при применении `slug: false` к `pages/[[...slug]]`, будет сгенерирована страница `/`

### Ключ fallback

Если `fallback` имеет значение `false`, отсутствующий путь будет разрешаться страницей 404.

Если `fallback` имеет значение `true`, поведение `getStaticProps` будет таким:

- пути из `getStaticPaths` будут сгенерированы во время сборки с помощью `getStaticProps`
  отсутствующий путь не будет разрешаться страницей 404. Вместо этого в ответ на запрос будет возвращена резервная страница
- в фоновом режиме выполняется генерация запрошенного HTML и JSON. Это включает в себя вызов `getStaticProps`
- браузер получает JSON для сгенерированного пути. Этот JSON используется для автоматического рендеринга страницы с обязательными пропами. Со стороны пользователя это выглядит как переключение между резервной и полной страницами
- новый путь добавляется в список предварительно отрендеренных страниц

Обратите внимание: `fallback: true` не поддерживается при использовании `next export`.

### Резервные страницы

В резервной версии страницы:

- пропы страницы будут пустыми
- определить, что рендерится резервная страница, можно с помощью роутера: `router.isFallback` будет иметь значение `true`

```js
// pages/posts/[id].js
import { useRouter } from 'next/router';

function Post({ post }) {
  const router = useRouter();

  // Если страница еще не сгенерирована, будет отображаться это
  // До тех пор, пока `getStaticProps` не закончит свою работу
  if (router.isFallback) {
    return <div>Загрузка...</div>;
  }

  // рендеринг поста
}

export async function getStaticPaths() {
  return {
    paths: [
      { params: { id: '1' } },
      { params: { id: '2' } },
    ],
    fallback: true,
  };
}

export async function getStaticProps({ params }) {
  const res = await fetch(`/posts/${params.id}`);
  const post = await res.json();

  return {
    props: {
      post,
    },
    revalidate: 1,
  };
}

export default Post;
```

### В каких случаях может быть полезен `fallback: true`?

`fallback: true` может быть полезен при очень большом количестве статических страниц, которые зависят от данных (например, очень большой интернет-магазин). Мы хотим предварительно рендерить все страницы, но понимаем, что сборка будет длиться целую вечность.

Вместо этого мы генерируем небольшой набор статических страниц и используем `fallback: true` для остальных. При запросе отсутствующей страницы пользователь какое-то время будет наблюдать индикатор загрузки (пока `getStaticProps` делает свое дело), затем увидит саму страницу. И после этого новая страница будет возвращаться в ответ на каждый запрос.

!!! warning "Обратите внимание"

    `fallback: true` не обновляет сгенерированные страницы. Для этого используется инкрементальная статическая регенерация.

Если `fallback` имеет значение `blocking`, отсутствующий путь также не будет разрешаться страницей 404, но и перехода между резервной и нормальной страницами не будет. Вместо этого запрашиваемая страница будет сгенерирована на сервере и отправлена браузеру, а пользователь после некоторого ожидания сразу увидит готовую страницу

### Случаи использования `getStaticPaths`

`getStaticPaths` используется для предварительного рендеринга страниц с динамической маршрутизацией.

### Использование с TypeScript

```ts
import { GetStaticPaths } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {};
```

### Технические подробности

- `getStaticPaths` должна использоваться совместно с `getStaticProps`. Она не может использоваться вместе с `getServerSideProps`
- `getStaticPaths` запускается только на сервере во время сборки
- `getStaticPaths` может экспортироваться только в компоненте-странице
- в режиме для разработки `getStaticPaths` запускается при каждом запросе

## getServerSideProps

Страница, из которой экспортируется асинхронная функция `getServerSideProps`, будет рендерится при каждом запросе с помощью возвращаемых этой функцией пропов.

```js
export async function getServerSideProps(context) {
  return {
    props: {},
  };
}
```

`context` — это объект со следующими свойствами:

- `params`: см. `getStaticProps`
- `req`: объект HTTP `IncomingMessage` (входящее сообщение, запрос)
- `res`: объект HTTP-ответа
- `query`: объектное представление строки запроса
- `preview`: см. `getStaticProps`
- `previewData`: см. `getStaticProps`
- `resolveUrl`: нормализованная версия запрашиваемого URL, из которой удален префикс `_next/data` и включены значения оригинальной строки запроса
- `locale`: см. `getStaticProps`
- `locales`: см. `getStaticProps`
- `defaultLocale`: см. `getStaticProps`

`getServerSideProps` должна возвращать объект с такими полями:

- `props` — см. `getStaticProps`
- `notFound` — см. `getStaticProps`

```js
export async function getServerSideProps(context) {
  const res = await fetch('/data');
  const data = await res.json();

  if (!data) {
    return {
      notFound: true,
    };
  }

  return {
    props: {},
  };
}
```

- `redirect` — см. `getStaticProps`

```js
export async function getServerSideProps(context) {
  const res = await fetch('/data');
  const data = await res.json();

  if (!data) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
      },
    };
  }

  return {
    props: {},
  };
}
```

Для `getServerSideProps` характерны те же особенности и ограничения, что и для `getStaticProps`.

### Случаи использования getServerSideProps

`getServerSideProps` следует использовать только при необходимости предварительного рендеринга страницы на основе данных, зависящих от запроса.

### Использование getServerSideProps с TypeScript

```ts
import { GetServerSideProps } from 'next';

export const getServerSideProps: GetServerSideProps = async () => {};
```

Для получения предполагаемых типов для пропов следует использовать `InferGetServerSidePropsType<typeof getServerSideProps>`:

```ts
import { InferGetServerSidePropsType } from 'next';

type Data = {};

export async function getServerSideProps() {
  const res = await fetch('/data');
  const data = await res.json();

  return {
    props: {
      data,
    },
  };
}

function Page({
  data,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  // ...
}

export default Page;
```

### Технические подробности

- `getServerSideProps` запускается только на сервере
- `getServerSideProps` может экспортироваться только в компоненте-странице

## Получение данных на стороне клиента

Если на странице имеются часто обновляемые данные, но страница не нуждается в предварительном рендеринге (по соображениям, связанным с SEO), тогда можно запрашивать такие данные на стороне клиента.

Команда Next.js рекомендует использовать для этого разработанный ими хук `useSWR`, который предоставляет такие возможности, как кеширование данных, инвалидация кеша, отслеживание фокуса, периодическое выполнение повторных запросов и т. д.

```js
import useSWR from 'swr';

const fetcher = (url) =>
  fetch(url).then((res) => res.json());

function Profile() {
  const { data, error } = useSWR('/api/user', fetcher);

  if (error)
    return <div>При загрузке данных возникла ошибка</div>;
  if (!data) return <div>Загрузка...</div>;

  return <div>Привет, {data.name}!</div>;
}
```
