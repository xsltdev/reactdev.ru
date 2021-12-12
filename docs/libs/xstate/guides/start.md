# Начнём

## Наш первый конечный автомат

Предположим, мы хотим смоделировать [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) как конечный автомат. Сначала установите XState с помощью NPM или Yarn:

```bash
npm install xstate --save
```

> Если вы используете VSCode, вам следует установить наше [расширение VSCode](https://marketplace.visualstudio.com/items?itemName=mattpocock.xstate-vscode), чтобы вы могли визуализировать автомат, который вы строите, в процессе работы.

Затем в своем проекте импортируйте `createMachine` — функцию, которая создает конечный автомат.

```js
import { createMachine } from 'xstate';

const promiseMachine = createMachine(/* ... */);
```

Мы передадим [конфигурацию автомата](./machines.md#configuration) `createMachine`. Нам потребуется предоставить:

- `id` — для идентификации автомата
- `initial` — для указания узла начального состояния, в котором должен находиться этот автомат
- `states` — для определения каждого из дочерних состояний:

```js
import { createMachine } from 'xstate';

const promiseMachine = createMachine({
  id: 'promise',
  initial: 'pending',
  states: {
    pending: {},
    resolved: {},
    rejected: {},
  },
});
```

Затем нам нужно добавить [переходы](./transitions.md) к узлам состояния.

```js
import { createMachine } from 'xstate';

const promiseMachine = createMachine({
  id: 'promise',
  initial: 'pending',
  states: {
    pending: {
      on: {
        RESOLVE: { target: 'resolved' },
        REJECT: { target: 'rejected' },
      },
    },
    resolved: {},
    rejected: {},
  },
});
```

Нам также нужно пометить узлы состояния `resolved` и `rejected`, как узлы [конечного состояния](./final.md), поскольку автомат Promise прекращает работу, как только достигает этих состояний:

```js
import { createMachine } from 'xstate';

const promiseMachine = createMachine({
  id: 'promise',
  initial: 'pending',
  states: {
    pending: {
      on: {
        RESOLVE: { target: 'resolved' },
        REJECT: { target: 'rejected' },
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
```

Теперь наш конечный автомат готов к визуализации. Вы можете скопировать / вставить приведенный выше код и визуализировать его в [Stately Viz](https://stately.ai/viz). Вот как это будет выглядеть:

<iframe src="https://stately.ai/viz/embed/68548871-eecb-479b-b92a-b261e7d89671?mode=viz&panel=code&readOnly=1&showOriginalLink=1&controls=0&pan=0&zoom=0"
allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"
sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts" width="100%" height="300"
></iframe>

## Запуск нашего автомата

То, как мы запускаем наш автомат, зависит от того, где мы планируем его использовать.

### В Node.js или Vanilla JS

Чтобы [интерпретировать](./interpretation.md) автомат и заставить его работать, нам нужно добавить интерпретатор. Этот код создает службу:

```js
import { createMachine, interpret } from 'xstate';

const promiseMachine = createMachine({
  /* ... */
});

const promiseService = interpret(
  promiseMachine
).onTransition((state) => console.log(state.value));

// Start the service
promiseService.start();
// => 'pending'

promiseService.send({ type: 'RESOLVE' });
// => 'resolved'
```

### В React

Если бы мы хотели использовать наш автомат внутри компонента React, мы могли бы использовать хук [`useMachine`](../packages/xstate-react.md):

> Дополнительно нам нужно установить пакет `@xstate/react`

```tsx
import { useMachine } from '@xstate/react';

const Component = () => {
  const [state, send] = useMachine(promiseMachine);

  return (
    <div>
      {/** You can listen to what state the service is in */}
      {state.matches('pending') && <p>Loading...</p>}
      {state.matches('rejected') && <p>Promise Rejected</p>}
      {state.matches('resolved') && <p>Promise Resolved</p>}
      <div>
        {/** You can send events to the running service */}
        <button onClick={() => send('RESOLVE')}>
          Resolve
        </button>
        <button onClick={() => send('REJECT')}>
          Reject
        </button>
      </div>
    </div>
  );
};
```
