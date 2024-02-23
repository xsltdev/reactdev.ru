---
status: experimental
---

<Canary>

The `preload` function is currently only available in React's Canary and experimental channels. Learn more about [React's release channels here](https://react.dev/community/versioning-policy#all-release-channels).

</Canary>

<Note>

[React-based frameworks](../../learn/start-a-new-react-project) frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework's documentation for details.

</Note>

<Intro>

`preload` lets you eagerly fetch a resource such as a stylesheet, font, or external script that you expect to use.

```js
preload('https://example.com/font.woff2', { as: 'font' });
```

</Intro>

<InlineToc />

---

## Reference {/_reference_/}

### `preload(href, options)` {/_preload_/}

To preload a resource, call the `preload` function from `react-dom`.

```js
import { preload } from 'react-dom';

function AppRoot() {
    preload('https://example.com/font.woff2', {
        as: 'font',
    });
    // ...
}
```

[See more examples below.](#usage)

The `preload` function provides the browser with a hint that it should start downloading the given resource, which can save time.

#### Parameters {/_parameters_/}

-   `href`: a string. The URL of the resource you want to download.
-   `options`: an object. It contains the following properties:
    -   `as`: a required string. The type of resource. Its [possible values](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#as) are `audio`, `document`, `embed`, `fetch`, `font`, `image`, `object`, `script`, `style`, `track`, `video`, `worker`.
    -   `crossOrigin`: a string. The [CORS policy](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) to use. Its possible values are `anonymous` and `use-credentials`. It is required when `as` is set to `"fetch"`.
    -   `referrerPolicy`: a string. The [Referrer header](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#referrerpolicy) to send when fetching. Its possible values are `no-referrer-when-downgrade` (the default), `no-referrer`, `origin`, `origin-when-cross-origin`, and `unsafe-url`.
    -   `integrity`: a string. A cryptographic hash of the resource, to [verify its authenticity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
    -   `type`: a string. The MIME type of the resource.
    -   `nonce`: a string. A cryptographic [nonce to allow the resource](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) when using a strict Content Security Policy.
    -   `fetchPriority`: a string. Suggests a relative priority for fetching the resource. The possible values are `auto` (the default), `high`, and `low`.
    -   `imageSrcSet`: a string. For use only with `as: "image"`. Specifies the [source set of the image](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).
    -   `imageSizes`: a string. For use only with `as: "image"`. Specifies the [sizes of the image](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

#### Returns {/_returns_/}

`preload` returns nothing.

#### Caveats {/_caveats_/}

-   Multiple equivalent calls to `preload` have the same effect as a single call. Calls to `preload` are considered equivalent according to the following rules:
    -   Two calls are equivalent if they have the same `href`, except:
    -   If `as` is set to `image`, two calls are equivalent if they have the same `href`, `imageSrcSet`, and `imageSizes`.
-   In the browser, you can call `preload` in any situation: while rendering a component, in an effect, in an event handler, and so on.
-   In server-side rendering or when rendering Server Components, `preload` only has an effect if you call it while rendering a component or in an async context originating from rendering a component. Any other calls will be ignored.

---

## Usage {/_usage_/}

### Preloading when rendering {/_preloading-when-rendering_/}

Call `preload` when rendering a component if you know that it or its children will use a specific resource.

<Recipes titleText="Examples of preloading">

#### Preloading an external script {/_preloading-an-external-script_/}

```js
import { preload } from 'react-dom';

function AppRoot() {
  preload("https://example.com/script.js", {as: "script"});
  return ...;
}
```

If you want the browser to start executing the script immediately (rather than just downloading it), use [`preinit`](/reference/react-dom/preinit) instead. If you want to load an ESM module, use [`preloadModule`](/reference/react-dom/preloadModule).

<Solution />

#### Preloading a stylesheet {/_preloading-a-stylesheet_/}

```js
import { preload } from 'react-dom';

function AppRoot() {
  preload("https://example.com/style.css", {as: "style"});
  return ...;
}
```

If you want the stylesheet to be inserted into the document immediately (which means the browser will start parsing it immediately rather than just downloading it), use [`preinit`](/reference/react-dom/preinit) instead.

<Solution />

#### Preloading a font {/_preloading-a-font_/}

```js
import { preload } from 'react-dom';

function AppRoot() {
  preload("https://example.com/style.css", {as: "style"});
  preload("https://example.com/font.woff2", {as: "font"});
  return ...;
}
```

If you preload a stylesheet, it's smart to also preload any fonts that the stylesheet refers to. That way, the browser can start downloading the font before it's downloaded and parsed the stylesheet.

<Solution />

#### Preloading an image {/_preloading-an-image_/}

```js
import { preload } from 'react-dom';

function AppRoot() {
  preload("/banner.png", {
    as: "image",
    imageSrcSet: "/banner512.png 512w, /banner1024.png 1024w",
    imageSizes: "(max-width: 512px) 512px, 1024px",
  });
  return ...;
}
```

When preloading an image, the `imageSrcSet` and `imageSizes` options help the browser [fetch the correctly sized image for the size of the screen](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

<Solution />

</Recipes>

### Preloading in an event handler {/_preloading-in-an-event-handler_/}

Call `preload` in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```js
import { preload } from 'react-dom';

function CallToAction() {
    const onClick = () => {
        preload('https://example.com/wizardStyles.css', {
            as: 'style',
        });
        startWizard();
    };
    return <button onClick={onClick}>Start Wizard</button>;
}
```
