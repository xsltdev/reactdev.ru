---
title: Конечные состояния
---

**Конечное состояние** — это одно из возможных состояний, в котором машина состояний может находиться в любой момент времени. Оно называется «конечным», потому что машины состояний имеют известное ограниченное количество возможных состояний. Состояние представляет, как машина «ведёт себя» в этом состоянии; её статус или режим.

Например, в форме обратной связи вы можете находиться в состоянии заполнения формы или в состоянии отправки формы. Вы не можете одновременно заполнять форму и отправлять её; это «невозможное состояние».

Машины состояний всегда начинают с [начального состояния](initial-states.md) и могут заканчиваться в [финальном состоянии](final-states.md). Машина состояний всегда находится в конечном состоянии.

```ts
const feedbackMachine = createMachine({
    id: 'feedback',

    // Начальное состояние
    initial: 'prompt',

    // Конечные состояния
    states: {
        prompt: {
            /* ... */
        },
        form: {
            /* ... */
        },
        thanks: {
            /* ... */
        },
        closed: {
            /* ... */
        },
    },
});
```

Вы можете комбинировать конечные состояния с [контекстом](context.md), которые составляют общее состояние машины:

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    context: {
        name: '',
        email: '',
        feedback: '',
    },

    initial: 'prompt',
    states: {
        prompt: {
            /* ... */
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

// Конечное состояние
console.log(feedbackActor.getSnapshot().value);
// выводит 'prompt'

// Контекст ("расширенное состояние")
console.log(feedbackActor.getSnapshot().context);
// выводит { name: '', email: '', feedback: '' }
```

## Начальное состояние

Начальное состояние — это состояние, в котором машина начинает работу. Оно определяется свойством `initial` в конфигурации машины:

```ts
const feedbackMachine = createMachine({
    id: 'feedback',

    // Начальное состояние
    initial: 'prompt',

    // Конечные состояния
    states: {
        prompt: {
            /* ... */
        },
        // ...
    },
});
```

[Подробнее о начальных состояниях](initial-states.md).

## Узлы состояний

В XState **узел состояния** — это «узлы» конечных состояний, которые составляют всё дерево диаграммы состояний. Узлы состояний определяются в свойстве `states` других узлов состояний, включая корневую конфигурацию машины (которая сама является узлом состояния):

```ts
// Машина — это корневой узел состояния
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'prompt',

    // Узлы состояний
    states: {
        // Узел состояния
        prompt: {
            /* ... */
        },
        // Узел состояния
        form: {
            /* ... */
        },
        // Узел состояния
        thanks: {
            /* ... */
        },
        // Узел состояния
        closed: {
            /* ... */
        },
    },
});
```

## Теги

Узлы состояний могут иметь **теги** — строковые термины, которые помогают группировать или категоризировать узел состояния. Например, вы можете указать, какие узлы состояний представляют состояния, в которых загружаются данные, используя тег "loading", и определить, содержит ли состояние эти помеченные узлы состояний с помощью `state.hasTag(tag)`:

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'prompt',
    states: {
        prompt: {
            tags: ['visible'],
            // ...
        },
        form: {
            tags: ['visible'],
            // ...
        },
        thanks: {
            tags: ['visible', 'confetti'],
            // ...
        },
        closed: {
            tags: ['hidden'],
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

console.log(feedbackActor.getSnapshot().hasTag('visible'));
// выводит true
```

Подробнее о [тегах](tags.md).

## Метаданные

Метаданные — это статические данные, которые описывают соответствующие свойства узла состояния. Вы можете указать метаданные в свойстве `.meta` любого узла состояния. Это может быть полезно для отображения информации о узле состояния в UI или для генерации документации.

Свойство `state.meta` собирает данные `.meta` из всех активных узлов состояний и помещает их в объект с ID узла состояния в качестве ключа и данными `.meta` в качестве значения:

```ts
const feedbackMachine = createMachine({
    id: 'feedback',
    initial: 'prompt',
    meta: {
        title: 'Feedback',
    },
    states: {
        prompt: {
            meta: {
                content: 'How was your experience?',
            },
        },
        form: {
            meta: {
                content: 'Please fill out the form below.',
            },
        },
        thanks: {
            meta: {
                content: 'Thank you for your feedback!',
            },
        },
        closed: {},
    },
});

const feedbackActor = createActor(feedbackMachine).start();

console.log(feedbackActor.getSnapshot().meta);
// выводит объект:
// {
//   feedback: {
//     title: 'Feedback',
//   },
//   'feedback.prompt': {
//     content: 'How was your experience?',
//   }
// }
```

## Переходы

Переходы — это способ перехода от одного конечного состояния к другому. Они определяются свойством `on` на узле состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                'feedback.good': {
                    target: 'thanks',
                },
            },
        },
        thanks: {
            /* ... */
        },
        // ...
    },
});

const feedbackActor = createActor(feedbackMachine).start();

console.log(feedbackActor.getSnapshot().value);
// выводит 'prompt'

feedbackActor.send({ type: 'feedback.good' });

console.log(feedbackActor.getSnapshot().value);
// выводит 'thanks'
```

Подробнее о [событиях и переходах](transitions.md).

## Цели

Свойство `target` перехода определяет, куда машина должна перейти, когда переход выполняется. Обычно оно нацелено на соседний узел состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                'feedback.good': {
                    // Нацеливание на соседний узел состояния `thanks`
                    target: 'thanks',
                },
            },
        },
        thanks: {
            /* ... */
        },
        // ...
    },
});
```

`target` также может быть нацелен на потомка соседнего узла состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                'feedback.good': {
                    // Нацеливание на соседний узел состояния `thanks.happy`
                    target: 'thanks.happy',
                },
            },
        },
        thanks: {
            initial: 'normal',
            states: {
                normal: {},
                happy: {},
            },
        },
        // ...
    },
});
```

Когда целевой узел состояния является потомком исходного узла состояния, ключ исходного узла состояния можно опустить:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    // ...
    states: {
        closed: {
            initial: 'normal',
            states: {
                normal: {},
                keypress: {},
            },
        },
    },
    on: {
        'feedback.close': {
            // Нацеливание на потомка `closed`
            target: '.closed',
        },
        'key.escape': {
            // Нацеливание на потомка `closed.keypress`
            target: '.closed.keypress',
        },
    },
});
```

Когда узел состояния не изменяется; то есть исходный и целевой узлы состояния одинаковы, свойство `target` можно опустить:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    // ...
    states: {
        form: {
            on: {
                'feedback.update': {
                    // Цель не определена — остаёмся на узле состояния `form`
                    // Эквивалентно `target: '.form'` или `target: undefined`
                    actions: 'updateForm',
                },
            },
        },
    },
});
```

Узлы состояний также могут быть нацелены по их `id`, добавив к `target` префикс `#`, за которым следует `id` узла состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        closed: {
            id: 'finished',
        },
        // ...
    },
    on: {
        'feedback.close': {
            target: '#finished',
        },
    },
});
```

## Идентификация узлов состояний

Состояния могут быть идентифицированы уникальным ID: `id: 'myState'`. Это полезно для нацеливания на состояние из любого другого состояния, даже если они имеют разные родительские состояния:

```ts
import { createMachine, createActor } from 'xstate';

const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        // ...
        closed: {
            id: 'finished',
            type: 'final',
        },
        // ...
    },
    on: {
        'feedback.close': {
            // Нацеливание на состояние `.closed` по его ID
            target: '#finished',
        },
    },
});
```

ID состояний не влияют на `state.value`. В приведённом выше примере `state.value` всё равно будет `closed`, хотя узел состояния идентифицирован как `#finished`.

## Другие типы состояний

В диаграммах состояний есть другие типы состояний:

-   [Родительские состояния (также известные как составные состояния)](parent-states.md)
-   [Параллельные состояния](parallel-states.md)
-   [Состояния истории](history-states.md)
-   [Финальные состояния](final-states.md)

## Моделирование состояний

При проектировании конечных состояний для вашей машины состояний следуйте этим рекомендациям для создания поддерживаемых и эффективных машин состояний:

### Начните просто и неглубоко

-   **Начните с минимального количества состояний**: Не создавайте множество конечных состояний, пока не станет очевидно, что поведение вашей логики различается в зависимости от некоторого конечного состояния, в котором она может находиться.
-   **Избегайте преждевременной оптимизации**: Начните с базовых состояний и добавляйте сложность только при необходимости.
-   **Предпочитайте плоские структуры изначально**: Глубокая вложенность может быть добавлена позже, когда появятся паттерны.

### Идентифицируйте различное поведение

-   **Разное поведение = разное состояние**: Создавайте отдельные состояния, когда приложение ведёт себя по-разному в ответ на одно и то же событие.
-   **Одинаковое поведение = одно состояние**: Если несколько «состояний» обрабатывают события одинаково, они, вероятно, должны быть одним состоянием.
-   **Ставьте под вопрос невозможные состояния**: Спросите «может ли существовать эта комбинация условий?» Если нет, моделируйте их как отдельные состояния.

### Называйте состояния чётко

-   **Используйте описательные имена**: Имена состояний должны чётко описывать, что делает машина или в каком режиме она находится.
-   **Избегайте технического жаргона**: Используйте доменно-специфический язык, который понимают заинтересованные стороны.
-   **Будьте последовательны**: Используйте согласованные соглашения об именовании во всех ваших машинах состояний.

```ts
// ❌ Плохое именование
const machine = createMachine({
    initial: 'state1',
    states: {
        state1: {}, // Что это представляет?
        state2: {}, // Что это представляет?
        error: {}, // Слишком общее
    },
});

// ✅ Хорошее именование
const authMachine = createMachine({
    initial: 'signedOut',
    states: {
        signedOut: {},
        signingIn: {},
        signedIn: {},
        authenticationFailed: {}, // Конкретное состояние ошибки
    },
});
```

### Моделируйте пользовательские рабочие процессы

-   **Следуйте пути пользователя**: Состояния должны отражать естественную прогрессию действий пользователя.
-   **Учитывайте все пути**: Включайте счастливые пути, состояния ошибок и граничные случаи.
-   **Учитывайте состояния загрузки**: Асинхронные операции часто требуют промежуточных состояний.

```ts
const checkoutMachine = createMachine({
    initial: 'cart',
    states: {
        cart: {
            on: {
                PROCEED: { target: 'shippingInfo' },
            },
        },
        shippingInfo: {
            on: {
                CONTINUE: { target: 'paymentInfo' },
                BACK: { target: 'cart' },
            },
        },
        paymentInfo: {
            on: {
                SUBMIT: { target: 'processing' },
                BACK: { target: 'shippingInfo' },
            },
        },
        processing: {
            on: {
                SUCCESS: { target: 'confirmed' },
                FAILURE: { target: 'paymentFailed' },
            },
        },
        paymentFailed: {
            on: {
                RETRY: { target: 'paymentInfo' },
            },
        },
        confirmed: {
            type: 'final',
        },
    },
});
```

### Учитывайте временные аспекты

-   **Чувствительные ко времени состояния**: Моделируйте состояния, которые существуют определённое время.
-   **Обработка истечения**: Включайте состояния для обработки таймаутов и истечений.
-   **Запланированные переходы**: Используйте отложенные переходы для изменений состояния на основе времени.

### Группируйте связанную функциональность

-   **Используйте теги для категоризации**: Группируйте состояния по общим характеристикам.
-   **Рассмотрите родительские состояния**: Когда несколько состояний имеют общие переходы, рассмотрите их группировку под родительским состоянием.
-   **Разделяйте задачи**: Держите разные домены или функции в отдельных состояниях.

```ts
const appMachine = createMachine({
    initial: 'loading',
    states: {
        loading: {
            tags: ['busy'],
            on: {
                LOADED: { target: 'idle' },
                ERROR: { target: 'error' },
            },
        },
        idle: {
            tags: ['interactive'],
            on: {
                START_WORK: { target: 'working' },
            },
        },
        working: {
            tags: ['busy', 'interactive'],
            on: {
                COMPLETE: { target: 'idle' },
                CANCEL: { target: 'idle' },
            },
        },
        error: {
            tags: ['error'],
            on: {
                RETRY: { target: 'loading' },
            },
        },
    },
});
```

### Обрабатывайте граничные случаи

-   **Недопустимые состояния**: Моделируйте состояния для обработки недопустимых или неожиданных условий.
-   **Состояния восстановления**: Предоставляйте способы восстановления из состояний ошибок.
-   **Резервное поведение**: Включайте состояния по умолчанию для необработанных сценариев.

### Проверяйте переходы состояний

-   **Убедитесь, что все переходы имеют смысл**: Каждый переход состояния должен представлять допустимое изменение бизнес-логики.
-   **Избегайте циклических зависимостей**: Будьте осторожны с состояниями, которые могут бесконечно переходить друг в друга без цели.
-   **Рассмотрите защиты**: Используйте защиты для предотвращения недопустимых переходов, даже когда события получены.

### Документируйте назначение состояний

-   **Используйте описания**: Добавляйте свойства `.description` для объяснения сложных состояний.
-   **Включайте метаданные**: Храните соответствующую информацию о том, что представляет каждое состояние.
-   **Комментируйте сложную логику**: Объясняйте, почему определённые состояния существуют и что они выполняют.

```ts
const feedbackMachine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            description:
                'Waiting for user to indicate their satisfaction level',
            meta: {
                analytics: 'feedback_prompt_shown',
            },
        },
        collectingDetails: {
            description:
                'User provided negative feedback, collecting detailed information',
            meta: {
                analytics: 'detailed_feedback_form_shown',
            },
        },
    },
});
```

## Конечные состояния и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Вы можете строго типизировать конечные состояния вашей машины, используя функцию `setup(...)`, которая обеспечивает отличный вывод типов TypeScript и автодополнение:

```ts
import { setup, createActor } from 'xstate';

const feedbackMachine = setup({
    types: {
        context: {} as { feedback: string; rating: number },
        events: {} as
            | { type: 'feedback.good' }
            | { type: 'feedback.bad' }
            | { type: 'feedback.submit' },
    },
}).createMachine({
    id: 'feedback',
    initial: 'prompt',
    context: {
        feedback: '',
        rating: 0,
    },
    states: {
        prompt: {
            on: {
                'feedback.good': { target: 'thanks' },
                'feedback.bad': { target: 'form' },
            },
        },
        form: {
            on: {
                'feedback.submit': { target: 'thanks' },
            },
        },
        thanks: {
            type: 'final',
        },
    },
});

const feedbackActor = createActor(feedbackMachine).start();

// ✅ Типобезопасно и с автодополнением
const currentState = feedbackActor.getSnapshot();

// ✅ `state.matches(...)` типобезопасен с автодополнением
if (currentState.matches('prompt')) {
    // TypeScript знает, что мы в состоянии 'prompt'
}

// ✅ Все значения состояний имеют автодополнение
const isFormState = currentState.matches('form');
const isThanksState = currentState.matches('thanks');

// ✅ `state.value` также строго типизирован
const stateValue = currentState.value; // 'prompt' | 'form' | 'thanks'
```

При использовании `setup(...).createMachine(...)` TypeScript обеспечивает:

-   **Типобезопасное сопоставление состояний**: `state.matches(...)` с автодополнением для всех возможных значений состояний
-   **Строго типизированные значения состояний**: `state.value` типизирован как объединение всех возможных имён состояний
-   **Типобезопасный контекст**: Полный вывод типов для `state.context`
-   **Типобезопасные события**: `actor.send(...)` принимает только определённые типы событий

## Шпаргалка по конечным состояниям

### Шпаргалка: создание конечных состояний

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    id: 'feedback',
    initial: 'prompt',
    states: {
        prompt: {},
        form: {},
        thanks: {},
        closed: {},
    },
});
```

### Шпаргалка: конечные состояния с переходами

```ts
import { createMachine } from 'xstate';

const machine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            on: {
                'feedback.good': { target: 'thanks' },
                'feedback.bad': { target: 'form' },
            },
        },
        form: {
            on: {
                'feedback.submit': { target: 'thanks' },
            },
        },
        thanks: {},
    },
});
```

### Шпаргалка: чтение текущего состояния

```ts
const actor = createActor(machine).start();
const state = actor.getSnapshot();

// Чтение значения состояния
console.log(state.value); // например, 'prompt'

// Проверка, находимся ли в определённом состоянии
const isPromptState = state.matches('prompt');

// Проверка нескольких состояний
const isFormOrThanks =
    state.matches('form') || state.matches('thanks');
```

### Шпаргалка: состояния с тегами

```ts
const machine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            tags: ['visible', 'interactive'],
        },
        form: {
            tags: ['visible', 'interactive'],
        },
        thanks: {
            tags: ['visible', 'success'],
        },
        closed: {
            tags: ['hidden'],
        },
    },
});

// Проверка тегов
const state = actor.getSnapshot();
const isVisible = state.hasTag('visible');
const isInteractive = state.hasTag('interactive');
```

### Шпаргалка: состояния с метаданными

```ts
const machine = createMachine({
    initial: 'prompt',
    states: {
        prompt: {
            meta: {
                title: 'How was your experience?',
                component: 'PromptView',
            },
        },
        form: {
            meta: {
                title: 'Tell us more',
                component: 'FormView',
            },
        },
    },
});

// Чтение метаданных
const state = actor.getSnapshot();
console.log(state.getMeta());
```

### Шпаргалка: нацеливание состояний по ID

```ts
const machine = createMachine({
    initial: 'start',
    states: {
        start: {
            on: {
                FINISH: { target: '#completed' },
            },
        },
        process: {
            states: {
                step1: {},
                step2: {},
            },
        },
        done: {
            id: 'completed',
            type: 'final',
        },
    },
});
```

### Шпаргалка: строго типизированные конечные состояния

```ts
import { setup } from 'xstate';

const machine = setup({
    types: {
        context: {} as { count: number },
        events: {} as
            | { type: 'increment' }
            | { type: 'decrement' },
    },
}).createMachine({
    initial: 'idle',
    context: { count: 0 },
    states: {
        idle: {
            on: {
                increment: { target: 'active' },
            },
        },
        active: {
            on: {
                decrement: { target: 'idle' },
            },
        },
    },
});

// Типобезопасное сопоставление состояний
const state = actor.getSnapshot();
const isIdle = state.matches('idle'); // ✅ Автодополнение
const stateValue = state.value; // ✅ 'idle' | 'active'
```
