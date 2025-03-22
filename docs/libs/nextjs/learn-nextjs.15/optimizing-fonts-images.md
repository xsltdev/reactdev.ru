---
description: In the previous chapter, you learned how to style your Next.js application. Let's continue working on your home page by adding a custom font and a hero image.
---

# Optimizing Fonts and Images

In the previous chapter, you learned how to style your Next.js application. Let's continue working on your home page by adding a custom font and a hero image.

!!!tip "Here are the topics we’ll cover:"

    :material-format-text: How to add custom fonts with next/font.

    :material-image-outline: How to add images with next/image.

    :material-check-circle-outline: How fonts and images are optimized in Next.js.

## Why optimize fonts?

Fonts play a significant role in the design of a website, but using custom fonts in your project can affect performance if the font files need to be fetched and loaded.

[Cumulative Layout Shift](https://vercel.com/blog/how-core-web-vitals-affect-seo) is a metric used by Google to evaluate the performance and user experience of a website. With fonts, layout shift happens when the browser initially renders text in a fallback or system font and then swaps it out for a custom font once it has loaded. This swap can cause the text size, spacing, or layout to change, shifting elements around it.

![Mock UI showing initial load of a page, followed by a layout shift as the custom font loads.](font-layout-shift.png)

Next.js automatically optimizes fonts in the application when you use the next/font module. It downloads font files at build time and hosts them with your other static assets. This means when a user visits your application, there are no additional network requests for fonts which would impact performance.

<?quiz?>

question: How does Next.js optimize fonts?
answer: It causes additional network requests which improve performance.
answer: It disables all custom fonts.
answer: It preloads all fonts at runtime.
answer-correct: It hosts font files with other static assets so that there are no additional network requests.
content:

<p>Next.js downloads font files at build time and hosts them with your other static assets. This means when a user visits your application, there are no additional network requests for fonts which would impact performance.</p>
<?/quiz?>

## Adding a primary font

Let's add a custom Google font to your application to see how this works.

In your `/app/ui` folder, create a new file called `fonts.ts`. You'll use this file to keep the fonts that will be used throughout your application.

Import the `Inter` font from the `next/font/google` module - this will be your primary font. Then, specify what [subset](https://fonts.google.com/knowledge/glossary/subsetting) you'd like to load. In this case, `'latin'`:

```ts title="/app/layout.tsx" hl_lines="2 12"
import '@/app/ui/global.css';
import { inter } from '@/app/ui/fonts';

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body
                className={`${inter.className} antialiased`}
            >
                {children}
            </body>
        </html>
    );
}
```

By adding `Inter` to the `<body>` element, the font will be applied throughout your application. Here, you're also adding the Tailwind [antialiased](https://tailwindcss.com/docs/font-smoothing) class which smooths out the font. It's not necessary to use this class, but it adds a nice touch.

Navigate to your browser, open dev tools and select the `body` element. You should see `Inter` and `Inter_Fallback` are now applied under styles.

## Practice: Adding a secondary font

You can also add fonts to specific elements of your application.

Now it's your turn! In your `fonts.ts` file, import a secondary font called `Lusitana` and pass it to the `<p>` element in your `/app/page.tsx` file. In addition to specifying a subset like you did before, you should also specify different font **weights**. For example, `400` (normal) and `700` (bold).

Once you're ready, expand the code snippet below to see the solution.

!!!tip "Hints:"

    -   If you're unsure what weight options to pass to a font, check the TypeScript errors in your code editor.
    -   Visit the Google Fonts website and search for Lusitana to see what options are available.
    -   See the documentation for adding multiple fonts and the full list of options.

???info "Reveal the solution"

    ```ts title="/app/ui/fonts.ts" hl_lines="1 5-8"
    import { Inter, Lusitana } from 'next/font/google';

    export const inter = Inter({ subsets: ['latin'] });

    export const lusitana = Lusitana({
    	weight: ['400', '700'],
    	subsets: ['latin'],
    });
    ```

    ---

    ```ts title="/app/page.tsx" hl_lines="4 10"
    import AcmeLogo from '@/app/ui/acme-logo';
    import { ArrowRightIcon } from '@heroicons/react/24/outline';
    import Link from 'next/link';
    import { lusitana } from '@/app/ui/fonts';

    export default function Page() {
    	return (
    		// ...
    		<p
    			className={`${lusitana.className} text-xl text-gray-800 md:text-3xl md:leading-normal`}
    		>
    			<strong>Welcome to Acme.</strong> This is the
    			example for the{' '}
    			<a
    				href="https://nextjs.org/learn/"
    				className="text-blue-500"
    			>
    				Next.js Learn Course
    			</a>
    			, brought to you by Vercel.
    		</p>
    		// ...
    	);
    }
    ```

Finally, the `<AcmeLogo />` component also uses Lusitana. It was commented out to prevent errors, you can now uncomment it:

```ts title="/app/page.tsx" hl_lines="7"
// ...

export default function Page() {
    return (
        <main className="flex min-h-screen flex-col p-6">
            <div className="flex h-20 shrink-0 items-end rounded-lg bg-blue-500 p-4 md:h-52">
                <AcmeLogo />
                {/* ... */}
            </div>
        </main>
    );
}
```

Great, you've added two custom fonts to your application! Next, let's add a hero image to the home page.

## Why optimize images?

Next.js can serve **static assets**, like images, under the top-level [/public](https://nextjs.org/docs/app/building-your-application/optimizing/static-assets) folder. Files inside `/public` can be referenced in your application.

With regular HTML, you would add an image as follows:

```html
<img
    src="/hero.png"
    alt="Screenshots of the dashboard project showing desktop version"
/>
```

However, this means you have to manually:

-   Ensure your image is responsive on different screen sizes.
-   Specify image sizes for different devices.
-   Prevent layout shift as the images load.
-   Lazy load images that are outside the user's viewport.

Image Optimization is a large topic in web development that could be considered a specialization in itself. Instead of manually implementing these optimizations, you can use the `next/image` component to automatically optimize your images.

## The `<Image>` component

The `<Image>` Component is an extension of the HTML `<img>` tag, and comes with automatic image optimization, such as:

-   Preventing layout shift automatically when images are loading.
-   Resizing images to avoid shipping large images to devices with a smaller viewport.
-   Lazy loading images by default (images load as they enter the viewport).
-   Serving images in modern formats, like [WebP](https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types#webp) and [AVIF](https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types#avif_image), when the browser supports it.

## Adding the desktop hero image

Let's use the `<Image>` component. If you look inside the `/public` folder, you'll see there are two images: `hero-desktop.png` and `hero-mobile.png`. These two images are completely different, and they'll be shown depending if the user's device is a desktop or mobile.

In your `/app/page.tsx` file, import the component from [next/image](https://nextjs.org/docs/api-reference/next/image). Then, add the image under the comment:

```ts title="/app/page.tsx" hl_lines="5 12-18"
import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { lusitana } from '@/app/ui/fonts';
import Image from 'next/image';

export default function Page() {
    return (
        // ...
        <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12">
            {/* Add Hero Images Here */}
            <Image
                src="/hero-desktop.png"
                width={1000}
                height={760}
                className="hidden md:block"
                alt="Screenshots of the dashboard project showing desktop version"
            />
        </div>
        //...
    );
}
```

Here, you're setting the `width` to `1000` and `height` to `760` pixels. It's good practice to set the `width` and `height` of your images to avoid layout shift, these should be an aspect ratio **identical** to the source image. These values are _not_ the size the image is rendered, but instead the size of the actual image file used to understand the aspect ratio.

You'll also notice the class `hidden` to remove the image from the DOM on mobile screens, and `md:block` to show the image on desktop screens.

This is what your home page should look like now:

![Styled home page with a custom font and hero image](home-page-with-hero.png)

## Practice: Adding the mobile hero image

Now it's your turn! Under the image you've just added, add another `<Image>` component for `hero-mobile.png`.

-   The image should have a `width` of `560` and `height` of `620` pixels.
-   It should be shown on mobile screens, and hidden on desktop - you can use dev tools to check if the desktop and mobile images are swapped correctly.

Once you're ready, expand the code snippet below to see the solution.

???info "Reveal the solution"

```ts title="/app/page.tsx" hl_lines="19-25"
import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { lusitana } from '@/app/ui/fonts';
import Image from 'next/image';

export default function Page() {
    return (
        // ...
        <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12">
            {/* Add Hero Images Here */}
            <Image
                src="/hero-desktop.png"
                width={1000}
                height={760}
                className="hidden md:block"
                alt="Screenshots of the dashboard project showing desktop version"
            />
            <Image
                src="/hero-mobile.png"
                width={560}
                height={620}
                className="block md:hidden"
                alt="Screenshot of the dashboard project showing mobile version"
            />
        </div>
        //...
    );
}
```

Great! Your home page now has a custom font and hero images.

<?quiz?>

question: True or False - Images without dimensions and web fonts are common causes of layout shift.
answer-correct: True
answer: False
content:

<p>Images without dimensions and web fonts are common causes of layout shift due to the browser having to download additional resources.</p>
<?/quiz?>

## Recommended reading

There's a lot more to learn about these topics, including optimizing remote images and using local font files. If you'd like to dive deeper into fonts and images, see:

-   [Image Optimization Docs](https://nextjs.org/docs/app/building-your-application/optimizing/images)
-   [Font Optimization Docs](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)
-   [Improving Web Performance with Images (MDN)](https://developer.mozilla.org/en-US/docs/Learn/Performance/Multimedia)
-   [Web Fonts (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Web_fonts)
-   [How Core Web Vitals Affect SEO](https://vercel.com/blog/how-core-web-vitals-affect-seo)
-   [How Google handles JavaScript throughout the indexing process](https://vercel.com/blog/how-google-handles-javascript-throughout-the-indexing-process)

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/optimizing-fonts-images></small>
