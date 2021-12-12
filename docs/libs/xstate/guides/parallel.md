# Параллельные узлы состояний

В диаграммах состояний вы можете объявить состояние как **параллельное состояние** (_parallel state_). Это означает, что все его дочерние состояния будут выполняться _одновременно_.

## API

Узел параллельного состояния указывается на машине и / или в любом вложенном составном состоянии путем установки типа `type: 'parallel'`.

Например, автомат из примера ниже позволяет одновременно активировать составные состояния `upload` и `download`. Представьте, что это приложение, в котором вы можете скачивать и загружать файлы одновременно:

```js hl_lines="3 5 21"
const fileMachine = createMachine({
  id: 'file',
  type: 'parallel',
  states: {
    upload: {
      initial: 'idle',
      states: {
        idle: {
          on: {
            INIT_UPLOAD: { target: 'pending' },
          },
        },
        pending: {
          on: {
            UPLOAD_COMPLETE: { target: 'success' },
          },
        },
        success: {},
      },
    },
    download: {
      initial: 'idle',
      states: {
        idle: {
          on: {
            INIT_DOWNLOAD: { target: 'pending' },
          },
        },
        pending: {
          on: {
            DOWNLOAD_COMPLETE: { target: 'success' },
          },
        },
        success: {},
      },
    },
  },
});

console.log(fileMachine.initialState.value);
// => {
//   upload: 'idle',
//   download: 'idle'
// }
```

---

<iframe src="https://stately.ai/viz/embed/?gist=ef808b0400ececa786ec17e20d62c1e0" width="100%" height="300"></iframe>

Значение состояния узла параллельного состояния представлено как объект. Это значение состояния объекта можно использовать для дальнейшего перехода в разные состояния в узле параллельного состояния:

```js
console.log(
  fileMachine.transition(
    {
      upload: 'pending',
      download: 'idle',
    },
    { type: 'UPLOAD_COMPLETE' }
  ).value
);
// => {
//   upload: 'success',
//   download: 'idle'
// }
```

Узел составного состояния может содержать узлы параллельного состояния. Конфигурация такая же, как и для узлов вложенного состояния:

```js
const lightMachine = createMachine({
  // not a parallel machine
  id: 'light',
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

    // nested parallel machine
    red: {
      type: 'parallel',
      states: {
        walkSign: {
          initial: 'solid',
          states: {
            solid: {
              on: {
                COUNTDOWN: { target: 'flashing' },
              },
            },
            flashing: {
              on: {
                STOP_COUNTDOWN: { target: 'solid' },
              },
            },
          },
        },
        pedestrian: {
          initial: 'walk',
          states: {
            walk: {
              on: {
                COUNTDOWN: { target: 'wait' },
              },
            },
            wait: {
              on: {
                STOP_COUNTDOWN: { target: 'stop' },
              },
            },
            stop: {
              type: 'final',
            },
          },
        },
      },
    },
  },
});

console.log(
  lightMachine.transition('yellow', { type: 'TIMER' }).value
);
// {
//   red: {
//     walkSign: 'solid',
//     pedestrian: 'walk'
//   }
// }
```

---

<iframe src="https://stately.ai/viz/embed/?gist=3887dee1e2bb6e84c3b5a42c056984ad" width="100%" height="300"></iframe>
