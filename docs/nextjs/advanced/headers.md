# Заголовки безопасности

Для улучшения безопасности приложения предназначена настройка `headers` в `next.config.js`. Данная настройка позволяет устанавливать HTTP-заголовки ответов для всех роутов в приложении:

```js
// next.config.js
// Список заголовков
const securityHeaders = [];

module.exports = {
  async headers() {
    return [
      {
        // Данные заголовки будут применяться ко всем роутам в приложении
        source: '/(.*)',
        headers: securityHeaders,
      },
    ];
  },
};
```

## Настройки

### X-DNS-Prefetch-Control

Данный заголовок управляет предварительной загрузкой (`prefetching`) DNS, позволяя браузерам заблаговременно разрешать названия доменов для внешних ссылок, изображений, CSS, JS и т. д. Предварительная загрузка выполняется в фоновом режиме и уменьшает время реакции на клик пользователя по ссылке:

```js
{
  key: 'X-DNS-Prefetch-Control',
  value: 'on'
}
```

### Strict-Transport-Security

Данный заголовок указывает браузеру использовать HTTPS вместо HTTP:

```js
{
  key: 'Strict-Transport-Security',
  // 2 года
  value: 'max-age=63072000; includeSubDomains; preload'
}
```

### X-XSS-Protection

Данный заголовок предназначен для блокировки межсайтового скриптинга в старых браузерах, не поддерживающих заголовок `Content-Security-Policy`:

```js
{
  key: 'X-XSS-Protection',
  value: '1; mode=block'
}
```

### X-Frame-Options

Данный заголовок определяет, может ли сайт открываться в [`iframe`](https://hcdev/html/iframe/). Он также предназначен для старых браузеров, не поддерживающих настройку `frame-ancestors` заголовка CSP:

```js
{
  key: 'X-Frame-Options',
  value: 'SAMEORIGIN'
}
```

### Permissions-Policy

Данный заголовок позволяет определять, какие возможности и API могут использоваться в браузере (раньше он назывался `Feature-Policy`):

```js
{
  key: 'Permissions-Policy',
  value: 'camera=(), microphone=(), geolocation=()'
}
```

### X-Content-Type-Options

Данный заголовок запрещает браузеру автоматически определять тип содержимого при отсутствии заголовка `Content-Type`:

```js
{
  key: 'X-Content-Type-Options',
  value: 'nosniff'
}
```

### Referrer-Policy

Данный заголовок управляет тем, какая информация о предыдущем сайте включается в ответ:

```js
{
  key: 'Referrer-Policy',
  value: 'origin-when-cross-origin'
}
```

### Content-Security-Policy

Данный заголовок определяет разрешенные источники для загрузки скриптов, стилей, изображений, шрифтов, медиа и др.:

```js
{
  key: 'Content-Security-Policy',
  value: // Политика `CSP`
}
```
