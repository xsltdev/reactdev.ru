# Кастомные страницы ошибок

Next.js предоставляет дефолтные страницы для ошибок 404 и 500. Для кастомизации этих страниц используются файлы `pages/404.js` и `pages/500.js`, соответственно:

```js
// pages/404.js
export default function Custom404() {
  return <h1>404 - Страница не найдена</h1>;
}
```

```js
// pages/500.js
export default function Custom500() {
  return <h1>500 - Ошибка на сервере</h1>;
}
```

Для получения данных во время сборки на этих страницах может использоваться `getStaticProps`.

Ошибки 500 обслуживаются как на стороне клиента, так и на стороне сервера компонентом `Error`. Для перезаписи этого компонента необходимо создать файл `pages/_error.js` и добавить в него код вроде следующего:

```js
export default function Error({ statusCode }) {
  return (
    <p>
      {statusCode
        ? `На сервере возникла ошибка ${statusCode}`
        : `Ошибка возникла на клиенте`}
    </p>
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res
    ? res.statusCode
    : err
    ? err.statusCode
    : 404;
  return { statusCode };
};
```

Обратите внимание: `pages/_error.js` используется только в продакшне. В режиме для разработки ошибка возвращается вместе со стеком вызовов для обеспечения возможности определения места ее возникновения.

Для рендеринга встроенной страницы ошибки также можно использовать компонент `Error`:

```js
import Error from 'next/error';

export async function getServerSideProps() {
  const res = await fetch(
    'https://api.github.com/repos/harryheman/react-total'
  );
  const errorCode = res.ok ? false : res.statusCode;
  const data = await res.json();

  return {
    props: {
      errorCode,
      stars: data.stergazers_count,
    },
  };
}

export default function Page({ errorCode, stars }) {
  if (errorCode) {
    return <Error statusCode={errorCode} />;
  }

  return <div>Количество звезд: {stars}</div>;
}
```

Компонент `Error` также принимает проп `title` для передачи текстового сообщения в дополнение к статус-коду.
