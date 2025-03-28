---
description: In the previous chapter, you finished building the invoices routes by adding form validation and improving accessibility. In this chapter, you'll be adding authentication to your dashboard.
---

# Adding Authentication

In the previous chapter, you finished building the invoices routes by adding form validation and improving accessibility. In this chapter, you'll be adding authentication to your dashboard.

!!!tip "Here are the topics we’ll cover"

    -   What is authentication.
    -   How to add authentication to your app using NextAuth.js.
    -   How to use Middleware to redirect users and protect your routes.
    -   How to use React's useActionState to handle pending states and form errors.

## What is authentication?

Authentication is a key part of many web applications today. It's how a system checks if the user is who they say they are.

A secure website often uses multiple ways to check a user's identity. For instance, after entering your username and password, the site may send a verification code to your device or use an external app like Google Authenticator. This 2-factor authentication (2FA) helps increase security. Even if someone learns your password, they can't access your account without your unique token.

### Authentication vs. Authorization

In web development, authentication and authorization serve different roles:

-   **Authentication** is about making sure the user is who they say they are. You're proving your identity with something you have like a username and password.
-   **Authorization** is the next step. Once a user's identity is confirmed, authorization decides what parts of the application they are allowed to use.

So, authentication checks who you are, and authorization determines what you can do or access in the application.

<?quiz?>

question: Which of the following best describes the difference between authentication and authorization?
answer: Authentication determines what you can access. Authorization verifies your identity.
answer: Authentication and authorization both decide what parts of the application a user can access.
answer-correct: Authentication verifies your identity. Authorization determines what you can access.
answer: There is no difference; both terms mean the same.
content:

<p>That's right! Although they sound similar, authentication verifies your identity while authorization determines what you can access.</p>
<?/quiz?>

## Creating the login route

Start by creating a new route in your application called `/login` and paste the following code:

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

You'll notice the page imports `<LoginForm />`, which you'll update later in the chapter. This component is wrapped with React `<Suspense>` because it will access information from the incoming request (URL search params).

## NextAuth.js

We will be using [NextAuth.js](https://nextjs.authjs.dev/) to add authentication to your application. NextAuth.js abstracts away much of the complexity involved in managing sessions, sign-in and sign-out, and other aspects of authentication. While you can manually implement these features, the process can be time-consuming and error-prone. NextAuth.js simplifies the process, providing a unified solution for auth in Next.js applications.

## Setting up NextAuth.js

Install NextAuth.js by running the following command in your terminal:

```sh title="Terminal"
pnpm i next-auth@beta
```

Here, you're installing the `beta` version of NextAuth.js, which is compatible with Next.js 14+.

Next, generate a secret key for your application. This key is used to encrypt cookies, ensuring the security of user sessions. You can do this by running the following command in your terminal:

```sh title="Terminal"
# macOS
openssl rand -base64 32
# Windows can use https://generate-secret.vercel.app/32
```

Then, in your `.env` file, add your generated key to the `AUTH_SECRET` variable:

```sh title=".env" hl_lines="1"
AUTH_SECRET=your-secret-key
```

For auth to work in production, you'll need to update your environment variables in your Vercel project too. Check out this [guide](https://vercel.com/docs/environment-variables) on how to add environment variables on Vercel.

### Adding the pages option

Create an `auth.config.ts` file at the root of our project that exports an `authConfig` object. This object will contain the configuration options for NextAuth.js. For now, it will only contain the `pages` option:

```ts title="/auth.config.ts"
import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
  pages: {
    signIn: '/login',
  },
} satisfies NextAuthConfig;
```

You can use the `pages` option to specify the route for custom sign-in, sign-out, and error pages. This is not required, but by adding `signIn: '/login'` into our `pages` option, the user will be redirected to our custom login page, rather than the NextAuth.js default page.

## Protecting your routes with Next.js Middleware

Next, add the logic to protect your routes. This will prevent users from accessing the dashboard pages unless they are logged in.

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

The `authorized` callback is used to verify if the request is authorized to access a page with [Next.js Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware). It is called before a request is completed, and it receives an object with the `auth` and `request` properties. The `auth` property contains the user's session, and the `request` property contains the incoming request.

The `providers` option is an array where you list different login options. For now, it's an empty array to satisfy NextAuth config. You'll learn more about it in the [Adding the Credentials provider](https://nextjs.org/learn/dashboard-app/adding-authentication#adding-the-credentials-provider) section.

Next, you will need to import the `authConfig` object into a Middleware file. In the root of your project, create a file called `middleware.ts` and paste the following code:

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

Here you're initializing NextAuth.js with the `authConfig` object and exporting the `auth` property. You're also using the `matcher` option from Middleware to specify that it should run on specific paths.

The advantage of employing Middleware for this task is that the protected routes will not even start rendering until the Middleware verifies the authentication, enhancing both the security and performance of your application.

### Password hashing

It's good practice to **hash** passwords before storing them in a database. Hashing converts a password into a fixed-length string of characters, which appears random, providing a layer of security even if the user's data is exposed.

When seeding your database, you used a package called `bcrypt` to hash the user's password before storing it in the database. You will use it _again_ later in this chapter to compare that the password entered by the user matches the one in the database. However, you will need to create a separate file for the `bcrypt` package. This is because `bcrypt` relies on Node.js APIs not available in Next.js Middleware.

Create a new file called `auth.ts` that spreads your `authConfig` object:

```ts title="/auth.ts"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
});
```

### Adding the Credentials provider

Next, you will need to add the `providers` option for NextAuth.js. `providers` is an array where you list different login options such as Google or GitHub. For this course, we will focus on using the [Credentials provider](https://authjs.dev/getting-started/providers/credentials-tutorial) only.

The Credentials provider allows users to log in with a username and a password.

```ts title="/auth.ts" hl_lines="3 7"
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
import Credentials from 'next-auth/providers/credentials';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [Credentials({})],
});
```

!!!info "Good to know"

    There are other alternative providers such as [OAuth](https://authjs.dev/getting-started/providers/oauth-tutorial) or [email](https://authjs.dev/getting-started/providers/email-tutorial). See the [NextAuth.js docs](https://authjs.dev/getting-started/providers) for a full list of options.

### Adding the sign in functionality

You can use the `authorize` function to handle the authentication logic. Similarly to Server Actions, you can use `zod` to validate the email and password before checking if the user exists in the database:

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

After validating the credentials, create a new `getUser` function that queries the user from the database.

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

Then, call `bcrypt.compare` to check if the passwords match:

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

Finally, if the passwords match you want to return the user, otherwise, return `null` to prevent the user from logging in.

### Updating the login form

Now you need to connect the auth logic with your login form. In your `actions.ts` file, create a new action called `authenticate`. This action should import the `signIn` function from `auth.ts`:

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

If there's a `'CredentialsSignin'` error, you want to show an appropriate error message. You can learn about NextAuth.js errors in [the documentation](https://errors.authjs.dev/).

Finally, in your `login-form.tsx` component, you can use React's `useActionState` to call the server action, handle form errors, and display the form's pending state:

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

## Adding the logout functionality

To add the logout functionality to `<SideNav />`, call the `signOut` function from `auth.ts` in your `<form>` element:

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

## Try it out

Now, try it out. You should be able to log in and out of your application using the following credentials:

-   Email: `user@nextmail.com`
-   Password: `123456`

<small>:material-information-outline: Источник &mdash; <https://nextjs.org/learn/dashboard-app/adding-authentication></small>
