---
description: Проверяет синтаксис, который компилятор React не поддерживает. Если такой синтаксис нужен, его всё равно можно использовать вне React, например в отдельной вспомогательной функции
---

# unsupported-syntax

<big>

Проверяет синтаксис, который компилятор React не поддерживает. Если такой синтаксис нужен, его всё равно можно использовать вне React, например в отдельной вспомогательной функции.

</big>

## Подробности правила {#rule-details}

Компилятору React нужно статически анализировать код, чтобы применять оптимизации. Возможности вроде `eval` и `with` не дают на этапе компиляции статически понять, что делает код, поэтому компилятор не может оптимизировать компоненты, которые их используют.

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Using eval in component
function Component({ code }) {
  const result = eval(code); // Can't be analyzed
  return <div>{result}</div>;
}

// ❌ Using with statement
function Component() {
  with (Math) { // Changes scope dynamically
    return <div>{sin(PI / 2)}</div>;
  }
}

// ❌ Dynamic property access with eval
function Component({propName}) {
  const value = eval(`props.${propName}`);
  return <div>{value}</div>;
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ Use normal property access
function Component({propName, props}) {
  const value = props[propName]; // Analyzable
  return <div>{value}</div>;
}

// ✅ Use standard Math methods
function Component() {
  return <div>{Math.sin(Math.PI / 2)}</div>;
}
```

## Устранение неполадок {#troubleshooting}

### Нужно вычислить динамический код {#evaluate-dynamic-code}

Иногда нужно вычислить код, который передал пользователь:

```js hl_lines="3"
// ❌ Wrong: eval in component
function Calculator({expression}) {
  const result = eval(expression); // Unsafe and unoptimizable
  return <div>Result: {result}</div>;
}
```

Используйте безопасный разбор выражений:

```js
// ✅ Better: Use a safe parser
import {evaluate} from 'mathjs'; // or similar library

function Calculator({expression}) {
  const [result, setResult] = useState(null);

  const calculate = () => {
    try {
      // Safe mathematical expression evaluation
      setResult(evaluate(expression));
    } catch (error) {
      setResult('Invalid expression');
    }
  };

  return (
    <div>
      <button onClick={calculate}>Calculate</button>
      {result && <div>Result: {result}</div>}
    </div>
  );
}
```

!!!note "Примечание"

    Никогда не используйте `eval` с пользовательским вводом: это угроза безопасности. Для конкретных задач — математических выражений, разбора JSON или вычисления шаблонов — берите специализированные библиотеки разбора.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax](https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax)</small>
