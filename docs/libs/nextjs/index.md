# Начало работы с Next.js

Для создания проекта рекомендуется использовать `create-next-app`:

```bash
yarn create next-app app-name
# typescript
yarn create next-app app-name --typescript
```

Ручная установка:

-   устанавливаем зависимости:

```bash
yarn add next react react-dom
```

-   обновляем `package.json`:

```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

Запуск сервера для разработки:

```bash
yarn dev
```
