# Руководство по TypeScript

## Базовое использование

Разница при использовании TypeScript заключается в том, что вместо того, чтобы писать `create(...)`, вы должны писать `create<T>()(...)` (обратите внимание на дополнительные скобки `()` вместе с параметром type), где `T` - это тип состояния, которое нужно аннотировать. Например:

```ts
import { create } from 'zustand';

interface BearState {
    bears: number;
    increase: (by: number) => void;
}

const useBearStore = create<BearState>()((set) => ({
    bears: 0,
    increase: (by) =>
        set((state) => ({ bears: state.bears + by })),
}));
```

!!!note "Почему мы не можем просто вывести тип из начального состояния?"

**TLDR**: Поскольку общее состояние `T` инвариантно.

Рассмотрим эту минимальную версию `create`:

```ts
declare const create: <T>(f: (get: () => T) => T) => T;

const x = create((get) => ({
    foo: 0,
    bar: () => get(),
}));
// `x` is inferred as `unknown` instead of
// interface X {
//   foo: number,
//   bar: () => X
// }
```

Здесь, если вы посмотрите на тип `f` в `create`, то есть `(get: () => T) => T`, он "дает" `T` через return (делая его ковариантным), но он также "берет" `T` через `get` (делая его контравариантным). "Так откуда же берется `T`?" задается вопросом TypeScript. Это похоже на проблему курицы или яйца. В конце концов TypeScript сдается и выводит `T` как `unknown`.

Таким образом, до тех пор, пока родовое понятие, которое нужно вывести, является инвариантным (то есть как ковариантным, так и контравариантным), TypeScript не сможет его вывести. Другим простым примером может быть следующий:

```ts
const createFoo = {} as <T>(f: (t: T) => T) => T;
const x = createFoo((_) => 'hello');
```

Здесь снова `x` - это `unknown`, а не `string`.

Подробнее о выводе (только для тех, кто интересуется TypeScript)

В каком-то смысле этот сбой в выводе не является проблемой, потому что значение типа `<T>(f: (t: T) => T) => T` не может быть записано. То есть вы не можете написать реальную реализацию `createFoo`. Давайте попробуем это сделать:

```js
const createFoo = (f) => f(/* ? */);
```

`createFoo` должен вернуть возвращаемое значение `f`. Для этого сначала нужно вызвать `f`. А для вызова нам нужно передать значение типа `T`. А чтобы передать значение типа `T`, его нужно сначала произвести. Но как мы можем получить значение типа `T`, если мы даже не знаем, что такое `T`? Единственный способ произвести значение типа `T` - это вызвать `f`, но тогда для вызова самого `f` нам нужно значение типа `T`. Таким образом, вы видите, что на самом деле невозможно написать `createFoo`.

Итак, мы говорим, что сбой вывода в случае `createFoo` на самом деле не является проблемой, потому что реализовать `createFoo` невозможно. Но как насчет сбоя в выводах в случае `create`? Это тоже не проблема, потому что реализовать `create` тоже невозможно. Минуточку, если невозможно реализовать `create`, то как же тогда Zustand реализует его? Ответ заключается в том, что никак.

Zustand лжет, что он реализовал тип `create`, но он реализовал только большую его часть. Вот простое доказательство, демонстрирующее несостоятельность. Рассмотрим следующий код:

```ts
import { create } from 'zustand';

const useBoundStore = create<{ foo: number }>()(
    (_, get) => ({
        foo: get().foo,
    })
);
```

Этот код компилируется. Но если мы запустим его, то получим исключение: "Uncaught TypeError: Cannot read properties of undefined (reading 'foo')". Это происходит потому, что `get` вернет `undefined` до того, как будет создано начальное состояние (следовательно, вы не должны вызывать `get` при создании начального состояния). Типы обещают, что `get` никогда не будет возвращать `undefined`, но изначально он возвращает, а значит, Zustand не смог реализовать его.

И, конечно, Zustand потерпел неудачу, потому что невозможно реализовать `create` так, как обещают типы (точно так же, как невозможно реализовать `createFoo`). Другими словами, у нас нет типа для выражения фактического `create`, который мы реализовали. Мы не можем определить тип `get` как `() => T | undefined`, потому что это вызовет неудобства, и это все равно будет неправильно, так как `get` действительно `() => T` в конечном счете, просто при синхронном вызове это будет `() => undefined`. Нам нужна какая-то функция TypeScript, которая позволит нам набирать `get` как `(() => T) & WhenSync<() => undefined>`, что, конечно, крайне надуманно.

Таким образом, у нас есть две проблемы: отсутствие умозаключений и несостоятельность. Отсутствие выводов можно решить, если TypeScript улучшит свои выводы для инвариантов. А несостоятельность можно решить, если TypeScript введет что-то вроде `WhenSync`. Чтобы обойти недостаток инференции, мы вручную аннотируем тип состояния. И мы не можем обойти проблему несостоятельности, но это не так важно, потому что это не так уж и много, вызов `get` синхронно в любом случае не имеет смысла.

---

!!!note "К чему эти кривляния `()(...)`?"

**TLDR**: Это обходной путь для [microsoft/TypeScript#10571](https://github.com/microsoft/TypeScript/issues/10571).

Представьте, что у вас есть такой сценарий:

```ts
declare const withError: <T, E>(
    p: Promise<T>
) => Promise<
    | [error: undefined, value: T]
    | [error: E, value: undefined]
>;
declare const doSomething: () => Promise<string>;

const main = async () => {
    let [error, value] = await withError(doSomething());
};
```

Здесь `T` предположительно является `string`, а `E` предположительно является `unknown`. Возможно, вы захотите аннотировать `E` как `Foo`, потому что вы уверены в том, какую форму ошибки выкинет `doSomething()`. Однако вы не можете этого сделать. Вы можете передать либо все дженерики, либо ни одного. Наряду с аннотацией `E` как `Foo`, вам также придется аннотировать `T` как `string`, хотя он все равно будет инферирован. Решение состоит в том, чтобы сделать curried-версию `withError`, которая ничего не делает во время выполнения. Ее цель - просто позволить вам аннотировать `E`.

```ts
declare const withError: {
    <E>(): <T>(
        p: Promise<T>
    ) => Promise<
        | [error: undefined, value: T]
        | [error: E, value: undefined]
    >;
    <T, E>(p: Promise<T>): Promise<
        | [error: undefined, value: T]
        | [error: E, value: undefined]
    >;
};
declare const doSomething: () => Promise<string>;
interface Foo {
    bar: string;
}

const main = async () => {
    let [error, value] = await withError<Foo>()(
        doSomething()
    );
};
```

Таким образом, `T` будет инферироваться, а вы сможете аннотировать `E`. Zustand имеет тот же случай использования, когда мы хотим аннотировать состояние (первый параметр типа), но позволяем другим параметрам быть инферированными.

---

В качестве альтернативы можно также использовать `combine`, который выдает состояние так, что вам не нужно его вводить.

```ts
import { create } from 'zustand';
import { combine } from 'zustand/middleware';

const useBearStore = create(
    combine({ bears: 0 }, (set) => ({
        increase: (by: number) =>
            set((state) => ({ bears: state.bears + by })),
    }))
);
```

!!!note "Будьте осторожны"

Мы достигаем этого вывода, немного солгав в типах `set`, `get` и `store`, которые вы получаете в качестве параметров. Ложь заключается в том, что они типизированы так, как будто состояние - это первый параметр, когда на самом деле состояние - это неглубокое слияние (`{ ...a, ...b }`) как первого параметра, так и возврата второго параметра. Например, `get` от второго параметра имеет тип `() => { bears: number }`, что является ложью, так как должно быть `() => { bears: number, increase: (by: number) => void }`. А `useBearStore` по-прежнему имеет правильный тип; например, `useBearStore.getState` имеет тип `() => { bears: number, increase: (by: number) => void }`.

На самом деле это не ложь, потому что `{ bears: number }` все равно является подтипом `{ bears: number, increase: (by: number) => void }`. Поэтому в большинстве случаев проблем не возникнет. Просто следует быть осторожным при использовании replace. Например, `set({ bears: 0 }, true)` скомпилируется, но будет некорректным, так как удалит функцию `increase`. Еще один случай, когда следует быть осторожным, - это использование `Object.keys`. `Object.keys(get())` вернет `["bears", "increase"]`, а не `["bears"]`. Тип возврата `get` может привести к подобным ошибкам.

`combine` обменивает немного безопасности типов на удобство, заключающееся в отсутствии необходимости писать тип для состояния. Следовательно, вы должны использовать `combine` соответствующим образом. В большинстве случаев она работает нормально, и вы можете использовать ее с удобством.

---

Обратите внимание, что мы не используем curried-версию при использовании `combine`, потому что `combine` "создает" состояние. При использовании промежуточного ПО, которое создает состояние, нет необходимости использовать curried-версию, потому что состояние теперь можно вывести. Другим промежуточным ПО, создающим состояние, является `redux`. Поэтому при использовании `combine`, `redux` или любого другого пользовательского промежуточного ПО, создающего состояние, мы не рекомендуем использовать curried-версию.

## Использование промежуточного ПО

Чтобы использовать промежуточные модули в TypeScript, не нужно делать ничего особенного.

```ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface BearState {
    bears: number;
    increase: (by: number) => void;
}

const useBearStore = create<BearState>()(
    devtools(
        persist(
            (set) => ({
                bears: 0,
                increase: (by) =>
                    set((state) => ({
                        bears: state.bears + by,
                    })),
            }),
            { name: 'bearStore' }
        )
    )
);
```

Просто убедитесь, что вы используете их непосредственно внутри `create`, чтобы контекстное заключение работало. Для того чтобы сделать что-то даже отдаленно похожее на следующие `myMiddlewares`, потребуются более продвинутые типы.

```ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

const myMiddlewares = (f) =>
    devtools(persist(f, { name: 'bearStore' }));

interface BearState {
    bears: number;
    increase: (by: number) => void;
}

const useBearStore = create<BearState>()(
    myMiddlewares((set) => ({
        bears: 0,
        increase: (by) =>
            set((state) => ({ bears: state.bears + by })),
    }))
);
```

Кроме того, мы рекомендуем использовать промежуточное ПО `devtools` как можно реже. Например, когда вы используете его с `immer` в качестве промежуточного ПО, это должно быть `devtools(immer(...))`, а не `immer(devtools(...))`. Это связано с тем, что `devtools` мутирует `setState` и добавляет к нему параметр типа, который может быть потерян, если другие промежуточные программы (например, `immer`) также мутируют `setState` перед `devtools`. Поэтому использование `devtools` в конце гарантирует, что никакие промежуточные программы не будут мутировать `setState` до него.

## Авторские промежуточные модули и расширенное использование

Представьте, что вам нужно написать следующее гипотетическое промежуточное ПО.

```ts
import { create } from 'zustand';

const foo = (f, bar) => (set, get, store) => {
    store.foo = bar;
    return f(set, get, store);
};

const useBearStore = create(
    foo(() => ({ bears: 0 }), 'hello')
);
console.log(useBearStore.foo.toUpperCase());
```

Посреднические программы Zustand могут мутировать хранилище. Но как мы можем закодировать мутацию на уровне типов? То есть как мы можем набрать `foo` так, чтобы этот код компилировался?

Для обычного статически типизированного языка это невозможно. Но благодаря TypeScript в Zustand появилось так называемый "мутатор высшего рода", который делает это возможным. Если вы имеете дело со сложными проблемами типов, такими как типизация промежуточного программного обеспечения или использование типа `StateCreator`, вам придется разобраться в этой детали реализации. Для этого вы можете [посмотреть #710](https://github.com/pmndrs/zustand/issues/710).

Если вам не терпится узнать, каков ответ на эту конкретную проблему, то вы можете [посмотреть здесь](#middleware-that-changes-the-store-type).

## Общие рецепты

### Middleware, которое не меняет тип хранилища

```ts
import {
    create,
    State,
    StateCreator,
    StoreMutatorIdentifier,
} from 'zustand';

type Logger = <
    T extends State,
    Mps extends [StoreMutatorIdentifier, unknown][] = [],
    Mcs extends [StoreMutatorIdentifier, unknown][] = []
>(
    f: StateCreator<T, Mps, Mcs>,
    name?: string
) => StateCreator<T, Mps, Mcs>;

type LoggerImpl = <T extends State>(
    f: StateCreator<T, [], []>,
    name?: string
) => StateCreator<T, [], []>;

const loggerImpl: LoggerImpl = (f, name) => (
    set,
    get,
    store
) => {
    type T = ReturnType<typeof f>;
    const loggedSet: typeof set = (...a) => {
        set(...a);
        console.log(...(name ? [`${name}:`] : []), get());
    };
    const setState = store.setState;
    store.setState = (...a) => {
        setState(...a);
        console.log(
            ...(name ? [`${name}:`] : []),
            store.getState()
        );
    };

    return f(loggedSet, get, store);
};

export const logger = (loggerImpl as unknown) as Logger;

// ---

const useBearStore = create<BearState>()(
    logger(
        (set) => ({
            bears: 0,
            increase: (by) =>
                set((state) => ({
                    bears: state.bears + by,
                })),
        }),
        'bear-store'
    )
);
```

### Middleware, изменяющее тип хранилища {#middleware-that-changes-the-store-type}

```ts
import {
    create,
    State,
    StateCreator,
    StoreMutatorIdentifier,
    Mutate,
    StoreApi,
} from 'zustand';

type Foo = <
    T extends State,
    A,
    Mps extends [StoreMutatorIdentifier, unknown][] = [],
    Mcs extends [StoreMutatorIdentifier, unknown][] = []
>(
    f: StateCreator<T, [...Mps, ['foo', A]], Mcs>,
    bar: A
) => StateCreator<T, Mps, [['foo', A], ...Mcs]>;

declare module 'zustand' {
    interface StoreMutators<S, A> {
        foo: Write<Cast<S, object>, { foo: A }>;
    }
}

type FooImpl = <T extends State, A>(
    f: StateCreator<T, [], []>,
    bar: A
) => StateCreator<T, [], []>;

const fooImpl: FooImpl = (f, bar) => (set, get, _store) => {
    type T = ReturnType<typeof f>;
    type A = typeof bar;

    const store = _store as Mutate<
        StoreApi<T>,
        [['foo', A]]
    >;
    store.foo = bar;
    return f(set, get, _store);
};

export const foo = (fooImpl as unknown) as Foo;

type Write<T extends object, U extends object> = Omit<
    T,
    keyof U
> &
    U;

type Cast<T, U> = T extends U ? T : U;

// ---

const useBearStore = create(
    foo(() => ({ bears: 0 }), 'hello')
);
console.log(useBearStore.foo.toUpperCase());
```

### `create` без использования curried обходного пути

Рекомендуемый способ использования `create` - это использование curried обходного пути, как показано ниже: `create<T>()(...)`. Это связано с тем, что так вы сможете определить тип хранилища. Но если по какой-то причине вы не хотите использовать это обходное решение, вы можете передать параметры типа следующим образом. Обратите внимание, что в некоторых случаях это работает как утверждение, а не аннотация, поэтому мы не рекомендуем это делать.

```ts
import { create } from "zustand"

interface BearState {
  bears: number
  increase: (by: number) => void
}

const useBearStore = create<
  BearState,
  [
    ['zustand/persist', BearState],
    ['zustand/devtools', never]
  ]
>(devtools(persist((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}), { name: 'bearStore' }))
```

### Slices паттерн

```ts
import { create, StateCreator } from 'zustand';

interface BearSlice {
    bears: number;
    addBear: () => void;
    eatFish: () => void;
}

interface FishSlice {
    fishes: number;
    addFish: () => void;
}

interface SharedSlice {
    addBoth: () => void;
    getBoth: () => void;
}

const createBearSlice: StateCreator<
    BearSlice & FishSlice,
    [],
    [],
    BearSlice
> = (set) => ({
    bears: 0,
    addBear: () =>
        set((state) => ({ bears: state.bears + 1 })),
    eatFish: () =>
        set((state) => ({ fishes: state.fishes - 1 })),
});

const createFishSlice: StateCreator<
    BearSlice & FishSlice,
    [],
    [],
    FishSlice
> = (set) => ({
    fishes: 0,
    addFish: () =>
        set((state) => ({ fishes: state.fishes + 1 })),
});

const createSharedSlice: StateCreator<
    BearSlice & FishSlice,
    [],
    [],
    SharedSlice
> = (set, get) => ({
    addBoth: () => {
        // you can reuse previous methods
        get().addBear();
        get().addFish();
        // or do them from scratch
        // set((state) => ({ bears: state.bears + 1, fishes: state.fishes + 1 })
    },
    getBoth: () => get().bears + get().fishes,
});

const useBoundStore = create<
    BearSlice & FishSlice & SharedSlice
>()((...a) => ({
    ...createBearSlice(...a),
    ...createFishSlice(...a),
    ...createSharedSlice(...a),
}));
```

Подробное объяснение шаблона slices можно найти [здесь](./slices-pattern.md).

Если у вас есть некоторые промежуточные модули, то замените `StateCreator<MyState, [], [], MySlice>` на `StateCreator<MyState, Mutators, [], MySlice>`. Например, если вы используете `devtools`, то это будет `StateCreator<MyState, [["zustand/devtools", never]], [], MySlice>`. Список всех мутаторов смотрите в разделе ["Middlewares и ссылки на их мутаторы"](#middlewares-and-their-mutators-reference).

### Ограниченный хук `useStore` для ванильных хранилищ

```ts
import { useStore } from 'zustand';
import { createStore } from 'zustand/vanilla';

interface BearState {
    bears: number;
    increase: (by: number) => void;
}

const bearStore = createStore<BearState>()((set) => ({
    bears: 0,
    increase: (by) =>
        set((state) => ({ bears: state.bears + by })),
}));

function useBearStore(): BearState;
function useBearStore<T>(
    selector: (state: BearState) => T
): T;
function useBearStore<T>(
    selector?: (state: BearState) => T
) {
    return useStore(bearStore, selector!);
}
```

Вы также можете сделать абстрактную функцию `createBoundedUseStore`, если вам нужно часто создавать ограниченные хуки `useStore`, и вы хотите, чтобы все было более рационально...

```ts
import { useStore, StoreApi } from 'zustand';
import { createStore } from 'zustand/vanilla';

interface BearState {
    bears: number;
    increase: (by: number) => void;
}

const bearStore = createStore<BearState>()((set) => ({
    bears: 0,
    increase: (by) =>
        set((state) => ({ bears: state.bears + by })),
}));

const createBoundedUseStore = ((store) => (selector) =>
    useStore(store)) as <S extends StoreApi<unknown>>(
    store: S
) => {
    (): ExtractState<S>;
    <T>(selector: (state: ExtractState<S>) => T): T;
};

type ExtractState<S> = S extends { getState: () => infer X }
    ? X
    : never;

const useBearStore = createBoundedUseStore(bearStore);
```

## Middlewares и ссылки на их мутаторы {#middlewares-and-their-mutators-reference}

-   `devtools` — `["zustand/devtools", never]`
-   `persist` — `["zustand/persist", YourPersistedState]` `YourPersistedState` is тип состояния, которое вы собираетесь сохранять, т.е. возвращаемый тип `options.partialize`, если вы не передаете `partialize` опции, то `YourPersistedState` становится `Partial<YourState>`. Также [иногда](https://github.com/pmndrs/zustand/issues/980#issuecomment-1162289836) передача фактического `PersistedState` не работает. В таких случаях попробуйте передать `unknown`.
-   `immer` — `["zustand/immer", never]`
-   `subscribeWithSelector` — `["zustand/subscribeWithSelector", never]`
-   `redux` — `["zustand/redux", YourAction]`
-   `combine` - нет мутатора, так как `combine` не мутирует хранилище

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/typescript></small>
