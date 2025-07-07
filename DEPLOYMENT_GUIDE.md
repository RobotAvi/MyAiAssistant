# Пошаговое руководство по развертыванию HR Assistant

## Подготовка к развертыванию

### Что понадобится:
- 📧 Email для настройки (Gmail или Yandex.Mail)
- 🤖 Telegram аккаунт для создания бота
- 💳 Банковская карта для оплаты хостинга
- 🔑 OpenAI API ключ ($18 депозит минимум)
- ⏰ 2-3 часа времени на настройку

## Шаг 1: Регистрация внешних сервисов

### 1.1 OpenAI API

```bash
# 1. Перейдите на https://platform.openai.com/
# 2. Зарегистрируйтесь или войдите
# 3. Добавьте $18+ на баланс (API Keys -> Billing)
# 4. Создайте API ключ (API Keys -> Create new secret key)
# Сохраните ключ: sk-...
```

### 1.2 Telegram Bot

```bash
# 1. Найдите @BotFather в Telegram
# 2. Отправьте команду: /newbot
# 3. Введите название: HR Assistant Bot
# 4. Введите username: your_hr_assistant_bot
# 5. Сохраните токен: 123456789:AAEhBOweik6ad9r_SmeN8owfY-MfqhqeEE

# Получите ваш Chat ID:
# 1. Найдите @userinfobot в Telegram
# 2. Отправьте команду: /start
# 3. Сохраните ваш ID: 123456789
```

### 1.3 HeadHunter API (опционально)

```bash
# 1. Перейдите на https://dev.hh.ru/
# 2. Зарегистрируйте приложение
# 3. Получите Client ID и Client Secret
# 4. Настройте Redirect URI: https://hrassistant.ru/auth/hh/callback
```

## Шаг 2: Выбор и заказ хостинга

### Вариант А: Selectel (Рекомендуемый)

#### Регистрация и заказ сервера:
```bash
# 1. Перейдите на https://selectel.ru/
# 2. Зарегистрируйтесь и пройдите верификацию
# 3. Пополните баланс на 5,000₽
# 4. В панели управления: Облачная платформа -> Серверы

# Конфигурация сервера:
Название: hr-assistant-prod
Образ: Ubuntu 22.04 LTS
Тариф: SSD-3 (4 CPU, 8GB RAM, 80GB SSD)
Сеть: Создать новую
Firewall: Стандартный (SSH, HTTP, HTTPS)
SSH ключ: Добавить публичный ключ

# Стоимость: ~3,500₽/месяц
```

#### Получение IP и подключение:
```bash
# После создания сервера получите:
SERVER_IP=185.22.153.45  # Ваш IP будет другой

# Подключение к серверу:
ssh root@$SERVER_IP

# При первом подключении ответьте: yes
```

### Вариант Б: Timeweb Cloud

```bash
# 1. Перейдите на https://timeweb.cloud/
# 2. Зарегистрируйтесь (быстрая регистрация через Telegram)
# 3. Пополните баланс на 3,000₽

# Создание сервера:
# Облачные серверы -> Создать сервер
Операционная система: Ubuntu 22.04
Конфигурация: Cloud VPS S4 (4 CPU, 8GB RAM, 160GB SSD)
Дополнительные IP: Не нужно
SSH ключи: Добавить ваш публичный ключ

# Стоимость: ~2,800₽/месяц
```

### Вариант В: VK Cloud

```bash
# 1. Перейдите на https://cloud.vk.com/
# 2. Зарегистрируйтесь через VK ID
# 3. Пройдите верификацию (загрузите паспорт)

# Создание инстанса:
# Облачные вычисления -> Создать инстанс
Название: hr-assistant
Операционная система: Ubuntu 22.04
Конфигурация: Стандарт S2 (4 CPU, 8GB RAM, 80GB SSD)
Сеть: Создать новую
Floating IP: Да

# Стоимость: ~3,000₽/месяц
```

## Шаг 3: Регистрация домена

### REG.RU (Рекомендуемый регистратор)

```bash
# 1. Перейдите на https://www.reg.ru/
# 2. Найдите свободное доменное имя:
hrassistant.ru
myhrbot.ru
jobassistant.ru

# 3. Добавьте в корзину и оплатите (~300₽/год)
# 4. В панели управления доменом настройте DNS:

# A записи:
@               → 185.22.153.45  # IP вашего сервера
www             → 185.22.153.45
api             → 185.22.153.45

# Время применения: 15-30 минут
```

### Альтернатива - Яндекс.Домены

```bash
# 1. Перейдите на https://domain.yandex.ru/
# 2. Найдите домен (~199₽/год для .ru)
# 3. Оплатите и настройте DNS аналогично выше
```

## Шаг 4: Базовая настройка сервера

### Подключение и первоначальная настройка:

```bash
# Подключение к серверу
ssh root@YOUR_SERVER_IP

# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y nginx postgresql postgresql-contrib redis-server \
               docker.io docker-compose git curl wget unzip \
               certbot python3-certbot-nginx htop

# Запуск служб
systemctl enable nginx postgresql redis-server docker
systemctl start nginx postgresql redis-server docker

# Настройка Firewall
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw --force enable

# Создание пользователя для приложения
adduser hrapp
usermod -aG docker hrapp
usermod -aG sudo hrapp

# Настройка SSH для hrapp
mkdir -p /home/hrapp/.ssh
cp ~/.ssh/authorized_keys /home/hrapp/.ssh/
chown -R hrapp:hrapp /home/hrapp/.ssh
chmod 700 /home/hrapp/.ssh
chmod 600 /home/hrapp/.ssh/authorized_keys
```

## Шаг 5: Настройка SSL сертификатов

```bash
# Убедитесь, что домен уже указывает на ваш сервер
nslookup hrassistant.ru

# Если домен настроен правильно, получите SSL сертификат:
certbot --nginx -d hrassistant.ru -d www.hrassistant.ru -d api.hrassistant.ru

# Введите email для уведомлений
# Согласитесь с условиями: Y
# Не разрешайте передачу email EFF: N

# Проверьте автоматическое обновление:
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

## Шаг 6: Настройка PostgreSQL

```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# Создание базы данных и пользователя
CREATE DATABASE hr_assistant;
CREATE USER hrapp WITH PASSWORD 'YOUR_SECURE_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON DATABASE hr_assistant TO hrapp;
\q

# Настройка подключений
echo "host hr_assistant hrapp 127.0.0.1/32 md5" >> /etc/postgresql/14/main/pg_hba.conf

# Перезапуск PostgreSQL
systemctl restart postgresql

# Проверка подключения
sudo -u hrapp psql -h localhost -d hr_assistant -c "SELECT version();"
```

## Шаг 7: Клонирование и настройка приложения

```bash
# Переключение на пользователя hrapp
su - hrapp

# Клонирование репозитория
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant

# Создание production .env файла
cp .env.example .env

# Редактирование конфигурации
nano .env
```

### Заполните .env файл:

```bash
# Database
DATABASE_URL=postgresql://hrapp:YOUR_SECURE_PASSWORD_HERE@localhost:5432/hr_assistant

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Telegram
TELEGRAM_BOT_TOKEN=123456789:AAEhBOweik6ad9r_SmeN8owfY-MfqhqeEE
TELEGRAM_CHAT_ID=123456789

# Email (для Gmail App Password)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your.email@gmail.com
EMAIL_PASSWORD=your-app-password

# Security
SECRET_KEY=generate-long-random-string-here-with-64-characters-minimum
DEBUG=False

# URLs
FRONTEND_URL=https://hrassistant.ru
TELEGRAM_WEBHOOK_URL=https://api.hrassistant.ru/api/telegram/webhook

# HeadHunter (опционально)
HH_API_KEY=your-hh-api-key-if-you-have
```

## Шаг 8: Создание production Docker Compose

```bash
# Создание production конфигурации
cat > docker-compose.prod.yml << 'EOF'
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
      - ./uploads:/app/uploads
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
      - ./uploads:/app/uploads
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
    networks:
      - hr-network

volumes:
  uploads:

networks:
  hr-network:
    driver: bridge
EOF

# Создание директории для загрузок
mkdir -p uploads/resumes
```

## Шаг 9: Настройка Nginx

```bash
# Возвращение к root пользователю
exit

# Создание конфигурации Nginx
cat > /etc/nginx/sites-available/hr-assistant << 'EOF'
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
        alias /home/hrapp/hr-assistant/uploads/;
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
EOF

# Активация конфигурации
ln -s /etc/nginx/sites-available/hr-assistant /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Проверка конфигурации
nginx -t

# Перезапуск Nginx
systemctl restart nginx
```

## Шаг 10: Запуск приложения

```bash
# Возврат к пользователю hrapp
su - hrapp
cd hr-assistant

# Сборка и запуск контейнеров
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Ожидайте появления строк:
# hr-frontend  | ✓ Ready in 2.3s
# hr-backend   | INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Шаг 11: Настройка Telegram webhook

```bash
# Настройка webhook для Telegram бота
curl -X POST https://api.hrassistant.ru/api/telegram/setup-webhook

# Проверка настройки
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo
```

## Шаг 12: Первоначальная проверка

### Проверка работоспособности:

```bash
# Проверка frontend
curl -I https://hrassistant.ru
# Ожидаемый ответ: HTTP/2 200

# Проверка API
curl https://api.hrassistant.ru/health
# Ожидаемый ответ: {"status":"healthy"}

# Проверка API документации
# Откройте в браузере: https://api.hrassistant.ru/docs
```

### Проверка Telegram бота:

```bash
# 1. Найдите вашего бота в Telegram
# 2. Отправьте команду: /start
# 3. Должно прийти приветственное сообщение
```

## Шаг 13: Настройка мониторинга

### Простой мониторинг с помощью cron:

```bash
# Возврат к root
exit

# Создание скрипта проверки
cat > /usr/local/bin/check-hr-assistant << 'EOF'
#!/bin/bash

# Проверка frontend
if ! curl -sf https://hrassistant.ru > /dev/null; then
    echo "Frontend недоступен!" | mail -s "HR Assistant Alert" admin@hrassistant.ru
    systemctl restart nginx
fi

# Проверка backend
if ! curl -sf https://api.hrassistant.ru/health > /dev/null; then
    echo "Backend недоступен!" | mail -s "HR Assistant Alert" admin@hrassistant.ru
    cd /home/hrapp/hr-assistant
    docker-compose -f docker-compose.prod.yml restart backend
fi

# Проверка дискового пространства
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    echo "Диск заполнен на $DISK_USAGE%!" | mail -s "HR Assistant Disk Alert" admin@hrassistant.ru
fi
EOF

chmod +x /usr/local/bin/check-hr-assistant

# Добавление в cron (проверка каждые 5 минут)
echo "*/5 * * * * /usr/local/bin/check-hr-assistant" | crontab -
```

## Шаг 14: Настройка backup

```bash
# Создание скрипта резервного копирования
cat > /usr/local/bin/backup-hr-assistant << 'EOF'
#!/bin/bash

BACKUP_DIR="/var/backups/hr-assistant"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup базы данных
sudo -u hrapp pg_dump -h localhost hr_assistant | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup файлов загрузок
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C /home/hrapp/hr-assistant uploads/

# Backup конфигурации
cp /home/hrapp/hr-assistant/.env $BACKUP_DIR/env_$DATE.backup

# Удаление старых бэкапов (>7 дней)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.backup" -mtime +7 -delete

echo "Backup завершен: $BACKUP_DIR"
EOF

chmod +x /usr/local/bin/backup-hr-assistant

# Ежедневный backup в 3:00
echo "0 3 * * * /usr/local/bin/backup-hr-assistant" | crontab -
```

## Шаг 15: Первый запуск и тестирование

### 1. Откройте сайт в браузере:
```
https://hrassistant.ru
```

### 2. Создайте первого пользователя:
- Заполните форму регистрации
- Укажите ваш email и Telegram Chat ID

### 3. Загрузите тестовое резюме:
- Используйте реальное резюме в формате PDF
- Дождитесь обработки (1-2 минуты)

### 4. Протестируйте поиск вакансий:
- Нажмите "Найти вакансии"
- Система должна найти релевантные предложения

### 5. Проверьте Telegram уведомления:
- В боте должно прийти сообщение с вакансиями
- Попробуйте выбрать несколько позиций

## Устранение неполадок

### Frontend не загружается:
```bash
# Проверка логов
docker logs hr-frontend

# Перезапуск
docker restart hr-frontend
```

### Backend возвращает 500 ошибку:
```bash
# Проверка логов
docker logs hr-backend

# Проверка подключения к БД
docker exec hr-backend python -c "from app.db.database import engine; print(engine.execute('SELECT 1').scalar())"
```

### Telegram webhook не работает:
```bash
# Проверка webhook
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo

# Переустановка webhook
curl -X POST https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook \
  -d "url=https://api.hrassistant.ru/api/telegram/webhook"
```

### OpenAI API ошибки:
```bash
# Проверка баланса
curl https://api.openai.com/v1/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Проверка в логах backend
docker logs hr-backend | grep -i openai
```

## Готово! 🎉

Ваш HR Assistant готов к работе. Система будет:

1. **Каждое утро в 9:00** искать новые вакансии
2. **Отправлять уведомления** в Telegram с лучшими совпадениями
3. **Автоматически подавать заявки** на выбранные позиции
4. **Уведомлять о результатах** и вести статистику

### Полезные команды для управления:

```bash
# Просмотр статуса всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Обновление приложения
git pull origin main
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Backup базы данных вручную
/usr/local/bin/backup-hr-assistant
```

### Поддержка:
- 📧 Email: support@hrassistant.ru
- 💬 Telegram: @hrassistantbot
- 🐛 Issues: GitHub репозиторий