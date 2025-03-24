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
