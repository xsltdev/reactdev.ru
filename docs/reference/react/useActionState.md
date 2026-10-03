---
description: useActionState - это хук React, который позволяет обновлять состояние с побочными эффектами через действия.
---

# useActionState

<big>`useActionState` - это хук React, который позволяет обновлять состояние с побочными эффектами через [действия](useTransition.md#functions-called-in-starttransition-are-called-actions).</big>

```js
const [state, dispatchAction, isPending] = useActionState(reducerAction, initialState, permalink?);
```

## Описание {#reference}

### `useActionState(reducerAction, initialState, permalink?)` {#useactionstate}

Вызовите `useActionState` на верхнем уровне компонента, чтобы создать состояние для результата действия.

```js
import { useActionState } from 'react';

function reducerAction(previousState, actionPayload) {
    // ...
}

function MyCart({ initialState }) {
    const [state, dispatchAction, isPending] = useActionState(reducerAction, initialState);
    // ...
}
```

[Смотрите примеры ниже.](#usage)

#### Параметры {#parameters}

-   `reducerAction`: функция, которая вызывается, когда запускается действие. При вызове она получает предыдущее состояние (сначала переданный `initialState`, затем предыдущее возвращённое значение) первым аргументом, а затем `actionPayload`, переданный в `dispatchAction`.
-   `initialState`: значение, которое состояние должно иметь в начале. React игнорирует этот аргумент после первого вызова `dispatchAction`.
-   **необязательно** `permalink`: строка с уникальным URL страницы, которую меняет эта форма.
    -   Для страниц с [серверными компонентами React](../rsc/server-components.md) и прогрессивным улучшением.
    -   Если `reducerAction` — [серверная функция](../rsc/server-functions.md) и форма отправлена до загрузки пакета JavaScript, браузер перейдёт на указанный permalink, а не на URL текущей страницы.

#### Возвращаемое значение {#returns}

`useActionState` возвращает массив ровно из трёх значений:

1.  Текущее состояние. При первом рендере оно совпадает с переданным `initialState`. После вызова `dispatchAction` оно совпадает со значением, которое вернула `reducerAction`.
2.  Функция `dispatchAction`, которую вызывают внутри [действий](useTransition.md#functions-called-in-starttransition-are-called-actions).
3.  Флаг `isPending`, который показывает, ожидает ли какое-либо действие, отправленное этим хуком.

#### Предупреждения {#caveats}

-   `useActionState` — хук, поэтому его можно вызывать только **на верхнем уровне компонента** или собственного хука. Его нельзя вызывать в циклах и условиях. Если это нужно, вынесите состояние в новый компонент.
-   React ставит несколько вызовов `dispatchAction` в очередь и выполняет их по порядку. Каждый вызов `reducerAction` получает результат предыдущего вызова.
-   У функции `dispatchAction` стабильная идентичность, поэтому её часто не указывают в зависимостях эффекта, но если указать, эффект из-за этого не запустится. Если линтер позволяет опустить зависимость без ошибок, так и можно сделать. [Подробнее об удалении зависимостей эффекта.](../../learn/removing-effect-dependencies.md#move-dynamic-objects-and-functions-inside-your-effect)
-   При использовании `permalink` на странице назначения должен рендериться тот же компонент формы (с той же `reducerAction` и тем же `permalink`), чтобы React знал, как передать состояние. Когда страница становится интерактивной, этот параметр уже ни на что не влияет.
-   При использовании серверных функций `initialState` должен быть [сериализуемым](../rsc/use-server.md#serializable-parameters-and-return-values) (обычные объекты, массивы, строки, числа).
-   Если `dispatchAction` выбрасывает ошибку, React отменяет все действия в очереди и показывает ближайшую [границу ошибки](Component.md#catching-rendering-errors-with-an-error-boundary).
-   Если одновременно идёт несколько действий, React объединяет их. Это ограничение, которое могут снять в будущем релизе.

!!!note "Примечание"

    `dispatchAction` нужно вызывать из действия.

    Можно обернуть вызов в [`startTransition`](startTransition.md) или передать его в [проп-действие](useTransition.md#exposing-action-props-from-components). Вызовы вне этой области не считаются частью перехода, и в режиме разработки [пишется ошибка](#async-function-outside-transition).

### Функция `reducerAction` {#reduceraction}

Функция `reducerAction`, переданная в `useActionState`, получает предыдущее состояние и возвращает новое.

В отличие от редюсеров в `useReducer`, `reducerAction` может быть асинхронной и выполнять побочные эффекты:

```js
async function reducerAction(previousState, actionPayload) {
  const newState = await post(actionPayload);
  return newState;
}
```

Каждый раз, когда вы вызываете `dispatchAction`, React вызывает `reducerAction` с `actionPayload`. Редюсер выполняет побочные эффекты, например отправляет данные, и возвращает новое состояние. Если `dispatchAction` вызван несколько раз, React ставит вызовы в очередь и выполняет их по порядку, поэтому результат предыдущего вызова передаётся как `previousState` в текущий.

#### Параметры {#reduceraction-parameters}

* `previousState`: последнее состояние. Сначала оно равно `initialState`. После первого вызова `dispatchAction` оно равно последнему возвращённому состоянию.

* **необязательно** `actionPayload`: аргумент, переданный в `dispatchAction`. Тип может быть любым. По соглашениям `useReducer` это обычно объект со свойством `type`, которое его определяет, и, необязательно, другими свойствами с дополнительными данными.

#### Возвращаемое значение {#reduceraction-returns}

`reducerAction` возвращает новое состояние и запускает переход, чтобы перерендерить компонент с этим состоянием.

#### Предупреждения {#reduceraction-caveats}

* `reducerAction` может быть синхронной или асинхронной. Она может выполнять синхронные действия, например показать уведомление, или асинхронные, например отправить обновления на сервер.
* `reducerAction` не вызывается дважды в `<StrictMode>`, потому что `reducerAction` рассчитана на побочные эффекты.
* Тип возврата `reducerAction` должен совпадать с типом `initialState`. Если TypeScript видит несовпадение, тип состояния, возможно, нужно указать явно.
* Если выставлять состояние после `await` внутри `reducerAction`, сейчас обновление состояния нужно обернуть в дополнительный `startTransition`. Подробнее в документации [`startTransition`](useTransition.md#react-doesnt-treat-my-state-update-after-await-as-a-transition).
* При использовании серверных функций `actionPayload` должен быть [сериализуемым](../rsc/use-server.md#serializable-parameters-and-return-values) (обычные объекты, массивы, строки, числа).

<a id="why-is-it-called-reduceraction"></a>

??? note "Почему она называется `reducerAction`?"

    Функцию, переданную в `useActionState`, называют *reducer action*, потому что:

    - Она *сводит* предыдущее состояние к новому, как `useReducer`.
    - Это *действие*, потому что её вызывают внутри перехода, и она может выполнять побочные эффекты.

    По смыслу `useActionState` похож на `useReducer`, но в редюсере можно делать побочные эффекты.

## Использование {#usage}

### Состояние у действия {#adding-state-to-an-action}

Вызовите `useActionState` на верхнем уровне компонента, чтобы создать состояние для результата действия.

```js hl_lines="7"
import { useActionState } from 'react';

async function addToCartAction(prevCount) {
  // ...
}
function Counter() {
  const [count, dispatchAction, isPending] = useActionState(addToCartAction, 0);

  // ...
}
```

`useActionState` возвращает массив ровно из трёх элементов:

1. Текущее состояние. Сначала оно равно переданному начальному состоянию.
2. Диспетчер действия, которым запускается `reducerAction`.
3. Состояние ожидания: идёт ли действие прямо сейчас.

Чтобы вызвать `addToCartAction`, вызовите диспетчер действия. React поставит вызовы `addToCartAction` в очередь вместе с предыдущим количеством.

=== "App.js"

    ```js

    import { useActionState, startTransition } from 'react';
    import { addToCart } from './api';
    import Total from './Total';

    export default function Checkout() {
        const [count, dispatchAction, isPending] = useActionState(async (prevCount) => {
            return await addToCart(prevCount)
        }, 0);

        function handleClick() {
            startTransition(() => {
                dispatchAction();
            });
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <span>Qty: {count}</span>
                </div>
                <div className="row">
                    <button onClick={handleClick}>Add Ticket{isPending ? ' 🌀' : '  '}</button>
                </div>
                <hr />
                <Total quantity={count} />
            </div>
        );
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity}) {
        return (
            <div className="row total">
                <span>Total</span>
                <span>{formatter.format(quantity * 9999)}</span>
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return count + 1;
    }

    export async function removeFromCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .row button {
      margin-left: auto;
      min-width: 150px;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }

    button {
      padding: 8px 16px;
      cursor: pointer;
    }
    ```

Каждый клик по «Add Ticket» ставит вызов `addToCartAction` в очередь. React показывает состояние ожидания, пока не добавятся все билеты, а затем перерендеривает компонент с итоговым состоянием.

<a id="how-useactionstate-queuing-works"></a>

??? note "Как устроена очередь `useActionState`"

    Попробуйте нажать «Add Ticket» несколько раз. Каждый клик ставит в очередь новый `addToCartAction`. Из-за искусственной задержки в 1 секунду 4 клика займут около 4 секунд.

    **Так задумано в `useActionState`.**

    Нужно дождаться предыдущего результата `addToCartAction`, чтобы передать `prevCount` в следующий вызов. Значит, React ждёт окончания предыдущего действия, прежде чем вызвать следующее.

    Обычно это решается [совместно с useOptimistic](useActionState.md#using-with-useoptimistic), а в более сложных случаях можно [отменять действия в очереди](#cancelling-queued-actions) или не использовать `useActionState`.

### Несколько типов действий {#using-multiple-action-types}

Чтобы обработать несколько типов, можно передать аргумент в `dispatchAction`.

По соглашению это пишут как `switch`. Для каждой ветки считается и возвращается следующее состояние. Форма аргумента может быть любой, но обычно передают объекты со свойством `type`, которое определяет действие.

=== "App.js"

    ```js

    import { useActionState, startTransition } from 'react';
    import { addToCart, removeFromCart } from './api';
    import Total from './Total';

    export default function Checkout() {
        const [count, dispatchAction, isPending] = useActionState(updateCartAction, 0);

        function handleAdd() {
            startTransition(() => {
                dispatchAction({ type: 'ADD' });
            });
        }

        function handleRemove() {
            startTransition(() => {
                dispatchAction({ type: 'REMOVE' });
            });
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <span className="stepper">
                        <span className="qty">{isPending ? '🌀' : count}</span>
                        <span className="buttons">
                            <button onClick={handleAdd}>▲</button>
                            <button onClick={handleRemove}>▼</button>
                        </span>
                    </span>
                </div>
                <hr />
                <Total quantity={count} isPending={isPending}/>
            </div>
        );
    }

    async function updateCartAction(prevCount, actionPayload) {
        switch (actionPayload.type) {
            case 'ADD': {
                return await addToCart(prevCount);
            }
            case 'REMOVE': {
                return await removeFromCart(prevCount);
            }
        }
        return prevCount;
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                {isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return count + 1;
    }

    export async function removeFromCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stepper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .qty {
      min-width: 20px;
      text-align: center;
    }

    .buttons {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .buttons button {
      padding: 0 8px;
      font-size: 10px;
      line-height: 1.2;
      cursor: pointer;
    }

    .pending {
      width: 20px;
      text-align: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }
    ```

Когда вы увеличиваете или уменьшаете количество, отправляется `"ADD"` или `"REMOVE"`. В `reducerAction` для обновления количества вызываются разные API.

В этом примере состояние ожидания действий заменяет и количество, и сумму. Если нужна немедленная обратная связь, например сразу обновить количество, используйте `useOptimistic`.

??? note "Чем `useActionState` отличается от `useReducer`?"

    Этот пример похож на `useReducer`, но задачи у них разные:

    - **`useReducer`** ведёт состояние интерфейса. Редюсер должен быть чистым.

    - **`useActionState`** ведёт состояние действий. Редюсер может выполнять побочные эффекты.

    `useActionState` можно считать `useReducer` для побочных эффектов действий пользователя. Поскольку следующее действие считается по предыдущему, вызовы приходится [выполнять по порядку](useActionState.md#how-useactionstate-queuing-works). Если действия должны идти параллельно, используйте `useState` и `useTransition` напрямую.

### Вместе с `useOptimistic` {#using-with-useoptimistic}

`useActionState` можно сочетать с [`useOptimistic`](useOptimistic.md), чтобы сразу обновить интерфейс:

=== "App.js"

    ```js

    import { useActionState, startTransition, useOptimistic } from 'react';
    import { addToCart, removeFromCart } from './api';
    import Total from './Total';

    export default function Checkout() {
        const [count, dispatchAction, isPending] = useActionState(updateCartAction, 0);
        const [optimisticCount, setOptimisticCount] = useOptimistic(count);

        function handleAdd() {
            startTransition(() => {
                setOptimisticCount(c => c + 1);
                dispatchAction({ type: 'ADD' });
            });
        }

        function handleRemove() {
            startTransition(() => {
                setOptimisticCount(c => c - 1);
                dispatchAction({ type: 'REMOVE' });
            });
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <span className="stepper">
                        <span className="pending">{isPending && '🌀'}</span>
                        <span className="qty">{optimisticCount}</span>
                        <span className="buttons">
                            <button onClick={handleAdd}>▲</button>
                            <button onClick={handleRemove}>▼</button>
                        </span>
                    </span>
                </div>
                <hr />
                <Total quantity={optimisticCount} isPending={isPending}/>
            </div>
        );
    }

    async function updateCartAction(prevCount, actionPayload) {
        switch (actionPayload.type) {
            case 'ADD': {
                return await addToCart(prevCount);
            }
            case 'REMOVE': {
                return await removeFromCart(prevCount);
            }
        }
        return prevCount;
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                <span>{isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}</span>
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return count + 1;
    }

    export async function removeFromCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stepper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .qty {
      min-width: 20px;
      text-align: center;
    }

    .buttons {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .buttons button {
      padding: 0 8px;
      font-size: 10px;
      line-height: 1.2;
      cursor: pointer;
    }

    .pending {
      width: 20px;
      text-align: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }
    ```

`setOptimisticCount` сразу обновляет количество, а `dispatchAction()` ставит `updateCartAction` в очередь. Индикатор ожидания появляется и у количества, и у суммы, чтобы пользователь видел, что обновление ещё применяется.

### Вместе с пропами-действиями {#using-with-action-props}

Если передать функцию `dispatchAction` в компонент, который отдаёт [проп-действие](useTransition.md#exposing-action-props-from-components), самим вызывать `startTransition` или `useOptimistic` не нужно.

В примере используются пропы `increaseAction` и `decreaseAction` компонента QuantityStepper:

=== "App.js"

    ```js

    import { useActionState } from 'react';
    import { addToCart, removeFromCart } from './api';
    import QuantityStepper from './QuantityStepper';
    import Total from './Total';

    export default function Checkout() {
        const [count, dispatchAction, isPending] = useActionState(updateCartAction, 0);

        function addAction() {
            dispatchAction({type: 'ADD'});
        }

        function removeAction() {
            dispatchAction({type: 'REMOVE'});
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <QuantityStepper
                        value={count}
                        increaseAction={addAction}
                        decreaseAction={removeAction}
                    />
                </div>
                <hr />
                <Total quantity={count} isPending={isPending} />
            </div>
        );
    }

    async function updateCartAction(prevCount, actionPayload) {
        switch (actionPayload.type) {
            case 'ADD': {
                return await addToCart(prevCount);
            }
            case 'REMOVE': {
                return await removeFromCart(prevCount);
            }
        }
        return prevCount;
    }
    ```

=== "QuantityStepper.js"

    ```js

    import { startTransition, useOptimistic } from 'react';

    export default function QuantityStepper({value, increaseAction, decreaseAction}) {
        const [optimisticValue, setOptimisticValue] = useOptimistic(value);
        const isPending = value !== optimisticValue;
        function handleIncrease() {
            startTransition(async () => {
                setOptimisticValue(c => c + 1);
                await increaseAction();
            });
        }

        function handleDecrease() {
            startTransition(async () => {
                setOptimisticValue(c => Math.max(0, c - 1));
                await decreaseAction();
            });
        }

        return (
            <span className="stepper">
                <span className="pending">{isPending && '🌀'}</span>
                <span className="qty">{optimisticValue}</span>
                <span className="buttons">
                    <button onClick={handleIncrease}>▲</button>
                    <button onClick={handleDecrease}>▼</button>
                </span>
            </span>
        );
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                {isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return count + 1;
    }

    export async function removeFromCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stepper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .qty {
      min-width: 20px;
      text-align: center;
    }

    .buttons {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .buttons button {
      padding: 0 8px;
      font-size: 10px;
      line-height: 1.2;
      cursor: pointer;
    }

    .pending {
      width: 20px;
      text-align: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }
    ```

У `<QuantityStepper>` уже есть поддержка переходов, состояния ожидания и оптимистичного обновления количества. Нужно только сказать действию, *что* менять, а *как* менять, компонент берёт на себя.

### Отмена действий в очереди {#cancelling-queued-actions}

Чтобы отменить ожидающие действия, можно использовать `AbortController`:

=== "App.js"

    ```js

    import { useActionState, useRef } from 'react';
    import { addToCart, removeFromCart } from './api';
    import QuantityStepper from './QuantityStepper';
    import Total from './Total';

    export default function Checkout() {
        const abortRef = useRef(null);
        const [count, dispatchAction, isPending] = useActionState(updateCartAction, 0);

        async function addAction() {
            if (abortRef.current) {
                abortRef.current.abort();
            }
            abortRef.current = new AbortController();
            await dispatchAction({ type: 'ADD', signal: abortRef.current.signal });
        }

        async function removeAction() {
            if (abortRef.current) {
                abortRef.current.abort();
            }
            abortRef.current = new AbortController();
            await dispatchAction({ type: 'REMOVE', signal: abortRef.current.signal });
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <QuantityStepper
                        value={count}
                        increaseAction={addAction}
                        decreaseAction={removeAction}
                    />
                </div>
                <hr />
                <Total quantity={count} isPending={isPending} />
            </div>
        );
    }

    async function updateCartAction(prevCount, actionPayload) {
        switch (actionPayload.type) {
            case 'ADD': {
                try {
                    return await addToCart(prevCount, { signal: actionPayload.signal });
                } catch (e) {
                    return prevCount + 1;
                }
            }
            case 'REMOVE': {
                try {
                    return await removeFromCart(prevCount, { signal: actionPayload.signal });
                } catch (e) {
                    return Math.max(0, prevCount - 1);
                }
            }
        }
        return prevCount;
    }
    ```

=== "QuantityStepper.js"

    ```js

    import { startTransition, useOptimistic } from 'react';

    export default function QuantityStepper({value, increaseAction, decreaseAction}) {
        const [optimisticValue, setOptimisticValue] = useOptimistic(value);
        const isPending = value !== optimisticValue;
        function handleIncrease() {
            startTransition(async () => {
                setOptimisticValue(c => c + 1);
                await increaseAction();
            });
        }

        function handleDecrease() {
            startTransition(async () => {
                setOptimisticValue(c => Math.max(0, c - 1));
                await decreaseAction();
            });
        }

        return (
                        <span className="stepper">
                <span className="pending">{isPending && '🌀'}</span>
                <span className="qty">{optimisticValue}</span>
                <span className="buttons">
                    <button onClick={handleIncrease}>▲</button>
                    <button onClick={handleDecrease}>▼</button>
                </span>
            </span>
        );
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                {isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    class AbortError extends Error {
        name = 'AbortError';
        constructor(message = 'The operation was aborted') {
            super(message);
        }
    }

    function sleep(ms, signal) {
        if (!signal) return new Promise((resolve) => setTimeout(resolve, ms));
        if (signal.aborted) return Promise.reject(new AbortError());

        return new Promise((resolve, reject) => {
            const id = setTimeout(() => {
                signal.removeEventListener('abort', onAbort);
                resolve();
            }, ms);

            const onAbort = () => {
                clearTimeout(id);
                reject(new AbortError());
            };

            signal.addEventListener('abort', onAbort, { once: true });
        });
    }
    export async function addToCart(count, opts) {
        await sleep(1000, opts?.signal);
        return count + 1;
    }

    export async function removeFromCart(count, opts) {
        await sleep(1000, opts?.signal);
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stepper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .qty {
      min-width: 20px;
      text-align: center;
    }

    .buttons {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .buttons button {
      padding: 0 8px;
      font-size: 10px;
      line-height: 1.2;
      cursor: pointer;
    }

    .pending {
      width: 20px;
      text-align: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }
    ```

Попробуйте несколько раз нажать увеличение или уменьшение: сумма обновится в пределах 1 секунды, сколько бы раз вы ни кликнули. Так происходит, потому что `AbortController` «завершает» предыдущее действие, и следующее может продолжиться.

!!!warning "Подводный камень"

    Отменять действие не всегда безопасно.

    Например, если действие делает мутацию (запись в базу), отмена сетевого запроса не откатывает изменение на сервере. Поэтому `useActionState` по умолчанию не отменяет действия. Это безопасно только если побочный эффект можно спокойно проигнорировать или повторить.

### Вместе с пропами-действиями `<form>` {#use-with-a-form}

Функцию `dispatchAction` можно передать в проп `action` у `<form>`.

В этом случае React сам оборачивает отправку в переход, и `startTransition` вызывать не нужно. `reducerAction` получает предыдущее состояние и отправленный `FormData`:

=== "App.js"

    ```js

    import { useActionState, useOptimistic } from 'react';
    import { addToCart, removeFromCart } from './api';
    import Total from './Total';

    export default function Checkout() {
        const [count, dispatchAction, isPending] = useActionState(updateCartAction, 0);
        const [optimisticCount, setOptimisticCount] = useOptimistic(count);

        async function formAction(formData) {
            const type = formData.get('type');
            if (type === 'ADD') {
                setOptimisticCount(c => c + 1);
            } else {
                setOptimisticCount(c => Math.max(0, c - 1));
            }
            return dispatchAction(formData);
        }

        return (
            <form action={formAction} className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <span className="stepper">
                        <span className="pending">{isPending && '🌀'}</span>
                        <span className="qty">{optimisticCount}</span>
                        <span className="buttons">
                            <button type="submit" name="type" value="ADD">▲</button>
                            <button type="submit" name="type" value="REMOVE">▼</button>
                        </span>
                    </span>
                </div>
                <hr />
                <Total quantity={count} isPending={isPending} />
            </form>
        );
    }

    async function updateCartAction(prevCount, formData) {
        const type = formData.get('type');
        switch (type) {
            case 'ADD': {
                return await addToCart(prevCount);
            }
            case 'REMOVE': {
                return await removeFromCart(prevCount);
            }
        }
        return prevCount;
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                {isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return count + 1;
    }

    export async function removeFromCart(count) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Math.max(0, count - 1);
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stepper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .qty {
      min-width: 20px;
      text-align: center;
    }

    .buttons {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .buttons button {
      padding: 0 8px;
      font-size: 10px;
      line-height: 1.2;
      cursor: pointer;
    }

    .pending {
      width: 20px;
      text-align: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }
    ```

В этом примере клик по стрелкам степпера отправляет форму, и `useActionState` вызывает `updateCartAction` с данными формы. Пример использует `useOptimistic`, чтобы сразу показать новое количество, пока сервер подтверждает обновление.

<RSC>

Вместе с [серверной функцией](../rsc/server-functions.md) `useActionState` позволяет показать ответ сервера ещё до завершения гидратации (когда React подключается к HTML, отрендеренному на сервере). Необязательный параметр `permalink` даёт прогрессивное улучшение (форма работает до загрузки JavaScript) на страницах с динамическим содержимым. Обычно это делает за вас фреймворк.

</RSC>

Подробнее об использовании действий с формами — в документации [`<form>`](../react-dom/components/form.md#handle-form-submission-with-a-server-function).

### Обработка ошибок {#handling-errors}

С `useActionState` ошибки обрабатывают двумя способами.

Известные ошибки, например ошибку проверки «quantity not available» с бэкенда, можно вернуть как часть состояния `reducerAction` и показать в интерфейсе.

Неизвестные ошибки, например `undefined is not a function`, можно бросить. React отменит все действия в очереди и покажет ближайшую [границу ошибки](Component.md#catching-rendering-errors-with-an-error-boundary), повторно бросив ошибку из хука `useActionState`.

=== "App.js"

    ```js

    import {useActionState, startTransition} from 'react';
    import {ErrorBoundary} from 'react-error-boundary';
    import {addToCart} from './api';
    import Total from './Total';

    function Checkout() {
        const [state, dispatchAction, isPending] = useActionState(
            async (prevState, quantity) => {
                const result = await addToCart(prevState.count, quantity);
                if (result.error) {
                    // Return the error from the API as state
                    return {...prevState, error: `Could not add quanitiy ${quantity}: ${result.error}`};
                }

                if (!isPending) {
                    // Clear the error state for the first dispatch.
                    return {count: result.count, error: null};
                }

                // Return the new count, and any errors that happened.
                return {count: result.count, error: prevState.error};

            },
            {
                count: 0,
                error: null,
            }
        );

        function handleAdd(quantity) {
            startTransition(() => {
                dispatchAction(quantity);
            });
        }

        return (
            <div className="checkout">
                <h2>Checkout</h2>
                <div className="row">
                    <span>Eras Tour Tickets</span>
                    <span>
                        {isPending && '🌀 '}Qty: {state.count}
                    </span>
                </div>
                <div className="buttons">
                    <button onClick={() => handleAdd(1)}>Add 1</button>
                    <button onClick={() => handleAdd(10)}>Add 10</button>
                    <button onClick={() => handleAdd(NaN)}>Add NaN</button>
                </div>
                {state.error && <div className="error">{state.error}</div>}
                <hr />
                <Total quantity={state.count} isPending={isPending} />
            </div>
        );
    }

    export default function App() {
        return (
            <ErrorBoundary
                fallbackRender={({resetErrorBoundary}) => (
                    <div className="checkout">
                        <h2>Something went wrong</h2>
                        <p>The action could not be completed.</p>
                        <button onClick={resetErrorBoundary}>Try again</button>
                    </div>
                )}>
                <Checkout />
            </ErrorBoundary>
        );
    }
    ```

=== "Total.js"

    ```js

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    });

    export default function Total({quantity, isPending}) {
        return (
            <div className="row total">
                <span>Total</span>
                <span>
                    {isPending ? '🌀 Updating...' : formatter.format(quantity * 9999)}
                </span>
            </div>
        );
    }
    ```

=== "api.js"

    ```js

    export async function addToCart(count, quantity) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        if (quantity > 5) {
            return {error: 'Quantity not available'};
        } else if (isNaN(quantity)) {
            throw new Error('Quantity must be a number');
        }
        return {count: count + quantity};
    }
    ```

=== "styles.css"

    ```css

    .checkout {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: system-ui;
    }

    .checkout h2 {
      margin: 0 0 8px 0;
    }

    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .total {
      font-weight: bold;
    }

    hr {
      width: 100%;
      border: none;
      border-top: 1px solid #ccc;
      margin: 4px 0;
    }

    button {
      padding: 8px 16px;
      cursor: pointer;
    }

    .buttons {
      display: flex;
      gap: 8px;
    }

    .error {
      color: red;
      font-size: 14px;
    }
    ```

=== "package.js"

    ```json

    {
      "dependencies": {
        "react": "19.0.0",
        "react-dom": "19.0.0",
        "react-scripts": "^5.0.0",
        "react-error-boundary": "4.0.3"
      },
      "main": "/index.js"
    }
    ```

В этом примере «Add 10» имитирует API, который возвращает ошибку проверки: `updateCartAction` кладёт её в состояние и показывает рядом. «Add NaN» даёт недопустимое количество, поэтому `updateCartAction` бросает ошибку, она проходит через `useActionState` к `ErrorBoundary` и показывает интерфейс сброса.


### Использование информации, возвращаемой действием формы {#using-information-returned-by-a-form-action}

Вызовите `useActionState` на верхнем уровне вашего компонента, чтобы получить доступ к возвращаемому значению действия из последнего раза, когда форма была отправлена.

```jsx
import { useActionState } from 'react';
import { action } from './actions.js';

function MyComponent() {
    const [state, formAction] = useActionState(
        action,
        null
    );
    // ...
    return <form action={formAction}>{/* ... */}</form>;
}
```

`useActionState` возвращает массив, содержащий ровно два элемента:

1.  Текущее состояние формы, которое первоначально устанавливается в указанное вами начальное состояние, а после отправки формы устанавливается в возвращаемое значение указанного вами действия.
2.  Новое действие, которое вы передаете в `<form>` в качестве его свойства `action`.

Когда форма будет отправлена, будет вызвана указанная вами функция действия. Ее возвращаемое значение станет новым текущим состоянием формы.

Предоставленное вами действие также получит новый первый аргумент, а именно текущее состояние формы. При первой отправке формы это будет начальное состояние, которое вы указали, а при последующих отправках - возвращаемое значение, полученное при последнем вызове действия. Остальные аргументы такие же, как если бы `useActionState` не использовался

```js
function action(currentState, formData) {
    // ...
    return 'next state';
}
```

### Отображение информации после отправки формы {#display-information-after-submitting-a-form}

**1. Отображение ошибок формы**

Чтобы отобразить сообщения, такие как сообщение об ошибке или тост, возвращаемый серверным действием, оберните действие вызовом `useActionState`.

=== "App.js"

    ```jsx
    import { useState } from 'react';
    import { useActionState } from 'react';
    import { addToCart } from './actions.js';

    function AddToCartForm({ itemID, itemTitle }) {
    	const [message, formAction] = useActionState(
    		addToCart,
    		null
    	);
    	return (
    		<form action={formAction}>
    			<h2>{itemTitle}</h2>
    			<input
    				type="hidden"
    				name="itemID"
    				value={itemID}
    			/>
    			<button type="submit">Add to Cart</button>
    			{message}
    		</form>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<AddToCartForm
    				itemID="1"
    				itemTitle="JavaScript: The Definitive Guide"
    			/>
    			<AddToCartForm
    				itemID="2"
    				itemTitle="JavaScript: The Good Parts"
    			/>
    		</>
    	);
    }
    ```

=== "actions.js"

    ```js
    'use server';

    export async function addToCart(prevState, queryData) {
    	const itemID = queryData.get('itemID');
    	if (itemID === '1') {
    		return 'Added to cart';
    	} else {
    		return "Couldn't add to cart: the item is sold out.";
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/yv2vzy?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="damp-tree-yv2vzy" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

**2. Отображение структурированной информации после отправки формы**

Возвращаемое значение действия сервера может быть любым сериализуемым значением. Например, это может быть объект, содержащий логическое значение, указывающее на успешность выполнения действия, сообщение об ошибке или обновленную информацию.

=== "App.js"

    ```jsx
    import { useState } from 'react';
    import { useActionState } from 'react';
    import { addToCart } from './actions.js';

    function AddToCartForm({ itemID, itemTitle }) {
    	const [formState, formAction] = useActionState(
    		addToCart,
    		{}
    	);
    	return (
    		<form action={formAction}>
    			<h2>{itemTitle}</h2>
    			<input
    				type="hidden"
    				name="itemID"
    				value={itemID}
    			/>
    			<button type="submit">Add to Cart</button>
    			{formState?.success && (
    				<div className="toast">
    					Added to cart! Your cart now has{' '}
    					{formState.cartSize} items.
    				</div>
    			)}
    			{formState?.success === false && (
    				<div className="error">
    					Failed to add to cart:{' '}
    					{formState.message}
    				</div>
    			)}
    		</form>
    	);
    }

    export default function App() {
    	return (
    		<>
    			<AddToCartForm
    				itemID="1"
    				itemTitle="JavaScript: The Definitive Guide"
    			/>
    			<AddToCartForm
    				itemID="2"
    				itemTitle="JavaScript: The Good Parts"
    			/>
    		</>
    	);
    }
    ```

=== "actions.js"

    ```js
    'use server';

    export async function addToCart(prevState, queryData) {
    	const itemID = queryData.get('itemID');
    	if (itemID === '1') {
    		return {
    			success: true,
    			cartSize: 12,
    		};
    	} else {
    		return {
    			success: false,
    			message: 'The item is sold out.',
    		};
    	}
    }
    ```

=== "CodeSandbox"

    <iframe src="https://codesandbox.io/embed/kmkspd?view=Editor+%2B+Preview&module=%2Fsrc%2FApp.js" style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;" title="jolly-minsky-kmkspd" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

## Решение проблем {#troubleshooting}

### Флаг `isPending` не обновляется {#ispending-not-updating}

Если вы вызываете `dispatchAction` вручную (не через проп-действие), оберните вызов в [`startTransition`](startTransition.md):

```js
import { useActionState, startTransition } from 'react';

function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(myAction, null);

  function handleClick() {
    // ✅ Correct: wrap in startTransition
    startTransition(() => {
      dispatchAction();
    });
  }

  // ...
}
```

Когда `dispatchAction` передают в проп-действие, React сам оборачивает его в переход.

### Действие не может прочитать данные формы {#action-cannot-read-form-data}

При использовании `useActionState` функция `reducerAction` получает дополнительный первый аргумент: предыдущее или начальное состояние. Данные отправленной формы поэтому оказываются вторым аргументом, а не первым.

```js hl_lines="2 7"
// Without useActionState
function action(formData) {
  const name = formData.get('name');
}

// With useActionState
function action(prevState, formData) {
  const name = formData.get('name');
}
```

### Действия пропускаются {#actions-skipped}

Если вызвать `dispatchAction` несколько раз и часть вызовов не выполняется, возможно, более ранний `dispatchAction` бросил ошибку.

Когда `reducerAction` бросает ошибку, React пропускает все последующие вызовы `dispatchAction` в очереди.

Чтобы это обработать, ловите ошибки внутри `reducerAction` и возвращайте состояние с ошибкой, а не бросайте её:

```js
async function myReducerAction(prevState, data) {
  try {
    const result = await submitData(data);
    return { success: true, data: result };
  } catch (error) {
    // ✅ Return error state instead of throwing
    return { success: false, error: error.message };
  }
}
```

### Состояние не сбрасывается {#reset-state}

У `useActionState` нет встроенной функции сброса. Чтобы сбросить состояние, научите `reducerAction` обрабатывать сигнал сброса:

```js
const initialState = { name: '', error: null };

async function formAction(prevState, payload) {
  // Handle reset
  if (payload === null) {
    return initialState;
  }
  // Normal action logic
  const result = await submitData(payload);
  return result;
}

function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(formAction, initialState);

  function handleReset() {
    startTransition(() => {
      dispatchAction(null); // Pass null to trigger reset
    });
  }

  // ...
}
```

Либо добавьте проп `key` компоненту с `useActionState`, чтобы он смонтировался заново со свежим состоянием, либо проп `action` у `<form>`, который сбрасывается сам после отправки.

### Ошибка: «An async function with useActionState was called outside of a transition.» {#async-function-outside-transition}

Частая ошибка — забыть вызвать `dispatchAction` изнутри перехода:

```text linenums="0"
<ConsoleLogLine level="error">

An async function with useActionState was called outside of a transition. This is likely not what you intended (for example, isPending will not update correctly). Either call the returned function inside startTransition, or pass it to an `action` or `formAction` prop.

</ConsoleLogLine>
```

Ошибка возникает, потому что `dispatchAction` должен выполняться внутри перехода:

```js
function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(myAsyncAction, null);

  function handleClick() {
    // ❌ Wrong: calling dispatchAction outside a Transition
    dispatchAction();
  }

  // ...
}
```

Чтобы исправить, либо оберните вызов в [`startTransition`](startTransition.md):

```js
import { useActionState, startTransition } from 'react';

function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(myAsyncAction, null);

  function handleClick() {
    // ✅ Correct: wrap in startTransition
    startTransition(() => {
      dispatchAction();
    });
  }

  // ...
}
```

Либо передайте `dispatchAction` в проп-действие: его вызов уже будет в переходе:

```js
function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(myAsyncAction, null);

  // ✅ Correct: action prop wraps in a Transition for you
  return <Button action={dispatchAction}>...</Button>;
}
```

### Ошибка: «Cannot update action state while rendering» {#cannot-update-during-render}

Нельзя вызывать `dispatchAction` во время рендера:

```text linenums="0"
Cannot update action state while rendering.
```

Так получается бесконечный цикл: вызов `dispatchAction` планирует обновление состояния, оно вызывает повторный рендер, а тот снова вызывает `dispatchAction`.

```js
function MyComponent() {
  const [state, dispatchAction, isPending] = useActionState(myAction, null);

  // ❌ Wrong: calling dispatchAction during render
  dispatchAction();

  // ...
}
```

Чтобы исправить, вызывайте `dispatchAction` только в ответ на действия пользователя (отправка формы или клик по кнопке).


### Мое действие больше не может читать данные отправленной формы {#my-action-can-no-longer-read-the-submitted-form-data}

Когда вы оборачиваете действие с помощью `useActionState`, оно получает дополнительный аргумент _в качестве первого аргумента_. Таким образом, отправленные данные формы являются его _вторым_ аргументом, а не первым, как это было бы обычно. Новый первый аргумент, который добавляется, - это текущее состояние формы.

```js
function action(currentState, formData) {
    // ...
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/useActionState](https://react.dev/reference/react/useActionState)</small>
