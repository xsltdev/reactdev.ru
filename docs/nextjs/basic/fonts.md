# Оптимизация шрифтов

Next.js автоматически встраивает шрифты в CSS во время сборки:

```html
// было
<link
  href="https://fonts.googleapis.com/css2?family=Inter"
  rel="stylesheet"
/>

// стало
<style
  data-href="https://fonts.googleapis.com/css2?family=Inter"
>
  @font-face {
    font-family: 'Inter';
    font-style: normal...;
  }
</style>
```

Для добавления на страницу шрифта используется компонент `Head`, импортируемый из `next/head`:

```js
// pages/index.js
import Head from 'next/head';

export default function IndexPage() {
  return (
    <div>
      <Head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
        />
      </Head>
      <p>Привет, народ!</p>
    </div>
  );
}
```

Для добавления шрифта в приложение следует создать кастомный документ:

```js
// pages/_document.js
import Document, {
  Html,
  Head,
  Main,
  NextScript,
} from 'next/document';

class MyDoc extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link
            rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
```

Автоматическую оптимизацию шрифтов можно отключить:

```js
// next.config.js
module.exports = {
  optimizeFonts: false,
};
```
