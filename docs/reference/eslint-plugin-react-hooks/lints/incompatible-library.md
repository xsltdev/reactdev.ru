---
description: Проверяет, что не используются библиотеки, несовместимые с мемоизацией (ручной или автоматической)
---

# incompatible-library

<big>

Проверяет, что не используются библиотеки, несовместимые с мемоизацией (ручной или автоматической).

</big>

!!!note "Примечание"

    Эти библиотеки проектировали до того, как правила мемоизации React были полностью описаны. Тогда их авторы правильно выбрали удобный способ держать компоненты ровно настолько реактивными, насколько меняется состояние приложения. Эти устаревшие паттерны работали, но с тех пор выяснилось, что они несовместимы с моделью программирования React. Мы продолжаем работать с авторами библиотек, чтобы перевести эти библиотеки на паттерны, которые следуют Правилам React.

## Подробности правила {#rule-details}

Некоторые библиотеки используют паттерны, которые React не поддерживает. Когда линт встречает вызовы таких API из [известного списка](https://github.com/react/react/blob/main/compiler/packages/babel-plugin-react-compiler/src/HIR/DefaultModuleTypeProvider.ts), он отмечает их этим правилом. Компилятор React может автоматически пропустить компоненты, которые используют эти несовместимые API, чтобы не сломать приложение.

```js
// Example of how memoization breaks with these libraries
function Form() {
  const { watch } = useForm();

  // ❌ This value will never update, even when 'name' field changes
  const name = useMemo(() => watch('name'), [watch]);

  return <div>Name: {name}</div>; // UI appears "frozen"
}
```

Компилятор React автоматически мемоизирует значения по Правилам React. Если что-то ломается при ручном `useMemo`, сломается и автоматическая оптимизация компилятора. Это правило помогает находить такие проблемные паттерны.

??? note "Проектирование API, которые следуют Правилам React"

    Когда проектируете API библиотеки или хук, стоит спросить себя: можно ли безопасно мемоизировать вызов этого API через `useMemo`. Если нельзя, сломается и ручная мемоизация, и мемоизация компилятора React, а вместе с ними и код пользователя.

    Один из таких несовместимых паттернов — «внутренняя изменяемость». Внутренняя изменяемость — это когда объект или функция хранит собственное скрытое состояние, которое меняется со временем, хотя ссылка на объект остаётся той же. Представьте коробку, которая снаружи выглядит одинаково, но внутри тайком перекладывает содержимое. React не видит изменений: он проверяет только, дали ли ему другую коробку, а не то, что внутри. Это ломает мемоизацию, потому что React рассчитывает, что внешний объект (или функция) изменится, если изменилась часть его значения.

    Практическое правило при проектировании API React: подумайте, не сломает ли его `useMemo`:

    ```js
    function Component() {
      const { someFunction } = useLibrary();
      // it should always be safe to memoize functions like this
      const result = useMemo(() => someFunction(), [someFunction]);
    }
    ```

    Вместо этого проектируйте API, которые возвращают неизменяемое состояние и используют явные функции обновления:

    ```js
    // ✅ Good: Return immutable state that changes reference when updated
    function Component() {
      const { field, updateField } = useLibrary();
      // this is always safe to memo
      const greeting = useMemo(() => `Hello, ${field.name}!`, [field.name]);

      return (
        <div>
          <input
            value={field.name}
            onChange={(e) => updateField('name', e.target.value)}
          />
          <p>{greeting}</p>
        </div>
      );
    }
    ```

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ react-hook-form `watch`
function Component() {
  const {watch} = useForm();
  const value = watch('field'); // Interior mutability
  return <div>{value}</div>;
}

// ❌ TanStack Table `useReactTable`
function Component({data}) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
  // table instance uses interior mutability
  return <Table table={table} />;
}
```

!!!warning "MobX"

    Паттерны MobX вроде `observer` тоже ломают допущения мемоизации, но линт их пока не обнаруживает. Если вы опираетесь на MobX и приложение не работает с компилятором React, может понадобиться директива `"use no memo"`.

    ```js
    // ❌ MobX `observer`
    const Component = observer(() => {
      const [timer] = useState(() => new Timer());
      return <span>Seconds passed: {timer.secondsPassed}</span>;
    });
    ```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ For react-hook-form, use `useWatch`:
function Component() {
  const {register, control} = useForm();
  const watchedValue = useWatch({
    control,
    name: 'field'
  });

  return (
    <>
      <input {...register('field')} />
      <div>Current value: {watchedValue}</div>
    </>
  );
}
```

У некоторых других библиотек ещё нет альтернативных API, совместимых с моделью мемоизации React. Если линт не пропускает автоматически ваши компоненты или хуки, которые вызывают такие API, [создайте issue](https://github.com/react/react/issues), чтобы мы добавили их в линт.

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library](https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library)</small>
