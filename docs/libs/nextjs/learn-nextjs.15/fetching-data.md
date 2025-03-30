---
description: Теперь, когда вы создали и запустили свою базу данных, давайте обсудим различные способы получения данных для вашего приложения и создадим страницу обзора дашборда.
---

# Получение данных

Теперь, когда вы создали и засеяли свою базу данных, давайте обсудим различные способы получения данных для вашего приложения и построим обзорную страницу дашборда.

!!!tip "Вот темы, которые мы рассмотрим"

    -   Узнайте о некоторых подходах к получению данных: API, ORM, SQL и т. д.
    - Как серверные компоненты могут помочь вам получить более безопасный доступ к внутренним ресурсам.
    - Что такое сетевые водопады.
    - Как реализовать параллельную выборку данных с помощью JavaScript-паттерна.

## Выбор способа получения данных.

### Слой API

API - это промежуточный слой между кодом вашего приложения и базой данных. Есть несколько случаев, когда вы можете использовать API:

-   Если вы используете сторонние сервисы, которые предоставляют API.
-   Если вы получаете данные от клиента, вам нужен слой API, работающий на сервере, чтобы не раскрывать клиенту секреты вашей базы данных.

В Next.js вы можете создавать конечные точки API с помощью [Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers).

### Запросы к базе данных

При создании приложения полного стека вам также потребуется написать логику для взаимодействия с базой данных. Для [реляционных баз данных](https://aws.amazon.com/relational-database/), таких как Postgres, вы можете сделать это с помощью SQL или [ORM](https://vercel.com/docs/storage/vercel-postgres/using-an-orm).

Есть несколько случаев, когда вам придется писать запросы к базе данных:

-   При создании конечных точек API вам нужно написать логику для взаимодействия с базой данных.
-   Если вы используете React Server Components (получение данных на сервере), вы можете пропустить слой API и запрашивать базу данных напрямую, не рискуя раскрыть секреты базы данных клиенту.

<?quiz?>

question: In which of these scenarios should you not query your database directly?
answer-correct: When you're fetching data on the client
answer: When you're fetching data on the server
answer: When you're creating your own API layer to interact with your database
content:

<p>That's right, you should not query your database directly when fetching data on the client as this would expose your database secrets.</p>
<?/quiz?>

Let's learn more about React Server Components.

### Using Server Components to fetch data

By default, Next.js applications use **React Server Components**. Fetching data with Server Components is a relatively new approach and there are a few benefits of using them:

-   Server Components support JavaScript Promises, providing a solution for asynchronous tasks like data fetching natively. You can use `async/await` syntax without needing `useEffect`, `useState` or other data fetching libraries.
-   Server Components run on the server, so you can keep expensive data fetches and logic on the server, only sending the result to the client.
-   Since Server Components run on the server, you can query the database directly without an additional API layer. This saves you from writing and maintaining additional code.

<?quiz?>

question: What's one advantage of using React Server Components to fetch data?
answer: They automatically protect you from SQL injection.
answer-correct: They allow you to query the database directly from the server without an additional API layer.
answer: They require you to use an API layer and create endpoints.
content:

<p>Server components allow you fetch data directly from your database.</p>
<?/quiz?>

## Using SQL

For your dashboard application, you'll write database queries using the [postgres.js](https://github.com/porsager/postgres) library and SQL. There are a few reasons why we'll be using SQL:

-   SQL is the industry standard for querying relational databases (e.g. ORMs generate SQL under the hood).
-   Having a basic understanding of SQL can help you understand the fundamentals of relational databases, allowing you to apply your knowledge to other tools.
-   SQL is versatile, allowing you to fetch and manipulate specific data.
-   The `postgres.js` library provides protection against [SQL injections](https://github.com/porsager/postgres?tab=readme-ov-file#query-parameters).

Don't worry if you haven't used SQL before - we have provided the queries for you.

Go to `/app/lib/data.ts`. Here you'll see that we're using `postgres`. The `sql` [function](https://github.com/porsager/postgres) allows you to query your database:

```ts title="/app/lib/data.ts"
import postgres from 'postgres';

const sql = postgres(process.env.POSTGRES_URL!, {
    ssl: 'require',
});

// ...
```

You can call `sql` anywhere on the server, like a Server Component. But to allow you to navigate the components more easily, we've kept all the data queries in the `data.ts` file, and you can import them into the components.

<?quiz?>

question: What does SQL allow you to do in terms of fetching data?
answer: Fetch all your data indiscriminately
answer-correct: Fetch and manipulate specific data
answer: Automatically cache data for better performance
answer: Change the database schema on the fly
content:

<p>SQL allows you to write targeted queries to fetch and manipulate specific data</p>
<?/quiz?>

!!!note ""

    If you used your own database provider in Chapter 6, you'll need to update the database queries to work with your provider. You can find the queries in `/app/lib/data.ts`.

## Fetching data for the dashboard overview page

Now that you understand different ways of fetching data, let's fetch data for the dashboard overview page. Navigate to `/app/dashboard/page.tsx`, paste the following code, and spend some time exploring it:

```ts title="/app/dashboard/page.tsx"
import { Card } from '@/app/ui/dashboard/cards';
import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import LatestInvoices from '@/app/ui/dashboard/latest-invoices';
import { lusitana } from '@/app/ui/fonts';

export default async function Page() {
    return (
        <main>
            <h1
                className={`${lusitana.className} mb-4 text-xl md:text-2xl`}
            >
                Dashboard
            </h1>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {/* <Card title="Collected" value={totalPaidInvoices} type="collected" /> */}
                {/* <Card title="Pending" value={totalPendingInvoices} type="pending" /> */}
                {/* <Card title="Total Invoices" value={numberOfInvoices} type="invoices" /> */}
                {/* <Card
          title="Total Customers"
          value={numberOfCustomers}
          type="customers"
        /> */}
            </div>
            <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
                {/* <RevenueChart revenue={revenue}  /> */}
                {/* <LatestInvoices latestInvoices={latestInvoices} /> */}
            </div>
        </main>
    );
}
```

The code above is intentionally commented out. We will now begin to example each piece.

-   The `page` is an **async** server component. This allows you to use `await` to fetch data.
-   There are also 3 components which receive data: `<Card>`, `<RevenueChart>`, and `<LatestInvoices>`. They are currently commented out and not yet implemented.

## Fetching data for `<RevenueChart/>`

To fetch data for the `<RevenueChart/>` component, import the `fetchRevenue` function from `data.ts` and call it inside your component:

```ts title="/app/dashboard/page.tsx" hl_lines="5 7-8"
import { Card } from '@/app/ui/dashboard/cards';
import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import LatestInvoices from '@/app/ui/dashboard/latest-invoices';
import { lusitana } from '@/app/ui/fonts';
import { fetchRevenue } from '@/app/lib/data';

export default async function Page() {
    const revenue = await fetchRevenue();
    // ...
}
```

Next, let's do the following:

-   Uncomment the `<RevenueChart/>` component.
-   Navigate to the component file (`/app/ui/dashboard/revenue-chart.tsx`) and uncomment the code inside it.
-   Check `localhost:3000` and you should see a chart that uses `revenue` data.

![Revenue chart showing the total revenue for the last 12 months](recent-revenue.png)

Let's continue importing more data and displaying it on the dashboard.

## Fetching data for `<LatestInvoices/>`

For the `<LatestInvoices />` component, we need to get the latest 5 invoices, sorted by date.

You could fetch all the invoices and sort through them using JavaScript. This isn't a problem as our data is small, but as your application grows, it can significantly increase the amount of data transferred on each request and the JavaScript required to sort through it.

Instead of sorting through the latest invoices in-memory, you can use an SQL query to fetch only the last 5 invoices. For example, this is the SQL query from your `data.ts` file:

```ts title="/app/lib/data.ts"
// Fetch the last 5 invoices, sorted by date
const data = await sql<LatestInvoiceRaw[]>`
  SELECT invoices.amount, customers.name, customers.image_url, customers.email
  FROM invoices
  JOIN customers ON invoices.customer_id = customers.id
  ORDER BY invoices.date DESC
  LIMIT 5`;
```

In your page, import the `fetchLatestInvoices` function:

```ts title="/app/dashboard/page.tsx" hl_lines="5-8 12"
import { Card } from '@/app/ui/dashboard/cards';
import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import LatestInvoices from '@/app/ui/dashboard/latest-invoices';
import { lusitana } from '@/app/ui/fonts';
import {
    fetchRevenue,
    fetchLatestInvoices,
} from '@/app/lib/data';

export default async function Page() {
    const revenue = await fetchRevenue();
    const latestInvoices = await fetchLatestInvoices();
    // ...
}
```

Then, uncomment the `<LatestInvoices />` component. You will also need to uncomment the relevant code in the `<LatestInvoices />` component itself, located at `/app/ui/dashboard/latest-invoices`.

If you visit your localhost, you should see that only the last 5 are returned from the database. Hopefully, you're beginning to see the advantages of querying your database directly!

![Latest invoices component alongside the revenue chart](latest-invoices.png)

## Practice: Fetch data for the `<Card>` components

Now it's your turn to fetch data for the `<Card>` components. The cards will display the following data:

-   Total amount of invoices collected.
-   Total amount of invoices pending.
-   Total number of invoices.
-   Total number of customers.

Again, you might be tempted to fetch all the invoices and customers, and use JavaScript to manipulate the data. For example, you could use `Array.length` to get the total number of invoices and customers:

```ts
const totalInvoices = allInvoices.length;
const totalCustomers = allCustomers.length;
```

But with SQL, you can fetch only the data you need. It's a little longer than using `Array.length`, but it means less data needs to be transferred during the request. This is the SQL alternative:

```ts title="/app/lib/data.ts"
const invoiceCountPromise = sql`SELECT COUNT(*) FROM invoices`;
const customerCountPromise = sql`SELECT COUNT(*) FROM customers`;
```

The function you will need to import is called `fetchCardData`. You will need to destructure the values returned from the function.

!!!tip "Hint"

    -   Check the card components to see what data they need.
    -   Check the data.ts file to see what the function returns.

Once you're ready, expand the toggle below for the final code:

???note "Reveal the solution"

    ```ts title="/app/dashboard/page.tsx" hl_lines="8 14-19"
    import { Card } from '@/app/ui/dashboard/cards';
    import RevenueChart from '@/app/ui/dashboard/revenue-chart';
    import LatestInvoices from '@/app/ui/dashboard/latest-invoices';
    import { lusitana } from '@/app/ui/fonts';
    import {
    	fetchRevenue,
    	fetchLatestInvoices,
    	fetchCardData,
    } from '@/app/lib/data';

    export default async function Page() {
    	const revenue = await fetchRevenue();
    	const latestInvoices = await fetchLatestInvoices();
    	const {
    		numberOfInvoices,
    		numberOfCustomers,
    		totalPaidInvoices,
    		totalPendingInvoices,
    	} = await fetchCardData();

    	return (
    		<main>
    			<h1
    				className={`${lusitana.className} mb-4 text-xl md:text-2xl`}
    			>
    				Dashboard
    			</h1>
    			<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
    				<Card
    					title="Collected"
    					value={totalPaidInvoices}
    					type="collected"
    				/>
    				<Card
    					title="Pending"
    					value={totalPendingInvoices}
    					type="pending"
    				/>
    				<Card
    					title="Total Invoices"
    					value={numberOfInvoices}
    					type="invoices"
    				/>
    				<Card
    					title="Total Customers"
    					value={numberOfCustomers}
    					type="customers"
    				/>
    			</div>
    			<div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
    				<RevenueChart revenue={revenue} />
    				<LatestInvoices
    					latestInvoices={latestInvoices}
    				/>
    			</div>
    		</main>
    	);
    }
    ```

Great! You've now fetched all the data for the dashboard overview page. Your page should look like this:

![Dashboard page with all the data fetched](complete-dashboard.png)

However... there are two things you need to be aware of:

-   The data requests are unintentionally blocking each other, creating a **request waterfall**.
-   By default, Next.js **prerenders** routes to improve performance, this is called Static Rendering. So if your data changes, it won't be reflected in your dashboard.

Let's discuss number 1 in this chapter, then look into detail at number 2 in the next chapter.

## What are request waterfalls?

A "waterfall" refers to a sequence of network requests that depend on the completion of previous requests. In the case of data fetching, each request can only begin once the previous request has returned data.

![Diagram showing time with sequential data fetching and parallel data fetching](sequential-parallel-data-fetching.png)

For example, we need to wait for `fetchRevenue()` to execute before `fetchLatestInvoices()` can start running, and so on.

```ts title="/app/dashboard/page.tsx"
const revenue = await fetchRevenue();
const latestInvoices = await fetchLatestInvoices(); // wait for fetchRevenue() to finish
const {
    numberOfInvoices,
    numberOfCustomers,
    totalPaidInvoices,
    totalPendingInvoices,
} = await fetchCardData(); // wait for fetchLatestInvoices() to finish
```

This pattern is not necessarily bad. There may be cases where you want waterfalls because you want a condition to be satisfied before you make the next request. For example, you might want to fetch a user's ID and profile information first. Once you have the ID, you might then proceed to fetch their list of friends. In this case, each request is contingent on the data returned from the previous request.

However, this behavior can also be unintentional and impact performance.

<?quiz?>

question: When might you want to use a waterfall pattern?
answer-correct: To satisfy a condition before making the next request
answer: To make all requests simultaneously
answer: To reduce the server load by doing one fetch at a time
content:

<p>For example, you might want to fetch a user's ID and profile information first. Once you have the ID, you might then proceed to fetch their list of friends.</p>
<?/quiz?>

## Parallel data fetching

A common way to avoid waterfalls is to initiate all data requests at the same time - in parallel.

In JavaScript, you can use the [`Promise.all()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) or [`Promise.allSettled()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled) functions to initiate all promises at the same time. For example, in `data.ts`, we're using `Promise.all()` in the `fetchCardData()` function:

```ts title="/app/lib/data.ts" hl_lines="10-14"
export async function fetchCardData() {
    try {
        const invoiceCountPromise = sql`SELECT COUNT(*) FROM invoices`;
        const customerCountPromise = sql`SELECT COUNT(*) FROM customers`;
        const invoiceStatusPromise = sql`SELECT
			SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) AS "paid",
			SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) AS "pending"
			FROM invoices`;

        const data = await Promise.all([
            invoiceCountPromise,
            customerCountPromise,
            invoiceStatusPromise,
        ]);
        // ...
    } catch (e) {
        // ...
    }
}
```

By using this pattern, you can:

-   Start executing all data fetches at the same time, which is faster than waiting for each request to complete in a waterfall.
-   Use a native JavaScript pattern that can be applied to any library or framework.

However, there is one **disadvantage** of relying only on this JavaScript pattern: what happens if one data request is slower than all the others? Let's find out more in the next chapter.
