## Бэк
Django REST Framework

## Фронт
Nuxt.js 3

## Настройка переменных окружения

1. Создайте файл `.env` в корне проекта (см. `ENV_SETUP.md`)
2. Установите SECRET_KEY и другие переменные окружения

## Разработка

Запустить докер с пробросом базы наружу:
```bash
docker compose -f compose.yaml -f compose.db.yaml up
```

Затем запустить бэк локально:
```bash
POSTGRES_PORT=88 POSTGRES_HOST=localhost poetry run python manage.py runserver
```

После запуска бэка запустить фронт:
```bash
NUXT_PUBLIC_API_BASE=http://localhost:8000 NUXT_PUBLIC_IMG_BASE=http://localhost:8000/media npm run dev
```