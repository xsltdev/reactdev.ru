---
description: Эти директивы нужны только в том случае, если вы используете React Server Components или собираете совместимую с ними библиотеку
status: experimental
---

# Директивы

!!!example "Canary"

    Эти директивы нужны только в том случае, если вы [используете React Server Components](../../learn/start-a-new-react-project.md#bleeding-edge-react-frameworks) или собираете совместимую с ними библиотеку.

!!!info ""

    Директивы содержат указания для [бандлеров, совместимых с React Server Components](../../learn/start-a-new-react-project.md#bleeding-edge-react-frameworks).

## Директивы исходного кода {#source-code-directives}

**[`'use client'`](./use-client.md)**

: позволяет отметить, какой код выполняется на клиенте.

**[`'use server'`](./use-server.md)**

: отмечает функции серверной стороны, которые могут быть вызваны из кода клиентской стороны.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/rsc/directives></small>
