# CSSTransition

Компонент перехода, созданный на основе замечательной библиотеки [`ng-animate`](https://docs.angularjs.org/api/ngAnimate). Его следует использовать, если вы используете CSS-переходы или анимацию. Он создан на основе компонента [`Transition`](transition.md), поэтому наследует все его реквизиты.

`CSSTransition` применяет пару имен классов во время состояний `appear`, `enter` и `exit` перехода. Применяется первый класс, а затем второй класс `*-active`, чтобы активировать CSS-переход. После перехода применяются соответствующие имена классов `*-done`, чтобы сохранить состояние перехода.

```jsx
function App() {
  const [inProp, setInProp] = useState(false);
  const nodeRef = useRef(null);
  return (
    <div>
      <CSSTransition
        nodeRef={nodeRef}
        in={inProp}
        timeout={200}
        classNames="my-node"
      >
        <div ref={nodeRef}>
          {"I'll receive my-node-* classes"}
        </div>
      </CSSTransition>
      <button type="button" onClick={() => setInProp(true)}>
        Click to Enter
      </button>
    </div>
  );
}
```

Когда параметр `in` установлен в `true`, дочерний компонент сначала получит класс `example-enter`, затем `example-enter-active` будет добавлен в следующем тике. `CSSTransition` [заставляет переливаться](https://github.com/reactjs/react-transition-group/blob/5007303e729a74be66a21c3e2205e4916821524b/src/CSSTransition.js#L208-L215) между перед добавлением `example-enter-active`. Это важный прием, поскольку он позволяет нам осуществить переход между `example-enter` и `example-enter-active`, даже если они были добавлены сразу же друг за другом. Более того, именно это позволяет нам анимировать _появление_.

```css
.my-node-enter {
  opacity: 0;
}
.my-node-enter-active {
  opacity: 1;
  transition: opacity 200ms;
}
.my-node-exit {
  opacity: 1;
}
.my-node-exit-active {
  opacity: 0;
  transition: opacity 200ms;
}
```

Классы `*-active` представляют стили, к которым вы хотите анимировать, поэтому важно добавить объявление `transition` только к ним, иначе переходы могут вести себя не так, как задумано! Это может быть неочевидно, когда переходы симметричны, т. е. когда `*-enter-active` является тем же самым, что и `*-exit`, как в примере выше (минус `transition`), но это становится очевидным при более сложных переходах.

!!!note ""

    Если вы используете реквизит `appear`, не забудьте определить стили и для классов `.appear-*`.

## Пример

<iframe title="CSSTransition Component" src="https://codesandbox.io/embed/m77l2vp00x?fontsize=14" sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin" style="display: block; width: 100%; height: 500px; border: 0px; border-radius: 4px; overflow: hidden;"></iframe>

## Свойства

Принимает все реквизиты из `<Transition>`, если не указано иное.

### classNames

Имена классов анимации, применяемые к компоненту при его появлении, входе, выходе или завершении перехода. Можно указать одно имя, которое будет иметь суффикс для каждого этапа, например, применяется `classNames="fade"`:

- `fade-appear`, `fade-appear-active`, `fade-appear-done`
- `fade-enter`, `fade-enter-active`, `fade-enter-done`
- `fade-exit`, `fade-exit-active`, `fade-exit-done`

Следует отметить несколько деталей о том, как применяются эти классы:

1. Они _соединяются_ с теми, которые уже определены для дочернего компонента, поэтому если вы хотите добавить некоторые базовые стили, вы можете использовать `className`, не беспокоясь о том, что он будет переопределен.
2. Если компонент перехода монтируется с `in={false}`, то никакие классы еще не применяются. Возможно, вы ожидаете `*-exit-done`, но если подумать, компонент не может завершить выход, если он еще не вошел.
3. Классы `fade-appear-done` и `fade-enter-done` будут _обоими_ применены. Это позволяет вам определить разное поведение для появления и обычного входа, используя селекторы типа `.fade-enter-done:not(.fade-appear-done)`. Например, вы можете применить эпическую анимацию входа, когда элемент впервые появляется в DOM, используя [Animate.css](https://daneden.github.io/animate.css/). В противном случае вы можете просто использовать `fade-enter-done` для определения обоих случаев.

Каждый отдельный `classNames` также может быть указан независимо, например:

```js
classNames={{
 appear: 'my-appear',
 appearActive: 'my-active-appear',
 appearDone: 'my-done-appear',
 enter: 'my-enter',
 enterActive: 'my-active-enter',
 enterDone: 'my-done-enter',
 exit: 'my-exit',
 exitActive: 'my-active-exit',
 exitDone: 'my-done-exit',
}}
```

Если вы хотите установить эти классы с помощью CSS Modules:

```js
import styles from './styles.css';
```

возможно, вы захотите использовать camelCase в вашем CSS-файле, таким образом, вы сможете просто разнести их вместо того, чтобы перечислять их по одному:

```js
classNames={{ ...styles }}
```

- type: `string | { appear?: string, appearActive?: string, appearDone?: string, enter?: string, enterActive?: string, enterDone?: string, exit?: string, exitActive?: string, exitDone?: string, }`
- default: `''`

### onEnter

Обратный вызов `<Transition>`, запускаемый сразу после применения класса `enter` или `appear`.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

- type: `Function(node: HtmlElement, isAppearing: bool)`

### onEntering

Обратный вызов `<Transition>`, запускаемый сразу после применения класса `enter-active` или `appear-active`.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

- type: `Function(node: HtmlElement, isAppearing: bool)`

### onEntered

Обратный вызов `<Transition>`, запускаемый сразу после того, как классы '`enter`' или '`appear`' **удалены** и класс `done` добавлен к узлу DOM.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

- type: `Function(node: HtmlElement, isAppearing: bool)`

### onExit

Обратный вызов `<Transition>`, выполняемый сразу после применения класса `exit`.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается

- type: `Function(node: HtmlElement)`

### onExiting

Обратный вызов `<Transition>`, выполняемый сразу после применения `exit-active`.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается

- type: `Function(node: HtmlElement)`

### onExited

Обратный вызов `<Transition>`, запускаемый сразу после того, как классы `exit` **удалены** и класс `exit-done` добавлен к узлу DOM.

!!!note ""

    Когда передается реквизит `nodeRef`, `node` не передается

- type: `Function(node: HtmlElement)`
