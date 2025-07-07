# HR Assistant

Автоматизированный HR-ассистент для поиска и отклика на вакансии

## Функциональность

- 📄 Загрузка и анализ резюме
- 🔍 Ежедневный поиск релевантных вакансий с помощью LLM
- 📱 Уведомления в Telegram о найденных вакансиях
- ✅ Выбор вакансий для отклика
- 📧 Автоматическая отправка резюме и писем HR-специалистам
- 📊 Веб-интерфейс для управления процессом

## Архитектура

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL
- **LLM**: OpenAI API
- **Scheduler**: Celery + Redis
- **Notifications**: Telegram Bot API
- **Email**: SMTP integration

## Установка и запуск

```bash
# Установка зависимостей
pip install -r requirements.txt
npm install

# Настройка переменных окружения
cp .env.example .env

# Запуск backend
uvicorn app.main:app --reload

# Запуск frontend
npm run dev
```

## Конфигурация

Настройте следующие переменные в `.env`:
- OpenAI API ключ
- Telegram Bot Token
- Настройки SMTP
- Настройки базы данных