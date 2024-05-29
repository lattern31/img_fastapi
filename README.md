# API для обработки картинок
## Технологии:
- Аутентификация: fastapi-users
- ORM: асинхронная sqlalchemy
- Фоновые задачи и их отслеживание: celery(redis), flower
- Дб: postgresql
- Контейнеризация: docker, docker-compose
## TODO:
- Кэширование на redis
- Миграции через alembic
- Поиск, фильтрация, пагинация картинок
- Тамбнэйлы через celery
- Тесты на pytest
## Запуск:
- Заполнить .env по аналогии с .env.example
- make, make logs, make down
