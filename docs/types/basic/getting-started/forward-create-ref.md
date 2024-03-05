---
description: forwardRef и createRef
---

# `forwardRef` и `createRef`

`createRef`:

```ts
import { createRef, PureComponent } from 'react';

class CssThemeProvider extends PureComponent<Props> {
    private rootRef = createRef<HTMLDivElement>(); // like this
    render() {
        return (
            <div ref={this.rootRef}>
                {this.props.children}
            </div>
        );
    }
}
```

`forwardRef`:

```ts
import { forwardRef, ReactNode } from 'react';

interface Props {
    children?: ReactNode;
    type: 'submit' | 'button';
}
export type Ref = HTMLButtonElement;

export const FancyButton = forwardRef<Ref, Props>(
    (props, ref) => (
        <button
            ref={ref}
            className="MyClassName"
            type={props.type}
        >
            {props.children}
        </button>
    )
);
```

!!!info "Примечание: `ref`, который вы получаете из `forwardRef`, мутабелен, так что вы можете присваивать его при необходимости."

    Это было сделано [специально](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/43265/). Вы можете сделать его неизменяемым, если нужно - назначьте `React.Ref`, если хотите, чтобы никто не переназначил его:

    ```ts
    import { forwardRef, ReactNode, Ref } from 'react';

    interface Props {
    	children?: ReactNode;
    	type: 'submit' | 'button';
    }

    export const FancyButton = forwardRef((
    	props: Props,
    	ref: Ref<HTMLButtonElement> // <-- here!
    ) => (
    	<button
    		ref={ref}
    		className="MyClassName"
    		type={props.type}
    	>
    		{props.children}
    	</button>
    ));
    ```

Если вы захватываете реквизиты компонента, который пересылает рефссылки, используйте [`ComponentPropsWithRef`](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/a05cc538a42243c632f054e42eab483ebf1560ab/types/react/index.d.ts#L770).

## Generic forwardRefs

Подробнее о контексте читайте в <https://fettblog.eu/typescript-react-generic-forward-refs/>:

### Вариант 1 - компонент-обертка

```ts
type ClickableListProps<T> = {
    items: T[];
    onSelect: (item: T) => void;
    mRef?: React.Ref<HTMLUListElement> | null;
};

export function ClickableList<T>(
    props: ClickableListProps<T>
) {
    return (
        <ul ref={props.mRef}>
            {props.items.map((item, i) => (
                <li key={i}>
                    <button
                        onClick={(el) =>
                            props.onSelect(item)
                        }
                    >
                        Select
                    </button>
                    {item}
                </li>
            ))}
        </ul>
    );
}
```

### Вариант 2 - Переопределение forwardRef

```ts
// Redeclare forwardRef
declare module 'react' {
    function forwardRef<T, P = {}>(
        render: (
            props: P,
            ref: React.Ref<T>
        ) => React.ReactElement | null
    ): (
        props: P & React.RefAttributes<T>
    ) => React.ReactElement | null;
}

// Just write your components like you're used to!
import { forwardRef, ForwardedRef } from 'react';

interface ClickableListProps<T> {
    items: T[];
    onSelect: (item: T) => void;
}

function ClickableListInner<T>(
    props: ClickableListProps<T>,
    ref: ForwardedRef<HTMLUListElement>
) {
    return (
        <ul ref={ref}>
            {props.items.map((item, i) => (
                <li key={i}>
                    <button
                        onClick={(el) =>
                            props.onSelect(item)
                        }
                    >
                        Select
                    </button>
                    {item}
                </li>
            ))}
        </ul>
    );
}

export const ClickableList = forwardRef(ClickableListInner);
```

## Дополнительная информация

-   <https://medium.com/@martin_hotell/react-refs-with-typescript-a32d56c4d315>

Возможно, вы также захотите сделать [Условный рендеринг с `forwardRef`](https://github.com/typescript-cheatsheets/react/issues/167).

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/forward_and_create_ref></small>
