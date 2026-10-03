---
description: Проверяет, что setState не вызывается синхронно в эффекте, потому что это приводит к повторным рендерам и ухудшает производительность
---

# set-state-in-effect

<big>

Проверяет, что setState не вызывается синхронно в эффекте: такие вызовы приводят к повторным рендерам и ухудшают производительность.

</big>

## Подробности правила {#rule-details}

Если установить состояние сразу внутри эффекта, React вынужден заново запустить весь цикл рендера. Когда состояние обновляется в эффекте, React должен снова отрендерить компонент, применить изменения к DOM и затем ещё раз запустить эффекты. Получается лишний проход рендера, которого можно было избежать, преобразовав данные прямо во время рендера или вычислив состояние из пропсов. Преобразуйте данные на верхнем уровне компонента. Этот код сам перезапустится, когда изменятся пропсы или состояние, и не запустит дополнительные циклы рендера.

Синхронные вызовы `setState` в эффектах вызывают немедленный повторный рендер ещё до того, как браузер успеет отрисовать кадр. Отсюда проблемы с производительностью и визуальные рывки. React приходится рендерить дважды: один раз, чтобы применить обновление состояния, и ещё раз после эффектов. Такой двойной рендер лишний, если тот же результат можно получить одним рендером.

Во многих случаях эффект вообще не нужен. Подробнее см. [Возможно, вам не нужен эффект](../../../learn/you-might-not-need-an-effect.md).

## Типичные нарушения {#common-violations}

Это правило ловит несколько паттернов, где синхронный setState не нужен:

- Синхронная установка состояния загрузки
- Вычисление состояния из пропсов в эффектах
- Преобразование данных в эффектах вместо рендера

### Неверно {#invalid}

Примеры неверного кода для этого правила:

```js
// ❌ Synchronous setState in effect
function Component({data}) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    setItems(data); // Extra render, use initial state instead
  }, [data]);
}

// ❌ Setting loading state synchronously
function Component() {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true); // Synchronous, causes extra render
    fetchData().then(() => setLoading(false));
  }, []);
}

// ❌ Transforming data in effect
function Component({rawData}) {
  const [processed, setProcessed] = useState([]);

  useEffect(() => {
    setProcessed(rawData.map(transform)); // Should derive in render
  }, [rawData]);
}

// ❌ Deriving state from props
function Component({selectedId, items}) {
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    setSelected(items.find(i => i.id === selectedId));
  }, [selectedId, items]);
}
```

### Верно {#valid}

Примеры верного кода для этого правила:

```js
// ✅ setState in an effect is fine if the value comes from a ref
function Tooltip() {
  const ref = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  useLayoutEffect(() => {
    const { height } = ref.current.getBoundingClientRect();
    setTooltipHeight(height);
  }, []);
}

// ✅ Calculate during render
function Component({selectedId, items}) {
  const selected = items.find(i => i.id === selectedId);
  return <div>{selected?.name}</div>;
}
```

**Если что-то можно вычислить из уже имеющихся пропсов или состояния, не кладите это в состояние.** Вычисляйте это во время рендеринга. Так код становится быстрее, проще и меньше подвержен ошибкам. Подробнее в [Возможно, вам не нужен эффект](../../../learn/you-might-not-need-an-effect.md).

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect)</small>
