---
description: В предыдущей главе вы улучшили производительность начальной загрузки дашборда с помощью потоковой передачи данных. Теперь давайте перейдем к странице invoices и узнаем, как добавить поиск и пагинацию
---

# Поиска и пагинации

<big>В предыдущей главе вы улучшили производительность начальной загрузки дашборда с помощью потоковой передачи данных. Теперь давайте перейдем к странице `/invoices` и узнаем, как добавить поиск и пагинацию.</big>

!!!tip "Вот темы, которые мы рассмотрим"

    -   Научитесь использовать API Next.js: `useSearchParams`, `usePathname` и `useRouter`.
    -   Внедрите поиск и пагинацию с помощью параметров поиска URL.

## Начальный код

Внутри файла `/dashboard/invoices/page.tsx` вставьте следующий код:

```ts title="/app/dashboard/invoices/page.tsx"
import Pagination from '@/app/ui/invoices/pagination';
import Search from '@/app/ui/search';
import Table from '@/app/ui/invoices/table';
import { CreateInvoice } from '@/app/ui/invoices/buttons';
import { lusitana } from '@/app/ui/fonts';
import { InvoicesTableSkeleton } from '@/app/ui/skeletons';
import { Suspense } from 'react';

export default async function Page() {
    return (
        <div className="w-full">
            <div className="flex w-full items-center justify-between">
                <h1
                    className={`${lusitana.className} text-2xl`}
                >
                    Invoices
                </h1>
            </div>
            <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
                <Search placeholder="Search invoices..." />
                <CreateInvoice />
            </div>
            {/*  <Suspense key={query + currentPage} fallback={<InvoicesTableSkeleton />}>
        <Table query={query} currentPage={currentPage} />
      </Suspense> */}
            <div className="mt-5 flex w-full justify-center">
                {/* <Pagination totalPages={totalPages} /> */}
            </div>
        </div>
    );
}
```

Потратьте некоторое время на ознакомление со страницей и компонентами, с которыми вам предстоит работать:

-   `<Search/>` позволяет пользователям искать конкретные счета-фактуры.
-   `<Pagination/>` позволяет пользователям перемещаться между страницами счетов-фактур.
-   `<Table/>` отображает счета-фактуры.

Функциональность поиска будет охватывать клиент и сервер. Когда пользователь ищет счет-фактуру на клиенте, параметры URL обновляются, данные извлекаются на сервере, и таблица перерисовывается на сервере с новыми данными.

## Зачем использовать параметры поиска по URL?

Как было сказано выше, вы будете использовать параметры поиска URL для управления состоянием поиска. Этот паттерн может быть новым, если вы привыкли делать это с состоянием на стороне клиента.

Есть несколько преимуществ реализации поиска с помощью параметров URL:

-   **URL, доступные для закладок и совместного использования**: Поскольку параметры поиска находятся в URL, пользователи могут сохранять текущее состояние приложения, включая поисковые запросы и фильтры, в закладках для последующего использования или обмена.
-   **Серверный рендеринг**: Параметры URL можно напрямую использовать на сервере для рендеринга начального состояния, что упрощает работу с серверным рендерингом.
-   **Аналитика и отслеживание**: Наличие поисковых запросов и фильтров непосредственно в URL упрощает отслеживание поведения пользователей, не требуя дополнительной логики на стороне клиента.

## Добавление функциональности поиска

Вот клиентские хуки Next.js, которые вы будете использовать для реализации функциональности поиска:

-   **`useSearchParams`**- Позволяет получить доступ к параметрам текущего URL. Например, параметры поиска для этого URL `/dashboard/invoices?page=1&query=pending` будут выглядеть следующим образом: `{page: '1', query: 'pending'}`.
-   **`usePathname`** - Позволяет прочитать имя пути текущего URL. Например, для маршрута `/dashboard/invoices`, `usePathname` вернет `'/dashboard/invoices'`.
-   **`useRouter`** - Обеспечивает навигацию между маршрутами внутри клиентских компонентов программным способом. Существует [несколько методов](https://nextjs.org/docs/app/api-reference/functions/use-router#userouter), которые вы можете использовать.

Вот краткий обзор шагов реализации:

1.  Перехватить ввод пользователя.
2.  Обновление URL с параметрами поиска.
3.  Поддерживайте синхронизацию URL с полем ввода.
4.  Обновите таблицу, чтобы отразить поисковый запрос.

### 1. Перехват пользовательского ввода

Перейдите в компонент `<Search>` (`/app/ui/search.tsx`), и вы заметите:

-   `"use client"` - Это клиентский компонент, что означает, что вы можете использовать обработчики событий и хуки.
-   `<input>` - поле ввода.

Создайте новую функцию `handleSearch` и добавьте обработчик `onChange` к элементу `<input>`. `onChange` будет вызывать `handleSearch` при каждом изменении значения ввода.

```ts title="/app/ui/search.tsx" hl_lines="10-12 22-24"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function Search({
    placeholder,
}: {
    placeholder: string;
}) {
    function handleSearch(term: string) {
        console.log(term);
    }

    return (
        <div className="relative flex flex-1 flex-shrink-0">
            <label htmlFor="search" className="sr-only">
                Search
            </label>
            <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                placeholder={placeholder}
                onChange={(e) => {
                    handleSearch(e.target.value);
                }}
            />
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
        </div>
    );
}
```

Убедитесь, что все работает правильно, открыв консоль в инструментах разработчика браузера, а затем наберите в поле поиска. Вы должны увидеть, как поисковый запрос записывается в консоль браузера.

Отлично! Вы перехватили поисковый ввод пользователя. Теперь вам нужно обновить URL, добавив в него поисковый запрос.

### 2. Обновление URL с параметрами поиска

Импортируйте хук `useSearchParams` из `next/navigation` и присвойте его переменной:

```ts title="/app/ui/search.tsx" hl_lines="4 7"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams } from 'next/navigation';

export default function Search() {
    const searchParams = useSearchParams();

    function handleSearch(term: string) {
        console.log(term);
    }
    // ...
}
```

Внутри `handleSearch` создайте новый экземпляр [`URLSearchParams`](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams), используя новую переменную `searchParams`.

```ts title="/app/ui/search.tsx" hl_lines="10"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams } from 'next/navigation';

export default function Search() {
    const searchParams = useSearchParams();

    function handleSearch(term: string) {
        const params = new URLSearchParams(searchParams);
    }
    // ...
}
```

`URLSearchParams` - это веб-интерфейс, предоставляющий методы для манипулирования параметрами запроса URL. Вместо того чтобы создавать сложный строковый литерал, вы можете использовать его для получения строки params типа `?page=1&query=a`.

Затем `set` строку params, основанную на вводе данных пользователем. Если введенное значение пустое, его нужно `delete`:

```ts title="/app/ui/search.tsx" hl_lines="11-15"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams } from 'next/navigation';

export default function Search() {
    const searchParams = useSearchParams();

    function handleSearch(term: string) {
        const params = new URLSearchParams(searchParams);
        if (term) {
            params.set('query', term);
        } else {
            params.delete('query');
        }
    }
    // ...
}
```

Теперь у вас есть строка запроса. Вы можете использовать хуки Next.js `useRouter` и `usePathname` для обновления URL.

Импортируйте `useRouter` и `usePathname` из `'next/navigation'` и используйте метод `replace` из `useRouter()` внутри `handleSearch`:

```ts title="/app/ui/search.tsx" hl_lines="4-8 12-13 22"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import {
    useSearchParams,
    usePathname,
    useRouter,
} from 'next/navigation';

export default function Search() {
    const searchParams = useSearchParams();
    const pathname = usePathname();
    const { replace } = useRouter();

    function handleSearch(term: string) {
        const params = new URLSearchParams(searchParams);
        if (term) {
            params.set('query', term);
        } else {
            params.delete('query');
        }
        replace(`${pathname}?${params.toString()}`);
    }
}
```

Вот краткое описание происходящего:

-   `${pathname}` - это текущий путь, в вашем случае `"/dashboard/invoices"`.
-   Когда пользователь набирает текст в строке поиска, `params.toString()` преобразует его в формат, удобный для URL.
-   `replace(${pathname}?${params.toString()})` обновляет URL с данными поиска пользователя. Например, `/dashboard/invoices?query=lee`, если пользователь ищет «Lee».
-   URL обновляется без перезагрузки страницы, благодаря навигации на стороне клиента Next.js, о которой вы узнали в главе [навигация между страницами](navigating-between-pages.md).

### 3. Обеспечение синхронизации URL и поля ввода

Чтобы убедиться, что поле ввода синхронизировано с URL и будет заполнено при совместном использовании, вы можете передать `defaultValue` в `input`, читая из `searchParams`:

```ts title="/app/ui/search.tsx" hl_lines="7"
<input
    className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
    placeholder={placeholder}
    onChange={(e) => {
        handleSearch(e.target.value);
    }}
    defaultValue={searchParams.get('query')?.toString()}
/>
```

!!!info "`defaultValue` vs. `value` / Контролируемые vs. Неконтролируемых"

    Если вы используете состояние для управления значением ввода, вы используете атрибут `value`, чтобы сделать его управляемым компонентом. Это означает, что React будет управлять состоянием ввода.

    Однако, поскольку вы не используете состояние, вы можете использовать `defaultValue`. Это означает, что нативный ввод будет управлять своим собственным состоянием. Это нормально, поскольку вы сохраняете поисковый запрос в URL вместо состояния.

### 4. Обновление таблицы

Наконец, вам нужно обновить компонент таблицы, чтобы отразить поисковый запрос.

Перейдите обратно на страницу счетов-фактур.

Компоненты страницы [принимают параметр `searchParams`](https://nextjs.org/docs/app/api-reference/file-conventions/page), поэтому вы можете передать текущие URL-параметры компоненту `<Table>`.

```ts title="/app/dashboard/invoices/page.tsx" hl_lines="9-17 32-40"
import Pagination from '@/app/ui/invoices/pagination';
import Search from '@/app/ui/search';
import Table from '@/app/ui/invoices/table';
import { CreateInvoice } from '@/app/ui/invoices/buttons';
import { lusitana } from '@/app/ui/fonts';
import { Suspense } from 'react';
import { InvoicesTableSkeleton } from '@/app/ui/skeletons';

export default async function Page(props: {
    searchParams?: Promise<{
        query?: string;
        page?: string;
    }>;
}) {
    const searchParams = await props.searchParams;
    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1;

    return (
        <div className="w-full">
            <div className="flex w-full items-center justify-between">
                <h1
                    className={`${lusitana.className} text-2xl`}
                >
                    Invoices
                </h1>
            </div>
            <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
                <Search placeholder="Search invoices..." />
                <CreateInvoice />
            </div>
            <Suspense
                key={query + currentPage}
                fallback={<InvoicesTableSkeleton />}
            >
                <Table
                    query={query}
                    currentPage={currentPage}
                />
            </Suspense>
            <div className="mt-5 flex w-full justify-center">
                {/* <Pagination totalPages={totalPages} /> */}
            </div>
        </div>
    );
}
```

Если вы перейдете к компоненту `<Table>`, то увидите, что два параметра, `query` и `currentPage`, передаются функции `fetchFilteredInvoices()`, которая возвращает счета-фактуры, соответствующие запросу.

```ts title="/app/ui/invoices/table.tsx"
// ...
export default async function InvoicesTable({
    query,
    currentPage,
}: {
    query: string;
    currentPage: number;
}) {
    const invoices = await fetchFilteredInvoices(
        query,
        currentPage
    );
    // ...
}
```

Внеся эти изменения, приступайте к тестированию. При поиске термина вы обновите URL-адрес, который отправит новый запрос на сервер, данные будут получены на сервере, и будут возвращены только те счета, которые соответствуют вашему запросу.

!!!note "Когда следует использовать хук `useSearchParams()`, а не свойство `searchParams`?"

    Вы могли заметить, что для извлечения параметров поиска используются два разных способа. Использование того или иного способа зависит от того, где вы работаете - на клиенте или на сервере.

    - `<Search>` - это клиентский компонент, поэтому вы использовали хук `useSearchParams()` для доступа к параметрам с клиента.
    - `<Table>` - это серверный компонент, который получает свои собственные данные, поэтому вы можете передавать свойство `searchParams` со страницы в компонент.

    Как правило, если вы хотите читать параметры с клиента, используйте хук `useSearchParams()`, так как это избавит вас от необходимости возвращаться на сервер.

### Лучшие практики: debouncing

Поздравляем! Вы реализовали поиск в Next.js! Но есть кое-что, что можно сделать для его оптимизации.

Внутри функции `handleSearch` добавьте следующий `console.log`:

```ts title="/app/ui/search.tsx" hl_lines="2"
function handleSearch(term: string) {
    console.log(`Searching... ${term}`);

    const params = new URLSearchParams(searchParams);
    if (term) {
        params.set('query', term);
    } else {
        params.delete('query');
    }
    replace(`${pathname}?${params.toString()}`);
}
```

Затем введите «Delba» в строку поиска и проверьте консоль в dev tools. Что происходит?

```sh title="Dev Tools Console"
Searching... D
Searching... De
Searching... Del
Searching... Delb
Searching... Delba
```

Вы обновляете URL при каждом нажатии клавиши, а значит, запрашиваете базу данных при каждом нажатии! Это не проблема, поскольку наше приложение небольшое, но представьте, если бы в вашем приложении были тысячи пользователей, каждый из которых отправлял бы новый запрос в вашу базу данных при каждом нажатии клавиши.

**Дебаунсинг** - это практика программирования, которая ограничивает скорость выполнения функции. В нашем случае вы хотите запрашивать базу данных только тогда, когда пользователь перестал набирать текст.

!!!note "Как работает дебаунсинг:"

    -   **Триггерное событие**: При наступлении события, которое должно быть отменено (например, нажатие клавиши в строке поиска), запускается таймер.
    -   **Ожидание**: Если до истечения срока действия таймера произойдет новое событие, таймер будет сброшен.
    -   **Исполнение**: Если таймер достигает конца обратного отсчета, выполняется функция дебаунсинга.

Вы можете реализовать дебаггинг несколькими способами, в том числе вручную создать собственную функцию дебаггинга. Для простоты мы будем использовать библиотеку под названием [use-debounce](https://www.npmjs.com/package/use-debounce).

Установите `use-debounce`:

```sh
pnpm i use-debounce
```

В компоненте `<Search>` импортируйте функцию `useDebouncedCallback`:

```ts title="/app/ui/search.tsx" hl_lines="2 5 15"
// ...
import { useDebouncedCallback } from 'use-debounce';

// Inside the Search Component...
const handleSearch = useDebouncedCallback((term) => {
    console.log(`Searching... ${term}`);

    const params = new URLSearchParams(searchParams);
    if (term) {
        params.set('query', term);
    } else {
        params.delete('query');
    }
    replace(`${pathname}?${params.toString()}`);
}, 300);
```

Эта функция будет оборачивать содержимое `handleSearch` и запускать код только через определенное время после того, как пользователь перестанет набирать текст (300 мс).

Теперь снова введите текст в строку поиска и откройте консоль в dev tools. Вы должны увидеть следующее:

```sh title="Dev Tools Console"
Searching... Delba
```

Дебаунсинг позволяет сократить количество запросов к базе данных и тем самым сэкономить ресурсы.

## Добавление пагинации

После внедрения функции поиска вы заметите, что в таблице отображается только 6 счетов за раз. Это связано с тем, что функция `fetchFilteredInvoices()` в `data.ts` возвращает максимум 6 счетов на страницу.

Добавление пагинации позволяет пользователям перемещаться по различным страницам, чтобы просмотреть все счета. Давайте посмотрим, как можно реализовать пагинацию с помощью параметров URL, как это было сделано с поиском.

Перейдите к компоненту `<Pagination/>`, и вы заметите, что это клиентский компонент. Вы не хотите получать данные на клиенте, так как это приведет к раскрытию секретов вашей базы данных (помните, что вы не используете слой API). Вместо этого вы можете получить данные на сервере и передать их компоненту в качестве параметра.

В файле `/dashboard/invoices/page.tsx` импортируйте новую функцию `fetchInvoicesPages` и передайте в качестве аргумента `query` из `searchParams`:

```ts title="/app/dashboard/invoices/page.tsx" hl_lines="2 13"
// ...
import { fetchInvoicesPages } from '@/app/lib/data';

export default async function Page(props: {
    searchParams?: Promise<{
        query?: string;
        page?: string;
    }>;
}) {
    const searchParams = await props.searchParams;
    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1;
    const totalPages = await fetchInvoicesPages(query);

    return (
		// ...
	);
}
```

Функция `fetchInvoicesPages` возвращает общее количество страниц по поисковому запросу. Например, если есть 12 счетов-фактур, соответствующих поисковому запросу, и на каждой странице отображается 6 счетов-фактур, то общее количество страниц будет равно 2.

Далее передайте параметр `totalPages` компоненту `<Pagination/>`:

```ts title="/app/dashboard/invoices/page.tsx" hl_lines="37"
// ...

export default async function Page(props: {
    searchParams?: Promise<{
        query?: string;
        page?: string;
    }>;
}) {
    const searchParams = await props.searchParams;
    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1;
    const totalPages = await fetchInvoicesPages(query);

    return (
        <div className="w-full">
            <div className="flex w-full items-center justify-between">
                <h1
                    className={`${lusitana.className} text-2xl`}
                >
                    Invoices
                </h1>
            </div>
            <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
                <Search placeholder="Search invoices..." />
                <CreateInvoice />
            </div>
            <Suspense
                key={query + currentPage}
                fallback={<InvoicesTableSkeleton />}
            >
                <Table
                    query={query}
                    currentPage={currentPage}
                />
            </Suspense>
            <div className="mt-5 flex w-full justify-center">
                <Pagination totalPages={totalPages} />
            </div>
        </div>
    );
}
```

Перейдите к компоненту `<Pagination/>` и импортируйте хуки `usePathname` и `useSearchParams`. Мы будем использовать их для получения текущей страницы и установки новой страницы. Не забудьте также откомментировать код в этом компоненте. Ваше приложение временно сломается, так как вы еще не реализовали логику `<Pagination/>`. Давайте сделаем это сейчас!

```ts title="/app/ui/invoices/pagination.tsx" hl_lines="10-13 20-23"
'use client';

import {
    ArrowLeftIcon,
    ArrowRightIcon,
} from '@heroicons/react/24/outline';
import clsx from 'clsx';
import Link from 'next/link';
import { generatePagination } from '@/app/lib/utils';
import {
    usePathname,
    useSearchParams,
} from 'next/navigation';

export default function Pagination({
    totalPages,
}: {
    totalPages: number;
}) {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const currentPage =
        Number(searchParams.get('page')) || 1;

    // ...
}
```

Далее создайте новую функцию внутри компонента `<Pagination>` под названием `createPageURL`. Аналогично поиску, вы будете использовать `URLSearchParams` для задания номера новой страницы и `pathName` для создания строки URL.

```ts title="/app/ui/invoices/pagination.tsx" hl_lines="25-29"
'use client';

import {
    ArrowLeftIcon,
    ArrowRightIcon,
} from '@heroicons/react/24/outline';
import clsx from 'clsx';
import Link from 'next/link';
import { generatePagination } from '@/app/lib/utils';
import {
    usePathname,
    useSearchParams,
} from 'next/navigation';

export default function Pagination({
    totalPages,
}: {
    totalPages: number;
}) {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const currentPage =
        Number(searchParams.get('page')) || 1;

    const createPageURL = (pageNumber: number | string) => {
        const params = new URLSearchParams(searchParams);
        params.set('page', pageNumber.toString());
        return `${pathname}?${params.toString()}`;
    };

    // ...
}
```

Вот краткое описание происходящего:

-   `createPageURL` создает экземпляр текущих параметров поиска.
-   Затем он обновляет параметр `page` до указанного номера страницы.
-   Наконец, он создает полный URL, используя имя пути и обновленные параметры поиска.

Остальная часть компонента `<Pagination>` занимается стилизацией и различными состояниями (первое, последнее, активное, отключенное и т. д.). Мы не будем вдаваться в подробности в рамках данного курса, но не стесняйтесь просмотреть код, чтобы увидеть, где вызывается `createPageURL`.

Наконец, когда пользователь набирает новый поисковый запрос, вы хотите сбросить номер страницы на `1`. Вы можете сделать это, обновив функцию `handleSearch` в компоненте `<Search>`:

```ts title="/app/ui/search.tsx" hl_lines="22"
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import {
    usePathname,
    useRouter,
    useSearchParams,
} from 'next/navigation';
import { useDebouncedCallback } from 'use-debounce';

export default function Search({
    placeholder,
}: {
    placeholder: string;
}) {
    const searchParams = useSearchParams();
    const { replace } = useRouter();
    const pathname = usePathname();

    const handleSearch = useDebouncedCallback((term) => {
        const params = new URLSearchParams(searchParams);
        params.set('page', '1');
        if (term) {
            params.set('query', term);
        } else {
            params.delete('query');
        }
        replace(`${pathname}?${params.toString()}`);
    }, 300);
}
```

## Резюме

Поздравляем! Вы только что реализовали поиск и пагинацию с помощью параметров поиска URL и API Next.js.

Подводя итог, можно сказать, что в этой главе

-   Вы реализовали поиск и пагинацию с помощью параметров поиска URL вместо состояния клиента.
-   Вы получали данные на сервере.
-   Вы используете крючок маршрутизатора `useRouter` для более плавных переходов на стороне клиента.

Эти паттерны отличаются от тех, к которым вы привыкли при работе с React на стороне клиента, но, надеемся, теперь вы лучше понимаете преимущества использования параметров поиска по URL и передачи этого состояния на сервер.

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/adding-search-and-pagination></small>
