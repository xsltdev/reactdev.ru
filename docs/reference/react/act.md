---
description: act - это тестовый хелпер, который применяет ожидающие обновления React перед утверждениями
---

# act

<big>**`act`** - это тестовый хелпер, который применяет ожидающие обновления React перед утверждениями.</big>

```js
await act(async actFn)
```

Чтобы подготовить компонент к утверждениям, оберните код, который его рендерит и выполняет обновления, в вызов `await act()`. Так тест будет работать ближе к тому, как React ведёт себя в браузере.

!!!note "Примечание"

    Прямое использование `act()` может показаться слишком многословным. Чтобы избежать части шаблонного кода, можно воспользоваться библиотекой вроде [React Testing Library](https://testing-library.com/docs/react-testing-library/intro), чьи хелперы уже обёрнуты в `act()`.

## Описание {#reference}

### `await act(async actFn)` {#await-act-async-actfn}

При написании UI-тестов такие задачи, как рендеринг, события пользователя или получение данных, можно рассматривать как «единицы» взаимодействия с пользовательским интерфейсом. React предоставляет хелпер `act()`, который гарантирует, что все обновления, связанные с этими «единицами», обработаны и применены к DOM до того, как вы сделаете какие-либо утверждения.

Имя `act` происходит от паттерна [Arrange-Act-Assert](https://wiki.c2.com/?ArrangeActAssert).

```js hl_lines="2 4"
it ('renders with button disabled', async () => {
  await act(async () => {
    root.render(<TestComponent />)
  });
  expect(container.querySelector('button')).toBeDisabled();
});
```

!!!note "Примечание"

    Мы рекомендуем использовать `act` с `await` и функцией `async`. Хотя синхронная версия работает во многих случаях, она работает не во всех, и из-за того, как React планирует обновления внутри, трудно предсказать, когда можно использовать синхронную версию.

    В будущем мы объявим синхронную версию устаревшей и удалим её.

#### Параметры {#parameters}

-   `async actFn`: Асинхронная функция, оборачивающая рендеринг или взаимодействия для тестируемых компонентов. Любые обновления, запущенные внутри `actFn`, добавляются во внутреннюю очередь act, которая затем сбрасывается целиком, чтобы обработать и применить изменения к DOM. Поскольку функция асинхронная, React также выполнит любой код, пересекающий асинхронную границу, и сбросит все запланированные обновления.

#### Возвращаемое значение {#returns}

`act` ничего не возвращает.

## Использование {#usage}

При тестировании компонента вы можете использовать `act`, чтобы делать утверждения о его выводе.

Например, допустим, у нас есть такой компонент `Counter`. Примеры использования ниже показывают, как его тестировать:

```js
function Counter() {
  const [count, setCount] = useState(0);
  const handleClick = () => {
    setCount(prev => prev + 1);
  }

  useEffect(() => {
    document.title = `You clicked ${count} times`;
  }, [count]);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={handleClick}>
        Click me
      </button>
    </div>
  )
}
```

### Рендеринг компонентов в тестах {#rendering-components-in-tests}

Чтобы проверить результат рендеринга компонента, оберните рендер в `act()`:

```js hl_lines="10 12"
import {act} from 'react';
import ReactDOMClient from 'react-dom/client';
import Counter from './Counter';

it('can render and update a counter', async () => {
  container = document.createElement('div');
  document.body.appendChild(container);

  // ✅ Render the component inside act().
  await act(() => {
    ReactDOMClient.createRoot(container).render(<Counter />);
  });

  const button = container.querySelector('button');
  const label = container.querySelector('p');
  expect(label.textContent).toBe('You clicked 0 times');
  expect(document.title).toBe('You clicked 0 times');
});
```

Здесь мы создаём контейнер, добавляем его в документ и рендерим компонент `Counter` внутри `act()`. Это гарантирует, что компонент отрендерен и его эффекты применены до утверждений.

Использование `act` гарантирует, что все обновления применены до того, как мы делаем утверждения.

### Отправка событий в тестах {#dispatching-events-in-tests}

Чтобы тестировать события, оберните отправку события в `act()`:

```js hl_lines="14 16"
import {act} from 'react';
import ReactDOMClient from 'react-dom/client';
import Counter from './Counter';

it.only('can render and update a counter', async () => {
  const container = document.createElement('div');
  document.body.appendChild(container);

  await act( async () => {
    ReactDOMClient.createRoot(container).render(<Counter />);
  });

  // ✅ Dispatch the event inside act().
  await act(async () => {
    button.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });

  const button = container.querySelector('button');
  const label = container.querySelector('p');
  expect(label.textContent).toBe('You clicked 1 times');
  expect(document.title).toBe('You clicked 1 times');
});
```

Здесь мы рендерим компонент с помощью `act`, а затем отправляем событие внутри другого `act()`. Это гарантирует, что все обновления от события применены до утверждений.

!!!warning "Подводный камень"

    Не забывайте, что отправка DOM-событий работает, только когда DOM-контейнер добавлен в документ. Вы можете использовать библиотеку вроде [React Testing Library](https://testing-library.com/docs/react-testing-library/intro), чтобы сократить шаблонный код.

## Устранение неполадок {#troubleshooting}

### Я получаю ошибку: "The current testing environment is not configured to support act(...)" {#error-the-current-testing-environment-is-not-configured-to-support-act}

Использование `act` требует установить `global.IS_REACT_ACT_ENVIRONMENT=true` в тестовом окружении. Это нужно, чтобы `act` использовался только в правильном окружении.

Если вы не установите эту глобальную переменную, вы увидите такую ошибку:

```text linenums="0"
Warning: The current testing environment is not configured to support act(...)
```

Чтобы исправить, добавьте это в файл глобальной настройки для тестов React:

```js
global.IS_REACT_ACT_ENVIRONMENT=true
```

!!!note "Примечание"

    В тестовых фреймворках вроде [React Testing Library](https://testing-library.com/docs/react-testing-library/intro) `IS_REACT_ACT_ENVIRONMENT` уже установлен за вас.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/react/act](https://react.dev/reference/react/act)</small>
