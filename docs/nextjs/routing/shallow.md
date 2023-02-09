# Поверхностная (тихая) маршрутизация (Shallow Routing)

Тихий роутинг позволяет менять URL без перезапуска методов для получения данных, включая функции `getServerSideProps` и `getStaticProps`.

Мы получаем обновленные `pathname` и `query` через объект `router` (получаемый с помощью `useRouter()` или `withRouter()`) без потери состояния компонента.

Для включения тихого роутинга используется настройка `{ shallow: true }`:

```js
import { useEffect } from 'react';
import { useRouter } from 'next/router';

// текущий `URL` имеет значение `/`
export default function Page() {
  const router = useRouter();

  useEffect(() => {
    // выполнить навигацию после первого рендеринга
    router.push('?counter=1', undefined, { shallow: true });
  }, []);

  useEffect(() => {
    // значение `counter` изменилось!
  }, [router.query.counter]);
}
```

При обновлении URL изменится только состояние роута.

Обратите внимание: тихий роутинг работает только в пределах одной страницы. Предположим, что у нас имеется страница `pages/about.js` и мы выполняем следующее:

```js
router.push('?counter=1', '/about?counter=1', {
  shallow: true,
});
```

В этом случае текущая страница выгружается, загружается новая, методы для получения данных перезапускаются (несмотря на наличие `{ shallow: true }`).
