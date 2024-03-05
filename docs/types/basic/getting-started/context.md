---
description: базовый пример создания контекста, содержащего активную тему
---

# Контекст

## Базовый пример

Вот базовый пример создания контекста, содержащего активную тему.

```ts
import { createContext } from 'react';

type ThemeContextType = 'light' | 'dark';

const ThemeContext = createContext<ThemeContextType>(
    'light'
);
```

Оберните компоненты, которым нужен контекст, поставщиком контекста:

```ts
import { useState } from 'react';

const App = () => {
    const [theme, setTheme] = useState<ThemeContextType>(
        'light'
    );

    return (
        <ThemeContext.Provider value={theme}>
            <MyComponent />
        </ThemeContext.Provider>
    );
};
```

Вызовите `useContext`, чтобы прочитать и подписаться на контекст.

```ts
import { useContext } from 'react';

const MyComponent = () => {
    const theme = useContext(ThemeContext);

    return <p>The current theme is {theme}.</p>;
};
```

## Без значения контекста по умолчанию

Если у вас нет значения по умолчанию, укажите `null`:

```ts
import { createContext } from 'react';

interface CurrentUserContextType {
    username: string;
}

const CurrentUserContext = createContext<CurrentUserContextType | null>(
    null
);
```

---

```ts
const App = () => {
    const [currentUser, setCurrentUser] = useState<
        CurrentUserContextType
    >({
        username: 'filiptammergard',
    });

    return (
        <CurrentUserContext.Provider value={currentUser}>
            <MyComponent />
        </CurrentUserContext.Provider>
    );
};
```

Теперь, когда тип контекста может быть `null`, вы заметите, что при попытке получить доступ к свойству `username` вы получите ошибку TypeScript `'currentUser' is possibly 'null'`. Для доступа к `username` можно использовать опциональную цепочку:

```ts
import { useContext } from 'react';

const MyComponent = () => {
    const currentUser = useContext(CurrentUserContext);

    return <p>Name: {currentUser?.username}.</p>;
};
```

Однако было бы предпочтительнее не проверять наличие `null`, поскольку мы знаем, что контекст не будет `null`. Один из способов сделать это - предоставить пользовательский хук для использования контекста, в котором будет вылетать ошибка, если контекст не предоставлен:

```ts
import { createContext } from 'react';

interface CurrentUserContextType {
    username: string;
}

const CurrentUserContext = createContext<CurrentUserContextType | null>(
    null
);

const useCurrentUser = () => {
    const currentUserContext = useContext(
        CurrentUserContext
    );

    if (!currentUserContext) {
        throw new Error(
            'useCurrentUser has to be used within <CurrentUserContext.Provider>'
        );
    }

    return currentUserContext;
};
```

Использование проверки типов во время выполнения дает возможность вывести в консоль четкое сообщение об ошибке, когда провайдер не оборачивает компоненты должным образом. Теперь можно получить доступ к `currentUser.username` без проверки на `null`:

```ts
import { useContext } from 'react';

const MyComponent = () => {
    const currentUser = useCurrentUser();

    return <p>Username: {currentUser.username}.</p>;
};
```

### Утверждение типа как альтернатива

Еще один способ избежать проверки на `null` - использовать утверждение типа, чтобы сообщить TypeScript, что контекст не является `null`:

```ts
import { useContext } from 'react';

const MyComponent = () => {
    const currentUser = useContext(CurrentUserContext);

    return <p>Name: {currentUser!.username}.</p>;
};
```

Другой вариант - использовать пустой объект в качестве значения по умолчанию и привести его к ожидаемому типу контекста:

```ts
const CurrentUserContext = createContext<
    CurrentUserContextType
>({} as CurrentUserContextType);
```

Вы также можете использовать утверждение non-null, чтобы получить тот же результат:

```tsx
const CurrentUserContext = createContext<
    CurrentUserContextType
>(null!);
```

Если вы не знаете, что выбрать, отдайте предпочтение проверке и отбрасыванию во время выполнения, а не утверждению типов.

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/context></small>
