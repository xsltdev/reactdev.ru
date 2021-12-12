# Иерархические узлы состояния

В диаграммах состояний состояния могут быть вложены в другие состояния. Эти вложенные состояния называются **составными состояниями** (_compound states_).

## API

Следующий пример - конечный автомат светофора с вложенными состояниями:

```js
const pedestrianStates = {
  initial: 'walk',
  states: {
    walk: {
      on: {
        PED_COUNTDOWN: { target: 'wait' },
      },
    },
    wait: {
      on: {
        PED_COUNTDOWN: { target: 'stop' },
      },
    },
    stop: {},
    blinking: {},
  },
};

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
      on: {
        TIMER: { target: 'green' },
      },
      ...pedestrianStates,
    },
  },
  on: {
    POWER_OUTAGE: { target: '.red.blinking' },
    POWER_RESTORED: { target: '.red' },
  },
});
```

---

<iframe src="https://stately.ai/viz/embed/?gist=e8af8924afe9352bf7d1e06f06407061" width="100%" height="300"></iframe>

`'green'` и `'yellow'` состояния - это **простые состояния** (_simple states_) - у них нет дочерних состояний. Напротив, `'red'` состояние является **составным состоянием** (_compound state_), поскольку оно состоит из **подсостояний** (_substates_) `pedestrianStates`.

## Начальные состояния

Когда вводится составное состояние, сразу же вводится и его начальное состояние. В следующем примере светофора:

1. переход в состояние `'red'`
2. поскольку `'red'` имеет начальное состояние `'walk'`, то переходим в состояние `{ red: 'walk' }`.

```js
console.log(
  lightMachine.transition('yellow', { type: 'TIMER' }).value
);
// => {
//   red: 'walk'
// }
```

## События

Когда простое состояние не обрабатывает `event`, это `event` распространяется до своего родительского состояния для обработки. В следующем примере светофора:

1. состояние `{red: 'stop'}` не обрабатывает событие `'TIMER'`
2. событие `'TIMER'` отправляется в `'red'` родительское состояние, которое обрабатывает событие.

```js
console.log(
  lightMachine.transition(
    { red: 'stop' },
    { type: 'TIMER' }
  ).value
);
// => 'green'
```

Если ни состояние, ни какое-либо из его предков (родительских) состояний не обрабатывают событие, переход не происходит. В `strict` режиме (указанном в [конфигурации](machines.md#configuration) автомата) это вызовет ошибку.

```js
console.log(
  lightMachine.transition('green', { type: 'UNKNOWN' })
    .value
);
// => 'green'
```
