---
title: Состояние
---

Состояние описывает статус или режим автомата, который может быть таким простым, как _Пауза_ и _Воспроизведение_. Конечный автомат может находиться только в одном состоянии в каждый момент времени.

Эти состояния «конечны»; автомат может переходить только между состояниями, которые вы предварительно определили.

<iframe loading="lazy" src="https://stately.ai/registry/editor/embed/e13bef2b-bb13-4465-96ac-0bc25340688e?machineId=741f69fd-7f01-4932-9407-6871e225bb6d&amp;colorMode=light" class="embed_rxbU" width="100%" height="500"></iframe>

!!!tip "Совет"

    Посмотрите наше видео ["Что такое состояния?" на YouTube](https://www.youtube.com/watch?v=z-6yhmSWUcc&list=PLvWgkXBB3dd4I_l-djWVU2UGPyBgKfnTQ&index=2) (53 сек).

## Объект состояния

Объект состояния представляет текущее состояние работающего автомата ([актора](actor-model.md)) и содержит следующие свойства:

-   **`value`**: текущее значение состояния, которое является либо:
    -   строкой, представляющей простое состояние, например `'playing'`, или:
    -   объектом, представляющим вложенные состояния, например `{ paused: 'buffering' }`.
-   **`context`**: текущий [context](context.md) (расширенное состояние).
-   **`meta`**: объект, содержащий метаданные узла состояния.

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'question',
    context: {
        feedback: '',
    },
    states: {
        question: {
            meta: {
                question: 'Как прошёл ваш опыт?',
            },
        },
    },
});

const actor = createActor(feedbackMachine);
actor.start();

console.log(actor.getSnapshot());
// Выводит объект, содержащий:
// {
//   value: 'question',
//   context: {
//     feedback: ''
//   },
//   meta: {
//     'feedback.question': {
//       question: 'Как прошёл ваш опыт?'
//     }
//   }
// }
```

## Доступ к снимкам состояния

Вы можете получить доступ к сгенерированному состоянию актора (или _снимку_), подписавшись на актора или прочитав метод `.getSnapshot()`.

```ts
const actor = createActor(feedbackMachine);

actor.subscribe((snapshot) => {
    console.log(snapshot);
    // выводит текущий снимок состояния, например:
    // { value: 'question', ... }
    // { value: 'thanks', ... }
});

actor.start();

console.log(actor.getSnapshot());
// выводит { value: 'question', ... }
```

## Значение состояния

Конечный автомат с вложенными состояниями (или _[диаграмма состояний](state-machines-and-statecharts.md#what-is-a-statechart)_) представляет собой древовидную структуру, где каждый узел является _узлом состояния_. Корневой узел состояния — это узел верхнего уровня, представляющий весь автомат. Корневой узел может иметь дочерние узлы состояний, которые могут иметь дочерние узлы состояний и так далее.

**Значение состояния** — это объект, представляющий все активные узлы состояний в автомате. Для конечных автоматов с узлами состояний без дочерних узлов значение состояния является строкой:

Скоро появится визуальный пример.

-   `state.value === 'question'`
-   `state.value === 'thanks'`
-   `state.value === 'closed'`

Для конечных автоматов с родительскими узлами состояний значение состояния является объектом:

Скоро появится визуальный пример.

-   `state.value === { form: 'invalid' }` — это представляет конечный автомат с активным дочерним узлом с ключом `form`, который имеет активный дочерний узел с ключом `invalid`

Для конечных автоматов с [параллельными узлами состояний](parallel-states.md) значение состояния содержит объект(ы) с несколькими ключами для каждого региона узла состояния:

```ts
state.value ===
    {
        monitor: 'on',
        mode: 'dark',
    };
```

Конечные автоматы также могут не иметь узлов состояний, кроме корневого узла. Для таких автоматов значение состояния равно `null`.

## Context состояния

Конечные автоматы могут иметь [context](context.md) — объект, представляющий расширенное состояние автомата. Context неизменяем и может быть обновлён только путём [присваивания](actions.md#assign-action) в действии. Вы можете прочитать свойство `state.context`, чтобы получить текущий context.

```ts
const currentState = feedbackActor.getSnapshot();

console.log(currentState.context);
// выводит { feedback: '' }
```

-   Объект пуст `{}` (по умолчанию), если `context` не указан в конфигурации автомата
-   Никогда не изменяйте этот объект напрямую; его следует рассматривать как неизменяемый/только для чтения

## Дочерние элементы состояния

Свойство `state.children` представляет всех текущих порождённых/вызванных акторов в текущем состоянии. Это объект с ключами, представляющими ID акторов, и значениями, представляющими экземпляры `ActorRef`.

-   Здесь вы получаете доступ к порождённым/вызванным акторам по их ID
-   Поэтому вам следует давать порождённым/вызванным акторам ID
-   Остановленные акторы не будут отображаться здесь

## `state.can(eventType)`

Метод `state.can(event)` определяет, вызовет ли объект `event` изменение состояния, если он будет отправлен актору автомата. Метод вернёт `true`, если состояние изменится в результате отправки `event`; в противном случае метод вернёт `false`:

```js
const feedbackMachine = createMachine({
    // ...
    states: {
        form: {
            // ...
            on: {
                'feedback.submit': {
                    guard: 'isValid',
                    target: 'thanks',
                },
            },
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

// ...

const currentState = feedbackActor.getSnapshot();

console.log(currentState.can({ type: 'feedback.submit' }));
// выводит `true`, если событие 'feedback.submit' вызовет переход, что произойдёт, если:
// - текущее состояние — 'form'
// - условие 'isValid' вычисляется в `true`
```

Состояние считается «изменённым», если для данного `state` и объекта `event` активирован переход.

!!!warning "Внимание"

    Метод `state.can(...)` также проверит условия переходов, выполняя их. Условия переходов должны быть чистыми функциями.

## `state.hasTag(tag)`

Метод `state.hasTag(tag)` определяет, имеет ли какой-либо узел состояния в текущем значении состояния заданный `tag`. Это полезно для определения, является ли состояние конкретным состоянием или принадлежит ли состояние к определённой группе состояний.

```js
const feedbackMachine = createMachine({
    // ...
    states: {
        submitting: {
            tags: ['loading'],
            // ...
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

const currentState = feedbackActor.getSnapshot();

const showLoadingSpinner = currentState.hasTag('loading');
```

Предпочитайте использовать `state.hasTag(tag)` вместо `state.matches(stateValue)`, так как `state.hasTag(tag)` более устойчив к изменениям в автомате.

## `state.matches(stateValue)`

Метод `state.matches(stateValue)` определяет, _соответствует_ ли текущее `state.value` заданному `stateValue`. Если текущее `state.value` является «подмножеством» предоставленного `stateValue`, то метод вернёт `true`.

```ts
// state.value === 'question'
state.matches('question'); // true

// state.value === { form: 'invalid' }
state.matches('form'); // true
state.matches('question'); // false
state.matches({ form: 'invalid' }); // true
state.matches({ form: 'valid' }); // false

// state.value === { 'form submitting' : 'invalid value' }
state.matches('form submitting'); // true
state.matches('form'); // false
state.matches({ 'form submitting': 'invalid value' }); // true
state.matches({ 'form submitting': 'value' }); // false
```

## `state.output`

Свойство `state.output` представляет выходные данные конечного автомата, когда он находится в финальном состоянии верхнего уровня; т.е. `state.status === 'done'`.

```ts
const state = actor.getSnapshot();

if (state.status === 'done') {
    console.log(state.output);
}
```

## `state.getMeta()`

Метод `state.getMeta()` представляет метаданные всех узлов состояний в `state`. Это объект с ключами, представляющими ID узлов состояний, и значениями, которые являются метаданными этого узла состояния.

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    // ...
    states: {
        form: {
            meta: {
                view: 'shortForm',
            },
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

// Предположим, текущее состояние — 'form'
const currentState = feedbackActor.getSnapshot();
console.log(currentState.getMeta());
// выводит { 'feedback.form': { view:'shortForm' } }
```

## Описания состояний

Вы можете добавить `.description` к состояниям, чтобы описать их назначение и поделиться связанными заметками с вашей командой. В редакторе Stately Studio эти описания отображаются в автомате и поддерживают markdown, включая ссылки, изображения и списки. [Подробнее об описаниях в Stately Studio](descriptions.md).

```ts
states: {
  "Loading Move Destinations": {
    // highlight-start
    description:
      "Загрузка данных с сервера на основе id и типа сущности (проект или автомат). Результат включает текущее расположение сущности и список или дерево допустимых вариантов назначения, куда пользователь может переместить эту сущность.",
    // highlight-end
    invoke: {
      src: "loadMoveData",
      id: "loadMoveData",
      onDone: [
        {
          target: "Destination Menu",
          actions: "setDestinations",
        },
      ],
      onError: [
        {
          target: "Data Loading Error",
        },
      ],
    },
  },
}
```

## Шпаргалка по состояниям

### Шпаргалка: чтение или сопоставление значения состояния

```ts
const state = actor.getSnapshot();

const currentStateValue = state.value;

const isLoading = state.matches('loading');
```

### Шпаргалка: чтение context состояния

```ts
console.log(state.context);
```

### Шпаргалка: чтение output состояния

```ts
if (state.status === 'done') {
    // Output может существовать
    console.log(state.output);
} else {
    // Output не существует
    state.output === undefined;
}
```

### Шпаргалка: чтение метаданных состояния

```ts
console.log(state.getMeta());
```

## Дополнительные ресурсы

[Персистентность состояния](persistence.md)
