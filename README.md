# Сервис микроблогов (Twitter-like)

Backend-часть корпоративного сервиса микроблогов, аналогичного Twitter. Реализована на FastAPI с использованием PostgreSQL в качестве базы данных.

## 🚀 Функциональность

- **Твиты**: создание, удаление, лента твитов
- **Медиа**: загрузка изображений к твитам
- **Лайки**: добавление/удаление лайков к твитам
- **Подписки**: подписка/отписка на других пользователей
- **Профили**: просмотр информации о пользователях
- **Авторизация**: через API-ключ в заголовках запросов

## 🛠 Технологический стек

- **Backend**: FastAPI
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Валидация**: Pydantic
- **Конфигурация**: Pydantic-Settings
- **Тестирование**: pytest
- **Контейнеризация**: Docker, Docker Compose
- **Управление зависимостями**: PDM
- **CI/CD**: GitHub Actions
- **Линтинг**: flake8, black

## 📋 API Endpoints

### Твиты
- `POST /api/tweets` - создание твита
- `DELETE /api/tweets/{id}` - удаление твита
- `GET /api/tweets` - получение ленты твитов
- `POST /api/tweets/{id}/likes` - лайк твита
- `DELETE /api/tweets/{id}/likes` - удаление лайка

### Медиа
- `POST /api/medias` - загрузка медиафайлов

### Пользователи
- `GET /api/users/me` - информация о текущем пользователе
- `GET /api/users/{id}` - информация о пользователе по ID
- `POST /api/users/{id}/follow` - подписка на пользователя
- `DELETE /api/users/{id}/follow` - отписка от пользователя

## 🏗 Архитектура

Проект реализован по трёхслойной архитектуре:

1. **API Layer** - обработка HTTP-запросов, валидация, сериализация
2. **Service Layer** - бизнес-логика приложения
3. **DAL (Data Access Layer)** - работа с базой данных

## 🚀 Запуск проекта

### Требования
- Docker
- Docker Compose

### Быстрый запуск


```bash

# Клонирование репозитория
git clone <repository-url>
cd microblog

# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка всех сервисов
docker-compose down
```

2. Создайте файл `.env` в директории `microblog/` со следующими параметрами по аналогии example.env:

```env
# Database
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=myapp_password
POSTGRES_DB=myapp
POSTGRES_HOST=db_postgres
POSTGRES_PORT=5432
```