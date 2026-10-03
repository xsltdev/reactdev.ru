---
description: cacheSignal позволяет узнать, когда время жизни cache() закончилось
---

# cacheSignal

<big>**`cacheSignal`** позволяет узнать, когда время жизни `cache()` закончилось.</big>

```js
const signal = cacheSignal();
```

<RSC>

Сейчас `cacheSignal` используется только с [серверными компонентами React](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components).

</RSC>

## Описание {#reference}

### `cacheSignal` {#cachesignal}

Вызовите `cacheSignal`, чтобы получить `AbortSignal`.

```js hl_lines="3 7"
import {cacheSignal} from 'react';
async function Component() {
  await fetch(url, { signal: cacheSignal() });
}
```

Когда React закончит рендеринг, `AbortSignal` будет прерван. Это позволяет отменить любую незавершённую работу, которая больше не нужна.
Рендеринг считается законченным, когда:
-   React успешно завершил рендеринг
-   рендеринг был прерван
-   рендеринг завершился ошибкой

#### Параметры {#parameters}

Эта функция не принимает никаких параметров.

#### Возвращаемое значение {#returns}

`cacheSignal` возвращает `AbortSignal`, если вызван во время рендеринга. В противном случае `cacheSignal()` возвращает `null`.

#### Предупреждения {#caveats}

-   Сейчас `cacheSignal` предназначен для использования только в [серверных компонентах React](../rsc/server-components.md). В клиентских компонентах он всегда возвращает `null`. В будущем он также будет использоваться для клиентских компонентов, когда клиентский кэш обновляется или инвалидируется. Не следует предполагать, что на клиенте он всегда будет `null`.
-   Если вызвать `cacheSignal` вне рендеринга, он вернёт `null`, чтобы было ясно, что текущая область видимости не кэшируется навсегда.

## Использование {#usage}

### Отмена незавершённых запросов {#cancel-in-flight-requests}

Вызовите `cacheSignal`, чтобы прервать незавершённые запросы.

```js hl_lines="4"
import {cache, cacheSignal} from 'react';
const dedupedFetch = cache(fetch);
async function Component() {
  await dedupedFetch(url, { signal: cacheSignal() });
}
```

!!!warning "Подводный камень"

    Вы не можете использовать `cacheSignal`, чтобы прервать асинхронную работу, начатую вне рендеринга, например

    ```js
    import {cacheSignal} from 'react';
    // 🚩 Pitfall: The request will not actually be aborted if the rendering of `Component` is finished.
    const response = fetch(url, { signal: cacheSignal() });
    async function Component() {
      await response;
    }
    ```

### Игнорирование ошибок после того, как React закончил рендеринг {#ignore-errors-after-react-has-finished-rendering}

Если функция выбрасывает исключение, это может быть из-за отмены (например, соединение с базой данных было закрыто). Вы можете использовать свойство `aborted`, чтобы проверить, была ли ошибка из-за отмены или это настоящая ошибка. Ошибки из-за отмены можно игнорировать.

```js hl_lines="2 8 12"
import {cacheSignal} from "react";
import {queryDatabase, logError} from "./database";

async function getData(id) {
  try {
     return await queryDatabase(id);
  } catch (x) {
     if (!cacheSignal()?.aborted) {
        // only log if it's a real error and not due to cancellation
       logError(x);
     }
     return null;
  }
}

async function Component({id}) {
  const data = await getData(id);
  if (data === null) {
    return <div>No data available</div>;
  }
  return <div>{data.name}</div>;
}
```

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/cacheSignal](https://react.dev/reference/react/cacheSignal)</small>
