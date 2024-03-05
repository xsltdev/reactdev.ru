---
id: error_boundaries
title: Error Boundaries
---

# Границы ошибок

## Вариант 1: Использование react-error-boundary

[React-error-boundary](https://github.com/bvaughn/react-error-boundary) - это легкий пакет, готовый к использованию для данного сценария со встроенной поддержкой TS.

Этот подход также позволяет избежать использования компонентов класса, которые уже не так популярны.

## Вариант 2: Написание собственного компонента границы ошибки

Если вы не хотите добавлять новый пакет npm для этого, вы также можете написать свой собственный компонент `ErrorBoundary`.

```ts
import React, {
    Component,
    ErrorInfo,
    ReactNode,
} from 'react';

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
    };

    public static getDerivedStateFromError(
        _: Error
    ): State {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    public componentDidCatch(
        error: Error,
        errorInfo: ErrorInfo
    ) {
        console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return <h1>Sorry.. there was an error</h1>;
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
```

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/error_boundaries></small>
