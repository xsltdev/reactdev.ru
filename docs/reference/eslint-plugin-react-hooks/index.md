---
description: eslint-plugin-react-hooks предоставляет правила ESLint, которые проверяют Правила React
---

# eslint-plugin-react-hooks

<big>

`eslint-plugin-react-hooks` предоставляет правила ESLint, которые проверяют [Правила React](../rules/index.md).

</big>

Этот плагин помогает находить нарушения правил React во время сборки и следить, чтобы компоненты и хуки соблюдали правила React ради корректности и производительности. Линты покрывают и базовые паттерны React (exhaustive-deps и rules-of-hooks), и проблемы, которые отмечает компилятор React. Этот плагин ESLint автоматически показывает диагностики компилятора React, и ими можно пользоваться, даже если приложение ещё не перешло на компилятор.

!!!note "Примечание"

    Если компилятор сообщает диагностику, значит, он статически нашёл паттерн, который не поддерживается или нарушает Правила React. Обнаружив такое, компилятор **автоматически** пропускает эти компоненты и хуки, а остальное приложение по-прежнему компилирует. Так безопасные оптимизации охватывают максимум кода и не ломают приложение.

    Для линта это значит, что не нужно исправлять все нарушения сразу. Разбирайте их в своём темпе, чтобы постепенно увеличивать число оптимизированных компонентов.

## Рекомендуемые правила {#recommended}

Эти правила входят в пресет `recommended` плагина `eslint-plugin-react-hooks`:

* [`exhaustive-deps`](lints/exhaustive-deps.md) — проверяет, что массивы зависимостей хуков React содержат все нужные зависимости
* [`rules-of-hooks`](lints/rules-of-hooks.md) — проверяет, что компоненты и хуки следуют Правилам хуков
* [`component-hook-factories`](lints/component-hook-factories.md) — проверяет функции высшего порядка, которые объявляют вложенные компоненты или хуки
* [`config`](lints/config.md) — проверяет параметры конфигурации компилятора
* [`error-boundaries`](lints/error-boundaries.md) — проверяет, что для ошибок дочерних компонентов используются границы ошибок, а не try/catch
* [`gating`](lints/gating.md) — проверяет конфигурацию режима gating
* [`globals`](lints/globals.md) — проверяет, что во время рендера нет присваивания и изменения глобальных переменных
* [`immutability`](lints/immutability.md) — проверяет, что пропсы, состояние и другие неизменяемые значения не мутируют
* [`incompatible-library`](lints/incompatible-library.md) — проверяет, что не используются библиотеки, несовместимые с мемоизацией
* [`preserve-manual-memoization`](lints/preserve-manual-memoization.md) — проверяет, что компилятор сохраняет существующую ручную мемоизацию
* [`purity`](lints/purity.md) — проверяет чистоту компонентов и хуков по вызовам заведомо нечистых функций
* [`refs`](lints/refs.md) — проверяет корректное использование рефов: их не читают и не записывают во время рендера
* [`set-state-in-effect`](lints/set-state-in-effect.md) — проверяет, что setState не вызывается синхронно в эффекте
* [`set-state-in-render`](lints/set-state-in-render.md) — проверяет, что состояние не устанавливается во время рендера
* [`static-components`](lints/static-components.md) — проверяет, что компоненты статичны и не создаются заново при каждом рендере
* [`unsupported-syntax`](lints/unsupported-syntax.md) — проверяет, что не используется синтаксис, который компилятор React не поддерживает
* [`use-memo`](lints/use-memo.md) — проверяет, что хук `useMemo` используется с возвращаемым значением

<small>:material-information-outline: Источник &mdash; [https://react.dev/reference/eslint-plugin-react-hooks/index](https://react.dev/reference/eslint-plugin-react-hooks/index)</small>
