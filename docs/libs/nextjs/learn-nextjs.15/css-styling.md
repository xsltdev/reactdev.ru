---
description: Currently, your home page doesn't have any styles. Let's look at the different ways you can style your Next.js application.
subtitle: Chapter 2
---

# CSS Styling

Currently, your home page doesn't have any styles. Let's look at the different ways you can style your Next.js application.

## In this chapter...

Here are the topics we’ll cover

-   How to add a global CSS file to your application.
-   Two different ways of styling: Tailwind and CSS modules.
-   How to conditionally add class names with the clsx utility package.

## Global styles

If you look inside the `/app/ui` folder, you'll see a file called `global.css`. You can use this file to add CSS rules to **all** the routes in your application - such as CSS reset rules, site-wide styles for HTML elements like links, and more.

You can import `global.css` in any component in your application, but it's usually good practice to add it to your top-level component. In Next.js, this is the [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layouts) (more on this later).

Add global styles to your application by navigating to `/app/layout.tsx` and importing the `global.css` file:

```ts title="/app/layout.tsx" hl_lines="1"
import '@/app/ui/global.css';

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
```

With the development server still running, save your changes and preview them in the browser. Your home page should now look like this:

![Styled page with the logo 'Acme', a description, and login link.](home-page-with-tailwind.png)

But wait a second, you didn't add any CSS rules, where did the styles come from?

If you take a look inside `global.css`, you'll notice some `@tailwind` directives:

```css title="/app/ui/global.css"
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Tailwind

[Tailwind](https://tailwindcss.com/) is a CSS framework that speeds up the development process by allowing you to quickly write [utility classes](https://tailwindcss.com/docs/utility-first) directly in your React code.

In Tailwind, you style elements by adding class names. For example, adding `"text-blue-500"` will turn the `<h1>` text blue:

```html
<h1 className="text-blue-500">I'm blue!</h1>
```

Although the CSS styles are shared globally, each class is singularly applied to each element. This means if you add or delete an element, you don't have to worry about maintaining separate stylesheets, style collisions, or the size of your CSS bundle growing as your application scales.

When you use `create-next-app` to start a new project, Next.js will ask if you want to use Tailwind. If you select `yes`, Next.js will automatically install the necessary packages and configure Tailwind in your application.

If you look at `/app/page.tsx`, you'll see that we're using Tailwind classes in the example.

```ts title="/app/page.tsx"
import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

export default function Page() {
    return (
        <main className="flex min-h-screen flex-col p-6">
            {/* These are Tailwind classes: */}
            <div className="flex h-20 shrink-0 items-end rounded-lg bg-blue-500 p-4 md:h-52">
                {/* ... */}
            </div>
        </main>
    );
}
```

Don't worry if this is your first time using Tailwind. To save time, we've already styled all the components you'll be using.

Let's play with Tailwind! Copy the code below and paste it above the `<p>` element in `/app/page.tsx`:

```html title="/app/page.tsx"
<div
    className="relative w-0 h-0 border-l-[15px] border-r-[15px] border-b-[26px] border-l-transparent border-r-transparent border-b-black"
/>
```

<?quiz?>

question: What shape do you see when using the code snippet above?
answer: A yellow star
answer: A blue triangle
answer-correct: A black triangle
answer: A red circle
content:

<h2>Provide some additional content</h2>
<?/quiz?>

If you prefer writing traditional CSS rules or keeping your styles separate from your JSX - CSS Modules are a great alternative.
