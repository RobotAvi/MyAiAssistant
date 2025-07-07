.PHONY: help install dev dev-backend dev-frontend docker-up docker-down clean test

help:
	@echo "HR Assistant - Команды для разработки"
	@echo ""
	@echo "install      - Установить зависимости"
	@echo "dev          - Запустить для разработки (без Docker)"
	@echo "dev-backend  - Запустить только backend"
	@echo "dev-frontend - Запустить только frontend"
	@echo "docker-up    - Запустить с Docker Compose"
	@echo "docker-down  - Остановить Docker контейнеры"
	@echo "clean        - Очистить временные файлы"
	@echo "test         - Запустить тесты"

install:
	@echo "Установка зависимостей..."
	pip install -r requirements.txt
	npm install

dev-backend:
	@echo "Запуск backend сервера..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "Запуск frontend сервера..."
	npm run dev

dev:
	@echo "Запуск full-stack приложения..."
	@echo "Убедитесь, что PostgreSQL и Redis запущены локально"
	make -j2 dev-backend dev-frontend

docker-up:
	@echo "Запуск с Docker Compose..."
	docker-compose up --build

docker-down:
	@echo "Остановка Docker контейнеров..."
	docker-compose down

clean:
	@echo "Очистка временных файлов..."
	rm -rf __pycache__/
	rm -rf app/__pycache__/
	rm -rf app/*/__pycache__/
	rm -rf app/*/*/__pycache__/
	rm -rf .next/
	rm -rf node_modules/.cache/
	rm -rf uploads/resumes/*

test:
	@echo "Запуск тестов..."
	python -m pytest tests/ -v

setup-env:
	@echo "Настройка переменных окружения..."
	cp .env.example .env
	cp .env.local.example .env.local
	@echo "Отредактируйте файлы .env и .env.local с вашими настройками"

init-db:
	@echo "Инициализация базы данных..."
	alembic upgrade head

celery-worker:
	@echo "Запуск Celery worker..."
	celery -A app.services.scheduler worker --loglevel=info

celery-beat:
	@echo "Запуск Celery beat scheduler..."
	celery -A app.services.scheduler beat --loglevel=info