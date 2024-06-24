# Настройка с Next.js

[Next.js](https://nextjs.org) - популярный серверный фреймворк рендеринга для React, который представляет некоторые уникальные проблемы для правильного использования Zustand. Помните, что хранилище Zustand является глобальной переменной (AKA состояние модуля), что делает необязательным использование `контекста`. К этим проблемам относятся:

-   **Хранилище для каждого запроса:** Сервер Next.js может обрабатывать несколько запросов одновременно. Это означает, что хранилище должно создаваться для каждого запроса и не должно быть общим для всех запросов.
-   **SSR friendly:** Приложения Next.js отображаются дважды: сначала на сервере, а затем на клиенте. Наличие разных выводов на клиенте и сервере приведет к "ошибкам гидрации". Чтобы избежать этого, хранилище необходимо инициализировать на сервере, а затем повторно инициализировать на клиенте с теми же данными. Подробнее об этом читайте в нашем руководстве [SSR и гидратация](./ssr-and-hydration.md).
-   **SPA-маршрутизация:** Next.js поддерживает гибридную модель маршрутизации на стороне клиента, что означает, что для сброса хранилища нам нужно инициализировать его на уровне компонента с помощью `Context`.
-   **Благодаря серверному кэшированию:** Последние версии Next.js (в частности, приложения, использующие архитектуру App Router) поддерживают агрессивное серверное кэширование. Поскольку наше хранилище является **модулем состояния**, оно полностью совместимо с этим кэшированием.

У нас есть следующие общие рекомендации по правильному использованию Zustand:

-   **Нет глобальных хранилищ** - Поскольку хранилище не должно быть общим для всех запросов, его не следует определять как глобальную переменную. Вместо этого хранилище должно создаваться для каждого запроса.
-   **Серверные компоненты React не должны читать из хранилища или записывать в него** - RSC не могут использовать хуки или контекст. Они не предназначены для работы с состоянием. Если RSC читает или записывает значения в глобальное хранилище, это нарушает архитектуру Next.js.

## Создание хранилища для каждого запроса

Давайте напишем функцию фабрики хранилищ, которая будет создавать новое хранилище для каждого запроса.

```json
// tsconfig.json
{
    "compilerOptions": {
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "noEmit": true,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve",
        "incremental": true,
        "plugins": [
            {
                "name": "next"
            }
        ],
        "paths": {
            "@/*": ["./src/*"]
        }
    },
    "include": [
        "next-env.d.ts",
        "**/*.ts",
        "**/*.tsx",
        ".next/types/**/*.ts"
    ],
    "exclude": ["node_modules"]
}
```

> **Примечание:** не забудьте удалить все комментарии из файла `tsconfig.json`.

```ts
// src/stores/counter-store.ts
import { createStore } from 'zustand/vanilla';

export type CounterState = {
    count: number;
};

export type CounterActions = {
    decrementCount: () => void;
    incrementCount: () => void;
};

export type CounterStore = CounterState & CounterActions;

export const defaultInitState: CounterState = {
    count: 0,
};

export const createCounterStore = (
    initState: CounterState = defaultInitState
) => {
    return createStore<CounterStore>()((set) => ({
        ...initState,
        decrementCount: () =>
            set((state) => ({ count: state.count - 1 })),
        incrementCount: () =>
            set((state) => ({ count: state.count + 1 })),
    }));
};
```

## Предоставление хранилища

Давайте используем `createCounterStore` в нашем компоненте и поделимся им с помощью контекстного провайдера.

```tsx
// src/providers/counter-store-provider.tsx
'use client'

import { type ReactNode, createContext, useRef, useContext } from 'react'
import { useStore } from 'zustand'

import { type CounterStore, createCounterStore } from '@/stores/counter-store'

export type CounterStoreApi = ReturnType<typeof createCounterStore>

export const CounterStoreContext = createContext<CounterStoreApi | undefined>(
  undefined,
)

export interface CounterStoreProviderProps {
  children: ReactNode
}

export const CounterStoreProvider = ({
  children,
}: CounterStoreProviderProps) => {
  const storeRef = useRef<CounterStoreApi>()
  if (!storeRef.current) {
    storeRef.current = createCounterStore()
  }

  return (
    <CounterStoreContext.Provider value={storeRef.current}>
      {children}
    </CounterStoreContext.Provider>
  )
}

export const useCounterStore = <T,>(
  selector: (store: CounterStore) => T,
): T => {
  const counterStoreContext = useContext(CounterStoreContext)

  if (!counterStoreContext) {
    throw new Error(`useCounterStore must be used within CounterStoreProvider`)
  }

  return useStore(counterStoreContext, selector)
}
```

> **Примечание:** В этом примере мы гарантируем, что этот компонент безопасен для повторного рендеринга, проверяя значение ссылки, так что хранилище создается только один раз. Этот компонент будет отображаться только один раз за запрос на сервере, но может быть перерисован несколько раз на клиенте, если выше этого компонента в дереве расположены клиентские компоненты с изменяемым состоянием, или если этот компонент содержит другое изменяемое состояние, вызывающее повторное отображение.

## Инициализация хранилища

```ts
// src/stores/counter-store.ts
import { createStore } from 'zustand/vanilla';

export type CounterState = {
    count: number;
};

export type CounterActions = {
    decrementCount: () => void;
    incrementCount: () => void;
};

export type CounterStore = CounterState & CounterActions;

export const initCounterStore = (): CounterState => {
    return { count: new Date().getFullYear() };
};

export const defaultInitState: CounterState = {
    count: 0,
};

export const createCounterStore = (
    initState: CounterState = defaultInitState
) => {
    return createStore<CounterStore>()((set) => ({
        ...initState,
        decrementCount: () =>
            set((state) => ({ count: state.count - 1 })),
        incrementCount: () =>
            set((state) => ({ count: state.count + 1 })),
    }));
};
```

```tsx
// src/providers/counter-store-provider.tsx
'use client'

import { type ReactNode, createContext, useRef, useContext } from 'react'
import { useStore } from 'zustand'

import {
  type CounterStore,
  createCounterStore,
  initCounterStore,
} from '@/stores/counter-store'

export type CounterStoreApi = ReturnType<typeof createCounterStore>

export const CounterStoreContext = createContext<CounterStoreApi | undefined>(
  undefined,
)

export interface CounterStoreProviderProps {
  children: ReactNode
}

export const CounterStoreProvider = ({
  children,
}: CounterStoreProviderProps) => {
  const storeRef = useRef<CounterStoreApi>()
  if (!storeRef.current) {
    storeRef.current = createCounterStore(initCounterStore())
  }

  return (
    <CounterStoreContext.Provider value={storeRef.current}>
      {children}
    </CounterStoreContext.Provider>
  )
}

export const useCounterStore = <T,>(
  selector: (store: CounterStore) => T,
): T => {
  const counterStoreContext = useContext(CounterStoreContext)

  if (!counterStoreContext) {
    throw new Error(`useCounterStore must be used within CounterStoreProvider`)
  }

  return useStore(counterStoreContext, selector)
}
```

## Использование хранилища в различных архитектурах

Существует две архитектуры для приложения Next.js: [Pages Router](https://nextjs.org/docs/pages/building-your-application/routing) и [App Router](https://nextjs.org/docs/app/building-your-application/routing). Использование Zustand в обеих архитектурах должно быть одинаковым с небольшими различиями, связанными с каждой архитектурой.

### Pages Router

```tsx
// src/components/pages/home-page.tsx
import { useCounterStore } from '@/providers/counter-store-provider.ts';

export const HomePage = () => {
    const {
        count,
        incrementCount,
        decrementCount,
    } = useCounterStore((state) => state);

    return (
        <div>
            Count: {count}
            <hr />
            <button
                type="button"
                onClick={() => void incrementCount()}
            >
                Increment Count
            </button>
            <button
                type="button"
                onClick={() => void decrementCount()}
            >
                Decrement Count
            </button>
        </div>
    );
};
```

```tsx
// src/_app.tsx
import type { AppProps } from 'next/app';

import { CounterStoreProvider } from '@/providers/counter-store-provider.tsx';

export default function App({
    Component,
    pageProps,
}: AppProps) {
    return (
        <CounterStoreProvider>
            <Component {...pageProps} />
        </CounterStoreProvider>
    );
}
```

```tsx
// src/pages/index.tsx
import { HomePage } from '@/components/pages/home-page.tsx';

export default function Home() {
    return <HomePage />;
}
```

> **Примечание:** создание хранилища для каждого маршрута потребует создания и совместного использования хранилища на уровне компонентов страницы (маршрута). Старайтесь не использовать эту функцию, если вам не нужно создавать хранилище для каждого маршрута.

```tsx
// src/pages/index.tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider.tsx';
import { HomePage } from '@/components/pages/home-page.tsx';

export default function Home() {
    return (
        <CounterStoreProvider>
            <HomePage />
        </CounterStoreProvider>
    );
}
```

### App Router

```tsx
// src/components/pages/home-page.tsx
'use client';

import { useCounterStore } from '@/providers/counter-store-provider';

export const HomePage = () => {
    const {
        count,
        incrementCount,
        decrementCount,
    } = useCounterStore((state) => state);

    return (
        <div>
            Count: {count}
            <hr />
            <button
                type="button"
                onClick={() => void incrementCount()}
            >
                Increment Count
            </button>
            <button
                type="button"
                onClick={() => void decrementCount()}
            >
                Decrement Count
            </button>
        </div>
    );
};
```

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

import { CounterStoreProvider } from '@/providers/counter-store-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Create Next App',
    description: 'Generated by create next app',
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <CounterStoreProvider>
                    {children}
                </CounterStoreProvider>
            </body>
        </html>
    );
}
```

```tsx
// src/app/page.tsx
import { HomePage } from '@/components/pages/home-page';

export default function Home() {
    return <HomePage />;
}
```

> **Примечание:** создание хранилища для каждого маршрута потребует создания и совместного использования хранилища на уровне компонентов страницы (маршрута). Старайтесь не использовать эту функцию, если вам не нужно создавать хранилище для каждого маршрута.

```tsx
// src/app/page.tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider';
import { HomePage } from '@/components/pages/home-page';

export default function Home() {
    return (
        <CounterStoreProvider>
            <HomePage />
        </CounterStoreProvider>
    );
}
```

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/nextjs></small>
