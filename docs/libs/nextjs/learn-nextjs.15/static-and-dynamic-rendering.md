---
description: Static and Dynamic Rendering
---

# Static and Dynamic Rendering

In the previous chapter, you fetched data for the Dashboard Overview page. However, we briefly discussed two limitations of the current setup:

-   The data requests are creating an unintentional waterfall.
-   The dashboard is static, so any data updates will not be reflected on your application.

!!!tip "Here are the topics we’ll cover"

-   What static rendering is and how it can improve your application's performance.
-   What dynamic rendering is and when to use it.
-   Different approaches to make your dashboard dynamic.
-   Simulate a slow data fetch to see what happens.

## What is Static Rendering?

With static rendering, data fetching and rendering happens on the server at build time (when you deploy) or when [revalidating data](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating#revalidating-data).

Whenever a user visits your application, the cached result is served. There are a couple of benefits of static rendering:

-   **Faster Websites** - Prerendered content can be cached and globally distributed when deployed to platforms like Vercel. This ensures that users around the world can access your website's content more quickly and reliably.
-   **Reduced Server Load** - Because the content is cached, your server does not have to dynamically generate content for each user request. This can reduce compute costs.
-   **SEO** - Prerendered content is easier for search engine crawlers to index, as the content is already available when the page loads. This can lead to improved search engine rankings.

Static rendering is useful for UI with **no data** or **data that is shared across users**, such as a static blog post or a product page. It might not be a good fit for a dashboard that has personalized data which is regularly updated.

The opposite of static rendering is dynamic rendering.

<?quiz?>

question: Why might static rendering not be a good fit for a dashboard app?
answer: Because it makes the website slower
answer: Because the server load will increase
answer-correct: Because the application will not reflect the latest data changes
answer: Because you need a Content Delivery Network
content:

<p>When your data updates, you want to show the latest changes in your dashboard. Static Rendering is not a good fit for this use case.</p>
<?/quiz?>

## What is Dynamic Rendering?

With dynamic rendering, content is rendered on the server for each user at **request time** (when the user visits the page). There are a couple of benefits of dynamic rendering:

-   **Real-Time Data** - Dynamic rendering allows your application to display real-time or frequently updated data. This is ideal for applications where data changes often.
-   **User-Specific Content** - It's easier to serve personalized content, such as dashboards or user profiles, and update the data based on user interaction.
-   **Request Time Information** - Dynamic rendering allows you to access information that can only be known at request time, such as cookies or the URL search parameters.

<?quiz?>

question: What kind of information is typically only known at request time?
answer: Database schema
answer: URL Path
answer-correct: Cookies and URL search params
content:

<p>Cookies and URL search params</p>
<?/quiz?>

## Simulating a Slow Data Fetch

The dashboard application we're building is dynamic.

However, there is still one problem mentioned in the previous chapter. What happens if one data request is slower than all the others?

Let's simulate a slow data fetch. In `app/lib/data.ts`, uncomment the `console.log` and `setTimeout` inside `fetchRevenue()`:

```ts title="/app/lib/data.ts" hl_lines="5-8 14-16"
export async function fetchRevenue() {
    try {
        // We artificially delay a response for demo purposes.
        // Don't do this in production :)
        console.log('Fetching revenue data...');
        await new Promise((resolve) =>
            setTimeout(resolve, 3000)
        );

        const data = await sql<
            Revenue[]
        >`SELECT * FROM revenue`;

        console.log(
            'Data fetch completed after 3 seconds.'
        );

        return data;
    } catch (error) {
        console.error('Database Error:', error);
        throw new Error('Failed to fetch revenue data.');
    }
}
```

Now open <http://localhost:3000/dashboard/> in a new tab and notice how the page takes longer to load. In your terminal, you should also see the following messages:

```sh
Fetching revenue data...
Data fetch completed after 3 seconds.
```

Here, you've added an artificial 3-second delay to simulate a slow data fetch. The result is that now your whole page is blocked from showing UI to the visitor while the data is being fetched. Which brings us to a common challenge developers have to solve:

With dynamic rendering, **your application is only as fast as your slowest data fetch**.

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/static-and-dynamic-rendering></small>
