# Transition

Компонент **`Transition`** позволяет вам описать переход от одного состояния компонента к другому во времени с помощью простого декларативного API. Чаще всего он используется для анимации монтажа и демонтажа компонента, но также может быть использован для описания состояний перехода на месте.

!!!note ""

    `Transition` — это базовый компонент, не зависящий от платформы. Если вы используете переходы в CSS, вам, вероятно, лучше использовать [CSSTransition](css-transition.md). Он наследует все возможности `Transition`, но содержит дополнительные возможности, необходимые для хорошей работы с переходами CSS (отсюда и название компонента).

По умолчанию компонент `Transition` не изменяет поведение компонента, который он отображает, он только отслеживает состояния "`enter`" и "`exit`" для компонентов. Вы сами можете придать смысл и эффект этим состояниям. Например, мы можем добавить стили к компоненту, когда он входит или выходит:

```js
import { Transition } from 'react-transition-group';
import { useRef } from 'react';

const duration = 300;

const defaultStyle = {
    transition: `opacity ${duration}ms ease-in-out`,
    opacity: 0,
};

const transitionStyles = {
    entering: { opacity: 1 },
    entered: { opacity: 1 },
    exiting: { opacity: 0 },
    exited: { opacity: 0 },
};

function Fade({ in: inProp }) {
    const nodeRef = useRef(null);
    return (
        <Transition
            nodeRef={nodeRef}
            in={inProp}
            timeout={duration}
        >
            {(state) => (
                <div
                    ref={nodeRef}
                    style={{
                        ...defaultStyle,
                        ...transitionStyles[state],
                    }}
                >
                    I'm a fade Transition!
                </div>
            )}
        </Transition>
    );
}
```

Существует 4 основных состояния, в которых может находиться `Transition`:

-   `entering`
-   `entered`
-   `exiting`
-   `exited`

Состояние `Transition` переключается с помощью параметра `in`. При значении `true` компонент начинает стадию "Enter". Во время этого этапа компонент переходит из текущего состояния перехода в состояние "`entering`" на время перехода, а затем в состояние "`entered`" после его завершения. Рассмотрим следующий пример (мы будем использовать хук [`useState`](https://reactjs.org/docs/hooks-reference.html#usestate)):

```js
import { Transition } from 'react-transition-group';
import { useState, useRef } from 'react';

function App() {
  const [inProp, setInProp] = useState(false);
  const nodeRef = useRef(null);
  return (
    <div>
      <Transition nodeRef={nodeRef} in={inProp} timeout={500}>
        {state => (
          // ...
        )}
      </Transition>
      <button onClick={() => setInProp(true)}>
        Click to Enter
      </button>
    </div>
  );
}
```

При нажатии на кнопку компонент перейдет в состояние '`entering`' и останется там в течение 500 мс (значение таймаута), прежде чем окончательно переключится в состояние '`entered`'.

Когда `in` равно `false`, происходит то же самое, только состояние переходит из состояния '`exiting`' в '`exited`'.

## Свойства

### nodeRef

Ссылка React на элемент DOM, который должен перейти: [https://stackoverflow.com/a/51127130/4671932](https://stackoverflow.com/a/51127130/4671932)

-   Этот параметр необязателен, но рекомендуется, чтобы избежать использования по умолчанию [`ReactDOM.findDOMNode`](https://reactjs.org/docs/react-dom.html#finddomnode), который является устаревшим в `StrictMode`.
-   При использовании свойства `nodeRef`, `node` не передается в функции обратного вызова (например, `onEnter`), поскольку пользователь уже имеет прямой доступ к узлу.
-   При изменении `key` prop `Transition` в `TransitionGroup` необходимо предоставить `Transition` новый `nodeRef` с измененным `key` prop (см. [`test/CSSTransition-test.js`](https://github.com/reactjs/react-transition-group/blob/13435f897b3ab71f6e19d724f145596f5910581c/test/CSSTransition-test.js#L362-L437)).

-   type: `shape`

### children

Вместо элемента React можно использовать дочернюю `function`. Эта функция вызывается с текущим статусом перехода ("`entering`", "`entered`", "`exiting`", "`exited`"), который можно использовать для применения к компоненту пропсов, зависящих от контекста.

```jsx
<Transition
    nodeRef={nodeRef}
    in={this.state.in}
    timeout={150}
>
    {(state) => (
        <MyComponent
            ref={nodeRef}
            className={`fade fade-${state}`}
        />
    )}
</Transition>
```

-   type: `Function | element`
-   required

### in

Показать компонент; вызывает состояния входа или выхода

-   type: `boolean`
-   default: `false`

### mountOnEnter

По умолчанию дочерний компонент монтируется сразу вместе с родительским компонентом `Transition`. Если вы хотите "лениво смонтировать" компонент при первом переходе `in={true}`, вы можете установить `mountOnEnter`. После первого перехода enter компонент останется смонтированным, даже при "выходе", если вы также не укажете `unmountOnExit`.

-   type: `boolean`
-   default: `false`

### unmountOnExit

По умолчанию дочерний компонент остается смонтированным после достижения состояния "`exited`". Установите `unmountOnExit`, если вы предпочитаете размонтировать компонент после завершения его выхода.

-   type: `boolean`
-   default: `false`

### appear

По умолчанию дочерний компонент не выполняет переход enter при первом подключении, независимо от значения `in`. Если вам нужно такое поведение, установите и `appear` и `in` в `true`.

!!!note ""

    Не существует специальных состояний появления, таких как `appearing/appeared`, этот пропс только добавляет дополнительный переход `enter`. Однако в компоненте `<CSSTransition>` этот первый переход `enter` приводит к появлению дополнительных классов `.appear-*`, таким образом, вы можете выбрать другой стиль.

-   type: `boolean`
-   default: `false`

### enter

Включение или отключение переходов ввода.

-   type: `boolean`
-   default: `true`

### exit

Включение или отключение переходов выхода.

-   type: `boolean`
-   default: `true`

### timeout

Продолжительность перехода, в миллисекундах. Требуется, если не указан `addEndListener`.

Вы можете указать единый таймаут для всех переходов:

```
timeout={500}
```

или индивидуально:

```
timeout={{
 appear: 500,
 enter: 300,
 exit: 500,
}}
```

-   `appear` по умолчанию принимает значение `enter`.
-   `enter` по умолчанию равно `0`
-   `exit` по умолчанию равно `0`

-   type: `number | { enter?: number, exit?: number, appear?: number }`

### addEndListener

Добавьте пользовательский триггер завершения перехода. Вызывается с помощью переходящего узла DOM и обратного вызова `done`. Позволяет более детально проработать логику завершения перехода. Таймауты по-прежнему используются в качестве запасного варианта, если они предусмотрены.

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается, поэтому `done` передается в качестве первого аргумента.

```js
addEndListener={(node, done) => {
  // use the css transitionend event to mark the finish of a transition
  node.addEventListener('transitionend', done, false);
}}
```

-   type: `Function`

### onEnter

Обратный вызов, выполняемый перед применением статуса "entering". Дополнительный параметр `isAppearing` используется для указания того, происходит ли стадия входа на начальном монтировании.

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

-   type: `Function(node: HtmlElement, isAppearing: bool) -> void`
-   default: `function noop() {}`

### onEntering

Обратный вызов, выполняемый после применения статуса "entering". Дополнительный параметр `isAppearing` используется для указания того, происходит ли стадия входа на начальном монтировании.

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

-   type: `Function(node: HtmlElement, isAppearing: bool)`
-   default: `function noop() {}`

### onEntered

Обратный вызов, выполняемый после применения статуса "entered". Дополнительный параметр `isAppearing` используется для указания того, происходит ли стадия входа на начальном монтировании.

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается, поэтому `isAppearing` передается в качестве первого аргумента.

-   type: `Function(node: HtmlElement, isAppearing: bool) -> void`
-   default: `function noop() {}`

### onExit

Обратный вызов, выполняемый перед применением статуса "exiting".

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается.

-   type: `Function(node: HtmlElement) -> void`
-   default: `function noop() {}`

### onExiting

Обратный вызов, выполняемый после применения статуса "exiting".

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается.

-   type: `Function(node: HtmlElement) -> void`
-   default: `function noop() {}`

### onExited

Обратный вызов, выполняемый после применения статуса "exited".

!!!note ""

    Когда передается пропс `nodeRef`, `node` не передается

-   type: `Function(node: HtmlElement) -> void`
-   default: `function noop() {}`
