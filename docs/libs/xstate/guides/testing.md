# Тестирование автоматов

В общем, тестирование конечных автоматов и диаграмм состояний должно выполняться путем тестирования _общего поведения_ машины; поэтому:

> В **текущем состоянии**, когда происходит **некоторая последовательность событий**, тестируемая система должна находиться в **определенном состоянии** или показывать определенные **выходные** данные.

Такое тестирование следует из [поведенческой разработки](<https://ru.wikipedia.org/wiki/BDD_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)>) (BDD) и стратегии тестирования методом [черного ящика](https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BF%D0%BE_%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B8_%D1%87%D1%91%D1%80%D0%BD%D0%BE%D0%B3%D0%BE_%D1%8F%D1%89%D0%B8%D0%BA%D0%B0). Не следует напрямую проверять внутреннюю работу машины; вместо этого следует проверить наблюдаемое поведение. По смыслу, тестирование автоматов ближе к интеграционным тестам, чем к модульным тестам.

## Тестирование чистой логики

Если вы не хотите тестировать побочные эффекты, такие как выполнение действий или вызов акторов, и вместо этого хотите протестировать чистую логику, можно использовать функцию `machine.transition(...)`, чтобы убедиться, что определенное состояние достигнуто при заданном исходное состояние и событие:

```js
import { lightMachine } from '../path/to/lightMachine';

it('should reach "yellow" given "green" when the "TIMER" event occurs', () => {
  const expectedValue = 'yellow'; // the expected state value

  const actualState = lightMachine.transition('green', {
    type: 'TIMER',
  });

  expect(actualState.matches(expectedValue)).toBeTruthy();
});
```

## Тестирование служб

Поведение и результат работы служб можно проверить, заявив, что они _в конечном итоге_ достигают ожидаемого состояния, учитывая начальное состояние и последовательность событий:

```js
import { fetchMachine } from '../path/to/fetchMachine';

it('should eventually reach "success"', (done) => {
  const fetchService = interpret(fetchMachine).onTransition(
    (state) => {
      // this is where you expect the state to eventually
      // be reached
      if (state.matches('success')) {
        done();
      }
    }
  );

  fetchService.start();

  // send zero or more events to the service that should
  // cause it to eventually reach its expected state
  fetchService.send({ type: 'FETCH', id: 42 });
});
```

!!!tip "Подсказка"

    Имейте в виду, что большинство платформ тестирования имеют тайм-аут по умолчанию, и ожидается, что асинхронные тесты завершатся до этого тайм-аута. При необходимости настройте тайм-аут (например, [`jest.setTimeout(timeout)`](https://jestjs.io/ru/docs/jest-object#jestsettimeouttimeout)) для более длительных тестов.

## Подмена (mock) реализации

Поскольку действия и запуск / создание акторов являются побочными эффектами, их выполнение в тестовой среде может быть нежелательным. Вы можете использовать параметр `machine.withConfig(...)`, чтобы изменить детали реализации определенных действий:

```js
import { fetchMachine } from '../path/to/fetchMachine';

it('should eventually reach "success"', (done) => {
  let userAlerted = false;

  const mockFetchMachine = fetchMachine.withConfig({
    services: {
      fetchFromAPI: (_, event) =>
        new Promise((resolve) => {
          setTimeout(() => {
            resolve({ id: event.id });
          }, 50);
        }),
    },
    actions: {
      alertUser: () => {
        // set a flag instead of executing the original action
        userAlerted = true;
      },
    },
  });

  const fetchService = interpret(
    mockFetchMachine
  ).onTransition((state) => {
    if (state.matches('success')) {
      // assert that effects were executed
      expect(userAlerted).toBeTruthy();
      done();
    }
  });

  fetchService.start();

  fetchService.send({ type: 'FETCH', id: 42 });
});
```
