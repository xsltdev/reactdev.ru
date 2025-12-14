---
title: Начальные состояния
---

Когда машина состояний запускается, она сначала входит в **начальное состояние**. Машина может иметь только одно начальное состояние верхнего уровня; если бы было несколько начальных состояний, машина не знала бы, с чего начать!

В XState начальное состояние определяется свойством `initial` в конфигурации машины:

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

В нашем видеоплеере paused является начальным состоянием, потому что видеоплеер по умолчанию приостановлен и требует взаимодействия пользователя для начала воспроизведения.

<iframe src="https://stately.ai/registry/editor/embed/e13bef2b-bb13-4465-96ac-0bc25340688e?machineId=3ebc8874-2294-480b-a06e-74845337cd8d" width="100%" height="400"></iframe>

## Указание начального состояния

Обычно машина состояний имеет несколько [конечных состояний](finite-states.md), в которых она может находиться. Свойство `initial` в конфигурации машины указывает начальное состояние, в котором машина должна начать работу.

[Родительские состояния](parent-states.md) также должны указывать начальное состояние в своём свойстве `initial`. Следующая `trafficLightMachine` начнёт в состоянии `'green'`, как указано в свойстве `initial` конфигурации машины.

Когда машина достигает родительского состояния `'red'`, она также будет в состоянии `'red.walk'`, как указано в свойстве `initial` состояния `'red'`.

```ts
import { createMachine } from 'xstate';

const trafficLightMachine = createMachine({
    initial: 'green',
    states: {
        green: {
            /* ... */
        },
        yellow: {
            /* ... */
        },
        red: {
            initial: 'walk',
            states: {
                walk: {
                    /* ... */
                },
                wait: {
                    /* ... */
                },
                stop: {
                    /* ... */
                },
            },
        },
    },
});

const trafficLightActor = createActor(trafficLightMachine);

trafficLightActor.subscribe((state) => {
    console.log(state.value);
});

trafficLightActor.start();
// выводит 'green'
```
