# Сохранение данных хранилища

Промежуточное ПО Persist позволяет хранить состояние Zustand в каком-либо хранилище (например, `localStorage`, `AsyncStorage`, `IndexedDB` и т. д.), тем самым сохраняя его данные.

Обратите внимание, что это промежуточное ПО поддерживает как синхронные хранилища, такие как `localStorage`, так и асинхронные, такие как `AsyncStorage`, но использование асинхронного хранилища связано с определенными затратами. Подробнее см. в разделе [Гидратация и асинхронные хранилища](#hydration-and-asynchronous-storages).

## Простой пример

```ts
import { create } from 'zustand';
import {
    persist,
    createJSONStorage,
} from 'zustand/middleware';

export const useBearStore = create(
    persist(
        (set, get) => ({
            bears: 0,
            addABear: () => set({ bears: get().bears + 1 }),
        }),
        {
            name: 'food-storage', // name of the item in the storage (must be unique)
            storage: createJSONStorage(
                () => sessionStorage
            ), // (optional) by default, 'localStorage' is used
        }
    )
);
```

## Параметры

### `name`

Это единственный обязательный параметр. Данное имя будет ключом, используемым для хранения вашего состояния Zustand в хранилище, поэтому оно должно быть уникальным.

### `storage`

> Тип: `() => StateStorage`

Хранилище `StateStorage` может быть импортировано с помощью:

```ts
import { StateStorage } from 'zustand/middleware';
```

> По-умолчанию: `createJSONStorage(() => localStorage)`

Позволяет использовать собственное хранилище. Просто передайте функцию, которая возвращает хранилище, которое вы хотите использовать. Рекомендуется использовать вспомогательную функцию [`createJSONStorage`](#createjsonstorage) для создания объекта `storage`, соответствующего интерфейсу `StateStorage`.

Пример:

```ts
import {
    persist,
    createJSONStorage,
} from 'zustand/middleware';

export const useBoundStore = create(
    persist(
        (set, get) => ({
            // ...
        }),
        {
            // ...
            storage: createJSONStorage(() => AsyncStorage),
        }
    )
);
```

### `partialize`

> Тип: `(state: Object) => Object`
>
> По-умолчанию: `(state) => state`

Позволяет выбрать некоторые поля состояния, которые будут хранилищем.

Вы можете опустить несколько полей, используя следующее:

```ts
export const useBoundStore = create(
    persist(
        (set, get) => ({
            foo: 0,
            bar: 1,
        }),
        {
            // ...
            partialize: (state) =>
                Object.fromEntries(
                    Object.entries(state).filter(
                        ([key]) => !['foo'].includes(key)
                    )
                ),
        }
    )
);
```

Или вы можете разрешить только определенные поля, используя следующее:

```ts
export const useBoundStore = create(
    persist(
        (set, get) => ({
            foo: 0,
            bar: 1,
        }),
        {
            // ...
            partialize: (state) => ({ foo: state.foo }),
        }
    )
);
```

### `onRehydrateStorage`

> Тип: `(state: Object) => ((state?: Object, error?: Error) => void) | void`

Этот параметр позволяет передать функцию-слушатель, которая будет вызываться при увлажнении хранилища.

Пример:

```ts
export const useBoundStore = create(
    persist(
        (set, get) => ({
            // ...
        }),
        {
            // ...
            onRehydrateStorage: (state) => {
                console.log('hydration starts');

                // optional
                return (state, error) => {
                    if (error) {
                        console.log(
                            'an error happened during hydration',
                            error
                        );
                    } else {
                        console.log('hydration finished');
                    }
                };
            },
        }
    )
);
```

### `version`

> Тип: `number`
>
> По-умолчанию: `0`

Если вы хотите внести в хранилище разрывное изменение (например, переименовать поле), вы можете указать новый номер версии. По умолчанию, если версия в хранилище не совпадает с версией в коде, хранилище не будет использоваться. Вы можете использовать функцию [migrate](#migrate) (см. ниже) для обработки разрывных изменений, чтобы сохранить ранее хранилище данных.

### `migrate`

> Тип: `(persistedState: Object, version: number) => Object | Promise<Object>`
>
> По-умолчанию: `(persistedState) => persistedState`

Вы можете использовать эту опцию для обработки миграции версий. Функция migrate принимает в качестве аргументов сохраняемое состояние и номер версии. Она должна вернуть состояние, соответствующее последней версии (версия в коде).

Например, если вы хотите переименовать поле, вы можете использовать следующее:

```ts
export const useBoundStore = create(
    persist(
        (set, get) => ({
            newField: 0, // let's say this field was named otherwise in version 0
        }),
        {
            // ...
            version: 1, // a migration will be triggered if the version in the storage mismatches this one
            migrate: (persistedState, version) => {
                if (version === 0) {
                    // if the stored value is in version 0, we rename the field to the new name
                    persistedState.newField =
                        persistedState.oldField;
                    delete persistedState.oldField;
                }

                return persistedState;
            },
        }
    )
);
```

### `merge`

> Тип: `(persistedState: Object, currentState: Object) => Object`
>
> По-умолчанию: `(persistedState, currentState) => ({ ...currentState, ...persistedState })`

В некоторых случаях вы можете захотеть использовать пользовательскую функцию слияния, чтобы объединить сохраненное значение с текущим состоянием.

По умолчанию промежуточное ПО выполняет неглубокое слияние. Неглубокого слияния может быть недостаточно, если у вас есть частично сохраняемые вложенные объекты. Например, если хранилище содержит следующее:

```ts
{
  foo: {
    bar: 0,
  }
}
```

Но ваше хранилище Zustand содержит:

```ts
{
  foo: {
    bar: 0,
    baz: 1,
  }
}
```

При неглубоком слиянии поле `baz` будет удалено из объекта `foo`. Одним из способов исправить это было бы создание собственной функции глубокого слияния:

```ts
export const useBoundStore = create(
    persist(
        (set, get) => ({
            foo: {
                bar: 0,
                baz: 1,
            },
        }),
        {
            // ...
            merge: (persistedState, currentState) =>
                deepMerge(currentState, persistedState),
        }
    )
);
```

### `skipHydration`

> Тип: `boolean | undefined`
>
> По-умолчанию: `undefined`

По умолчанию хранилище увлажняется при инициализации.

В некоторых приложениях вам может потребоваться контролировать момент первого увлажнения. Например, в приложениях с рендерингом сервера.

Если вы установите `skipHydration`, начальный вызов гидратации не будет вызываться, и вам останется вручную вызвать `rehydrate()`.

```ts
export const useBoundStore = create(
    persist(
        () => ({
            count: 0,
            // ...
        }),
        {
            // ...
            skipHydration: true,
        }
    )
);
```

---

```tsx
import { useBoundStore } from './path-to-store';

export function StoreConsumer() {
  // hydrate persisted store after on mount
  useEffect(() => {
    useBoundStore.persist.rehydrate();
  }, [])

  return (
    //...
  )
}
```

## API

> Версия: >=3.6.3

Persist API позволяет вам осуществлять ряд взаимодействий с промежуточным ПО Persist изнутри или снаружи компонента React.

### `getOptions`

> Тип: `() => Partial<PersistOptions>`
>
> Возвращает: Options of the Persist middleware

Например, с его помощью можно получить имя хранилища:

```ts
useBoundStore.persist.getOptions().name;
```

### `setOptions`

> Тип: `(newOptions: Partial<PersistOptions>) => void`

Изменяет параметры промежуточного ПО. Обратите внимание, что новые параметры будут объединены с текущими.

Например, это можно использовать для изменения имени хранилища:

```ts
useBoundStore.persist.setOptions({
    name: 'new-name',
});
```

Или даже сменить механизм хранения:

```ts
useBoundStore.persist.setOptions({
    storage: createJSONStorage(() => sessionStorage),
});
```

### `clearStorage`

> Тип: `() => void`

Очищает все, что хранилище под ключом [name](#name).

```ts
useBoundStore.persist.clearStorage();
```

### `rehydrate`

> Тип: `() => Promise<void>`

В некоторых случаях вы можете захотеть запустить регидратацию вручную. Это можно сделать, вызвав метод `rehydrate`.

```ts
await useBoundStore.persist.rehydrate();
```

### `hasHydrated`

> Тип: `() => boolean`

Это нереактивный геттер для проверки того, было ли хранилище увлажнено (обратите внимание, что он обновляется при вызове [`rehydrate`](#rehydrate)).

```ts
useBoundStore.persist.hasHydrated();
```

### `onHydrate`

> Тип: `(listener: (state) => void) => () => void`

> Возвращает: функция отписки

Этот обработчик будет вызван, когда начнется процесс гидратации.

```ts
const unsub = useBoundStore.persist.onHydrate((state) => {
    console.log('hydration starts');
});

// later on...
unsub();
```

### `onFinishHydration`

> Тип: `(listener: (state) => void) => () => void`

> Возвращает: функция отписки

Этот слушатель будет вызван, когда процесс гидратации завершится.

```ts
const unsub = useBoundStore.persist.onFinishHydration(
    (state) => {
        console.log('hydration finished');
    }
);

// later on...
unsub();
```

### `createJSONStorage`

> Тип: `(getStorage: () => StateStorage, options?: JsonStorageOptions) => StateStorage`
>
> Возвращает: `PersistStorage`

Эта вспомогательная функция позволяет создать объект [`storage`](#storage), что полезно, когда вы хотите использовать пользовательский механизм хранения.

`getStorage` - это функция, которая возвращает механизм хранения со свойствами `getItem`, `setItem` и `removeItem`.

`options` - это необязательный объект, который может быть использован для настройки сериализации и десериализации данных. `options.reviver` - это функция, которая передается в `JSON.parse` для десериализации данных. `options.replacer` - это функция, которая передается в `JSON.stringify` для сериализации данных.

```ts
import { createJSONStorage } from 'zustand/middleware';

const storage = createJSONStorage(() => sessionStorage, {
    reviver: (key, value) => {
        if (value && value.type === 'date') {
            return new Date(value);
        }
        return value;
    },
    replacer: (key, value) => {
        if (value instanceof Date) {
            return {
                type: 'date',
                value: value.toISOString(),
            };
        }
        return value;
    },
});
```

## Гидратация и асинхронные хранилища

Чтобы объяснить, в чем заключается "стоимость" асинхронных хранилищ, необходимо понять, что такое гидратация.

В двух словах, гидратация - это процесс извлечения сохраненного состояния из хранилища и слияния его с текущим состоянием.

Промежуточное ПО Persist выполняет два вида гидратации: синхронную и асинхронную. Если данное хранилище является синхронным (например, `localStorage`), гидратация будет выполняться синхронно. С другой стороны, если данное хранилище является асинхронным (например, `AsyncStorage`), гидратация будет выполняться асинхронно (шокирующе, я знаю!).

Но в чем подвох? При синхронном гидратировании хранилище Zustand уже будет гидратировано при его создании. При асинхронном увлажнении хранилище Zustand, напротив, будет увлажнено позже, в микрозадаче.

Почему это важно? Асинхронная гидратация может привести к неожиданному поведению. Например, если вы используете Zustand в приложении React, хранилище **не** будет гидратировано при начальном рендере. В случаях, когда ваше приложение зависит от сохраняемого значения при загрузке страницы, вы можете захотеть подождать, пока хранилище будет гидратировано, прежде чем показывать что-либо. Например, ваше приложение может думать, что пользователь не вошел в систему, потому что так принято по умолчанию, но на самом деле хранилище еще не гидратировано.

Если ваше приложение зависит от сохраненного состояния при загрузке страницы, смотрите [_Как я могу проверить, было ли мое хранилище гидратировано_](#how-can-i-check-if-my-store-has-been-hydrated) в разделе [FAQ](#faq) ниже.

### Использование в Next.js

NextJS использует Server Side Rendering, и он будет сравнивать рендеринг компонента на сервере с рендерингом на клиенте. Но поскольку вы используете данные из браузера для изменения компонента, два рендера будут отличаться, и Next выдаст вам предупреждение.

Обычно ошибки выглядят следующим образом:

-   Текстовое содержимое не соответствует HTML, отрендеренному на сервере
-   Гидратация не удалась, потому что исходный пользовательский интерфейс не соответствует тому, что было отрисовано на сервере
-   Во время гидрирования произошла ошибка. Поскольку ошибка произошла за пределами границы Suspense, весь корень переключится на клиентский рендеринг.

Чтобы устранить эти ошибки, создайте пользовательский хук, чтобы Zustand немного подождал перед изменением компонентов.

Создайте файл со следующими параметрами:

```ts
// useStore.ts
import { useState, useEffect } from 'react';

const useStore = <T, F>(
    store: (callback: (state: T) => unknown) => unknown,
    callback: (state: T) => F
) => {
    const result = store(callback) as F;
    const [data, setData] = useState<F>();

    useEffect(() => {
        setData(result);
    }, [result]);

    return data;
};

export default useStore;
```

Теперь на своих страницах вы будете использовать хук немного по-другому:

```ts
// useBearStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// the store itself does not need any change
export const useBearStore = create(
    persist(
        (set, get) => ({
            bears: 0,
            addABear: () => set({ bears: get().bears + 1 }),
        }),
        {
            name: 'food-storage',
        }
    )
);
```

```ts
// yourComponent.tsx

import useStore from './useStore';
import { useBearStore } from './stores/useBearStore';

const bears = useStore(
    useBearStore,
    (state) => state.bears
);
```

Кредиты: [Этот ответ на вопрос](https://github.com/pmndrs/zustand/issues/938#issuecomment-1481801942), который указывает на [эту запись в блоге](https://dev.to/abdulsamad/how-to-use-zustands-persist-middleware-in-nextjs-4lb5).

## FAQ

### Как я могу проверить, было ли мое хранилище увлажнено

Есть несколько различных способов сделать это.

Вы можете использовать функцию-слушатель [`onRehydrateStorage`](#onrehydratestorage) для обновления поля в хранилище:

```ts
const useBoundStore = create(
  persist(
    (set, get) => ({
      // ...
      _hasHydrated: false,
      setHasHydrated: (state) => {
        set({
          _hasHydrated: state
        });
      }
    }),
    {
      // ...
      onRehydrateStorage: () => (state) => {
        state.setHasHydrated(true)
      }
    }
  )
);

export default function App() {
  const hasHydrated = useBoundStore(state => state._hasHydrated);

  if (!hasHydrated) {
    return <p>Loading...</p>
  }

  return (
    // ...
  );
}
```

Вы также можете создать собственный хук `useHydration`:

```ts
const useBoundStore = create(persist(...))

const useHydration = () => {
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    // Note: This is just in case you want to take into account manual rehydration.
    // You can remove the following line if you don't need it.
    const unsubHydrate = useBoundStore.persist.onHydrate(() => setHydrated(false))

    const unsubFinishHydration = useBoundStore.persist.onFinishHydration(() => setHydrated(true))

    setHydrated(useBoundStore.persist.hasHydrated())

    return () => {
      unsubHydrate()
      unsubFinishHydration()
    }
  }, [])

  return hydrated
}
```

### Как я могу использовать пользовательский механизм хранения данных

Если хранилище, которое вы хотите использовать, не соответствует ожидаемому API, вы можете создать собственное хранилище:

```ts
import { create } from 'zustand';
import {
    persist,
    createJSONStorage,
    StateStorage,
} from 'zustand/middleware';
import { get, set, del } from 'idb-keyval'; // can use anything: IndexedDB, Ionic Storage, etc.

// Custom storage object
const storage: StateStorage = {
    getItem: async (
        name: string
    ): Promise<string | null> => {
        console.log(name, 'has been retrieved');
        return (await get(name)) || null;
    },
    setItem: async (
        name: string,
        value: string
    ): Promise<void> => {
        console.log(
            name,
            'with value',
            value,
            'has been saved'
        );
        await set(name, value);
    },
    removeItem: async (name: string): Promise<void> => {
        console.log(name, 'has been deleted');
        await del(name);
    },
};

export const useBoundStore = create(
    persist(
        (set, get) => ({
            bears: 0,
            addABear: () => set({ bears: get().bears + 1 }),
        }),
        {
            name: 'food-storage', // unique name
            storage: createJSONStorage(() => storage),
        }
    )
);
```

Если вы используете тип, который `JSON.stringify()` не поддерживает, вам придется написать свой собственный код сериализации/десериализации. Однако, если это утомительно, вы можете использовать сторонние библиотеки для сериализации и десериализации различных типов данных.

Например, [Superjson](https://github.com/blitz-js/superjson) может сериализовать данные вместе с их типом, позволяя при десериализации вернуть их к исходному типу

```ts
import superjson from 'superjson'; //  can use anything: serialize-javascript, devalue, etc.
import { PersistStorage } from 'zustand/middleware';

interface BearState {
    bear: Map<string, string>;
    fish: Set<string>;
    time: Date;
    query: RegExp;
}

const storage: PersistStorage<BearState> = {
    getItem: (name) => {
        const str = localStorage.getItem(name);
        if (!str) return null;
        return superjson.parse(str);
    },
    setItem: (name, value) => {
        localStorage.setItem(
            name,
            superjson.stringify(value)
        );
    },
    removeItem: (name) => localStorage.removeItem(name),
};

const initialState: BearState = {
    bear: new Map(),
    fish: new Set(),
    time: new Date(),
    query: new RegExp(''),
};

export const useBearStore = create<BearState>()(
    persist(
        (set) => ({
            ...initialState,
            // ...
        }),
        {
            name: 'food-storage',
            storage,
        }
    )
);
```

### Как я могу регидратировать по событию хранения

Вы можете использовать Persist API для создания собственной реализации, подобной приведенному ниже примеру:

```ts
type StoreWithPersist = Mutate<StoreApi<State>, [["zustand/persist", unknown]]>

export const withStorageDOMEvents = (store: StoreWithPersist) => {
  const storageEventCallback = (e: StorageEvent) => {
    if (e.key === store.persist.getOptions().name && e.newValue) {
      store.persist.rehydrate()
    }
  }

  window.addEventListener('storage', storageEventCallback)

  return () => {
    window.removeEventListener('storage', storageEventCallback)
  }
}

const useBoundStore = create(persist(...))
withStorageDOMEvents(useBoundStore)
```

### Как использовать его с TypeScript

Базовое использование в TypeScript не требует ничего особенного, кроме написания `create<State>()(...)` вместо `create(...)`.

```tsx
import { create } from 'zustand';
import {
    persist,
    createJSONStorage,
} from 'zustand/middleware';

interface MyState {
    bears: number;
    addABear: () => void;
}

export const useBearStore = create<MyState>()(
    persist(
        (set, get) => ({
            bears: 0,
            addABear: () => set({ bears: get().bears + 1 }),
        }),
        {
            name: 'food-storage', // name of item in the storage (must be unique)
            storage: createJSONStorage(
                () => sessionStorage
            ), // (optional) by default the 'localStorage' is used
            partialize: (state) => ({ bears: state.bears }),
        }
    )
);
```

### Как использовать его с Map и Set

Чтобы сохранить такие типы объектов, как `Map` и `Set`, их необходимо преобразовать в JSON-сериализуемые типы, такие как `Array`, что можно сделать, определив пользовательский движок `storage`.

Допустим, ваше состояние использует `Map` для обработки списка `transactions`, тогда вы можете преобразовать `Map` в `Array` в свойстве `storage`, которое показано ниже:

```ts
interface BearState {
  // .
  // .
  // .
  transactions: Map<any>
}

  storage: {
    getItem: (name) => {
      const str = localStorage.getItem(name);
      if (!str) return null;
      const { state } = JSON.parse(str);
      return {
        state: {
          ...state,
          transactions: new Map(state.transactions),
        },
      }
    },
    setItem: (name, newValue: StorageValue<BearState>) => {
      // functions cannot be JSON encoded
      const str = JSON.stringify({
        state: {
          ...newValue.state,
          transactions: Array.from(newValue.state.transactions.entries()),
        },
      })
      localStorage.setItem(name, str)
    },
    removeItem: (name) => localStorage.removeItem(name),
  },
```

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/integrations/persisting-store-data></small>
