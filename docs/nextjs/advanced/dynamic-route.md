# Динамическая маршрутизация

Next.js поддерживает динамический `import`. Он позволяет загружать модули по необходимости. Это также работает с SSR.

В следующем примере мы реализуем неточный (fuzzy) поиск с помощью `fuse.js`, загружая этот модуль динамически после того, как пользователь начинает вводить данные в поле для поиска:

```js
import { useState } from 'react';

const names = ['John', 'Jane', 'Alice', 'Bob', 'Harry'];

export default function Page() {
  const [results, setResults] = useState([]);

  return (
    <div>
      <input
        type="text"
        placeholder="Поиск"
        onChange={async ({ currentTarget: { value } }) => {
          // загружаем модуль динамически
          const Fuse = (await import('fuse.js')).default;
          const fuse = new Fuse(names);

          setResults(fuse.search(value));
        }}
      />
      <pre>
        Результаты поиска:{' '}
        {JSON.stringify(results, null, 2)}
      </pre>
    </div>
  );
}
```

Динамический импорт — это способ разделения кода на части (code splitting), позволяющий загружать только тот код, который фактически используется на текущей странице.

Для динамического импорта React-компонентов рекомендуется использовать `next/dynamic`.

## Обычное использование

В следующем примере мы динамически загружаем модель `../components/Hello`:

```js
import dynamic from 'next/dynamic';
import Header from '../components/Header';

const DynamicHello = dynamic(() =>
  import('../components/Hello')
);

export default function Home() {
  return (
    <div>
      <Header />
      <DynamicHello />
      <h1>Главная страница</h1>
    </div>
  );
}
```

## Динамический импорт именованного компонента

Предположим, что у нас имеется такой компонент:

```js
// components/Hello.js
export const Hello = () => <p>Привет!</p>;
```

Для его динамического импорта его необходимо вернуть из `Promise`, возвращаемого `import`:

```js
import dynamic from 'next/dynamic';
import Header from '../components/Header';

const DynamicHello = dynamic(() =>
  import('../components/Hello').then(
    (module) => module.Hello
  )
);

export default function Home() {
  return (
    <div>
      <Header />
      <DynamicHello />
      <h1>Главная страница</h1>
    </div>
  );
}
```

## Индикатор загрузки

Для рендеринга состояния загрузки можно использовать настройку `loading`:

```js
import dynamic from 'next/dynamic';
import Header from '../components/Header';

const DynamicHelloWithCustomLoading = dynamic(
  () => import('../components/Hello'),
  { loading: () => <p>Загрузка...</p> }
);

export default function Home() {
  return (
    <div>
      <Header />
      <DynamicHelloWithCustomLoading />
      <h1>Главная страница</h1>
    </div>
  );
}
```

## Отключение SSR

Для отключения импорта модуля на стороне сервера можно использовать настройку `ssr`:

```js
import dynamic from 'next/dynamic';
import Header from '../components/Header';

const DynamicHelloWithNoSSR = dynamic(
  () => import('../components/Hello'),
  { ssr: false }
);

export default function Home() {
  return (
    <div>
      <Header />
      <DynamicHelloWithNoSSR />
      <h1>Главная страница</h1>
    </div>
  );
}
```

Настройка suspense позволяет загружать компонент лениво подобно тому, как это делает сочетание `React.lazy` и `<Suspense>`. Обратите внимание, что это работает только на клиенте или на сервере с `fallback`. Полная поддержка SSR в конкурентном режиме находится в процессе разработки:

```js
import dynamic from 'next/dynamic';
import Header from '../components/Header';

const DynamicLazyHello = dynamic(
  () => import('../components/Hello'),
  { suspense: true }
);

export default function Home() {
  return (
    <div>
      <Header />
      <DynamicLazyHello />
      <h1>Главная страница</h1>
    </div>
  );
}
```
