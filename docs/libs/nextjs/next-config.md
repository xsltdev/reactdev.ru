# next.config.js

Файл `next.config.js` или `next.config.mjs` предназначен для кастомной продвинутой настройки Next.js.

Пример `next.config.js`:

```js
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  /* настройки */
};

module.exports = nextConfig;
```

Пример `next.config.mjs`:

```js
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  /* настройки */
};

export default nextConfig;
```

Можно использовать функцию:

```js
module.exports = (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    /* настройки */
  };
  return nextConfig;
};
```

`phase` — это текущий контекст, для которого загружаются настройки. Доступными фазами являются:

- `PHASE_EXPORT`
- `PHASE_PRODUCTION_BUILD`
- `PHASE_PRODUCTION_SERVER`
- `PHASE_DEVELOPMENT_SERVER`

Фазы импортируются из `next/constants`:

```js
const {
  PHASE_DEVELOPMENT_SERVER,
} = require('next/constants');

module.exports = (phase, { defaultConfig }) => {
  if (phase === PHASE_DEVELOPMENT_SERVER) {
    return {
      /* настройки для разработки */
    };
  }

  return {
    /* другие настройки */
  };
};
```

## Переменные среды окружения

Пример:

```js
module.exports = {
  env: {
    someKey: 'some-value',
  },
};
```

Использование:

```js
export default function Page() {
  return (
    <h1>
      Значением `someKey` является `{process.env.someKey}`
    </h1>
  );
}
```

Результат:

```js
export default function Page() {
  return <h1>Значением `someKey` является `some-value`</h1>;
}
```

## Заголовки

Настройка `headers` позволяет устанавливать кастомные HTTP-заголовки для входящих запросов:

```js
module.exports = {
  async headers() {
    return [
      {
        source: '/about',
        headers: [
          {
            key: 'x-custom-header',
            value: 'кастомное значение заголовка',
          },
          {
            key: 'x-another-custom-header',
            value: 'еще одно кастомное значение заголовка',
          },
        ],
      },
    ];
  },
};
```

`headers` — асинхронная функция, возвращающая массив объектов со свойствами `source` и `headers`:

- `source` — адрес входящего запроса
- `headers` — массив объектов со свойствами `key` и `value`

Дополнительные параметры:

- `basePath: false | undefined` — если `false`, `basePath` не будет учитываться при совпадении, может использоваться только для внешних перезаписей
- `locale: false | undefined` — определяет, должна ли при совпадении включаться локаль
- `has` — массив объектов со свойствами `type`, `key` и `value`

Если в настройках определены два кастомных заголовка с одинаковыми ключами, будет учитываться только значение последнего заголовка.

**Поиск совпадения путей**. Разрешен поиск совпадения путей. Например, путь `/blog/:slug` будет совпадать с `/blog/hello-world` (без вложенных путей):

```js
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:slug',
        headers: [
          {
            key: 'x-slug',
            value: ':slug', // Совпавшие параметры могут использоваться в качестве значений
          },
          {
            key: 'x-slug-:slug', // Совпавшие параметры могут использоваться в качестве ключей
            value: 'кастомное значение заголовка',
          },
        ],
      },
    ];
  },
};
```

**Поиск всех совпадений путей**. Для поиска всех совпадений можно использовать `*` после параметра, например, `/blog/:slug*` будет совпадать с `/blog/a/b/c/d/hello-world`:

```js
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:slug*',
        headers: [
          {
            key: 'x-slug',
            value: ':slug*',
          },
          {
            key: 'x-slug-:slug*',
            value: 'кастомное значение заголовка',
          },
        ],
      },
    ];
  },
};
```

**Поиск совпадений путей с помощью регулярных выражений**. Для поиска совпадений с помощью регулярок используются круглые скобки после параметра, например, `/blog/:slug(\\d{1,})` будет совпадать с `/blog/123`, но не с `/blog/abc`:

```js
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:post(\\d{1,})',
        headers: [
          {
            key: 'x-post',
            value: ':post',
          },
        ],
      },
    ];
  },
};
```

Символы `( ) { } : * + ?` считаются частью регулярного выражения, поэтому при использовании в `source` в качестве обычных символов они должны быть экранированы с помощью `\\`:

```js
module.exports = {
  async headers() {
    return [
      {
        // Это будет совпадать с `/english(default)/something`
        source: '/english\\(default\\)/:slug',
        headers: [
          {
            key: 'x-header',
            value: 'some-value',
          },
        ],
      },
    ];
  },
};
```

**Поиск совпадения на основе заголовка, куки и строки запроса**. Для этого используется поле `has`. Заголовок будет установлен только при совпадении полей `source` и `has`.

Значением `has` является массив объектов со следующими свойствами:

- `type: string` — `header | cookie | host | query`
- `key: string` — ключ для поиска совпадения
- `value: string | undefined` — значение для проверки. Если `undefined`, любое значение будет совпадать. Для захвата определенной части значения может использоваться регулярное выражение. Например, если для `hello-world` используется значение `hello-(?<param>.*)`, `world` можно использовать в качестве значения `destination` как `:param`:

```js
module.exports = {
  async headers() {
    return [
      // Если имеется заголовок `x-add-header`,
      // будет установлен заголовок `x-another-header`
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-add-header',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: 'hello',
          },
        ],
      },
      // Если совпадают `source`, `query` и `cookie`,
      // будет установлен заголовок `x-authorized`
      {
        source: '/specific/:path*',
        has: [
          {
            type: 'query',
            key: 'page',
            // Значение `page` будет недоступно в заголовке,
            // поскольку значение указано и при этом
            // не используются именованная группа захвата, например `(?<page>home)`
            value: 'home',
          },
          {
            type: 'cookie',
            key: 'authorized',
            value: 'true',
          },
        ],
        headers: [
          {
            key: 'x-authorized',
            value: ':authorized',
          },
        ],
      },
      // Если имеется заголовок `x-authorized` и он
      // содержит искомое значение, будет установлен заголовок `x-another-header`
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-authorized',
            value: '(?<authorized>yes|true)',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: ':authorized',
          },
        ],
      },
      // Если значением хоста является `example.com`,
      // будет установлен данный заголовок
      {
        source: '/:path*',
        has: [
          {
            type: 'host',
            value: 'example.com',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: ':authorized',
          },
        ],
      },
    ];
  },
};
```

**`basePath` и `i18n`**. При наличии `basePath`, его значение автоматически добавляется к значению `source`, если не определено `basePath: false`:

```js
module.exports = {
  basePath: '/docs',

  async headers() {
    return [
      {
        source: '/with-basePath', // становится /docs/with-basePath
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        source: '/without-basePath', // не модифицируется
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
        basePath: false,
      },
    ];
  },
};
```

При наличии `i18n` к значению `source` автоматически добавляются значения `locales`, если не определено `locale: false` — в этом случае значение `source` должно включать префикс локали:

```js
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'de'],
    defaultLocale: 'en',
  },

  async headers() {
    return [
      {
        source: '/with-locale', // автоматическая обработка всех локалей
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // ручная установка локали
        source: '/nl/with-locale-manual',
        locale: false,
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // это совпадает с `/`, поскольку `en` является `defaultLocale`
        source: '/en',
        locale: false,
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // это преобразуется в /(en|fr|de)/(.*), поэтому не будет совпадать с роутами верхнего уровня, такими как
        // `/` или `/fr`, а с `/:path*` будет
        source: '/(.*)',
        headers: [
          {
            key: 'x-hello',
            value: 'worlld',
          },
        ],
      },
    ];
  },
};
```

## Дополнительная настройка Webpack

Перед кастомизацией Вебпака убедитесь, что Next.js не имеет поддержки необходимого функционала.

Пример определения функции для настройки webpack:

```js
module.exports = {
  webpack: (
    config,
    { buildId, dev, isServer, defaultLoaders, webpack }
  ) => {
    // не забудьте вернуть модифицированный конфиг
    return config;
  },
};
```

Данная функция выполняется дважды: один раз для сервера и еще один для клиента. Это позволяет разделять настройки с помощью свойства `isServer`.

Вторым аргументом, передаваемым функции является объект со следующими свойствами:

- `buildId: string` — уникальный идентификатор сборки
- `dev: boolean` — индикатор компиляции в режиме разработки
- `isServer: boolean` — если `true`, значит, выполняется компиляция для сервера
- `defaultLocales: object` — дефолтные лоадеры:
- `babel: object` — дефолтные настройки `babel-loader`

Пример использования `defaultLoaders.babel`:

```js
module.exports = {
  webpack: (config, options) => {
    config.module.rules.push({
      test: /\.mdx/,
      use: [
        options.defaultLoaders.babel,
        {
          loader: '@mdx-js/loader',
          options: pluginOptions.options,
        },
      ],
    });

    return config;
  },
};
```

Настройка `distDir` позволяет определять директорию для сборки:

```js
module.exports = {
  distDir: 'build',
};
```

Настройка `generateBuildId` позволяет определять идентификатор сборки:

```js
module.exports = {
  generateBuildId: async () => {
    // Здесь можно использовать, например, хеш последнего гит-коммита
    return 'my-build-id';
  },
};
```

Пример отключения проверки кода с помощью `eslint` при сборке проекта:

```js
module.exports = {
  eslint: {
    ignoreDuringBuilds: true,
  },
};
```

Пример отключения typescript при сборке проекта:

```js
module.exports = {
  typescript: {
    ignoreBuildErrors: true,
  },
};
```
