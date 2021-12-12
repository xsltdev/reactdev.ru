# Модели

В XState вы можете моделировать контекст `context` и события `event` автомата извне, используя `createModel(...)`. Это обеспечивает удобный способ строгого ввода контекста и событий, а также помощников для создания, назначения событий и других деталей реализации в будущем.

Использование `createModel(...)` _совершенно необязательно_ и предназначено для улучшения взаимодействия с разработчиками. Основные причины его использования:

- Разделение и организация контекста и событий строго типизированным способом
- Предотвращение проблем с вводом текста с помощью `assign(...)`
- Указание создателей событий для более простого и безопасного создания событий
- Возможность совместного использования модели с другими машинами
- Будущие улучшения взаимодействия с разработчиками, такие как определение действий, защитных функций и т. д.

## `createModel(...)`

Функция `createModel(...)` принимает:

| Параметр         | Тип    | Описание                                       |
| ---------------- | ------ | ---------------------------------------------- |
| `initialContext` | object | Начальное значение контекста                   |
| `creators?`      | object | Объект, содержащий различные создатели событий |

Объект `creators` содержит свойства:

| Свойство | Тип    | Описание                             |
| -------- | ------ | ------------------------------------ |
| `events` | object | Объект, содержащий создатели событий |

Ключи объекта `creators.events` — это типы событий, а значения — это функции, которые принимают любое количество аргументов и возвращают данные события.

## Моделирование контекста

Поскольку модель определяет контекст автомата, модель можно использовать для определении автомата, чтобы установить ее начальный контекст с помощью `model.initialContext` и обновить контекст автомата с помощью `model.assign`.

Функция `model.assign` типизирована в соответствии с формой контекста модели, что делает ее удобной и надежной заменой действия `assign`.

```js
import { createModel } from 'xstate/lib/model';

const userModel = createModel({
  name: 'Someone',
  age: 0,
});

// ...

const machine = userModel.createMachine({
  context: userModel.initialContext,
  // ...
  entry: userModel.assign({ name: '' }),
});
```

## Моделирование событий

Моделирование событий автомата в модели дает два преимущества:

- События можно создавать, вызывая `model.events.eventName(...)`
- Предоставляет информацию о типе для определения автомата, обеспечивая безопасность типов для определений действий

```ts
import { createModel } from 'xstate/lib/model';

const userModel = createModel(
  // Initial context
  {
    name: 'David',
    age: 30,
  },
  {
    // Event creators
    events: {
      updateName: (value) => ({ value }),
      updateAge: (value) => ({ value }),
      anotherEvent: () => ({}), // no payload
    },
  }
);

const machine = userModel.createMachine(
  {
    context: userModel.initialContext,
    initial: 'active',
    states: {
      active: {
        on: {
          updateName: {
            actions: userModel.assign({
              name: (_, event) => event.value,
            }),
          },
          updateAge: {
            actions: 'assignAge',
          },
        },
      },
    },
  },
  {
    actions: {
      assignAge: userModel.assign({
        age: (_, event) => event.value, // inferred
      }),
    },
  }
);

// This sends the following event:
// {
//   type: 'updateName',
//   value: 'David'
// }
const nextState = machine.transition(
  undefined,
  userModel.events.updateName('David')
);
```

## TypeScript

Функция `createModel(...)` определяет следующие типы:

- `context` выводится из первого аргумента в `createModel(initialContext, creators)`
- `event` выводятся из `creators.events` в `createModel(initialContext, creators)`

```ts
import { createModel } from 'xstate/lib/model';

const userModel = createModel(
  {
    name: 'David', // inferred as `string`
    age: 30, // inferred as `number`
    friends: [] as string[], // explicit type
  },
  {
    events: {
      updateName: (value: string) => ({ value }),
      updateAge: (value: number) => ({ value }),
      anotherEvent: () => ({}), // no payload
    },
  }
);

// Context inferred as:
// {
//   name: string;
//   age: number;
//   friends: string[];
// }

// Events inferred as:
// | { type: 'updateName'; value: string; }
// | { type: 'updateAge'; value: number; }
// | { type: 'anotherEvent'; }
```

### Создание автомата из модели

Вместо того, чтобы явно указывать тип контекста и события как параметры типа в `createMachine<TContext, TEvent>(...)`, следует использовать метод `model.createMachine(...)`:

```ts hl_lines="1"
const machine = userModel.createMachine({
  context: userModel.initialContext,
  initial: 'active',
  states: {
    active: {
      on: {
        updateName: {
          actions: userModel.assign({
            name: (_, event) => event.value, // inferred
          }),
        },
      },
    },
  },
});
```

### Сужение типов события

Когда действие `assign()` упоминается в `options.actions`, вы можете сузить тип события, которое передается в действие вторым аргументом `model.assign(assignments, eventType)`:

```ts
const assignAge = userModel.assign(
  {
    // The `event.type` here is restricted to "updateAge"
    age: (_, event) => event.value, // inferred as `number`
  },
  'updateAge' // Restricts the `event` allowed by the "assignAge" action
);

const machine = userModel.createMachine({
  context: userModel.initialContext,
  initial: 'active',
  states: {
    active: {
      on: {
        updateAge: {
          actions: assignAge,
        },
      },
    },
  },
});
```

!!!warning "Внимание"

    Назначенные действия с суженными типами событий _нельзя_ помещать в свойство `actions: {...}` параметров автомата в `createMachine(configuration, options)`. Это связано с тем, что действия в `options.actions` должны предполагать потенциально получение _любого_ события, даже если конфигурация машины предполагает иное.

### Извлечение типов из модели

_Начиная с версии 4.22.1_

Вы можете извлечь типы контекста и событий из модели, используя типы `ContextFrom<T>` и `EventFrom<T>`:

```ts hl_lines="1 15-16"
import { ContextFrom, EventFrom } from 'xstate';
import { createModel } from 'xstate/lib/model';

const someModel = createModel(
  {
    /* ... */
  },
  {
    events: {
      /* ... */
    },
  }
);

type SomeContext = ContextFrom<typeof someModel>;
type SomeEvent = EventFrom<typeof someModel>;
```
