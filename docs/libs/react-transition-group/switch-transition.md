# SwitchTransition

Компонент перехода, вдохновленный [vue transition modes](https://vuejs.org/v2/guide/transitions.html#Transition-Modes). Вы можете использовать его, когда хотите управлять рендерингом между переходами состояний. Основываясь на выбранном режиме и дочернем ключе, который является компонентом `Transition` или `CSSTransition`, `SwitchTransition` осуществляет последовательный переход между ними.

Если выбран режим `out-in`, `SwitchTransition` ждет, пока старый ребенок не выйдет, а затем вставляет нового ребенка. Если выбран режим `in-out`, `SwitchTransition` сначала вставляет нового ребенка, ждет, пока новый ребенок войдет, а затем удаляет старого ребенка.

!!!note ""

    Если вы хотите, чтобы анимация происходила одновременно (то есть, чтобы старый ребенок удалялся, а новый вставлялся **в одно и то же время**), вам следует использовать [`TransitionGroup`](transition-group.md).

```jsx
function App() {
  const [state, setState] = useState(false);
  const helloRef = useRef(null);
  const goodbyeRef = useRef(null);
  const nodeRef = state ? goodbyeRef : helloRef;
  return (
    <SwitchTransition>
      <CSSTransition
        key={state ? 'Goodbye, world!' : 'Hello, world!'}
        nodeRef={nodeRef}
        addEndListener={(node, done) =>
          node.addEventListener(
            'transitionend',
            done,
            false
          )
        }
        classNames="fade"
      >
        <button
          ref={nodeRef}
          onClick={() => setState((state) => !state)}
        >
          {state ? 'Goodbye, world!' : 'Hello, world!'}
        </button>
      </CSSTransition>
    </SwitchTransition>
  );
}
```

```css
.fade-enter {
  opacity: 0;
}
.fade-exit {
  opacity: 1;
}
.fade-enter-active {
  opacity: 1;
}
.fade-exit-active {
  opacity: 0;
}
.fade-enter-active,
.fade-exit-active {
  transition: opacity 500ms;
}
```

## Пример

<iframe title="SwitchTransition Component" src="https://codesandbox.io/embed/switchtransition-component-iqm0d?fontsize=14" sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin" style="display: block; width: 100%; height: 500px; border: 0px; border-radius: 4px; overflow: hidden;"></iframe>

## Свойства

### mode

Режимы перехода. `out-in`: Сначала происходит переход от текущего элемента, затем, когда он завершен, происходит переход к новому элементу. `in-out`: Новый элемент сначала переходит внутрь, затем, после завершения, текущий элемент переходит наружу.

- type: `'out-in'|'in-out'`
- default: `'out-in'`

### children

Любой компонент `Transition` или `CSSTransition`.

- type: `element`
