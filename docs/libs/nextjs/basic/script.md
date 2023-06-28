# Компонент Script

Компонент `Script` позволяет разработчикам определять приоритет загрузки сторонних скриптов, что экономит время и улучшает производительность.

Приоритет загрузки скрипта определяется с помощью пропа `strategy`, который принимает одно из следующих значений:

- `beforeInteractive`: предназначено для важных скриптов, которые должны быть загружены и выполнены до того, как страница станет интерактивной. К таким скриптам относятся, например, обнаружение ботов и запрос разрешений. Такие скрипты внедряются в первоначальный HTML и запускаются перед остальным JS
- `afterInteractive`: для скриптов, которые могут загружаться и выполняться после того, как страница стала интерактивной. К таким скриптам относятся, например, менеджеры тегов и аналитика. Такие скрипты выполняются на стороне клиента и запускаются после гидратации
- `lazyOnload`: для скриптов, которые могут быть загружены в период простоя. К таким скриптам относятся, например, поддержка чатов и виджеты социальных сетей

!!! warning "Обратите внимание"

    `Script` поддерживает встроенные скрипты со стратегиями `afterInteractive` и `lazyOnload`

встроенные скрипты, обернутые в `Script`, должны иметь атрибут `id` для их отслеживания и оптимизации

## Примеры

!!! warning "Обратите внимание"

    Компонент `Script` не должен помещаться внутрь компонента `Head` или кастомного документа.

Загрузка полифилов

```js
import Script from 'next/script';

export default function Home() {
  return (
    <>
      <Script
        src="https://polyfill.io/v3/polyfill.min.js?features=IntersectionObserverEntry%2CIntersectionObserver"
        strategy="beforeInteractive"
      />
    </>
  );
}
```

Отложенная загрузка

```js
import Script from 'next/script';

export default function Home() {
  return (
    <>
      <Script
        src="https://connect.facebook.net/en_US/sdk.js"
        strategy="lazyOnload"
      />
    </>
  );
}
```

Выполнение кода после полной загрузки страницы

```js
import { useState } from 'react';
import Script from 'next/script';

export default function Home() {
  const [stripe, setStripe] = useState(null);

  return (
    <>
      <Script
        id="stripe-js"
        src="https://js.stripe.com/v3/"
        onLoad={() => {
          setStripe({
            stripe: window.Stripe('pk_test_12345'),
          });
        }}
      />
    </>
  );
}
```

Встроенные скрипты

```js
import Script from 'next/script'

<Script id="show-banner" strategy="lazyOnload">
  {`document.getElementById('banner').classList.remove('hidden')`}
</Script>

// или
<Script
  id="show-banner"
  dangerouslySetInnerHTML={{
    __html: `document.getElementById('banner').classList.remove('hidden')`
  }}
/>
```

Передача атрибутов

```js
import Script from 'next/script';

export default function Home() {
  return (
    <>
      <Script
        src="https://www.google-analytics.com/analytics.js"
        id="analytics"
        nonce="XUENAJFW"
        data-test="analytics"
      />
    </>
  );
}
```
