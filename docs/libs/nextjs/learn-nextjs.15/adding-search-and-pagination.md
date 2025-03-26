---
description: learn how to add search and pagination
---

# Adding Search and Pagination

In the previous chapter, you improved your dashboard's initial loading performance with streaming. Now let's move on to the `/invoices` page, and learn how to add search and pagination.

!!!tip "Here are the topics we’ll cover"

-   Learn how to use the Next.js APIs: useSearchParams, usePathname, and useRouter.
-   Implement search and pagination using URL search params.

## Starting code

Inside your `/dashboard/invoices/page.tsx` file, paste the following code:

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

Spend some time familiarizing yourself with the page and the components you'll be working with:

-   `<Search/>` allows users to search for specific invoices.
-   `<Pagination/>` allows users to navigate between pages of invoices.
-   `<Table/>` displays the invoices.

Your search functionality will span the client and the server. When a user searches for an invoice on the client, the URL params will be updated, data will be fetched on the server, and the table will re-render on the server with the new data.

## Why use URL search params?

As mentioned above, you'll be using URL search params to manage the search state. This pattern may be new if you're used to doing it with client side state.

There are a couple of benefits of implementing search with URL params:

-   **Bookmarkable and shareable URLs**: Since the search parameters are in the URL, users can bookmark the current state of the application, including their search queries and filters, for future reference or sharing.
-   **Server-side rendering**: URL parameters can be directly consumed on the server to render the initial state, making it easier to handle server rendering.
-   **Analytics and tracking**: Having search queries and filters directly in the URL makes it easier to track user behavior without requiring additional client-side logic.

## Adding the search functionality

These are the Next.js client hooks that you'll use to implement the search functionality:

-   **`useSearchParams`**- Allows you to access the parameters of the current URL. For example, the search params for this URL `/dashboard/invoices?page=1&query=pending` would look like this: `{page: '1', query: 'pending'}`.
-   **`usePathname`** - Lets you read the current URL's pathname. For example, for the route `/dashboard/invoices`, `usePathname` would return `'/dashboard/invoices'`.
-   **`useRouter`** - Enables navigation between routes within client components programmatically. There are [multiple methods](https://nextjs.org/docs/app/api-reference/functions/use-router#userouter) you can use.

Here's a quick overview of the implementation steps:

1.  Capture the user's input.
2.  Update the URL with the search params.
3.  Keep the URL in sync with the input field.
4.  Update the table to reflect the search query.

### 1. Capture the user's input

Go into the `<Search>` Component (`/app/ui/search.tsx`), and you'll notice:

-   `"use client"` - This is a Client Component, which means you can use event listeners and hooks.
-   `<input>` - This is the search input.

Create a new `handleSearch` function, and add an `onChange` listener to the `<input>` element. `onChange` will invoke `handleSearch` whenever the input value changes.

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

Verify that it's working correctly by opening the console in your browser developer tools, then type into the search field. You should see the search term logged to the browser console.

Great! You're capturing the user's search input. Now, you need to update the URL with the search term.

### 2. Update the URL with the search params

Import the `useSearchParams` hook from `next/navigation` and assign it to a variable:

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

Inside `handleSearch`, create a new [`URLSearchParams`](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams) instance using your new `searchParams` variable.

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

`URLSearchParams` is a Web API that provides utility methods for manipulating the URL query parameters. Instead of creating a complex string literal, you can use it to get the params string like `?page=1&query=a`.

Next, `set` the params string based on the user’s input. If the input is empty, you want to `delete` it:

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

Now that you have the query string. You can use Next.js's `useRouter` and `usePathname` hooks to update the URL.

Import `useRouter` and `usePathname` from `'next/navigation'`, and use the `replace` method from `useRouter()` inside `handleSearch`:

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

Here's a breakdown of what's happening:

-   `${pathname}` is the current path, in your case, `"/dashboard/invoices"`.
-   As the user types into the search bar, `params.toString()` translates this input into a URL-friendly format.
-   `replace(${pathname}?${params.toString()})` updates the URL with the user's search data. For example, `/dashboard/invoices?query=lee` if the user searches for "Lee".
-   The URL is updated without reloading the page, thanks to Next.js's client-side navigation (which you learned about in the chapter on [navigating between pages](navigating-between-pages.md).

### 3. Keeping the URL and input in sync

To ensure the input field is in sync with the URL and will be populated when sharing, you can pass a `defaultValue` to input by reading from `searchParams`:

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

!!!info "`defaultValue` vs. `value` / Controlled vs. Uncontrolled"

    If you're using state to manage the value of an input, you'd use the `value` attribute to make it a controlled component. This means React would manage the input's state.

    However, since you're not using state, you can use `defaultValue`. This means the native input will manage its own state. This is okay since you're saving the search query to the URL instead of state.

### 4. Updating the table

Finally, you need to update the table component to reflect the search query.

Navigate back to the invoices page.

Page components [accept a prop called `searchParams`](https://nextjs.org/docs/app/api-reference/file-conventions/page), so you can pass the current URL params to the `<Table>` component.

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

If you navigate to the `<Table>` Component, you'll see that the two props, `query` and `currentPage`, are passed to the `fetchFilteredInvoices()` function which returns the invoices that match the query.

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

With these changes in place, go ahead and test it out. If you search for a term, you'll update the URL, which will send a new request to the server, data will be fetched on the server, and only the invoices that match your query will be returned.

!!!note "When to use the `useSearchParams()` hook vs. the `searchParams` prop?"

    You might have noticed you used two different ways to extract search params. Whether you use one or the other depends on whether you're working on the client or the server.

    -   `<Search>` is a Client Component, so you used the `useSearchParams()` hook to access the params from the client.
    -   `<Table>` is a Server Component that fetches its own data, so you can pass the `searchParams` prop from the page to the component.

    As a general rule, if you want to read the params from the client, use the `useSearchParams()` hook as this avoids having to go back to the server.

### Best practice: Debouncing

Congratulations! You've implemented search with Next.js! But there's something you can do to optimize it.

Inside your `handleSearch` function, add the following `console.log`:

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

Then type "Delba" into your search bar and check the console in dev tools. What is happening?

```sh title="Dev Tools Console"
Searching... D
Searching... De
Searching... Del
Searching... Delb
Searching... Delba
```

You're updating the URL on every keystroke, and therefore querying your database on every keystroke! This isn't a problem as our application is small, but imagine if your application had thousands of users, each sending a new request to your database on each keystroke.

**Debouncing** is a programming practice that limits the rate at which a function can fire. In our case, you only want to query the database when the user has stopped typing.

!!!note "How Debouncing Works:"

    -   **Trigger Event**: When an event that should be debounced (like a keystroke in the search box) occurs, a timer starts.
    -   **Wait**: If a new event occurs before the timer expires, the timer is reset.
    -   **Execution**: If the timer reaches the end of its countdown, the debounced function is executed.

You can implement debouncing in a few ways, including manually creating your own debounce function. To keep things simple, we'll use a library called [use-debounce](https://www.npmjs.com/package/use-debounce).

Install `use-debounce`:

```sh
pnpm i use-debounce
```

In your `<Search>` Component, import a function called `useDebouncedCallback`:

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

This function will wrap the contents of `handleSearch`, and only run the code after a specific time once the user has stopped typing (300ms).

Now type in your search bar again, and open the console in dev tools. You should see the following:

```sh title="Dev Tools Console"
Searching... Delba
```

By debouncing, you can reduce the number of requests sent to your database, thus saving resources.

<?quiz?>

question: What problem does debouncing solve in the search feature?
answer: It speeds up database queries
answer: It makes the URL bookmarkable
answer-correct: It prevents a new database query on every keystroke
answer: It helps in SEO optimization
content:

<p>That's right! Debouncing prevents a new database query on every keystroke, thus saving resources.</p>
<?/quiz?>

## Adding pagination

After introducing the search feature, you'll notice the table displays only 6 invoices at a time. This is because the `fetchFilteredInvoices()` function in `data.ts` returns a maximum of 6 invoices per page.

Adding pagination allows users to navigate through the different pages to view all the invoices. Let's see how you can implement pagination using URL params, just like you did with search.

Navigate to the `<Pagination/>` component and you'll notice that it's a Client Component. You don't want to fetch data on the client as this would expose your database secrets (remember, you're not using an API layer). Instead, you can fetch the data on the server, and pass it to the component as a prop.

In `/dashboard/invoices/page.tsx`, import a new function called `fetchInvoicesPages` and pass the `query` from `searchParams` as an argument:

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

`fetchInvoicesPages` returns the total number of pages based on the search query. For example, if there are 12 invoices that match the search query, and each page displays 6 invoices, then the total number of pages would be 2.

Next, pass the `totalPages` prop to the `<Pagination/>` component:

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

Navigate to the `<Pagination/>` component and import the `usePathname` and `useSearchParams` hooks. We will use this to get the current page and set the new page. Make sure to also uncomment the code in this component. Your application will break temporarily as you haven't implemented the `<Pagination/>` logic yet. Let's do that now!

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

Next, create a new function inside the `<Pagination>` Component called `createPageURL`. Similarly to the search, you'll use `URLSearchParams` to set the new page number, and `pathName` to create the URL string.

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

Here's a breakdown of what's happening:

-   `createPageURL` creates an instance of the current search parameters.
-   Then, it updates the "page" parameter to the provided page number.
-   Finally, it constructs the full URL using the pathname and updated search parameters.

The rest of the `<Pagination>` component deals with styling and different states (first, last, active, disabled, etc). We won't go into detail for this course, but feel free to look through the code to see where `createPageURL` is being called.

Finally, when the user types a new search query, you want to reset the page number to 1. You can do this by updating the `handleSearch` function in your `<Search>` component:

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

## Summary

Congratulations! You've just implemented search and pagination using URL search params and Next.js APIs.

To summarize, in this chapter:

-   You've handled search and pagination with URL search parameters instead of client state.
-   You've fetched data on the server.
-   You're using the `useRouter` router hook for smoother, client-side transitions.

These patterns are different from what you may be used to when working with client-side React, but hopefully, you now better understand the benefits of using URL search params and lifting this state to the server.

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/adding-search-and-pagination></small>
