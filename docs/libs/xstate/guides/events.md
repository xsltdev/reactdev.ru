# События

**Событие** - это то, что заставляет конечный автомат [переходить](./transitions.md) из текущего [состояния](./states.md) в следующее состояние.

## API

Событие - это объект со свойством `type`, указывающим, к какому типу оно относится:

```js
const timerEvent = {
  type: 'TIMER', // the convention is to use CONST_CASE for event names
};
```

В XState события, которые имеют только `type`, могут быть представлены только их строковым типом, как сокращение:

```js
// equivalent to { type: 'TIMER' }
const timerEvent = 'TIMER';
```

Объекты событий также могут иметь другие свойства, которые представляют данные, связанные с событием:

```js
const keyDownEvent = {
  type: 'keydown',
  key: 'Enter',
};
```

## Отправка событий

Переход определяет, каким будет следующее состояние, учитывая текущее состояние и событие, определенные в его свойстве `on: {...}`. Это можно увидеть, передав событие в [метод перехода](./transitions.md#machine-transition-method):

```js
import { createMachine } from 'xstate';

const lightMachine = createMachine({
  /* ... */
});

const { initialState } = lightMachine;

let nextState = lightMachine.transition(
  initialState,
  'TIMER'
); // string event
console.log(nextState.value);
// => 'yellow'

nextState = lightMachine.transition(nextState, {
  type: 'TIMER',
}); // event object
console.log(nextState.value);
// => 'red'
```

Многие нативные события, такие как события DOM, совместимы и могут использоваться напрямую с XState, указав тип события в свойстве `type`:

```js
import { createMachine, interpret } from 'xstate';

const mouseMachine = createMachine({
  on: {
    mousemove: {
      actions: [
        (context, event) => {
          const { offsetX, offsetY } = event;
          console.log({ offsetX, offsetY });
        },
      ],
    },
  },
});
const mouseService = interpret(mouseMachine).start();

window.addEventListener('mousemove', (event) => {
  // event can be sent directly to service
  mouseService.send(event);
});
```

## Безусловные события

!!!warning "Внимание"

    Синтаксис безусловного события `({on: {'': ...}})` будет устаревшим в версии 5. Вместо него следует использовать новый синтаксис [`always`](./transitions.md#eventless-always-transitions).

Безусловное событие - это событие, которое не имеет типа и происходит сразу после входа в состояние. В переходах оно представлено пустой строкой (`''`):

```js
// contrived example
const skipMachine = createMachine({
  id: 'skip',
  initial: 'one',
  states: {
    one: {
      on: { CLICK: 'two' },
    },
    two: {
      // null event '' always occurs once state is entered
      // immediately take the transition to 'three'
      on: { '': 'three' },
    },
    three: {
      type: 'final',
    },
  },
});

const { initialState } = skipMachine;
const nextState = skipMachine.transition(
  initialState,
  'CLICK'
);

console.log(nextState.value);
// => 'three'
```

---

<iframe src="https://stately.ai/viz/embed?gist=f8b1c6470371b13eb2838b84194ca428" width="100%" height="280"></iframe>

Существует много вариантов использования безусловных событий, особенно при определении [переходов](./transitions.md#transient-transitions), когда (потенциально [переходное](./statenodes.md#transient-state-nodes)) состояние сразу определяет, какое следующее состояние должно быть основано на [условиях](./guards.md):

```js
const isAdult = ({ age }) => age >= 18;
const isMinor = ({ age }) => age < 18;

const ageMachine = createMachine({
  id: 'age',
  context: { age: undefined }, // age unknown
  initial: 'unknown',
  states: {
    unknown: {
      on: {
        // immediately take transition that satisfies conditional guard.
        // otherwise, no transition occurs
        '': [
          { target: 'adult', cond: isAdult },
          { target: 'child', cond: isMinor },
        ],
      },
    },
    adult: { type: 'final' },
    child: { type: 'final' },
  },
});

console.log(ageMachine.initialState.value);
// => 'unknown'

const personData = { age: 28 };

const personMachine = ageMachine.withContext(personData);

console.log(personMachine.initialState.value);
// => 'adult'
```

---

<iframe src="https://stately.ai/viz/embed?gist=2f9f2f4bd5dcd5ff262c7f2a7e9199aa" width="100%" height="280"></iframe>
