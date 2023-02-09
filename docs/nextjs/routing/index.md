# Введение

Маршрутизация в Next.js основана на концепции страниц.

Файл, помещаемый в директорию `pages`, автоматически становится роутом.

Файлы `index.js` привязываются к корневой директории:

```
pages/index.js -> /
pages/blog/index.js -> /blog
```

Роутер поддерживает вложенные файлы:

```
pages/blog/first-post.js -> /blog/first-post
pages/dashboard/settings/username.js -> /dashboard/settings/username
```

Динамические сегменты маршрутов определяются с помощью квадратных скобок:

```
pages/blog/[slug].js -> /blog/:slug (blog/first-post)
pages/[username]/settings.js -> /:username/settings (/johnsmith/settings)
pages/post/[...all].js -> /post/* (/post/2021/id/title)
```

## Связь между страницами

Для маршрутизации на стороне клиента используется компонент `Link`:

```js
import Link from 'next/link';

export default function Home() {
  return (
    <ul>
      <li>
        <Link href="/">Главная</Link>
      </li>
      <li>
        <Link href="/about">О нас</Link>
      </li>
      <li>
        <Link href="/blog/first-post">Пост номер раз</Link>
      </li>
    </ul>
  );
}
```

Здесь:

```
/ → pages/index.js
/about → pages/about.js
/blog/first-post → pages/blog/[slug].js
```

Для динамических сегментов можно использовать интерполяцию:

```js
import Link from 'next/link';

export default function Post({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link
            href={`/blog/${encodeURIComponent(post.slug)}`}
          >
            {post.title}
          </Link>
        </li>
      ))}
    </ul>
  );
}
```

Или объект `URL`:

```js
import Link from 'next/link';

export default function Post({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link
            href={{
              pathname: '/blog/[slug]',
              query: { slug: post.slug },
            }}
          >
            <a>{post.title}</a>
          </Link>
        </li>
      ))}
    </ul>
  );
}
```

Здесь:

- `pathname` — это название страницы в директории `pages` (`/blog/[slug]` в данном случае)
- `query` — это объект с динамическим сегментом (`slug` в данном случае)

Для доступа к объекту `router` в компоненте можно использовать хук `useRouter` или утилиту `withRouter`. Рекомендуется использовать `useRouter`.
