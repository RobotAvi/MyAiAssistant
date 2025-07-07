# Архитектура HR Assistant

## Обзор системы

HR Assistant - это автоматизированная система поиска работы, использующая искусственный интеллект для анализа резюме, поиска релевантных вакансий и автоматической отправки заявок. Система построена на микросервисной архитектуре с разделением на frontend, backend, фоновые задачи и внешние интеграции.

## Архитектурная диаграмма

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Пользователь   │    │  Telegram Bot   │    │   HR/Рекрутер   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ HTTPS               │ Webhook               │ Email
          ▼                      ▼                      ▲
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX (Reverse Proxy)                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
          ┌───────────┴────────────┐
          │                        │
          ▼                        ▼
┌─────────────────┐    ┌─────────────────┐
│  Next.js App    │    │  FastAPI App    │
│  (Frontend)     │    │  (Backend)      │
│  Port: 3000     │    │  Port: 8000     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          │ API Calls           │ Database
          └──────────────────────┘ Queries
                                 │
                    ┌────────────┴─────────────┐
                    │                          │
                    ▼                          ▼
          ┌─────────────────┐    ┌─────────────────┐
          │   PostgreSQL    │    │     Redis       │
          │   (Database)    │    │    (Cache +     │
          │                 │    │   Message Q)    │
          └─────────────────┘    └─────────┬───────┘
                                           │
                              ┌────────────┴─────────────┐
                              │                          │
                              ▼                          ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │ Celery Worker   │    │  Celery Beat    │
                    │ (Job Processing)│    │  (Scheduler)    │
                    └─────────┬───────┘    └─────────────────┘
                              │
                              │ External APIs
                              ▼
          ┌─────────────────────────────────────────────────────┐
          │              External Services                      │
          │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
          │ │  OpenAI     │ │ HeadHunter  │ │    SMTP     │    │
          │ │     API     │ │     API     │ │   Server    │    │
          │ └─────────────┘ └─────────────┘ └─────────────┘    │
          └─────────────────────────────────────────────────────┘
```

## Компоненты системы

### Frontend (Next.js)
- **Технологии**: React 18, TypeScript, Tailwind CSS
- **Функции**: 
  - Пользовательский интерфейс
  - Загрузка резюме
  - Просмотр вакансий и заявок
  - Управление настройками
- **Особенности**: SSR, адаптивный дизайн, PWA возможности

### Backend (FastAPI)
- **Технологии**: Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **API Endpoints**:
  - `/api/users/` - управление пользователями
  - `/api/resumes/` - работа с резюме
  - `/api/jobs/` - поиск и управление вакансиями
  - `/api/telegram/` - Telegram интеграция
- **Особенности**: автодокументация, валидация данных, async/await

### База данных (PostgreSQL)
- **Модели данных**:
  ```sql
  Users (id, email, telegram_chat_id, settings)
  Resumes (id, user_id, file_path, analysis, embedding)
  Jobs (id, external_id, platform, details, match_score)
  JobApplications (id, user_id, job_id, status, emails)
  TelegramNotifications (id, user_id, type, data)
  ```

### Кэш и очереди (Redis)
- **Кэш**: результаты API запросов, сессии пользователей
- **Очереди**: фоновые задачи, отложенные операции
- **Pub/Sub**: real-time уведомления

### Фоновые задачи (Celery)
- **Worker**: обработка задач (анализ резюме, поиск вакансий)
- **Beat**: планировщик (ежедневный поиск в 9:00)
- **Задачи**:
  - `daily_job_search()` - поиск новых вакансий
  - `analyze_resume()` - анализ загруженного резюме
  - `send_applications()` - отправка заявок на вакансии
  - `weekly_summary()` - еженедельная статистика

### Внешние интеграции

#### AI/ML сервисы
- **OpenAI GPT-3.5/4**: анализ резюме, генерация писем
- **OpenAI Embeddings**: векторное представление текстов

#### Job platforms
- **HeadHunter API**: основной источник вакансий
- **hh.ru парсинг**: дополнительные данные
- **Расширения**: SuperJob, LinkedIn (planned)

#### Коммуникации
- **Telegram Bot API**: уведомления и интерактивность
- **SMTP**: отправка email заявок
- **Push notifications**: веб-уведомления (planned)

## Поток данных

### 1. Регистрация и настройка
```
Пользователь → Frontend → Backend → Database
                                 ↓
                            Telegram Setup
```

### 2. Загрузка резюме
```
File Upload → Backend → File Storage → LLM Analysis → Database
                                           ↓
                                    Embeddings Creation
```

### 3. Ежедневный поиск вакансий
```
Celery Beat → Celery Worker → Job APIs → LLM Matching → Database
                                                           ↓
                                              Telegram Notification
```

### 4. Отклик на вакансии
```
Telegram → Backend → LLM (Cover Letter) → Email Send → HR
                                             ↓
                                        Status Update
```

## Установка в продакшене с российскими провайдерами

### 1. Выбор хостинг-провайдера

#### Рекомендуемые VPS провайдеры:

**Selectel (selectel.ru)**
- **Конфигурация**: Cloud Server SSD-3 (4 CPU, 8GB RAM, 80GB SSD)
- **Цена**: ~3,500₽/месяц
- **Особенности**: российские ЦОД, высокая скорость
```bash
# Заказ через API Selectel
curl -X POST https://api.selectel.ru/servers/v2/servers \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"hr-assistant","flavor":"SSD-3","image":"ubuntu-22.04"}'
```

**Timeweb Cloud (timeweb.cloud)**
- **Конфигурация**: Cloud VPS S4 (4 CPU, 8GB RAM, 160GB SSD)
- **Цена**: ~2,800₽/месяц
- **Особенности**: российская компания, хорошая поддержка

**REG.RU Cloud (cloud.reg.ru)**
- **Конфигурация**: Облачный сервер M (4 CPU, 8GB RAM, 80GB SSD)
- **Цена**: ~4,200₽/месяч
- **Особенности**: интеграция с доменными услугами

**VK Cloud (cloud.vk.com)**
- **Конфигурация**: Стандарт S2 (4 CPU, 8GB RAM, 80GB SSD)
- **Цена**: ~3,000₽/месяц
- **Особенности**: часть экосистемы VK, российские сервисы

### 2. Настройка сервера

#### Подключение и базовая настройка:
```bash
# Подключение к серверу
ssh root@your-server-ip

# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y nginx postgresql postgresql-contrib redis-server \
               docker.io docker-compose certbot python3-certbot-nginx \
               git curl wget htop

# Настройка firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable
```

#### Настройка пользователя:
```bash
# Создание пользователя для приложения
adduser hrapp
usermod -aG docker hrapp
usermod -aG sudo hrapp

# Настройка SSH ключей
mkdir -p /home/hrapp/.ssh
cp ~/.ssh/authorized_keys /home/hrapp/.ssh/
chown -R hrapp:hrapp /home/hrapp/.ssh
chmod 700 /home/hrapp/.ssh
chmod 600 /home/hrapp/.ssh/authorized_keys
```

### 3. Настройка домена

#### Регистрация домена в российских регистраторах:

**REG.RU**
```bash
# Поиск и регистрация домена
# Интерфейс: https://www.reg.ru/domain/new/
# Стоимость .ru домена: ~300₽/год
```

**Яндекс.Домены (domain.yandex.ru)**
```bash
# Регистрация через Яндекс
# Стоимость .ru домена: ~199₽/год
```

#### DNS настройки:
```bash
# A записи
hrassistant.ru      → your-server-ip
api.hrassistant.ru  → your-server-ip
www.hrassistant.ru  → your-server-ip

# CNAME записи (если используете CDN)
static.hrassistant.ru → cdn.selectel.ru
```

### 4. Настройка SSL сертификатов

```bash
# Установка Certbot для Nginx
certbot --nginx -d hrassistant.ru -d api.hrassistant.ru -d www.hrassistant.ru

# Автоматическое обновление
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### 5. Настройка базы данных

#### Локальная PostgreSQL:
```bash
# Настройка PostgreSQL
sudo -u postgres psql
CREATE DATABASE hr_assistant;
CREATE USER hrapp WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE hr_assistant TO hrapp;
\q

# Настройка подключений
echo "host hr_assistant hrapp 127.0.0.1/32 md5" >> /etc/postgresql/14/main/pg_hba.conf
systemctl restart postgresql
```

#### Или Yandex Managed PostgreSQL:
```bash
# Создание кластера через yc CLI
yc managed-postgresql cluster create \
  --name hr-assistant-db \
  --environment production \
  --network-name default \
  --host zone-id=ru-central1-a,subnet-name=default-ru-central1-a \
  --postgresql-version 14 \
  --resource-preset s2.micro \
  --disk-size 20GB \
  --disk-type network-ssd

# Получение строки подключения
yc managed-postgresql cluster list-hosts hr-assistant-db
```

### 6. Конфигурация приложения

#### Production .env файл:
```bash
# /home/hrapp/hr-assistant/.env
DATABASE_URL=postgresql://hrapp:secure_password@localhost:5432/hr_assistant
REDIS_URL=redis://localhost:6379

# OpenAI (через российские прокси если нужно)
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1  # или российский прокси

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_WEBHOOK_URL=https://api.hrassistant.ru/api/telegram/webhook

# Email через российские SMTP
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=587
EMAIL_USER=noreply@hrassistant.ru
EMAIL_PASSWORD=your-app-password

# HeadHunter API
HH_API_KEY=your-hh-api-key

# Security
SECRET_KEY=generate-secure-secret-key-here
DEBUG=False
FRONTEND_URL=https://hrassistant.ru

# Yandex Object Storage для файлов
AWS_ACCESS_KEY_ID=your-yandex-key
AWS_SECRET_ACCESS_KEY=your-yandex-secret
AWS_STORAGE_BUCKET_NAME=hr-assistant-files
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net
```

### 7. Настройка файлового хранилища

#### Yandex Object Storage:
```bash
# Создание бакета через консоль или CLI
yc storage bucket create --name hr-assistant-files

# Настройка CORS для веб-доступа
yc storage bucket update \
  --name hr-assistant-files \
  --cors file://cors-config.json
```

#### Локальное хранилище с бэкапом:
```bash
# Создание директорий
mkdir -p /var/www/hr-assistant/uploads
chown -R hrapp:hrapp /var/www/hr-assistant

# Настройка rsync бэкапа в Object Storage
# /etc/cron.daily/backup-uploads
#!/bin/bash
rsync -avz /var/www/hr-assistant/uploads/ \
  hrapp@backup-server:/backups/hr-assistant/
```

### 8. Настройка Nginx

```nginx
# /etc/nginx/sites-available/hr-assistant
server {
    listen 80;
    server_name hrassistant.ru www.hrassistant.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name hrassistant.ru www.hrassistant.ru;

    ssl_certificate /etc/letsencrypt/live/hrassistant.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hrassistant.ru/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Frontend
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

    # Static files
    location /uploads/ {
        alias /var/www/hr-assistant/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

server {
    listen 443 ssl http2;
    server_name api.hrassistant.ru;

    ssl_certificate /etc/letsencrypt/live/hrassistant.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hrassistant.ru/privkey.pem;

    # API Backend
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Увеличиваем лимиты для загрузки файлов
        client_max_body_size 50M;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

### 9. Docker Compose для продакшена

```yaml
# /home/hrapp/hr-assistant/docker-compose.prod.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: hr-frontend
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.hrassistant.ru/api
    ports:
      - "3000:3000"
    networks:
      - hr-network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: hr-backend
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - /var/www/hr-assistant/uploads:/app/uploads
    depends_on:
      - redis
    networks:
      - hr-network

  celery-worker:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: hr-celery-worker
    restart: unless-stopped
    command: celery -A app.services.scheduler worker --loglevel=info --concurrency=4
    env_file:
      - .env
    volumes:
      - /var/www/hr-assistant/uploads:/app/uploads
    depends_on:
      - redis
    networks:
      - hr-network

  celery-beat:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: hr-celery-beat
    restart: unless-stopped
    command: celery -A app.services.scheduler beat --loglevel=info
    env_file:
      - .env
    depends_on:
      - redis
    networks:
      - hr-network

  redis:
    image: redis:7-alpine
    container_name: hr-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - hr-network

volumes:
  redis_data:

networks:
  hr-network:
    driver: bridge
```

### 10. Мониторинг и логирование

#### Настройка логирования:
```bash
# Настройка rsyslog для централизованного логирования
echo "*.* @@logs.hrassistant.ru:514" >> /etc/rsyslog.conf

# Ротация логов
cat > /etc/logrotate.d/hr-assistant << EOF
/var/log/hr-assistant/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 0640 hrapp hrapp
    postrotate
        systemctl reload nginx
    endscript
}
EOF
```

#### Мониторинг с российскими сервисами:

**Yandex Monitoring**
```bash
# Установка агента мониторинга
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
yc config profile create production

# Настройка алертов через API
yc monitoring alert-rule create \
  --name "HR Assistant High CPU" \
  --folder-id $FOLDER_ID \
  --condition "cpu_utilization > 80"
```

**Zabbix (self-hosted)**
```bash
# Установка Zabbix агента
wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-4+ubuntu22.04_all.deb
dpkg -i zabbix-release_6.0-4+ubuntu22.04_all.deb
apt update && apt install zabbix-agent2

# Настройка мониторинга
echo "Server=monitoring.hrassistant.ru" >> /etc/zabbix/zabbix_agent2.conf
systemctl enable zabbix-agent2
systemctl start zabbix-agent2
```

### 11. Автоматизация развертывания

#### GitHub Actions для CD:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: hrapp
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /home/hrapp/hr-assistant
            git pull origin main
            docker-compose -f docker-compose.prod.yml down
            docker-compose -f docker-compose.prod.yml build
            docker-compose -f docker-compose.prod.yml up -d
            
            # Применение миграций
            docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
            
            # Проверка здоровья сервисов
            sleep 30
            curl -f http://localhost:8000/health || exit 1
            curl -f http://localhost:3000 || exit 1
```

#### Ansible плейбук:
```yaml
# deploy/ansible/playbook.yml
---
- hosts: hr-assistant
  become: yes
  vars:
    app_user: hrapp
    app_dir: /home/hrapp/hr-assistant
    
  tasks:
    - name: Update system packages
      apt:
        update_cache: yes
        upgrade: yes
        
    - name: Install required packages
      apt:
        name:
          - docker.io
          - docker-compose
          - nginx
          - certbot
          - python3-certbot-nginx
        state: present
        
    - name: Clone application repository
      git:
        repo: https://github.com/your-username/hr-assistant.git
        dest: "{{ app_dir }}"
        force: yes
      become_user: "{{ app_user }}"
      
    - name: Copy environment variables
      template:
        src: env.j2
        dest: "{{ app_dir }}/.env"
        owner: "{{ app_user }}"
        mode: '0600'
        
    - name: Start application services
      docker_compose:
        project_src: "{{ app_dir }}"
        files:
          - docker-compose.prod.yml
        state: present
      become_user: "{{ app_user }}"
```

### 12. Безопасность

#### Настройка firewall:
```bash
# UFW правила
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow from 10.0.0.0/8 to any port 5432  # PostgreSQL только для внутренней сети
ufw enable
```

#### Backup стратегия:
```bash
# Ежедневный backup базы данных
cat > /etc/cron.daily/backup-db << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/hr-assistant"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -h localhost -U hrapp hr_assistant | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Загрузка в Object Storage
s3cmd put $BACKUP_DIR/db_$DATE.sql.gz s3://hr-assistant-backups/db/

# Удаление старых локальных копий (>7 дней)
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /etc/cron.daily/backup-db
```

### 13. Масштабирование

#### Horizontal scaling с Load Balancer:
```bash
# Создание дополнительных серверов через Terraform
terraform apply -var="instance_count=3"

# Настройка Nginx upstream
upstream hr_backend {
    server 10.0.1.10:8000;
    server 10.0.1.11:8000;
    server 10.0.1.12:8000;
}

upstream hr_frontend {
    server 10.0.1.10:3000;
    server 10.0.1.11:3000;
    server 10.0.1.12:3000;
}
```

#### Managed Kubernetes (Yandex Cloud):
```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hr-assistant-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hr-assistant-backend
  template:
    metadata:
      labels:
        app: hr-assistant-backend
    spec:
      containers:
      - name: backend
        image: registry.hrassistant.ru/hr-assistant-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: hr-assistant-secrets
              key: database-url
```

## Стоимость эксплуатации

### Базовая конфигурация (до 1000 пользователей):
- **VPS**: 3,500₽/месяц (Selectel)
- **Домен**: 300₽/год
- **SSL**: бесплатно (Let's Encrypt)
- **Мониторинг**: 500₽/месяц (Zabbix Pro)
- **Резервное копирование**: 200₽/месяц (Object Storage)
- **OpenAI API**: ~$50/месяц при активном использовании

**Итого**: ~4,200₽/месяц + API затраты

### Масштабируемая конфигурация (до 10,000 пользователей):
- **Load Balancer**: 1,500₽/месяц
- **VPS x3**: 10,500₽/месяц
- **Managed PostgreSQL**: 8,000₽/месяц
- **Object Storage**: 1,000₽/месяц
- **CDN**: 2,000₽/месяц
- **Мониторинг**: 2,000₽/месяц

**Итого**: ~25,000₽/месяц + API затраты

Данная архитектура обеспечивает надежную, масштабируемую и безопасную работу HR Assistant в российской инфраструктуре с возможностью горизонтального масштабирования и интеграции с российскими сервисами.