---
description: Как использовать Zustand
---

# Введение

![Промо Zustand](bear.jpg)

Небольшое, быстрое и масштабируемое решение для управления состояниями в Bearbones. Zustand имеет удобный API, основанный на хуках. В нем нет шаблонов и разногласий, но есть достаточно соглашений, чтобы быть явным и потоковым.

Не пренебрегайте им, потому что он милый, у него есть когти! Много времени было потрачено на решение распространенных проблем, таких как [проблема зомби-потомков](https://react-redux.js.org/api/hooks#stale-props-and-zombie-children), [параллелизм React](https://github.com/bvaughn/rfcs/blob/useMutableSource/text/0000-use-mutable-source.md) и [потеря контекста](https://github.com/facebook/react/issues/13332) между различными рендерами. Возможно, это единственный менеджер состояний в окружении React, который справляется со всеми этими проблемами.

Вы можете попробовать живую демонстрацию [здесь](https://codesandbox.io/s/dazzling-moon-itop4).

## Установка

Zustand доступен в виде пакета на NPM для использования:

```bash
# NPM
npm install zustand
# Or, use any package manager of your choice.
```

## Сначала создайте хранилище

Ваше хранилище - это хук! Вы можете поместить в него что угодно: примитивы, объекты, функции. Функция `set` _обновляет_ состояние.

```js
import { create } from 'zustand';

const useStore = create((set) => ({
    bears: 0,
    increasePopulation: () =>
        set((state) => ({ bears: state.bears + 1 })),
    removeAllBears: () => set({ bears: 0 }),
    updateBears: (newBears) => set({ bears: newBears }),
}));
```

## Затем соедините ваши компоненты, и все!

Вы можете использовать хук в любом месте, без провайдеров. Выберите состояние, и при изменении состояния требуемый компонент будет перерисовываться.

```jsx
function BearCounter() {
    const bears = useStore((state) => state.bears);
    return <h1>{bears} around here...</h1>;
}

function Controls() {
    const increasePopulation = useStore(
        (state) => state.increasePopulation
    );
    return (
        <button onClick={increasePopulation}>one up</button>
    );
}
```

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/getting-started/introduction></small>
