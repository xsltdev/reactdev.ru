# Деятельности

**Деятельность** (_activity_) - это действие, которое происходит с течением времени, и его можно запускать и останавливать. Согласно оригинальной бумаге с диаграммами состояний Харела:

> Деятельности всегда занимают ненулевое количество времени, например звуковой сигнал, отображение или выполнение длительных вычислений.

Например, переключатель, который "подает звуковой сигнал", когда он активен, может быть представлен деятельностью `'beeping'`:

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

В XState деятельности указываются в свойстве `activity` узла состояния. При входе в узел состояния интерпретатор должен **начать** свои деятельности, а при выходе из него он должен **прекратить** свои деятельности.

Чтобы определить, какие деятельности в настоящее время активны, у `State` есть свойство `activities`, которое является отображением имен деятельностей в `true`, если деятельность запущена (активна), и `false`, если она остановлена.

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

В приведенной выше конфигурации автомата `activateCrosswalkLight` запускается при переходе в состояние «`light.red`». Он также выполнит специальное действие `xstate.start`, сообщая [сервису](interpretation.md), что она должна начать деятельность:

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

Переход в том же родительском состоянии _не_ приведет к перезапуску его деятельностей, хотя он может начать новые деятельности:

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

При выходе из состояния его деятельность прекратится:

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

И любая остановленная деятельность будет остановлена ​​только один раз:

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

In the machine options, the "start" and "stop" behavior of the activity can be defined in the `activities` property. This is done by:

- Passing in a function that **starts** the activity (as a side-effect)
- From that function, returning another function that **stops** the activity (also as a side-effect).

For example, here's how a `'beeping'` activity that logs `'BEEP!'` to the console every `context.interval` would be implemented:

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

The activity creator is always given two arguments:

- the current `context`
- the defined `activity`
  - e.g., `{ type: 'beeping' }`

Then you would pass this into the machine options (second argument) under the `activities` property:

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

Using XState's [interpreter](./interpretation.md), every time an action occurs to start an activity, it will call that activity creator to start the activity, and use the returned "stopper" (if it is returned) to stop the activity:

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

## Restarting Activities

When [restoring a persisted state](./states.md#persisting-state), activities that were previously running are _not restarted_ by default. This is to prevent undesirable and/or unexpected behavior. However, activities can be manually started by adding `start(...)` actions to the persisted state before restarting a service:

```js
import { State, actions } from 'xstate';

// ...

const restoredState = State.create(somePersistedStateJSON);

// Select activities to be restarted
Object.keys(restoredState.activities).forEach(
  (activityKey) => {
    if (restoredState.activities[activityKey]) {
      // Filter activities, and then add the start() action to the restored state
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
