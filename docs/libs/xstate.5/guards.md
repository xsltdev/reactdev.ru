---
title: Условия
---

**Условие** (guard) — это функция-условие, которую машина проверяет при обработке события. Если условие равно `true`, машина следует переходу в следующее состояние. Если условие равно `false`, машина следует остальным условиям к следующему состоянию.

**Защищённый переход** — это переход, который активен только если его `guard` вычисляется как `true`. Условие определяет, может ли переход быть активирован. Любой переход может быть защищённым переходом.

Условия должны быть чистыми, синхронными функциями, возвращающими либо `true`, либо `false`.

```ts
const feedbackMachine = createMachine(
    {
        // ...
        states: {
            form: {
                on: {
                    'feedback.submit': {
                        guard: 'isValid',
                        target: 'submitting',
                    },
                },
            },
            submitting: {
                // ...
            },
        },
    },
    {
        guards: {
            isValid: ({ context }) => {
                return context.feedback.length > 0;
            },
        },
    }
);
```

<iframe src="https://stately.ai/registry/editor/embed/c447d996-cef1-421d-a422-8be695668764?mode=design&machineId=2e91a914-7f83-45fe-9216-e1b5c495a44a" width="100%" height="400"></iframe>

## Множественные защищённые переходы

Если вы хотите, чтобы одно событие переходило в разные состояния в определённых ситуациях, вы можете предоставить массив защищённых переходов. Каждый переход будет проверяться по порядку, и первый переход, чей `guard` вычисляется как `true`, будет выполнен.

Вы можете указать переход по умолчанию как последний переход в массиве. Если ни одно из условий не вычисляется как `true`, будет выполнен переход по умолчанию.

```ts
const feedbackMachine = createMachine({
    // ...
    prompt: {
        on: {
            'feedback.provide': [
                // Выполняется, если условие 'sentimentGood' равно `true`
                {
                    guard: 'sentimentGood',
                    target: 'thanks',
                },
                // Выполняется, если ни один из вышеуказанных защищённых переходов не был выполнен
                // и если условие 'sentimentBad' равно `true`
                {
                    guard: 'sentimentBad',
                    target: 'form',
                },
                // Переход по умолчанию
                { target: 'form' },
            ],
        },
    },
});
```

## Встроенные условия

Вы можете определить условия как встроенную функцию. Это полезно для быстрого прототипирования, но мы обычно рекомендуем использовать сериализованные условия (строки или объекты) для лучшей переиспользуемости и визуализации.

```ts
on: {
  event: {
    guard: ({ context, event }) => true,
    target: 'someState'
  }
}
```

## Объект условия

Условие может быть определено как объект с `type`, который является типом условия, ссылающимся на предоставленную реализацию условия, и необязательным `params`, который может быть прочитан реализованным условием:

```ts
const feedbackMachine = createMachine(
    {
        // ...
        states: {
            // ...
            form: {
                on: {
                    submit: {
                        guard: {
                            type: 'isValid',
                            params: { maxLength: 50 },
                        },
                        target: 'submitting',
                    },
                },
            },
            // ...
        },
    },
    {
        guards: {
            isValid: ({ context }, params) => {
                return (
                    context.feedback.length > 0 &&
                    context.feedback.length <=
                        params.maxLength
                );
            },
        },
    }
);
```

Условия могут быть позже предоставлены или переопределены путём предоставления пользовательских реализаций условий в методе `.provide()`:

```ts
const feedbackActor = createActor(
    feedbackMachine.provide({
        guards: {
            isValid: ({ context }, params) => {
                return (
                    context.feedback.length > 0 &&
                    context.feedback.length <=
                        params.maxLength &&
                    isNotSpam(context.feedback)
                );
            },
        },
    })
).start();
```

## Условия высшего порядка

XState предоставляет условия высшего порядка, которые являются условиями, композирующими другие условия. Есть три условия высшего порядка — `and`, `or` и `not`:

-   `and([...])` — вычисляется как `true`, если все условия в `and([...guards])` вычисляются как `true`
-   `or([...])` — вычисляется как `true`, если _любое_ условие в `or([...guards])` вычисляется как `true`
-   `not(...)` — вычисляется как `true`, если условие в `not(guard)` вычисляется как `false`

```ts
on: {
    event: {
        guard: and(['isValid', 'isAuthorized']);
    }
}
```

Условия высшего порядка могут быть комбинированы:

```ts
on: {
    event: {
        guard: and([
            'isValid',
            or(['isAuthorized', 'isGuest']),
        ]);
    }
}
```

## Условия проверки состояния

Вы можете использовать условие `stateIn(stateValue)` для проверки, соответствует ли текущее состояние предоставленному `stateValue`. Это наиболее полезно для [параллельных состояний](parallel-states.md).

```ts
on: {
  event: {
    guard: stateIn('#state1');
  },
  anotherEvent: {
    guard: stateIn({ form: 'submitting' })
  }
}
```

Условия проверки состояния соответствуют состоянию всей машины, а не узла состояния. Обычно нет необходимости использовать условия проверки состояния для обычных состояний. Сначала попробуйте смоделировать переходы в ваших машинах состояний так, чтобы вам не нужно было использовать условия проверки состояния.

## Сокращения

Рекомендуется определять условия как объекты условий, например, `{ type: 'someGuard', params: { ... } }`. Однако, если условие не имеет параметров, вы можете указать его как строку:

```ts
on: {
    someEvent: {
        // Эквивалентно:
        // guard: { type: 'someGuard' }
        guard: 'someGuard';
    }
}
```

## Условия и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать `guards` вашей машины, настроив их реализации в `setup({ guards: { … } })`. Вы можете предоставить тип `params` во втором аргументе функции условия:

```ts
import { setup } from 'xstate';

const machine = setup({
    guards: {
        isGreaterThan: (
            _,
            params: { count: number; min: number }
        ) => {
            return params.count > params.min;
        },
    },
}).createMachine({
    // ...
    on: {
        someEvent: {
            guard: {
                type: 'isGreaterThan',
                // Строго типизированные параметры
                params: ({ event }) => ({
                    count: event.count,
                    min: 10,
                }),
            },
            // ...
        },
    },
});
```

## Шпаргалка по условиям

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine(
    {
        // ...
        states: {
            form: {
                on: {
                    'feedback.submit': {
                        guard: 'isValid',
                        target: 'submitting',
                    },
                },
            },
            submitting: {
                // ...
            },
        },
    },
    {
        guards: {
            isValid: ({ context }) => {
                return context.feedback.length > 0;
            },
        },
    }
);
```

### Шпаргалка: множественные защищённые переходы

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
    // ...
    prompt: {
        on: {
            'feedback.provide': [
                // Выполняется, если условие 'sentimentGood' равно `true`
                {
                    guard: 'sentimentGood',
                    target: 'thanks',
                },
                // Выполняется, если ни один из вышеуказанных защищённых переходов не был выполнен
                // и если условие 'sentimentBad' равно `true`
                {
                    guard: 'sentimentBad',
                    target: 'form',
                },
                // Переход по умолчанию
                { target: 'form' },
            ],
        },
    },
});
```

### Шпаргалка: условия высшего порядка

```ts
import { createMachine, and } from 'xstate';

const loginMachine = createMachine({
    on: {
        event: {
            guard: and(['isValid', 'isAuthorized']);
        },
    },
});
```

### Шпаргалка: комбинированные условия высшего порядка

```ts
import { createMachine, and, or } from 'xstate';

const loginMachine = createMachine({
    on: {
        event: {
            guard: and(['isValid', or(['isAuthorized', 'isGuest'])]);
        },
    },
});
```
