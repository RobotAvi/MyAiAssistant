# Российские альтернативы и интеграции для HR Assistant

## Обзор

Данный документ описывает альтернативные российские сервисы и настройки для случаев, когда международные провайдеры недоступны или нежелательны для использования.

## AI и LLM сервисы

### 1. YandexGPT (Рекомендуемый)

**Описание**: Российская языковая модель от Яндекса
**Ссылка**: https://cloud.yandex.ru/services/yandexgpt
**Стоимость**: От 1₽ за 1000 токенов

#### Настройка YandexGPT:

```python
# app/services/llm_service_yandex.py
import requests
import json
from typing import Dict, Any
from app.core.config import settings

class YandexLLMService:
    def __init__(self):
        self.api_key = settings.yandex_api_key
        self.folder_id = settings.yandex_folder_id
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1"
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Анализ резюме с помощью YandexGPT"""
        
        prompt = f"""
        Проанализируй следующее резюме и извлеки ключевую информацию в формате JSON:

        Резюме:
        {resume_text}

        Верни JSON с полями:
        - skills: список навыков (массив строк)
        - experience_years: количество лет опыта (число)
        - position_title: желаемая должность (строка)
        - location: местоположение (строка)
        - salary_expectation: ожидаемая зарплата (строка)

        Отвечай только JSON без дополнительного текста.
        """
        
        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 500
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты эксперт по анализу резюме. Анализируй резюме и возвращай структурированные данные в JSON формате."
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/completion",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["result"]["alternatives"][0]["message"]["text"]
                return json.loads(content)
            else:
                raise Exception(f"YandexGPT API error: {response.status_code}")
                
        except Exception as e:
            print(f"Ошибка анализа резюме с YandexGPT: {e}")
            return {
                "skills": [],
                "experience_years": 0,
                "position_title": "",
                "location": "",
                "salary_expectation": ""
            }
    
    async def generate_cover_letter(self, resume_text: str, job_description: str, company_name: str) -> str:
        """Генерация сопроводительного письма"""
        
        prompt = f"""
        Напиши персонализированное сопроводительное письмо для соискателя работы.

        Информация о кандидате (из резюме):
        {resume_text[:1500]}

        Описание вакансии:
        {job_description[:1500]}

        Название компании: {company_name}

        Требования к письму:
        - Длина: 150-250 слов
        - Профессиональный тон
        - Подчеркни соответствие навыков требованиям
        - Покажи интерес к компании
        - Пиши на русском языке

        Верни только текст письма.
        """
        
        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 400
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты эксперт по написанию сопроводительных писем для поиска работы."
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/completion",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["result"]["alternatives"][0]["message"]["text"]
            else:
                raise Exception(f"YandexGPT API error: {response.status_code}")
                
        except Exception as e:
            print(f"Ошибка генерации письма с YandexGPT: {e}")
            return f"Здравствуйте!\n\nЯ заинтересован в вакансии в компании {company_name}. Мой опыт и навыки соответствуют требованиям позиции.\n\nС уважением"
```

#### Конфигурация .env для YandexGPT:

```bash
# YandexGPT
YANDEX_API_KEY=your-yandex-api-key
YANDEX_FOLDER_ID=your-folder-id

# Переключение на YandexGPT
USE_YANDEX_LLM=true
```

### 2. GigaChat (Сбер)

**Описание**: Российская языковая модель от Сбера
**Ссылка**: https://developers.sber.ru/portal/products/gigachat
**Стоимость**: Бесплатная версия доступна

#### Настройка GigaChat:

```python
# app/services/llm_service_gigachat.py
import requests
import json
import uuid
from typing import Dict, Any
from app.core.config import settings

class GigaChatService:
    def __init__(self):
        self.client_id = settings.gigachat_client_id
        self.client_secret = settings.gigachat_client_secret
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
    
    async def get_access_token(self):
        """Получение токена доступа"""
        
        auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self.client_secret}"
        }
        
        payload = {
            "scope": "GIGACHAT_API_PERS"
        }
        
        response = requests.post(auth_url, headers=headers, data=payload, verify=False)
        
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
        else:
            raise Exception(f"GigaChat auth error: {response.status_code}")
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Анализ резюме с помощью GigaChat"""
        
        if not self.access_token:
            await self.get_access_token()
        
        prompt = f"""
        Проанализируй резюме и извлеки ключевую информацию в JSON формате:
        
        {resume_text}
        
        Верни JSON с полями: skills, experience_years, position_title, location, salary_expectation
        """
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        payload = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                raise Exception(f"GigaChat API error: {response.status_code}")
                
        except Exception as e:
            print(f"Ошибка анализа резюме с GigaChat: {e}")
            return {
                "skills": [],
                "experience_years": 0,
                "position_title": "",
                "location": "",
                "salary_expectation": ""
            }
```

### 3. Локальные LLM модели

Для полной независимости можно развернуть локальные модели:

#### Установка Ollama с русскими моделями:

```bash
# Установка Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Загрузка русской модели
ollama pull saiga/mistral-7b-instruct-v0.2

# Запуск API сервера
ollama serve
```

#### Интеграция с Ollama:

```python
# app/services/llm_service_local.py
import requests
import json
from typing import Dict, Any

class LocalLLMService:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "saiga/mistral-7b-instruct-v0.2"
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Анализ резюме с локальной моделью"""
        
        prompt = f"""
        Проанализируй резюме и извлеки информацию в JSON:
        
        {resume_text}
        
        Верни JSON с полями: skills, experience_years, position_title, location, salary_expectation
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 500
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["response"]
                return json.loads(content)
            else:
                raise Exception(f"Local LLM error: {response.status_code}")
                
        except Exception as e:
            print(f"Ошибка локальной LLM: {e}")
            return {
                "skills": [],
                "experience_years": 0,
                "position_title": "",
                "location": "",
                "salary_expectation": ""
            }
```

## Email сервисы

### 1. Yandex.Mail для домена

**Описание**: Корпоративная почта от Яндекса
**Ссылка**: https://connect.yandex.ru/
**Стоимость**: 200₽/месяц за почтовый ящик

#### Настройка Yandex.Mail:

```bash
# .env конфигурация
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=587
EMAIL_USER=noreply@hrassistant.ru
EMAIL_PASSWORD=your-yandex-app-password

# Альтернативно для личной почты Yandex
EMAIL_USER=your-email@yandex.ru
```

### 2. Mail.ru для бизнеса

**Описание**: Корпоративная почта от Mail.ru
**Ссылка**: https://biz.mail.ru/
**Стоимость**: 150₽/месяц за почтовый ящик

```bash
# .env конфигурация для Mail.ru
SMTP_SERVER=smtp.mail.ru
SMTP_PORT=587
EMAIL_USER=noreply@hrassistant.ru
EMAIL_PASSWORD=your-mailru-app-password
```

### 3. REG.RU почта

**Описание**: Почтовые услуги от регистратора доменов
**Ссылка**: https://www.reg.ru/hosting/mail/
**Стоимость**: 100₽/месяц за почтовый ящик

```bash
# .env конфигурация для REG.RU
SMTP_SERVER=mail.hosting.reg.ru
SMTP_PORT=587
EMAIL_USER=noreply@hrassistant.ru
EMAIL_PASSWORD=your-regru-password
```

## Файловые хранилища

### 1. Yandex Object Storage

**Описание**: S3-совместимое хранилище от Яндекса
**Ссылка**: https://cloud.yandex.ru/services/storage
**Стоимость**: 1.53₽/ГБ в месяц

#### Настройка Object Storage:

```bash
# Создание сервисного аккаунта
yc iam service-account create --name hr-assistant-storage

# Назначение роли
yc resource-manager folder add-access-binding $FOLDER_ID \
  --role storage.editor \
  --service-account-name hr-assistant-storage

# Создание ключей доступа
yc iam access-key create --service-account-name hr-assistant-storage

# Создание бакета
yc storage bucket create --name hr-assistant-files
```

```python
# app/services/storage_service.py
import boto3
from botocore.config import Config
from app.core.config import settings

class YandexStorageService:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=settings.yandex_access_key,
            aws_secret_access_key=settings.yandex_secret_key,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = settings.yandex_bucket_name
    
    async def upload_file(self, file_path: str, object_name: str) -> str:
        """Загрузка файла в Object Storage"""
        
        try:
            self.client.upload_file(file_path, self.bucket_name, object_name)
            return f"https://storage.yandexcloud.net/{self.bucket_name}/{object_name}"
        except Exception as e:
            print(f"Ошибка загрузки в Yandex Storage: {e}")
            return None
```

### 2. VK Cloud Solutions (MCS)

**Описание**: Облачное хранилище от VK
**Ссылка**: https://mcs.mail.ru/storage/
**Стоимость**: 1.90₽/ГБ в месяц

### 3. Selectel Object Storage

**Описание**: S3-совместимое хранилище от Selectel
**Ссылка**: https://selectel.ru/services/cloud/storage/
**Стоимость**: 1.69₽/ГБ в месяц

## Мониторинг и аналитика

### 1. Yandex Monitoring

**Описание**: Система мониторинга от Яндекса
**Ссылка**: https://cloud.yandex.ru/services/monitoring
**Стоимость**: Бесплатно до 50 метрик

#### Настройка мониторинга:

```bash
# Установка агента
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Создание конфига мониторинга
cat > /etc/yandex-monitoring/config.yaml << EOF
service:
  enabled: true
  name: hr-assistant
  
metrics:
  - name: cpu_usage
    type: gauge
    command: "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    
  - name: memory_usage
    type: gauge
    command: "free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'"
    
  - name: disk_usage
    type: gauge
    command: "df / | tail -1 | awk '{printf \"%.2f\", $3/$2 * 100.0}'"
EOF
```

### 2. Zabbix (Российская поддержка)

**Описание**: Система мониторинга с российской поддержкой
**Ссылка**: https://www.zabbix.com/ru/
**Стоимость**: Open source / коммерческая поддержка

### 3. Графана + Prometheus

**Описание**: Open source решение для мониторинга
**Установка на российских серверах**:

```bash
# Установка Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
sudo mv prometheus-*/prometheus /usr/local/bin/
sudo mv prometheus-*/promtool /usr/local/bin/

# Установка Grafana
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install grafana
```

## CDN и ускорение

### 1. Yandex CDN

**Описание**: CDN от Яндекса
**Ссылка**: https://cloud.yandex.ru/services/cdn
**Стоимость**: 0.85₽/ГБ трафика

### 2. Selectel CDN

**Описание**: CDN от Selectel
**Ссылка**: https://selectel.ru/services/additional/cdn/
**Стоимость**: 0.90₽/ГБ трафика

### 3. VK Cloud CDN

**Описание**: CDN от VK Cloud
**Ссылка**: https://mcs.mail.ru/cdn/
**Стоимость**: 1.20₽/ГБ трафика

## Настройка прокси для международных API

Для случаев, когда нужен доступ к международным сервисам:

### 1. Nginx как прокси

```nginx
# /etc/nginx/sites-available/api-proxy
server {
    listen 8080;
    server_name localhost;
    
    location /openai/ {
        proxy_pass https://api.openai.com/;
        proxy_set_header Host api.openai.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_ssl_server_name on;
    }
    
    location /telegram/ {
        proxy_pass https://api.telegram.org/;
        proxy_set_header Host api.telegram.org;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_ssl_server_name on;
    }
}
```

### 2. Использование VPN на сервере

```bash
# Установка WireGuard
apt install wireguard

# Конфигурация VPN
cat > /etc/wireguard/wg0.conf << EOF
[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = VPN_SERVER_PUBLIC_KEY
Endpoint = vpn.server.com:51820
AllowedIPs = 0.0.0.0/0
EOF

# Запуск VPN
wg-quick up wg0
```

## Полная российская конфигурация

### .env файл для полностью российской настройки:

```bash
# Database (локальная или Yandex Managed PostgreSQL)
DATABASE_URL=postgresql://hrapp:password@localhost:5432/hr_assistant

# Redis (локальный или Yandex Managed Redis)
REDIS_URL=redis://localhost:6379

# LLM Service
USE_YANDEX_LLM=true
YANDEX_API_KEY=your-yandex-api-key
YANDEX_FOLDER_ID=your-folder-id

# Telegram (через российские прокси если нужно)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_API_URL=http://localhost:8080/telegram/bot

# Email (Yandex.Mail)
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=587
EMAIL_USER=noreply@hrassistant.ru
EMAIL_PASSWORD=your-yandex-app-password

# File Storage (Yandex Object Storage)
USE_YANDEX_STORAGE=true
YANDEX_ACCESS_KEY=your-access-key
YANDEX_SECRET_KEY=your-secret-key
YANDEX_BUCKET_NAME=hr-assistant-files

# HeadHunter API (российский сервис)
HH_API_KEY=your-hh-api-key

# Security
SECRET_KEY=your-secret-key
DEBUG=False

# URLs
FRONTEND_URL=https://hrassistant.ru
```

### Docker Compose с российскими сервисами:

```yaml
# docker-compose.russian.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.hrassistant.ru/api
      - NEXT_PUBLIC_USE_RUSSIAN_SERVICES=true
    ports:
      - "3000:3000"

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - USE_YANDEX_LLM=true
      - USE_YANDEX_STORAGE=true
    env_file:
      - .env
    ports:
      - "8000:8000"

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: ["serve"]

volumes:
  ollama_data:
```

Данная конфигурация обеспечивает полную работоспособность HR Assistant с использованием только российских сервисов и инфраструктуры.