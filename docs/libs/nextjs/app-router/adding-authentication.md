---
description: В предыдущей главе вы завершили создание маршрутов счетов-фактур, добавив проверку формы и улучшив доступность. В этой главе вы добавите аутентификацию в дашборд.
---

# Аутентификация

<big>В предыдущей главе вы завершили создание маршрутов счетов-фактур, добавив проверку формы и улучшив доступность. В этой главе вы добавите аутентификацию в дашборд.</big>

!!!tip "Вот темы, которые мы рассмотрим"

    - Что такое аутентификация.
    - Как добавить аутентификацию в приложение с помощью NextAuth.js.
    - Как использовать Middleware для перенаправления пользователей и защиты маршрутов.
    - Как использовать `UseActionState` в React для обработки отложенных состояний и ошибок формы.

## Что такое аутентификация?

Аутентификация - ключевая часть многих современных веб-приложений. С ее помощью система проверяет, является ли пользователь тем, за кого себя выдает.

Безопасный веб-сайт часто использует несколько способов проверки личности пользователя. Например, после ввода имени пользователя и пароля сайт может отправить проверочный код на ваше устройство или использовать внешнее приложение, например Google Authenticator. Такая двухфакторная аутентификация (2FA) помогает повысить уровень безопасности. Даже если кто-то узнает ваш пароль, он не сможет получить доступ к вашей учетной записи без вашего уникального маркера.

### Аутентификация и авторизация

В веб-разработке аутентификация и авторизация выполняют разные функции:

-   **Аутентификация** - это проверка того, что пользователь является тем, за кого себя выдает. Вы подтверждаете свою личность с помощью чего-то, что у вас есть, например, имени пользователя и пароля.
-   **Авторизация** - это следующий шаг. После того как личность пользователя подтверждена, авторизация определяет, какие части приложения ему разрешено использовать.

Итак, аутентификация проверяет, кто вы, а авторизация определяет, что вы можете делать или к чему можете получить доступ в приложении.

<?quiz?>

question: Что из перечисленного ниже лучше всего описывает разницу между аутентификацией и авторизацией?
answer: Аутентификация определяет, к чему вы можете получить доступ. Авторизация подтверждает вашу личность.
answer: Аутентификация и авторизация определяют, к каким частям приложения пользователь может получить доступ.
answer-correct: Аутентификация подтверждает вашу личность. Авторизация определяет, к чему вы можете получить доступ.
answer: Разницы нет; оба термина означают одно и то же.
content:

<p>Именно так! Хотя эти понятия похожи, аутентификация подтверждает вашу личность, а авторизация определяет, к чему вы можете получить доступ.</p>
<?/quiz?>

## Создание маршрута входа в систему

Начните с создания нового маршрута в вашем приложении под названием `/login` и вставьте следующий код:

```ts title="/app/login/page.tsx"
import AcmeLogo from '@/app/ui/acme-logo';
import LoginForm from '@/app/ui/login-form';
import { Suspense } from 'react';

export default function LoginPage() {
    return (
        <main className="flex items-center justify-center md:h-screen">
            <div className="relative mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4 md:-mt-32">
                <div className="flex h-20 w-full items-end rounded-lg bg-blue-500 p-3 md:h-36">
                    <div className="w-32 text-white md:w-36">
                        <AcmeLogo />
                    </div>
                </div>
                <Suspense>
                    <LoginForm />
                </Suspense>
            </div>
        </main>
    );
}
```

Вы заметите, что страница импортирует `<LoginForm />`, который вы обновите позже в этой главе. Этот компонент обернут в React `<Suspense>`, потому что он будет получать доступ к информации из входящего запроса (параметры поиска URL).

## NextAuth.js

Мы будем использовать [NextAuth.js](https://nextjs.authjs.dev/) для добавления аутентификации в ваше приложение. NextAuth.js абстрагирует большую часть сложностей, связанных с управлением сессиями, входом и выходом из системы, а также другими аспектами аутентификации. Хотя вы можете реализовать эти функции вручную, этот процесс может занять много времени и привести к ошибкам. NextAuth.js упрощает этот процесс, предоставляя унифицированное решение для аутентификации в приложениях Next.js.

## Установка NextAuth.js

Установите NextAuth.js, выполнив следующую команду в терминале:

```sh title="Terminal"
pnpm i next-auth@beta
```

Здесь вы устанавливаете `beta` версию NextAuth.js, которая совместима с Next.js 14+.

Далее сгенерируйте секретный ключ для вашего приложения. Этот ключ используется для шифрования файлов cookie, обеспечивая безопасность пользовательских сессий. Для этого выполните следующую команду в терминале:

```sh title="Terminal"
# macOS
openssl rand -base64 32
# Windows can use https://generate-secret.vercel.app/32
```

Затем в файле `.env` добавьте сгенерированный ключ в переменную `AUTH_SECRET`:

```sh title=".env" hl_lines="1"
AUTH_SECRET=your-secret-key
```

Чтобы auth работал в продакшне, вам нужно будет обновить переменные окружения и в проекте Vercel. Посмотрите это [руководство](https://vercel.com/docs/environment-variables) о том, как добавить переменные окружения в Vercel.

### Добавление опции `pages`

Создайте файл `auth.config.ts` в корне нашего проекта, который экспортирует объект `authConfig`. Этот объект будет содержать параметры конфигурации для NextAuth.js. Пока что он будет содержать только опцию `pages`:

```ts title="/auth.config.ts"
import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
  pages: {
    signIn: '/login',
  },
} satisfies NextAuthConfig;
```

Вы можете использовать опцию `pages`, чтобы указать маршрут для пользовательских страниц входа, выхода и ошибок. Это не обязательно, но если добавить `signIn: '/login'` в опцию `pages`, пользователь будет перенаправлен на нашу пользовательскую страницу входа, а не на страницу NextAuth.js по умолчанию.

## Защита маршрутов с помощью Next.js Middleware

Далее добавьте логику для защиты маршрутов. Это не позволит пользователям получить доступ к страницам дашборда, если они не вошли в систему.

```ts title="/auth.config.ts" hl_lines="7-19"
import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
	pages: {
		signIn: '/login',
	},
	callbacks: {
		authorized({ auth, request: { nextUrl } }) {
		const isLoggedIn = !!auth?.user;
		const isOnDashboard = nextUrl.pathname.startsWith('/dashboard');
		if (isOnDashboard) {
			if (isLoggedIn) return true;
			return false; // Redirect unauthenticated users to login page
		} else if (isLoggedIn) {
			return Response.redirect(new URL('/dashboard', nextUrl));
		}
			return true;
		},
	},
	providers: [], // Add providers with an empty array for now
} satisfies NextAuthConfig;
```

Коллбэк `authorized` используется для проверки того, авторизован ли запрос для доступа к странице с помощью [Next.js Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware). Он вызывается перед завершением запроса и получает объект со свойствами `auth` и `request`. Свойство `auth` содержит сессию пользователя, а свойство `request` - входящий запрос.

Параметр `providers` представляет собой массив, в котором перечисляются различные варианты входа в систему. На данный момент это пустой массив, чтобы удовлетворить конфигурацию NextAuth. Подробнее об этом вы узнаете в разделе [Добавление провайдера учетных данных](https://nextjs.org/learn/dashboard-app/adding-authentication#adding-the-credentials-provider).

Далее вам нужно будет импортировать объект `authConfig` в файл Middleware. В корне вашего проекта создайте файл `middleware.ts` и вставьте в него следующий код:

```ts title="/middleware.ts"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';

export default NextAuth(authConfig).auth;

export const config = {
    // https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher
    matcher: [
        '/((?!api|_next/static|_next/image|.*\\.png$).*)',
    ],
};
```

Здесь вы инициализируете NextAuth.js объектом `authConfig` и экспортируете свойство `auth`. Вы также используете опцию `matcher` из Middleware, чтобы указать, что он должен запускаться по определенным путям.

Преимущество использования Middleware для этой задачи заключается в том, что защищенные маршруты не начнут отрисовываться, пока Middleware не проверит аутентификацию, что повышает как безопасность, так и производительность вашего приложения.

### Хеширование паролей

Хорошей практикой является **хеширование** паролей перед их хранением в базе данных. Хеширование преобразует пароль в строку символов фиксированной длины, которая выглядит случайной, обеспечивая уровень безопасности, даже если данные пользователя открыты.

При загрузке базы данных вы использовали пакет `bcrypt` для хэширования пароля пользователя перед его сохранением в базе данных. Позже в этой главе вы снова будете использовать его для проверки соответствия пароля, введенного пользователем, паролю в базе данных. Однако для пакета `bcrypt` вам придется создать отдельный файл. Это связано с тем, что `bcrypt` опирается на API Node.js, недоступные в Next.js Middleware.

Создайте новый файл `auth.ts`, который будет содержать объект `authConfig`:

```ts title="/auth.ts"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
});
```

### Добавление провайдера учетных данных

Далее вам нужно будет добавить опцию `providers` для NextAuth.js. `providers` - это массив, в котором вы перечисляете различные варианты входа в систему, такие как Google или GitHub. В этом курсе мы сосредоточимся на использовании только [Credentials provider](https://authjs.dev/getting-started/providers/credentials-tutorial).

Провайдер Credentials позволяет пользователям входить в систему с помощью имени пользователя и пароля.

```ts title="/auth.ts" hl_lines="3 7"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
import Credentials from 'next-auth/providers/credentials';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [Credentials({})],
});
```

!!!info "Полезно знать"

    Существуют и другие альтернативные провайдеры, такие как [OAuth](https://authjs.dev/getting-started/providers/oauth-tutorial) или [email](https://authjs.dev/getting-started/providers/email-tutorial). Полный список возможностей см. в [документации NextAuth.js](https://authjs.dev/getting-started/providers).

### Добавление функциональности авторизации

Вы можете использовать функцию `authorize` для обработки логики аутентификации. Аналогично Server Actions, вы можете использовать `zod` для проверки электронной почты и пароля перед тем, как проверить, существует ли пользователь в базе данных:

```ts title="/auth.ts" hl_lines="4 9-18"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
import Credentials from 'next-auth/providers/credentials';
import { z } from 'zod';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                const parsedCredentials = z
                    .object({
                        email: z.string().email(),
                        password: z.string().min(6),
                    })
                    .safeParse(credentials);
            },
        }),
    ],
});
```

После проверки учетных данных создайте новую функцию `getUser`, которая будет запрашивать пользователя из базы данных.

```ts title="/auth.ts" hl_lines="9-11 13-25 38-45"
import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import { authConfig } from './auth.config';
import { z } from 'zod';
import type { User } from '@/app/lib/definitions';
import bcrypt from 'bcrypt';
import postgres from 'postgres';

const sql = postgres(process.env.POSTGRES_URL!, {
    ssl: 'require',
});

async function getUser(
    email: string
): Promise<User | undefined> {
    try {
        const user = await sql<
            User[]
        >`SELECT * FROM users WHERE email=${email}`;
        return user[0];
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw new Error('Failed to fetch user.');
    }
}

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                const parsedCredentials = z
                    .object({
                        email: z.string().email(),
                        password: z.string().min(6),
                    })
                    .safeParse(credentials);

                if (parsedCredentials.success) {
                    const {
                        email,
                        password,
                    } = parsedCredentials.data;
                    const user = await getUser(email);
                    if (!user) return null;
                }

                return null;
            },
        }),
    ],
});
```

Затем вызовите `bcrypt.compare`, чтобы проверить, совпадают ли пароли:

```ts title="/auth.ts" title="9-11 28 34"
import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import { authConfig } from './auth.config';
import { z } from 'zod';
import type { User } from '@/app/lib/definitions';
import bcrypt from 'bcrypt';
import postgres from 'postgres';

const sql = postgres(process.env.POSTGRES_URL!, {
    ssl: 'require',
});

// ...

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                // ...

                if (parsedCredentials.success) {
                    const {
                        email,
                        password,
                    } = parsedCredentials.data;
                    const user = await getUser(email);
                    if (!user) return null;
                    const passwordsMatch = await bcrypt.compare(
                        password,
                        user.password
                    );

                    if (passwordsMatch) return user;
                }

                console.log('Invalid credentials');
                return null;
            },
        }),
    ],
});
```

Наконец, если пароли совпадают, вы хотите вернуть пользователя, в противном случае верните `null`, чтобы пользователь не смог войти в систему.

### Обновление формы входа

Теперь вам нужно связать логику авторизации с формой входа. В файле `actions.ts` создайте новое действие под названием `authenticate`. Это действие должно импортировать функцию `signIn` из файла `auth.ts`:

```ts title="/app/lib/actions.ts"
'use server';

import { signIn } from '@/auth';
import { AuthError } from 'next-auth';

// ...

export async function authenticate(
    prevState: string | undefined,
    formData: FormData
) {
    try {
        await signIn('credentials', formData);
    } catch (error) {
        if (error instanceof AuthError) {
            switch (error.type) {
                case 'CredentialsSignin':
                    return 'Invalid credentials.';
                default:
                    return 'Something went wrong.';
            }
        }
        throw error;
    }
}
```

Если возникла ошибка `'CredentialsSignin'`, вы хотите вывести соответствующее сообщение об ошибке. Вы можете узнать об ошибках NextAuth.js в [документации](https://errors.authjs.dev/).

Наконец, в компоненте `login-form.tsx` вы можете использовать функцию React `useActionState` для вызова действия сервера, обработки ошибок формы и отображения ее состояния ожидания:

```ts title="app/ui/login-form.tsx" hl_lines="1 11-13 16-23 26 74-85 91-98"
'use client';

import { lusitana } from '@/app/ui/fonts';
import {
    AtSymbolIcon,
    KeyIcon,
    ExclamationCircleIcon,
} from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from '@/app/ui/button';
import { useActionState } from 'react';
import { authenticate } from '@/app/lib/actions';
import { useSearchParams } from 'next/navigation';

export default function LoginForm() {
    const searchParams = useSearchParams();
    const callbackUrl =
        searchParams.get('callbackUrl') || '/dashboard';
    const [
        errorMessage,
        formAction,
        isPending,
    ] = useActionState(authenticate, undefined);

    return (
        <form action={formAction} className="space-y-3">
            <div className="flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8">
                <h1
                    className={`${lusitana.className} mb-3 text-2xl`}
                >
                    Please log in to continue.
                </h1>
                <div className="w-full">
                    <div>
                        <label
                            className="mb-3 mt-5 block text-xs font-medium text-gray-900"
                            htmlFor="email"
                        >
                            Email
                        </label>
                        <div className="relative">
                            <input
                                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                                id="email"
                                type="email"
                                name="email"
                                placeholder="Enter your email address"
                                required
                            />
                            <AtSymbolIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
                        </div>
                    </div>
                    <div className="mt-4">
                        <label
                            className="mb-3 mt-5 block text-xs font-medium text-gray-900"
                            htmlFor="password"
                        >
                            Password
                        </label>
                        <div className="relative">
                            <input
                                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                                id="password"
                                type="password"
                                name="password"
                                placeholder="Enter password"
                                required
                                minLength={6}
                            />
                            <KeyIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
                        </div>
                    </div>
                </div>
                <input
                    type="hidden"
                    name="redirectTo"
                    value={callbackUrl}
                />
                <Button
                    className="mt-4 w-full"
                    aria-disabled={isPending}
                >
                    Log in{' '}
                    <ArrowRightIcon className="ml-auto h-5 w-5 text-gray-50" />
                </Button>
                <div
                    className="flex h-8 items-end space-x-1"
                    aria-live="polite"
                    aria-atomic="true"
                >
                    {errorMessage && (
                        <>
                            <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
                            <p className="text-sm text-red-500">
                                {errorMessage}
                            </p>
                        </>
                    )}
                </div>
            </div>
        </form>
    );
}
```

## Добавление функции выхода из системы

Чтобы добавить функцию выхода из системы в `<SideNav />`, вызовите функцию `signOut` из `auth.ts` в элементе `<form>`:

```ts title="/ui/dashboard/sidenav.tsx" hl_lines="5 15-18"
import Link from 'next/link';
import NavLinks from '@/app/ui/dashboard/nav-links';
import AcmeLogo from '@/app/ui/acme-logo';
import { PowerIcon } from '@heroicons/react/24/outline';
import { signOut } from '@/auth';

export default function SideNav() {
    return (
        <div className="flex h-full flex-col px-3 py-4 md:px-2">
            // ...
            <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
                <NavLinks />
                <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>
                <form
                    action={async () => {
                        'use server';
                        await signOut({ redirectTo: '/' });
                    }}
                >
                    <button className="flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3">
                        <PowerIcon className="w-6" />
                        <div className="hidden md:block">
                            Sign Out
                        </div>
                    </button>
                </form>
            </div>
        </div>
    );
}
```

## Попробуйте

Теперь попробуйте. Вы должны иметь возможность входить и выходить из приложения, используя следующие учетные данные:

-   Email: `user@nextmail.com`
-   Password: `123456`

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/adding-authentication></small>
