---
description: Контекст позволяет передавать данные через дерево компонентов без необходимости передавать пропсы на промежуточных уровнях
---

# Контекст

Контекст позволяет передавать данные через дерево компонентов без необходимости передавать пропсы на промежуточных уровнях.

В типичном React-приложении данные передаются сверху вниз (от родителя к дочернему компоненту) с помощью пропсов. Однако, этот способ может быть чересчур громоздким для некоторых типов пропсов (например, выбранный язык, UI-тема), которые необходимо передавать во многие компоненты в приложении. Контекст предоставляет способ делиться такими данными между компонентами без необходимости явно передавать пропсы через каждый уровень дерева.

- [Когда использовать контекст](#when-to-use-context)
- [Перед тем, как вы начнёте использовать контекст](#before-you-use-context)
- [API](#api)
  - [React.createContext](#reactcreatecontext)
  - [Context.Provider](#contextprovider)
  - [Class.contextType](#classcontexttype)
  - [Context.Consumer](#contextconsumer)
- [Примеры](#examples)
  - [Динамический контекст](#dynamic-context)
  - [Изменение контекста из вложенного компонента](#updating-context-from-a-nested-component)
  - [Использование нескольких контекстов](#consuming-multiple-contexts)
- [Предостережения](#caveats)
- [Устаревший API](#legacy-api)

## Когда использовать контекст {#when-to-use-context}

Контекст разработан для передачи данных, которые можно назвать «глобальными» для всего дерева React-компонентов (например, текущий аутентифицированный пользователь, UI-тема или выбранный язык). В примере ниже мы вручную передаём проп `theme`, чтобы стилизовать компонент Button:

```js
class App extends React.Component {
  render() {
    return <Toolbar theme="dark" />;
  }
}

function Toolbar(props) {
  // highlight-range{1-5,8}
  // Компонент Toolbar должен передать проп "theme" ниже,
  // фактически не используя его. Учитывая, что у вас в приложении
  // могут быть десятки компонентов, использующих UI-тему,
  // вам придётся передавать проп "theme" через все компоненты.
  // И в какой-то момент это станет большой проблемой.
  return (
    <div>
      <ThemedButton theme={props.theme} />
    </div>
  );
}

class ThemedButton extends React.Component {
  render() {
    return <Button theme={this.props.theme} />;
  }
}
```

Контекст позволяет избежать передачи пропсов в промежуточные компоненты:

```js
// highlight-range{1-5}
// Контекст позволяет передавать значение глубоко
// в дерево компонентов без явной передачи пропсов
// на каждом уровне. Создадим контекст для текущей
// UI-темы (со значением "light" по умолчанию).
const ThemeContext = React.createContext('light');

class App extends React.Component {
  render() {
    // highlight-range{1-4,6}
    // Компонент Provider используется для передачи текущей
    // UI-темы вниз по дереву. Любой компонент может использовать
    // этот контекст и не важно, как глубоко он находится.
    // В этом примере мы передаём "dark" в качестве значения контекста.
    return (
      <ThemeContext.Provider value="dark">
        <Toolbar />
      </ThemeContext.Provider>
    );
  }
}

// highlight-range{1,2}
// Компонент, который находится в середине,
// больше не должен явно передавать тему вниз.
function Toolbar() {
  return (
    <div>
      <ThemedButton />
    </div>
  );
}

class ThemedButton extends React.Component {
  // highlight-range{1-4,7}
  // Определяем contextType, чтобы получить значение контекста.
  // React найдёт (выше по дереву) ближайший Provider-компонент,
  // предоставляющий этот контекст, и использует его значение.
  // В этом примере значение UI-темы будет "dark".
  static contextType = ThemeContext;
  render() {
    return <Button theme={this.context} />;
  }
}
```

## Перед тем, как вы начнёте использовать контекст {#before-you-use-context}

Обычно контекст используется, если необходимо обеспечить доступ данных во _многих_ компонентах на разных уровнях вложенности. По возможности не используйте его, так как это усложняет повторное использование компонентов.

**Если вы хотите избавиться от передачи некоторых пропсов на множество уровней вниз, обычно [композиция компонентов](composition-vs-inheritance.md) является более простым решением, чем контекст.**

Например, давайте рассмотрим компонент `Page`, который передаёт пропсы `user` и `avatarSize` на несколько уровней вниз, чтобы глубоко вложенные компоненты `Link` и `Avatar` смогли их использовать:

```js
<Page user={user} avatarSize={avatarSize} />
// ... который рендерит ...
<PageLayout user={user} avatarSize={avatarSize} />
// ... который рендерит ...
<NavigationBar user={user} avatarSize={avatarSize} />
// ... который рендерит ...
<Link href={user.permalink}>
  <Avatar user={user} size={avatarSize} />
</Link>
```

Передача пропсов `user` и `avatarSize` вниз выглядит избыточной, если в итоге их использует только компонент `Avatar`. Так же плохо, если компоненту `Avatar` вдруг потребуется больше пропсов сверху, тогда вам придётся добавить их на все промежуточные уровни.

Один из способов решить эту проблему **без контекста** — [передать вниз сам компонент `Avatar`](composition-vs-inheritance.md#containment), в случае чего промежуточным компонентам не нужно знать о пропсах `user` и `avatarSize`:

```js
function Page(props) {
  const user = props.user;
  const userLink = (
    <Link href={user.permalink}>
      <Avatar user={user} size={props.avatarSize} />
    </Link>
  );
  return <PageLayout userLink={userLink} />;
}

// Теперь, это выглядит так:
<Page user={user} avatarSize={avatarSize}/>
// ... который рендерит ...
<PageLayout userLink={...} />
// ... который рендерит ...
<NavigationBar userLink={...} />
// ... который рендерит ...
{props.userLink}
```

С этими изменениями, только корневой компонент `Page` знает о том, что компоненты `Link` и `Avatar` используют `user` и `avatarSize`.

Этот способ может сделать ваш код чище во многих случаях, уменьшая количество пропсов, которые вы должны передавать через ваше приложение, и давая больше контроля корневым компонентам. Однако, это решение не является верным в каждом случае. Перемещая больше сложной логики вверх по дереву, вы перегружаете вышестоящие компоненты.

Вы не ограничены в передаче строго одного компонента. Вы можете передать несколько дочерних компонентов или, даже, создать для них разные «слоты», [как показано здесь](composition-vs-inheritance.md#containment):

```js
function Page(props) {
  const user = props.user;
  const content = <Feed user={user} />;
  const topBar = (
    <NavigationBar>
      <Link href={user.permalink}>
        <Avatar user={user} size={props.avatarSize} />
      </Link>
    </NavigationBar>
  );
  return <PageLayout topBar={topBar} content={content} />;
}
```

Этого паттерна достаточно для большинства случаев, когда вам необходимо отделить дочерний компонент от его промежуточных родителей. Вы можете пойти ещё дальше, используя [рендер-пропсы](render-props.md), если дочерним компонентам необходимо взаимодействовать с родителем перед рендером.

Однако, иногда одни и те же данные должны быть доступны во многих компонентах на разных уровнях дерева и вложенности. Контекст позволяет распространить эти данные и их изменения на все компоненты ниже по дереву. Управление текущим языком, UI темой или кешем данных — это пример тех случаев, когда реализация с помощью контекста будет проще использования альтернативных подходов.

## API {#api}

### React.createContext {#reactcreatecontext}

```js
const MyContext = React.createContext(defaultValue);
```

Создание объекта Context. Когда React рендерит компонент, который подписан на этот объект, React получит текущее значение контекста из ближайшего подходящего `Provider` выше в дереве компонентов.

Аргумент `defaultValue` используется **только** в том случае, если для компонента нет подходящего `Provider` выше в дереве. Это может быть полезно для тестирования компонентов в изоляции без необходимости оборачивать их. Обратите внимание: если передать `undefined` как значение `Provider`, компоненты, использующие этот контекст, не будут использовать `defaultValue`.

### Context.Provider {#contextprovider}

```js
<MyContext.Provider value={/* некоторое значение */}>
```

Каждый объект Контекста используется вместе с `Provider` компонентом, который позволяет дочерним компонентам, использующим этот контекст, подписаться на его изменения.

Принимает проп `value`, который будут передан во все компоненты, использующие этот контекст и являющиеся потомками этого Provider компонента. Один Provider может быть связан с несколькими компонентами, потребляющими контекст. Так же Provider компоненты могут быть вложены друг в друга, переопределяя значение контекста глубже в дереве.

Все потребители, которые являются потомками Provider, будут повторно рендериться, как только проп `value` у Provider изменится. Потребитель перерендерится при изменении контекста, даже если его родитель, не использующий данный контекст, блокирует повторные рендеры с помощью `shouldComponentUpdate`.

Изменения определяются с помощью сравнения нового и старого значения, используя алгоритм, аналогичный [`Object.is`](//developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Object/is#Description).

> Примечание
>
> Способ, по которому определяются изменения, может вызвать проблемы при передаче объекта в `value`: смотрите [Предостережения](#caveats).

### Class.contextType {#classcontexttype}

```js
class MyClass extends React.Component {
  componentDidMount() {
    let value = this.context;
    /* выполнить побочный эффект на этапе монтирования, используя значение MyContext */
  }
  componentDidUpdate() {
    let value = this.context;
    /* ... */
  }
  componentWillUnmount() {
    let value = this.context;
    /* ... */
  }
  render() {
    let value = this.context;
    /* отрендерить что-то, используя значение MyContext */
  }
}
MyClass.contextType = MyContext;
```

В свойство класса `contextType` может быть назначен объект контекста, созданный с помощью [`React.createContext()`](#reactcreatecontext). Это позволяет вам использовать ближайшее и актуальное значение указанного контекста при помощи `this.context`. В этом случае вы получаете доступ к контексту, как во всех методах жизненного цикла, так и в рендер методе.

> Примечание
>
> Вы можете подписаться только на один контекст, используя этот API. В случае, если вам необходимо использовать больше одного, смотрите [Использование нескольких контекстов](#consuming-multiple-contexts).
>
> Если вы используете экспериментальный [синтаксис публичных полей класса](https://babeljs.io/docs/plugins/transform-class-properties/), вы можете использовать **static** поле класса, чтобы инициализировать ваш `contextType`.

```js
class MyClass extends React.Component {
  static contextType = MyContext;
  render() {
    let value = this.context;
    /* отрендерить что-то, используя значение MyContext */
  }
}
```

### Context.Consumer {#contextconsumer}

```js
<MyContext.Consumer>
  {value => /* отрендерить что-то, используя значение контекста */}
</MyContext.Consumer>
```

`Consumer` — это React-компонент, который подписывается на изменения контекста. В свою очередь, это позволяет вам подписаться на контекст в [функциональном компоненте](components-and-props.md#function-and-class-components).

`Consumer` принимает [функцию в качестве дочернего компонента](render-props.md#using-props-other-than-render). Эта функция принимает текущее значение контекста и возвращает React-компонент. Передаваемый аргумент `value` будет равен ближайшему (вверх по дереву) значению этого контекста, а именно пропу `value` Provider компонента. Если такого Provider компонента не существует, аргумент `value` будет равен значению `defaultValue`, которое было передано в `createContext()`.

> Примечание
>
> Подробнее про паттерн «_функция как дочерний компонент_» можно узнать на странице [Рендер-пропсы](render-props.md).

## Примеры {#examples}

### Динамический контекст {#dynamic-context}

Более сложный пример динамических значений для UI темы:

**theme-context.js**

```js
export const themes = {
  light: {
    foreground: '#000000',
    background: '#eeeeee',
  },
  dark: {
    foreground: '#ffffff',
    background: '#222222',
  },
};

// highlight-range{1-3}
export const ThemeContext = React.createContext(
  themes.dark // значение по умолчанию
);
```

**themed-button.js**

```js
import { ThemeContext } from './theme-context';

class ThemedButton extends React.Component {
  // highlight-range{3,12}
  render() {
    let props = this.props;
    let theme = this.context;
    return (
      <button
        {...props}
        style={{ backgroundColor: theme.background }}
      />
    );
  }
}
ThemedButton.contextType = ThemeContext;

export default ThemedButton;
```

**app.js**

```js
import { ThemeContext, themes } from './theme-context';
import ThemedButton from './themed-button';

// Промежуточный компонент, который использует ThemedButton
function Toolbar(props) {
  return (
    <ThemedButton onClick={props.changeTheme}>
      Change Theme
    </ThemedButton>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      theme: themes.light,
    };

    this.toggleTheme = () => {
      this.setState((state) => ({
        theme:
          state.theme === themes.dark
            ? themes.light
            : themes.dark,
      }));
    };
  }

  render() {
    //highlight-range{1-4}
    // ThemedButton внутри ThemeProvider использует
    // значение светлой UI-темы из состояния, в то время как
    // ThemedButton, который находится вне ThemeProvider,
    // использует тёмную UI-тему из значения по умолчанию
    //highlight-range{3-5,7}
    return (
      <Page>
        <ThemeContext.Provider value={this.state.theme}>
          <Toolbar changeTheme={this.toggleTheme} />
        </ThemeContext.Provider>
        <Section>
          <ThemedButton />
        </Section>
      </Page>
    );
  }
}

ReactDOM.render(<App />, document.root);
```

### Изменение контекста из вложенного компонента {#updating-context-from-a-nested-component}

Довольно часто необходимо изменить контекст из компонента, который находится где-то глубоко в дереве компонентов. В этом случае вы можете добавить в контекст функцию, которая позволит потребителям изменить значение этого контекста:

**theme-context.js**

```js
// Убедитесь, что форма значения по умолчанию,
// передаваемого в createContext, совпадает с формой объекта,
// которую ожидают потребители контекста.
// highlight-range{2-3}
export const ThemeContext = React.createContext({
  theme: themes.dark,
  toggleTheme: () => {},
});
```

**theme-toggler-button.js**

```js
import { ThemeContext } from './theme-context';

function ThemeTogglerButton() {
  // highlight-range{1-2,5}
  // ThemeTogglerButton получает из контекста
  // не только значение UI-темы, но и функцию toggleTheme.
  return (
    <ThemeContext.Consumer>
      {({ theme, toggleTheme }) => (
        <button
          onClick={toggleTheme}
          style={{ backgroundColor: theme.background }}
        >
          Toggle Theme
        </button>
      )}
    </ThemeContext.Consumer>
  );
}

export default ThemeTogglerButton;
```

**app.js**

```js
import { ThemeContext, themes } from './theme-context';
import ThemeTogglerButton from './theme-toggler-button';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.toggleTheme = () => {
      this.setState((state) => ({
        theme:
          state.theme === themes.dark
            ? themes.light
            : themes.dark,
      }));
    };

    // highlight-range{1-2,5}
    // Состояние хранит функцию для обновления контекста,
    // которая будет также передана в Provider-компонент.
    this.state = {
      theme: themes.light,
      toggleTheme: this.toggleTheme,
    };
  }

  render() {
    // highlight-range{1,3}
    // Всё состояние передаётся в качестве значения контекста
    return (
      <ThemeContext.Provider value={this.state}>
        <Content />
      </ThemeContext.Provider>
    );
  }
}

function Content() {
  return (
    <div>
      <ThemeTogglerButton />
    </div>
  );
}

ReactDOM.render(<App />, document.root);
```

### Использование нескольких контекстов {#consuming-multiple-contexts}

Чтобы последующие рендеры (связанные с контекстом) были быстрыми, React делает каждого потребителя контекста отдельным компонентом в дереве.

```js
// Контекст UI-темы, со светлым значением по умолчанию
const ThemeContext = React.createContext('light');

// Контекст активного пользователя
const UserContext = React.createContext({
  name: 'Guest',
});

class App extends React.Component {
  render() {
    const { signedInUser, theme } = this.props;

    // Компонент App, который предоставляет начальные значения контекстов
    // highlight-range{2-3,5-6}
    return (
      <ThemeContext.Provider value={theme}>
        <UserContext.Provider value={signedInUser}>
          <Layout />
        </UserContext.Provider>
      </ThemeContext.Provider>
    );
  }
}

function Layout() {
  return (
    <div>
      <Sidebar />
      <Content />
    </div>
  );
}

// Компонент, который может использовать несколько контекстов
function Content() {
  // highlight-range{2-10}
  return (
    <ThemeContext.Consumer>
      {(theme) => (
        <UserContext.Consumer>
          {(user) => (
            <ProfilePage user={user} theme={theme} />
          )}
        </UserContext.Consumer>
      )}
    </ThemeContext.Consumer>
  );
}
```

Если два или более значений контекста часто используются вместе, возможно, вам стоит рассмотреть создание отдельного компонента, который будет передавать оба значения дочерним компонентам с помощью паттерна «рендер-пропс».

## Предостережения {#caveats}

Контекст использует сравнение по ссылкам, чтобы определить, когда запускать последующий рендер. Из-за этого существуют некоторые подводные камни, например, случайные повторные рендеры потребителей, при перерендере родителя Provider-компонента. В следующем примере будет происходить повторный рендер потребителя каждый повторный рендер Provider-компонента, потому что новый объект, передаваемый в `value`, будет создаваться каждый раз:

```js
class App extends React.Component {
  render() {
    // highlight-range{2}
    return (
      <MyContext.Provider
        value={{ something: 'something' }}
      >
        <Toolbar />
      </MyContext.Provider>
    );
  }
}
```

Один из вариантов решения этой проблемы — хранение этого объекта в состоянии родительского компонента:

```js
class App extends React.Component {
  constructor(props) {
    super(props);
    // highlight-range{2}
    this.state = {
      value: { something: 'something' },
    };
  }

  render() {
    // highlight-range{2}
    return (
      <Provider value={this.state.value}>
        <Toolbar />
      </Provider>
    );
  }
}
```

## Устаревший API {#legacy-api}

> Примечание
>
> В прошлом React имел только экспериментальный API контекста. Старый API будет поддерживаться во всех 16.x релизах, но использующие его приложения должны перейти на новую версию. Устаревший API будет удалён в будущем крупном релизе React.
