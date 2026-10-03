---
description: React Compiler — новый инструмент времени сборки, который автоматически оптимизирует приложение React. Он работает с обычным JavaScript и понимает Правила React, поэтому переписывать код, чтобы им пользоваться, не нужно
---

# Введение

<big>

React Compiler — новый инструмент времени сборки, который автоматически оптимизирует приложение React. Он работает с обычным JavaScript и понимает [Правила React](../../reference/rules/index.md), поэтому переписывать код, чтобы им пользоваться, не нужно.

</big>

!!!tip "Вы узнаете"

    * Что делает React Compiler
    * Как начать работу с компилятором
    * Стратегии постепенного внедрения
    * Отладка и устранение неполадок, когда что-то идёт не так
    * Использование компилятора в библиотеке React

## Что делает React Compiler? {#what-does-react-compiler-do}

React Compiler автоматически оптимизирует приложение React во время сборки. React часто и без оптимизации достаточно быстр, но иногда приходится вручную мемоизировать компоненты и значения, чтобы приложение оставалось отзывчивым. Такая ручная мемоизация утомительна, в ней легко ошибиться, и она добавляет лишний код, который нужно сопровождать. React Compiler делает эту оптимизацию автоматически, снимая эту умственную нагрузку, чтобы вы могли сосредоточиться на создании возможностей.

### До React Compiler {#before-react-compiler}

Без компилятора, чтобы оптимизировать повторные рендеринги, компоненты и значения нужно мемоизировать вручную:

```js
import { useMemo, useCallback, memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data, onClick }) {
  const processedData = useMemo(() => {
    return expensiveProcessing(data);
  }, [data]);

  const handleClick = useCallback((item) => {
    onClick(item.id);
  }, [onClick]);

  return (
    <div>
      {processedData.map(item => (
        <Item key={item.id} onClick={() => handleClick(item)} />
      ))}
    </div>
  );
});
```

!!!note "Примечание"

    В этой ручной мемоизации есть тонкая ошибка, которая ломает мемоизацию:

    ```js hl_lines="1"
    <Item key={item.id} onClick={() => handleClick(item)} />
    ```

    Хотя `handleClick` обёрнут в `useCallback`, стрелочная функция `() => handleClick(item)` создаёт новую функцию при каждом рендеринге компонента. Это значит, что `Item` всегда получает новый проп `onClick`, и мемоизация ломается.

    React Compiler умеет оптимизировать это правильно и со стрелочной функцией, и без неё, гарантируя, что `Item` повторно рендерится, только когда меняется `props.onClick`.

### После React Compiler {#after-react-compiler}

С React Compiler вы пишете тот же код без ручной мемоизации:

```js
function ExpensiveComponent({ data, onClick }) {
  const processedData = expensiveProcessing(data);

  const handleClick = (item) => {
    onClick(item.id);
  };

  return (
    <div>
      {processedData.map(item => (
        <Item key={item.id} onClick={() => handleClick(item)} />
      ))}
    </div>
  );
}
```

_[Посмотрите этот пример в песочнице React Compiler](https://playground.react.dev/#N4Igzg9grgTgxgUxALhAMygOzgFwJYSYAEAogB4AOCmYeAbggMIQC2Fh1OAFMEQCYBDHAIA0RQowA2eOAGsiAXwCURYAB1iROITA4iFGBERgwCPgBEhAogF4iCStVoMACoeO1MAcy6DhSgG4NDSItHT0ACwFMPkkmaTlbIi48HAQWFRsAPlUQ0PFMKRlZFLSWADo8PkC8hSDMPJgEHFhiLjzQgB4+eiyO-OADIwQTM0thcpYBClL02xz2zXz8zoBJMqJZBABPG2BU9Mq+BQKiuT2uTJyomLizkoOMk4B6PqX8pSUFfs7nnro3qEapgFCAFEA)_

React Compiler автоматически применяет оптимальную мемоизацию и гарантирует, что приложение повторно рендерится, только когда это необходимо.

??? note "Какую мемоизацию добавляет React Compiler?"

    Автоматическая мемоизация React Compiler в первую очередь направлена на **улучшение производительности обновлений** (повторный рендеринг уже существующих компонентов), поэтому она сосредоточена на двух сценариях:

    1. **Пропуск каскадного повторного рендеринга компонентов**
        * Повторный рендеринг `<Parent />` заставляет повторно рендериться многие компоненты в его дереве, хотя изменился только `<Parent />`
    1. **Пропуск дорогих вычислений вне React**
        * Например, вызов `expensivelyProcessAReallyLargeArrayOfObjects()` внутри компонента или хука, которому нужны эти данные

    #### Оптимизация повторных рендерингов {#optimizing-re-renders}

    React позволяет описывать интерфейс как функцию текущего состояния (конкретнее: пропсов, состояния и контекста). В текущей реализации, когда состояние компонента меняется, React повторно рендерит этот компонент _и всех его потомков_ — если только вы не применили какую-то ручную мемоизацию с помощью `useMemo()`, `useCallback()` или `React.memo()`. Например, в следующем примере `<MessageButton>` будет повторно рендериться всякий раз, когда меняется состояние `<FriendList>`:

    ```js
    function FriendList({ friends }) {
      const onlineCount = useFriendOnlineCount();
      if (friends.length === 0) {
        return <NoFriends />;
      }
      return (
        <div>
          <span>{onlineCount} online</span>
          {friends.map((friend) => (
            <FriendListCard key={friend.id} friend={friend} />
          ))}
          <MessageButton />
        </div>
      );
    }
    ```
    [_Посмотрите этот пример в песочнице React Compiler_](https://playground.react.dev/#N4Igzg9grgTgxgUxALhAMygOzgFwJYSYAEAYjHgpgCYAyeYOAFMEWuZVWEQL4CURwADrEicQgyKEANnkwIAwtEw4iAXiJQwCMhWoB5TDLmKsTXgG5hRInjRFGbXZwB0UygHMcACzWr1ABn4hEWsYBBxYYgAeADkIHQ4uAHoAPksRbisiMIiYYkYs6yiqPAA3FMLrIiiwAAcAQ0wU4GlZBSUcbklDNqikusaKkKrgR0TnAFt62sYHdmp+VRT7SqrqhOo6Bnl6mCoiAGsEAE9VUfmqZzwqLrHqM7ubolTVol5eTOGigFkEMDB6u4EAAhKA4HCEZ5DNZ9ErlLIWYTcEDcIA)

    React Compiler автоматически применяет эквивалент ручной мемоизации и гарантирует, что при изменении состояния повторно рендерятся только нужные части приложения. Иногда это называют «мелкозернистой реактивностью». В примере выше React Compiler определяет, что возвращаемое значение `<FriendListCard />` можно переиспользовать, даже когда `friends` меняется, и может избежать пересоздания этого JSX _и_ повторного рендеринга `<MessageButton>`, когда счётчик меняется.

    #### Дорогие вычисления тоже мемоизируются {#expensive-calculations-also-get-memoized}

    React Compiler также может автоматически мемоизировать дорогие вычисления, которые используются во время рендеринга:

    ```js
    // **Not** memoized by React Compiler, since this is not a component or hook
    function expensivelyProcessAReallyLargeArrayOfObjects() { /* ... */ }

    // Memoized by React Compiler since this is a component
    function TableContainer({ items }) {
      // This function call would be memoized:
      const data = expensivelyProcessAReallyLargeArrayOfObjects(items);
      // ...
    }
    ```
    [_Посмотрите этот пример в песочнице React Compiler_](https://playground.react.dev/#N4Igzg9grgTgxgUxALhAejQAgFTYHIQAuumAtgqRAJYBeCAJpgEYCemASggIZyGYDCEUgAcqAGwQwANJjBUAdokyEAFlTCZ1meUUxdMcIcIjyE8vhBiYVECAGsAOvIBmURYSonMCAB7CzcgBuCGIsAAowEIhgYACCnFxioQAyXDAA5gixMDBcLADyzvlMAFYIvGAAFACUmMCYaNiYAHStOFgAvk5OGJgAshTUdIysHNy8AkbikrIKSqpaWvqGIiZmhE6u7p7ymAAqXEwSguZcCpKV9VSEFBodtcBOmAYmYHz0XIT6ALzefgFUYKhCJRBAxeLcJIsVIZLI5PKFYplCqVa63aoAbm6u0wMAQhFguwAPPRAQA+YAfL4dIloUmBMlODogDpAA)

    Однако если `expensivelyProcessAReallyLargeArrayOfObjects` действительно дорогая функция, возможно, стоит реализовать для неё собственную мемоизацию вне React, потому что:

    - React Compiler мемоизирует только компоненты и хуки React, а не каждую функцию
    - Мемоизация React Compiler не разделяется между несколькими компонентами или хуками

    Поэтому если `expensivelyProcessAReallyLargeArrayOfObjects` используется во многих разных компонентах, дорогое вычисление будет выполняться снова и снова, даже если передаются в точности те же элементы. Мы рекомендуем сначала [профилировать](../../reference/react/useMemo.md#how-to-tell-if-a-calculation-is-expensive) и убедиться, что вычисление действительно настолько дорогое, прежде чем усложнять код.

## Стоит ли попробовать компилятор? {#should-i-try-out-the-compiler}

Мы призываем всех начать использовать React Compiler. Сегодня компилятор всё ещё необязательное дополнение к React, но в будущем некоторым возможностям он может понадобиться, чтобы работать в полную силу.

### Безопасно ли его использовать? {#is-it-safe-to-use}

React Compiler теперь стабилен и тщательно проверен в производственной среде. Им уже пользуются в производственной среде такие компании, как Meta, но выкатка компилятора в производственную среду вашего приложения будет зависеть от состояния кодовой базы и от того, насколько хорошо вы следуете [Правилам React](../../reference/rules/index.md).

## Какие инструменты сборки поддерживаются? {#what-build-tools-are-supported}

React Compiler можно установить в [нескольких инструментах сборки](installation.md), таких как Babel, Vite, Metro и Rsbuild.

React Compiler — это в первую очередь лёгкая обёртка в виде плагина Babel вокруг ядра компилятора, которое спроектировано так, чтобы не зависеть от самого Babel. Начальная стабильная версия компилятора останется в первую очередь плагином Babel, но мы работаем с командами swc и [oxc](https://github.com/oxc-project/oxc/issues/10048), чтобы сделать первоклассную поддержку React Compiler, и в будущем вам не придётся возвращать Babel в конвейеры сборки.

Пользователи Next.js могут включить React Compiler, вызываемый через swc, начиная с [v15.3.1](https://github.com/vercel/next.js/releases/tag/v15.3.1).

## Что делать с useMemo, useCallback и React.memo? {#what-should-i-do-about-usememo-usecallback-and-reactmemo}

По умолчанию React Compiler мемоизирует код на основе своего анализа и эвристик. В большинстве случаев эта мемоизация будет такой же точной или даже точнее той, что вы написали бы сами.

Однако иногда разработчикам нужен больший контроль над мемоизацией. Хуки `useMemo` и `useCallback` можно по-прежнему использовать вместе с React Compiler как аварийный люк, чтобы управлять тем, какие значения мемоизируются. Типичный случай — когда мемоизированное значение используется как зависимость эффекта, чтобы эффект не срабатывал повторно, даже если его зависимости по сути не изменились.

Для нового кода мы рекомендуем полагаться на компилятор в мемоизации и использовать `useMemo`/`useCallback` там, где нужен точный контроль.

Для существующего кода мы рекомендуем либо оставить текущую мемоизацию на месте (её удаление может изменить результат компиляции), либо тщательно протестировать код, прежде чем убирать мемоизацию.

## Попробуйте React Compiler {#try-react-compiler}

Этот раздел поможет начать работу с React Compiler и понять, как эффективно использовать его в проектах.

* **[Установка](installation.md)** — установите React Compiler и настройте его для инструментов сборки
* **[Совместимость версий React](../../reference/react-compiler/target.md)** — поддержка React 17, 18 и 19
* **[Конфигурация](../../reference/react-compiler/configuration.md)** — настройте компилятор под свои задачи
* **[Постепенное внедрение](incremental-adoption.md)** — стратегии постепенной выкатки компилятора в существующих кодовых базах
* **[Отладка и устранение неполадок](debugging.md)** — находите и исправляйте проблемы при использовании компилятора
* **[Компиляция библиотек](../../reference/react-compiler/compiling-libraries.md)** — лучшие практики поставки скомпилированного кода
* **[Справочник API](../../reference/react-compiler/configuration.md)** — подробная документация всех параметров конфигурации

## Дополнительные материалы {#additional-resources}

Помимо этих документов мы рекомендуем заглянуть в [рабочую группу React Compiler](https://github.com/reactwg/react-compiler), где есть дополнительная информация и обсуждение компилятора.

<small>:material-information-outline: Источник &mdash; [https://react.dev/learn/react-compiler/introduction](https://react.dev/learn/react-compiler/introduction)</small>
