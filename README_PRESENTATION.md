# 📊 HR Assistant - Marp Презентация

## 🎯 Описание

Создана интерактивная **Marp презентация** для HR Assistant с подробным описанием:
- 🏗️ Архитектуры системы
- 🚀 Развертывания на российских хостингах (Selectel, Yandex Cloud, VK Cloud)
- ⚙️ Инструкций по настройке и конфигурации
- 📊 Мониторинга и оптимизации
- 🔒 Безопасности и масштабирования

## 🛠️ Как просмотреть презентацию

### Вариант 1: Marp CLI (рекомендуется)

```bash
# Установка Marp CLI
npm install -g @marp-team/marp-cli

# Просмотр в браузере
marp HR_Assistant_Presentation.md --preview

# Экспорт в HTML
marp HR_Assistant_Presentation.md --html --output hr-assistant-presentation.html

# Экспорт в PDF
marp HR_Assistant_Presentation.md --pdf --output hr-assistant-presentation.pdf

# Экспорт в PowerPoint
marp HR_Assistant_Presentation.md --pptx --output hr-assistant-presentation.pptx
```

### Вариант 2: Marp для VS Code

1. Установите расширение "Marp for VS Code"
2. Откройте `HR_Assistant_Presentation.md`
3. Нажмите `Ctrl+Shift+P` → "Marp: Open Preview"

### Вариант 3: Онлайн редактор

1. Перейдите на https://web.marp.app/
2. Вставьте содержимое файла `HR_Assistant_Presentation.md`
3. Просматривайте презентацию в режиме реального времени

## 📝 Структура презентации

| Слайд | Тема | Описание |
|-------|------|----------|
| 1 | Титульная | Обзор HR Assistant |
| 2 | Обзор решения | Ключевые возможности |
| 3-5 | Архитектура | Технический стек и компоненты |
| 6-12 | Развертывание | Пошаговые инструкции для хостингов |
| 13-15 | Мониторинг | Логирование и метрики |
| 16-17 | Безопасность | Firewall, backup, рекомендации |
| 18-19 | Оптимизация | Настройки производительности |
| 20-21 | Масштабирование | Горизонтальное масштабирование |
| 22 | Troubleshooting | Диагностика проблем |
| 23 | Сравнение хостингов | Стоимость и особенности |
| 24-25 | Контакты | Поддержка и roadmap |

## 🎨 Настройки презентации

### Используемые стили
- **Тема**: Default
- **Размер**: 16:9 (широкоэкранный)
- **Пагинация**: Включена
- **Фон**: #f8f9fa (светло-серый)
- **Цвет текста**: #343a40 (темно-серый)

### Кастомные CSS классы
- `.columns` - Двухколоночная разметка
- `.highlight` - Выделенные блоки с градиентом
- `.tech-stack` - Теги технологий

## 🚀 Развертывание презентации

### Статический хостинг

```bash
# Генерация HTML файла
marp HR_Assistant_Presentation.md --html --output index.html

# Деплой на GitHub Pages
git add index.html
git commit -m "Add HR Assistant presentation"
git push origin main

# Включите GitHub Pages в настройках репозитория
```

### Docker контейнер

```dockerfile
# Dockerfile для презентации
FROM node:18-alpine
RUN npm install -g @marp-team/marp-cli
WORKDIR /app
COPY HR_Assistant_Presentation.md .
EXPOSE 8080
CMD ["marp", "HR_Assistant_Presentation.md", "--preview", "--port", "8080", "--host", "0.0.0.0"]
```

```bash
# Сборка и запуск
docker build -t hr-assistant-presentation .
docker run -p 8080:8080 hr-assistant-presentation
```

## 📱 Адаптивность

Презентация оптимизирована для:
- 💻 **Десктоп** (1920x1080, 1366x768)
- 📱 **Планшет** (768x1024)
- 📟 **Проектор** (4:3, 16:9, 16:10)

## 🔧 Кастомизация

### Изменение темы
```yaml
---
theme: gaia  # или uncover, gaia, default
---
```

### Добавление собственных стилей
```yaml
style: |
  .custom-class {
    background: #your-color;
    padding: 1rem;
  }
```

### Интеграция с брендингом
- Замените `https://via.placeholder.com/` на реальные изображения
- Обновите контактную информацию
- Добавьте логотипы компаний

## 📊 Метрики использования

Рекомендуется отслеживать:
- Время просмотра слайдов
- Конверсию в GitHub stars
- Обращения в поддержку
- Использование развертывания

## 🔄 Обновления

Для обновления презентации:
1. Отредактируйте `HR_Assistant_Presentation.md`
2. Регенерируйте HTML/PDF: `marp HR_Assistant_Presentation.md --html`
3. Деплойте обновленную версию

## 📞 Поддержка

По вопросам презентации:
- 📧 Email: presentation@hrassistant.ru
- 🐙 GitHub Issues: https://github.com/your-username/hr-assistant/issues
- 📱 Telegram: @hrassistantbot

---

*Презентация создана с использованием Marp - Markdown Presentation Ecosystem*