# Переходы

**Переходы** (_Transitions_) определяют, как конечный автомат реагирует на события.

## API

Переходы состояний определяются на узлах состояний в свойстве `on`:

```js hl_lines="11 14-16"
import { createMachine } from 'xstate';

const promiseMachine = createMachine({
  id: 'promise',
  initial: 'pending',
  states: {
    pending: {
      on: {
        // state transition (shorthand)
        // this is equivalent to { target: 'resolved' }
        RESOLVE: 'resolved',

        // state transition (object)
        REJECT: {
          target: 'rejected',
        },
      },
    },
    resolved: {
      type: 'final',
    },
    rejected: {
      type: 'final',
    },
  },
});

const { initialState } = promiseMachine;

console.log(initialState.value);
// => 'pending'

const nextState = promiseMachine.transition(initialState, {
  type: 'RESOLVE',
});

console.log(nextState.value);
// => 'resolved'
```

В приведенном выше примере, когда автомат находится в состоянии `pending` и получает событие `RESOLVE`, он переходит в состояние `resolved`.

Переход между состояниями можно определить как:

- строка, например `RESOLVE: 'resolved'`, что эквивалентно ...
- объект со свойством `target`, например, `RESOLVE: {target: 'resolved'}`,
- массив объектов перехода, которые используются для [условных переходов](guards.md)

## Метод автомата `.transition()`

Метод `machine.transition(...)` - это чистая функция, которая принимает два аргумента:

- `state` - [состояние](states.md), из которого будет осуществлен переход
- `event` - [событие](events.md) вызывающее переход

Метов возвращает новый экземпляр `State`, который является результатом выполнения всех переходов, разрешенных текущим состоянием и событием.

```js hl_lines="8"
const lightMachine = createMachine({
  /* ... */
});

const greenState = lightMachine.initialState;

// determine next state based on current state and event
const yellowState = lightMachine.transition(greenState, {
  type: 'TIMER',
});

console.log(yellowState.value);
// => 'yellow'
```

## Выбор разрешенных переходов

**Разрешенный переход** (_enabled transition_) - это переход, который будет выполняться условно, в зависимости от текущего состояния и события. Он будет принят тогда и только тогда, когда:

- он определяется на [узле состояния](statenodes.md), который соответствует текущему значению состояния
- [защитник перехода](guards.md) (свойство `cond`) вернул `true`
- он не заменяется более специфичным переходом.

В [иерархических автоматах](hierarchical.md) переходы имеют приоритет в зависимости от того, насколько глубоко они находятся в дереве; более глубокие переходы более конкретны и, следовательно, имеют более высокий приоритет. Это работает аналогично тому, как работают события DOM: если вы нажмете кнопку, обработчик события щелчка непосредственно на кнопке будет более конкретным, чем обработчик события щелчка в окне.

```js hl_lines="10 21-22 27"
const wizardMachine = createMachine({
  id: 'wizard',
  initial: 'open',
  states: {
    open: {
      initial: 'step1',
      states: {
        step1: {
          on: {
            NEXT: { target: 'step2' },
          },
        },
        step2: {
          /* ... */
        },
        step3: {
          /* ... */
        },
      },
      on: {
        NEXT: { target: 'goodbye' },
        CLOSE: { target: 'closed' },
      },
    },
    goodbye: {
      on: {
        CLOSE: { target: 'closed' },
      },
    },
    closed: {
      type: 'final',
    },
  },
});

// { open: 'step1' }
const { initialState } = wizardMachine;

// the NEXT transition defined on 'open.step1'
// supersedes the NEXT transition defined
// on the parent 'open' state
const nextStepState = wizardMachine.transition(
  initialState,
  { type: 'NEXT' }
);
console.log(nextStepState.value);
// => { open: 'step2' }

// there is no CLOSE transition on 'open.step1'
// so the event is passed up to the parent
// 'open' state, where it is defined
const closedState = wizardMachine.transition(initialState, {
  type: 'CLOSE',
});
console.log(closedState.value);
// => 'closed'
```

## Дескрипторы событий

**Дескриптор события** (_Event Descriptors_) — это строка, описывающая тип события, которому будет соответствовать переход. Часто это эквивалентно свойству `event.type` объекта `event`, отправленного на конечный автомат:

```js
// ...
{
  on: {
    // "CLICK" is the event descriptor.
    // This transition matches events with { type: 'CLICK' }
    CLICK: 'someState',
    // "SUBMIT" is the event descriptor.
    // This transition matches events with { type: 'SUBMIT' }
    SUBMIT: 'anotherState'
  }
}
// ...
```

Другие дескрипторы событий включают:

- **Дескрипторы нулевых событий** `""` (_Null event descriptors_), которые не соответствуют никаким событиям (т. е. "нулевые" события) и представляют собой переходы, выполненные сразу после входа в состояние.
- **Дескрипторы событий по-умолчанию** `"*"` (_Wildcard event descriptors_) (для версии 4.7+), которые срабатывают, если никакие другие события не подошли.

## Переходы без смены состояния

**Переходы без смены состояния** (_Self Transitions_) - это когда состояние переходит в само себя, из которого оно _может_ выйти, а затем снова войти в себя. Они могут быть внутренними или внешними:

- **Внутренний переход** (_internal transition_) не будет ни выходом, ни повторным входом, но может входить в другие дочерние состояния.
- **Внешний переход** (_external transition_) выйдет и повторно войдет в себя, а также может выйти или войти в дочерние состояния.

По умолчанию все переходы с указанной целью являются внешними.

См. [действия при переходах без смены состояния](./actions.md#actions-on-self-transitions) для детальной информации, как это происходит.

### Внутренние переходы

**Внутренний переход** (_internal transition_) - это переход, который не выходит из своего узла состояния. Внутренние переходы создаются путем указания [относительной цели](./ids.md#relative-targets) (например, `'.left'`) или путем явной установки `{internal: true}` перехода. Например, рассмотрим автомат, который устанавливает абзац текста для выравнивания `'left'`, `'right'`, `'center'` или `'justify'`:

```js hl_lines="14-17"
import { createMachine } from 'xstate';

const wordMachine = createMachine({
  id: 'word',
  initial: 'left',
  states: {
    left: {},
    right: {},
    center: {},
    justify: {},
  },
  on: {
    // внутренние переходы
    LEFT_CLICK: '.left',
    RIGHT_CLICK: { target: '.right' }, // идентично '.right'
    CENTER_CLICK: { target: '.center', internal: true }, // идентично '.center'
    JUSTIFY_CLICK: { target: '.justify', internal: true }, // идентично '.justify'
  },
});
```

Вышеупомянутый автомат запустится в состоянии `left` и в зависимости от того, что будет нажато, внутренне перейдет в другие дочерние состояния. Кроме того, поскольку переходы являются внутренними, вход, выход или какие-либо действия, определенные в родительском узле состояния, заново не выполняются.

Переходы, у которых есть `{target: undefined}` (или нет `target`), также являются внутренними переходами:

```js hl_lines="11-13"
const buttonMachine = createMachine({
  id: 'button',
  initial: 'inactive',
  states: {
    inactive: {
      on: { PUSH: 'active' },
    },
    active: {
      on: {
        // No target - internal transition
        PUSH: {
          actions: 'logPushed',
        },
      },
    },
  },
});
```

**Шпаргалка по внутренним переходам:**

- `EVENT: '.foo'` - внутренний переход к дочернему состоянию
- `EVENT: { target: '.foo' }` - внутренний переход к дочернему состоянию (начинается с `'.'`)
- `EVENT: undefined` - запрещенный переход
- `EVENT: { actions: [ ... ] }` - внутренний переход без смены состояния
- `EVENT: { actions: [ ... ], internal: true }` - внутренний переход без смены состояния, идентичен предыдущему
- `EVENT: { target: undefined, actions: [ ... ] }` - внутренний переход без смены состояния, идентичен предыдущему

### Внешние переходы

**Внешние переходы** (_external transition_) будут выходить и повторно входить в узел состояния, в котором определен переход. В приведенном выше примере для родительского узла состояния `word` (корневого узла состояния) при переходах выполняются действия выхода и входа.

По умолчанию переходы являются внешними, но любой переход можно сделать явно внешним, установив для перехода `{internal: false}`.

```js hl_lines="4-9"
// ...
on: {
  // external transitions
  LEFT_CLICK: 'word.left',
  RIGHT_CLICK: 'word.right',
  CENTER_CLICK: {
	target: '.center', internal: false }, // идентично 'word.center'
  JUSTIFY_CLICK: {
	target: 'word.justify', internal: false } // идентично 'word.justify'
}
// ...
```

Каждый переход, описанный выше, является внешним, и для него будут выполняться действия выхода и входа родительского состояния.

**Шпаргалка по внешним переходам:**

- `EVENT: { target: 'foo' }` - все переходы в соседние узлы состояния - внешние
- `EVENT: { target: '#someTarget' }` - все переходы к другим узлам состояния - внешние
- `EVENT: { target: 'same.foo' }` - внешний переход к собственному дочернему узлу состояния (эквивалентно `{ target: '.foo', internal: false }`)
- `EVENT: { target: '.foo', internal: false }` - внешний переход к дочернему узлу состояния - в противном случае это был бы внутренний переход
- `EVENT: { actions: [ ... ], internal: false }` - внешний переход без смены состояния
- `EVENT: { target: undefined, actions: [ ... ], internal: false }` - внешний переход без смены состояния, аналогичен предыдущему

## Проходные переходы

!!!warning

    Синтаксис пустой строки (`{on: {'': ...}}`) не рекомендуется использовать c версии 5. Следует отдавать предпочтение новому синтаксису `always` c версии 4.11+. См. ниже раздел о [переходах без событий](#eventless-always-transitions), которые аналогичны проходным переходам.

**Проходной переход** (_transient transition_) - это переход, который активируется нулевым событием (null event). Другими словами, это переход, который выполняется немедленно (т. е. без инициирующего события), пока выполняются какие-либо условия:

```js hl_lines="14-17"
const gameMachine = createMachine(
  {
    id: 'game',
    initial: 'playing',
    context: {
      points: 0,
    },
    states: {
      playing: {
        on: {
          // Transient transition
          // Will transition to either 'win' or 'lose' immediately upon
          // (re)entering 'playing' state if the condition is met.
          '': [
            { target: 'win', cond: 'didPlayerWin' },
            { target: 'lose', cond: 'didPlayerLose' },
          ],
          // Self-transition
          AWARD_POINTS: {
            actions: assign({
              points: 100,
            }),
          },
        },
      },
      win: { type: 'final' },
      lose: { type: 'final' },
    },
  },
  {
    guards: {
      didPlayerWin: (context, event) => {
        // check if player won
        return context.points > 99;
      },
      didPlayerLose: (context, event) => {
        // check if player lost
        return context.points < 0;
      },
    },
  }
);

const gameService = interpret(gameMachine)
  .onTransition((state) => console.log(state.value))
  .start();

// Still in 'playing' state because no conditions of
// transient transition were met
// => 'playing'

// When 'AWARD_POINTS' is sent, a self-transition to 'PLAYING' occurs.
// The transient transition to 'win' is taken because the 'didPlayerWin'
// condition is satisfied.
gameService.send('AWARD_POINTS');
// => 'win'
```

Как и переходы, проходные переходы могут быть указаны как один переход (например, `'': 'someTarget'`) или как массив условных переходов. Если никакие условные переходы при проходном переходе не выполняются, автомат остается в том же состоянии.

Нулевые события всегда «отправляются» для каждого перехода, внутреннего или внешнего.

## Безсобытийные "Always" переходы

_Начиная с версии 4.11+_

**Бессобытийный переход** (_Eventless transition_) - это переход, который всегда выполняется, когда автомат находится в состоянии, в котором он определен, и когда его `cond` защитной функцией оценивается как `true`. Они проверяются:

- сразу при входе в узел состояния
- каждый раз, когда машина получает действующее событие (независимо от того, запускает ли событие внутренний или внешний переход)

Бессобытийные переходы определены в свойстве `always` узла состояния:

```js hl_lines="14-17"
const gameMachine = createMachine(
  {
    id: 'game',
    initial: 'playing',
    context: {
      points: 0,
    },
    states: {
      playing: {
        // Eventless transition
        // Will transition to either 'win' or 'lose' immediately upon
        // entering 'playing' state or receiving AWARD_POINTS event
        // if the condition is met.
        always: [
          { target: 'win', cond: 'didPlayerWin' },
          { target: 'lose', cond: 'didPlayerLose' },
        ],
        on: {
          // Self-transition
          AWARD_POINTS: {
            actions: assign({
              points: 100,
            }),
          },
        },
      },
      win: { type: 'final' },
      lose: { type: 'final' },
    },
  },
  {
    guards: {
      didPlayerWin: (context, event) => {
        // check if player won
        return context.points > 99;
      },
      didPlayerLose: (context, event) => {
        // check if player lost
        return context.points < 0;
      },
    },
  }
);

const gameService = interpret(gameMachine)
  .onTransition((state) => console.log(state.value))
  .start();

// Still in 'playing' state because no conditions of
// transient transition were met
// => 'playing'

// When 'AWARD_POINTS' is sent, a self-transition to 'PLAYING' occurs.
// The transient transition to 'win' is taken because the 'didPlayerWin'
// condition is satisfied.
gameService.send({ type: 'AWARD_POINTS' });
// => 'win'
```

### Бессобытийные переходы против переходов по-умолчанию

- [Переходы по-умолчанию](#wildcard-descriptors) (Wildcard transitions) не проверяются при входе в узлы состояния, а бессобытийные переходы - проверяются. Защитные функции для переходов без событий выполняются перед тем, как делать что-либо еще (даже до выполнения защитных функций входных действий).
- Повторная оценка бессобытийных переходов запускается любым действующим событием. Повторная оценка переходов по-умолчанию запускается только событием, не совпадающим с явными дескрипторами событий.

!!!warning "Внимание"

    При неправильном использовании бессобытийных переходов можно создавать бесконечные циклы.

    Бессобытийные переходы следует определять с помощью `target`, `cond` + `target`, `cond` + `actions` или `cond` + `target` + `actions`. Цель, если она объявлена, должна отличаться от узла текущего состояния. Бессобытийные переходы без `target` или `cond` вызовут бесконечный цикл. Переходы с `cond` и `actions` могут превратиться в бесконечный цикл, если его защитная функция `cond` продолжает возвращать `true`.

!!!tip "Подсказка"

    Когда проверяются бессобытийные переходы, их защитные функции повторно запускаются до тех пор, пока все они не вернут `false`, или переход с `target` не будет подтвержден. Каждый раз, когда какая-либо защитная функция возвращает `true` во время этого процесса, связанные с ним действия будут выполнены один раз. Таким образом, возможно, что во время одной микрозадачи некоторые переходы без целей выполняются несколько раз.

    Это контрастирует с обычными переходами, где всегда можно сделать максимум один переход.

## Запрещенные переходы

В XState **«запрещенный» переход** (_"forbidden" transition_) - это переход, который указывает, что переход состояния не должен происходить с указанным событием. То есть при запрещенном переходе ничего не должно происходить, и событие не должно обрабатываться узлами родительского состояния.

Запрещенный переход задается путем явного указания `target` как `undefined`. Это то же самое, что указать его как внутренний переход без действий:

```js hl_lines="3"
on: {
  // запрещенный переход
  LOG: undefined,
  // идентично
  LOG: {
    actions: []
  }
}
```

Например, мы можем смоделировать, что телеметрия может регистрироваться для всех событий, кроме случаев, когда пользователь вводит личную информацию:

```js hl_lines="15"
const formMachine = createMachine({
  id: 'form',
  initial: 'firstPage',
  states: {
    firstPage: {
      /* ... */
    },
    secondPage: {
      /* ... */
    },
    userInfoPage: {
      on: {
        // явно запретить событию LOG что-либо делать
        // или любые переходы в любое другое состояние
        LOG: undefined,
      },
    },
  },
  on: {
    LOG: {
      actions: 'logTelemetry',
    },
  },
});
```

!!!tip "Подсказка"

    Обратите внимание, что при определении нескольких переходов с одним и тем же именем события в иерархической цепочке «предок-потомок» будет использоваться только самый внутренний переход. В приведенном выше примере именно поэтому действие `logTelemetry`, определенное в родительском событии `LOG`, не будет выполняться, как только компьютер достигнет состояния `userInfoPage`.

## Несколько целей

Переход, основанный на одном событии, может иметь несколько целевых узлов состояния. Это необычно и допустимо только в том случае, если узлы состояния легальны; например, переход к двум узлам состояния одного и того же уровня в узле составного состояния является недопустимым, поскольку (непараллельный) конечный автомат может находиться только в одном состоянии в любой момент времени.

Несколько целей указываются в виде массива в `target: [...]`, где каждая цель в массиве является относительным ключом или идентификатором узла состояния, как и отдельные цели.

```js hl_lines="24"
const settingsMachine = createMachine({
  id: 'settings',
  type: 'parallel',
  states: {
    mode: {
      initial: 'active',
      states: {
        inactive: {},
        pending: {},
        active: {},
      },
    },
    status: {
      initial: 'enabled',
      states: {
        disabled: {},
        enabled: {},
      },
    },
  },
  on: {
    // Multiple targets
    DEACTIVATE: {
      target: ['.mode.inactive', '.status.disabled'],
    },
  },
});
```

## События по-умолчанию

Начиная с версии 4.7+

Переход, указанный с помощью дескриптора **события по-умолчанию** «`*`» (_wildcard event descriptor_), активируется любым событием. Это означает, что любое событие будет соответствовать переходу, который имеет: `{"*": ...}`, и если защитные функции вернут `true`, этот переход будет выполнен.

Явные дескрипторы событий всегда будут выбираться вместо дескрипторов событий по-умолчанию, если переходы не определены в массиве. В этом случае порядок переходов в массиве и определяет, какой из них будет выбран.

```js hl_lines="4 9"
// Для события SOME_EVENT будет выбран переход "here"
on: {
  "*": "elsewhere",
  "SOME_EVENT": "here"
}

// Для события SOME_EVENT будет выбран переход по-умолчанию "elsewhere"
on: [
  { event: "*", target: "elsewhere" },
  { event: "SOME_EVENT", target: "here" },
]
```

!!!tip "Подсказка"

    Дескрипторы по-умолчанию (Wildcard descriptors) не ведут себя так же, как проходные переходы (transient transitions) (с нулевыми (null) дескрипторами событий). В то время как проходные переходы будут выполняться немедленно, когда состояние активно, переходы по-умолчанию (wildcard transitions) по-прежнему нуждаются в каком-либо событии, которое должно быть отправлено в его состояние для запуска.

**Пример:**

```js hl_lines="7 8"
const quietMachine = createMachine({
  id: 'quiet',
  initial: 'idle',
  states: {
    idle: {
      on: {
        WHISPER: undefined,
        // On any event besides a WHISPER, transition to the 'disturbed' state
        '*': 'disturbed',
      },
    },
    disturbed: {},
  },
});

quietMachine.transition(quietMachine.initialState, {
  type: 'WHISPER',
});
// => State { value: 'idle' }

quietMachine.transition(quietMachine.initialState, {
  type: 'SOME_EVENT',
});
// => State { value: 'disturbed' }
```

## Вопросы и ответы

### Как мне выполнить логику if / else при переходах?

Иногда вам захочется сказать:

- Если что-то `true`, перейти в это состояние
- Если что-то еще `true`, перейдите в это состояние
- Иначе перейти в это состояние

Для этого можно использовать [защищенные переходы](guards.md#guarded-transitions).

### Как мне перейти в _любое_ состояние?

Вы можете перейти в _любое_ состояние, присвоив этому состоянию собственный идентификатор и используя `target: '#customId'`. Вы можете прочитать полную документацию по [пользовательским идентификаторам](ids.md#custom-ids) здесь.

Это позволяет вам переходить от дочерних состояний к одноуровневым родительским состояниям, например, в событиях `CANCEL` и `done` в этом примере:

<iframe src="https://stately.ai/viz/embed/835aee58-1c36-41d3-bb02-b56ceb06072e?mode=viz&panel=code&readOnly=1&showOriginalLink=1&controls=0&pan=0&zoom=0"
allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"
sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts" width="100%" height="360"
></iframe>
