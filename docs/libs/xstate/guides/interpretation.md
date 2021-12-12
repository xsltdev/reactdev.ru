# Интерпретация автоматов

Хотя конечный автомат / диаграмма состояний с чистой функцией `.transition()` полезны для обеспечения гибкости, чистоты и тестируемости, но для того, чтобы ее можно было использовать в реальном приложении, нужно еще кое-что:

- Следить за текущим состоянием и сохранять его
- Выполнять побочные эффекты
- Обрабатывать отложенные переходы и события
- Общаться с внешними службами

**Интерпретатор** (_interpreter_) отвечает за _интерпретацию_ конечного автомата / диаграммы состояний и выполнение всего вышеперечисленного, то есть его синтаксического анализа и выполнения в среде выполнения. Интерпретируемый, работающий экземпляр диаграммы состояний называется **службой** (_service_).

## Интерпретатор

_Начиная с версии 4.0+_

Доступен дополнительный интерпретатор, который можно использовать для запуска диаграмм состояний. Интерпретатор, в частности, поддерживает:

- Переходы между состояниями
- Выполнение действий (побочные эффекты)
- Отложенные события с возможностью отмены
- Активности (постоянно выполняемые действия)
- Вызов или создание дочерних служб диаграммы состояний
- Поддержка нескольких слушателей для переходов состояний, изменений контекста, событий и т. д.

```js
import { createMachine, interpret } from 'xstate';

const machine = createMachine(/* machine config */);

// Interpret the machine, and add a listener for whenever a transition occurs.
const service = interpret(machine).onTransition((state) => {
  console.log(state.value);
});

// Start the service
service.start();

// Send events
service.send({ type: 'SOME_EVENT' });

// Stop the service when you are no longer using it.
service.stop();
```

## Отправка событий

События отправляются в работающую службу путем вызова `service.send(event)`. Событие можно отправить тремя способами:

```js hl_lines="4 8 12"
service.start();

// As an object (preferred):
service.send({ type: 'CLICK', x: 40, y: 21 });

// As a string:
// (same as service.send({ type: 'CLICK' }))
service.send('CLICK');

// As a string with an object payload:
// (same as service.send({ type: 'CLICK', x: 40, y: 21 }))
service.send('CLICK', { x: 40, y: 21 });
```

- Как объект события (например, `.send({ type: 'CLICK', x: 40, y: 21 })`)
  : - Объект события должен иметь строковое свойство `type: ...`.
- Как строка (например, `.send('CLICK')`, что равносильно отправке `{ type: 'CLICK' }`)
  : - Строка представляет тип события.
- В виде строки, за которой следует полезная нагрузка в виде объекта (например, `.send('CLICK', { x: 40, y: 21 })`), реализовано _начиная с версии 4.5+_
  : - Первый строковый аргумент представляет тип события.
  : - Второй аргумент должен быть объектом без свойства `type: ...`

!!!warning "Внимание"

    Если служба не инициализирована (то есть, если `service.start()` еще не был вызван), события будут **отложены** до запуска службы. Это означает, что события не будут обрабатываться до тех пор, пока не будет вызван `service.start()`, а затем все они будут последовательно обработаны.

    Это поведение можно изменить, установив `{deferEvents: false}` в параметрах службы. Когда `deferEvents` имеет значение `false`, отправка события неинициализированной службе вызовет ошибку.

## Пакетные события

Несколько событий можно отправить в виде группы или «пакета» в работающую службу, вызвав `service.send(events)` с массивом событий:

```js
service.send([
  // String events
  'CLICK',
  'CLICK',
  'ANOTHER_EVENT',
  // Event objects
  { type: 'CLICK', x: 40, y: 21 },
  { type: 'KEYDOWN', key: 'Escape' },
]);
```

Это немедленно запланирует последовательную обработку всех пакетных событий. Поскольку каждое событие вызывает переход состояния, который может иметь действия для выполнения, действия в промежуточных состояниях откладываются до тех пор, пока все события не будут обработаны, а затем они выполняются в состоянии, в котором они были созданы (а не в конечном состоянии).

Это означает, что конечное состояние (после обработки всех событий) будет иметь массив `.actions` _всех_ накопленных действий из промежуточных состояний. Каждое из этих действий будет связано с соответствующими промежуточными состояниями.

!!!warning "Внимание"

    Только одно состояние — **конечное состояние** (т. е. результирующее состояние после обработки всех событий) — будет отправлено слушателю `.onTransition(...)`. Это делает пакетные события оптимальным подходом для повышения производительности.

!!!tip "Подсказка"

    Пакетные события полезны для подходов к [поиску событий](https://martinfowler.com/eaaDev/EventSourcing.html). Журнал событий может быть сохранен, а затем воспроизведен путем отправки пакетных событий службе для достижения того же состояния.

## Переходы

Слушатели для переходов между состояниями регистрируются с помощью метода `.onTransition(...)`, который принимает прослушиватель состояния. Слушатели состояния вызываются каждый раз, когда происходит переход состояния (включая начальное состояние) с экземпляром текущего состояния:

```js
// Interpret the machine
const service = interpret(machine);

// Add a state listener, which is called whenever a state transition occurs.
service.onTransition((state) => {
  console.log(state.value);
});

service.start();
```

!!!tip "Подсказка"

    Если вы хотите, чтобы обработчики `.onTransition (...)` вызывались только при изменении состояния (то есть, когда изменяется `state.value`, изменяется `state.context` или появляются новые `state.actions`), используйте [`state.changed`](states.md#state-changed):

    ```js hl_lines="2"
    service.onTransition((state) => {
    	if (state.changed) {
    		console.log(state.value);
    	}
    });
    ```

!!!tip "Подсказка"

    Обратный вызов `.onTransition()` не будет выполняться между переходами без событий или другими микрошагами. Он работает только на макрошагах. Микрошаги — это промежуточные переходы между макрошагами.

## Запуск и остановка

Службу можно инициализировать (т. е. запустить) и остановить с помощью `.start()` и `.stop()`. Вызов `.start()` немедленно переведет службу в исходное состояние. Вызов `.stop()` удалит всех слушателей из службы и выполнит любую очистку слушателей, если это возможно.

```js
const service = interpret(machine);

// Start the machine
service.start();

// Stop the machine
service.stop();

// Restart the machine
service.start();
```

Службы можно запускать из определенного [состояния](states.md), передав состояние в `service.start(state)`. Это полезно при восстановлении сервиса из ранее сохраненного состояния.

```js
// Starts the service from the specified state,
// instead of from the machine's initial state.
service.start(previousState);
```

## Выполнение действий

[Действия](actions.md) (побочные эффекты) по умолчанию выполняются сразу после перехода состояния. Это можно настроить, установив параметр `{execute: false}`. Каждый объект действия, указанный в `state`, может иметь свойство `.exec`, которое вызывается с контекстом состояния `context` и объектом события `event`.

Действия можно выполнить вручную, вызвав `service.execute(state)`. Это полезно, когда вы хотите контролировать выполнение действий:

```js
const service = interpret(machine, {
  execute: false, // do not execute actions on state transitions
});

service.onTransition((state) => {
  // execute actions on next animation frame
  // instead of immediately
  requestAnimationFrame(() => service.execute(state));
});

service.start();
```

## Параметры

Следующие параметры могут быть переданы интерпретатору в качестве второго аргумента (`interpret(machine, options)`):

- `execute` (boolean) — Указывает, следует ли выполнять действия состояния при переходе. По-умолчанию `true`.
- `deferEvents` (boolean) — Указывает, должны ли события, отправленные в неинициализированную службу (т. е. до вызова `service.start()`), откладываться до инициализации службы. По умолчанию `true`.
  : - Если `false`, события, отправленные в неинициализированную службу, вызовут ошибку.
- `devTools` (boolean) — Указывает, следует ли отправлять события в расширение [Redux DevTools](https://github.com/zalmoxisus/redux-devtools-extension). По-умолчанию — `false`.
- `logger` — Задает средство ведения журнала, которое будет использоваться для действий `log(...)`. По-умолчанию используется собственный метод `console.log`.
- `clock` — Задает [интерфейс часов](delays.md#interpretation) для отложенных действий. По-умолчанию используются собственные функции `setTimeout` и `clearTimeout`.

## Пользовательские интерпретаторы

Вы можете использовать любой интерпретатор (или создать свой собственный) для запуска вашего конечного автомата / диаграммы состояний. Вот пример минимальной реализации, демонстрирующий, насколько гибкой может быть интерпретация (несмотря на количество шаблонов):

```js
const machine = createMachine(/* machine config */);

// Keep track of the current state, and start
// with the initial state
let currentState = machine.initialState;

// Keep track of the listeners
const listeners = new Set();

// Have a way of sending/dispatching events
function send(event) {
  // Remember: machine.transition() is a pure function
  currentState = machine.transition(currentState, event);

  // Get the side-effect actions to execute
  const { actions } = currentState;

  actions.forEach((action) => {
    // If the action is executable, execute it
    typeof action.exec === 'function' && action.exec();
  });

  // Notify the listeners
  listeners.forEach((listener) => listener(currentState));
}

function listen(listener) {
  listeners.add(listener);
}

function unlisten(listener) {
  listeners.delete(listener);
}

// Now you can listen and send events to update state
listen((state) => {
  console.log(state.value);
});

send('SOME_EVENT');
```

## Примечания

- Функция `interpret` экспортируется непосредственно из `xstate` начиная с версии 4.3+ (т. е. `import { interpret } from 'xstate'`). Для предыдущих версий он импортируется из `'xstate/lib/interpreter'`.
- Большинство методов интерпретатора можно объединить в цепочку:

```js
const service = interpret(machine)
  .onTransition((state) => console.log(state))
  .onDone(() => console.log('done'))
  .start(); // returns started service
```

- Не вызывайте `service.send(...)` непосредственно из действий. Это затрудняет тестирование, визуализацию и анализ. Вместо этого используйте [`invoke`](communication.md).
