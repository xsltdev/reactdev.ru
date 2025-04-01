---
description: В предыдущей главе вы создали макет и страницы дашборда. Теперь давайте добавим несколько ссылок, чтобы пользователи могли перемещаться между маршрутами дашборда.
---

# Навигация между страницами

<big>В предыдущей главе вы создали макет и страницы дашборда. Теперь давайте добавим несколько ссылок, чтобы пользователи могли перемещаться между маршрутами дашборда.</big>

!!!tip "Вот темы, которые мы рассмотрим"

    -   Как использовать компонент `next/link`.
    -   Как показать активную ссылку с помощью хука `usePathname()`.
    -   Как работает навигация в Next.js.

## Зачем оптимизировать навигацию?

Для ссылок между страницами традиционно используется HTML-элемент `<a>`. В данный момент ссылки на боковую панель используют элементы `<a>`, но обратите внимание, что происходит, когда вы переходите между страницами «Главная», «Счета» и «Клиенты» в вашем браузере.

Вы видели?

На каждой странице навигации происходит полное обновление страницы!

## Компонент `<Link>`

В Next.js вы можете использовать компонент `<Link />` для создания ссылок между страницами в вашем приложении. `<Link>` позволяет осуществлять [навигацию на стороне клиента](https://nextjs.org/docs/app/building-your-application/routing/linking-and-navigating#how-routing-and-navigation-works) с помощью JavaScript.

Чтобы использовать компонент `<Link />`, откройте файл `/app/ui/dashboard/nav-links.tsx` и импортируйте компонент Link из [`next/link`](https://nextjs.org/docs/app/api-reference/components/link). Затем замените тег `<a>` на `<Link>`:

```ts title="/app/ui/dashboard/nav-links.tsx" hl_lines="6 16 25"
import {
    UserGroupIcon,
    HomeIcon,
    DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';

// ...

export default function NavLinks() {
    return (
        <>
            {links.map((link) => {
                const LinkIcon = link.icon;
                return (
                    <Link
                        key={link.name}
                        href={link.href}
                        className="flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3"
                    >
                        <LinkIcon className="w-6" />
                        <p className="hidden md:block">
                            {link.name}
                        </p>
                    </Link>
                );
            })}
        </>
    );
}
```

Как видите, компонент `Link` похож на использование тегов `<a>`, но вместо `<a href="...">` вы используете `<Link href="...">`.

Сохраните изменения и проверьте, работает ли это на вашем localhost. Теперь вы должны иметь возможность перемещаться между страницами без полного обновления. Хотя части вашего приложения отображаются на сервере, полное обновление страницы не происходит, что позволяет чувствовать себя как родное веб-приложение. Почему так?

## Автоматическое разделение кода и предварительная выборка

Для улучшения навигации Next.js автоматически разделяет код вашего приложения по сегментам маршрута. Это отличается от традиционного React [SPA](https://nextjs.org/docs/app/building-your-application/upgrading/single-page-applications), где браузер загружает весь код вашего приложения при начальной загрузке страницы.

Разделение кода по маршрутам означает, что страницы становятся изолированными. Если на какой-то странице произойдет ошибка, остальная часть приложения будет работать. Кроме того, браузеру приходится разбирать меньше кода, что делает ваше приложение быстрее.

Кроме того, в процессе работы, когда в области просмотра браузера появляются компоненты [`<Link>`](https://nextjs.org/docs/api-reference/next/link), Next.js автоматически **загружают** код для связанного маршрута в фоновом режиме. К тому моменту, когда пользователь нажимает на ссылку, код целевой страницы уже будет загружен в фоновом режиме, и именно это делает переход на страницу практически мгновенным!

Подробнее о том [как работает навигация](https://nextjs.org/docs/app/building-your-application/routing/linking-and-navigating#how-routing-and-navigation-works).

<?quiz?>

question: Что делает Next.js, когда компонент Link появляется в области просмотра браузера в "production" окружении?
answer: Загружает дополнительный CSS
answer: Предзагружает изображения
answer-correct: Предварительно загружает код для связанного маршрута
answer: Включает ленивую загрузку для связанного маршрута
content:

<p>Next.js автоматически подгружает код для маршрута, на который ведет ссылка, в фоновом режиме. К тому моменту, когда пользователь нажимает на ссылку, код целевой страницы уже будет загружен в фоновом режиме, и именно это делает переход на страницу практически мгновенным!</p>
<?/quiz?>

## Паттерн: Показ активных ссылок

Распространенным шаблоном пользовательского интерфейса является отображение активной ссылки, чтобы указать пользователю, на какой странице он находится в данный момент. Для этого необходимо получить текущий путь пользователя из URL. Next.js предоставляет хук [`usePathname()`](https://nextjs.org/docs/app/api-reference/functions/use-pathname), который можно использовать для проверки пути и реализации этого паттерна.

Поскольку [`usePathname()`](https://nextjs.org/docs/app/api-reference/functions/use-pathname) - это хук React, вам нужно будет превратить `nav-links.tsx` в клиентский компонент. Добавьте директиву React `"use client"` в верхнюю часть файла, затем импортируйте `usePathname()` из `next/navigation`:

```ts title="/app/ui/dashboard/nav-links.tsx" hl_lines="1 9"
'use client';

import {
    UserGroupIcon,
    HomeIcon,
    DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

// ...
```

Затем присвойте путь переменной `pathname` внутри компонента `<NavLinks />`:

```ts title="/app/ui/dashboard/nav-links.tsx" hl_lines="2"
export default function NavLinks() {
    const pathname = usePathname();
    // ...
}
```

!!!note ""

    `nav-links.tsx` не является специальным файлом для Next.js - его можно назвать как угодно. Если вы переименуете его, убедитесь, что вы соответствующим образом обновили операторы импорта.

Вы можете использовать библиотеку `clsx`, представленную в главе [CSS styling](./css-styling.md), для условного применения имен классов, когда ссылка активна. Когда `link.href` совпадает с `pathname`, ссылка должна отображаться с синим текстом и светло-голубым фоном.

Вот финальный код для `nav-links.tsx`:

```ts title="/app/ui/dashboard/nav-links.tsx" hl_lines="10 25-30"
'use client';

import {
    UserGroupIcon,
    HomeIcon,
    DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

// ...

export default function NavLinks() {
    const pathname = usePathname();

    return (
        <>
            {links.map((link) => {
                const LinkIcon = link.icon;
                return (
                    <Link
                        key={link.name}
                        href={link.href}
                        className={clsx(
                            'flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
                            {
                                'bg-sky-100 text-blue-600':
                                    pathname === link.href,
                            }
                        )}
                    >
                        <LinkIcon className="w-6" />
                        <p className="hidden md:block">
                            {link.name}
                        </p>
                    </Link>
                );
            })}
        </>
    );
}
```

Сохраните и проверьте свой localhost. Теперь вы должны увидеть активную ссылку, выделенную синим цветом.

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/navigating-between-pages></small>
