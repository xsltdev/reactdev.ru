# История

[Узел состояния](statenodes.md) истории (_history_) - это особый вид узла состояния, который при достижении указывает машине перейти к последнему значению состояния этой области. Есть два типа состояний истории:

- `'shallow'`, который указывает только значение истории верхнего уровня, или
- `'deep'`, который определяет верхний уровень и все значения истории дочернего уровня.

## Конфигурация состояния истории

Конфигурация для состояния истории такая же, как и для узла атомарного состояния, с некоторыми дополнительными свойствами:

- `type: 'history'` чтобы указать, что это узел состояния истории
- `history` (`shallow` | `deep`) - глубина истории. По-умолчанию `shallow`.
- `target` (StateValue) - цель по умолчанию, если история не существует. По умолчанию используется значение начального состояния родительского узла.

Рассмотрим следующую (надуманную) диаграмму состояний:

```js
const fanMachine = createMachine({
  id: 'fan',
  initial: 'fanOff',
  states: {
    fanOff: {
      on: {
        // transitions to history state
        POWER: { target: 'fanOn.hist' },
        HIGH_POWER: { target: 'fanOn.highPowerHist' },
      },
    },
    fanOn: {
      initial: 'first',
      states: {
        first: {
          on: {
            SWITCH: { target: 'second' },
          },
        },
        second: {
          on: {
            SWITCH: { target: 'third' },
          },
        },
        third: {},

        // shallow history state
        hist: {
          type: 'history',
          history: 'shallow', // optional; default is 'shallow'
        },

        // shallow history state with default
        highPowerHist: {
          type: 'history',
          target: 'third',
        },
      },
      on: {
        POWER: { target: 'fanOff' },
      },
    },
  },
});
```

В приведенной выше машине переход от `fanOff` по событию `POWER` переходит в состояние `fanOn.hist`, которое определяется как состояние неглубокой истории. Это означает, что автомат должен перейти в состояние `fanOn` и в какое бы ни было предыдущее подсостояние `fanOn`. По умолчанию `fanOn` перейдет в исходное состояние `first`, если нет состояния истории.

```js
const firstState = fanMachine.transition(
  fanMachine.initialState,
  {
    type: 'POWER',
  }
);
console.log(firstState.value);
// transitions to the initial state of 'fanOn' since there is no history
// => {
//   fanOn: 'first'
// }

const secondState = fanMachine.transition(firstState, {
  type: 'SWITCH',
});
console.log(secondState.value);
// => {
//   fanOn: 'second'
// }

const thirdState = fanMachine.transition(secondState, {
  type: 'POWER',
});
console.log(thirdState.value);
// => 'fanOff'

console.log(thirdState.history);
// => State {
//   value: { fanOn: 'second' },
//   actions: []
// }

const fourthState = fanMachine.transition(thirdState, {
  type: 'POWER',
});
console.log(fourthState.value);
// transitions to 'fanOn.second' from history
// => {
//   fanOn: 'second'
// }
```

Если задана цель `target`, и история не существует для региона состояния, в котором задано состояние истории, по умолчанию она перейдет в состояние `target`:

```js
const firstState = fanMachine.transition(
  fanMachine.initialState,
  {
    type: 'HIGH_POWER',
  }
);
console.log(firstState.value);
// transitions to the target state of 'fanOn.third' since there is no history
// => {
//   fanOn: 'third'
// }
```

## Примечания

- К состояниям истории можно получить прямой доступ из экземпляров `State` в `state.history`, но это редко бывает необходимо.
