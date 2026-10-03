---
description: Проверяет, что хук useMemo используется с возвращаемым значением. Подробнее в документации useMemo
---

# use-memo

<big>

Проверяет, что хук `useMemo` используется с возвращаемым значением. Подробнее в [документации `useMemo`](../../react/useMemo.md).

</big>

## Подробности правила {#rule-details}

`useMemo` нужен, чтобы вычислять и кэшировать дорогие значения, а не для побочных эффектов. Без возвращаемого значения `useMemo` возвращает `undefined`, что лишает хук смысла и обычно значит, что выбран не тот хук.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js hl_lines="3"
// ❌ No return value
function Component({ data }) {
  const processed = useMemo(() => {
    data.forEach(item => console.log(item));
    // Missing return!
  }, [data]);

  return <div>{processed}</div>; // Always undefined
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Returns computed value
function Component({ data }) {
  const processed = useMemo(() => {
    return data.map(item => item * 2);
  }, [data]);

  return <div>{processed}</div>;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно выполнять побочные эффекты при изменении зависимостей {#side-effects}

Может возникнуть соблазн использовать `useMemo` для побочных эффектов:

```js hl_lines="4"
// ❌ Wrong: Side effects in useMemo
function Component({user}) {
  // No return value, just side effect
  useMemo(() => {
    analytics.track('UserViewed', {userId: user.id});
  }, [user.id]);

  // Not assigned to a variable
  useMemo(() => {
    return analytics.track('UserViewed', {userId: user.id});
  }, [user.id]);
}
```

Если побочный эффект должен происходить в ответ на действие пользователя, лучше держать его рядом с событием:

```js
// ✅ Good: Side effects in event handlers
function Component({user}) {
  const handleClick = () => {
    analytics.track('ButtonClicked', {userId: user.id});
    // Other click logic...
  };

  return <button onClick={handleClick}>Click me</button>;
}
```

Если побочный эффект синхронизирует состояние React с каким-то внешним состоянием (или наоборот), используйте `useEffect`:

```js
// ✅ Good: Synchronization in useEffect
function Component({theme}) {
  useEffect(() => {
    localStorage.setItem('preferredTheme', theme);
    document.body.className = theme;
  }, [theme]);

  return <div>Current theme: {theme}</div>;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/use-memo](https://react.dev/reference/eslint-plugin-react-hooks/lints/use-memo)</small>
