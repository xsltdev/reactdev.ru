---
title: 'Выходные данные'
---

Output (выходные данные) — это финальные данные, которые производит [актор](actors.md). Когда актор отвечает за выполнение какой-либо задачи, такой как сетевой запрос или сложные вычисления, он возвращает output после завершения этой задачи. Output представляет результат работы актора. Акторы производят output только когда их статус равен «done»; т.е. когда они находятся в своём [финальном состоянии](final-states.md).

Некоторые акторы могут работать бесконечно и не производить никакого output.

## Output в акторах автоматов

Прочитайте [финальные состояния](final-states.md) для получения дополнительной информации о том, как указать output в акторах автоматов.

## Output в promise-акторах

Когда promise-актор разрешается, он может производить выходные данные. Вы можете указать эти выходные данные в свойстве `.output` автомата:

```ts
import { fromPromise, createActor } from 'xstate';

const promiseLogic = fromPromise(async () => {
    const response = await fetch('https://example.com');

    return response.json() as { message: string };
});

const actor = createActor(promiseLogic);

actor.subscribe((snapshot) => {
    if (snapshot.status === 'done') {
        console.log(snapshot.output.message);
    }
});

actor.start();
```

## Output и TypeScript

!!!typescript "TypeScript"

    **XState v5 требует TypeScript версии 5.0 или выше.**

    Для лучших результатов используйте последнюю версию TypeScript. [Подробнее о XState и TypeScript](typescript.md)

Свойство `output` может быть типизировано в свойстве `.types` настройки автомата:

```ts
import { setup, createActor } from 'xstate';

const machine = setup({
    // highlight-start
    types: {
        output: {} as { total: number },
    },
    // highlight-end
}).createMachine({
    // ...
    output: ({ context }) => ({
        total: context.items.reduce(
            (total, item) => total + item.price,
            0
        ),
    }),
});

const actor = createActor(machine);

actor.subscribe((snapshot) => {
    if (snapshot.status === 'done') {
        console.log(snapshot.output.total);
    }
});
```

Вы можете прочитать тип output из любого актора, используя `OutputFrom<typeof actor>`:

```ts
import type { OutputFrom } from 'xstate';
import { machine } from './machine';

const actor = createActor(machine);

function acceptOutput<T>(output: OutputFrom<typeof actor>) {
    console.log(output.total);
}
```
