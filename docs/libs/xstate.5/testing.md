---
title: Тестирование
description: Как тестировать логику машин состояний и акторов в XState
---

## Тестирование логики

Тестирование логики акторов важно для обеспечения того, чтобы логика была корректной и вела себя ожидаемо. Вы можете тестировать свои машины состояний и акторы, используя различные библиотеки и инструменты тестирования. При написании тестов для машин состояний и акторов следует следовать паттерну **Arrange, Act, Assert** (Подготовка, Действие, Проверка):

-   **Arrange (Подготовка)** — настройте тест, создав логику акторов (например, машину состояний) и акторы из логики акторов.
-   **Act (Действие)** — отправьте событие(я) актору(ам).
-   **Assert (Проверка)** — убедитесь, что актор(ы) достигли ожидаемого состояния(й) и/или выполнили ожидаемые побочные эффекты.

```ts
import { setup, createActor } from 'xstate';
import { test, expect } from 'vitest';

test('some actor', async () => {
    const notifiedMessages: string[] = [];

    // 1. Подготовка
    const machine = setup({
        actions: {
            notify: (_, params) => {
                notifiedMessages.push(params.message);
            },
        },
    }).createMachine({
        initial: 'inactive',
        states: {
            inactive: {
                on: { toggle: { target: 'active' } },
            },
            active: {
                entry: {
                    type: 'notify',
                    params: { message: 'Active!' },
                },
                on: { toggle: { target: 'inactive' } },
            },
        },
    });

    const actor = createActor(machine);

    // 2. Действие
    actor.start();
    actor.send({ type: 'toggle' }); // => должен быть в состоянии 'active'
    actor.send({ type: 'toggle' }); // => должен быть в состоянии 'inactive'
    actor.send({ type: 'toggle' }); // => должен быть в состоянии 'active'

    // 3. Проверка
    expect(actor.getSnapshot().value).toBe('active');
    expect(notifiedMessages).toEqual([
        'Active!',
        'Active!',
    ]);
});
```

## Тестирование акторов

При тестировании акторов вы обычно хотите убедиться, что они переходят в правильное состояние и соответствующим образом обновляют свой контекст при получении событий.

```ts
import { setup, createActor } from 'xstate';
import { test, expect } from 'vitest';

test('actor transitions correctly', () => {
    const toggleMachine = setup({}).createMachine({
        initial: 'inactive',
        context: { count: 0 },
        states: {
            inactive: {
                on: {
                    activate: {
                        target: 'active',
                        actions: assign({
                            count: ({ context }) =>
                                context.count + 1,
                        }),
                    },
                },
            },
            active: {
                on: {
                    deactivate: 'inactive',
                },
            },
        },
    });

    const actor = createActor(toggleMachine);
    actor.start();

    // Тест начального состояния
    expect(actor.getSnapshot().value).toBe('inactive');
    expect(actor.getSnapshot().context.count).toBe(0);

    // Отправка события и тест перехода
    actor.send({ type: 'activate' });

    expect(actor.getSnapshot().value).toBe('active');
    expect(actor.getSnapshot().context.count).toBe(1);

    // Отправка другого события
    actor.send({ type: 'deactivate' });

    expect(actor.getSnapshot().value).toBe('inactive');
    expect(actor.getSnapshot().context.count).toBe(1);
});
```

## Мокирование эффектов

При тестировании машин состояний с побочными эффектами (такими как API-вызовы, логирование или другие внешние взаимодействия) следует мокировать эти эффекты, чтобы сделать тесты детерминированными и изолированными.

```ts
import { setup, createActor } from 'xstate';
import { test, expect, vi } from 'vitest';

test('mocking actions', () => {
    const mockLogger = vi.fn();

    const machine = setup({
        actions: {
            // Мокируем действие логирования
            logMessage: mockLogger,
        },
    }).createMachine({
        initial: 'idle',
        states: {
            idle: {
                on: {
                    start: {
                        target: 'running',
                        actions: {
                            type: 'logMessage',
                            params: { message: 'Started!' },
                        },
                    },
                },
            },
            running: {},
        },
    });

    const actor = createActor(machine);
    actor.start();

    actor.send({ type: 'start' });

    expect(actor.getSnapshot().value).toBe('running');
    expect(mockLogger).toHaveBeenCalledWith(
        expect.anything(), // метаданные действия
        { message: 'Started!' } // параметры
    );
});
```

Для промис-акторов вы можете мокировать промисы:

```ts
test('mocking promise actors', async () => {
    const mockFetch = vi
        .fn()
        .mockResolvedValue({ data: 'test' });

    const machine = setup({
        actors: {
            fetchData: fromPromise(mockFetch),
        },
    }).createMachine({
        initial: 'idle',
        states: {
            idle: {
                on: {
                    fetch: 'loading',
                },
            },
            loading: {
                invoke: {
                    src: 'fetchData',
                    onDone: 'success',
                    onError: 'error',
                },
            },
            success: {},
            error: {},
        },
    });

    const actor = createActor(machine);
    actor.start();

    actor.send({ type: 'fetch' });

    // Ожидание разрешения промиса
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(actor.getSnapshot().value).toBe('success');
    expect(mockFetch).toHaveBeenCalled();
});
```

## Использование `@xstate/test`

!!!warning "Внимание"

    Утилиты модельного тестирования XState Test были перемещены в сам `xstate` и теперь доступны в `xstate/graph`. Отдельный пакет `@xstate/test` устарел в пользу интегрированных утилит тестирования.

Утилиты модельного тестирования позволяют автоматически генерировать тестовые случаи из ваших машин состояний, обеспечивая полное покрытие всех возможных путей и граничных случаев.
