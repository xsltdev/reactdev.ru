---
description: Now that you've created and seeded your database, let's discuss the different ways you can fetch data for your application, and build out your dashboard overview page.
---

# Fetching Data

Now that you've created and seeded your database, let's discuss the different ways you can fetch data for your application, and build out your dashboard overview page.

!!!tip "Here are the topics we’ll cover"

    -   Learn about some approaches to fetching data: APIs, ORMs, SQL, etc.
    -   How Server Components can help you access back-end resources more securely.
    -   What network waterfalls are.
    -   How to implement parallel data fetching using a JavaScript Pattern.

## Choosing how to fetch data

### API layer

APIs are an intermediary layer between your application code and database. There are a few cases where you might use an API:

-   If you're using third-party services that provide an API.
-   If you're fetching data from the client, you want to have an API layer that runs on the server to avoid exposing your database secrets to the client.

In Next.js, you can create API endpoints using [Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers).

### Database queries

When you're creating a full-stack application, you'll also need to write logic to interact with your database. For [relational databases](https://aws.amazon.com/relational-database/) like Postgres, you can do this with SQL or with an [ORM](https://vercel.com/docs/storage/vercel-postgres/using-an-orm).

There are a few cases where you have to write database queries:

-   When creating your API endpoints, you need to write logic to interact with your database.
-   If you are using React Server Components (fetching data on the server), you can skip the API layer, and query your database directly without risking exposing your database secrets to the client.

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
