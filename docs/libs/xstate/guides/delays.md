# Отложенные события и переходы

Задержки и таймауты можно декларативно обрабатывать с помощью диаграмм состояний.

## Отложенные переходы

Переходы могут выполняться автоматически после задержки. Это настраивается в состоянии в свойстве `after`, которое задает миллисекундные задержки на переходы:

```js
const lightDelayMachine = createMachine({
  id: 'lightDelay',
  initial: 'green',
  states: {
    green: {
      after: {
        // after 1 second, transition to yellow
        1000: { target: 'yellow' },
      },
    },
    yellow: {
      after: {
        // after 0.5 seconds, transition to red
        500: { target: 'red' },
      },
    },
    red: {
      after: {
        // after 2 seconds, transition to green
        2000: { target: 'green' },
      },
    },
  },
});
```

Отложенные переходы можно указать так же, как вы указываете их в свойстве `on: ...` Они могут быть явными:

```js
// ...
states: {
  green: {
    after: {
      1000: { target: 'yellow' }
    }
  }
}
// ...
```

Отложенные переходы также могут быть условными по отношению к единственному значению задержки:

```js
// ...
states: {
  green: {
    after: {
      1000: [
        { target: 'yellow', cond: 'trafficIsLight' },
        { target: 'green' } // reenter 'green' state
      ]
    }
  }
}
// ...
```

Или отложенные переходы могут быть обусловлены несколькими задержками. Будет выполнен первый выбранный отложенный переход, который предотвратит выполнение последующих переходов. В следующем примере, если условие `trafficIsLight` истинно, то более поздний переход `2000: 'yellow'` не будет выполняться:

```js
// ...
states: {
  green: {
    after: {
      1000: { target: 'yellow', cond: 'trafficIsLight' },
	  // always transition to 'yellow' after 2 seconds
      2000: { target: 'yellow' }
    }
  }
}
// ...
```

Условные отложенные переходы также можно указать в виде массива:

```js
// ...
states: {
  green: {
    after: [
      {
        delay: 1000,
        target: 'yellow',
        cond: 'trafficIsLight',
      },
      { delay: 2000, target: 'yellow' },
    ];
  }
}
// ...
```

### Вычисляемые задержки на переходах

_Начиная с версии 4.4+_

Отложенные переходы, указанные в свойстве `after: {...}`, могут иметь динамические задержки, задаваемые строковой ссылкой на задержку:

```js
const lightDelayMachine = createMachine(
  {
    id: 'lightDelay',
    initial: 'green',
    context: {
      trafficLevel: 'low',
    },
    states: {
      green: {
        after: {
          // after 1 second, transition to yellow
          LIGHT_DELAY: { target: 'yellow' },
        },
      },
      yellow: {
        after: {
          YELLOW_LIGHT_DELAY: { target: 'red' },
        },
      },
      // ...
    },
  },
  {
    // String delays configured here
    delays: {
      LIGHT_DELAY: (context, event) => {
        return context.trafficLevel === 'low' ? 1000 : 3000;
      },
      YELLOW_LIGHT_DELAY: 500, // static value
    },
  }
);
```

Или напрямую функцией, как условные отложенные переходы:

```js
// ...
green: {
  after: [
    {
      delay: (context, event) => {
        return context.trafficLevel === 'low' ? 1000 : 3000;
      },
      target: 'yellow'
    }
  ]
},
// ...
```

Однако предпочтительнее использовать строковые ссылки на задержку, как в первом примере, или в свойстве задержки:

```js
// ...
green: {
  after: [
    {
      delay: 'LIGHT_DELAY',
      target: 'yellow'
    }
  ]
},
// ...
```

## Отложенные события

Если вы просто хотите отправить событие после задержки, вы можете указать `delay` в качестве опции во втором аргументе создателя действия `send(...)`:

```js
import { actions } from 'xstate';
const { send } = actions;

// action to send the 'TIMER' event after 1 second
const sendTimerAfter1Second = send(
  { type: 'TIMER' },
  { delay: 1000 }
);
```

Вы также можете предотвратить отправку этих отложенных событий, отменив их. Это делается с помощью создателя действия `cancel(...)`:

```js
import { actions } from 'xstate';
const { send, cancel } = actions;

// action to send the 'TIMER' event after 1 second
const sendTimerAfter1Second = send(
  { type: 'TIMER' },
  {
    delay: 1000,
    id: 'oneSecondTimer', // give the event a unique ID
  }
);

// pass the ID of event to cancel
const cancelTimer = cancel('oneSecondTimer');

const toggleMachine = createMachine({
  id: 'toggle',
  initial: 'inactive',
  states: {
    inactive: {
      entry: sendTimerAfter1Second,
      on: {
        TIMER: { target: 'active' },
        CANCEL: { actions: cancelTimer },
      },
    },
    active: {},
  },
});

// if the CANCEL event is sent before 1 second,
// the TIMER event will be canceled.
```

## Вычисляемые задержки

_Начиная с версии 4.3+_

Параметр `delay` также может быть вычислен как выражение задержки, которое представляет собой функцию, которая принимает текущий контекст `context` и событие `event`, вызвавшее действие `send()`, и возвращает вычисленный `delay` (в миллисекундах):

```js
const dynamicDelayMachine = createMachine({
  id: 'dynamicDelay',
  context: {
    initialDelay: 1000,
  },
  initial: 'idle',
  states: {
    idle: {
      on: {
        ACTIVATE: { target: 'pending' },
      },
    },
    pending: {
      entry: send(
        { type: 'FINISH' },
        {
          // delay determined from custom event.wait property
          delay: (context, event) =>
            context.initialDelay + event.wait || 0,
        }
      ),
      on: {
        FINISH: { target: 'finished' },
      },
    },
    finished: { type: 'final' },
  },
});

const dynamicDelayService = interpret(dynamicDelayMachine)
  .onDone(() => console.log('done!'))
  .start();

dynamicDelayService.send({
  type: 'ACTIVATE',
  // arbitrary property
  wait: 2000,
});

// after 3000ms (1000 + 2000), console will log:
// => 'done!'
```

## Интерпретация

С [интерпретатором](interpretation.md) XState для отложенных действий будут использоваться собственные функции `setTimeout` и `clearTimeout`:

```js
import { interpret } from 'xstate';

const service = interpret(
  lightDelayMachine
).onTransition((state) => console.log(state.value));

service.start();
// => 'green'

// (after 1 second)

// => 'yellow'
```

Для тестирования интерпретатор XState предоставляет `SimulatedClock`:

```js
import { interpret } from 'xstate';
// import { SimulatedClock } from 'xstate/lib/interpreter'; // < 4.6.0
import { SimulatedClock } from 'xstate/lib/SimulatedClock'; // >= 4.6.0

const service = interpret(lightDelayMachine, {
  clock: new SimulatedClock(),
}).onTransition((state) => console.log(state.value));

service.start();
// => 'green'

// move the SimulatedClock forward by 1 second
service.clock.increment(1000);
// => 'yellow'
```

Вы можете создать свои собственные «часы», чтобы предоставить их интерпретатору. Интерфейс часов - это объект с двумя функциями / методами:

- `setTimeout` — те же аргументы, что и `window.setTimeout(fn, timeout)`
- `clearTimeout` — те же аргументы, что и `window.clearTimeout(id)`

## За кулисами

Свойство `after: ...` не вносит ничего нового в семантику диаграммы состояний. Вместо этого он создает обычные переходы, которые выглядят следующим образом:

```js
// ...
states: {
  green: {
    entry: [
      send(after(1000, 'light.green'), { delay: 1000 }),
      send(after(2000, 'light.green'), { delay: 2000 })
    ],
    onExit: [
      cancel(after(1000, 'light.green')),
      cancel(after(2000, 'light.green'))
    ],
    on: {
      [after(1000, 'light.green')]: {
        target: 'yellow',
        cond: 'trafficIsLight'
      },
      [after(2000, 'light.green')]: {
        target: 'yellow'
      }
    }
  }
}
// ...
```

Интерпретируемая диаграмма состояний будет отправлять `send(...)` события `after(...)` после их задержки `delay`, если только узел состояния не будет закрыт, что отменит `cancel(...)` эти отложенные события `send(...)`.
