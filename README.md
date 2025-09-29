# README


## Описание


Блог-платформа на FastAPI.


---
## Требования

- Python
- PostgreSQL
- Docker и Docker Compose
- Git

Установка
---
1. `git clone https://github.com/OverCart345/Savin.git` и `cd Savin`
2. `python -m venv .venv`
3. Активировать виртуальное окружение
4. `pip install -r requirements.txt`
5. `cp .env.example .env`
6. Заполнить `.env` по таблице ниже

---
## Описание полей .env файла

Вот описание для твоих переменных окружения:

- `POSTGRES_HOST`: адрес сервера базы данных PostgreSQL (например, `localhost` для локального запуска или хост в облаке).  
- `POSTGRES_PORT`: порт, на котором доступна база данных PostgreSQL (по умолчанию `5432`).  
- `POSTGRES_DB`: имя базы данных, к которой будет подключаться приложение.  
- `POSTGRES_USER`: имя пользователя для подключения к базе данных.  
- `POSTGRES_PASSWORD`: пароль пользователя для подключения к базе данных.  

- `SECRET_KEY`: секретный ключ, используемый для генерации и проверки JWT-токенов.  
- `ALGORITHM`: алгоритм шифрования/подписи JWT (обычно `HS256`).  
- `ACCESS_TOKEN_EXPIRE_MINUTES`: время жизни access-токена в минутах.  

---

## Запуск через dev профиль

- Запуск БД (Docker): `docker compose --profile dev up --build -d`
 - Применить миграции: `docker compose --profile dev run --rm app alembic upgrade head`
- Запуск приложения: `uvicorn src.main:app --reload`
- Хелсчек: `curl http://localhost:8000/healthz`

Запуск через prod профиль
---

 - Запуск БД + приложение: `docker compose --profile prod up --build -d`
 - Применить миграции: `docker compose --profile prod run --rm app alembic upgrade head`
- Хелсчек: `curl http://localhost:8000/healthz`
