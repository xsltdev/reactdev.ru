# Обзор функций

## Маршрутизация на стороне клиента

React Router обеспечивает "маршрутизацию на стороне клиента".

На традиционных веб-сайтах браузер запрашивает документ с веб-сервера, загружает и оценивает CSS и JavaScript-активы, а также отображает HTML, присланный с сервера. Когда пользователь нажимает на ссылку, процесс начинается заново для новой страницы.

Маршрутизация на стороне клиента позволяет приложению обновлять URL-адрес, полученный при переходе по ссылке, без повторного запроса документа с сервера. Вместо этого приложение может сразу отобразить новый пользовательский интерфейс и выполнить запрос данных с помощью `fetch` для обновления страницы новой информацией.

Это позволяет ускорить работу пользователя, поскольку браузеру не нужно запрашивать совершенно новый документ или заново оценивать CSS- и JavaScript-активы для следующей страницы. Кроме того, это обеспечивает более динамичную работу с такими элементами, как анимация.

Маршрутизация на стороне клиента обеспечивается созданием `Router` и ссылками/редиректами на страницы с помощью `Link` и `<Form>`:

```js
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import {
    createBrowserRouter,
    RouterProvider,
    Route,
    Link,
} from 'react-router-dom';

const router = createBrowserRouter([
    {
        path: '/',
        element: (
            <div>
                <h1>Hello World</h1>
                <Link to="about">About Us</Link>
            </div>
        ),
    },
    {
        path: 'about',
        element: <div>About</div>,
    },
]);

createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
);
```

## Вложенные маршруты

Вложенная маршрутизация - это общая идея связывания сегментов URL с иерархией компонентов и данными. Вложенные маршруты React Router были вдохновлены системой маршрутизации в Ember.js примерно в 2014 году. Команда Ember поняла, что почти в каждом случае сегменты URL определяют:

-   макеты, которые будут отображаться на странице
-   зависимости данных от этих макетов.

В React Router эта концепция реализована с помощью API для создания вложенных макетов, связанных с сегментами URL и данными.

```js
// Configure nested routes with JSX
createBrowserRouter(
    createRoutesFromElements(
        <Route path="/" element={<Root />}>
            <Route path="contact" element={<Contact />} />
            <Route
                path="dashboard"
                element={<Dashboard />}
                loader={({ request }) =>
                    fetch('/api/dashboard.json', {
                        signal: request.signal,
                    })
                }
            />
            <Route element={<AuthLayout />}>
                <Route
                    path="login"
                    element={<Login />}
                    loader={redirectIfUser}
                />
                <Route path="logout" action={logoutUser} />
            </Route>
        </Route>
    )
);

// Or use plain objects
createBrowserRouter([
    {
        path: '/',
        element: <Root />,
        children: [
            {
                path: 'contact',
                element: <Contact />,
            },
            {
                path: 'dashboard',
                element: <Dashboard />,
                loader: ({ request }) =>
                    fetch('/api/dashboard.json', {
                        signal: request.signal,
                    }),
            },
            {
                element: <AuthLayout />,
                children: [
                    {
                        path: 'login',
                        element: <Login />,
                        loader: redirectIfUser,
                    },
                    {
                        path: 'logout',
                        action: logoutUser,
                    },
                ],
            },
        ],
    },
]);
```

Эта [визуализация](https://remix.run/_docs/routing) может оказаться полезной.

## Динамические сегменты

Сегменты URL могут быть динамическими заполнителями, которые анализируются и предоставляются различным apis.

```js
<Route path="projects/:projectId/tasks/:taskId" />
```

Два сегмента с `:` являются динамическими и предоставляются следующим API:

```js
// If the current location is /projects/abc/tasks/3
<Route
    // sent to loaders
    loader={({ params }) => {
        params.projectId; // abc
        params.taskId; // 3
    }}
    // and actions
    action={({ params }) => {
        params.projectId; // abc
        params.taskId; // 3
    }}
    element={<Task />}
/>;

function Task() {
    // returned from `useParams`
    const params = useParams();
    params.projectId; // abc
    params.taskId; // 3
}

function Random() {
    const match = useMatch(
        '/projects/:projectId/tasks/:taskId'
    );
    match.params.projectId; // abc
    match.params.taskId; // 3
}
```

См:

-   [`<Route path>`][path]
-   [`<Route loader>`][loader]
-   [`<Route action>`][action]
-   [`useParams`][useparams]
-   [`useMatch`][usematch]

## Ранжированное сопоставление маршрутов

При сопоставлении URL с маршрутами React Router ранжирует маршруты по количеству сегментов, статических сегментов, динамических сегментов, сплетов и т.д. и выбирает _самое конкретное_ соответствие.

Например, рассмотрим эти два маршрута:

```js
<Route path="/teams/:teamId" />
<Route path="/teams/new" />
```

Теперь рассмотрим URL-адрес `http://example.com/teams/new`.

Несмотря на то, что технически оба маршрута соответствуют URL (`new` может быть `:teamId`), интуитивно понятно, что мы хотим выбрать второй маршрут (`/teams/new`). Алгоритм согласования React Router тоже это знает.

При использовании ранжированных маршрутов не нужно заботиться об упорядочивании маршрутов.

## Активные ссылки

Большинство веб-приложений имеют постоянные разделы навигации в верхней части пользовательского интерфейса, в боковой панели, а зачастую и на нескольких уровнях. Стилизация активных элементов навигации, чтобы пользователь знал, где он находится (`isActive`) или куда направляется (`isPending`) в приложении, легко выполняется с помощью `<NavLink>`.

```js
<NavLink
    style={({ isActive, isPending }) => {
        return {
            color: isActive ? 'red' : 'inherit',
        };
    }}
    className={({ isActive, isPending }) => {
        return isActive
            ? 'active'
            : isPending
            ? 'pending'
            : '';
    }}
/>
```

Вы также можете [`useMatch`][usematch] для любого другого "активного" указания вне ссылок.

```js
function SomeComp() {
    const match = useMatch('/messages');
    return (
        <li className={Boolean(match) ? 'active' : ''} />
    );
}
```

См:

-   [`NavLink`][navlink]
-   [`useMatch`][usematch]

## Относительные ссылки

Как и HTML `<a href>`, `<Link to>` и `<NavLink to>` могут принимать относительные пути, при этом улучшается поведение с вложенными маршрутами.

Приведем следующую конфигурацию маршрута:

```js
<Route path="home" element={<Home />}>
    <Route path="project/:projectId" element={<Project />}>
        <Route path=":taskId" element={<Task />} />
    </Route>
</Route>
```

Рассмотрим url `https://example.com/home/project/123`, который отображает следующую иерархию компонентов маршрута:

```js
<Home>
    <Project />
</Home>
```

Если `<Project />` отображает следующие ссылки, то `hrefs` этих ссылок разрешатся следующим образом:

| In `<Project>` @ `/home/project/123` | Resolved `<a href>`     |
| ------------------------------------ | ----------------------- |
| `<Link to="abc">`                    | `/home/project/123/abc` |
| `<Link to=".">`                      | `/home/project/123`     |
| `<Ссылка на="...">`                  | `/home`                 |
| `<Ссылка на="..." relative="path">`  | `/home/project`         |

Обратите внимание, что первый `..` удаляет оба сегмента маршрута `project/:projectId`. По умолчанию `..` в относительных ссылках обходит иерархию маршрутов, а не сегменты URL. Добавление `relative="path"` в следующем примере позволяет обходить сегменты пути.

Относительные ссылки всегда относятся к пути маршрута, по которому они _предоставлены_, а не к полному URL. Это означает, что если пользователь перейдет по ссылке `<Link to="abc">` к ссылке `<Task />` на URL `/home/project/123/abc`, то hrefs в `<Project>` не изменится (в отличие от простого `<a href>`, что является распространенной проблемой маршрутизаторов на стороне клиента).

## Загрузка данных

Поскольку сегменты URL обычно связаны с постоянными данными вашего приложения, React Router предоставляет обычные крючки загрузки данных для инициирования загрузки данных во время навигации. В сочетании с вложенными маршрутами все данные для нескольких макетов по определенному URL-адресу могут загружаться параллельно.

```js
<Route
    path="/"
    loader={async ({ request }) => {
        // loaders can be async functions
        const res = await fetch('/api/user.json', {
            signal: request.signal,
        });
        const user = await res.json();
        return user;
    }}
    element={<Root />}
>
    <Route
        path=":teamId"
        // loaders understand Fetch Responses and will automatically
        // unwrap the res.json(), so you can simply return a fetch
        loader={({ params }) => {
            return fetch(`/api/teams/${params.teamId}`);
        }}
        element={<Team />}
    >
        <Route
            path=":gameId"
            loader={({ params }) => {
                // of course you can use any data store
                return fakeSdk.getTeam(params.gameId);
            }}
            element={<Game />}
        />
    </Route>
</Route>
```

Данные предоставляются вашим компонентам через `useLoaderData`.

```js
function Root() {
    const user = useLoaderData();
    // data from <Route path="/">
}

function Team() {
    const team = useLoaderData();
    // data from <Route path=":teamId">
}

function Game() {
    const game = useLoaderData();
    // data from <Route path=":gameId">
}
```

Когда пользователь посещает или переходит по ссылке на `https://example.com/real-salt-lake/45face3`, все три загрузчика маршрутов будут вызваны и загружены параллельно, до того, как отобразится пользовательский интерфейс для этого URL.

## Перенаправления

При загрузке или изменении данных часто требуется [перенаправить][redirect] пользователя на другой маршрут.

```js
<Route
    path="dashboard"
    loader={async () => {
        const user = await fake.getUser();
        if (!user) {
            // if you know you can't render the route, you can
            // throw a redirect to stop executing code here,
            // sending the user to a new route
            throw redirect('/login');
        }

        // otherwise continue
        const stats = await fake.getDashboardStats();
        return { user, stats };
    }}
/>
```

---

```js
<Route
    path="project/new"
    action={async ({ request }) => {
        const data = await request.formData();
        const newProject = await createProject(data);
        // it's common to redirect after actions complete,
        // sending the user to the new record
        return redirect(`/projects/${newProject.id}`);
    }}
/>
```

См:

-   [`redirect`][redirect]
-   [Throwing in Loaders][loader]
-   [`useNavigate`][usenavigate]

## Отложенный навигационный UI

Когда пользователи перемещаются по приложению, данные для следующей страницы загружаются до ее отображения. Важно обеспечить обратную связь с пользователем в это время, чтобы приложение не казалось неотзывчивым.

```js
function Root() {
    const navigation = useNavigation();
    return (
        <div>
            {navigation.state === 'loading' && (
                <GlobalSpinner />
            )}
            <FakeSidebar />
            <Outlet />
            <FakeFooter />
        </div>
    );
}
```

См:

-   [`useNavigation`][usenavigation]

## Скелетный пользовательский интерфейс с `<Suspense>`

Вместо того чтобы ждать данных для следующей страницы, можно [`отложить`][defer] данные, чтобы пользовательский интерфейс переходил к следующему экрану с пользовательским интерфейсом-заполнителем сразу же, пока данные загружаются.

```js
<Route
    path="issue/:issueId"
    element={<Issue />}
    loader={async ({ params }) => {
        // these are promises, but *not* awaited
        const comments = fake.getIssueComments(
            params.issueId
        );
        const history = fake.getIssueHistory(
            params.issueId
        );
        // the issue, however, *is* awaited
        const issue = await fake.getIssue(params.issueId);

        // defer enables suspense for the un-awaited promises
        return defer({ issue, comments, history });
    }}
/>;

function Issue() {
    const { issue, history, comments } = useLoaderData();
    return (
        <div>
            <IssueDescription issue={issue} />

            {/* Suspense provides the placeholder fallback */}
            <Suspense fallback={<IssueHistorySkeleton />}>
                {/* Await manages the deferred data (promise) */}
                <Await resolve={history}>
                    {/* this calls back when the data is resolved */}
                    {(resolvedHistory) => (
                        <IssueHistory
                            history={resolvedHistory}
                        />
                    )}
                </Await>
            </Suspense>

            <Suspense fallback={<IssueCommentsSkeleton />}>
                <Await resolve={comments}>
                    {/* ... or you can use hooks to access the data */}
                    <IssueComments />
                </Await>
            </Suspense>
        </div>
    );
}

function IssueComments() {
    const comments = useAsyncValue();
    return <div>{/* ... */}</div>;
}
```

См.

-   [Руководство по отложенным данным][deferreddata]
-   [`defer`][defer]
-   [`Await`][await]
-   [`useAsyncValue`][useasyncvalue]

## Мутации данных

HTML-формы, как и ссылки, являются навигационными событиями. React Router поддерживает работу с HTML-формами с помощью маршрутизации на стороне клиента.

При отправке формы предотвращается обычное навигационное событие браузера и создается [`Request`][request] с телом, содержащим [`FormData`][formdata] отправки. Этот запрос отправляется на `<Route action>`, соответствующий `<Form action>` формы.

В действие передается свойство `name` элементов формы:

```js
<Form action="/project/new">
    <label>
        Project title
        <br />
        <input type="text" name="title" />
    </label>

    <label>
        Target Finish Date
        <br />
        <input type="date" name="due" />
    </label>
</Form>
```

Обычный запрос HTML-документа предотвращается и направляется в действие соответствующего маршрута (`<Route path>`, совпадающего с `<form action>`), включая `request.formData`.

```js
<Route
    path="project/new"
    action={async ({ request }) => {
        const formData = await request.formData();
        const newProject = await createProject({
            title: formData.get('title'),
            due: formData.get('due'),
        });
        return redirect(`/projects/${newProject.id}`);
    }}
/>
```

## Ревалидация данных

Согласно десятилетним веб-соглашениям, когда форма отправляется на сервер, данные изменяются, и на экране появляется новая страница. Эта конвенция соблюдается в API мутации данных на основе HTML в React Router.

После вызова действий маршрута загрузчики всех данных на странице вызываются снова, чтобы пользовательский интерфейс автоматически обновлял данные. Никаких истекающих ключей кэша, никаких перезагрузок провайдеров контекста.

См:

-   [Туториал "Создание контактов"][creatingcontacts].

## Индикаторы занятости

Когда формы отправляются на маршрутные действия, вы имеете доступ к состоянию навигации для отображения индикаторов занятости, отключения наборов полей и т. д.

```js
function NewProjectForm() {
    const navigation = useNavigation();
    const busy = navigation.state === 'submitting';
    return (
        <Form action="/project/new">
            <fieldset disabled={busy}>
                <label>
                    Project title
                    <br />
                    <input type="text" name="title" />
                </label>

                <label>
                    Target Finish Date
                    <br />
                    <input type="date" name="due" />
                </label>
            </fieldset>
            <button type="submit" disabled={busy}>
                {busy ? 'Creating...' : 'Create'}
            </button>
        </Form>
    );
}
```

См:

-   [`useNavigation`][usenavigation]

## Оптимистичный пользовательский интерфейс

Знание того, что [`formData`][formdata] отправляется в [action][action], часто бывает достаточно, чтобы пропустить индикаторы занятости и сразу перевести пользовательский интерфейс в следующее состояние, даже если ваша асинхронная работа еще не завершена. Это называется "оптимистичный пользовательский интерфейс".

```js
function LikeButton({ tweet }) {
    const fetcher = useFetcher();

    // if there is `formData` then it is posting to the action
    const liked = fetcher.formData
        ? // check the formData to be optimistic
          fetcher.formData.get('liked') === 'yes'
        : // if its not posting to the action, use the record's value
          tweet.liked;

    return (
        <fetcher.Form method="post" action="toggle-liked">
            <button
                type="submit"
                name="liked"
                value={liked ? 'yes' : 'no'}
            />
        </fetcher.Form>
    );
}
```

(Да, кнопки HTML могут иметь `имя` и `значение`).

Хотя чаще всего оптимизация пользовательского интерфейса осуществляется с помощью [`fetcher`][fetcher], то же самое можно сделать и с обычной формой, используя [`navigation.formData`][navigationformdata].

## Фетчеры данных

HTML-формы являются образцом для мутаций, но у них есть одно существенное ограничение: одновременно можно использовать только одну форму, поскольку отправка формы - это навигация.

В большинстве веб-приложений необходимо, чтобы одновременно происходило несколько мутаций, например, список записей, каждая из которых может быть независимо удалена, отмечена как завершенная, понравилась и т. д.

[Fetchers][fetcher] позволяет взаимодействовать с маршрутом [actions][action] и [loaders][loader], не вызывая навигации в браузере, но при этом получая все традиционные преимущества, такие как обработка ошибок, ревалидация, обработка прерываний и условий гонки.

Представьте себе список задач:

```js
function Tasks() {
    const tasks = useLoaderData();
    return tasks.map((task) => (
        <div>
            <p>{task.name}</p>
            <ToggleCompleteButton task={task} />
        </div>
    ));
}
```

Каждая задача может быть помечена как завершенная независимо от остальных, со своим собственным состоянием ожидания и не вызывая навигации с [fetcher][fetcher]:

```js
function ToggleCompleteButton({ task }) {
    const fetcher = useFetcher();

    return (
        <fetcher.Form
            method="post"
            action="/toggle-complete"
        >
            <fieldset disabled={fetcher.state !== 'idle'}>
                <input
                    type="hidden"
                    name="id"
                    value={task.id}
                />
                <input
                    type="hidden"
                    name="status"
                    value={
                        task.complete
                            ? 'incomplete'
                            : 'complete'
                    }
                />
                <button type="submit">
                    {task.status === 'complete'
                        ? 'Mark Incomplete'
                        : 'Mark Complete'}
                </button>
            </fieldset>
        </fetcher.Form>
    );
}
```

См:

-   [`useFetcher`][fetcher]

## Обработка гоночных условий

React Router отменяет устаревшие операции и автоматически фиксирует только свежие данные.

В любом асинхронном пользовательском интерфейсе существует риск возникновения условий гонки: когда асинхронная операция начинается после, а завершается до выполнения более ранней операции. В результате пользовательский интерфейс отображает неверное состояние.

Рассмотрим поле поиска, которое обновляет список по мере ввода пользователем текста:

```
?q=ry    |---------------|
                         ^ commit wrong state
?q=ryan     |--------|
                     ^ lose correct state
```

Несмотря на то, что запрос для `q?=ryan` вышел позже, он завершился раньше. При неправильной обработке результаты ненадолго станут правильными для `?q=ryan`, но затем перейдут к неправильным результатам для `?q=ry`. Дросселирования и дебаунсинга недостаточно (вы все равно можете прерывать проходящие запросы). Необходима отмена.

Если вы используете соглашения данных React Router, вы полностью и автоматически избегаете этой проблемы.

```
?q=ry    |-----------X
                     ^ cancel wrong state when
                       correct state completes earlier
?q=ryan     |--------|
                     ^ commit correct state
```

React Router справляется с условиями гонки не только при подобной навигации, но и во многих других случаях, например при загрузке результатов автозаполнения или при выполнении нескольких одновременных мутаций с помощью [`fetcher`][fetcher] (и его автоматических, одновременных повторных проверок).

## Обработка ошибок

Подавляющее большинство ошибок вашего приложения обрабатывается React Router автоматически. Он перехватывает все ошибки, возникающие при:

-   рендеринга
-   загрузка данных
-   обновлении данных

На практике это практически все ошибки в вашем приложении, за исключением тех, которые возникают в обработчиках событий (`<button onClick>`) или `useEffect`. В приложениях React Router их, как правило, очень мало.

При возникновении ошибки вместо отображения [`element`][element] маршрута отображается [`errorElement`][errorelement].

```js
<Route
    path="/"
    loader={() => {
        something.that.throws.an.error();
    }}
    // this will not be rendered
    element={<HappyPath />}
    // but this will instead
    errorElement={<ErrorBoundary />}
/>
```

Если маршрут не имеет `errorElement`, то ошибка переходит на ближайший родительский маршрут с `errorElement`:

```js
<Route
    path="/"
    element={<HappyPath />}
    errorElement={<ErrorBoundary />}
>
    {/* Errors here bubble up to the parent route */}
    <Route path="login" element={<Login />} />
</Route>
```

См:

-   [`<Route errorElement>`][errorelement]
-   [`useRouteError`][userouteerror]

## Восстановление прокрутки

React Router эмулирует восстановление прокрутки браузера при навигации, ожидая загрузки данных перед прокруткой. Это гарантирует, что позиция прокрутки будет восстановлена в нужном месте.

Вы также можете настроить поведение, восстанавливая прокрутку не по местоположению (например, по пути к url) и запрещая прокрутку по определенным ссылкам (например, по вкладкам в середине страницы).

См:

-   [`<ScrollRestoration>`][scrollrestoration]

## API веб-стандартов

React Router построен на основе стандартных веб-интерфейсов. [Loaders][loader] и [actions][action] получают стандартные объекты Web Fetch API [`Request`][request] и могут также возвращать объекты [`Response`][response]. Отмена выполняется с помощью [Abort Signals][signal], параметры поиска обрабатываются с помощью [`URLSearchParams`][urlsearchparams], а мутации данных - с помощью [HTML Forms][htmlform].

Когда вы лучше разбираетесь в React Router, вы лучше разбираетесь в веб-платформе.

[path]: https://reactrouter.com/en/main/route/route#path
[loader]: https://reactrouter.com/en/main/route/loader
[action]: https://reactrouter.com/en/main/route/action
[useparams]: https://reactrouter.com/en/main/hooks/use-params
[usematch]: https://reactrouter.com/en/main/hooks/use-match
[navlink]: https://reactrouter.com/en/main/components/nav-link
[redirect]: https://reactrouter.com/en/main/fetch/redirect
[throwing]: https://reactrouter.com/en/main/route/loader#throwing-in-loaders
[usenavigate]: https://reactrouter.com/en/main/hooks/use-navigate
[useparams]: https://reactrouter.com/en/main/hooks/use-params
[usematch]: https://reactrouter.com/en/main/hooks/use-match
[defer]: https://reactrouter.com/en/main/utils/defer
[await]: https://reactrouter.com/en/main/components/await
[useasyncvalue]: https://reactrouter.com/en/main/hooks/use-async-value
[deferreddata]: https://reactrouter.com/en/main/guides/deferred
[usenavigation]: https://reactrouter.com/en/main/hooks/use-navigation
[request]: https://developer.mozilla.org/docs/Web/API/Request
[formdata]: https://developer.mozilla.org/docs/Web/API/FormData
[creatingcontacts]: tutorial.md#creating-contacts
[navigationformdata]: https://reactrouter.com/en/main/hooks/use-navigation#navigationformdata
[fetcher]: https://reactrouter.com/en/main/hooks/use-fetcher
[errorelement]: https://reactrouter.com/en/main/route/error-element
[userouteerror]: https://reactrouter.com/en/main/hooks/use-route-error
[element]: https://reactrouter.com/en/main/route/route#element
[scrollrestoration]: https://reactrouter.com/en/main/components/scroll-restoration
[request]: https://developer.mozilla.org/docs/Web/API/Request
[response]: https://developer.mozilla.org/docs/Web/API/Response
[signal]: https://developer.mozilla.org/docs/Web/API/AbortSignal
[urlsearchparams]: https://developer.mozilla.org/docs/Web/API/URLSearchParams
[htmlform]: https://developer.mozilla.org/docs/Web/HTML/Element/form

## Ссылки

-   [Feature Overview](https://reactrouter.com/en/main/start/overview)
