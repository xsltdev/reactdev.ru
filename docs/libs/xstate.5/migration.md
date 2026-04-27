---
title: Миграция с XState v4 на v5
---

В приведенном ниже руководстве объясняется, как перейти с XState версии 4 на версию 5. Миграция с XState v4 на v5 должна быть простым процессом. Если вы застряли или у вас возникли вопросы, обратитесь к команде Stately в [нашем Discord](https://discord.gg/xstate).

!!! note "Примечание"

    Прочтите [запись в блоге Дэвида о запуске XState v5](https://stately.ai/blog/2023-12-01-xstate-v5).

Это руководство предназначено для разработчиков, которые хотят обновить свою кодовую базу с версии 4 до версии 5, а также будет полезно для всех разработчиков, желающих узнать различия между версией 4 и версии 5.

!!! note "Примечание"

    Предпочитаете видео? [Посмотрите наш вебинар по XState v5 на YouTube](https://www.youtube.com/live/TRVjeil-y74).

## XState v5 и TypeScript

XState v5 и связанные с ним библиотеки написаны на TypeScript и используют сложные типы, чтобы обеспечить вам максимальную безопасность типов и логический вывод. **XState v5 требует TypeScript версии 5.0 или более поздней.** Для достижения наилучших результатов используйте последнюю версию TypeScript.

Следуйте этим рекомендациям, чтобы убедиться, что ваш проект TypeScript готов к использованию XState v5:

-   Используйте последнюю версию TypeScript, версию 5.0 или более позднюю (обязательно).

```bash
  npm install typescript@latest --save-dev
```

-   Установите для параметра [`strictNullChecks`](https://www.typescriptlang.org/tsconfig#strictNullChecks) значение `true` в вашем файле `tsconfig.json`. Это обеспечит правильную работу наших типов, а также поможет обнаружить ошибки в вашем коде (настоятельно рекомендуется).

```json5
// tsconfig.json
{
    compilerOptions: {
        // ...
        strictNullChecks: true,
        // or set `strict` to true, which includes `strictNullChecks`
        // "strict": true
    },
}
```

-   Установите для параметра [`skipLibCheck`](https://www.typescriptlang.org/tsconfig#skipLibCheck) значение `true` в вашем файле `tsconfig.json` (рекомендуется).

## Создание машин и актеров

### Используйте `createMachine()`, а не `Machine()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Функция Machine(config) теперь называется createMachine(config):

=== "XState v5"

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    // ...
});
```

=== "XState v4"

```ts
// ❌ DEPRECATED
import { Machine } from 'xstate';

const machine = Machine({
    // ...
});
```

### Используйте `createActor()`, а не `interpret()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Функция `interpret()` была переименована в `createActor()`:

=== "XState v5"

```ts
import { createMachine, createActor } from 'xstate';

const machine = createMachine(/* ... */);

// ✅
const actor = createActor(machine, {
    // actor options
});
```

=== "XState v4"

```ts
import { createMachine, interpret } from 'xstate';

const machine = createMachine(/* ... */);

// ❌ DEPRECATED
const actor = interpret(machine, {
    // actor options
});
```

### Используйте `machine.provide()`, а не `machine.withConfig()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Методmachine.withConfig() был переименован вmachine.provide():

=== "XState v5"

```ts
// ✅
const specificMachine = machine.provide({
    actions: {
        /* ... */
    },
    guards: {
        /* ... */
    },
    actors: {
        /* ... */
    },
    // ...
});
```

=== "XState v4"

```ts
// ❌ DEPRECATED
const specificMachine = machine.withConfig({
    actions: {
        /* ... */
    },
    guards: {
        /* ... */
    },
    services: {
        /* ... */
    },
    // ...
});
```

### Установите контекст с помощью `input`, а не `machine.withContext()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Метод `machine.withContext(...)` больше нельзя использовать, поскольку `context` больше нельзя переопределить напрямую. Вместо этого используйте [input](input.md):

=== "XState v5"

```ts
// ✅
const machine = createMachine({
    context: ({ input }) => ({
        actualMoney: Math.min(input.money, 42),
    }),
});

const actor = createActor(machine, {
    input: {
        money: 1000,
    },
});
```

=== "XState v4"

```ts
// ❌ DEPRECATED
const machine = createMachine({
    context: {
        actualMoney: 0,
    },
});

const moneyMachine = machine.withContext({
    actualMoney: 1000,
});
```

### Действия упорядочены по умолчанию, `predictableActionArguments` больше не требуется

!!! warning "Критическое изменение"

    Несовместимое изменение.

По умолчанию действия теперь располагаются в предсказуемом порядке, поэтому флаг `predictableActionArguments` больше не требуется. Действия назначения всегда будут выполняться в том порядке, в котором они определены.

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	entry: [
    		({ context }) => {
    			console.log(context.count); // 0
    		},
    		assign({ count: 1 }),
    		({ context }) => {
    			console.log(context.count); // 1
    		},
    		assign({ count: 2 }),
    		({ context }) => {
    			console.log(context.count); // 2
    		},
    	],
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	predictableActionArguments: true,
    	entry: [
    		(context) => {
    			console.log(context.count); // 0
    		},
    		assign({ count: 1 }),
    		(context) => {
    			console.log(context.count); // 1
    		},
    		assign({ count: 2 }),
    		(context) => {
    			console.log(context.count); // 2
    		},
    	],
    });
    ```

### Функция `spawn()` удалена.

Вместо использования импортированной функции spawn() для создания актеров внутри действий Assign(...):

-   Используйте создатель действия `spawnChild(...)` (предпочтительно)
-   Или используйте метод spawn(...)` из первого аргумента, переданного функции присваивания внутри действий assign(...)` (полезно, если вам нужна ссылка на актера в `context`)

Прочтите документацию по [порождению актеров](spawn.md) для получения дополнительной информации.

=== "XState v5"

    ```ts
    // ✅
    import { spawnChild, assign } from 'xstate';

    // Spawning a direct child:
    const machine1 = createMachine({
    	// ...
    	entry: spawnChild('someChildLogic', {
    		id: 'someChild',
    	}),
    });

    // Spawning a child with the actor ref in `context`:
    const machine2 = createMachine({
    	// ...
    	entry: assign({
    		child: ({ spawn }) => spawn('someChildLogic'),
    	}),
    });
    ```

=== "XState v4"

    ```ts
    // ❌
    import { assign, spawn } from 'xstate';

    const machine = createMachine({
    	// ...
    	entry: assign({
    		child: () => spawn('someChildLogic'),
    	}),
    });
    ```

### Используйте `getNextSnapshot(…)` вместо `machine.transition(…)`

Метод `machine.transition(…)` теперь требует "области действия актера" для третьего аргумента, который создается внутри `createActor(…)`. Вместо этого используйте `getNextSnapshot(…)`, чтобы получить следующий снимок из некоторой логики актера на основе текущего снимка и события:

=== "XState v5"

    ```ts
    // ✅
    import { createMachine, getNextSnapshot } from 'xstate';

    const machine = createMachine({
    	// ...
    });
    const nextState = getNextSnapshot(
    	machine,
    	machine.resolveState({ value: 'green' }),
    	{ type: 'timer' }
    );

    nextState.value; // yellow
    ```

=== "XState v4"

    ```ts
    // ❌
    import { createMachine } from 'xstate';

    const machine = createMachine({
    	// ...
    });

    const nextState = machine.transition('green', {
    	type: 'timer',
    });

    nextState.value; // yellow
    ```

### Отправлять события явно вместо использования `autoForward`

Свойство autoForward в конфигурациях вызова было удалено. Вместо этого отправляйте события явно.

В общем, _не_ рекомендуется пересылать все события актеру. Вместо этого пересылайте только те события, которые нужны актеру.

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	invoke: {
    		src: 'someSource',
    		id: 'someId',
    	},
    	always: {
    		// Forward events to the invoked actor
    		// This will not cause an infinite loop in XState v5
    		actions: sendTo('someId', ({ event }) => event),
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌
    const machine = createMachine({
    // ...
    invoke: {
    	src: 'someSource',
    	id: 'someId'
    	autoForward: true // deprecated
    }
    });
    ```

## Штаты

### Используйте `state.getMeta()` вместо `state.meta`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство `state.meta` было переименовано в `state.getMeta()`:

=== "XState v5"

    ```ts
    // ✅
    state.getMeta();
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    state.meta;
    ```

### Метод `state.toStrings()` был удален.

!!! warning "Критическое изменение"

    Несовместимое изменение.

```ts
import { type StateValue } from 'xstate';

export function getStateValueStrings(stateValue: StateValue): string[] {
  if (typeof stateValue === 'string') {
    return [stateValue];
  }
  const valueKeys = Object.keys(stateValue);

  return valueKeys.concat(
    ...valueKeys.map((key) =>
      getStateValueStrings(stateValue[key]!).map((s) => key + '.' + s),
    ),
  );
}

// ...

const stateValueStrings = getStateValueStrings(stateValue);
// e.g. ['green', 'yellow', 'red', 'red.walk', 'red.wait', …]
```

### Используйте `state._nodes` вместо `state.configuration`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство `state.configuration` было переименовано в `state._nodes`:

=== "XState v5"

    ```ts
    // ✅
    state._nodes;
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    state.configuration;
    ```

### Чтение событий из API проверки вместо `state.events`

Свойство `state.events` было удалено, поскольку события не являются частью состояния, если вы явно не добавите их в `context` состояния. Вместо этого используйте [inspection API](inspection.md) для наблюдения за событиями или явно добавьте событие в `context` состояния:

=== "XState v5"

    ```ts
    // ✅
    import { createActor } from 'xstate';
    import { someMachine } from './someMachine';

    const actor = createActor(someMachine, {
    	inspect: (inspEvent) => {
    		if (inspEvent.type === '@xstate.event') {
    			console.log(inspEvent.event);
    		}
    	},
    });
    ```

=== "XState v5 (контекст)"

    ```ts
    // ✅
    import { setup, createActor } from 'xstate';

    const someMachine = setup({
    	// ...
    	actions: {
    		recordEvent: assign({
    			event: ({ event }) => event,
    		}),
    	},
    }).createMachine({
    	context: { event: undefined },
    	on: {
    		someEvent: {
    			// ...
    			actions: ['recordEvent'],
    		},
    	},
    });

    const someActor = createActor(someMachine);
    someActor.subscribe((snapshot) => {
    	console.log(snapshot.context.event);
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    import { interpret } from 'xstate';
    import { someMachine } from './someMachine';

    const actor = interpret(someMachine);
    actor.subscribe((state) => {
    	console.log(state.event); // Removed
    });
    ```

## События и переходы

### Функции реализации получают один аргумент

!!! warning "Критическое изменение"

    Несовместимое изменение.

Функции реализации теперь принимают один аргумент: объект с контекстом, событием и другими свойствами.

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	entry: ({ context, event }) => {
    		// ...
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	entry: (context, event) => {
    		// ...
    	},
    });
    ```

### `send()` удален; используйте `raise()` или `sendTo()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Создатель действия `send(...)` удален. Вместо этого используйте `raise(...)` для отправки событий себе или `sendTo(...)` для отправки событий другим актерам.

Прочтите документацию по действию [`sendTo`](actions.md#send-to-action) и [действию `raise`](actions.md#raise-action) для получения дополнительной информации.

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	entry: [
    		// Send an event to self
    		raise({ type: 'someEvent' }),

    		// Send an event to another actor
    		sendTo('someActor', { type: 'someEvent' }),
    	],
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	entry: [
    		// Send an event to self
    		send({ type: 'someEvent' }),

    		// Send an event to another actor
    		send({ type: 'someEvent' }, { to: 'someActor' }),
    	],
    });
    ```

**Совет перед переносом.** Обновите проекты версии 4, чтобы использовать sendTo или Raise вместо send.

### Используйте `enqueueActions()` вместо `pure()` и `choose()`

Методы `pure()` и `choose()` были удалены. Вместо этого используйте enqueueActions().

Для действий `pure()`:

=== "XState v5"

    ```ts
    // ✅
    entry: [
    	enqueueActions(({ context, event, enqueue }) => {
    		enqueue('action1');
    		enqueue('action2');
    	}),
    ];
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    entry: [
    	pure(() => {
    		return ['action1', 'action2'];
    	}),
    ];
    ```

Для действий `choose()`:

=== "XState v5"

    ```ts
    // ✅
    entry: [
    	enqueueActions(({ enqueue, check }) => {
    		if (check('someGuard')) {
    			enqueue('action1');
    			enqueue('action2');
    		}
    	}),
    ];
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    entry: [
    	choose([
    		{
    			guard: 'someGuard',
    			actions: ['action1', 'action2'],
    		},
    	]),
    ];
    ```

### `actor.send()` больше не принимает строковые типы

!!! warning "Критическое изменение"

    Несовместимое изменение.

Строковые типы событий больше нельзя отправлять, например, `actor.send(event)`; вместо этого вы должны отправить объект события:

=== "XState v5"

    ```ts
    // ✅
    actor.send({ type: 'someEvent' });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    actor.send('someEvent');
    ```

**Совет перед переносом:** Обновите проекты версии 4, чтобы передать объект в `.send()`.

### `state.can()` больше не принимает строковые типы

!!! warning "Критическое изменение"

    Несовместимое изменение.

Строковые типы событий больше нельзя отправлять, например, в `state.can(event)`; вместо этого вы должны отправить объект события:

=== "XState v5"

    ```ts
    // ✅
    state.can({ type: 'someEvent' });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    state.can('someEvent');
    ```

### Защищенные переходы используют `guard`, а не `cond`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство перехода cond для защищенных переходов теперь называется Guard:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	on: {
    		someEvent: {
    			guard: 'someGuard',
    			target: 'someState',
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	on: {
    		someEvent: {
    			// renamed to `guard` in v5
    			cond: 'someGuard',
    			target: 'someState',
    		},
    	},
    });
    ```

### Используйте `params` для передачи параметров действиям и охранникам

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойства, отличные от `type` для объектов действия и объектов защиты, должны быть вложены в свойство `params`; `{ type: 'someType', message: 'hello' }` становится `{ type: 'someType', params: { message: 'hello' }}`. Эти параметры затем передаются во второй аргумент реализации действия или защиты:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	entry: {
    		type: 'greet',
    		params: {
    			message: 'Hello world',
    		},
    	},
    	on: {
    		someEvent: {
    			guard: {
    				type: 'isGreaterThan',
    				params: { value: 42 },
    			},
    		},
    	},
    }).provide({
    	actions: {
    		greet: ({ context, event }, params) => {
    			console.log(params.message); // 'Hello world'
    		},
    	},
    	guards: {
    		isGreaterThan: ({ context, event }, params) => {
    			return event.value > params.value;
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine(
    	{
    		entry: {
    			type: 'greet',
    			message: 'Hello world',
    		},
    		on: {
    			someEvent: {
    				cond: { type: 'isGreaterThan', value: 42 },
    			},
    		},
    	},
    	{
    		actions: {
    			greet: (context, event, { action }) => {
    				console.log(action.message); // 'Hello world'
    			},
    		},
    		guards: {
    			isGreaterThan: (context, event, { guard }) => {
    				return event.value > guard.value;
    			},
    		},
    	}
    );
    ```

**Совет перед переносом.** Обновите объекты действий и защиты в проектах версии 4, чтобы переместить свойства (кроме типа) в объект Params.

### Используйте переходы с подстановочными знаками `*`, а не строгий режим

!!! warning "Критическое изменение"

    Несовместимое изменение.

Строгий режим удален. Если вы хотите генерировать необработанные события, вам следует использовать переход с подстановочными знаками:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	on: {
    		knownEvent: {
    			// ...
    		},
    		'*': {
    			// unknown event
    			actions: ({ event }) => {
    				throw new Error(
    					`Unknown event: ${event.type}`
    				);
    			},
    		},
    	},
    });

    const actor = createActor(machine);

    actor.subscribe({
    	error: (err) => {
    		console.error(err);
    	},
    });

    actor.start();

    actor.send({ type: 'unknownEvent' });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	strict: true,
    	on: {
    		knownEvent: {
    			// ...
    		},
    	},
    });

    const service = interpret(machine);

    service.send({ type: 'unknownEvent' });
    ```

### Используйте явные бессобытийные («всегда») переходы

!!! warning "Критическое изменение"

    Несовместимое изменение.

Бессобытийные («всегда») переходы теперь должны определяться через свойство «всегда: { ... }» узла состояния; их больше нельзя определить с помощью пустой строки:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	states: {
    		someState: {
    			always: {
    				target: 'anotherState',
    			},
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	states: {
    		someState: {
    			on: {
    				'': {
    					target: 'anotherState',
    				},
    			},
    		},
    	},
    });
    ```

**Совет перед переносом.** Обновите проекты версии 4, чтобы использовать параметр «всегда» для переходов _eventless_.

### Используйте `reenter: true`, а не `internal: false`

!!! warning "Критическое изменение"

    Несовместимое изменение.

`internal: false` теперь `reenter: true`

Внешние переходы, ранее заданные с помощью «internal: false», теперь указываются с помощью «reenter: true»:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	on: {
    		someEvent: {
    			target: 'sameState',
    			reenter: true,
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	on: {
    		someEvent: {
    			target: 'sameState',
    			internal: false,
    		},
    	},
    });
    ```

### Переходы по умолчанию внутренние, а не внешние

!!! warning "Критическое изменение"

    Несовместимое изменение.

Все переходы являются **внутренними по умолчанию**. Это изменение актуально для переходов, определенных на узлах состояния с действиями «вход» или «выход», вызванными актерами или отложенными переходами («после»). Если вы полагались на предыдущее поведение XState v4, где переходы неявно повторно входили в узел состояния, используйте `reenter: true`:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			entry: 'someAction',
    			on: {
    				someEvent: {
    					target: 'compoundState.childState',
    					// Reenters the `compoundState` state,
    					// just like an external transition
    					reenter: true,
    				},
    				selfEvent: {
    					target: 'childState',
    					reenter: true,
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {},
    			},
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			entry: 'someAction',
    			on: {
    				someEvent: {
    					// implicitly external
    					target: 'compoundState.childState', // non-relative target
    				},
    				selfEvent: {
    					target: 'compoundState',
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {},
    			},
    		},
    	},
    });
    ```

---

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			after: {
    				1000: {
    					target: 'compoundState.childState',
    					reenter: true, // make it external explicitly!
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {},
    			},
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			after: {
    				1000: {
    					// implicitly external
    					target: 'compoundState.childState', // non-relative target
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {},
    			},
    		},
    	},
    });
    ```

### Дочерние узлы состояния всегда вводятся повторно

!!! warning "Критическое изменение"

    Несовместимое изменение.

Дочерние узлы состояния всегда вводятся повторно, когда на них нацелены переходы (как внешние, так и внутренние), определенные на узлах составного состояния. Это изменение актуально только в том случае, если дочерний узел состояния имеет действия «входа» или «выхода», вызванных актеров или отложенных переходов («после»). Добавьте защиту `stateIn`, чтобы предотвратить нежелательный повторный вход в дочернее состояние:

=== "XState v5"

    ```ts
    // ✅

    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			on: {
    				someEvent: {
    					guard: not(
    						stateIn({
    							compoundState: 'childState',
    						})
    					),
    					target: '.childState',
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {
    					entry: 'someAction',
    				},
    			},
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED

    const machine = createMachine({
    	// ...
    	states: {
    		compoundState: {
    			on: {
    				someEvent: {
    					// Implicitly internal; childState not re-entered
    					target: '.childState',
    				},
    			},
    			initial: 'childState',
    			states: {
    				childState: {
    					entry: 'someAction',
    				},
    			},
    		},
    	},
    });
    ```

### Используйте `stateIn()` для проверки переходов состояний, а не `in`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство перехода `in: 'someState'` удалено. Вместо этого используйте `guard:stateIn(...)`:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	on: {
    		someEvent: {
    			guard: stateIn({ form: 'submitting' }),
    			target: 'someState',
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    on: {
    	someEvent: {
    	in: '#someMachine.form.submitting'
    	target: 'someState',
    	},
    },
    });
    ```

### Используйте `actor.subscribe()` вместо `state.history`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство `state.history` удалено. Если вам нужен предыдущий снимок, вам следует сохранить его через `actor.subscribe(...)`.

=== "XState v5"

    ```ts
    // ✅
    let previousSnapshot = actor.getSnapshot();

    actor.subscribe((snapshot) => {
    	doSomeComparison(previousSnapshot, snapshot);
    	previousSnapshot = snapshot;
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    actor.subscribe((state) => {
    	doSomeComparison(state.history, state);
    });
    ```

**Совет перед переносом:** Обновите проекты версии 4, чтобы отслеживать историю с помощью actor.subscribe().

### Действия могут выбрасывать ошибки без `escalate`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Создатель действия «эскалация» удален. В XState v5 действия могут вызывать ошибки, и они будут распространяться ожидаемым образом. Ошибки можно обрабатывать с помощью перехода onError.

=== "XState v5"

    ```ts
    // ✅
    const childMachine = createMachine({
    	// This will be sent to the parent machine that invokes this child
    	entry: () => {
    		throw new Error('This is some error');
    	},
    });

    const parentMachine = createMachine({
    	invoke: {
    		src: childMachine,
    		onError: {
    			actions: ({ context, event }) => {
    				console.log(event.error);
    				//  {
    				//    type: ...,
    				//    error: {
    				//      message: 'This is some error'
    				//    }
    				//  }
    			},
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const childMachine = createMachine({
    	entry: escalate('This is some error'),
    });

    /* ... */
    ```

## Актеры

### Используйте создатели логики актеров для `invoke.src` вместо функций {#use-actor-logic-creators-for-invokesrc-instead-of-functions}

!!! warning "Критическое изменение"

    Несовместимое изменение.

Доступные создатели логики актеров:

-   `createMachine`
-   `fromPromise`
-   `fromObservable`
-   `fromEventObservable`
-   `fromTransition`
-   `fromCallback`

Дополнительную информацию см. в разделе [Актеры](actors.md).

=== "XState v5"

    ```ts
    // ✅
    import { fromPromise, setup } from 'xstate';

    const machine = setup({
    	actors: {
    		getUser: fromPromise(
    			async ({
    				input,
    			}: {
    				input: { userId: string };
    			}) => {
    				const data = await getData(input.userId);
    				// ...
    				return data;
    			}
    		),
    	},
    }).createMachine({
    	invoke: {
    		src: 'getUser',
    		input: ({ context, event }) => ({
    			userId: context.userId,
    		}),
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    import { createMachine } from 'xstate';

    const machine = createMachine({
    	invoke: {
    		src: (context) => async () => {
    			const data = await getData(context.userId);

    			// ...
    			return data;
    		},
    	},
    });
    ```

---

=== "XState v5"

    ```ts
    // ✅
    import { fromCallback, createMachine } from 'xstate';

    const machine = createMachine({
    	invoke: {
    		src: fromCallback(
    			({ sendBack, receive, input }) => {
    				// ...
    			}
    		),
    		input: ({ context, event }) => ({
    			userId: context.userId,
    		}),
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    import { createMachine } from 'xstate';

    const machine = createMachine({
    	invoke: {
    		src: (context, event) => (sendBack, receive) => {
    			// context.userId
    			// ...
    		},
    	},
    });
    ```

---

=== "XState v5"

    ```ts
    // ✅
    import { fromEventObservable, createMachine } from 'xstate';
    import { interval, mapTo } from 'rxjs';

    const machine = createMachine({
    	invoke: {
    		src: fromEventObservable(() =>
    			interval(1000).pipe(mapTo({ type: 'tick' }))
    		),
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    import { createMachine } from 'xstate';
    import { interval, mapTo } from 'rxjs';

    const machine = createMachine({
    	invoke: {
    		src: () =>
    			interval(1000).pipe(mapTo({ type: 'tick' })),
    	},
    });
    ```

### Используйте `invoke.input` вместо `invoke.data`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство invoke.data удалено. Если вы хотите предоставить контекст вызываемым актерам, используйте invoke.input:

=== "XState v5"

    ```ts
    // ✅
    const someActor = createMachine({
    	// The input must be consumed by the invoked actor:
    	context: ({ input }) => input,
    	// ...
    });

    const machine = createMachine({
    	// ...
    	invoke: {
    		src: 'someActor',
    		input: {
    			value: 42,
    		},
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const someActor = createMachine({
    	// ...
    });

    const machine = createMachine({
    	// ...
    	invoke: {
    		src: 'someActor',
    		data: {
    			value: 42,
    		},
    	},
    });
    ```

### Используйте `output` в конечных состояниях вместо `data`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Чтобы получить выходные данные от машины, которая достигла своего конечного состояния, используйте свойство верхнего уровня «output» вместо «data»:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	states: {
    		finished: {
    			type: 'final',
    		},
    	},
    	output: {
    		answer: 42,
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	states: {
    		finished: {
    			type: 'final',
    			data: {
    				answer: 42,
    			},
    		},
    	},
    });
    ```

Чтобы обеспечить динамически генерируемый вывод, замените `invoke.data` на `invoke.output` и добавьте свойство `output` верхнего уровня:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	states: {
    		finished: {
    			type: 'final',
    			output: ({ event }) => ({
    				answer: event.someValue,
    			}),
    		},
    	},
    	output: ({ event }) => event.output,
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    // ...
    states: {
    	finished: {
    	type: 'final',
    	data: (context, event) => {
    		answer: event.someValue,
    	},
    	},
    },
    });
    ```

### Не используйте преобразователи свойств во входных и выходных данных.

!!! warning "Критическое изменение"

    Несовместимое изменение.

Если вы хотите предоставить динамический контекст вызываемым актерам или создать динамический вывод из конечных состояний, используйте функцию вместо объекта с преобразователями свойств.

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	// ...
    	invoke: {
    		src: 'someActor',
    		input: ({ context, event }) => ({
    			value: event.value,
    		}),
    	},
    });

    // The input must be consumed by the invoked actor:
    const someActor = createMachine({
    	// ...
    	context: ({ input }) => input,
    });

    // Producing machine output
    const machine = createMachine({
    	// ...
    	states: {
    		finished: {
    			type: 'final',
    		},
    	},
    	output: ({ context, event }) => ({
    		answer: context.value,
    	}),
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	// ...
    	invoke: {
    		src: 'someActor',
    		data: {
    			value: (context, event) => event.value, // a property mapper
    		},
    	},
    });

    // Producing machine output
    const machine = createMachine({
    	// ...
    	states: {
    		finished: {
    			type: 'final',
    			data: {
    				answer: (context, event) => context.value, // a property mapper
    			},
    		},
    	},
    });
    ```

### Используйте свойство `actors` для объекта `options` вместо `services`

!!! warning "Критическое изменение"

    Несовместимое изменение.

`services` были переименованы в `actors`:

=== "XState v5"

    ```ts
    // ✅
    const specificMachine = machine.provide({
    	actions: {
    		/* ... */
    	},
    	guards: {
    		/* ... */
    	},
    	actors: {
    		/* ... */
    	},
    	// ...
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const specificMachine = machine.withConfig({
    	actions: {
    		/* ... */
    	},
    	guards: {
    		/* ... */
    	},
    	services: {
    		/* ... */
    	},
    	// ...
    });
    ```

### Для изменений используйте `subscribe()`, а не `onTransition()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Метод `actor.onTransition(...)` удален. Вместо этого используйте `actor.subscribe(...)`.

=== "XState v5"

    ```ts
    // ✅
    const actor = createActor(machine);
    actor.subscribe((state) => {
    	// ...
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const actor = interpret(machine);
    actor.onTransition((state) => {
    	// ...
    });
    ```

### `createActor()` (ранее `interpret()`) принимает второй аргумент для восстановления состояния

!!! warning "Критическое изменение"

    Несовместимое изменение.

`interpret(machine).start(state)` теперь называется `createActor(machine, { snapshot }).start()`

Чтобы восстановить актера в определенном состоянии, теперь вам следует передать это состояние как свойство snapshot аргумента options функции createActor(logic, options) . Свойство «actor.start()» больше не принимает аргумент «state».

=== "XState v5"

    ```ts
    // ✅
    const actor = createActor(machine, { snapshot: someState });
    actor.start();
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const actor = interpret(machine);
    actor.start(someState);
    ```

### Используйте `actor.getSnapshot()`, чтобы получить состояние актера

!!! warning "Критическое изменение"

    Несовместимое изменение.

Подписка на актера (`actor.subscribe(...)`) после запуска актера больше не будет немедленно создавать текущий снимок. Вместо этого прочитайте текущий снимок из `actor.getSnapshot()`:

=== "XState v5"

    ```ts
    // ✅
    const actor = createActor(machine);
    actor.start();

    const initialState = actor.getSnapshot();

    actor.subscribe((state) => {
    	// Snapshots from when the subscription was created
    	// Will not emit the current snapshot until a transition happens
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const actor = interpret(machine);
    actor.start();

    actor.subscribe((state) => {
    	// Current snapshot immediately emitted
    });
    ```

### Перебор событий вместо использования `actor.batch()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Метод `actor.batch([...])` для пакетной обработки событий удален.

=== "XState v5"

    ```ts
    // ✅
    for (const event of events) {
    	actor.send(event);
    }
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    actor.batch(events);
    ```

**Совет перед переносом.** Обновите проекты версии 4, чтобы обеспечить циклическую обработку событий и отправку их в виде пакета.

### Используйте `snapshot.status === 'done'` вместо `snapshot.done`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство snapshot.done, которое ранее было в объекте моментального снимка акторов конечного автомата, удалено. Вместо этого используйте `snapshot.status === 'done'`, который доступен всем актерам:

=== "XState v5"

    ```ts
    // ✅
    const actor = createActor(machine);
    actor.start();

    actor.subscribe((snapshot) => {
    	if (snapshot.status === 'done') {
    		// ...
    	}
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const actor = interpret(machine);
    actor.start();

    actor.subscribe((state) => {
    	if (state.done) {
    		// ...
    	}
    });
    ```

### `state.nextEvents` был удален

!!! warning "Критическое изменение"

    Несовместимое изменение.

Свойство `state.nextEvents` удалено, поскольку оно не является полностью безопасным/надежным способом определения следующих событий, которые могут быть отправлены актеру. Если вы хотите получить следующие события в соответствии с предыдущим поведением, вы можете использовать эту вспомогательную функцию:

    ```ts
    import type { AnyMachineSnapshot } from 'xstate';

    function getNextEvents(snapshot: AnyMachineSnapshot) {
    	return [
    		...new Set([
    			...snapshot._nodes.flatMap(
    				(sn) => sn.ownEvents
    			),
    		]),
    	];
    }

    // Instead of `state.nextEvents`:
    const nextEvents = getNextEvents(state);
    ```

## Типскрипт

### Используйте `types` вместо `schema`

!!! warning "Критическое изменение"

    Несовместимое изменение.

СвойствоmachineConfig.schema переименовано вmachineConfig.types:

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	types: {} as {
    		context: {
    			/* ...*/
    		};
    		events: {
    			/* ...*/
    		};
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	schema: {} as {
    		context: {
    			/* ...*/
    		};
    		events: {
    			/* ...*/
    		};
    	},
    });
    ```

### Используйте `types.typegen` вместо `tsTypes`

!!! warning "Критическое изменение"

    Несовместимое изменение.

!!! note "Примечание"

    XState Typegen пока не полностью поддерживает XState v5. Тем не менее, машины со строгой типизацией все же можно создать и без Typegen.

Свойство «machineConfig.tsTypes» было переименовано и теперь находится в «machineConfig.types.typegen».

=== "XState v5"

    ```ts
    // ✅
    const machine = createMachine({
    	types: {} as {
    		typegen: {};
    		context: {
    			/* ...*/
    		};
    		events: {
    			/* ...*/
    		};
    	},
    });
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    const machine = createMachine({
    	tsTypes: {};
    	schema: {} as {
    		context: {
    		/* ...*/
    		};
    		events: {
    		/* ...*/
    		};
    	},
    });
    ```

## `@xstate/реагировать`

### `useInterpret()` теперь называется `useActorRef()`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Хук `useInterpret()`, который используется для возврата `actorRef` ("сервиса" в XState v4), переименован в `useActorRef()`.

=== "XState v5"

    ```ts
    // ✅
    import { useActorRef } from '@xstate/react';

    const actorRef = useActorRef(machine); // or any other logic
    ```

=== "XState v4"

    ```ts
    // ❌ DEPRECATED
    import { useInterpret } from '@xstate/react';

    const service = useInterpret(machine);
    ```

### `useActor(logic)` теперь принимает логику актера, а не актера

!!! warning "Критическое изменение"

    Несовместимое изменение.

Хук `useActor(logic)` теперь принимает _actor logic_ (например, `fromPromise(...)`, `createMachine(...)` и т.д.) вместо существующего `ActorRef`.

Чтобы использовать существующий ActorRef, используйтеactor.send(...)` для отправки событий и useSelector(actor, ...)` для получения снимка:

=== "XState v5"

    ```tsx
    // ✅
    import { useSelector } from '@xstate/react';

    function Component({ someActorRef }) {
    	const state = useSelector(someActorRef, (s) => s);

    	return (
    		<button
    			onClick={() =>
    				someActorRef.send({ type: 'someEvent' })
    			}
    		/>
    	);
    }
    ```

=== "XState v4"

    ```tsx
    // ❌ DEPRECATED
    import { useActor } from '@xstate/react';

    function Component({ someActorRef }) {
    	const [state, send] = useActor(someActorRef);

    	return (
    		<button
    			onClick={() => send({ type: 'someEvent' })}
    		/>
    	);
    }
    ```

## Используйте `machine.provide()` для предоставления реализаций в хуках

!!! warning "Критическое изменение"

    Несовместимое изменение.

Для динамического создания машин с предоставленными реализациями перехватчики `useMachine(...)`, `useActor(...)` и `useActorRef(...)` больше не принимают:

-   Ленивые создатели машин как первый аргумент
-   Реализации, переданные во второй аргумент

Вместо этого `machine.provide(...)` следует передать непосредственно в первый аргумент.

Пакет `@xstate/react` считает машины с одинаковой конфигурацией одной и той же машиной, поэтому он сводит к минимуму повторную отрисовку, но при этом поддерживает актуальность предоставленных реализаций.

=== "XState v5"

    ```tsx
    // ✅
    import { useMachine } from '@xstate/react';
    import { someMachine } from './someMachine';

    function Component(props) {
    	const [state, send] = useMachine(
    		someMachine.provide({
    			actions: {
    				doSomething: () => {
    					props.onSomething?.(); // Kept up-to-date
    				},
    			},
    		})
    	);

    	// ...
    }
    ```

=== "XState v4"

    ```tsx
    // ❌ DEPRECATED
    import { useMachine } from '@xstate/react';
    import { someMachine } from './someMachine';

    function Component(props) {
    	const [state, send] = useMachine(someMachine, {
    		actions: {
    			doSomething: () => {
    				props.onSomething?.();
    			},
    		},
    	});

    	// ...
    }
    ```

=== "XState v4"

    ```tsx
    // ❌ DEPRECATED
    import { useMachine } from '@xstate/react';
    import { someMachine } from './someMachine';

    function Component(props) {
    	const [state, send] = useMachine(() =>
    		someMachine.withConfig({
    			actions: {
    				doSomething: () => {
    					props.onSomething?.();
    				},
    			},
    		})
    	);

    	// ...
    }
    ```

## `@xstate/vue`

### `useMachine()` теперь возвращает `snapshot` вместо `state` и `actor` вместо `service`

!!! warning "Критическое изменение"

    Несовместимое изменение.

Чтобы сохранить согласованность именования с остальной частью XState и связанными с ней библиотеками:

-   «состояние» теперь является «снимком»
-   «сервис» теперь является «актером»

=== "XState v5"

    ```tsx
    // ✅
    import { useMachine } from '@xstate/vue';

    // ...

    const {
    	snapshot, // Renamed from `state`
    	send,
    	actor, // Renamed from `service`
    } = useMachine(someMachine);
    ```

=== "XState v4"

    ```tsx
    // ❌ DEPRECATED
    import { useMachine } from '@xstate/vue';

    // ...

    const {
    	state, // Renamed to `snapshot` in @xstate/vue 3.0.0
    	send,
    	service, // Renamed to `actor` in @xstate/vue 3.0.0
    } = useMachine(someMachine);
    ```

## Новые возможности

-   [Создать системы актеров](system.md)
-   [Новые создатели логики актеров](./actors.md#actor-logic-creators)
-   [Глубокое сохранение для вызванных и порожденных актеров](persistence.md)
-   [Предоставить входные данные конечным автоматам и актерам](input.md)
-   [Укажите выходные данные «готово» для актеров](output.md)
-   [Частичные дескрипторы событий (частичные подстановочные знаки)](./transitions.md#partial-wildcard-transitions)
-   [Действия постановки в очередь](./actions.md#enqueue-actions)
-   [Охранники более высокого уровня](./guards.md#higher-level-guards)
-   [API настройки для указания типов и строго типизированных значений состояния](./machines.md#providing-implementations)
-   [Проверить API](inspection.md)

## Часто задаваемые вопросы

### Когда Stately Studio будет совместима с XState v5?

В настоящее время мы работаем над совместимостью [Stately Studio](https://stately.ai/docs/studio) с XState v5. Экспорт в XState v5 (JavaScript или TypeScript) уже доступен. Мы работаем над поддержкой новых функций XState v5, таких как защита высшего порядка, частичные подстановочные знаки событий и машинный ввод/вывод.

Проголосуйте или прокомментируйте [Совместимость Stately Studio + XState v5 в нашей дорожной карте](https://feedback.stately.ai/editor/p/stately-studio-xstate-v5-compatibility), чтобы оставаться в курсе нашего прогресса.

### Когда расширение XState VS Code будет совместимо с XState v5?

[Расширение XState VS Code](https://marketplace.visualstudio.com/items?itemName=statelyai.stately-vscode) пока не совместимо с XState v5. Продление является для нас приоритетом, и работа уже ведется.

Проголосуйте или прокомментируйте [совместимость XState v5 для расширения VS Code в нашей дорожной карте](https://feedback.stately.ai/devtools/p/xstate-v5-compatibility-for-vs-code-extension), чтобы оставаться в курсе нашего прогресса.

### Когда в XState v5 появится typegen?

Вывод TypeScript был значительно улучшен в XState v5. Благодаря таким функциям, как API `setup()` и динамическим параметрам, основные варианты использования typegen больше не нужны.

Однако мы понимаем, что у typegen все еще могут быть некоторые конкретные варианты использования. Проголосуйте или прокомментируйте [Typegen для XState v5 в нашей дорожной карте](https://feedback.stately.ai/xstate/p/typegen-for-xstate-v5), чтобы оставаться в курсе нашего прогресса.

### Как я могу использовать XState v4 и v5?

Вы можете использовать XState v4 и v5 в одном проекте, что полезно для постепенного перехода на XState v5. Чтобы использовать оба варианта, добавьте «xstate5»: «npm:xstate@5» в свой «package.json» вручную или через CLI:

```bash
npm i xstate5@npm:xstate@5
```

Затем вы можете импортировать версию XState v5 в свой код:

```ts
import { createMachine } from 'xstate5';
// or { createMachine as createMachine5 } from 'xstate5';
```

Если вам нужно использовать разные версии пакета интеграции, например `@xstate/react`, вы можете использовать стратегию, аналогичную описанной выше, но вам нужно будет указать правильную версию XState в пакете интеграции. Это можно сделать с помощью скрипта:

```bash
npm i xstate5@npm:xstate@5 @xstate5/react@npm:@xstate/react@4 --force
```

```js
// scripts/xstate5-react-script.js
const fs = require('fs-extra');
const path = require('path');

const rootNodeModules = path.join(
    __dirname,
    '..',
    'node_modules'
);

fs.ensureSymlinkSync(
    path.join(rootNodeModules, 'xstate5'),
    path.join(
        rootNodeModules,
        '@xstate5',
        'react',
        'node_modules',
        'xstate'
    )
);
```

```json5
// package.json
"scripts": {
  "postinstall": "node scripts/xstate5-react-script.js"
}
```

Затем вы можете использовать в своем коде совместимую с XState v5 версию `@xstate/react`:

```ts
import { useMachine } from '@xstate5/react';
// or { useMachine as useMachine5 } from '@xstate5/react';
import { createMachine } from 'xstate5';
// or { createMachine as createMachine5 } from 'xstate5';

// ...
```
