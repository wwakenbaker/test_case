Чтобы запустить тесты, нужно добавить точку в начале импортов
models и schemas в app.py

Запуск приложения командой docker compose up

Запуск отдельно базы данных:
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:12-alpine