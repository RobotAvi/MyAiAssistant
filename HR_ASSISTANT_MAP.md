# 🎯 HR Assistant - Map-презентация решения

## 📋 Обзор решения

**HR Assistant** - автоматизированная система для поиска работы и отклика на вакансии с использованием ИИ.

### 🚀 Ключевые возможности
- 📄 **Анализ резюме** с помощью LLM
- 🔍 **Автоматический поиск** релевантных вакансий
- 📱 **Telegram уведомления** о найденных позициях
- ✅ **Интеллектуальный отбор** вакансий
- 📧 **Автоматическая отправка** резюме и сопроводительных писем
- 📊 **Веб-интерфейс** для управления процессом

---

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────────┐
│                         HR ASSISTANT                            │
├─────────────────────────────────────────────────────────────────┤
│                      🌐 Frontend Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Next.js 14    │  │  Tailwind CSS   │  │   TypeScript    │  │
│  │  React 18.2     │  │   Responsive    │  │   Type Safety   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                      ⚙️ Backend Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │    FastAPI      │  │   SQLAlchemy    │  │     Pydantic    │  │
│  │  Async/Await    │  │      ORM        │  │   Validation    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                    🔄 Task Processing                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │     Celery      │  │   Celery Beat   │  │      Redis      │  │
│  │    Workers      │  │   Scheduler     │  │     Broker      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     💾 Data Layer                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   PostgreSQL    │  │     Alembic     │  │   File Storage  │  │
│  │   Database      │  │   Migrations    │  │    Uploads      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                  🌍 External Services                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   OpenAI API    │  │  Telegram Bot   │  │   Email SMTP    │  │
│  │   GPT Models    │  │  Notifications  │  │   Mail Sender   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 Технический стек

| Компонент | Технология | Версия | Назначение |
|-----------|------------|--------|------------|
| **Frontend** | Next.js | 14.0.3 | React-фреймворк с SSR |
| **UI** | Tailwind CSS | 3.3.6 | Responsive дизайн |
| **Backend** | FastAPI | Latest | Асинхронный API сервер |
| **Database** | PostgreSQL | 15+ | Основная база данных |
| **Cache/Queue** | Redis | 7+ | Кэш и брокер сообщений |
| **Task Queue** | Celery | Latest | Асинхронные задачи |
| **LLM** | OpenAI API | GPT-4 | Анализ резюме и вакансий |
| **Notifications** | Telegram Bot API | Latest | Уведомления пользователю |
| **Email** | SMTP | - | Отправка резюме |

---

## 🚀 Развертывание на российских хостингах

### 🎯 Selectel Cloud

#### 1. Создание инфраструктуры

```bash
# 1. Создайте виртуальную машину в Selectel
# Рекомендуемая конфигурация:
# - CPU: 2 vCPU
# - RAM: 4 GB
# - SSD: 40 GB
# - OS: Ubuntu 22.04 LTS

# 2. Подключитесь к серверу
ssh root@your-server-ip
```

#### 2. Установка зависимостей

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Установка Nginx
apt install nginx -y
```

#### 3. Клонирование и настройка проекта

```bash
# Клонирование репозитория
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant

# Настройка переменных окружения
cp .env.example .env
nano .env
```

#### 4. Конфигурация .env для production

```env
# Database
DATABASE_URL=postgresql://hr_user:your_secure_password@postgres:5432/hr_assistant

# Redis
REDIS_URL=redis://redis:6379

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Email
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Production settings
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.ru,your-server-ip

# Security
SECRET_KEY=your-very-secure-secret-key
```

#### 5. Настройка Nginx

```bash
# Создание конфигурации Nginx
cat > /etc/nginx/sites-available/hr-assistant << 'EOF'
server {
    listen 80;
    server_name your-domain.ru www.your-domain.ru;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Активация конфигурации
ln -s /etc/nginx/sites-available/hr-assistant /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 6. SSL сертификат (Let's Encrypt)

```bash
# Установка Certbot
apt install certbot python3-certbot-nginx -y

# Получение SSL сертификата
certbot --nginx -d your-domain.ru -d www.your-domain.ru
```

#### 7. Запуск приложения

```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### 🌟 Yandex Cloud

#### 1. Создание Compute Instance

```bash
# Через CLI Yandex Cloud
yc compute instance create \
  --name hr-assistant \
  --zone ru-central1-a \
  --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts,size=40GB \
  --memory 4GB \
  --cores 2 \
  --ssh-key ~/.ssh/id_rsa.pub
```

#### 2. Настройка Managed PostgreSQL

```bash
# Создание кластера PostgreSQL
yc managed-postgresql cluster create \
  --name hr-assistant-db \
  --environment production \
  --network-name default \
  --postgresql-version 15 \
  --resource-preset s2.micro \
  --disk-size 20GB \
  --user name=hr_user,password=your_secure_password \
  --database name=hr_assistant,owner=hr_user
```

#### 3. Object Storage для файлов

```bash
# Создание S3 bucket для загрузок
yc storage bucket create --name hr-assistant-uploads
```

### 🔧 VK Cloud (mail.ru)

#### Быстрое развертывание

```bash
# 1. Создание инстанса через web-интерфейс
# 2. Подключение к серверу
ssh ubuntu@your-server-ip

# 3. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Клонирование и запуск
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant
cp .env.example .env
# Отредактируйте .env файл
docker-compose up -d --build
```

---

## 📊 Мониторинг и логирование

### 1. Системные метрики

```bash
# Установка Node Exporter
docker run -d --name node-exporter \
  -p 9100:9100 \
  prom/node-exporter

# Установка Prometheus
docker run -d --name prometheus \
  -p 9090:9090 \
  prom/prometheus
```

### 2. Логирование приложения

```bash
# Просмотр логов сервисов
docker-compose logs -f backend
docker-compose logs -f celery
docker-compose logs -f frontend

# Настройка ротации логов
nano /etc/logrotate.d/hr-assistant
```

### 3. Healthcheck endpoints

```bash
# Проверка здоровья сервисов
curl http://localhost:8000/health
curl http://localhost:3000/api/health
```

---

## 🔒 Безопасность

### 1. Firewall настройки

```bash
# UFW конфигурация
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable
```

### 2. Backup стратегия

```bash
# Создание backup скрипта
cat > /root/backup-hr-assistant.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec postgres pg_dump -U hr_user hr_assistant > /backups/hr_assistant_$DATE.sql
find /backups -name "hr_assistant_*.sql" -mtime +7 -delete
EOF

chmod +x /root/backup-hr-assistant.sh

# Добавление в crontab (ежедневно в 2:00)
echo "0 2 * * * /root/backup-hr-assistant.sh" | crontab -
```

---

## 🚀 Оптимизация производительности

### 1. Redis настройки

```bash
# Оптимизация Redis для production
echo "maxmemory 1gb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
systemctl restart redis
```

### 2. PostgreSQL тюнинг

```sql
-- Оптимизация для 4GB RAM
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
ALTER SYSTEM SET wal_buffers = '16MB';
SELECT pg_reload_conf();
```

### 3. Nginx кэширование

```nginx
# Добавление кэширования статических файлов
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 📈 Масштабирование

### Горизонтальное масштабирование

```yaml
# docker-compose.scale.yml
version: '3.8'
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
    depends_on:
      - backend
```

### Load Balancer настройка

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

---

## 📞 Поддержка и контакты

### 🆘 Troubleshooting

| Проблема | Решение |
|----------|---------|
| Сервис не запускается | `docker-compose logs service_name` |
| БД недоступна | Проверить `docker-compose ps postgres` |
| Redis ошибки | `redis-cli ping` |
| Медленная работа | Проверить метрики `htop`, `docker stats` |

### 📧 Контакты

- **GitHub Issues**: https://github.com/your-username/hr-assistant/issues
- **Email поддержка**: support@hrassistant.ru
- **Telegram**: @hrassistantbot
- **Документация**: https://docs.hrassistant.ru

### 💰 Стоимость инфраструктуры

#### Selectel (месяц)
- VM (2 vCPU, 4GB RAM): ~1,500₽
- Домен + SSL: ~500₽
- **Итого**: ~2,000₽/месяц

#### Yandex Cloud (месяц)
- Compute Instance: ~1,800₽
- Managed PostgreSQL: ~1,200₽
- Object Storage: ~200₽
- **Итого**: ~3,200₽/месяц

#### VK Cloud (месяц)
- Virtual Machine: ~1,400₽
- Database: ~1,000₽
- **Итого**: ~2,400₽/месяц

---

*Создано с ❤️ для автоматизации поиска работы в России*