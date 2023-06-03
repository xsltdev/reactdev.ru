# createPortal

`createPortal` позволяет вам выводить некоторые дочерние элементы в другую часть DOM.

<!-- 0001.part.md -->

```js
<div>
  <SomeComponent />
  {createPortal(children, domNode, key?)}
</div>
```

## Описание

### `createPortal(children, domNode, key?)`

Чтобы создать портал, вызовите `createPortal`, передав некоторый JSX и DOM-узел, в котором он должен быть отображен:

<!-- 0003.part.md -->

```js
import { createPortal } from 'react-dom';

// ...

<div>
    <p>This child is placed in the parent div.</p>
    {createPortal(
        <p>This child is placed in the document body.</p>,
        document.body
    )}
</div>;
```

<!-- 0004.part.md -->

Портал изменяет только физическое размещение узла DOM. Во всех остальных отношениях JSX, который вы отображаете в портал, действует как дочерний узел компонента React, который его отображает. Например, дочерний узел может получить доступ к контексту, предоставляемому родительским деревом, а события передаются от дочерних узлов к родительским в соответствии с деревом React.

#### Параметры

-   `children`: Все, что может быть отображено с помощью React, например, фрагмент JSX (т. е. `<div />` или `<SomeComponent />`), [Fragment](Fragment.md) (<code><>...&lt;/&gt;</code>), строка или число, или массив из них.

-   `domNode`: Некоторый узел DOM, например, возвращаемый `document.getElementById()`. Узел должен уже существовать. Передача другого узла DOM во время обновления приведет к тому, что содержимое портала будет создано заново.

-   **опционально** `key`: Уникальная строка или число, которое будет использоваться в качестве [ключа](../learn/rendering-lists.md) портала.

#### Возвращает

`createPortal` возвращает узел React, который может быть включен в JSX или возвращен из компонента React. Если React встретит его в выводе рендера, он поместит предоставленные `children` внутрь предоставленного `domNode`.

#### Предупреждения

-   События от порталов распространяются в соответствии с деревом React, а не с деревом DOM. Например, если вы щелкните внутри портала, а портал обернут в `<div onClick>`, то сработает обработчик `onClick`. Если это вызывает проблемы, либо остановите распространение событий внутри портала, либо переместите сам портал вверх в дереве React.

## Использование

### Рендеринг в другую часть DOM

_Порталы_ позволяют вашим компонентам рендерить некоторые из своих дочерних компонентов в другое место в DOM. Это позволяет части вашего компонента "вырваться" из контейнеров, в которых он может находиться. Например, компонент может отображать модальный диалог или всплывающую подсказку, которая появляется над и вне остальной части страницы.

Чтобы создать портал, отобразите результат `createPortal` с некоторым JSX и узлом DOM, где он должен быть размещен:

<!-- 0005.part.md -->

```js
import { createPortal } from 'react-dom';

function MyComponent() {
    return (
        <div style={{ border: '2px solid black' }}>
            <p>This child is placed in the parent div.</p>
            {createPortal(
                <p>
                    This child is placed in the document
                    body.
                </p>,
                document.body
            )}
        </div>
    );
}
```

<!-- 0006.part.md -->

React поместит DOM-узлы для переданного вами JSX внутрь предоставленного вами DOM-узла.

Без портала второй `p` был бы помещен внутрь родительского `div`, но портал "телепортировал" его в [`document.body`:](https://developer.mozilla.org/docs/Web/API/Document/body)

<!-- 0007.part.md -->

```js
import { createPortal } from 'react-dom';

export default function MyComponent() {
    return (
        <div style={{ border: '2px solid black' }}>
            <p>This child is placed in the parent div.</p>
            {createPortal(
                <p>
                    This child is placed in the document
                    body.
                </p>,
                document.body
            )}
        </div>
    );
}
```

<!-- 0008.part.md -->

Обратите внимание, что второй абзац визуально появляется вне родительского `div` с границей. Если вы просмотрите структуру DOM с помощью инструментов разработчика, вы увидите, что второй `p` был помещен непосредственно в `body`:

```html
<body>
    <div id="root">
        ...
        <div style="border: 2px solid black">
            <p>
                This child is placed inside the parent div.
            </p>
        </div>
        ...
    </div>
    <p>This child is placed in the document body.</p>
</body>
```

Портал изменяет только физическое размещение узла DOM. Во всех остальных отношениях JSX, который вы отображаете в портал, действует как дочерний узел компонента React, который его отображает. Например, дочерний узел может получить доступ к контексту, предоставляемому родительским деревом, а события по-прежнему передаются от дочерних узлов к родительским в соответствии с деревом React.

### Рендеринг модального диалога с помощью портала

Вы можете использовать портал для создания модального диалога, который парит над остальной частью страницы, даже если компонент, вызывающий диалог, находится внутри контейнера с `overflow: hidden` или другими стилями, которые мешают диалогу.

В этом примере два контейнера имеют стили, которые мешают модальному диалогу, но тот, который отображается в портале, не затронут, потому что в DOM модальный диалог не содержится в родительских JSX-элементах.

=== "App.js"

    ```js
    import NoPortalExample from './NoPortalExample';
    import PortalExample from './PortalExample';

    export default function App() {
    	return (
    		<>
    			<div className="clipping-container">
    				<NoPortalExample />
    			</div>
    			<div className="clipping-container">
    				<PortalExample />
    			</div>
    		</>
    	);
    }
    ```

=== "NoPortalExample.js"

    ```js
    import { useState } from 'react';
    import ModalContent from './ModalContent.js';

    export default function NoPortalExample() {
    	const [showModal, setShowModal] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShowModal(true)}>
    				Show modal without a portal
    			</button>
    			{showModal && (
    				<ModalContent
    					onClose={() => setShowModal(false)}
    				/>
    			)}
    		</>
    	);
    }
    ```

=== "PortalExample.js"

    ```js
    import { useState } from 'react';
    import { createPortal } from 'react-dom';
    import ModalContent from './ModalContent.js';

    export default function PortalExample() {
    	const [showModal, setShowModal] = useState(false);
    	return (
    		<>
    			<button onClick={() => setShowModal(true)}>
    				Show modal using a portal
    			</button>
    			{showModal &&
    				createPortal(
    					<ModalContent
    						onClose={() => setShowModal(false)}
    					/>,
    					document.body
    				)}
    		</>
    	);
    }
    ```

=== "ModalContent.js"

    ```js
    export default function ModalContent({ onClose }) {
    	return (
    		<div className="modal">
    			<div>I'm a modal dialog</div>
    			<button onClick={onClose}>Close</button>
    		</div>
    	);
    }
    ```

<!-- 0018.part.md -->

!!!warning ""

    Важно убедиться, что ваше приложение доступно при использовании порталов. Например, вам может понадобиться управлять фокусом клавиатуры, чтобы пользователь мог перемещать фокус в портал и из него естественным образом.

    При создании модалов следуйте [WAI-ARIA Modal Authoring Practices](https://www.w3.org/WAI/ARIA/apg/#dialog_modal). Если вы используете пакет сообщества, убедитесь, что он доступен и следует этим рекомендациям.

### Рендеринг компонентов React в серверную разметку, не относящуюся к React

Порталы могут быть полезны, если ваш React root является лишь частью статической или серверной страницы, построенной не на React. Например, если ваша страница построена на серверном фреймворке, таком как Rails, вы можете создавать интерактивные области внутри статичных областей, таких как боковые панели. По сравнению с наличием [нескольких отдельных корней React](createRoot.md), порталы позволяют рассматривать приложение как единое дерево React с общим состоянием, даже если его части отображаются в разных частях DOM.

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html>
    <head><title>My app</title></head>
    <body>
    	<h1>Welcome to my hybrid app</h1>
    	<div class="parent">
    	<div class="sidebar">
    		This is server non-React markup
    		<div id="sidebar-content"></div>
    	</div>
    	<div id="root"></div>
    	</div>
    </body>
    </html>
    ```

=== "index.js"

    ```js
    import { StrictMode } from 'react';
    import { createRoot } from 'react-dom/client';
    import App from './App.js';
    import './styles.css';

    const root = createRoot(document.getElementById('root'));
    root.render(
    	<StrictMode>
    		<App />
    	</StrictMode>
    );
    ```

=== "App.js"

    ```js
    import { createPortal } from 'react-dom';

    const sidebarContentEl = document.getElementById(
    	'sidebar-content'
    );

    export default function App() {
    	return (
    		<>
    			<MainContent />
    			{createPortal(
    				<SidebarContent />,
    				sidebarContentEl
    			)}
    		</>
    	);
    }

    function MainContent() {
    	return <p>This part is rendered by React</p>;
    }

    function SidebarContent() {
    	return <p>This part is also rendered by React!</p>;
    }
    ```

### Рендеринг компонентов React в не-React DOM-узлы

Вы также можете использовать портал для управления содержимым DOM-узла, который управляется вне React. Например, предположим, что вы интегрируетесь с виджетом карты, не принадлежащим React, и хотите отобразить содержимое React во всплывающем окне. Чтобы сделать это, объявите переменную состояния `popupContainer` для хранения DOM-узла, в который будет производиться рендеринг:

<!-- 0025.part.md -->

```js
const [popupContainer, setPopupContainer] = useState(null);
```

<!-- 0026.part.md -->

Когда вы создаете сторонний виджет, сохраните узел DOM, возвращаемый виджетом, чтобы вы могли выполнить в нем рендеринг:

<!-- 0027.part.md -->

```js
useEffect(() => {
    if (mapRef.current === null) {
        const map = createMapWidget(containerRef.current);
        mapRef.current = map;
        const popupDiv = addPopupToMapWidget(map);
        setPopupContainer(popupDiv);
    }
}, []);
```

<!-- 0028.part.md -->

Это позволит вам использовать `createPortal` для рендеринга React-контента в `popupContainer`, как только он станет доступен:

<!-- 0029.part.md -->

```js
return (
    <div
        style={{ width: 250, height: 250 }}
        ref={containerRef}
    >
        {popupContainer !== null &&
            createPortal(
                <p>Hello from React!</p>,
                popupContainer
            )}
    </div>
);
```

<!-- 0030.part.md -->

Вот полный пример, с которым вы можете поиграть:

=== "App.js"

    ```js
    import { useRef, useEffect, useState } from 'react';
    import { createPortal } from 'react-dom';
    import {
    	createMapWidget,
    	addPopupToMapWidget,
    } from './map-widget.js';

    export default function Map() {
    	const containerRef = useRef(null);
    	const mapRef = useRef(null);
    	const [popupContainer, setPopupContainer] = useState(
    		null
    	);

    	useEffect(() => {
    		if (mapRef.current === null) {
    			const map = createMapWidget(
    				containerRef.current
    			);
    			mapRef.current = map;
    			const popupDiv = addPopupToMapWidget(map);
    			setPopupContainer(popupDiv);
    		}
    	}, []);

    	return (
    		<div
    			style={{ width: 250, height: 250 }}
    			ref={containerRef}
    		>
    			{popupContainer !== null &&
    				createPortal(
    					<p>Hello from React!</p>,
    					popupContainer
    				)}
    		</div>
    	);
    }
    ```

=== "map-widget.js"

    ```js
    import 'leaflet/dist/leaflet.css';
    import * as L from 'leaflet';

    export function createMapWidget(containerDomNode) {
    	const map = L.map(containerDomNode);
    	map.setView([0, 0], 0);
    	L.tileLayer(
    		'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    		{
    			maxZoom: 19,
    			attribution: '© OpenStreetMap',
    		}
    	).addTo(map);
    	return map;
    }

    export function addPopupToMapWidget(map) {
    	const popupDiv = document.createElement('div');
    	L.popup()
    		.setLatLng([0, 0])
    		.setContent(popupDiv)
    		.openOn(map);
    	return popupDiv;
    }
    ```

## Ссылки

-   [https://react.dev/reference/react-dom/createPortal](https://react.dev/reference/react-dom/createPortal)
