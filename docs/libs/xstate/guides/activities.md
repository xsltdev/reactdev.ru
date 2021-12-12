# Активности

**Активность** (_activity_) - это действие, которое происходит с течением времени, и его можно запускать и останавливать. Согласно оригинальной бумаге с диаграммами состояний Харела:

> Активности всегда занимают ненулевое количество времени, например звуковой сигнал, отображение или выполнение длительных вычислений.

Например, переключатель, который "подает звуковой сигнал", когда он активен, может быть представлен активностью `'beeping'`:

```js
const toggleMachine = createMachine(
  {
    id: 'toggle',
    initial: 'inactive',
    states: {
      inactive: {
        on: {
          TOGGLE: { target: 'active' },
        },
      },
      active: {
        // The 'beeping' activity will take place as long as
        // the machine is in the 'active' state
        activities: ['beeping'],
        on: {
          TOGGLE: { target: 'inactive' },
        },
      },
    },
  },
  {
    activities: {
      beeping: () => {
        // Start the beeping activity
        const interval = setInterval(
          () => console.log('BEEP!'),
          1000
        );

        // Return a function that stops the beeping activity
        return () => clearInterval(interval);
      },
    },
  }
);
```

В XState активности указываются в свойстве `activity` узла состояния. При входе в узел состояния интерпретатор должен **начать** свои активности, а при выходе из него он должен **прекратить** свои активности.

Чтобы определить, какие активности в настоящее время работают, у `State` есть свойство `activities`, которое является отображением имен активностей в `true`, если активность запущена (активна), и `false`, если она остановлена.

```js
const lightMachine = createMachine({
  key: 'light',
  initial: 'green',
  states: {
    green: {
      on: {
        TIMER: { target: 'yellow' },
      },
    },
    yellow: {
      on: {
        TIMER: { target: 'red' },
      },
    },
    red: {
      initial: 'walk',
      // the 'activateCrosswalkLight' activity is started upon entering
      // the 'light.red' state, and stopped upon exiting it.
      activities: ['activateCrosswalkLight'],
      on: {
        TIMER: { target: 'green' },
      },
      states: {
        walk: {
          on: {
            PED_WAIT: { target: 'wait' },
          },
        },
        wait: {
          // the 'blinkCrosswalkLight' activity is started upon entering
          // the 'light.red.wait' state, and stopped upon exiting it
          // or its parent state.
          activities: ['blinkCrosswalkLight'],
          on: {
            PED_STOP: { target: 'stop' },
          },
        },
        stop: {},
      },
    },
  },
});
```

В приведенной выше конфигурации автомата `activateCrosswalkLight` запускается при переходе в состояние «`light.red`». Он также выполнит специальное действие `xstate.start`, сообщая [службе](interpretation.md), что она должна начать активность:

```js
const redState = lightMachine.transition('yellow', {
  type: 'TIMER',
});

redState.activities;
// => {
//   activateCrosswalkLight: true
// }

redState.actions;
// The 'activateCrosswalkLight' activity is started
// => [
//   { type: 'xstate.start', activity: 'activateCrosswalkLight' }
// ]
```

Переход в том же родительском состоянии _не_ приведет к перезапуску его активностей, хотя он может запустить новые активности:

```js
const redWaitState = lightMachine.transition(redState, {
  type: 'PED_WAIT',
});

redWaitState.activities;
// => {
//   activateCrosswalkLight: true,
//   blinkCrosswalkLight: true
// }

redWaitState.actions;
// The 'blinkCrosswalkLight' activity is started
// Note: the 'activateCrosswalkLight' activity is not restarted
// => [
//   { type: 'xstate.start', activity: 'blinkCrosswalkLight' }
// ]
```

При выходе из состояния его активность прекратится:

```js
const redStopState = lightMachine.transition(redWaitState, {
  type: 'PED_STOP',
});

redStopState.activities;
// The 'blinkCrosswalkLight' activity is stopped
// => {
//   activateCrosswalkLight: true,
//   blinkCrosswalkLight: false
// }

redStopState.actions;
// The 'blinkCrosswalkLight' activity is stopped
// => [
//   { type: 'xstate.stop', activity: 'blinkCrosswalkLight' }
// ]
```

И любая остановленная активность будет остановлена только один раз:

```js
const greenState = lightMachine.transition(redStopState, {
  type: 'TIMER',
});

green.activities;
// No active activities
// => {
//   activateCrosswalkLight: false,
//   blinkCrosswalkLight: false
// }

green.actions;
// The 'activateCrosswalkLight' activity is stopped
// Note: the 'blinkCrosswalkLight' activity is not stopped again
// => [
//   { type: 'xstate.stop', activity: 'activateCrosswalkLight' }
// ]
```

## Интерпретация

В параметрах автомата поведение `start` и `stop` активности, может быть определено в свойстве `activities`. Это делают:

- Передача функции, запускающей активность (как побочный эффект)
- Из этой функции возвращается другая функция, которая останавливает активность (также как побочный эффект).

Например, вот как "пищит" активность, которая пишет "`BEEP!`" в консоль каждые `context.interval` миллисекунд:

```js
function createBeepingActivity(context, activity) {
  // Start the beeping activity
  const interval = setInterval(() => {
    console.log('BEEP!');
  }, context.interval);

  // Return a function that stops the beeping activity
  return () => clearInterval(interval);
}
```

Создателю активности всегда передается два аргумента:

- текущий контекст `context`
- определенная активность `activity`, например `{ type: 'beeping' }`

Затем вы должны передать их в параметры автомата (второй аргумент) в свойстве `activities`:

```js
const toggleMachine = createMachine(
  {
    id: 'toggle',
    initial: 'inactive',
    context: {
      interval: 1000, // beep every second
    },
    states: {
      inactive: {
        on: {
          TOGGLE: { target: 'active' },
        },
      },
      active: {
        activities: ['beeping'],
        on: {
          TOGGLE: { target: 'inactive' },
        },
      },
    },
  },
  {
    activities: {
      beeping: createBeepingActivity,
    },
  }
);
```

Используя [интерпретатор](interpretation.md) XState, каждый раз, когда происходит действие для запуска активности, он вызывает этого создателя активности, чтобы запустить действие, и возвращает функцию-стопор (если она возвращается), чтобы остановить активность:

```js
import { interpret } from 'xstate';

// ... (previous code)

const service = interpret(toggleMachine);

service.start();

// nothing logged yet

service.send({ type: 'TOGGLE' });

// => 'BEEP!'
// => 'BEEP!'
// => 'BEEP!'
// ...

service.send({ type: 'TOGGLE' });

// no more beeps!
```

## Перезапуск активностей

При [восстановлении постоянного состояния](states.md#persisting-state) ранее запущенные активности _не перезапускаются_ по умолчанию. Это сделано для предотвращения нежелательного или неожиданного поведения. Однако активности можно запустить вручную, добавив действия `start(...)` в постоянное состояние перед перезапуском службы:

```js
import { State, actions } from 'xstate';

// ...

const restoredState = State.create(somePersistedStateJSON);

// Select activities to be restarted
Object.keys(restoredState.activities).forEach(
  (activityKey) => {
    if (restoredState.activities[activityKey]) {
      // Filter activities,
      // and then add the start() action to the restored state
      restoredState.actions.push(
        actions.start(activityKey)
      );
    }
  }
);

// This will start someService
// with the activities restarted.
someService.start(restoredState);
```
