# Использование Map и Set

Вам нужно обернуть Map и Set внутри объекта. Когда вы хотите, чтобы его обновление отражалось (например, в React), вы делаете это, вызывая `setState` на нем:

**Посмотреть кодбокс можно здесь: <https://codesandbox.io/s/late-https-bxz9qy>**.

```js
import { create } from 'zustand';

const useFooBar = create(() => ({
    foo: new Map(),
    bar: new Set(),
}));

function doSomething() {
    // doing something...

    // If you want to update some React component that uses `useFooBar`, you have to call setState
    // to let React know that an update happened.
    // Following React's best practices, you should create a new Map/Set when updating them:
    useFooBar.setState((prev) => ({
        foo: new Map(prev.foo).set('newKey', 'newValue'),
        bar: new Set(prev.bar).add('newKey'),
    }));
}
```
