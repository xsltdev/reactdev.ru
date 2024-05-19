---
description: Серверные компоненты - это новый тип компонентов, которые рендерятся заранее, до сборки, в среде, отдельной от вашего клиентского приложения или сервера SSR
status: experimental
---

# Компоненты React Server

<big>
**Серверные компоненты** - это новый тип компонентов, которые рендерятся заранее, до сборки, в среде, отдельной от вашего клиентского приложения или сервера SSR.
</big>

Эта отдельная среда является «сервером» в React Server Components. Серверные компоненты могут запускаться один раз во время сборки на вашем CI-сервере, или они могут запускаться для каждого запроса с помощью веб-сервера.

!!!note "Как обеспечить поддержку серверных компонентов?"

    В то время как React Server Components в React 19 стабильны и не ломаются между основными версиями, базовые API, используемые для реализации бандлера или фреймворка React Server Components, не следуют semver и могут ломаться между основными версиями в React 19.x.

    Для поддержки React Server Components в качестве бандлера или фреймворка мы рекомендуем привязываться к определенной версии React или использовать релиз Canary. Мы продолжим работу с бандлерами и фреймворками, чтобы стабилизировать API, используемые для реализации React Server Components в будущем.

## Серверные компоненты без сервера {#server-components-without-a-server}

Серверные компоненты могут запускаться во время сборки для чтения из файловой системы или получения статического содержимого, поэтому веб-сервер не требуется. Например, вам может понадобиться считывать статические данные из системы управления контентом.

Без серверных компонентов статические данные обычно считываются на клиенте с помощью Effect:

```js title="bundle.js"
import marked from 'marked'; // 35.9K (11.2K gzipped)
import sanitizeHtml from 'sanitize-html'; // 206K (63.3K gzipped)

function Page({ page }) {
    const [content, setContent] = useState('');
    // NOTE: loads *after* first page render.
    useEffect(() => {
        fetch(`/api/content/${page}`).then((data) => {
            setContent(data.content);
        });
    }, [page]);

    return <div>{sanitizeHtml(marked(content))}</div>;
}
```

---

```js title="api.js"
app.get(`/api/content/:page`, async (req, res) => {
    const page = req.params.page;
    const content = await file.readFile(`${page}.md`);
    res.send({ content });
});
```

Этот шаблон означает, что пользователям нужно загрузить и разобрать дополнительные 75K (gzipped) библиотек, а также ожидать второго запроса для получения данных после загрузки страницы, только чтобы отобразить статическое содержимое, которое не будет меняться в течение всего времени существования страницы.

С помощью Server Components вы можете отобразить эти компоненты один раз во время сборки:

```js
import marked from 'marked'; // Not included in bundle
import sanitizeHtml from 'sanitize-html'; // Not included in bundle

async function Page({ page }) {
    // NOTE: loads *during* render, when the app is built.
    const content = await file.readFile(`${page}.md`);

    return <div>{sanitizeHtml(marked(content))}</div>;
}
```

Полученный результат можно перевести на сторону сервера (SSR) в HTML и загрузить в CDN. Когда приложение загрузится, клиент не увидит ни оригинального компонента `Page`, ни дорогостоящих библиотек для рендеринга уценки. Клиент увидит только отрендеренный результат:

```js
<div><!-- html for markdown --></div>
```

Это означает, что контент виден при первой загрузке страницы, а в сборку не входят дорогостоящие библиотеки, необходимые для рендеринга статического контента.

!!!note ""

    Вы можете заметить, что приведенный выше серверный компонент является асинхронной функцией:

    ```js
    async function Page({ page }) {
    	//...
    }
    ```

    Async-компоненты - это новая возможность серверных компонентов, которая позволяет вам `await` при рендеринге.

    См. раздел [Асинхронные компоненты с серверными компонентами](#async-components-with-server-components) ниже.

## Серверные компоненты с сервером {#server-components-with-a-server}

Серверные компоненты также могут запускаться на веб-сервере во время запроса страницы, позволяя вам получить доступ к слою данных без необходимости создавать API. Они отображаются до сборки приложения и могут передавать данные и JSX в качестве пропсов клиентским компонентам.

Без серверных компонентов часто приходится получать динамические данные на клиенте в Effect:

```js title="bundle.js"
function Note({ id }) {
    const [note, setNote] = useState('');
    // NOTE: loads *after* first render.
    useEffect(() => {
        fetch(`/api/notes/${id}`).then((data) => {
            setNote(data.note);
        });
    }, [id]);

    return (
        <div>
            <Author id={note.authorId} />
            <p>{note}</p>
        </div>
    );
}

function Author({ id }) {
    const [author, setAuthor] = useState('');
    // NOTE: loads *after* Note renders.
    // Causing an expensive client-server waterfall.
    useEffect(() => {
        fetch(`/api/authors/${id}`).then((data) => {
            setAuthor(data.author);
        });
    }, [id]);

    return <span>By: {author.name}</span>;
}
```

---

```js title="api.js"
import db from './database';

app.get(`/api/notes/:id`, async (req, res) => {
    const note = await db.notes.get(id);
    res.send({ note });
});

app.get(`/api/authors/:id`, async (req, res) => {
    const author = await db.authors.get(id);
    res.send({ author });
});
```

С помощью серверных компонентов вы можете считывать данные и отображать их в компоненте:

```js
import db from './database';

async function Note({ id }) {
    // NOTE: loads *during* render.
    const note = await db.notes.get(id);
    return (
        <div>
            <Author id={note.authorId} />
            <p>{note}</p>
        </div>
    );
}

async function Author({ id }) {
    // NOTE: loads *after* Note,
    // but is fast if data is co-located.
    const author = await db.authors.get(id);
    return <span>By: {author.name}</span>;
}
```

Затем компоновщик объединяет данные, отрисованные компоненты сервера и динамические компоненты клиента в сборку. По желанию, эта сборка может быть отрендерена на стороне сервера (SSR) для создания исходного HTML для страницы. Когда страница загружается, браузер не видит оригинальных компонентов `Note` и `Author`; клиенту передается только отрендеренный вывод:

```js
<div>
    <span>By: The React Team</span>
    <p>React 19 Beta is...</p>
</div>
```

Серверные компоненты можно сделать динамичными, повторно получая их с сервера, где они могут получить доступ к данным и отрисовать их заново. Эта новая архитектура приложений сочетает в себе простую ментальную модель «запрос/ответ» многостраничных приложений, ориентированных на сервер, и бесшовную интерактивность одностраничных приложений, ориентированных на клиента, предоставляя вам лучшее из обоих миров.

## Добавление интерактивности к серверным компонентам {#adding-interactivity-to-server-components}

Серверные компоненты не отправляются в браузер, поэтому они не могут использовать интерактивные API, такие как `useState`. Чтобы добавить интерактивность серверным компонентам, вы можете объединить их с клиентскими компонентами с помощью директивы `"use server"`.

!!!note "Директива для серверных компонентов отсутствует"

    Распространенное заблуждение заключается в том, что серверные компоненты обозначаются `"use server"`, но директивы для серверных компонентов не существует. Директива `"use server"` используется для Server Actions.

    Более подробную информацию можно найти в документации по [Directives](./directives.md).

В следующем примере серверный компонент `Notes` импортирует клиентский компонент `Expandable`, который использует состояние для переключения своего состояния `expanded`:

```js title="Server Component"
import Expandable from './Expandable';

async function Notes() {
    const notes = await db.notes.getAll();
    return (
        <div>
            {notes.map((note) => (
                <Expandable key={note.id}>
                    <p note={note} />
                </Expandable>
            ))}
        </div>
    );
}
```

---

```js title="Client Component"
'use client';

export default function Expandable({ children }) {
    const [expanded, setExpanded] = useState(false);
    return (
        <div>
            <button onClick={() => setExpanded(!expanded)}>
                Toggle
            </button>
            {expanded && children}
        </div>
    );
}
```

Для этого сначала отображается `Notes` как серверный компонент, а затем дается указание бандлеру создать бандл для клиентского компонента `Expandable`. В браузере клиентские компоненты будут видеть вывод серверных компонентов, переданных в качестве пропсов:

```js
<head>
  <!-- the bundle for Client Components -->
  <script src="bundle.js" />
</head>
<body>
  <div>
    <Expandable key={1}>
      <p>this is the first note</p>
    </Expandable>
    <Expandable key={2}>
      <p>this is the second note</p>
    </Expandable>
    <!--...-->
  </div>
</body>
```

## Асинхронные компоненты с серверными компонентами {#async-components-with-server-components}

Серверные компоненты представляют новый способ написания компонентов с использованием async/await. При использовании `await` в async-компоненте React приостанавливает выполнение обещания и ждет, пока оно разрешится, прежде чем возобновить рендеринг. Это работает через границы сервера/клиента с потоковой поддержкой Suspense.

Вы даже можете создать обещание на сервере и ожидать его на клиенте:

```js title="Server Component"
import db from './database';

async function Page({ id }) {
    // Will suspend the Server Component.
    const note = await db.notes.get(id);

    // NOTE: not awaited, will start here and await on the client.
    const commentsPromise = db.comments.get(note.id);
    return (
        <div>
            {note}
            <Suspense fallback={<p>Loading Comments...</p>}>
                <Comments
                    commentsPromise={commentsPromise}
                />
            </Suspense>
        </div>
    );
}
```

---

```js title="Client Component"
'use client';
import { use } from 'react';

function Comments({ commentsPromise }) {
    // NOTE: this will resume the promise from the server.
    // It will suspend until the data is available.
    const comments = use(commentsPromise);
    return comments.map((commment) => <p>{comment}</p>);
}
```

Содержимое `note` - это важные данные для рендеринга страницы, поэтому мы `await` его на сервере. Комментарии находятся под сгибом и имеют более низкий приоритет, поэтому мы запускаем обещание на сервере и ожидаем его на клиенте с помощью API `use`. Это приостановит выполнение обещания на клиенте, не блокируя рендеринг содержимого `note`.

Поскольку асинхронные компоненты не поддерживаются на клиенте, мы ожидаем обещание с помощью `use`.

<small>:material-information-outline: Источник &mdash; <https://react.dev/reference/rsc/server-components></small>
