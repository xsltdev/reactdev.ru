---
description: Вызовите предоставленную функцию set с новым состоянием, и оно будет неглубоко объединено с существующим состоянием в хранилище
---

# Обновление состояния

## Плоские обновления

Обновлять состояние с помощью Zustand очень просто! Вызовите предоставленную функцию `set` с новым состоянием, и оно будет неглубоко объединено с существующим состоянием в хранилище. **Примечание** См. следующий раздел о вложенных состояниях.

```tsx
import { create } from 'zustand';

type State = {
    firstName: string;
    lastName: string;
};

type Action = {
    updateFirstName: (
        firstName: State['firstName']
    ) => void;
    updateLastName: (lastName: State['lastName']) => void;
};

// Create your store, which includes both state and (optionally) actions
const usePersonStore = create<State & Action>((set) => ({
    firstName: '',
    lastName: '',
    updateFirstName: (firstName) =>
        set(() => ({ firstName: firstName })),
    updateLastName: (lastName) =>
        set(() => ({ lastName: lastName })),
}));

// In consuming app
function App() {
    // "select" the needed state and actions, in this case, the firstName value
    // and the action updateFirstName
    const firstName = usePersonStore(
        (state) => state.firstName
    );
    const updateFirstName = usePersonStore(
        (state) => state.updateFirstName
    );

    return (
        <main>
            <label>
                First name
                <input
                    // Update the "firstName" state
                    onChange={(e) =>
                        updateFirstName(
                            e.currentTarget.value
                        )
                    }
                    value={firstName}
                />
            </label>

            <p>
                Hello, <strong>{firstName}!</strong>
            </p>
        </main>
    );
}
```

## Глубоко вложенный объект

Если у вас есть объект с глубоким состоянием, например, такой:

```ts
type State = {
    deep: {
        nested: {
            obj: { count: number };
        };
    };
};
```

Обновление вложенного состояния требует определенных усилий для обеспечения неизменяемости процесса.

### Обычный подход

Как и в React или Redux, обычный подход заключается в копировании каждого уровня объекта состояния. Это делается с помощью оператора спреда `...`, а также путем ручного объединения с новыми значениями состояния. Например:

```ts
  normalInc: () =>
    set((state) => ({
      deep: {
        ...state.deep,
        nested: {
          ...state.deep.nested,
          obj: {
            ...state.deep.nested.obj,
            count: state.deep.nested.obj.count + 1
          }
        }
      }
    })),
```

Это очень долго! Давайте рассмотрим некоторые альтернативы, которые облегчат вам жизнь.

### С Immer

Многие люди используют [Immer](https://github.com/immerjs/immer) для обновления вложенных значений. Immer можно использовать в любое время, когда вам нужно обновить вложенное состояние, например, в React, Redux и, конечно же, Zustand!

Вы можете использовать Immer, чтобы сократить время обновления состояния для глубоко вложенного объекта. Давайте посмотрим на пример:

```ts
  immerInc: () =>
    set(produce((state: State) => { ++state.deep.nested.obj.count })),
```

Какое сокращение! Пожалуйста, примите к сведению ["загвоздки", перечисленные здесь](../integrations/immer-middleware.md).

### С optics-ts

Есть еще один вариант с [optics-ts](https://github.com/akheron/optics-ts/):

```ts
  opticsInc: () =>
    set(O.modify(O.optic<State>().path("deep.nested.obj.count"))((c) => c + 1)),
```

В отличие от Immer, optics-ts не использует прокси или синтаксис мутации.

### С Ramda

Вы также можете использовать [Ramda](https://ramdajs.com/):

```ts
  ramdaInc: () =>
    set(R.modifyPath(["deep", "nested", "obj", "count"], (c) => c + 1)),
```

И ramda, и optics-ts также работают с типами.

### CodeSandbox демо

<iframe src="https://codesandbox.io/embed/ynn3o?view=editor+%2B+preview&module=%2Fsrc%2FApp.tsx" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="zustand normal/immer/optics/ramda updating" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/getting-started/introduction></small>
