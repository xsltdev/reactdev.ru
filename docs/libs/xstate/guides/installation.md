# Установка

Вы можете установить XState из NPM или Yarn, или вы можете встроить `<script>` прямо из CDN.

## Пакетные менеджеры

```bash
npm install xstate@latest --save
# or:
yarn add xstate@latest --save
```

## CDN

Вы можете включить XState прямо из [unpkg CDN](https://unpkg.com/xstate@4/dist/):

- XState core: [https://unpkg.com/xstate@4/dist/xstate.js](https://unpkg.com/xstate@4/dist/xstate.js)
- XState web: [https://unpkg.com/xstate@4/dist/xstate.web.js](https://unpkg.com/xstate@4/dist/xstate.web.js)

```html
<script src="https://unpkg.com/xstate@4/dist/xstate.js"></script>
```

Переменная `XState` будет доступна глобально, что даст вам доступ к экспорту верхнего уровня.

```js
// global variable: window.XState
const { createMachine, actions, interpret } = XState;

const lightMachine = createMachine({
  // ...
});

const lightService = interpret(lightMachine);
```
