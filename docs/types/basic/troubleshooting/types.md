---
description: Сталкиваетесь со странными ошибками типов? Вы не одиноки. Это самая сложная часть использования TypeScript в React. Будьте терпеливы - в конце концов, вы изучаете новый язык
---

# Типы

> ⚠️ Читали ли вы [FAQ по TypeScript](https://github.com/microsoft/TypeScript/wiki/FAQ?) Ваш ответ может быть там!

Сталкиваетесь со странными ошибками типов? Вы не одиноки. Это самая сложная часть использования TypeScript в React. Будьте терпеливы - в конце концов, вы изучаете новый язык. Однако чем больше вы будете разбираться в этом, тем меньше времени вы будете работать _против_ компилятора и тем больше он будет работать _за_ вас!

Чтобы ощутить все преимущества TypeScript, старайтесь по возможности избегать типизации с `any`. Вместо этого давайте попробуем ознакомиться с некоторыми распространенными стратегиями решения этих проблем.

## Союзные типы и защита типов

Для решения некоторых проблем с типизацией удобно использовать союзные типы:

```ts
class App extends React.Component<
    {},
    {
        count: number | null; // like this
    }
> {
    state = {
        count: null,
    };
    render() {
        return (
            <div onClick={() => this.increment(1)}>
                {this.state.count}
            </div>
        );
    }
    increment = (amt: number) => {
        this.setState((state) => ({
            count: (state.count || 0) + amt,
        }));
    };
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCtAGxQGc64BBMMOJADxiQDsATRsnQwAdAGFckHrxgAeCnDgBvAL4AaBcs2K0EAK48YALjg89IAEZIocAD6m91agG44AejdxqwANZI4MAAWwHSaKhQAfFrkinQwKNxwALzRijr6hiZmTmHOmkT81gAUAJSpaUQwelA8cLJ8wABucBA8Yt5oPklKpclRQSEiwDxoRCAyRQCMJSoRSgN0InEJSCK6BjAqsm4NjRF5MXDhh8OjSOOGyXBFKCDGDpbWZUlRStoBwYt0SDAAyvHcIrLRIva5vQ5pODrTLXYGraHwWz2AAMZQA1HBbjB3ioSiUDooVAcVEA)

**Охрана типов**: Иногда союзные типы решают проблему в одной области, но создают другую. Если `A` и `B` - оба типа объектов, то `A | B` - это не "либо A, либо B", а "A или B, либо оба сразу", что приводит к некоторой путанице, если вы ожидали, что это будет первое. Научитесь писать проверки, защиты и утверждения (см. также раздел "Условный рендеринг" ниже). Например:

```ts
interface Admin {
    role: string;
}
interface User {
    email: string;
}

// Method 1: use `in` keyword
function redirect(user: Admin | User) {
    if ('role' in user) {
        // use the `in` operator for typeguards since TS 2.7+
        routeToAdminPage(user.role);
    } else {
        routeToHomePage(user.email);
    }
}

// Метод 2: пользовательская защита типа, делает то же самое
// в старых версиях TS или там, где `in` недостаточно
function isAdmin(user: Admin | User): user is Admin {
    return (user as any).role !== undefined;
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoC4AOxiSk3STgEEATEGuAbwrjhwAbJAC44AZxhQaAcwDcFAL5Va9RmmYBVcfR584SECmCCxk6dXlKKFTAFdqGYBGoCIdugBUI7TtQAKKDJIABTiwDLUwJjA9ACUeuT80XBhEVExugC8OQR2OlAIEML4CbxJ-AJIMHZQrvi+NGQVinDWlOT2jjDOrjgeSN4AErhIgcFpkdGxUGX6KZMZM3A5WQSGxoKliZVVNXUEIyBIYEFIzfzK5FcUAPS3cACy1QAWEGxwAIxi+cwABjQ-nAANZIACeAHdoGxbA4nC4qmxgEQMCFflAxI1XAAfODaeI7ODREIAIiESBJRNc6LKcHucF+cBgL3+gLgEDA9BQMGgcEwvJgYM5MjsKCgbHEEhoGjgngAynAAEwAOgA7ABqfT8fpeHwcGjjULo5XkuIKFoGQQ6Qna9y6o5jM5ogrKjYmM36K43cj057M95KsRofI8vCCzlwEVitgAGjgbAgSElzOY4hQxyZL1kVPZgjYunlcAAbvRwi5JbyISyiHAAdQgcBxLQDNR3DIXrDur0ieIsc76Jj9Ti8QU4j8Cj3WEPCUR9q5+1A4ChJShqGC4ibiswAIS5Bz5mLUJAw65AA)

Метод 2 также известен как [User-Defined Type Guards](https://www.typescriptlang.org/docs/handbook/advanced-types.html#user-defined-type-guards) и может быть очень удобен для читабельного кода. Так TS сам уточняет типы с помощью `typeof` и `instanceof`.

Если вам нужны цепочки `if...else` или оператор `switch` вместо них, то это должно "просто работать", но если вам нужна помощь, посмотрите [Discriminated Unions](https://www.typescriptlang.org/docs/handbook/advanced-types.html#discriminated-unions). (См. также: [Basarat's writeup](https://basarat.gitbook.io/typescript/type-system/discriminated-unions)). Это удобно при наборе редукторов для `useReducer` или Redux.

## Необязательные типы

Если компонент имеет необязательное свойство, добавьте вопросительный знак и назначьте его во время деструктуризации (или используйте defaultProps).

```ts
class MyComponent extends React.Component<{
    message?: string; // like this
}> {
    render() {
        const { message = 'default' } = this.props;
        return <div>{message}</div>;
    }
}
```

Вы также можете использовать символ `!` для утверждения, что что-то не является неопределенным, но это не приветствуется.

## Типы перечислений

**Мы рекомендуем избегать использования перечислений по мере возможности**.

У перечислений есть несколько [документированных проблем](https://fettblog.eu/tidy-typescript-avoid-enums/) (команда TS [согласна](https://twitter.com/orta/status/1348966323271987201?s=20)). Более простой альтернативой перечислениям является объявление типа объединения строковых литералов:

```ts
export declare type Position =
    | 'left'
    | 'right'
    | 'top'
    | 'bottom';
```

Если вам необходимо использовать перечисления, помните, что перечисления в TypeScript по умолчанию имеют вид чисел. Обычно их лучше использовать как строки:

```ts
export enum ButtonSizes {
    default = 'default',
    small = 'small',
    large = 'large',
}

// usage
export const PrimaryButton = (
    props: Props & React.HTMLProps<HTMLButtonElement>
) => <Button size={ButtonSizes.default} {...props} />;
```

## Утверждение типа

Иногда вы знаете лучше, чем TypeScript, что используемый вами тип более узкий, чем он думает, или что типы union нужно привести к более конкретному типу для работы с другими API, поэтому утверждайте с ключевым словом `as`. Это говорит компилятору, что вы знаете больше, чем он.

```ts
class MyComponent extends React.Component<{
    message: string;
}> {
    render() {
        const { message } = this.props;
        return (
            <Component2
                message={message as SpecialMessageType}
            >
                {message}
            </Component2>
        );
    }
}
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCmATzCTgGU61gUAbAWSQGduUBzJABVa9ALwFuMKMAB2-fAG4KFOTCRRM6egAUcYbnADeFOHBA8+ggFxwpM+XAA+cAK6yAJkkxykH5eQAvirkaBCyUnAAwriQskiyMABMtsjoMAB0AGJRADx6EAYAfHASABRG5pYCSIEAlKUlZaZwuR7AAG5FLWa5ABYAjEVGFrw1gbkA9IPd5L2T7V0UdSFobCi8cBzUMeDhCfBIAB7qnoZpGBm7cQe5JnNVYzZ20nL8AYEl92ZEnhplDW+ZjgYQi8Eqoys9ECpTgMD6wG4GTA+m4AWBcCIMFcUFkcGaDwxuWu+0SSUeULEI2qgjgG0YzFYnBpwlEn2pT1qUxJ8TJswxdXRcGCQSAA)

Обратите внимание, что вы не можете утверждать свой путь к чему-либо - в основном он предназначен только для уточнения типов. Поэтому это не то же самое, что "приведение" типа.

Вы также можете утверждать, что свойство не является нулевым, при обращении к нему:

```ts
// ! до начала
element.parentNode!.removeChild(element);
// ! после получения доступа к свойствам
myFunction(document.getElementById(dialog.id!)!);
// определенное утверждение о назначении... будьте осторожны!
let userID!: string;
```

Конечно, попробуйте на самом деле обработать нулевой случай вместо того, чтобы утверждать.

## Моделирование номинальных типов

Структурная типизация TS удобна, пока не становится неудобной. Однако вы можете имитировать номинальную типизацию с помощью [`type branding`](https://basarat.gitbook.io/typescript/main-1/nominaltyping):

```ts
type OrderID = string & { readonly brand: unique symbol };
type UserID = string & { readonly brand: unique symbol };
type ID = OrderID | UserID;
```

Мы можем создать эти значения с помощью паттерна Companion Object Pattern:

```ts
function OrderID(id: string) {
    return id as OrderID;
}
function UserID(id: string) {
    return id as UserID;
}
```

Теперь TypeScript не позволит вам использовать неправильный ID в неправильном месте:

```ts
function queryForUser(id: UserID) {
    // ...
}
// Ошибка, Аргумент типа 'OrderID' не может быть присвоен
// параметру типа 'UserID'
queryForUser(OrderID('foobar'));
```

В будущем вы можете использовать ключевое слово `unique` для брендирования. [См. этот PR](https://github.com/microsoft/TypeScript/pull/33038).

## Пересечение типов

Добавление двух типов вместе может быть удобно, например, когда ваш компонент должен отражать реквизиты собственного компонента, такого как `button`:

```ts
export interface PrimaryButtonProps {
    label: string;
}
export const PrimaryButton = (
    props: PrimaryButtonProps &
        React.ButtonHTMLAttributes<HTMLButtonElement>
) => {
    // do custom buttony stuff
    return <button {...props}> {props.label} </button>;
};
```

_Playground [здесь](https://www.typescriptlang.org/play?ssl=4&ssc=1&pln=12&pc=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCipAD0ljmADsYkpN0k4AFKUFKAE8AQgFcYMCE14QwAZzgBvCnDgAbFACMkagFxw5MPkwDmAbgoBfanWjw0Uwzz4gBI8ZKZwAvHAAUKnBgOPL6vPxCYhJSMvJwAGSIxDAAdFGeABIAKgCyADIAghJ8muJIcgA82fnpUgCiakggSCwAfBQAlD6tSoEA9H1wACYQcGiihrhwpdFMggYwopiYgUSLUF4VM55KKXvBsnKWPYoH8ika2mqWcBV921KtFuSWQA)_

Вы также можете использовать типы пересечений для создания многократно используемых подмножеств реквизитов для похожих компонентов:

```ts
type BaseProps = {
   className?: string,
   style?: React.CSSProperties
   name: string // used in both
}
type DogProps = {
  tailsCount: number
}
type HumanProps = {
  handsCount: number
}
export const Human = (props: BaseProps & HumanProps) => // ...
export const Dog = (props: BaseProps & DogProps) => // ...
```

[Посмотреть в TypeScript Playground](https://www.typescriptlang.org/play/?jsx=2#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wFgAoCmATzCTgCEUBnJABRzGbgF44BvCnGFoANi2YA5FCCQB+AFxxmMKMAB2AcwA0Q4Suqj5S5OhgA6AMIBlaxwh1YwJMz1x1MpEpVqtcAPT+cACurAAmcBpwAEYQMAAWFAC+VLT0ACIQmvZcvAJ6MCjAosyWEMHqMErqwSDRSFDJqXRwABK1KOo53HyC5MLxnWGl5ZXVtfWN5CnkSAAekLBwaBDqKm0d6ibEFgBilgA8TKzdcABkGyCd3QB8eQAUAJS8d-d6B2HAAG4BNxSPFAo80W8BWa3gmU02zM5n2RxY7E43AukNuD2ePFe70+P38f3IjyAA)

Не путайте типы пересечения (которые являются операциями **and**) с типами объединения (которые являются операциями **or**).

## Union Types

Этот раздел еще предстоит написать (пожалуйста, внесите свой вклад!). А пока ознакомьтесь с нашим [комментарием о случаях использования типов Union](https://github.com/typescript-cheatsheets/react/blob/main/README.md#union-types-and-type-guarding).

В шпаргалке ADVANCED также есть информация о дискриминируемых союзных типах, которые полезны, когда TypeScript, похоже, не сужает тип союза так, как вы ожидаете.

## Перегрузка типов функций

Когда речь идет о функциях, вам может потребоваться перегрузка вместо типа union. Чаще всего для записи типов функций используется сокращение:

```ts
type FunctionType1 = (x: string, y: number) => number;
```

Но это не позволяет вам делать перегрузку. Если у вас есть реализация, вы можете поместить их друг за другом с помощью ключевого слова function:

```ts
function pickCard(
    x: { suit: string; card: number }[]
): number;
function pickCard(
    x: number
): { suit: string; card: number };
function pickCard(x): any {
    // implementation with combined signature
    // ...
}
```

Однако если у вас нет реализации и вы просто пишете файл определений `.d.ts`, это вам тоже не поможет. В этом случае вы можете отказаться от сокращений и писать их по старинке. Главное, что нужно помнить: для TypeScript `функции - это просто вызываемые объекты без ключа`:

```ts
type pickCard = {
    (x: { suit: string; card: number }[]): number;
    (x: number): { suit: string; card: number };
    // В этой форме нет необходимости в комбинированной подписи
    // Вы также можете вводить сюда статические свойства функций,
    // например `pickCard.wasCalled`.
};
```

Обратите внимание, что когда вы реализуете фактическую перегруженную функцию, реализация должна будет объявить комбинированную сигнатуру вызова, которую вы будете обрабатывать, она не будет выведена за вас. Примеры перегрузки можно легко увидеть в API DOM, например, `createElement`.

[Подробнее о перегрузке читайте в справочнике](https://www.typescriptlang.org/docs/handbook/functions.html#overloads)

## Использование инференционных типов

Опираться на TypeScript's Type Inference - это здорово... пока вы не поймете, что вам нужен тип, который был выведен, и вам придется вернуться и явно объявить типы/интерфейсы, чтобы вы могли экспортировать их для повторного использования.

К счастью, с `typeof` вам не придется этого делать. Просто используйте его для любого значения:

```ts
const [state, setState] = useState({
    foo: 1,
    bar: 2,
}); // state's type inferred to be {foo: number, bar: number}

const someMethod = (obj: typeof state) => {
    // grabbing the type of state even though it was inferred
    // some code using obj
    setState(obj); // this works
};
```

## Использование частичных типов

Работа с нарезкой состояния и реквизитов - обычное дело в React. Опять же, вам не нужно явно переопределять свои типы, если вы используете общий тип `Partial`:

```ts
const [state, setState] = useState({
    foo: 1,
    bar: 2,
}); // state's type inferred to be {foo: number, bar: number}

// NOTE: stale state merging is not actually encouraged in useState
// we are just demonstrating how to use Partial here
const partialStateUpdate = (obj: Partial<typeof state>) =>
    setState({ ...state, ...obj });

// later on...
partialStateUpdate({ foo: 2 }); // this works
```

!!!info "Небольшие предостережения по использованию `Partial`"

    Обратите внимание, что есть некоторые пользователи TS, которые не согласны с использованием `Partial` в его нынешнем виде. Смотрите [тонкие подводные камни приведенного выше примера здесь](https://twitter.com/ferdaber/status/1084798596027957248), а также ознакомьтесь с этим длинным обсуждением [почему @types/react использует Pick вместо Partial](https://github.com/DefinitelyTyped/DefinitelyTyped/issues/18365).

## Нужные мне типы не были экспортированы!

Это может раздражать, но вот способы получить типы!

-   Получение типов Prop компонента: Используйте `React.ComponentProps` и `typeof`, и опционально `Omit` любые перекрывающиеся типы.

```ts
// but doesn't export ButtonProps! oh no!
import { Button } from 'library';

// no problem! grab your own!
type ButtonProps = React.ComponentProps<typeof Button>;

// modify
type AlertButtonProps = Omit<ButtonProps, 'onClick'>;
const AlertButton = (props: AlertButtonProps) => (
    <Button onClick={() => alert('hello')} {...props} />
);
```

Вы также можете использовать [`ComponentPropsWithoutRef`](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/a05cc538a42243c632f054e42eab483ebf1560ab/types/react/index.d.ts#L774) (вместо ComponentProps) и [`ComponentPropsWithRef`](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/a05cc538a42243c632f054e42eab483ebf1560ab/types/react/index.d.ts#L770) (если ваш компонент специально пересылает ссылки).

-   Получение возвращаемого типа функции: используйте `ReturnType`:

```ts
// внутри некоторой библиотеки - возвращаемый тип
// { baz: number } выводится, но не экспортируется
function foo(bar: string) {
    return { baz: 1 };
}

//  inside your app, if you need { baz: number }
type FooReturn = ReturnType<typeof foo>; // { baz: number }
```

На самом деле вы можете захватить практически все, что угодно, публично: [см. этот блогпост от Ивана Кошелева](http://ikoshelev.azurewebsites.net/search/id/11/Pragmatic-uses-of-TypeScript-type-system-My-type-of-type)

```ts
function foo() {
    return {
        a: 1,
        b: 2,
        subInstArr: [
            {
                c: 3,
                d: 4,
            },
        ],
    };
}

type InstType = ReturnType<typeof foo>;
type SubInstArr = InstType['subInstArr'];
type SubInstType = SubInstArr[0];

let baz: SubInstType = {
    c: 5,
    d: 6, // type checks ok!
};

//You could just write a one-liner,
//But please make sure it is forward-readable
//(you can understand it from reading once left-to-right with no jumps)
type SubInstType2 = ReturnType<typeof foo>['subInstArr'][0];
let baz2: SubInstType2 = {
    c: 5,
    d: 6, // type checks ok!
};
```

-   TS также поставляется с типом утилиты `Parameters` для извлечения параметров функции
-   Для чего-нибудь более "индивидуального" ключевое слово `infer` является основным строительным блоком для этого, но требует некоторого привыкания. Посмотрите исходный код для вышеупомянутых типов утилит и [этот пример](https://twitter.com/mgechev/status/1211030455224422401?s=20), чтобы получить представление. Basarat [также есть хорошее видео по `infer`](https://www.youtube.com/watch?v=ijK-1R-LFII&list=PLYvdvJlnTOjF6aJsWWAt7kZRJvzw-en8B&index=3&t=0s).

## Типы, которые мне нужны, не существуют!

Что может быть более раздражающим, чем модули с неэкспортированными типами? Модули, которые **не типизированы**!

> Прежде чем продолжить - убедитесь, что вы проверили, что типы не существуют в [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) или [TypeSearch](https://microsoft.github.io/TypeSearch/).

Не волнуйтесь! Есть более чем пара способов решить эту проблему.

### Применять `any` ко всему.

Более **легкий** способ - создать новый файл объявления типов, скажем, `typedec.d.ts` - если у вас его еще нет. Убедитесь, что путь к файлу может быть разрешен TypeScript, проверив массив `include` в файле `tsconfig.json` в корне вашей директории.

```json
// inside tsconfig.json
{
    // ...
    "include": [
        "src" // automatically resolves if the path to declaration is src/typedec.d.ts
    ]
    // ...
}
```

В этом файле добавьте синтаксис `declare` для нужного вам модуля, скажем, `my-untyped-module`- в файл объявления:

```ts
// inside typedec.d.ts
declare module 'my-untyped-module';
```

Одной этой фразы достаточно, если вам нужно, чтобы все работало без ошибок. Еще более хакерским способом, который можно написать один раз и забыть, было бы использование `"*"` вместо этого, что привело бы к применению типа `Any` для всех существующих и будущих нетипизированных модулей.

Это решение хорошо работает в качестве обходного пути, если у вас меньше пары нетипизированных модулей. Если больше, то у вас в руках окажется тикающая бомба типов. Единственным способом обойти эту проблему будет определение недостающих типов для этих нетипизированных модулей, как описано в следующих разделах.

### Автогенерация типов

Вы можете использовать TypeScript с `--allowJs` и `--declaration`, чтобы увидеть "лучшее предположение" TypeScript о типах библиотеки.

Если это не работает достаточно хорошо, используйте [`dts-gen`](https://github.com/Microsoft/dts-gen), чтобы использовать форму объекта во время выполнения для точного перечисления всех доступных свойств. Это, как правило, очень точно, но инструмент пока не поддерживает поиск комментариев JSDoc для получения дополнительных типов.

```bash
npm install -g dts-gen
dts-gen -m <your-module>
```

Существуют и другие автоматические средства преобразования JS в TS и стратегии миграции - см. [наш чит-лист MIGRATION](https://react-typescript-cheatsheet.netlify.app/docs/migration/from_js).

### Типизация экспортированных хуков

Типизация хуков - это то же самое, что и типизация чистых функций.

Следующие шаги выполняются при двух предположениях:

-   Вы уже создали файл объявления типов, как указано ранее в этом разделе.
-   У вас есть доступ к исходному коду - в частности, к коду, который непосредственно экспортирует функции, которые вы будете использовать. В большинстве случаев он находится в файле `index.js`.
    Обычно для полного определения хука требуется как минимум **два** объявления типа (одно для **Input Prop** и другое для **Return Prop**). Предположим, что хук, который вы хотите набрать, имеет следующую структуру,

```js
// ...
const useUntypedHook = (prop) => {
    // some processing happens here
    return {
        /* ReturnProps */
    };
};
export default useUntypedHook;
```

то ваше объявление типа, скорее всего, должно соответствовать следующему синтаксису.

```ts
declare module 'use-untyped-hook' {
  export interface InputProps { ... }   // type declaration for prop
  export interface ReturnProps { ... } // type declaration for return props
  export default function useUntypedHook(
    prop: InputProps
    // ...
  ): ReturnProps;
}
```

!!!info "Например, хук [useDarkMode](https://github.com/donavon/use-dark-mode) экспортирует функции, которые следуют аналогичной структуре."

    ```js
    // inside src/index.js
    const useDarkMode = (
    	initialValue = false, // -> input props / config props to be exported
    	{
    		// -> input props / config props to be exported
    		element,
    		classNameDark,
    		classNameLight,
    		onChange,
    		storageKey = 'darkMode',
    		storageProvider,
    		global,
    	} = {}
    ) => {
    	// ...
    	return {
    		// -> return props to be exported
    		value: state,
    		enable: useCallback(() => setState(true), [
    			setState,
    		]),
    		disable: useCallback(() => setState(false), [
    			setState,
    		]),
    		toggle: useCallback(
    			() => setState((current) => !current),
    			[setState]
    		),
    	};
    };
    export default useDarkMode;
    ```

    Как следует из комментариев, экспорт этих реквизитов конфигурации и реквизитов возврата в соответствии с вышеупомянутой структурой приведет к экспорту следующего типа.

    ```ts
    declare module 'use-dark-mode' {
    	/**
    	 * Объект конфигурации, позволяющий указать некоторые аспекты `useDarkMode`.
    	 */
    	export interface DarkModeConfig {
    		// A className to set "dark mode". Default = "dark-mode".
    		classNameDark?: string;

    		// A className to set "light mode". Default = "light-mode".
    		classNameLight?: string;

    		// The element to apply the className. Default = `document.body`
    		element?: HTMLElement;

    		// Override the default className handler with a custom callback.
    		onChange?: (val?: boolean) => void;

    		// Specify the `localStorage` key. Default = "darkMode".
    		// Set to `null` to disable persistent storage.
    		storageKey?: string;

    		// A storage provider. Default = `localStorage`.
    		storageProvider?: WindowLocalStorage;

    		// The global object. Default = `window`.
    		global?: Window;
    	}
    	/**
    	 * An object returned from a call to `useDarkMode`.
    	 */
    	export interface DarkMode {
    		readonly value: boolean;
    		enable: () => void;
    		disable: () => void;
    		toggle: () => void;
    	}
    	/**
    	 * A custom React Hook to help you implement a "dark mode"
    	 * component for your application.
    	 */
    	export default function useDarkMode(
    		initialState?: boolean,
    		config?: DarkModeConfig
    	): DarkMode;
    }
    ```

### Типизация экспортируемых компонентов

В случае типизации компонентов нетипизированных классов разницы в подходе практически нет, за исключением того, что после объявления типов вы экспортируете расширенный тип с помощью `class UntypedClassComponent extends React.Component<UntypedClassComponentProps, any> {}`, где `UntypedClassComponentProps` содержит объявление типа.

Например, в [sw-yx's Gist on React Router 6 types](https://gist.github.com/sw-yx/37a6a3d248c2d4031801f0d568904df8) реализован аналогичный метод типизации тогда еще не типизированного RR6.

```ts
declare module 'react-router-dom' {
    import * as React from 'react';
    // ...
    type NavigateProps<T> = {
        to: string | number;
        replace?: boolean;
        state?: T;
    };
    //...
    export class Navigate<T = any> extends React.Component<
        NavigateProps<T>
    > {}
    // ...
}
```

Для получения дополнительной информации о создании определений типов для компонентов классов вы можете обратиться к этому [посту](https://templecoding.com/blog/2016/03/31/creating-typescript-typings-for-existing-react-components) для справки.

## Часто встречающиеся проблемы с TypeScript

Просто список проблем, с которыми часто сталкиваются разработчики React и для которых у TS нет решения. Не обязательно только TSX.

### TypeScript не сужается после проверки нулевого элемента объекта

[![https://pbs.twimg.com/media/E0u6b9uUUAAgwAk?format=jpg&name=medium](https://pbs.twimg.com/media/E0u6b9uUUAAgwAk?format=jpg&name=medium)](https://mobile.twitter.com/tannerlinsley/status/1390409931627499523)

Ссылка: <https://mobile.twitter.com/tannerlinsley/status/1390409931627499523>. см. также <https://github.com/microsoft/TypeScript/issues/9998>

### TypeScript не позволяет ограничить тип дочерних элементов.

Гарантировать безопасность типов для такого рода API невозможно:

```tsx
<Menu>
  <MenuItem/> {/* ok */}
  <MenuLink/> {/* ok */}
  <div> {/* error */}
</Menu>
```

<https://twitter.com/ryanflorence/status/1085745787982700544?s=20>

<small>:material-information-outline: Источник &mdash; <https://react-typescript-cheatsheet.netlify.app/docs/basic/troubleshooting/types></small>
