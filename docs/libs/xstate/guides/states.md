# Состояния

**Состояние** - это абстрактное представление системы (например, приложения) в определенный момент времени.

## API

Текущее состояние машины представлено экземпляром `State`:

```js hl_lines="13-18 23-28"
const lightMachine = createMachine({
  id: 'light',
  initial: 'green',
  states: {
    green: {
      /* ... */
    },
    // ...
  },
});

console.log(lightMachine.initialState);
// State {
//   value: 'green',
//   actions: [],
//   context: undefined,
//   // ...
// }

console.log(
  lightMachine.transition('yellow', { type: 'TIMER' })
);
// State {
//   value: { red: 'walk' },
//   actions: [],
//   context: undefined,
//   // ...
// }
```

## Определение состояния

Экземпляр объекта `State` является сериализуемым в формате JSON и имеет следующие свойства:

- `value` - текущее значение состояния (например, `{red: 'walk'}`)
- `context` - текущее значение [контекста](./context.md) этого состояния
- `event` - объект события, вызвавший переход в это состояние
- `actions` - массив [действий](./actions.md), которые нужно выполнить
- `activities` - отображение [видов деятельности](./activities.md) в `true`, если деятельность началась или в `false`, если остановлена.
- `history` - предыдущее состояние `State`
- `meta` - любая статичная метаинформация, определенная в свойстве `meta` [узла состояния](./statenodes.md)
- `done` - признак конечного состояния

Объект `State` также содержит другие свойства, такие как `historyValue`, `events`, `tree` и другие, которые обычно не имеют отношения к делу и предназначены для внутреннего использования.

## Методы и свойства состояния

Вот несколько полезных методов и свойств, которые можно использовать для улучшения процесса разработки:

### `state.matches()`

Метод `state.matches(parentStateValue)` определяет, является ли текущее значение `state.value` подмножеством заданного `parentStateValue`. Метод определяет, «совпадает» ли значение родительского состояния со значением состояния. Например, если текущее значение `state.value` равно `{red: 'stop'}`:

```js
console.log(state.value);
// => { red: 'stop' }

console.log(state.matches('red'));
// => true

console.log(state.matches('red.stop'));
// => true

console.log(state.matches({ red: 'stop' }));
// => true

console.log(state.matches('green'));
// => false
```

!!!tip "Подсказка"

    Если вы хотите сравнить одно из нескольких состояний, вы можете использовать [`.some()`](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Array/some) для массива значений состояния, чтобы выполнить это:

    ```js
    const isMatch = [
      { customer: 'deposit' },
      { customer: 'withdrawal' },
    ].some(state.matches);
    ```

### `state.nextEvents`

`state.nextEvents` указывает следующие события, которые вызовут переход из текущего состояния:

```js
const { initialState } = lightMachine;

console.log(initialState.nextEvents);
// => ['TIMER', 'EMERGENCY']
```

`state.nextEvents` полезен для определения, какие следующие события могут быть выполнены, и представления этих потенциальных событий в пользовательском интерфейсе, таких как включение или отключение определенных кнопок.

### `state.changed`

`state.changed` указывает, изменилось ли это состояние по сравнению с предыдущим состоянием. Состояние считается «измененным», если:

- Его значение не равно его предыдущему значению, или:
- У него есть какие-либо новые действия (побочные эффекты) для выполнения.

Исходное состояние (без истории) вернет `undefined`.

```js
const { initialState } = lightMachine;

console.log(initialState.changed);
// => undefined

const nextState = lightMachine.transition(initialState, {
  type: 'TIMER',
});

console.log(nextState.changed);
// => true

const unchangedState = lightMachine.transition(nextState, {
  type: 'UNKNOWN_EVENT',
});

console.log(unchangedState.changed);
// => false
```

### `state.done`

`state.done` указывает, является ли состояние [«конечным состоянием»](./final.md) - это состояние, которое указывает, что его автомат достиг своего конечного (терминального) состояния и больше не может переходить в какое-либо другое состояние.

```js
const answeringMachine = createMachine({
  initial: 'unanswered',
  states: {
    unanswered: {
      on: {
        ANSWER: { target: 'answered' },
      },
    },
    answered: {
      type: 'final',
    },
  },
});

const { initialState } = answeringMachine;
initialState.done; // false

const answeredState = answeringMachine.transition(
  initialState,
  {
    type: 'ANSWER',
  }
);
answeredState.done; // true
```

### `state.toStrings()`

Метод `state.toStrings()` возвращает массив строк, представляющих _все_ пути значений состояния. Например, если текущее значение `state.value` равно `{red: 'stop'}`:

```js
console.log(state.value);
// => { red: 'stop' }

console.log(state.toStrings());
// => ['red', 'red.stop']
```

Метод `state.toStrings()` полезен для представления текущего состояния в строковых средах, таких как классы CSS или атрибуты данных.

### `state.children`

`state.children` is an object mapping spawned service/actor IDs to their instances. See [📖 Referencing Services](./communication.md#referencing-services) for more details.

`state.children` - это объект, отображающий идентификаторы порожденных служб / акторов на их экземпляры. См. [📖 Referencing Services](./communication.md#referencing-services) для более подробной информации.

Пример:

```js
const machine = createMachine({
  // ...
  invoke: [
    { id: 'notifier', src: createNotifier },
    { id: 'logger', src: createLogger },
  ],
  // ...
});

const service = invoke(machine)
  .onTransition((state) => {
    state.children.notifier; // service from createNotifier()
    state.children.logger; // service from createLogger()
  })
  .start();
```

### `state.hasTag()`

_С версии 4.19.0_

Метод `state.hasTag(tag)` определяет, есть ли в текущей конфигурации состояния узел состояния с данным тегом.

```js hl_lines="5 8 11"
const machine = createMachine({
  initial: 'green',
  states: {
    green: {
      tags: 'go', // single tag
    },
    yellow: {
      tags: 'go',
    },
    red: {
      tags: ['stop', 'other'], // multiple tags
    },
  },
});
```

Например, если указанный выше автомат находится в зеленом или желтом состоянии, вместо прямого сопоставления состояния с помощью `state.matches('green') || state.matches('yellow')`, можно использовать `state.hasTag('go')`:

```js
const canGo = state.hasTag('go');
// => `true` if in 'green' or 'yellow' state
```

### `state.can()`

_С версии 4.25.0_

Метод `state.can(event)` определяет, вызовет ли событие изменение состояния, если оно будет отправлено на интерпретируемый автомат. Метод вернет истину, если состояние изменится из-за отправляемого события; иначе метод вернет `false`:

```js
const machine = createMachine({
  initial: 'inactive',
  states: {
    inactive: {
      on: {
        TOGGLE: 'active',
      },
    },
    active: {
      on: {
        DO_SOMETHING: { actions: ['something'] },
      },
    },
  },
});

const inactiveState = machine.initialState;

inactiveState.can('TOGGLE'); // true
inactiveState.can('DO_SOMETHING'); // false

// Also takes in full event objects:
inactiveState.can({
  type: 'DO_SOMETHING',
  data: 42,
}); // false

const activeState = machine.transition(
  inactiveState,
  'TOGGLE'
);

activeState.can('TOGGLE'); // false
activeState.can('DO_SOMETHING'); // true, since an action will be executed
```

Состояние считается «измененным», если [`state.changed`](#state-changed) `true` и если выполняется любое из следующих условий:

- значение `state.value` изменилось
- есть новые `state.actions`, которые нужно выполнить
- значение `state.context` изменилось

## Сохранение состояния

Как уже упоминалось, объект `State` можно сохранить, сериализовав его в строковый формат JSON:

```js
const jsonState = JSON.stringify(currentState);

// Example: persisting to localStorage
try {
  localStorage.setItem('app-state', jsonState);
} catch (e) {
  // unable to save to localStorage
}
```

Состояние можно восстановить с помощью статического метода `State.create(...)`:

```js
import { State, interpret } from 'xstate';
import { myMachine } from '../path/to/myMachine';

// Retrieving the state definition from localStorage,
// if localStorage is empty use machine initial state
const stateDefinition =
  JSON.parse(localStorage.getItem('app-state')) ||
  myMachine.initialState;

// Use State.create() to restore state from a plain object
const previousState = State.create(stateDefinition);
```

Затем вы можете интерпретировать автомат из этого состояния, передав `State` в метод `.start(...)` интерпретируемого сервиса:

```js
// ...

// This will start the service at the specified State
const service = interpret(myMachine).start(previousState);
```

This will also maintain and restore previous [history states]() and ensures that `.events` and `.nextEvents` represent the correct values.

Это также будет поддерживать и восстанавливать предыдущие [состояния истории](./history.md) и гарантирует, что `.events` и `.nextEvents` представляют правильные значения.

!!!warning "Внимание"

    Сохранение созданных [акторов](actors.md) еще не поддерживается в XState.

## Метаданные состояния

Мета-данные, которые представляют собой статические данные, описывающие соответствующие свойства любого узла состояния, могут быть указаны в свойстве `.meta` узла состояния:

```js hl_lines="17-19 22-24 30-32 35-37 40-42"
const fetchMachine = createMachine({
  id: 'fetch',
  initial: 'idle',
  states: {
    idle: {
      on: { FETCH: { target: 'loading' } },
    },
    loading: {
      after: {
        3000: 'failure.timeout',
      },
      on: {
        RESOLVE: { target: 'success' },
        REJECT: { target: 'failure' },
        TIMEOUT: { target: 'failure.timeout' }, // manual timeout
      },
      meta: {
        message: 'Loading...',
      },
    },
    success: {
      meta: {
        message: 'The request succeeded!',
      },
    },
    failure: {
      initial: 'rejection',
      states: {
        rejection: {
          meta: {
            message: 'The request failed.',
          },
        },
        timeout: {
          meta: {
            message: 'The request timed out.',
          },
        },
      },
      meta: {
        alert: 'Uh oh.',
      },
    },
  },
});
```

Текущее состояние машины собирает `.meta` данные всех узлов состояния, представленные значением состояния, и помещает их в объект, где:

- Ключи - это [идентификаторы узлов состояния](./ids.md).
- Значения - это значения мета-узла состояния `.meta`.

Например, если вышеуказанный автомат находится в состоянии `failure.timeout` (которое представлено двумя узлами состояния с идентификаторами «`failure`» и «`failure.timeout`»), свойство `.meta` объединит все значения `.meta` следующим образом:

```js hl_lines="9-16"
const failureTimeoutState = fetchMachine.transition(
  'loading',
  {
    type: 'TIMEOUT',
  }
);

console.log(failureTimeoutState.meta);
// => {
//   failure: {
//     alert: 'Uh oh.'
//   },
//   'failure.timeout': {
//     message: 'The request timed out.'
//   }
// }
```

!!!tip "Подсказка: Агрегирование метаданных"

    Что делать с метаданными - решать вам. В идеале метаданные должны содержать _только_ значения, сериализуемые в формате JSON. Рассмотрите возможность слияния / агрегирования метаданных иначе. Например, следующая функция отбрасывает ключи идентификатора узла состояния (если они неактуальны) и объединяет метаданные:

    ```js
    function mergeMeta(meta) {
    	return Object.keys(meta).reduce((acc, key) => {
    		const value = meta[key];

    		// Assuming each meta value is an object
    		Object.assign(acc, value);

    		return acc;
    	}, {});
    }

    const failureTimeoutState = fetchMachine.transition(
    	'loading',
    	{
    		type: 'TIMEOUT',
    	}
    );

    console.log(mergeMeta(failureTimeoutState.meta));
    // => {
    //   alert: 'Uh oh.',
    //   message: 'The request timed out.'
    // }
    ```

## Примечания

- Вам никогда не придется создавать экземпляр `State` вручную. Считайте `State` объектом, доступным только для чтения, который поступает _только_ от `machine.transition(...)` или `service.onTransition(...)`.
- `state.history` не сохраняет свою историю во избежание утечек памяти. `state.history.history === undefined`. В противном случае вы создадите огромный связанный список и заново изобретете блокчейн, чего мы не собираемся делать.
- Это поведение может быть изменено в будущих версиях.
