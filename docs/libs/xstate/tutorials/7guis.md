# Task 1: Counter

This is the first of [The 7 Tasks from 7GUIs](https://eugenkiss.github.io/7guis/tasks#counter):

> _Challenge:_ Understanding the basic ideas of a language/toolkit.
>
> The task is to build a frame containing a label or read-only textfield T and a button B. Initially, the value in T is “0” and each click of B increases the value in T by one.
>
> Counter serves as a gentle introduction to the basics of the language, paradigm and toolkit for one of the simplest GUI applications imaginable. Thus, Counter reveals the required scaffolding and how the very basic features work together to build a GUI application. A good solution will have almost no scaffolding.

## Modeling

In this simple UI, there is only one finite state, which can be named `"active"`. The context, however, will contain the `count`, which represents the current count with an initial value of `0` and can be infinite. An `"INCREMENT"` event will trigger an update to the context which assigns a new value to `count` based on the current `context.count` value.

**States:**

- `"active"` - the state where counting is enabled

**Context:**

- `count` - the current count value

**Events:**

- `"INCREMENT"` - signals that the count should be increased by one

## Coding

```js
import { createMachine, assign } from 'xstate';

export const counterMachine = createMachine({
  initial: 'active',
  context: { count: 0 },
  states: {
    active: {
      on: {
        INCREMENT: {
          actions: assign({
            count: (ctx) => ctx.count + 1,
          }),
        },
      },
    },
  },
});
```

## Result

<iframe
  src="https://codesandbox.io/embed/7guis-counter-19d6v?fontsize=14&hidenavigation=1&theme=dark"
  style="width:100%; height:500px; border:0; border-radius: 4px; overflow:hidden;"
  title="7GUIs: Counter"
  allow="geolocation; microphone; camera; midi; vr; accelerometer; gyroscope; payment; ambient-light-sensor; encrypted-media; usb"
  sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"
></iframe>

# Task 2: Temperature

This is the second of [The 7 Tasks from 7GUIs](https://eugenkiss.github.io/7guis/tasks#temp):

> Challenges: bidirectional data flow, user-provided text input.
>
> The task is to build a frame containing two textfields TC and TF representing the temperature in Celsius and Fahrenheit, respectively. Initially, both TC and TF are empty. When the user enters a numerical value into TC the corresponding value in TF is automatically updated and vice versa. When the user enters a non-numerical string into TC the value in TF is not updated and vice versa. The formula for converting a temperature C in Celsius into a temperature F in Fahrenheit is C = (F - 32) \* (5/9) and the dual direction is F = C \* (9/5) + 32.
>
> Temperature Converter increases the complexity of Counter by having bidirectional data flow between the Celsius and Fahrenheit inputs and the need to check the user input for validity. A good solution will make the bidirectional dependency very clear with minimal boilerplate code.
>
> Temperature Converter is inspired by the Celsius/Fahrenheit converter from the book Programming in Scala. It is such a widespread example—sometimes also in the form of a currency converter—that one could give a thousand references. The same is true for the Counter task.

## Modeling

Instead of thinking about this as bidirectional data flow, it can be simpler to think of this as a UI rendered from two values: `C` and `F`, and these two values can be updated due to events, such as `CELSIUS` for changing the C˚ input value and `FAHRENHEIT` for changing the F˚ input value. It just so happens that the `<input>` element both displays and updates the values, but that's just an implementation detail.

Note that when one of these events is sent to the machine, two things happen simultaneously:

- The desired temperature value is assigned to the _event value_
- The other temperature value is calculated and assigned based on that same _event value_

**States:**

- `"active"` - the state where converting the temperature is enabled

**Context:**

- `C` - the temperature in degrees Celsius
- `F` - the temperature in degrees Fahrenheit

**Events:**

- `"CELSIUS"` - signals that the Celsius value should change
- `"FAHRENHEIT"` - signals that the Fahrenheit value should change

## Coding

```js
import { createMachine, assign } from 'xstate';

export const temperatureMachine = createMachine({
  initial: 'active',
  context: { C: undefined, F: undefined },
  states: {
    active: {
      on: {
        CELSIUS: {
          actions: assign({
            C: (_, event) => event.value,
            F: (_, event) =>
              event.value.length
                ? +event.value * (9 / 5) + 32
                : '',
          }),
        },
        FAHRENHEIT: {
          actions: assign({
            C: (_, event) =>
              event.value.length
                ? (+event.value - 32) * (5 / 9)
                : '',
            F: (_, event) => event.value,
          }),
        },
      },
    },
  },
});
```

## Result

<iframe
  src="https://codesandbox.io/embed/7guis-counter-68083?fontsize=14&hidenavigation=1&theme=dark"
  style="width:100%; height:500px; border:0; border-radius: 4px; overflow:hidden;"
  title="7GUIs: Temperature"
  allow="geolocation; microphone; camera; midi; vr; accelerometer; gyroscope; payment; ambient-light-sensor; encrypted-media; usb"
  sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"
></iframe>

# Task 3: Flight Booker

This is the third of [The 7 Tasks from 7GUIs](https://eugenkiss.github.io/7guis/tasks#flight):

> Challenges: constraints.
>
> The task is to build a frame containing a combobox C with the two options “one-way flight” and “return flight”, two textfields T1 and T2 representing the start and return date, respectively, and a button B for submitting the selected flight. T2 is enabled iff C’s value is “return flight”. When C has the value “return flight” and T2’s date is strictly before T1’s then B is disabled. When a non-disabled textfield T has an ill-formatted date then T is colored red and B is disabled. When clicking B a message is displayed informing the user of his selection (e.g. “You have booked a one-way flight on 04.04.2014.”). Initially, C has the value “one-way flight” and T1 as well as T2 have the same (arbitrary) date (it is implied that T2 is disabled).
>
> The focus of Flight Booker lies on modelling constraints between widgets on the one hand and modelling constraints within a widget on the other hand. Such constraints are very common in everyday interactions with GUI applications. A good solution for Flight Booker will make the constraints clear, succinct and explicit in the source code and not hidden behind a lot of scaffolding.
>
> Flight Booker is directly inspired by the Flight Booking Java example in Sodium with the simplification of using textfields for date input instead of specialized date picking widgets as the focus of Flight Booker is not on specialized/custom widgets.

## Modeling

Overall, there's two possible states this form can be in: `editing` or `submitted`. We can model updating the `startDate`, `returnDate`, and `trip` fields by using events, with the constraint that these fields can only be edited when in the `editing` state. Additionally, the `returnDate` can only be edited when `trip` is `"roundTrip"`, and we can enforce that constraint by using a guard.

A `SET_TRIP` event controls the `trip` field, and can only be assigned in the `editing` state (try editing it in `submitted` - even if it's not disabled, it will not change). We can add the additional constraint that it must either be `"oneWay"` or `"roundTrip"`.

To transition from `editing` to `submitted`, a `SUBMIT` event needs to be sent. Validation occurs in this transition by using a guard to ensure that there is a `startDate` if the `trip` is `"oneWay"`, or that there is a `startDate` and `returnDate` if the `trip` is `"roundTrip"`.

::: tip TIP: Context vs. State
Notice that we decided not to model the machine with nested states for the `trip`, such as `editing.oneWay` or `editing.roundTrip`. The reason is simply that even though this is technically a finite state (and you are free to model it this way), it is also a contextual value that we need to read from in order to display the value in the `trip` select input: `context.trip`.

However, you _can_ model this using nested states, and it's a good exercise to try it on your own; it might even simplify some of the guard logic in the `SUBMIT` transition. Try it out:

```js
// ...
initial: 'oneWay',
states: {
  oneWay: {
    entry: assign({ trip: 'oneWay' }),
    // ...
  },
  roundTrip: {
    entry: assign({ trip: 'roundTrip' }),
    // ...
  }
},
// ...
```

:::

**States:**

- `"editing"` - the state where the flight booking information is being edited
- `"submitted"` - the state where the flight booking information has been submitted successfully, and no further changes can be made

**Context:**

```ts
interface FlightContext {
  startDate?: string;
  returnDate?: string;
  trip: 'oneWay' | 'roundTrip';
}
```

**Events:**

```ts
type FlightEvent =
  | {
      type: 'SET_TRIP';
      value: 'oneWay' | 'roundTrip';
    }
  | {
      type: 'startDate.UPDATE';
      value: string;
    }
  | {
      type: 'returnDate.UPDATE';
      value: string;
    }
  | { type: 'SUBMIT' };
```

## Coding

```js
import { createMachine, assign } from 'xstate';

export const flightMachine = createMachine({
  id: 'flight',
  initial: 'editing',
  context: {
    startDate: undefined,
    returnDate: undefined,
    trip: 'oneWay', // or 'roundTrip'
  },
  states: {
    editing: {
      on: {
        'startDate.UPDATE': {
          actions: assign({
            startDate: (_, event) => event.value,
          }),
        },
        'returnDate.UPDATE': {
          actions: assign({
            returnDate: (_, event) => event.value,
          }),
          cond: (context) => context.trip === 'roundTrip',
        },
        SET_TRIP: {
          actions: assign({
            trip: (_, event) => event.value,
          }),
          cond: (_, event) =>
            event.value === 'oneWay' ||
            event.value === 'roundTrip',
        },
        SUBMIT: {
          target: 'submitted',
          cond: (context) => {
            if (context.trip === 'oneWay') {
              return !!context.startDate;
            } else {
              return (
                !!context.startDate &&
                !!context.returnDate &&
                context.returnDate > context.startDate
              );
            }
          },
        },
      },
    },
    submitted: {
      type: 'final',
    },
  },
});
```

## Result

<iframe
  src="https://codesandbox.io/embed/7guis-flight-ulux2?fontsize=14&hidenavigation=1&theme=dark"
  style="width:100%; height:500px; border:0; border-radius: 4px; overflow:hidden;"
  title="7GUIs: Flight"
  allow="geolocation; microphone; camera; midi; vr; accelerometer; gyroscope; payment; ambient-light-sensor; encrypted-media; usb"
  sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"
></iframe>

# Task 4: Timer

This is the fourth of [The 7 Tasks from 7GUIs](https://eugenkiss.github.io/7guis/tasks#timer):

> Challenges: concurrency, competing user/signal interactions, responsiveness.
>
> The task is to build a frame containing a gauge G for the elapsed time e, a label which shows the elapsed time as a numerical value, a slider S by which the duration d of the timer can be adjusted while the timer is running and a reset button R. Adjusting S must immediately reflect on d and not only when S is released. It follows that while moving S the filled amount of G will (usually) change immediately. When e ≥ d is true then the timer stops (and G will be full). If, thereafter, d is increased such that d > e will be true then the timer restarts to tick until e ≥ d is true again. Clicking R will reset e to zero.
>
> Timer deals with concurrency in the sense that a timer process that updates the elapsed time runs concurrently to the user’s interactions with the GUI application. This also means that the solution to competing user and signal interactions is tested. The fact that slider adjustments must be reflected immediately moreover tests the responsiveness of the solution. A good solution will make it clear that the signal is a timer tick and, as always, has not much scaffolding.
>
> Timer is directly inspired by the timer example in the paper [Crossing State Lines: Adapting Object-Oriented Frameworks to Functional Reactive Languages](http://cs.brown.edu/~sk/Publications/Papers/Published/ick-adapt-oo-fwk-frp/paper.pdf).

## Modeling

The key point in modeling this timer is in the description itself:

> A good solution will make it clear that **the signal is a timer tick**

Indeed, we can model timer ticks as a signal (event) that updates the context of some parent timer machine. The timer can be in either the `paused` state or the `running` state, and these timer ticks should ideally only be active when the machine is in the `running` state. This gives us a good basis for how we can model the other requirements:

- When in the `running` state, some `elapsed` variable is incremented by some `interval` on every `TICK` event.
- Always check that `elapsed` does not exceed `duration` (guarded transition) in the `running` state (transient transition)
  - If `elapsed` exceeds `duration`, transition to the `paused` state.
- Always check that `duration` does not exceed `elapsed` (guarded transition) in the `paused` state.
  - If `duration` exceeds `elapsed`, transition to the `running` state.
- The `duration` can always be updated via some `DURATION.UPDATE` event.
- A `RESET` event resets `elapsed` to `0`.

In the `running` state, we can invoke a service that calls `setInterval(...)` to send a `TICK` event on the desired `interval`.

By modeling everything as a "signal" (event), such as `DURATION.UPDATE`, `TICK`, `RESET`, etc., the interface is fully reactive and concurrent. It also simplifies the implementation.

**States:**

- `"running"` - the state where the timer is running, receiving `TICK` events from some invoked interval service, and updating `context.elapsed`.
- `"paused"` - the state where the timer is not running and no longer receiving `TICK` events.

**Context:**

```ts
interface TimerContext {
  // The elapsed time (in seconds)
  elapsed: number;
  // The maximum time (in seconds)
  duration: number;
  // The interval to send TICK events (in seconds)
  interval: number;
}
```

**Events:**

```ts
type TimerEvent =
  | {
      // The TICK event sent by the spawned interval service
      type: 'TICK';
    }
  | {
      // User intent to update the duration
      type: 'DURATION.UPDATE';
      value: number;
    }
  | {
      // User intent to reset the elapsed time to 0
      type: 'RESET';
    };
```

## Coding

```js
export const timerMachine = createMachine({
  initial: 'running',
  context: {
    elapsed: 0,
    duration: 5,
    interval: 0.1,
  },
  states: {
    running: {
      invoke: {
        src: (context) => (cb) => {
          const interval = setInterval(() => {
            cb('TICK');
          }, 1000 * context.interval);

          return () => {
            clearInterval(interval);
          };
        },
      },
      on: {
        '': {
          target: 'paused',
          cond: (context) => {
            return context.elapsed >= context.duration;
          },
        },
        TICK: {
          actions: assign({
            elapsed: (context) =>
              +(context.elapsed + context.interval).toFixed(
                2
              ),
          }),
        },
      },
    },
    paused: {
      on: {
        '': {
          target: 'running',
          cond: (context) =>
            context.elapsed < context.duration,
        },
      },
    },
  },
  on: {
    'DURATION.UPDATE': {
      actions: assign({
        duration: (_, event) => event.value,
      }),
    },
    RESET: {
      actions: assign({
        elapsed: 0,
      }),
    },
  },
});
```

## Result

<iframe
  src="https://codesandbox.io/embed/7guis-timer-2gzst?fontsize=14&hidenavigation=1&theme=dark"
  style="width:100%; height:500px; border:0; border-radius: 4px; overflow:hidden;"
  title="7GUIs: Timer"
  allow="geolocation; microphone; camera; midi; vr; accelerometer; gyroscope; payment; ambient-light-sensor; encrypted-media; usb"
  sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"
></iframe>
