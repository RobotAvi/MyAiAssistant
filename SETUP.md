# Установка и настройка HR Assistant

## Требования

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Git

## Быстрый старт с Docker

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant
```

2. **Настройте переменные окружения:**
```bash
make setup-env
```

3. **Отредактируйте `.env` файл:**
```bash
# Добавьте ваши API ключи
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
```

4. **Запустите с Docker:**
```bash
make docker-up
```

5. **Откройте в браузере:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Локальная разработка

### 1. Установка зависимостей

```bash
# Python зависимости
pip install -r requirements.txt

# Node.js зависимости
npm install
```

### 2. Настройка базы данных

```bash
# Создайте базу данных PostgreSQL
createdb hr_assistant

# Настройте переменные окружения
export DATABASE_URL=postgresql://user:password@localhost:5432/hr_assistant

# Примените миграции
make init-db
```

### 3. Запуск Redis

```bash
# Ubuntu/Debian
sudo systemctl start redis-server

# macOS (Homebrew)
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 4. Запуск приложения

**Вариант 1: Полный стек**
```bash
make dev
```

**Вариант 2: Раздельно**
```bash
# Terminal 1: Backend
make dev-backend

# Terminal 2: Frontend
make dev-frontend

# Terminal 3: Celery Worker (опционально)
make celery-worker

# Terminal 4: Celery Beat (опционально)
make celery-beat
```

## Настройка внешних сервисов

### OpenAI API

1. Зарегистрируйтесь на https://platform.openai.com/
2. Получите API ключ
3. Добавьте в `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

### Telegram Bot

1. Создайте бота через @BotFather в Telegram
2. Получите токен бота
3. Добавьте в `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. Настройте webhook:
```bash
curl -X POST http://localhost:8000/api/telegram/setup-webhook
```

### Email (Gmail)

1. Включите двухфакторную аутентификацию
2. Создайте пароль приложения
3. Добавьте в `.env`:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
```

### HeadHunter API (опционально)

1. Зарегистрируйте приложение на https://dev.hh.ru/
2. Добавьте API ключ в `.env`:
```
HH_API_KEY=your_hh_api_key_here
```

## Использование

### 1. Первоначальная настройка

1. Откройте http://localhost:3000
2. Создайте пользователя или войдите
3. Загрузите ваше резюме
4. Настройте Telegram уведомления

### 2. Автоматический поиск

- Система автоматически ищет вакансии каждое утро в 9:00
- Уведомления приходят в Telegram
- Выбирайте интересные вакансии прямо в боте

### 3. Отклик на вакансии

- Система автоматически генерирует сопроводительные письма
- Отправляет резюме на выбранные вакансии
- Ищет и пишет HR-специалистам

## Troubleshooting

### Ошибки запуска

**"ModuleNotFoundError"**
```bash
# Переустановите зависимости
pip install -r requirements.txt
```

**"Connection refused" (PostgreSQL)**
```bash
# Проверьте статус PostgreSQL
sudo systemctl status postgresql

# Запустите сервис
sudo systemctl start postgresql
```

**"Connection refused" (Redis)**
```bash
# Проверьте статус Redis
redis-cli ping

# Запустите Redis
sudo systemctl start redis-server
```

### Проблемы с Telegram

**Webhook не работает**
- Убедитесь, что сервер доступен извне
- Используйте ngrok для локальной разработки:
```bash
ngrok http 8000
# Используйте HTTPS URL для webhook
```

### Проблемы с Email

**"Authentication failed"**
- Убедитесь, что используете пароль приложения, а не обычный пароль
- Проверьте настройки безопасности Gmail

## Разработка

### Структура проекта

```
hr-assistant/
├── app/                    # Backend (FastAPI)
│   ├── api/               # API роутеры
│   ├── models/            # Модели БД
│   ├── services/          # Бизнес-логика
│   ├── core/              # Конфигурация
│   └── db/                # База данных
├── app/                   # Frontend (Next.js)
│   ├── components/        # React компоненты
│   ├── pages/             # Страницы
│   ├── styles/            # Стили
│   └── utils/             # Утилиты
├── uploads/               # Загруженные файлы
└── docs/                  # Документация
```

### API документация

После запуска backend, API документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Тестирование

```bash
# Запуск тестов
make test

# Тестирование конкретного модуля
python -m pytest tests/test_llm_service.py -v
```

## Деплой

### Production настройки

1. Используйте отдельные `.env` файлы для production
2. Настройте reverse proxy (nginx)
3. Используйте HTTPS
4. Настройте мониторинг и логирование
5. Создайте резервные копии БД

### Docker Swarm / Kubernetes

Файлы конфигурации для оркестрации находятся в папке `deploy/`.

## Поддержка

- GitHub Issues: https://github.com/your-username/hr-assistant/issues
- Email: support@hrassistant.ru
- Telegram: @hrassistantbot