---
description: addTransitionType позволяет указать причину перехода
---

# addTransitionType

<big>**`addTransitionType`** позволяет указать причину перехода.</big>

```js
startTransition(() => {
  addTransitionType('my-transition-type');
  setState(newState);
});
```

## Описание {#reference}

### `addTransitionType` {#addtransitiontype}

#### Параметры {#parameters}

-   `type`: Тип перехода, который нужно добавить. Это может быть любая строка.

#### Возвращаемое значение {#returns}

`addTransitionType` ничего не возвращает.

#### Предупреждения {#caveats}

-   Если несколько переходов объединяются, собираются все типы переходов. К переходу также можно добавить больше одного типа.
-   Типы переходов сбрасываются после каждого коммита. Это значит, что фолбэк `<Suspense>` свяжет типы после `startTransition`, но раскрытие содержимого — нет.

## Использование {#usage}

### Добавление причины перехода {#adding-the-cause-of-a-transition}

Вызовите `addTransitionType` внутри `startTransition`, чтобы указать причину перехода:

```text hl_lines="6 5"
import { startTransition, addTransitionType } from 'react';

function Submit({action) {
  function handleClick() {
    startTransition(() => {
      addTransitionType('submit-click');
      action();
    });
  }

  return <button onClick={handleClick}>Click me</button>;
}

```

Когда вы вызываете addTransitionType в области видимости startTransition, React свяжет submit-click как одну из причин перехода.

Сейчас типы переходов можно использовать, чтобы настраивать разные анимации в зависимости от того, что вызвало переход. Есть три способа их использовать:

-   [Настройка анимаций с помощью типов перехода представления в браузере](#customize-animations-using-browser-view-transition-types)
-   [Настройка анимаций с помощью класса `View Transition`](#customize-animations-using-view-transition-class)
-   [Настройка анимаций с помощью событий `ViewTransition`](#customize-animations-using-viewtransition-events)

В будущем мы планируем поддержать больше сценариев использования причины перехода.

### Настройка анимаций с помощью типов перехода представления в браузере {#customize-animations-using-browser-view-transition-types}

Когда [`ViewTransition`](ViewTransition.md) активируется из перехода, React добавляет все типы переходов как браузерные [типы перехода представления](https://www.w3.org/TR/css-view-transitions-2/#active-view-transition-pseudo-examples) к элементу.

Это позволяет настраивать разные анимации на основе областей CSS:

```js hl_lines="11"
function Component() {
  return (
    <ViewTransition>
      <div>Hello</div>
    </ViewTransition>
  );
}

startTransition(() => {
  addTransitionType('my-transition-type');
  setShow(true);
});
```

```css
:root:active-view-transition-type(my-transition-type) {
  &::view-transition-...(...) {
    ...
  }
}
```

### Настройка анимаций с помощью класса `View Transition` {#customize-animations-using-view-transition-class}

Вы можете настраивать анимации активированного `ViewTransition` в зависимости от типа, передав объект в класс View Transition:

```js
function Component() {
  return (
    <ViewTransition enter={{
      'my-transition-type': 'my-transition-class',
    }}>
      <div>Hello</div>
    </ViewTransition>
  );
}

// ...
startTransition(() => {
  addTransitionType('my-transition-type');
  setState(newState);
});
```

Если совпадает несколько типов, они объединяются. Если ни один тип не совпал, вместо этого используется специальная запись "default". Если у какого-либо типа значение "none", оно побеждает, и ViewTransition отключается (имя не назначается).

Их можно сочетать с пропсами enter/exit/update/layout/share, чтобы сопоставлять по виду триггера и типу перехода.

```js
<ViewTransition enter={{
  'navigation-back': 'enter-right',
  'navigation-forward': 'enter-left',
}}
exit={{
  'navigation-back': 'exit-right',
  'navigation-forward': 'exit-left',
}}>
```

### Настройка анимаций с помощью событий `ViewTransition` {#customize-animations-using-viewtransition-events}

Вы можете императивно настраивать анимации активированного `ViewTransition` в зависимости от типа с помощью событий View Transition:

```
<ViewTransition onUpdate={(inst, types) => {
  if (types.includes('navigation-back')) {
    ...
  } else if (types.includes('navigation-forward')) {
    ...
  } else {
    ...
  }
}}>
```

Это позволяет выбирать разные императивные анимации в зависимости от причины.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/addTransitionType](https://react.dev/reference/react/addTransitionType)</small>
