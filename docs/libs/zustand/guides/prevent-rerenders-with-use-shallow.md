# Предотвращение повторных рендерингов с помощью useShallow

Если вам нужно подписаться на вычисляемое состояние из хранилища, рекомендуется использовать селектор.

Вычисляемый селектор вызовет повторный рендер, если вывод изменился в соответствии с [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is?retiredLocale=it).

В этом случае вы можете использовать `useShallow`, чтобы избежать повторного рендеринга, если вычисляемое значение всегда неглубоко и равно предыдущему.

## Пример

У нас есть хранилище, в котором каждый медведь ассоциируется с едой, и мы хотим отобразить их имена.

```js
import { create } from 'zustand';

const useMeals = create(() => ({
    papaBear: 'large porridge-pot',
    mamaBear: 'middle-size porridge pot',
    littleBear: 'A little, small, wee pot',
}));

export const BearNames = () => {
    const names = useMeals((state) => Object.keys(state));

    return <div>{names.join(', ')}</div>;
};
```

Теперь папа-медведь хочет пиццу:

```js
useMeals.setState({
    papaBear: 'a large pizza',
});
```

Это изменение вызывает повторные рендеры `BearNames`, даже если фактический вывод `names` не изменился в соответствии с shallow equal.

Мы можем исправить это с помощью `useShallow`!

```js
import { create } from 'zustand';
import { useShallow } from 'zustand/react/shallow';

const useMeals = create(() => ({
    papaBear: 'large porridge-pot',
    mamaBear: 'middle-size porridge pot',
    littleBear: 'A little, small, wee pot',
}));

export const BearNames = () => {
    const names = useMeals(
        useShallow((state) => Object.keys(state))
    );

    return <div>{names.join(', ')}</div>;
};
```

Теперь все они могут заказывать другие блюда, не вызывая ненужных повторных запусков нашего компонента `BearNames`.

<small>:material-information-outline: Источник &mdash; <https://docs.pmnd.rs/zustand/guides/prevent-rerenders-with-use-shallow></small>
