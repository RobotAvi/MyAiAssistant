---
marp: true
theme: default
paginate: true
size: 16:9
backgroundColor: #f8f9fa
color: #343a40
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
  .highlight {
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
  }
  .tech-stack {
    background: #e9ecef;
    padding: 0.5rem;
    margin: 0.2rem;
    border-radius: 4px;
    display: inline-block;
  }
---

# 🎯 HR Assistant
## Автоматизированный AI-помощник для поиска работы

![bg right:40% 80%](https://via.placeholder.com/400x300/667eea/ffffff?text=HR+Assistant)

**Презентация решения**
- Архитектура системы
- Развертывание на российских хостингах
- Инструкции по настройке

---

## 📋 Обзор решения

<div class="highlight">

**HR Assistant** - полностью автоматизированная система для поиска работы с использованием ИИ

</div>

### 🚀 Ключевые возможности
- 📄 **Анализ резюме** с помощью LLM
- 🔍 **Автоматический поиск** релевантных вакансий
- 📱 **Telegram уведомления** о найденных позициях
- ✅ **Интеллектуальный отбор** вакансий
- 📧 **Автоматическая отправка** резюме
- 📊 **Веб-интерфейс** для управления

---

## 🏗️ Архитектура системы

<div class="columns">

<div>

### Frontend Layer
<div class="tech-stack">Next.js 14</div>
<div class="tech-stack">React 18.2</div>
<div class="tech-stack">Tailwind CSS</div>
<div class="tech-stack">TypeScript</div>

### Backend Layer
<div class="tech-stack">FastAPI</div>
<div class="tech-stack">SQLAlchemy</div>
<div class="tech-stack">Pydantic</div>

</div>

<div>

### Task Processing
<div class="tech-stack">Celery Workers</div>
<div class="tech-stack">Celery Beat</div>
<div class="tech-stack">Redis Broker</div>

### Data Layer
<div class="tech-stack">PostgreSQL 15</div>
<div class="tech-stack">Alembic</div>
<div class="tech-stack">File Storage</div>

</div>

</div>

---

## � C4 Архитектурные диаграммы

### Level 1: System Context Diagram

```mermaid
C4Context
    title System Context диаграмма для HR Assistant

    Person(user, "Соискатель", "Пользователь, ищущий работу")
    Person(hr, "HR Специалист", "Получает резюме и отклики")
    
    System(hrAssistant, "HR Assistant", "Автоматизированная система поиска работы с использованием ИИ")
    
    System_Ext(jobSites, "Job Sites", "HeadHunter, SuperJob, Habr Career")
    System_Ext(openai, "OpenAI API", "GPT-4 для анализа резюме и вакансий")
    System_Ext(telegram, "Telegram Bot API", "Уведомления пользователю")
    System_Ext(email, "Email Service", "SMTP для отправки резюме")
    
    Rel(user, hrAssistant, "Загружает резюме, настраивает поиск")
    Rel(hrAssistant, user, "Отправляет уведомления о вакансиях")
    Rel(hrAssistant, jobSites, "Парсит вакансии")
    Rel(hrAssistant, openai, "Анализирует резюме и вакансии")
    Rel(hrAssistant, telegram, "Отправляет уведомления")
    Rel(hrAssistant, email, "Отправляет резюме HR")
    Rel(hrAssistant, hr, "Отправляет резюме и сопроводительные письма")
```

---

### Level 2: Container Diagram

```mermaid
C4Container
    title Container диаграмма для HR Assistant

    Person(user, "Соискатель", "Пользователь системы")
    
    Container_Boundary(c1, "HR Assistant System") {
        Container(frontend, "Web Frontend", "Next.js, React, TypeScript", "Веб-интерфейс для управления")
        Container(api, "API Backend", "FastAPI, Python", "REST API для бизнес-логики")
        Container(celery, "Task Workers", "Celery Workers", "Фоновая обработка задач")
        Container(scheduler, "Task Scheduler", "Celery Beat", "Планировщик периодических задач")
        Container(db, "Database", "PostgreSQL", "Хранение данных")
        Container(cache, "Cache & Queue", "Redis", "Кэш и очереди задач")
    }
    
    System_Ext(jobSites, "Job Sites", "Источники вакансий")
    System_Ext(openai, "OpenAI API", "ИИ анализ")
    System_Ext(telegram, "Telegram", "Уведомления")
    System_Ext(email, "Email SMTP", "Отправка резюме")
    
    Rel(user, frontend, "Использует", "HTTPS")
    Rel(frontend, api, "API вызовы", "JSON/REST")
    Rel(api, db, "Читает/записывает", "SQL")
    Rel(api, cache, "Кэширует данные", "Redis Protocol")
    Rel(scheduler, cache, "Ставит задачи в очередь", "Redis")
    Rel(celery, cache, "Получает задачи", "Redis")
    Rel(celery, db, "Читает/записывает", "SQL")
    Rel(celery, jobSites, "Парсит вакансии", "HTTP")
    Rel(celery, openai, "Анализирует", "API")
    Rel(celery, telegram, "Уведомляет", "Bot API")
    Rel(celery, email, "Отправляет резюме", "SMTP")
```

---

### Level 3: Component Diagram (Backend API)

```mermaid
C4Component
    title Component диаграмма для API Backend

    Container(frontend, "Web Frontend", "Next.js")
    Container(workers, "Celery Workers", "Background Tasks")
    
    Container_Boundary(api, "API Backend") {
        Component(userController, "User Controller", "FastAPI Router", "Управление пользователями")
        Component(resumeController, "Resume Controller", "FastAPI Router", "Управление резюме")
        Component(jobController, "Job Controller", "FastAPI Router", "Управление вакансиями")
        Component(telegramController, "Telegram Controller", "FastAPI Router", "Telegram интеграция")
        
        Component(resumeProcessor, "Resume Processor", "Service", "Обработка резюме")
        Component(jobScraper, "Job Scraper", "Service", "Парсинг вакансий")
        Component(llmService, "LLM Service", "Service", "ИИ анализ")
        Component(emailService, "Email Service", "Service", "Отправка email")
        Component(telegramService, "Telegram Service", "Service", "Telegram уведомления")
        
        Component(userModel, "User Model", "SQLAlchemy", "Модель пользователя")
        Component(resumeModel, "Resume Model", "SQLAlchemy", "Модель резюме")
        Component(jobModel, "Job Model", "SQLAlchemy", "Модель вакансии")
    }
    
    ContainerDb(db, "PostgreSQL", "База данных")
    Container(cache, "Redis", "Кэш и очереди")
    
    Rel(frontend, userController, "API запросы")
    Rel(frontend, resumeController, "API запросы")
    Rel(frontend, jobController, "API запросы")
    Rel(frontend, telegramController, "API запросы")
    
    Rel(userController, userModel, "Использует")
    Rel(resumeController, resumeModel, "Использует")
    Rel(resumeController, resumeProcessor, "Использует")
    Rel(jobController, jobModel, "Использует")
    Rel(telegramController, telegramService, "Использует")
    
    Rel(workers, jobScraper, "Выполняет задачи")
    Rel(workers, llmService, "Выполняет анализ")
    Rel(workers, emailService, "Отправляет email")
    Rel(workers, telegramService, "Отправляет уведомления")
    
    Rel(userModel, db, "SQL запросы")
    Rel(resumeModel, db, "SQL запросы")
    Rel(jobModel, db, "SQL запросы")
    
    Rel(resumeProcessor, cache, "Кэширует результаты")
    Rel(jobScraper, cache, "Кэширует данные")
```

---

### Data Flow Diagram - Поток обработки данных

```mermaid
flowchart TD
    A[Пользователь загружает резюме] --> B[Resume Processor]
    B --> C[LLM Service анализирует резюме]
    C --> D[Извлекает навыки и опыт]
    D --> E[Сохраняет в PostgreSQL]
    
    F[Celery Beat запускает поиск] --> G[Job Scraper]
    G --> H[Парсит вакансии с job-сайтов]
    H --> I[LLM Service анализирует вакансии]
    I --> J{Вакансия подходит?}
    
    J -->|Да| K[Сохраняет вакансию в DB]
    J -->|Нет| L[Отклоняет вакансию]
    
    K --> M[Telegram Service уведомляет]
    M --> N[Пользователь выбирает вакансии]
    N --> O[Email Service отправляет резюме]
    
    P[Redis Cache] -.-> G
    P -.-> I
    P -.-> M
    
    Q[(PostgreSQL)] -.-> E
    Q -.-> K
    Q -.-> O
    
    style A fill:#e1f5fe
    style M fill:#f3e5f5
    style O fill:#e8f5e8
    style J fill:#fff3e0
```

---

### Схема интеграций и внешних сервисов

```mermaid
graph TB
    subgraph "HR Assistant System"
        API[FastAPI Backend]
        WEB[Next.js Frontend]
        CELERY[Celery Workers]
        DB[(PostgreSQL)]
        REDIS[(Redis)]
    end
    
    subgraph "Внешние job-сайты"
        HH[HeadHunter.ru]
        SJ[SuperJob.ru]
        HC[Habr Career]
    end
    
    subgraph "AI и уведомления"
        OPENAI[OpenAI GPT-4]
        TG[Telegram Bot API]
        SMTP[Email SMTP]
    end
    
    subgraph "Пользователи"
        USER[Соискатель]
        HR[HR Специалист]
    end
    
    USER --> WEB
    WEB --> API
    API --> DB
    API --> REDIS
    
    CELERY --> DB
    CELERY --> REDIS
    CELERY --> HH
    CELERY --> SJ
    CELERY --> HC
    CELERY --> OPENAI
    CELERY --> TG
    CELERY --> SMTP
    
    TG --> USER
    SMTP --> HR
    
    style USER fill:#bbdefb
    style HR fill:#c8e6c9
    style OPENAI fill:#ffecb3
    style TG fill:#f8bbd9
    style DB fill:#b39ddb
    style REDIS fill:#ffcdd2
```

---

## �🔧 Технический стек

| Компонент | Технология | Версия | Назначение |
|-----------|------------|--------|------------|
| **Frontend** | Next.js | 14.0.3 | React-фреймворк с SSR |
| **UI** | Tailwind CSS | 3.3.6 | Responsive дизайн |
| **Backend** | FastAPI | Latest | Асинхронный API сервер |
| **Database** | PostgreSQL | 15+ | Основная база данных |
| **Cache/Queue** | Redis | 7+ | Кэш и брокер сообщений |
| **Task Queue** | Celery | Latest | Асинхронные задачи |
| **LLM** | OpenAI API | GPT-4 | Анализ резюме и вакансий |
| **Notifications** | Telegram Bot | Latest | Уведомления пользователю |

---

## 🐳 Docker архитектура

```yaml
services:
  frontend:     # Next.js приложение (порт 3000)
  backend:      # FastAPI сервер (порт 8000) 
  postgres:     # База данных (порт 5432)
  redis:        # Брокер сообщений (порт 6379)
  celery:       # Фоновые задачи
  celery-beat:  # Планировщик задач
```

### 🔄 Взаимодействие сервисов
- Frontend ↔ Backend (REST API)
- Backend ↔ PostgreSQL (ORM)
- Backend ↔ Redis (кэш + очереди)
- Celery ↔ Redis (задачи)
- Celery ↔ External APIs (OpenAI, Telegram, Email)

---

## 🚀 Развертывание: Selectel Cloud

### 1️⃣ Создание инфраструктуры

<div class="columns">

<div>

**Рекомендуемая конфигурация:**
- CPU: 2 vCPU
- RAM: 4 GB  
- SSD: 40 GB
- OS: Ubuntu 22.04 LTS

</div>

<div>

```bash
# Подключение к серверу
ssh root@your-server-ip

# Обновление системы
apt update && apt upgrade -y
```

</div>

</div>

### 💰 Стоимость: ~2,000₽/месяц
- VM (2 vCPU, 4GB RAM): ~1,500₽
- Домен + SSL: ~500₽

---

## 🔧 Установка зависимостей

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Установка Nginx
apt install nginx -y

# Клонирование проекта
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant
```

---

## ⚙️ Конфигурация .env

```env
# Database
DATABASE_URL=postgresql://hr_user:secure_password@postgres:5432/hr_assistant

# Redis
REDIS_URL=redis://redis:6379

# OpenAI API
OPENAI_API_KEY=sk-your-openai-key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Email SMTP
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Production settings
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.ru,your-server-ip
SECRET_KEY=your-very-secure-secret-key
```

---

## 🌐 Настройка Nginx

```nginx
server {
    listen 80;
    server_name your-domain.ru;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 🔒 SSL сертификат
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.ru
```

---

## 🚀 Запуск приложения

```bash
# Настройка переменных окружения
cp .env.example .env
nano .env

# Сборка и запуск контейнеров
docker-compose up -d --build

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### ✅ Проверка работоспособности
- Frontend: http://your-domain.ru
- Backend API: http://your-domain.ru/api
- API Docs: http://your-domain.ru/api/docs

---

## 🌟 Yandex Cloud

<div class="columns">

<div>

### Создание инфраструктуры
```bash
yc compute instance create \
  --name hr-assistant \
  --zone ru-central1-a \
  --memory 4GB \
  --cores 2 \
  --ssh-key ~/.ssh/id_rsa.pub
```

### Managed PostgreSQL
```bash
yc managed-postgresql cluster create \
  --name hr-assistant-db \
  --postgresql-version 15 \
  --disk-size 20GB
```

</div>

<div>

### 💰 Стоимость: ~3,200₽/месяц
- Compute Instance: ~1,800₽
- Managed PostgreSQL: ~1,200₽  
- Object Storage: ~200₽

### Преимущества
- ✅ Managed сервисы
- ✅ Автобэкапы
- ✅ Мониторинг из коробки

</div>

</div>

---

## 🔧 VK Cloud (mail.ru)

<div class="columns">

<div>

### Быстрое развертывание
```bash
# Подключение к серверу
ssh ubuntu@your-server-ip

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Запуск приложения
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant
cp .env.example .env
docker-compose up -d --build
```

</div>

<div>

### 💰 Стоимость: ~2,400₽/месяц
- Virtual Machine: ~1,400₽
- Database: ~1,000₽

### Особенности
- ✅ Российская юрисдикция
- ✅ Техподдержка на русском
- ✅ Быстрое развертывание

</div>

</div>

---

## 📊 Мониторинг и логирование

<div class="columns">

<div>

### Системные метрики
```bash
# Node Exporter
docker run -d --name node-exporter \
  -p 9100:9100 \
  prom/node-exporter

# Prometheus
docker run -d --name prometheus \
  -p 9090:9090 \
  prom/prometheus
```

</div>

<div>

### Логирование
```bash
# Просмотр логов сервисов
docker-compose logs -f backend
docker-compose logs -f celery
docker-compose logs -f frontend

# Health checks
curl http://localhost:8000/health
curl http://localhost:3000/api/health
```

</div>

</div>

### 📈 Метрики для отслеживания
- Использование CPU/RAM
- Количество обработанных вакансий
- Время отклика API
- Статус внешних сервисов (OpenAI, Telegram)

---

## 🔒 Безопасность

<div class="columns">

<div>

### Firewall
```bash
# UFW конфигурация
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP  
ufw allow 443/tcp   # HTTPS
ufw --force enable
```

### Backup стратегия
```bash
# Ежедневный backup БД
docker exec postgres pg_dump \
  -U hr_user hr_assistant > \
  /backups/hr_assistant_$(date +%Y%m%d).sql
```

</div>

<div>

### Рекомендации
- ✅ Использовать сильные пароли
- ✅ Настроить SSH ключи
- ✅ Регулярно обновлять систему
- ✅ Ограничить доступ к портам
- ✅ Настроить автобэкапы
- ✅ Мониторить логи безопасности

</div>

</div>

---

## 🚀 Оптимизация производительности

### Redis настройки
```bash
echo "maxmemory 1gb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
systemctl restart redis
```

### PostgreSQL тюнинг
```sql
-- Оптимизация для 4GB RAM
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
SELECT pg_reload_conf();
```

### Nginx кэширование
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 📈 Масштабирование

<div class="columns">

<div>

### Горизонтальное масштабирование
```yaml
# docker-compose.scale.yml
services:
  backend:
    deploy:
      replicas: 2
  
  celery:
    deploy:
      replicas: 3
      
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
```

</div>

<div>

### Load Balancer
```nginx
upstream backend {
    server backend_1:8000;
    server backend_2:8000;
}

upstream frontend {
    server frontend_1:3000;
    server frontend_2:3000;
}
```

### Когда масштабировать?
- > 1000 пользователей
- > 100 вакансий в день
- CPU > 80%
- RAM > 85%

</div>

</div>

---

## 🆘 Troubleshooting

| Проблема | Диагностика | Решение |
|----------|-------------|---------|
| Сервис не запускается | `docker-compose logs service_name` | Проверить конфигурацию |
| БД недоступна | `docker-compose ps postgres` | Перезапустить контейнер |
| Redis ошибки | `redis-cli ping` | Проверить память Redis |
| Медленная работа | `htop`, `docker stats` | Оптимизировать ресурсы |
| OpenAI ошибки | Проверить API ключ | Обновить токен |
| Telegram не работает | Проверить webhook | Настроить ngrok для локальной разработки |

### 🔧 Полезные команды
```bash
# Перезапуск сервиса
docker-compose restart service_name

# Просмотр ресурсов
docker stats

# Очистка логов
docker-compose logs --tail=0 -f
```

---

## 💰 Сравнение хостингов

| Хостинг | Месячная стоимость | Преимущества | Недостатки |
|---------|-------------------|--------------|------------|
| **Selectel** | ~2,000₽ | Доступность, простота | Ручная настройка |
| **Yandex Cloud** | ~3,200₽ | Managed сервисы, автобэкапы | Высокая стоимость |
| **VK Cloud** | ~2,400₽ | Российская юрисдикция | Меньше managed сервисов |

### 🏆 Рекомендации
- **Для стартапов**: Selectel (минимальная стоимость)
- **Для бизнеса**: Yandex Cloud (надежность)
- **Для корпораций**: VK Cloud (соответствие законодательству)

---

## 📞 Поддержка и контакты

<div class="highlight">

### 📧 Контакты
- **GitHub Issues**: https://github.com/your-username/hr-assistant/issues
- **Email поддержка**: support@hrassistant.ru
- **Telegram**: @hrassistantbot
- **Документация**: https://docs.hrassistant.ru

</div>

### 🎯 Roadmap
- [ ] Интеграция с российскими job-сайтами
- [ ] Мобильное приложение
- [ ] A/B тестирование сопроводительных писем
- [ ] Интеграция с LinkedIn через API
- [ ] Аналитика эффективности откликов

---

## 🎉 Спасибо за внимание!

<div class="highlight">

**HR Assistant** - ваш персональный AI-помощник для поиска работы

</div>

### 🚀 Готовы начать?
1. Клонируйте репозиторий
2. Настройте переменные окружения  
3. Запустите `docker-compose up -d --build`
4. Откройте http://localhost:3000

### ❓ Вопросы?
Задавайте вопросы прямо сейчас!

*Создано с ❤️ для автоматизации поиска работы в России*