# Идентификация узлов состояния

По-умолчанию идентификатором `id` узла состояния является его полный путь с разделителями. Вы можете использовать этот идентификатор `id` по-умолчанию, чтобы указать узел состояния:

```js
const lightMachine = createMachine({
  id: 'light',
  initial: 'green',
  states: {
    green: {
      // default ID: 'light.green'
      on: {
        // You can target state nodes by their default ID.
        // This is the same as TIMER: 'yellow'
        TIMER: { target: '#light.yellow' },
      },
    },
    yellow: {
      on: {
        TIMER: { target: 'red' },
      },
    },
    red: {
      on: {
        TIMER: { target: 'green' },
      },
    },
  },
});
```

## Относительные цели

Узлы дочернего состояния могут быть нацелены относительно их родительских, указав точку ('`.`'), За которой следует их ключ:

```js hl_lines="10-12"
const optionsMachine = createMachine({
  id: 'options',
  initial: 'first',
  states: {
    first: {},
    second: {},
    third: {},
  },
  on: {
    SELECT_FIRST: { target: '.first' }, // resolves to 'options.first'
    SELECT_SECOND: { target: '.second' }, // 'options.second'
    SELECT_THIRD: { target: '.third' }, // 'options.third'
  },
});
```

По умолчанию относительные цели - это [внутренние переходы](transitions.md#internal-transitions), что означает, что родительское состояние _не будет_ выходить и повторно входить. Вы можете сделать относительные цели внешних переходов, указав `internal: false`:

```js hl_lines="4"
// ...
on: {
  SELECT_FIRST: {
    target: { target: '.first' },
    internal: false // external transition, will exit/reenter parent state node
  }
}
```

## Пользовательские идентификаторы

Узлы состояния могут быть обозначены с помощью уникальных идентификаторов, а не с помощью относительных идентификаторов. Это может упростить создание сложных диаграмм состояний.

Чтобы указать идентификатор для узла состояния, укажите уникальный строковый идентификатор в качестве его свойства `id`, например `id: 'greenLight'`.

Чтобы сослаться на узел состояния по его идентификатору, добавьте к его строковому идентификатору символ '`#`', например, `TIMER: '#greenLight'`.

```js
const lightMachine = createMachine({
  id: 'light',
  initial: 'green',
  states: {
    green: {
      // custom identifier
      id: 'greenLight',
      on: {
        // target state node by its ID
        TIMER: { target: '#yellowLight' },
      },
    },
    yellow: {
      id: 'yellowLight',
      on: {
        TIMER: { target: '#redLight' },
      },
    },
    red: {
      id: 'redLight',
      on: {
        // relative targets will still work
        TIMER: { target: 'green' },
      },
    },
  },
});
```

**Примечания:**

- Для корневого узла состояния всегда рекомендуются задавать идентификатор.
- Убедитесь, что все идентификаторы уникальны, чтобы предотвратить конфликты имен. Естественно, уникальность обеспечивается автоматически сгенерированными идентификаторами.

!!!warning "Внимание"

    Не смешивайте пользовательские идентификаторы с относительными идентификаторами. Например, если узел состояния `red` выше имеет пользовательский идентификатор `redLight` и дочерний узел состояния `walking`, например:

    ```js
    // ...
    red: {
    	id: 'redLight',
    	initial: 'walking',
    	states: {
    		// ID still resolves to 'light.red.walking'
    		walking: {/* ... */},
    		// ...
    	}
    }
    // ...
    ```

    Тогда вы не можете настроить таргетинг на состояние `'walking'` с помощью `'#redLight.walking'`, потому что его идентификатор преобразован в `'#light.red.walking'`. Цель, которая начинается с `'#'`, всегда будет относиться к _точному совпадению_ для `'#[state node ID]'`.

## Краткий справочник

**Идентификатор по умолчанию, автоматически сгенерированный:**

```js
const lightMachine = createMachine({
  id: 'light',
  initial: 'green',
  states: {
    // ID: "light.green"
    green: {
      /* ... */
    },
    // ID: "light.yellow"
    yellow: {
      /* ... */
    },
    // ID: "light.red"
    red: {
      /* ... */
    },
  },
});
```

**Пользовательский идентификатор**

```js
// ...
states: {
  active: {
    id: 'custom-active', // can be any unique string
    // ...
  }
}
```

**Таргетинг узла состояния по идентификатору**

```js
// ...
on: {
  EVENT: { target: '#light.yellow' }, // target default ID
  ANOTHER_EVENT: { target: '#custom-id' } // target custom ID
}
```
