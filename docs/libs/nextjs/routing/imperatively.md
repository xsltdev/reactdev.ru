# Императивный подход к навигации на стороне клиента

В большинстве случаев для реализации навигации на стороне клиента достаточно компонента `Link` из `next/link`. Однако, для этого можно использовать и роутер из `next/router`:

```js
import { useRouter } from 'next/router';

export default function ReadMore() {
  const router = useRouter();

  return (
    <button onClick={() => router.push('/about')}>
      Читать подробнее
    </button>
  );
}
```
