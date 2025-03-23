## Бэк
Джанго

## Фронт
nuxt

## Разработка

Запустить докер с пробросом базы наружу `docker compose -f compose.yaml -f compose.db.yaml`, потом запустить бэк `POSTGRES_PORT=88 POSTGRES_HOST=localhost poetry run python manage.py runserver`