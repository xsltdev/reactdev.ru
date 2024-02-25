# Общие компоненты

Все встроенные компоненты браузера, такие как [`<div>`](https://hcdev.ru/html/div/), поддерживают некоторые общие пропсы и события.

## Описание

### Общий компонент

```js
<div className="wrapper">Some content</div>
```

**Свойства**

Эти специальные пропсы React поддерживаются для всех встроенных компонентов:

-   `children`: Узел React (элемент, строка, число, [портал](../createPortal.md), пустой узел типа `null`, `undefined` и booleans, или массив других узлов React). Определяет содержимое внутри компонента. Когда вы используете JSX, вы обычно неявно указываете пропс `children` путем вложения тегов типа `<div><span /></div>`.
-   `dangerouslySetInnerHTML`: Объект вида `{ __html: '<p>some html</p>' }` с необработанной HTML-строкой внутри. Переопределяет свойство [`innerHTML`](https://developer.mozilla.org/docs/Web/API/Element/innerHTML) узла DOM и отображает переданный HTML внутри. Это следует использовать с особой осторожностью! Если HTML внутри не является доверенным (например, если он основан на данных пользователя), вы рискуете получить [XSS](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%B6%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%D1%8B%D0%B9_%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%B8%D0%BD%D0%B3) уязвимость.
-   `ref`: Объект ссылки из [`useRef`](../../react/useRef.md) или [`createRef`](../../react/createRef.md), или функция обратного вызова `ref`, или строка для [legacy refs](https://reactjs.org/docs/refs-and-the-dom.html#legacy-api-string-refs). Ваш ref будет заполнен элементом DOM для этого узла.
-   `suppressContentEditableWarning`: Булево значение. Если `true`, подавляет предупреждение, которое React показывает для элементов, имеющих одновременно `children` и `contentEditable={true}` (которые обычно не работают вместе). Используйте это, если вы создаете библиотеку ввода текста, которая управляет содержимым `contentEditable` вручную.
-   `suppressHydrationWarning`: Булево значение. Если вы используете [серверный рендеринг,](../server/index.md), обычно появляется предупреждение, когда сервер и клиент рендерят разное содержимое. В некоторых редких случаях (например, временные метки) очень трудно или невозможно гарантировать точное совпадение. Если вы установите `uppressHydrationWarning` в `true`, React не будет предупреждать вас о несоответствии атрибутов и содержимого этого элемента. Эта функция работает только на одном уровне и предназначена для использования в качестве аварийного люка. Не злоупотребляйте им. [Читайте о подавлении ошибок гидратации](../client/hydrateRoot.md#suppressing-unavoidable-hydration-mismatch-errors).
-   `style`: Объект со стилями CSS, например `{ fontWeight: 'bold', margin: 20 }`. Аналогично свойству DOM [`style`](https://developer.mozilla.org/docs/Web/API/HTMLElement/style), имена свойств CSS должны быть написаны в `camelCase`, например `fontWeight` вместо `font-weight`. В качестве значений можно передавать строки или числа. Если вы передаете число, например `width: 100`, React автоматически добавит `px` ("пиксели") к значению, если только это не [свойство без единиц измерения](https://github.com/facebook/react/blob/81d4ee9ca5c405dce62f64e61506b8e155f38d8d/packages/react-dom-bindings/src/shared/CSSProperty.js#L8-L57). Мы рекомендуем использовать `style` только для динамических стилей, значения которых заранее не известны. В других случаях применение простых CSS-классов с `className` более эффективно.

Эти стандартные пропсы DOM также поддерживаются для всех встроенных компонентов:

-   [`accessKey`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/accesskey): Строка. Указывает комбинацию клавиш для элемента. [Обычно не рекомендуется](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/accesskey#accessibility_concerns).
-   [`aria-*`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Attributes): Атрибуты ARIA позволяют указать информацию дерева доступности для этого элемента. Полное руководство см. в [Атрибуты ARIA](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Attributes). В React все имена атрибутов ARIA точно такие же, как и в HTML.
-   [`autoCapitalize`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/autocapitalize): Строка. Определяет, должен ли пользовательский ввод набираться заглавными буквами и каким образом.
-   [`className`](https://developer.mozilla.org/docs/Web/API/Element/className): Строка. Указывает имя CSS-класса элемента.
-   [`contentEditable`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/contenteditable): Булево значение. Если `true`, браузер позволяет пользователю редактировать отображаемый элемент напрямую. Это используется для реализации библиотек богатого текстового ввода, таких как [Lexical.](https://lexical.dev/) React предупреждает, если вы пытаетесь передать дочерние элементы React элементу с `contentEditable={true}`, потому что React не сможет обновить его содержимое после редактирования пользователем.
-   [`data-*`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/data-*): Атрибуты Data позволяют прикрепить к элементу строковые данные, например, `data-fruit="banana"`. В React они не часто используются, потому что обычно вместо этого вы считываете данные из `props` или `state`.
-   [`dir`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/dir): Либо `'ltr'`, либо `'rtl'`. Указывает направление текста элемента.
-   [`draggable`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/draggable): Булево значение. Определяет, является ли элемент перетаскиваемым. Часть [HTML Drag and Drop API](https://developer.mozilla.org/docs/Web/API/HTML_Drag_and_Drop_API).
-   [`enterKeyHint`](https://developer.mozilla.org/docs/Web/API/HTMLElement/enterKeyHint): Строка. Определяет, какое действие должно быть представлено для клавиши Enter на виртуальных клавиатурах.
-   [`htmlFor`](https://developer.mozilla.org/docs/Web/API/HTMLLabelElement/htmlFor): Строка. Для [`label`](https://hcdev.ru/html/label/) и [`output`](https://hcdev.ru/html/output/) позволяет [связать метку с некоторым элементом управления](./input.md#providing-a-label-for-an-input). Аналогично [`for` HTML-атрибуту](https://developer.mozilla.org/docs/Web/HTML/Attributes/for). React использует стандартные имена свойств DOM (`htmlFor`) вместо имен HTML-атрибутов.
-   [`hidden`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/hidden): Булево значение или строка. Указывает, должен ли элемент быть скрытым.
-   [`id`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/id): Строка. Задает уникальный идентификатор для этого элемента, который может быть использован для его последующего поиска или связи с другими элементами. Генерируйте его вместе с [`useId`](../../react/useId.md), чтобы избежать столкновений между несколькими экземплярами одного и того же компонента.
-   [`is`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/is): Строка. Если указана, компонент будет вести себя как [пользовательский элемент](./index.md#custom-html-elements)
-   [`inputMode`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/inputmode): Строка. Определяет, какой тип клавиатуры отображать (например, текстовый, цифровой или телефонный).
-   [`itemProp`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/itemprop): Строка. Указывает, какое свойство представляет элемент для краулеров структурированных данных.
-   [`lang`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/lang): Строка. Указывает язык элемента.
-   [`onAnimationEnd`](https://developer.mozilla.org/docs/Web/API/Element/animationend_event): Функция обработчика `AnimationEvent`. Срабатывает при завершении CSS-анимации.
-   `onAnimationEndCapture`: Версия `onAnimationEnd`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onAnimationIteration`](https://developer.mozilla.org/docs/Web/API/Element/animationiteration_event): Функция обработчика `AnimationEvent`. Срабатывает, когда итерация CSS-анимации заканчивается и начинается другая.
-   `onAnimationIterationCapture`: Версия `onAnimationIteration`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onAnimationStart`](https://developer.mozilla.org/docs/Web/API/Element/animationstart_event): Функция обработчика `AnimationEvent`. Срабатывает при запуске CSS-анимации.
-   `onAnimationStartCapture`: `onAnimationStart`, но срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onAuxClick`](https://developer.mozilla.org/docs/Web/API/Element/auxclick_event): Функция обработчика `MouseEvent`. Срабатывает, когда была нажата не основная кнопка указателя.
-   `onAuxClickCapture`: Версия `onAuxClick`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   `onBeforeInput`: Функция обработчика `InputEvent`. Срабатывает перед изменением значения редактируемого элемента. React пока _не_ использует собственное событие [`beforeinput`](https://developer.mozilla.org/docs/Web/API/HTMLElement/beforeinput_event), и вместо этого пытается заполнить его с помощью других событий.
-   `onBeforeInputCapture`: Версия `onBeforeInput`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   `onBlur`: Функция обработчика `FocusEvent`. Срабатывает, когда элемент теряет фокус. В отличие от встроенного события браузера [`blur`](https://developer.mozilla.org/docs/Web/API/Element/blur_event), в React событие `onBlur` пузырится.
-   `onBlurCapture`: Версия `onBlur`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onClick`](https://developer.mozilla.org/docs/Web/API/Element/click_event): Функция обработчика `MouseEvent`. Срабатывает при нажатии основной кнопки на указывающем устройстве.
-   `onClickCapture`: Версия `onClick`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onCompositionStart`](https://developer.mozilla.org/docs/Web/API/Element/compositionstart_event): Функция обработчика `CompositionEvent`. Срабатывает, когда [редактор методов ввода](https://developer.mozilla.org/docs/Glossary/Input_method_editor) начинает новую сессию композиции.
-   `onCompositionStartCapture`: Версия функции `onCompositionStart`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onCompositionEnd`](https://developer.mozilla.org/docs/Web/API/Element/compositionend_event): Функция обработчика `CompositionEvent`. Срабатывает, когда [редактор методов ввода](https://developer.mozilla.org/docs/Glossary/Input_method_editor) завершает или отменяет сеанс композиции.
-   `onCompositionEndCapture`: Версия функции `onCompositionEnd`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onCompositionUpdate`](https://developer.mozilla.org/docs/Web/API/Element/compositionupdate_event): Функция обработчика `CompositionEvent`. Срабатывает, когда [редактор метода ввода](https://developer.mozilla.org/docs/Glossary/Input_method_editor) получает новый символ.
-   `onCompositionUpdateCapture`: Версия функции `onCompositionUpdate`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onContextMenu`](https://developer.mozilla.org/docs/Web/API/Element/contextmenu_event): Функция обработчика `MouseEvent`. Срабатывает, когда пользователь пытается открыть контекстное меню.
-   `onContextMenuCapture`: Версия `onContextMenu`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onCopy`](https://developer.mozilla.org/docs/Web/API/Element/copy_event): Функция обработчика `ClipboardEvent`. Срабатывает, когда пользователь пытается скопировать что-либо в буфер обмена.
-   `onCopyCapture`: Версия `onCopy`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onCut`](https://developer.mozilla.org/docs/Web/API/Element/cut_event): Функция обработчика `ClipboardEvent`. Срабатывает, когда пользователь пытается вырезать что-то в буфере обмена.
-   `onCutCapture`: Версия `onCut`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   `onDoubleClick`: Функция обработчика `MouseEvent`. Срабатывает, когда пользователь дважды щелкает мышью. Соответствует событию браузера [`dblclick`.](https://developer.mozilla.org/docs/Web/API/Element/dblclick_event)
-   `onDoubleClickCapture`: Версия `onDoubleClick`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onDrag`](https://developer.mozilla.org/docs/Web/API/HTMLElement/drag_event): Функция обработчика `DragEvent`. Срабатывает, когда пользователь что-то перетаскивает.
-   `onDragCapture`: Версия функции `onDrag`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onDragEnd`](https://developer.mozilla.org/docs/Web/API/HTMLElement/dragend_event): Функция обработчика `DragEvent`. Срабатывает, когда пользователь прекращает перетаскивать что-то.
-   `onDragEndCapture`: Версия функции `onDragEnd`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onDragEnter`](https://developer.mozilla.org/docs/Web/API/HTMLElement/dragenter_event): Функция обработчика `DragEvent`. Срабатывает, когда перетаскиваемое содержимое попадает в допустимую цель падения.
-   `onDragEnterCapture`: Версия функции `onDragEnter`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onDragOver`](https://developer.mozilla.org/docs/Web/API/HTMLElement/dragover_event): Функция обработчика `DragEvent`. Срабатывает на действительной цели падения, когда перетаскиваемое содержимое перетаскивается на нее. Вы должны вызвать `e.preventDefault()` здесь, чтобы разрешить перетаскивание.
-   `onDragOverCapture`: Версия `onDragOver`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onDragStart`](https://developer.mozilla.org/docs/Web/API/HTMLElement/dragstart_event): Функция обработчика `DragEvent`. Срабатывает, когда пользователь начинает перетаскивать элемент.
-   `onDragStartCapture`: Версия `onDragStart`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onDrop`](https://developer.mozilla.org/docs/Web/API/HTMLElement/drop_event): Функция обработчика `DragEvent`. Срабатывает, когда что-то падает на допустимую цель падения.
-   `onDropCapture`: Версия `onDrop`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   `onFocus`: Функция обработчика `FocusEvent`. Срабатывает, когда элемент потерял фокус. В отличие от встроенного события браузера [`focus`](https://developer.mozilla.org/docs/Web/API/Element/focus_event), в React событие `onFocus` пузырится.
-   `onFocusCapture`: Версия `onFocus`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onGotPointerCapture`](https://developer.mozilla.org/docs/Web/API/Element/gotpointercapture_event): Функция обработчика `PointerEvent`. Срабатывает, когда элемент программно захватывает указатель.
-   `onGotPointerCaptureCapture`: Версия `onGotPointerCapture`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onKeyDown`](https://developer.mozilla.org/docs/Web/API/Element/keydown_event): Функция обработчика `KeyboardEvent`. Срабатывает при нажатии клавиши.
-   `onKeyDownCapture`: Версия функции `onKeyDown`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onKeyPress`](https://developer.mozilla.org/docs/Web/API/Element/keypress_event): Функция обработчика `KeyboardEvent`. Исправлено. Вместо нее используйте `onKeyDown` или `onBeforeInput`.
-   `onKeyPressCapture`: Версия `onKeyPress`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onKeyUp`](https://developer.mozilla.org/docs/Web/API/Element/keyup_event): Функция обработчика `KeyboardEvent`. Срабатывает при отпускании клавиши.
-   `onKeyUpCapture`: Версия функции `onKeyUp`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onLostPointerCapture`](https://developer.mozilla.org/docs/Web/API/Element/lostpointercapture_event): Функция обработчика `PointerEvent`. Срабатывает, когда элемент перестает захватывать указатель.
-   `onLostPointerCaptureCapture`: Версия `onLostPointerCapture`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onMouseDown`](https://developer.mozilla.org/docs/Web/API/Element/mousedown_event): Функция обработчика `MouseEvent`. Срабатывает при нажатии указателя вниз.
-   `onMouseDownCapture`: Версия `onMouseDown`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onMouseEnter`](https://developer.mozilla.org/docs/Web/API/Element/mouseenter_event): Функция обработчика `MouseEvent`. Срабатывает, когда указатель перемещается внутри элемента. Не имеет фазы захвата. Вместо этого `onMouseLeave` и `onMouseEnter` распространяются от покидаемого элемента к вводимому.
-   [`onMouseLeave`](https://developer.mozilla.org/docs/Web/API/Element/mouseleave_event): Функция обработчика `MouseEvent`. Срабатывает, когда указатель перемещается за пределы элемента. Не имеет фазы захвата. Вместо этого `onMouseLeave` и `onMouseEnter` распространяются от покидаемого элемента к вводимому.
-   [`onMouseMove`](https://developer.mozilla.org/docs/Web/API/Element/mousemove_event): Функция обработчика `MouseEvent`. Срабатывает при изменении координат указателя.
-   `onMouseMoveCapture`: Версия функции `onMouseMove`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onMouseOut`](https://developer.mozilla.org/docs/Web/API/Element/mouseout_event): Функция обработчика `MouseEvent`. Срабатывает, когда указатель перемещается за пределы элемента, или если он перемещается в дочерний элемент.
-   `onMouseOutCapture`: Версия функции `onMouseOut`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onMouseUp`](https://developer.mozilla.org/docs/Web/API/Element/mouseup_event): Функция обработчика `MouseEvent`. Срабатывает при освобождении указателя.
-   `onMouseUpCapture`: Версия функции `onMouseUp`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPointerCancel`](https://developer.mozilla.org/docs/Web/API/Element/pointercancel_event): Функция обработчика `PointerEvent`. Срабатывает, когда браузер отменяет взаимодействие с указателем.
-   `onPointerCancelCapture`: Версия `onPointerCancel`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPointerDown`](https://developer.mozilla.org/docs/Web/API/Element/pointerdown_event): Функция обработчика `PointerEvent`. Срабатывает, когда указатель становится активным.
-   `onPointerDownCapture`: Версия `onPointerDown`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPointerEnter`](https://developer.mozilla.org/docs/Web/API/Element/pointerenter_event): Функция обработчика `PointerEvent`. Срабатывает, когда указатель перемещается внутри элемента. Не имеет фазы захвата. Вместо этого `onPointerLeave` и `onPointerEnter` распространяются от покидаемого элемента к вводимому.
-   [`onPointerLeave`](https://developer.mozilla.org/docs/Web/API/Element/pointerleave_event): Функция обработчика `PointerEvent`. Срабатывает, когда указатель перемещается за пределы элемента. Не имеет фазы захвата. Вместо этого `onPointerLeave` и `onPointerEnter` распространяются от покидаемого элемента к вводимому.
-   [`onPointerMove`](https://developer.mozilla.org/docs/Web/API/Element/pointermove_event): Функция обработчика `PointerEvent`. Срабатывает при изменении координат указателя.
-   `onPointerMoveCapture`: Версия `onPointerMove`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onPointerOut`](https://developer.mozilla.org/docs/Web/API/Element/pointerout_event): Функция обработчика `PointerEvent`. Срабатывает при перемещении указателя за пределы элемента, при отмене взаимодействия с указателем и [по некоторым другим причинам](https://developer.mozilla.org/docs/Web/API/Element/pointerout_event).
-   `onPointerOutCapture`: Версия `onPointerOut`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onPointerUp`](https://developer.mozilla.org/docs/Web/API/Element/pointerup_event): Функция обработчика `PointerEvent`. Срабатывает, когда указатель больше не активен.
-   `onPointerUpCapture`: Версия `onPointerUp`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPaste`](https://developer.mozilla.org/docs/Web/API/Element/paste_event): Функция обработчика `ClipboardEvent`. Срабатывает, когда пользователь пытается вставить что-то из буфера обмена.
-   `onPasteCapture`: Версия `onPaste`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onScroll`](https://developer.mozilla.org/docs/Web/API/Element/scroll_event): Функция обработчика `event`. Срабатывает, когда элемент был прокручен. Это событие не вызывает пузырьков.
-   `onScrollCapture`: Версия `onScroll`, срабатывающая в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onSelect`](https://developer.mozilla.org/docs/Web/API/HTMLInputElement/select_event): Функция обработчика `event`. Срабатывает после изменения выбора внутри редактируемого элемента, например, ввода. React расширяет событие `onSelect`, чтобы оно работало и для элементов `contentEditable={true}`. Кроме того, React расширяет его для срабатывания при пустом выделении и при редактировании (которое может повлиять на выделение).
-   `onSelectCapture`: Версия `onSelect`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onTouchCancel`](https://developer.mozilla.org/docs/Web/API/Element/touchcancel_event): Функция обработчика `TouchEvent`. Срабатывает, когда браузер отменяет сенсорное взаимодействие.
-   `onTouchCancelCapture`: Версия `onTouchCancel`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onTouchEnd`](https://developer.mozilla.org/docs/Web/API/Element/touchend_event): Функция обработчика `TouchEvent`. Срабатывает при удалении одной или нескольких точек касания.
-   `onTouchEndCapture`: Версия `onTouchEnd`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onTouchMove`](https://developer.mozilla.org/docs/Web/API/Element/touchmove_event): Функция обработчика `TouchEvent`. Вызывает перемещение одной или нескольких точек касания.
-   `onTouchMoveCapture`: Версия `onTouchMove`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onTouchStart`](https://developer.mozilla.org/docs/Web/API/Element/touchstart_event): Функция обработчика `TouchEvent`. Срабатывает при размещении одной или нескольких точек касания.
-   `onTouchStartCapture`: Версия `onTouchStart`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onTransitionEnd`](https://developer.mozilla.org/docs/Web/API/Element/transitionend_event): Функция обработчика `TransitionEvent`. Срабатывает при завершении CSS-перехода.
-   `onTransitionEndCapture`: Версия функции `onTransitionEnd`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onWheel`](https://developer.mozilla.org/docs/Web/API/Element/wheel_event): Функция обработчика `WheelEvent`. Срабатывает, когда пользователь поворачивает кнопку колеса.
-   `onWheelCapture`: Версия `onWheel`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events)
-   [`роль`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Roles): Строка. Определяет роль элемента в явном виде для вспомогательных технологий.
-   [`slot`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Roles): Строка. Указывает имя слота при использовании теневого DOM. В React эквивалентная схема обычно достигается путем передачи JSX в качестве props, например `<Layout left={<Sidebar />} right={<Content />} />`.
-   [`spellCheck`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/spellcheck): Булево значение или null. При явном значении `true` или `false` включает или выключает проверку орфографии.
-   [`tabIndex`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/tabindex): Число. Переопределяет поведение кнопки Tab по умолчанию. [Избегайте использования значений, отличных от `-1` и `0`.](https://www.tpgi.com/using-the-tabindex-attribute/)
-   [`title`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/title): Строка. Определяет текст подсказки для элемента.
-   [`translate`](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/translate): Либо `yes`, либо `no`. Передача `no` исключает перевод содержимого элемента.

Вы также можете передавать пользовательские атрибуты в качестве пропсов, например, `mycustomprop="someValue"`. Это может быть полезно при интеграции со сторонними библиотеками. Имя пользовательского атрибута должно быть в нижнем регистре и не должно начинаться с `on`. Значение будет преобразовано в строку. Если вы передадите `null` или `undefined`, пользовательский атрибут будет удален.

Эти события срабатывают только для элементов [`<form>`](https://hcdev.ru/html/form/):

-   [`onReset`](https://developer.mozilla.org/docs/Web/API/HTMLFormElement/reset_event): Функция обработчика `event`. Срабатывает при сбросе формы.
-   `onResetCapture`: Версия функции `onReset`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onSubmit`](https://developer.mozilla.org/docs/Web/API/HTMLFormElement/submit_event): Функция обработчика `event`. Срабатывает при отправке формы.
-   `onSubmitCapture`: Версия `onSubmit`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).

Эти события срабатывают только для элементов [`<dialog>`](https://hcdev.ru/html/dialog/). В отличие от событий браузера, в React они вызывают пузырьки:

-   [`onCancel`](https://developer.mozilla.org/docs/Web/API/HTMLDialogElement/cancel_event): Функция обработчика `event`. Срабатывает, когда пользователь пытается закрыть диалог.
-   `onCancelCapture`: Версия `onCancel`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onClose`](https://developer.mozilla.org/docs/Web/API/HTMLDialogElement/close_event): Функция обработчика `event`. Срабатывает, когда диалог был закрыт.
-   `onCloseCapture`: Версия `onClose`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).

Эти события срабатывают только для элементов [`<details>`](https://hcdev.ru/html/details/). В отличие от браузерных событий, в React они вызывают пузырьки:

-   [`onToggle`](https://developer.mozilla.org/docs/Web/API/HTMLDetailsElement/toggle_event): Функция обработчика `event`. Срабатывает, когда пользователь переключает детали.
-   `onToggleCapture`: Версия `onToggle`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).

Эти события происходят для элементов [`<img>`](https://hcdev.ru/html/img/), [`<iframe>`](https://hcdev.ru/html/iframe/), [`<object>`](https://hcdev.ru/html/object/), [`<embed>`](https://hcdev.ru/html/embed/), [`<link>`](https://hcdev.ru/html/link/) и [SVG `<image>`](https://developer.mozilla.org/docs/Web/SVG/Tutorial/SVG_Image_Tag). В отличие от событий браузера, в React они "всплывают":

-   `onLoad`: Функция обработчика `event`. Срабатывает, когда ресурс загрузился.
-   `onLoadCapture`: Версия `onLoad`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onError`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/error_event): Функция обработчика `event`. Срабатывает, когда ресурс не может быть загружен.
-   `onErrorCapture`: Версия `onError`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).

Эти события происходят для таких ресурсов, как [`<audio>`](https://hcdev.ru/html/audio/) и [`<video>`](https://hcdev.ru/html/video/). В отличие от браузерных событий, в React они "всплывают":

-   [`onAbort`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/abort_event): Функция обработчика `event`. Срабатывает, когда ресурс не загрузился полностью, но не из-за ошибки.
-   `onAbortCapture`: Версия `onAbort`, срабатывающая на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onCanPlay`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/canplay_event): Функция обработчика `event`. Срабатывает, когда данных достаточно для начала воспроизведения, но недостаточно для воспроизведения до конца без буферизации.
-   `onCanPlayCapture`: Версия `onCanPlay`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onCanPlayThrough`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/canplaythrough_event): Функция обработчика `event`. Срабатывает, когда данных достаточно, чтобы можно было начать воспроизведение без буферизации до конца.
-   `onCanPlayThroughCapture`: Версия `onCanPlayThrough`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onDurationChange`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/durationchange_event): Функция обработчика `event`. Срабатывает при обновлении длительности носителя.
-   `onDurationChangeCapture`: Версия `onDurationChange`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onEmptied`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/emptied_event): Функция обработчика `event`. Срабатывает, когда носитель становится пустым.
-   `onEmptiedCapture`: Версия `onEmptied`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onEncrypted`](https://w3c.github.io/encrypted-media/#dom-evt-encrypted): Функция обработчика `event`. Срабатывает, когда браузер сталкивается с зашифрованным медиа.
-   `onEncryptedCapture`: Версия `onEncrypted`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onEnded`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/ended_event): Функция обработчика `event`. Срабатывает, когда воспроизведение останавливается, потому что больше нечего воспроизводить.
-   `onEndedCapture`: Версия `onEnded`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onError`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/error_event): Функция обработчика `event`. Срабатывает, когда ресурс не может быть загружен.
-   `onErrorCapture`: Версия `onError`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onLoadedData`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/loadeddata_event): Функция обработчика `event`. Срабатывает при загрузке текущего кадра воспроизведения.
-   `onLoadedDataCapture`: Версия `onLoadedData`, которая срабатывает в [фазе захвата.](../../../learn/responding-to-events.md#capture-phase-events)
-   [`onLoadedMetadata`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/loadedmetadata_event): Функция обработчика `event`. Срабатывает при загрузке метаданных.
-   `onLoadedMetadataCapture`: Версия `onLoadedMetadata`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   Срабатывает при загрузке метаданных.
-   `onLoadedMetadataCapture`: Версия `onLoadedMetadata`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onLoadStart`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/loadstart_event): Функция обработчика `event`. Срабатывает, когда браузер начал загрузку ресурса.
-   `onLoadStartCapture`: Версия `onLoadStart`, которая срабатывает на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPause`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/pause_event): Функция обработчика `event`. Срабатывает, когда медиа было приостановлено.
-   `onPauseCapture`: Версия `onPause`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPlay`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/play_event): Функция обработчика `event`. Срабатывает, когда медиа больше не приостановлено.
-   `onPlayCapture`: Версия `onPlay`, срабатывающая в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onPlaying`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/playing_event): Функция обработчика `event`. Срабатывает, когда медиа начинает или возобновляет воспроизведение.
-   `onPlayingCapture`: Версия функции `onPlaying`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onProgress`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/progress_event): Функция обработчика `event`. Периодически срабатывает во время загрузки ресурса.
-   `onProgressCapture`: Версия функции `onProgress`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onRateChange`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/ratechange_event): Функция обработчика `event`. Срабатывает при изменении скорости воспроизведения.
-   `onRateChangeCapture`: Версия `onRateChange`, срабатывающая в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   `onResize`: Функция обработчика `event`. Срабатывает при изменении размера видео.
-   `onResizeCapture`: Версия `onResize`, срабатывающая на [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onSeeked`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/seeked_event): Функция обработчика `event`. Срабатывает при завершении операции поиска.
-   `onSeekedCapture`: Версия функции `onSeeked`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onSeeking`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/seeking_event): Функция обработчика `event`. Срабатывает, когда начинается операция поиска.
-   `onSeekingCapture`: Версия функции `onSeeking`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onStalled`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/stalled_event): Функция обработчика `event`. Срабатывает, когда браузер ожидает данные, но они не загружаются.
-   `onStalledCapture`: Версия функции `onStalled`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onSuspend`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/suspend_event): Функция обработчика `event`. Срабатывает, когда загрузка ресурса была приостановлена.
-   `onSuspendCapture`: Версия `onSuspend`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onTimeUpdate`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/timeupdate_event): Функция обработчика `event`. Срабатывает при обновлении текущего времени воспроизведения.
-   `onTimeUpdateCapture`: Версия `onTimeUpdate`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onVolumeChange`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/volumechange_event): Функция обработчика `event`. Срабатывает при изменении громкости.
-   `onVolumeChangeCapture`: Версия функции `onVolumeChange`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).
-   [`onWaiting`](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement/waiting_event): Функция обработчика `event`. Срабатывает, когда воспроизведение остановилось из-за временного отсутствия данных.
-   `onWaitingCapture`: Версия функции `onWaiting`, которая срабатывает в [фазе захвата](../../../learn/responding-to-events.md#capture-phase-events).

**Предостережения**

-   Вы не можете одновременно передавать `children` и `dangerouslySetInnerHTML`.
-   Некоторые события (например, `onAbort` и `onLoad`) не отображаются в браузере, но отображаются в React.

### `ref` функция обратного вызова

Вместо объекта ref (например, возвращаемого [`useRef`](../../react/useRef.md#manipulating-the-dom-with-a-ref)), вы можете передать функцию в атрибут `ref`.

```js
<div ref={(node) => console.log(node)} />
```

[Смотрите пример использования обратного вызова `ref`.](../../../learn/manipulating-the-dom-with-refs.md#how-to-manage-a-list-of-refs-using-a-ref-callback)

Когда DOM-узел `div` будет добавлен на экран, React вызовет ваш обратный вызов `ref` с DOM-узлом `node` в качестве аргумента. Когда этот DOM-узел `div` будет удален, React вызовет ваш обратный вызов `ref` с аргументом `null`.

React также будет вызывать ваш обратный вызов `ref` всякий раз, когда вы передадите _другой_ обратный вызов `ref`. В приведенном выше примере `(node) => { ... }` - это разные функции при каждом рендере. При повторном рендеринге вашего компонента будет вызвана _предыдущая_ функция с `null` в качестве аргумента, а _следующая_ функция будет вызвана с DOM-узлом.

**Параметры**

-   `node`: Узел DOM или `null`. React передаст вам узел DOM, когда ссылка будет присоединена, и `null`, когда ссылка будет отсоединена. Если вы не передадите одну и ту же ссылку на функцию для обратного вызова `ref` при каждом рендере, обратный вызов будет временно отсоединен и вновь присоединен при каждом повторном рендере компонента.

**Возвращает**

Не возвращает ничего из обратного вызова `ref`.

### Объект события React

Ваши обработчики событий будут получать _объект события React._ Он также иногда известен как "синтетическое событие".

```js
<button
    onClick={(e) => {
        console.log(e); // React event object
    }}
/>
```

Он соответствует тому же стандарту, что и базовые события DOM, но исправляет некоторые несоответствия в браузере.

Некоторые события React не отображаются непосредственно на "родные" события браузера. Например, в `onMouseLeave`, `e.nativeEvent` будет указывать на событие `mouseout`. Конкретное сопоставление не является частью общедоступного API и может измениться в будущем. Если вам зачем-то нужно базовое событие браузера, считайте его из `e.nativeEvent`.

**Свойства**

Объекты событий React реализуют некоторые из стандартных свойств [`Event`](https://developer.mozilla.org/docs/Web/API/Event):

-   [`bubbles`](https://developer.mozilla.org/docs/Web/API/Event/bubbles): Булево. Возвращает, распространяется ли событие через DOM.
-   [`cancelable`](https://developer.mozilla.org/docs/Web/API/Event/cancelable): Булево. Возвращает, может ли событие быть отменено.
-   [`currentTarget`](https://developer.mozilla.org/docs/Web/API/Event/currentTarget): Узел DOM. Возвращает узел, к которому прикреплен текущий обработчик в дереве React.
-   [`defaultPrevented`](https://developer.mozilla.org/docs/Web/API/Event/defaultPrevented): Булево значение. Возвращает, была ли вызвана функция `preventDefault`.
-   [`eventPhase`](https://developer.mozilla.org/docs/Web/API/Event/eventPhase): Число. Возвращает, в какой фазе находится событие в данный момент.
-   [`isTrusted`](https://developer.mozilla.org/docs/Web/API/Event/isTrusted): Булево значение. Возвращает, было ли событие инициировано пользователем.
-   [`target`](https://developer.mozilla.org/docs/Web/API/Event/target): Узел DOM. Возвращает узел, на котором произошло событие (который может быть дальним потомком).
-   [`timeStamp`](https://developer.mozilla.org/docs/Web/API/Event/timeStamp): Число. Возвращает время, когда произошло событие.

Кроме того, объекты событий React предоставляют следующие свойства:

-   `nativeEvent`: DOM [`Event`](https://developer.mozilla.org/docs/Web/API/Event). Оригинальный объект события браузера.

**Методы**

Объекты событий React реализуют некоторые из стандартных методов [`Event`](https://developer.mozilla.org/docs/Web/API/Event):

-   [`preventDefault()`](https://developer.mozilla.org/docs/Web/API/Event/preventDefault): Предотвращает действие браузера по умолчанию для данного события.
-   [`stopPropagation()`](https://developer.mozilla.org/docs/Web/API/Event/stopPropagation): Останавливает распространение события по дереву React.

Кроме того, объекты событий React предоставляют следующие методы:

-   `isDefaultPrevented()`: Возвращает булево значение, указывающее, было ли вызвано `preventDefault`.
-   `isPropagationStopped()`: Возвращает булево значение, указывающее, была ли вызвана функция `stopPropagation`.
-   `persist()`: Не используется в React DOM. В React Native вызовите эту функцию, чтобы прочитать свойства события после его наступления.
-   `isPersistent()`: Не используется в React DOM. В React Native возвращает, была ли вызвана функция `persist`.

**Ограничения**

-   Значения `currentTarget`, `eventPhase`, `target` и `type` отражают значения, которые ожидает ваш код React. Под капотом React прикрепляет обработчики событий к корню, но это не отражается в объектах событий React. Например, `e.currentTarget` может не совпадать с базовым `e.nativeEvent.currentTarget`. Для полизаполненных событий `e.type` (тип события React) может отличаться от `e.nativeEvent.type` (базовый тип).

### `AnimationEvent` функция обработчика

Тип обработчика событий для событий [CSS animation](https://developer.mozilla.org/docs/Web/CSS/CSS_Animations/Using_CSS_animations).

```js
<div
    onAnimationStart={(e) =>
        console.log('onAnimationStart')
    }
    onAnimationIteration={(e) =>
        console.log('onAnimationIteration')
    }
    onAnimationEnd={(e) => console.log('onAnimationEnd')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`AnimationEvent`](https://developer.mozilla.org/docs/Web/API/AnimationEvent):

    -   [`animationName`](https://developer.mozilla.org/docs/Web/API/AnimationEvent/animationName)
    -   [`elapsedTime`](https://developer.mozilla.org/docs/Web/API/AnimationEvent/elapsedTime)
    -   [`псевдоэлемент`](https://developer.mozilla.org/docs/Web/API/AnimationEvent)

### `ClipboardEvent` функция обработчика

Тип обработчика событий для событий [Clipboard API](https://developer.mozilla.org/docs/Web/API/Clipboard_API).

```js
<input
    onCopy={(e) => console.log('onCopy')}
    onCut={(e) => console.log('onCut')}
    onPaste={(e) => console.log('onPaste')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`ClipboardEvent`](https://developer.mozilla.org/docs/Web/API/ClipboardEvent):

    -   [`clipboardData`](https://developer.mozilla.org/docs/Web/API/ClipboardEvent/clipboardData)

### `CompositionEvent` функция обработчика

Тип обработчика событий для событий [редактора методов ввода (IME)](https://developer.mozilla.org/docs/Glossary/Input_method_editor).

```js
<input
    onCompositionStart={(e) =>
        console.log('onCompositionStart')
    }
    onCompositionUpdate={(e) =>
        console.log('onCompositionUpdate')
    }
    onCompositionEnd={(e) =>
        console.log('onCompositionEnd')
    }
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`CompositionEvent`](https://developer.mozilla.org/docs/Web/API/CompositionEvent):

    -   [`data`](https://developer.mozilla.org/docs/Web/API/CompositionEvent/data)

### `DragEvent` функция обработчика

Тип обработчика событий для событий [HTML Drag and Drop API](https://developer.mozilla.org/docs/Web/API/HTML_Drag_and_Drop_API).

```js
<>
    <div
        draggable={true}
        onDragStart={(e) => console.log('onDragStart')}
        onDragEnd={(e) => console.log('onDragEnd')}
    >
        Drag source
    </div>

    <div
        onDragEnter={(e) => console.log('onDragEnter')}
        onDragLeave={(e) => console.log('onDragLeave')}
        onDragOver={(e) => {
            e.preventDefault();
            console.log('onDragOver');
        }}
        onDrop={(e) => console.log('onDrop')}
    >
        Drop target
    </div>
</>
```

**Параметры**

-   `e`: React event object с этими дополнительными свойствами [`DragEvent`](https://developer.mozilla.org/docs/Web/API/DragEvent):

    -   [`dataTransfer`](https://developer.mozilla.org/docs/Web/API/DragEvent/dataTransfer)

    Он также включает унаследованные свойства [`MouseEvent`](https://developer.mozilla.org/docs/Web/API/MouseEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/altKey)
    -   [`button`](https://developer.mozilla.org/docs/Web/API/MouseEvent/button)
    -   [`buttons`](https://developer.mozilla.org/docs/Web/API/MouseEvent/buttons)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/ctrlKey)
    -   [`clientX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientX)
    -   [`clientY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientY)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/MouseEvent/getModifierState)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/metaKey)
    -   [`movementX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementX)
    -   [`movementY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementY)
    -   [`pageX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageX)
    -   [`pageY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageY)
    -   [`relatedTarget`](https://developer.mozilla.org/docs/Web/API/MouseEvent/relatedTarget)
    -   [`screenX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenX)
    -   [`screenY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenY)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/shiftKey)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `FocusEvent` функция обработчика

Тип обработчика событий для событий фокуса.

```js
<input
    onFocus={(e) => console.log('onFocus')}
    onBlur={(e) => console.log('onBlur')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`FocusEvent`](https://developer.mozilla.org/docs/Web/API/FocusEvent):

    -   [`relatedTarget`](https://developer.mozilla.org/docs/Web/API/FocusEvent/relatedTarget)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `Event` функция обработчика

Тип обработчика событий для общих событий.

**Параметры**

-   `e`: объект события React без дополнительных свойств.

### `InputEvent` функция-обработчик

Тип обработчика события для события `onBeforeInput`.

```js
<input
    onBeforeInput={(e) => console.log('onBeforeInput')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`InputEvent`](https://developer.mozilla.org/docs/Web/API/InputEvent):

    -   [`data`](https://developer.mozilla.org/docs/Web/API/InputEvent/data)

### `KeyboardEvent` функция обработчика

Тип обработчика событий для событий клавиатуры.

```js
<input
    onKeyDown={(e) => console.log('onKeyDown')}
    onKeyUp={(e) => console.log('onKeyUp')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`KeyboardEvent`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/altKey)
    -   [`charCode`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/charCode)
    -   [`code`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/code)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/ctrlKey)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/getModifierState)
    -   [`key`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/key)
    -   [`keyCode`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/keyCode)
    -   [`locale`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/locale)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/metaKey)
    -   [`location`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/location)
    -   [`repeat`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/repeat)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/shiftKey)
    -   [`which`](https://developer.mozilla.org/docs/Web/API/KeyboardEvent/which)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `MouseEvent` функция-обработчик

Тип обработчика событий для событий мыши.

```js
<div
    onClick={(e) => console.log('onClick')}
    onMouseEnter={(e) => console.log('onMouseEnter')}
    onMouseOver={(e) => console.log('onMouseOver')}
    onMouseDown={(e) => console.log('onMouseDown')}
    onMouseUp={(e) => console.log('onMouseUp')}
    onMouseLeave={(e) => console.log('onMouseLeave')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`MouseEvent`](https://developer.mozilla.org/docs/Web/API/MouseEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/altKey)
    -   [`button`](https://developer.mozilla.org/docs/Web/API/MouseEvent/button)
    -   [`buttons`](https://developer.mozilla.org/docs/Web/API/MouseEvent/buttons)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/ctrlKey)
    -   [`clientX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientX)
    -   [`clientY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientY)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/MouseEvent/getModifierState)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/metaKey)
    -   [`movementX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementX)
    -   [`movementY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementY)
    -   [`pageX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageX)
    -   [`pageY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageY)
    -   [`relatedTarget`](https://developer.mozilla.org/docs/Web/API/MouseEvent/relatedTarget)
    -   [`screenX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenX)
    -   [`screenY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenY)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/shiftKey)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `PointerEvent` функция обработчика

Тип обработчика событий для [событий указателя.](https://developer.mozilla.org/docs/Web/API/Pointer_events)

```js
<div
    onPointerEnter={(e) => console.log('onPointerEnter')}
    onPointerMove={(e) => console.log('onPointerMove')}
    onPointerDown={(e) => console.log('onPointerDown')}
    onPointerUp={(e) => console.log('onPointerUp')}
    onPointerLeave={(e) => console.log('onPointerLeave')}
/>
```

**Параметры**

-   `e`: Объект React event object с этими дополнительными свойствами [`PointerEvent`](https://developer.mozilla.org/docs/Web/API/PointerEvent):

    -   [`height`](https://developer.mozilla.org/docs/Web/API/PointerEvent/height)
    -   [`isPrimary`](https://developer.mozilla.org/docs/Web/API/PointerEvent/isPrimary)
    -   [`pointerId`](https://developer.mozilla.org/docs/Web/API/PointerEvent/pointerId)
    -   [`pointerType`](https://developer.mozilla.org/docs/Web/API/PointerEvent/pointerType)
    -   [`pressure`](https://developer.mozilla.org/docs/Web/API/PointerEvent/pressure)
    -   [`tangentialPressure`](https://developer.mozilla.org/docs/Web/API/PointerEvent/tangentialPressure)
    -   [`tiltX`](https://developer.mozilla.org/docs/Web/API/PointerEvent/tiltX)
    -   [`tiltY`](https://developer.mozilla.org/docs/Web/API/PointerEvent/tiltY)
    -   [`twist`](https://developer.mozilla.org/docs/Web/API/PointerEvent/twist)
    -   [`width`](https://developer.mozilla.org/docs/Web/API/PointerEvent/width)

    Он также включает унаследованные свойства [`MouseEvent`](https://developer.mozilla.org/docs/Web/API/MouseEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/altKey)
    -   [`button`](https://developer.mozilla.org/docs/Web/API/MouseEvent/button)
    -   [`buttons`](https://developer.mozilla.org/docs/Web/API/MouseEvent/buttons)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/ctrlKey)
    -   [`clientX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientX)
    -   [`clientY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientY)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/MouseEvent/getModifierState)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/metaKey)
    -   [`movementX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementX)
    -   [`movementY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementY)
    -   [`pageX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageX)
    -   [`pageY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageY)
    -   [`relatedTarget`](https://developer.mozilla.org/docs/Web/API/MouseEvent/relatedTarget)
    -   [`screenX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenX)
    -   [`screenY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenY)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/shiftKey)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `TouchEvent` функция обработчика

Тип обработчика событий для [событий касания.](https://developer.mozilla.org/docs/Web/API/Touch_events)

```js
<div
    onTouchStart={(e) => console.log('onTouchStart')}
    onTouchMove={(e) => console.log('onTouchMove')}
    onTouchEnd={(e) => console.log('onTouchEnd')}
    onTouchCancel={(e) => console.log('onTouchCancel')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`TouchEvent`](https://developer.mozilla.org/docs/Web/API/TouchEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/TouchEvent/altKey)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/TouchEvent/ctrlKey)
    -   [`changedTouches`](https://developer.mozilla.org/docs/Web/API/TouchEvent/changedTouches)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/TouchEvent/getModifierState)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/TouchEvent/metaKey)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/TouchEvent/shiftKey)
    -   [`touches`](https://developer.mozilla.org/docs/Web/API/TouchEvent/touches)
    -   [`targetTouches`](https://developer.mozilla.org/docs/Web/API/TouchEvent/targetTouches)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `TransitionEvent` функция обработчика

Тип обработчика событий для событий перехода CSS.

```js
<div
    onTransitionEnd={(e) => console.log('onTransitionEnd')}
/>
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`TransitionEvent`](https://developer.mozilla.org/docs/Web/API/TransitionEvent):

    -   [`elapsedTime`](https://developer.mozilla.org/docs/Web/API/TransitionEvent/elapsedTime)
    -   [`propertyName`](https://developer.mozilla.org/docs/Web/API/TransitionEvent/propertyName)
    -   [`pseudoElement`](https://developer.mozilla.org/docs/Web/API/TransitionEvent/pseudoElement)

### `UIEvent` функция обработчик

Тип обработчика событий для общих событий пользовательского интерфейса.

```js
<div onScroll={(e) => console.log('onScroll')} />
```

**Параметры**

-   `e`: объект события React с этими дополнительными свойствами [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

### `WheelEvent` функция обработчика

Тип обработчика события для события `onWheel`.

```js
<div onScroll={(e) => console.log('onScroll')} />
```

**Параметры**

-   `e`: React event object с этими дополнительными свойствами [`WheelEvent`](https://developer.mozilla.org/docs/Web/API/WheelEvent):

    -   [`deltaMode`](https://developer.mozilla.org/docs/Web/API/WheelEvent/deltaMode)
    -   [`deltaX`](https://developer.mozilla.org/docs/Web/API/WheelEvent/deltaX)
    -   [`deltaY`](https://developer.mozilla.org/docs/Web/API/WheelEvent/deltaY)
    -   [`deltaZ`](https://developer.mozilla.org/docs/Web/API/WheelEvent/deltaZ)

    Он также включает унаследованные свойства [`MouseEvent`](https://developer.mozilla.org/docs/Web/API/MouseEvent):

    -   [`altKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/altKey)
    -   [`button`](https://developer.mozilla.org/docs/Web/API/MouseEvent/button)
    -   [`buttons`](https://developer.mozilla.org/docs/Web/API/MouseEvent/buttons)
    -   [`ctrlKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/ctrlKey)
    -   [`clientX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientX)
    -   [`clientY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/clientY)
    -   [`getModifierState(key)`](https://developer.mozilla.org/docs/Web/API/MouseEvent/getModifierState)
    -   [`metaKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/metaKey)
    -   [`movementX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementX)
    -   [`movementY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/movementY)
    -   [`pageX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageX)
    -   [`pageY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/pageY)
    -   [`relatedTarget`](https://developer.mozilla.org/docs/Web/API/MouseEvent/relatedTarget)
    -   [`screenX`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenX)
    -   [`screenY`](https://developer.mozilla.org/docs/Web/API/MouseEvent/screenY)
    -   [`shiftKey`](https://developer.mozilla.org/docs/Web/API/MouseEvent/shiftKey)

    Он также включает унаследованные свойства [`UIEvent`](https://developer.mozilla.org/docs/Web/API/UIEvent):

    -   [`detail`](https://developer.mozilla.org/docs/Web/API/UIEvent/detail)
    -   [`view`](https://developer.mozilla.org/docs/Web/API/UIEvent/view)

## Использование

### Применение стилей CSS

В React вы указываете CSS-класс с помощью [`className`](https://developer.mozilla.org/docs/Web/API/Element/className). Это работает как атрибут `class` в HTML:

```js
<img className="avatar" />
```

Затем вы пишете правила CSS для него в отдельном файле CSS:

```css
/* In your CSS */
.avatar {
    border-radius: 50%;
}
```

React не предписывает, как добавлять файлы CSS. В простейшем случае вы добавляете тег [`<link>`](https://hcdev.ru/html/link/) в HTML. Если вы используете инструмент сборки или фреймворк, обратитесь к его документации, чтобы узнать, как добавить CSS-файл в ваш проект.

Иногда значения стиля зависят от данных. Используйте атрибут `style`, чтобы передать некоторые стили динамически:

```js
<img
    className="avatar"
    style={{
        width: user.imageSize,
        height: user.imageSize,
    }}
/>
```

В приведенном выше примере `style={{}}` - это не специальный синтаксис, а обычный объект `{}` внутри `style={ }` [фигурные скобки JSX.](../../../learn/javascript-in-jsx-with-curly-braces.md) Мы рекомендуем использовать атрибут `style` только тогда, когда ваши стили зависят от переменных JavaScript.

=== "App.js"

    ```js
    import Avatar from './Avatar.js';

    const user = {
    	name: 'Hedy Lamarr',
    	imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',
    	imageSize: 90,
    };

    export default function App() {
    	return <Avatar user={user} />;
    }
    ```

=== "Avatar.js"

    ```js
    export default function Avatar({ user }) {
    	return (
    		<img
    			src={user.imageUrl}
    			alt={'Photo of ' + user.name}
    			className="avatar"
    			style={{
    				width: user.imageSize,
    				height: user.imageSize,
    			}}
    		/>
    	);
    }
    ```

=== "styles.css"

    ```css
    .avatar {
    	border-radius: 50%;
    }
    ```

!!!note "Как применить несколько классов CSS условно?"

    Чтобы применить классы CSS условно, вам нужно создать строку `className` самостоятельно с помощью JavaScript.

    Например, `className={'row ' + (isSelected ? 'selected': '')}` создаст либо `className="row"`, либо `className="row selected"` в зависимости от того, является ли `isSelected` `true`.

    Чтобы сделать это более читабельным, вы можете использовать небольшую вспомогательную библиотеку, например [`classnames`:](https://github.com/JedWatson/classnames)

    ```js
    import cn from 'classnames';

    function Row({ isSelected }) {
    	return (
    		<div
    			className={cn('row', isSelected && 'selected')}
    		>
    			...
    		</div>
    	);
    }
    ```

    Это особенно удобно, если у вас несколько условных классов:

    ```js
    import cn from 'classnames';

    function Row({ isSelected, size }) {
    	return (
    		<div
    			className={cn('row', {
    				selected: isSelected,
    				large: size === 'large',
    				small: size === 'small',
    			})}
    		>
    			...
    		</div>
    	);
    }
    ```

### Манипулирование узлом DOM с помощью ссылки

Иногда вам нужно получить узел DOM браузера, связанный с тегом в JSX. Например, если вы хотите сфокусировать `input` при нажатии на кнопку, вам нужно вызвать [`focus()`](https://developer.mozilla.org/docs/Web/API/HTMLElement/focus) на DOM-узле браузера `input`.

Чтобы получить DOM-узел браузера для тега, [объявите ссылку](../../react/useRef.md) и передайте ее в качестве атрибута `ref` этому тегу:

```js
import { useRef } from 'react';

export default function Form() {
    const inputRef = useRef(null);
    // ...
    return (
        <input ref={inputRef} />
        // ..
    );
}
```

React поместит узел DOM в `inputRef.current` после того, как он будет выведен на экран.

```js
import { useRef } from 'react';

export default function Form() {
    const inputRef = useRef(null);

    function handleClick() {
        inputRef.current.focus();
    }

    return (
        <>
            <input ref={inputRef} />
            <button onClick={handleClick}>
                Focus the input
            </button>
        </>
    );
}
```

Читайте больше о [манипулировании DOM с помощью ссылок](../../../learn/manipulating-the-dom-with-refs.md) и [посмотрите больше примеров](../../react/useRef.md#examples-dom).

Для более сложных случаев использования атрибут `ref` также принимает функцию обратного вызова.

### Опасная установка внутреннего HTML

Вы можете передать необработанную строку HTML элементу следующим образом:

```js
const markup = { __html: '<p>some raw html</p>' };
return <div dangerouslySetInnerHTML={markup} />;
```

**Это опасно. Как и в случае со свойством [`innerHTML`](https://developer.mozilla.org/docs/Web/API/Element/innerHTML), лежащим в основе DOM, вы должны проявлять крайнюю осторожность! Если только разметка не поступает из абсолютно надежного источника, то таким образом можно легко внедрить [XSS](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%B6%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%D1%8B%D0%B9_%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%B8%D0%BD%D0%B3) уязвимость**.

Например, если вы используете библиотеку Markdown, которая преобразует Markdown в HTML, доверяете, что ее парсер не содержит ошибок, а пользователь видит только свой собственный ввод, вы можете отобразить полученный HTML следующим образом:

=== "App.js"

    ```js
    import { useState } from 'react';
    import MarkdownPreview from './MarkdownPreview.js';

    export default function MarkdownEditor() {
    	const [postContent, setPostContent] = useState(
    		'_Hello,_ **Markdown**!'
    	);
    	return (
    		<>
    			<label>
    				Enter some markdown:
    				<textarea
    					value={postContent}
    					onChange={(e) =>
    						setPostContent(e.target.value)
    					}
    				/>
    			</label>
    			<hr />
    			<MarkdownPreview markdown={postContent} />
    		</>
    	);
    }
    ```

=== "MarkdownPreview.js"

    ```js
    import { Remarkable } from 'remarkable';

    const md = new Remarkable();

    function renderMarkdownToHTML(markdown) {
    	// This is ONLY safe because the output HTML
    	// is shown to the same user, and because you
    	// trust this Markdown parser to not have bugs.
    	const renderedHTML = md.render(markdown);
    	return { __html: renderedHTML };
    }

    export default function MarkdownPreview({ markdown }) {
    	const markup = renderMarkdownToHTML(markdown);
    	return <div dangerouslySetInnerHTML={markup} />;
    }
    ```

Чтобы понять, почему рендеринг произвольного HTML опасен, замените приведенный выше код на следующий:

```js
const post = {
    // Imagine this content is stored in the database.
    content: `<img src="" onerror='alert("you were hacked")'>`,
};

export default function MarkdownPreview() {
    // 🔴 SECURITY HOLE: passing untrusted input to dangerouslySetInnerHTML
    const markup = { __html: post.content };
    return <div dangerouslySetInnerHTML={markup} />;
}
```

Код, встроенный в HTML, будет запущен. Хакер может использовать эту брешь в безопасности для кражи информации пользователя или выполнения действий от его имени. **Используйте `dangerouslySetInnerHTML` только с доверенными и проверенными данными.**.

### Обработка событий мыши

Этот пример показывает некоторые общие события мыши и время их возникновения.

```js
export default function MouseExample() {
    return (
        <div
            onMouseEnter={(e) =>
                console.log('onMouseEnter (parent)')
            }
            onMouseLeave={(e) =>
                console.log('onMouseLeave (parent)')
            }
        >
            <button
                onClick={(e) =>
                    console.log('onClick (first button)')
                }
                onMouseDown={(e) =>
                    console.log(
                        'onMouseDown (first button)'
                    )
                }
                onMouseEnter={(e) =>
                    console.log(
                        'onMouseEnter (first button)'
                    )
                }
                onMouseLeave={(e) =>
                    console.log(
                        'onMouseLeave (first button)'
                    )
                }
                onMouseOver={(e) =>
                    console.log(
                        'onMouseOver (first button)'
                    )
                }
                onMouseUp={(e) =>
                    console.log('onMouseUp (first button)')
                }
            >
                First button
            </button>
            <button
                onClick={(e) =>
                    console.log('onClick (second button)')
                }
                onMouseDown={(e) =>
                    console.log(
                        'onMouseDown (second button)'
                    )
                }
                onMouseEnter={(e) =>
                    console.log(
                        'onMouseEnter (second button)'
                    )
                }
                onMouseLeave={(e) =>
                    console.log(
                        'onMouseLeave (second button)'
                    )
                }
                onMouseOver={(e) =>
                    console.log(
                        'onMouseOver (second button)'
                    )
                }
                onMouseUp={(e) =>
                    console.log('onMouseUp (second button)')
                }
            >
                Second button
            </button>
        </div>
    );
}
```

### Обработка событий указателя

Этот пример показывает некоторые общие события pointer-events и время их возникновения.

```js
export default function PointerExample() {
    return (
        <div
            onPointerEnter={(e) =>
                console.log('onPointerEnter (parent)')
            }
            onPointerLeave={(e) =>
                console.log('onPointerLeave (parent)')
            }
            style={{ padding: 20, backgroundColor: '#ddd' }}
        >
            <div
                onPointerDown={(e) =>
                    console.log(
                        'onPointerDown (first child)'
                    )
                }
                onPointerEnter={(e) =>
                    console.log(
                        'onPointerEnter (first child)'
                    )
                }
                onPointerLeave={(e) =>
                    console.log(
                        'onPointerLeave (first child)'
                    )
                }
                onPointerMove={(e) =>
                    console.log(
                        'onPointerMove (first child)'
                    )
                }
                onPointerUp={(e) =>
                    console.log('onPointerUp (first child)')
                }
                style={{
                    padding: 20,
                    backgroundColor: 'lightyellow',
                }}
            >
                First child
            </div>
            <div
                onPointerDown={(e) =>
                    console.log(
                        'onPointerDown (second child)'
                    )
                }
                onPointerEnter={(e) =>
                    console.log(
                        'onPointerEnter (second child)'
                    )
                }
                onPointerLeave={(e) =>
                    console.log(
                        'onPointerLeave (second child)'
                    )
                }
                onPointerMove={(e) =>
                    console.log(
                        'onPointerMove (second child)'
                    )
                }
                onPointerUp={(e) =>
                    console.log(
                        'onPointerUp (second child)'
                    )
                }
                style={{
                    padding: 20,
                    backgroundColor: 'lightblue',
                }}
            >
                Second child
            </div>
        </div>
    );
}
```

### Обработка событий фокуса

В React, focus events пузырьковый. Вы можете использовать `currentTarget` и `relatedTarget`, чтобы отличить, если события фокусировки или размытия возникли вне родительского элемента. Пример показывает, как обнаружить фокусировку дочернего элемента, фокусировку родительского элемента, а также как обнаружить вхождение или выход фокуса из всего поддерева.

```js
export default function FocusExample() {
    return (
        <div
            tabIndex={1}
            onFocus={(e) => {
                if (e.currentTarget === e.target) {
                    console.log('focused parent');
                } else {
                    console.log(
                        'focused child',
                        e.target.name
                    );
                }
                if (
                    !e.currentTarget.contains(
                        e.relatedTarget
                    )
                ) {
                    // Not triggered when swapping focus between children
                    console.log('focus entered parent');
                }
            }}
            onBlur={(e) => {
                if (e.currentTarget === e.target) {
                    console.log('unfocused parent');
                } else {
                    console.log(
                        'unfocused child',
                        e.target.name
                    );
                }
                if (
                    !e.currentTarget.contains(
                        e.relatedTarget
                    )
                ) {
                    // Not triggered when swapping focus between children
                    console.log('focus left parent');
                }
            }}
        >
            <label>
                First name:
                <input name="firstName" />
            </label>
            <label>
                Last name:
                <input name="lastName" />
            </label>
        </div>
    );
}
```

### Обработка событий клавиатуры

Этот пример показывает некоторые общие клавиатурные события и время их возникновения.

```js
export default function KeyboardExample() {
    return (
        <label>
            First name:
            <input
                name="firstName"
                onKeyDown={(e) =>
                    console.log('onKeyDown:', e.key, e.code)
                }
                onKeyUp={(e) =>
                    console.log('onKeyUp:', e.key, e.code)
                }
            />
        </label>
    );
}
```
