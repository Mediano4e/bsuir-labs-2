# Система контроля удовлетворённости клиентов

#### [Диаграммы и описание системы](https://docs.google.com/document/d/1_MS2gQn3VS9mhUCzXOjkoSgQmgv0ZgbJ7ZDY-ttQgS4/edit?tab=t.0)

### Запуск программы

1. Подготовка окружения
   ```
   cd lab2
   mv .env.example .env
   ```
2. Запуск докер сервисов
   ```
   docker compose up --build
   ```

### Структура проекта

```
lab2
├─ .env
├─ Dockerfile
├─ README.md
├─ application.log
├─ docker-compose.yml
├─ init.sql
├─ main.py
├─ requirements.txt
└─ src
   ├─ __init__.py
   ├─ control
   │  ├─ __init__.py
   │  ├─ authorization.py
   │  └─ registration.py
   ├─ model
   │  ├─ __init__.py
   │  └─ user.py
   └─ view
      ├─ administrator.html
      ├─ analyst.html
      ├─ auth.html
      ├─ client.html
      └─ registration.html

```

### P.S. Восстановление пароля реализовывать лень
