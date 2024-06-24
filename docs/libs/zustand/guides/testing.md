---
description: Написание тестов
---

# Тестирование

## Настройка тестовой среды

## Программы запуска тестов

Обычно программа запуска тестов должна быть настроена на выполнение синтаксиса JavaScript/TypeScript. Если вы собираетесь тестировать компоненты пользовательского интерфейса, вам, вероятно, потребуется настроить программу для тестирования на использование JSDOM для создания имитации DOM-окружения.

Инструкции по настройке тестового прогона см. на этих ресурсах:

-   **Jest**
    -   [Jest: Getting Started](https://jestjs.io/docs/getting-started)
    -   [Jest: Configuration - Test Environment](https://jestjs.io/docs/configuration#testenvironment-string)
-   **Vitest**
    -   [Vitest: Getting Started](https://vitest.dev/guide)
    -   [Vitest: Конфигурация - тестовая среда](https://vitest.dev/config/#environment)

### Инструменты для тестирования пользовательского интерфейса и сети

**Мы рекомендуем использовать [React Testing Library (RTL)](https://testing-library.com/docs/react-testing-library/intro) для тестирования компонентов React, подключаемых к Zustand**. RTL - это простая и полная утилита для тестирования React DOM, которая поощряет хорошие практики тестирования. Она использует функцию `render` ReactDOM и `act` из `react-dom/tests-utils`. Кроме того, [Native Testing Library (RNTL)](https://testing-library.com/docs/react-native-testing-library/intro) - это альтернатива RTL для тестирования компонентов React Native. Семейство инструментов [Testing Library](https://testing-library.com/) также включает адаптеры для многих других популярных фреймворков.

Мы также рекомендуем использовать [Mock Service Worker (MSW)](https://mswjs.io/) для имитации сетевых запросов, так как это означает, что логику вашего приложения не нужно менять или имитировать при написании тестов.

-   **Библиотека тестирования реакций (DOM)**
    -   [DOM Testing Library: Setup](https://testing-library.com/docs/dom-testing-library/setup)
    -   [React Testing Library: Setup](https://testing-library.com/docs/react-testing-library/setup)
    -   [Библиотека тестирования Jest-DOM Matchers](https://testing-library.com/docs/ecosystem-jest-dom)
-   **Нативная библиотека тестирования (React Native)**
    -   [Native Testing Library: Setup](https://testing-library.com/docs/react-native-testing-library/setup)
-   **Библиотека тестирования пользовательских событий (DOM)**
    -   ["Библиотека тестирования пользовательских событий: настройка"](https://testing-library.com/docs/user-event/setup)
-   **TypeScript for Jest**
    -   [TypeScript для Jest: Установка](https://kulshekhar.github.io/ts-jest/docs/getting-started/installation)
-   **TypeScript для Node**
    -   [TypeScript для Node: Установка](https://typestrong.org/ts-node/docs/installation)
-   **Mock Service Worker**
    -   [MSW: Установка](https://mswjs.io/docs/getting-started/install)
    -   [MSW: Настройка имитационных запросов](https://mswjs.io/docs/getting-started/mocks/rest-api)
    -   [MSW: Конфигурация имитационного сервера для Node](https://mswjs.io/docs/getting-started/integrate/node)

## Настройка Zustand для тестирования

> **Примечание**: Поскольку Jest и Vitest имеют небольшие различия, например, Vitest использует **ES модули**, а Jest использует
> **CommonJS модули**, вам нужно иметь это в виду, если вы используете Vitest вместо Jest.

Макет, представленный ниже, позволит соответствующему тестовому прогону сбрасывать хранилища zustand после каждого теста.

### Общий код только для целей тестирования

Этот общий код был добавлен, чтобы избежать дублирования кода в нашем демо, поскольку мы используем одного и того же создателя хранилища для обеих реализаций, с API `Context` и без него - `createStore` и `create`, соответственно.

```ts
// shared/counter-store-creator.ts
import { type StateCreator } from 'zustand'

export type CounterStore = {
  count: number
  inc: () => void
}

export const counterStoreCreator: StateCreator<CounterStore> = (set) => ({
  count: 1,
  inc: () => set((state) => ({ count: state.count + 1 })),
})
```

### Jest

В следующих шагах мы настроим наше окружение Jest, чтобы использовать Zustand.

```ts
// __mocks__/zustand.ts
import * as zustand from 'zustand';
import { act } from '@testing-library/react';

const {
    create: actualCreate,
    createStore: actualCreateStore,
} = jest.requireActual<typeof zustand>('zustand');

// a variable to hold reset functions for all stores declared in the app
export const storeResetFns = new Set<() => void>();

const createUncurried = <T>(
    stateCreator: zustand.StateCreator<T>
) => {
    const store = actualCreate(stateCreator);
    const initialState = store.getInitialState();
    storeResetFns.add(() => {
        store.setState(initialState, true);
    });
    return store;
};

// when creating a store, we get its initial state, create a reset function and add it in the set
export const create = (<T>(
    stateCreator: zustand.StateCreator<T>
) => {
    console.log('zustand create mock');

    // to support curried version of create
    return typeof stateCreator === 'function'
        ? createUncurried(stateCreator)
        : createUncurried;
}) as typeof zustand.create;

const createStoreUncurried = <T>(
    stateCreator: zustand.StateCreator<T>
) => {
    const store = actualCreateStore(stateCreator);
    const initialState = store.getInitialState();
    storeResetFns.add(() => {
        store.setState(initialState, true);
    });
    return store;
};

// when creating a store, we get its initial state, create a reset function and add it in the set
export const createStore = (<T>(
    stateCreator: zustand.StateCreator<T>
) => {
    console.log('zustand createStore mock');

    // to support curried version of createStore
    return typeof stateCreator === 'function'
        ? createStoreUncurried(stateCreator)
        : createStoreUncurried;
}) as typeof zustand.createStore;

// reset all stores after each test run
afterEach(() => {
    act(() => {
        storeResetFns.forEach((resetFn) => {
            resetFn();
        });
    });
});
```

```ts
// setup-jest.ts
import '@testing-library/jest-dom';
```

```ts
// jest.config.ts
import type { JestConfigWithTsJest } from 'ts-jest';

const config: JestConfigWithTsJest = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['./setup-jest.ts'],
};

export default config;
```

> **Примечание**: для использования TypeScript нам необходимо установить два пакета `ts-jest` и `ts-node`.

### Vitest

В следующих шагах мы настроим наше окружение Vitest, чтобы выполнить имитацию Zustand.

> **Предупреждение:** В Vitest вы можете изменить [root](https://vitest.dev/config/#root). В связи с этим вам необходимо убедиться, что вы создаете каталог `__mocks__` в правильном месте. Допустим, вы изменили **root** на `./src`, это означает, что вам нужно создать директорию `__mocks__` в `./src`. В итоге получится `./src/__mocks__`, а не `./__mocks__`. Создание директории `__mocks__` в неправильном месте может привести к проблемам при использовании Vitest.

```ts
// __mocks__/zustand.ts
import * as zustand from 'zustand';
import { act } from '@testing-library/react';

const {
    create: actualCreate,
    createStore: actualCreateStore,
} = await vi.importActual<typeof zustand>('zustand');

// a variable to hold reset functions for all stores declared in the app
export const storeResetFns = new Set<() => void>();

const createUncurried = <T>(
    stateCreator: zustand.StateCreator<T>
) => {
    const store = actualCreate(stateCreator);
    const initialState = store.getInitialState();
    storeResetFns.add(() => {
        store.setState(initialState, true);
    });
    return store;
};

// when creating a store, we get its initial state, create a reset function and add it in the set
export const create = (<T>(
    stateCreator: zustand.StateCreator<T>
) => {
    console.log('zustand create mock');

    // to support curried version of create
    return typeof stateCreator === 'function'
        ? createUncurried(stateCreator)
        : createUncurried;
}) as typeof zustand.create;

const createStoreUncurried = <T>(
    stateCreator: zustand.StateCreator<T>
) => {
    const store = actualCreateStore(stateCreator);
    const initialState = store.getInitialState();
    storeResetFns.add(() => {
        store.setState(initialState, true);
    });
    return store;
};

// when creating a store, we get its initial state, create a reset function and add it in the set
export const createStore = (<T>(
    stateCreator: zustand.StateCreator<T>
) => {
    console.log('zustand createStore mock');

    // to support curried version of createStore
    return typeof stateCreator === 'function'
        ? createStoreUncurried(stateCreator)
        : createStoreUncurried;
}) as typeof zustand.createStore;

// reset all stores after each test run
afterEach(() => {
    act(() => {
        storeResetFns.forEach((resetFn) => {
            resetFn();
        });
    });
});
```

> **Примечание**: без включенной [globals configuration](https://vitest.dev/config/#globals) нам нужно добавить `import { afterEach, vi } из 'vitest'` в верхней части.

```ts
// global.d.ts
/// <reference types="vite/client" />
/// <reference types="vitest/globals" />
```

> **Примечание**: без включения [globals configuration](https://vitest.dev/config/#globals) необходимо удалить `/// <reference types="vitest/globals" />`.

```ts
// setup-vitest.ts
import '@testing-library/jest-dom';

vi.mock('zustand'); // to make it work like Jest (auto-mocking)
```

> **Примечание**: без включенной [globals configuration](https://vitest.dev/config/#globals) нам нужно добавить `import { vi } from 'vitest'` в верхней части.

```ts
// vitest.config.ts
import { defineConfig, mergeConfig } from 'vitest/config';
import viteConfig from './vite.config';

export default mergeConfig(
    viteConfig,
    defineConfig({
        test: {
            globals: true,
            environment: 'jsdom',
            setupFiles: ['./setup-vitest.ts'],
        },
    })
);
```

### Тестирование компонентов

В следующих примерах мы будем использовать `useCounterStore`

> **Примечание**: все эти примеры написаны с использованием TypeScript.

```ts
// stores/counter-store-creator.ts
import { type StateCreator } from 'zustand'

export type CounterStore = {
  count: number
  inc: () => void
}

export const counterStoreCreator: StateCreator<CounterStore> = (set) => ({
  count: 1,
  inc: () => set((state) => ({ count: state.count + 1 })),
})
```

---

```ts
// stores/user-counter-store.ts
import { create } from 'zustand'

import {
  type CounterStore,
  counterStoreCreator,
} from '../shared/counter-store-creator'

export const useCounterStore = create<CounterStore>()(counterStoreCreator)
```

---

```ts
// contexts/use-counter-store-context.tsx
import { type ReactNode, createContext, useContext, useRef } from 'react'
import { createStore } from 'zustand'
import { useStoreWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

import {
  type CounterStore,
  counterStoreCreator,
} from '../shared/counter-store-creator'

export const createCounterStore = () => {
  return createStore<CounterStore>(counterStoreCreator)
}

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
  const counterStoreRef = useRef<CounterStoreApi>()
  if (!counterStoreRef.current) {
    counterStoreRef.current = createCounterStore()
  }

  return (
    <CounterStoreContext.Provider value={counterStoreRef.current}>
      {children}
    </CounterStoreContext.Provider>
  )
}

export type UseCounterStoreContextSelector<T> = (store: CounterStore) => T

export const useCounterStoreContext = <T,>(
  selector: UseCounterStoreContextSelector<T>,
): T => {
  const counterStoreContext = useContext(CounterStoreContext)

  if (counterStoreContext === undefined) {
    throw new Error(
      'useCounterStoreContext must be used within CounterStoreProvider',
    )
  }

  return useStoreWithEqualityFn(counterStoreContext, selector, shallow)
}
```

---

```tsx
// components/counter/counter.tsx
import { useCounterStore } from '../../stores/use-counter-store';

export function Counter() {
    const { count, inc } = useCounterStore();

    return (
        <div>
            <h2>Counter Store</h2>
            <h4>{count}</h4>
            <button onClick={inc}>One Up</button>
        </div>
    );
}
```

---

```ts
// components/counter/index.ts
export * from './counter';
```

---

```tsx
// components/counter/counter.test.tsx
import {
    act,
    render,
    screen,
} from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { Counter } from './counter';

describe('Counter', () => {
    test('should render with initial state of 1', async () => {
        renderCounter();

        expect(
            await screen.findByText(/^1$/)
        ).toBeInTheDocument();
        expect(
            await screen.findByRole('button', {
                name: /one up/i,
            })
        ).toBeInTheDocument();
    });

    test('should increase count by clicking a button', async () => {
        const user = userEvent.setup();

        renderCounter();

        expect(
            await screen.findByText(/^1$/)
        ).toBeInTheDocument();

        await act(async () => {
            await user.click(
                await screen.findByRole('button', {
                    name: /one up/i,
                })
            );
        });

        expect(
            await screen.findByText(/^2$/)
        ).toBeInTheDocument();
    });
});

const renderCounter = () => {
    return render(<Counter />);
};
```

---

```tsx
// components/counter-with-context/counter-with-context.tsx
import {
    CounterStoreProvider,
    useCounterStoreContext,
} from '../../contexts/use-counter-store-context';

const Counter = () => {
    const { count, inc } = useCounterStoreContext(
        (state) => state
    );

    return (
        <div>
            <h2>Counter Store Context</h2>
            <h4>{count}</h4>
            <button onClick={inc}>One Up</button>
        </div>
    );
};

export const CounterWithContext = () => {
    return (
        <CounterStoreProvider>
            <Counter />
        </CounterStoreProvider>
    );
};
```

---

```tsx
// components/counter-with-context/index.ts
export * from './counter-with-context';
```

---

```tsx
// components/counter-with-context/counter-with-context.test.tsx
import {
    act,
    render,
    screen,
} from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { CounterWithContext } from './counter-with-context';

describe('CounterWithContext', () => {
    test('should render with initial state of 1', async () => {
        renderCounterWithContext();

        expect(
            await screen.findByText(/^1$/)
        ).toBeInTheDocument();
        expect(
            await screen.findByRole('button', {
                name: /one up/i,
            })
        ).toBeInTheDocument();
    });

    test('should increase count by clicking a button', async () => {
        const user = userEvent.setup();

        renderCounterWithContext();

        expect(
            await screen.findByText(/^1$/)
        ).toBeInTheDocument();

        await act(async () => {
            await user.click(
                await screen.findByRole('button', {
                    name: /one up/i,
                })
            );
        });

        expect(
            await screen.findByText(/^2$/)
        ).toBeInTheDocument();
    });
});

const renderCounterWithContext = () => {
    return render(<CounterWithContext />);
};
```

> **Примечание**: без включения [globals configuration](https://vitest.dev/config/#globals) необходимо добавить `import { describe, test, expect } из 'vitest'` в начало каждого тестового файла.

**Демонстрации в кодовой песочнице**

-   Демонстрация Jest: <https://stackblitz.com/edit/jest-zustand>
-   Vitest Demo: <https://stackblitz.com/edit/vitest-zustand>

## Ссылки

-   **React Testing Library**: [React Testing Library (RTL)](https://testing-library.com/docs/react-testing-library/intro) - это очень легковесное решение для тестирования React-компонентов. Она предоставляет вспомогательные функции поверх `react-dom` и `react-dom/test-utils`, таким образом, чтобы поощрять лучшие практики тестирования. Его основной руководящий принцип таков: "Чем больше ваши тесты похожи на то, как используется ваше программное обеспечение, тем больше уверенности они могут вам дать".
-   **Нативная библиотека тестирования**: [Native Testing Library (RNTL)](https://testing-library.com/docs/react-native-testing-library/intro) - очень легкое решение для тестирования компонентов React Native, аналогично RTL, но его функции построены поверх `react-test-renderer`.
-   **Детали реализации тестирования**: Заметка в блоге Кента Доддса о том, почему он рекомендует избегать [testing implementation details](https://kentcdodds.com/blog/testing-implementation-details).

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/testing></small>
