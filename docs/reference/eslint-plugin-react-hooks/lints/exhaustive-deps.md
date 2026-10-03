---
description: Проверяет, что массивы зависимостей хуков React содержат все нужные зависимости
---

# exhaustive-deps

<big>

Проверяет, что массивы зависимостей хуков React содержат все нужные зависимости.

</big>

## Подробности правила {#rule-details}

Хуки React вроде `useEffect`, `useMemo` и `useCallback` принимают массивы зависимостей. Если значение, на которое есть ссылка внутри такого хука, не входит в массив зависимостей, React не перезапустит эффект и не пересчитает значение, когда эта зависимость изменится. Из-за этого возникают устаревшие замыкания: хук использует устаревшие значения.

## Типичные нарушения {#common-violations}

Эта ошибка часто появляется, когда React пытаются «обмануть» насчёт зависимостей, чтобы управлять тем, когда запускается эффект. Эффекты должны синхронизировать компонент с внешними системами. Массив зависимостей сообщает React, какие значения использует эффект, чтобы React знал, когда синхронизировать его заново.

Если вы спорите с линтом, код, скорее всего, нужно перестроить. Как это сделать, см. в [Удаление зависимостей эффектов](../../../learn/removing-effect-dependencies.md).

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Missing dependency
useEffect(() => {
  console.log(count);
}, []); // Missing 'count'

// ❌ Missing prop
useEffect(() => {
  fetchUser(userId);
}, []); // Missing 'userId'

// ❌ Incomplete dependencies
useMemo(() => {
  return items.sort(sortOrder);
}, [items]); // Missing 'sortOrder'
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ All dependencies included
useEffect(() => {
  console.log(count);
}, [count]);

// ✅ All dependencies included
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

## Устранение неполадок {#troubleshooting}

### Зависимость-функция вызывает бесконечный цикл {#function-dependency-loops}

Есть эффект, но на каждом рендере создаётся новая функция:

```js
// ❌ Causes infinite loop
const logItems = () => {
  console.log(items);
};

useEffect(() => {
  logItems();
}, [logItems]); // Infinite loop!
```

В большинстве случаев эффект не нужен. Вызывайте функцию там, где происходит действие:

```js
// ✅ Call it from the event handler
const logItems = () => {
  console.log(items);
};

return <button onClick={logItems}>Log</button>;

// ✅ Or derive during render if there's no side effect
items.forEach(item => {
  console.log(item);
});
```

Если эффект действительно нужен (например, чтобы на что-то подписаться снаружи), сделайте зависимость стабильной:

```js
// ✅ useCallback keeps the function reference stable
const logItems = useCallback(() => {
  console.log(items);
}, [items]);

useEffect(() => {
  logItems();
}, [logItems]);

// ✅ Or move the logic straight into the effect
useEffect(() => {
  console.log(items);
}, [items]);
```

### Запуск эффекта только один раз {#effect-on-mount}

Нужно запустить эффект один раз при монтировании, но линт сообщает о пропущенной зависимости:

```js
// ❌ Missing dependency
useEffect(() => {
  sendAnalytics(userId);
}, []); // Missing 'userId'
```

Либо включите зависимость (так и стоит делать), либо используйте реф, если запуск действительно должен быть однократным:

```js
// ✅ Include dependency
useEffect(() => {
  sendAnalytics(userId);
}, [userId]);

// ✅ Or use a ref guard inside an effect
const sent = useRef(false);

useEffect(() => {
  if (sent.current) {
    return;
  }

  sent.current = true;
  sendAnalytics(userId);
}, [userId]);
```

## Параметры {#options}

Пользовательские хуки-эффекты можно настроить через общие параметры ESLint (доступно в `eslint-plugin-react-hooks` 6.1.1 и новее):

```js
{
  "settings": {
    "react-hooks": {
      "additionalEffectHooks": "(useMyEffect|useCustomEffect)"
    }
  }
}
```

- `additionalEffectHooks`: регулярное выражение для пользовательских хуков, у которых нужно проверять полноту зависимостей. Эта настройка общая для всех правил `react-hooks`.

Для обратной совместимости правило также принимает параметр на уровне самого правила:

```js
{
  "rules": {
    "react-hooks/exhaustive-deps": ["warn", {
      "additionalHooks": "(useMyCustomHook|useAnotherHook)"
    }]
  }
}
```

- `additionalHooks`: регулярное выражение для хуков, у которых нужно проверять полноту зависимостей. **Примечание:** если задан этот параметр уровня правила, он важнее общей конфигурации `settings`.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps](https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps)</small>
