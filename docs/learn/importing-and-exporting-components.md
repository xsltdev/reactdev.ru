---
description: По мере того, как вы создаете все больше и больше компонентов, часто имеет смысл начать разделять их на разные файлы. Это позволяет легко сканировать файлы и повторно использовать компоненты в большем количестве мест
---

# Импорт и экспорт компонентов

<big>Магия компонентов заключается в возможности их повторного использования: вы можете создавать компоненты, которые состоят из других компонентов. Но по мере того, как вы создаете все больше и больше компонентов, часто имеет смысл начать разделять их на разные файлы. Это позволяет легко сканировать файлы и повторно использовать компоненты в большем количестве мест.</big>

!!!tip "Вы узнаете"

    -   Что такое файл корневого компонента
    -   Как импортировать и экспортировать компонент
    -   Когда использовать импорт и экспорт по умолчанию и по имени
    -   Как импортировать и экспортировать несколько компонентов из одного файла
    -   Как разделить компоненты на несколько файлов

## Корневой файл компонента {#the-root-component-file}

В [вашем первом компоненте](your-first-component.md) вы создали компонент `Profile` и компонент `Gallery`, который его отображает:

=== "App.js"

    ```js
    function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/MK3eW3As.jpg"
    			alt="Katherine Johnson"
    		/>
    	);
    }

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/xgy8t9?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Сейчас они находятся в **корневом файле компонента,** названном в данном примере `App.js`. В [Create React App](https://create-react-app.dev/) ваше приложение находится в `src/App.js`. Однако, в зависимости от вашей конфигурации, ваш корневой компонент может находиться в другом файле. Если вы используете фреймворк с файловой маршрутизацией, например Next.js, ваш корневой компонент будет разным для каждой страницы.

## Экспорт и импорт компонента {#exporting-and-importing-a-component}

Что если в будущем вы захотите изменить целевой экран и поместить туда список научных книг? Или разместить все профили в другом месте? Имеет смысл перенести `Gallery` и `Profile` из корневого файла компонента. Это сделает их более модульными и пригодными для повторного использования в других файлах. Вы можете переместить компонент в три этапа:

1.  **Сделайте** новый JS-файл, в который поместите компоненты.
2.  **Экспортируйте** свою функцию-компонент из этого файла (используя экспорт [default](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/export#using_the_default_export) или [named](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/export#using_named_exports)).
3.  **Импортируйте** его в файл, где вы будете использовать компонент (используя соответствующую технику для импорта [default](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import#importing_defaults) или [named](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import#import_a_single_export_from_a_module) exports).

Здесь `Profile` и `Gallery` были перенесены из `App.js` в новый файл `Gallery.js`. Теперь вы можете изменить `App.js`, чтобы импортировать `Gallery` из `Gallery.js`:

=== "App.js"

    ```js
    import Gallery from './Gallery.js';

    export default function App() {
    	return <Gallery />;
    }
    ```

=== "Gallery.js"

    ```js
    function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/QIrZWGIs.jpg"
    			alt="Alan L. Hart"
    		/>
    	);
    }

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/nfmfwy?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Обратите внимание, что теперь этот пример разбит на два составных файла:

1.  `Gallery.js`:
    -   Определяет компонент `Profile`, который используется только в пределах одного файла и не экспортируется.
    -   Экспортирует компонент `Gallery` как **экспорт по умолчанию.**.
2.  `App.js`:
    -   Импортирует `Gallery` как **импорт по умолчанию** из `Gallery.js`.
    -   Экспортирует корневой компонент `App` как **экспорт по умолчанию.**.

!!!note ""

    Вы можете встретить файлы, в которых расширение `.js` опускается, например:

    ```js
    import Gallery from './Gallery';
    ```

    Либо `'./Gallery.js'`, либо `'./Gallery'` будут работать с React, хотя первый вариант ближе к тому, как работают [native ES Modules](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Modules).

!!!note "Экспорт по умолчанию и именованный экспорт"

    Существует два основных способа экспорта значений в JavaScript: экспорт по умолчанию и именованный экспорт. До сих пор в наших примерах использовался только экспорт по умолчанию. Но вы можете использовать один или оба из них в одном файле. **В файле может быть не более одного _дефолтного_ экспорта, но в нем может быть сколько угодно _именованных_ экспортов.**

    ![Экспорт по умолчанию и именованный экспорт](i_import-export.svg)

    То, как вы экспортируете свой компонент, диктует, как вы должны его импортировать. Вы получите ошибку, если попытаетесь импортировать экспорт по умолчанию так же, как и именованный экспорт! Эта диаграмма поможет вам следить за этим:

    | Синтаксис    | Утверждение экспорта                  | Утверждение импорта                     |
    | ------------ | ------------------------------------- | --------------------------------------- |
    | По умолчанию | `export default function Button() {}` | `import Button from './Button.js';`     |
    | Именованный  | `export function Button() {}`         | `import { Button } from './Button.js';` |

    Когда вы пишете импорт _по умолчанию_, вы можете поместить любое имя после `import`. Например, вы можете написать `import Banana from './Button.js'` вместо этого, и это все равно предоставит вам тот же экспорт по умолчанию. В отличие от этого, при именованном импорте имя должно совпадать с обеих сторон. Вот почему они называются _именованными_ импортами!

    **Люди часто используют экспорт по умолчанию, если файл экспортирует только один компонент, и используют именованный экспорт, если он экспортирует несколько компонентов и значений.** Независимо от того, какой стиль кодирования вы предпочитаете, всегда давайте осмысленные имена вашим компонентным функциям и файлам, которые их содержат. Компоненты без имен, такие как `export default () => {}`, не рекомендуется использовать, поскольку они затрудняют отладку.

## Экспорт и импорт нескольких компонентов из одного файла {#exporting-and-importing-multiple-components-from-the-same-file}

Что если вы хотите показать только один `Профиль` вместо галереи? Вы можете экспортировать и компонент `Profile`. Но `Gallery.js` уже имеет экспорт по _умолчанию_, а вы не можете иметь _два_ экспорта по умолчанию. Вы можете создать новый файл с экспортом по умолчанию, или добавить _именной_ экспорт для `Profile`. **Файл может иметь только один экспорт по умолчанию, но может иметь множество именованных экспортов!**

!!!note "Стиль экспорта"

    Чтобы уменьшить потенциальную путаницу между экспортом по умолчанию и именованным экспортом, некоторые команды предпочитают придерживаться только одного стиля (по умолчанию или именованного), или избегать их смешивания в одном файле. Делайте то, что подходит именно вам!

Во-первых, **экспортируйте** `Profile` из `Gallery.js`, используя именованный экспорт (без ключевого слова `default`):

```js
export function Profile() {
    // ...
}
```

Затем **импортируйте** `Profile` из `Gallery.js` в `App.js`, используя именованный импорт (с фигурными скобками):

```js
import { Profile } from './Gallery.js';
```

Наконец, **render** `<Profile />` из компонента `App`:

```js
export default function App() {
    return <Profile />;
}
```

Теперь `Gallery.js` содержит два экспорта: экспорт по умолчанию `Gallery` и именованный экспорт `Profile`. `App.js` импортирует их оба. Попробуйте изменить `<Profile />` на `<Gallery />` и обратно в этом примере:

=== "App.j"

    ```js
    import Gallery from './Gallery.js';
    import { Profile } from './Gallery.js';

    export default function App() {
    	return <Profile />;
    }
    ```

=== "Gallery.js"

    ```js
    export function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/QIrZWGIs.jpg"
    			alt="Alan L. Hart"
    		/>
    	);
    }

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/5qcqj6?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

Теперь вы используете смесь экспорта по умолчанию и именованных экспортов:

-   `Gallery.js`:
    -   Экспортирует компонент `Profile` как **именованный экспорт под названием `Profile`**.
    -   Экспортирует компонент `Gallery` как **экспорт по умолчанию.**.
-   `App.js`:
    -   Импортирует `Profile` как **именованный импорт под названием `Profile`** из `Gallery.js`.
    -   Импортирует `Gallery` как **импорт по умолчанию** из `Gallery.js`.
    -   Экспортирует корневой компонент `App` как **экспорт по умолчанию.**.

!!!note "Итоги"

    На этой странице вы узнали:

    -   Что такое файл корневого компонента
    -   Как импортировать и экспортировать компонент
    -   Когда и как использовать импорт и экспорт по умолчанию и по имени
    -   Как экспортировать несколько компонентов из одного файла

## Задача {#challenges}

### 1. Разделяйте компоненты дальше {#split-the-components-further}

В настоящее время `Gallery.js` экспортирует и `Profile` и `Gallery`, что немного запутывает.

Переместите компонент `Profile` в собственный `Profile.js`, а затем измените компонент `App`, чтобы он отображал и `<Profile />`, и `<Gallery />` друг за другом.

Вы можете использовать либо экспорт по умолчанию, либо именованный экспорт для `Profile`, но убедитесь, что вы используете соответствующий синтаксис импорта как в `App.js`, так и в `Gallery.js`! Вы можете обратиться к таблице из глубокого погружения выше:

| Синтаксис    | Утверждение экспорта                  | Утверждение импорта                     |
| ------------ | ------------------------------------- | --------------------------------------- |
| По-умолчанию | `export default function Button() {}` | `import Button from './Button.js'';`    |
| Именованный  | `export function Button() {}`         | `import { Button } from './Button.js''` |

Не забывайте импортировать свои компоненты там, где они вызываются. Разве `Gallery` не использует `Profile` тоже?

=== "App.js"

    ```js
    import Gallery from './Gallery.js';
    import { Profile } from './Gallery.js';

    export default function App() {
    	return (
    		<div>
    			<Profile />
    		</div>
    	);
    }
    ```

=== "Gallery.js"

    ```js
    // Перемести в Profile.js!
    export function Profile() {
    	return (
    		<img
    			src="https://i.imgur.com/QIrZWGIs.jpg"
    			alt="Alan L. Hart"
    		/>
    	);
    }

    export default function Gallery() {
    	return (
    		<section>
    			<h1>Amazing scientists</h1>
    			<Profile />
    			<Profile />
    			<Profile />
    		</section>
    	);
    }
    ```

=== "Profile.js"

    ```js

    ```

=== "Результат"

    <iframe src="https://codesandbox.io/embed/w759z8?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

После того, как вы заставите его работать с одним видом экспорта, заставьте его работать с другим видом.

???info "Показать подсказку"

    Не забудьте импортировать свои компоненты туда, где они вызываются. Разве `Gallery` тоже не использует `Profile`?

???success "Показать решение 1"

    Это решение с именованным экспортом:

    === "App.js"

    	```js
    	import Gallery from './Gallery.js';
    	import { Profile } from './Profile.js';

    	export default function App() {
    		return (
    			<div>
    				<Profile />
    				<Gallery />
    			</div>
    		);
    	}
    	```

    === "Gallery.js"

    	```js
    	import { Profile } from './Profile.js';

    	export default function Gallery() {
    		return (
    			<section>
    				<h1>Amazing scientists</h1>
    				<Profile />
    				<Profile />
    				<Profile />
    			</section>
    		);
    	}
    	```

    === "Profile.js"

    	```js
    	export function Profile() {
    		return (
    			<img
    				src="https://i.imgur.com/QIrZWGIs.jpg"
    				alt="Alan L. Hart"
    			/>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/kz3qn4?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

???success "Показать решение 2"

    Это решение с экспортом по умолчанию:

    === "App.js"

    	```js
    	import Gallery from './Gallery.js';
    	import Profile from './Profile.js';

    	export default function App() {
    		return (
    			<div>
    				<Profile />
    				<Gallery />
    			</div>
    		);
    	}
    	```

    === "Gallery.js"

    	```js
    	import Profile from './Profile.js';

    	export default function Gallery() {
    		return (
    			<section>
    				<h1>Amazing scientists</h1>
    				<Profile />
    				<Profile />
    				<Profile />
    			</section>
    		);
    	}
    	```

    === "Profile.js"

    	```js
    	export default function Profile() {
    		return (
    			<img
    				src="https://i.imgur.com/QIrZWGIs.jpg"
    				alt="Alan L. Hart"
    			/>
    		);
    	}
    	```

    === "Результат"

    	<iframe src="https://codesandbox.io/embed/l2py7r?view=Editor+%2B+Preview" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="react.dev" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/importing-and-exporting-components](https://react.dev/learn/importing-and-exporting-components)</small>
