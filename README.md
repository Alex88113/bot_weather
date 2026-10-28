<div align="center">

# 🌤️ Weather Bot — Погода в Севастополе

**Telegram-бот на aiogram 3.x с асинхронным парсингом погоды и кэшированием в Redis**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-async-0A0A0A?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-43B02A?style=for-the-badge)
![loguru](https://img.shields.io/badge/loguru-logging-8A2BE2?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

**Статус: ✅ Бот работает и отвечает на команды**

</div>

---

## 📑 Содержание

| Основное | Детали |
|:---------|:-------|
| [📖 О проекте](#-о-проекте) | [🐳 Инфраструктура](#-инфраструктура) |
| [🚀 Возможности](#-возможности) | [🧪 Тестирование](#-тестирование) |
| [🛠 Стек технологий](#-стек-технологий) | [📝 Логирование](#-логирование) |
| [📁 Структура проекта](#-структура-проекта) | [🔮 Ограничения и улучшения](#-ограничения-и-улучшения) |
| [⚙️ Установка и запуск](#️-установка-и-запуск) | |

---

## 📖 О проекте

**Weather Bot** — Telegram-бот, который по команде `/weather` парсит сайт `pogodaiklimat.ru`, извлекает текущую погоду в Севастополе и отправляет её пользователю в удобном формате.

### 🎯 Цель

Продемонстрировать навыки асинхронной разработки: работа с внешним API через `httpx`, парсинг HTML через `BeautifulSoup`, кэширование в Redis, логирование через `loguru` и обработка сетевых исключений.

### 📊 Характеристики

| Параметр | Значение |
|----------|----------|
| Тип | Telegram-бот |
| Язык | Python 3.13 |
| Фреймворк | aiogram 3.x |
| Источник данных | pogodaiklimat.ru (HTML-парсинг) |
| Кэш | Redis (TTL) |
| Логирование | loguru (JSON + текст) |
| Статус | ✅ Работает |

---

## 🚀 Возможности

- ✅ Команда `/start` — приветствие и краткая инструкция.
- ✅ Команда `/help` — список доступных команд.
- ✅ Команда `/weather` — текущая погода в Севастополе.
- ✅ Асинхронный HTTP-клиент (`httpx.AsyncClient`) с обработкой ошибок.
- ✅ Кэширование ответов API в Redis (с TTL), чтобы не дёргать сайт лишний раз.
- ✅ Логирование через `loguru` с разделением на уровни (`app.log`, `error.log`, `debug.log`, `critical_error.log`).
- ✅ Обработка сетевых исключений (`ConnectError`, `TimeoutException`, `HTTPStatusError`).
- ✅ Парсинг HTML через `BeautifulSoup` с извлечением температуры, влажности, ветра и облачности.

---

## 🛠 Стек технологий

| Технология | Роль |
|:-----------|:-----|
| **Python 3.13** | Язык разработки |
| **aiogram 3.x** | Асинхронный фреймворк для Telegram-ботов |
| **httpx** | Асинхронный HTTP-клиент |
| **BeautifulSoup 4** | Парсинг HTML |
| **Redis (redis.asyncio)** | Кэширование ответов API |
| **loguru** | Логирование |
| **pytest / pytest-asyncio** | Тестирование |
| **respx** | Мокирование HTTP-запросов |
| **uv** | Управление зависимостями |

---

## 📁 Структура проекта

```
bot_weather/
│
├── 📂 app/
│   ├── 📂 bot/
│   │   ├── 📂 configs/              # Настройки бота
│   │   │   └── bot_config.py
│   │   ├── 📂 handlers/             # Обработчики команд
│   │   │   └── commands.py          # /start, /help, /weather
│   │   ├── 📂 services/             # Бизнес-логика
│   │   │   ├── exceptions.py        # Кастомные исключения
│   │   │   ├── redis_service.py     # Работа с Redis
│   │   │   └── weather_service.py   # Парсинг погоды
│   │   ├── 📂 utils/
│   │   │   └── logger/              # Настройка loguru
│   │   ├── 📂 logs/                 # Логи бота
│   │   └── main.py                  # Точка входа бота
│   │
│   ├── 📂 logs/                     # Логи приложения
│   └── __init__.py
│
├── 📂 tests/
│   └── 📂 test_services/
│       ├── 📂 test_mock/
│       │   └── test_mock_weather_api.py
│       ├── test_networks_exceptions.py
│       └── test_weather_service.py
│
├── 📂 logs/                         # Корневые логи
│
├── 📄 Dockerfile                    # Сборка образа (планируется)
├── 📄 README.md
├── 📄 pyproject.toml                # Метаданные проекта
├── 📄 requirements.txt              # Зависимости
├── 📄 requirements-dev.txt          # Dev-зависимости
├── 📄 requirements-testing.txt      # Test-зависимости
├── 📄 run.py                        # Точка входа
├── 📄 systemd_service.service       # Юнит для systemd
└── 📄 uv.lock                       # Lock-файл uv
⚙️ Установка и запуск
✅ Требования
☑ Python 3.13

☑ Redis (локально или в Docker)

☑ Токен Telegram-бота (от @BotFather)

1. Клонировать репозиторий
git clone https://github.com/Alex88113/bot_weather.git
cd bot_weather
2. Установить зависимости
uv sync
Или через pip:
pip install -r requirements.txt
3. Настроить .env
Создай .env в корне проекта:

env
# Telegram
BOT_TOKEN=your_bot_token_here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API погоды
WEATHER_URL=https://pogodaiklimat.ru/weather.php?id=33991

4. Запустить Redis
docker run -d -p 6379:6379 --name redis redis:alpine

5. Запустить бота
python run.py
Или через systemd (юнит уже есть в systemd_service.service):

sudo systemctl start weather-bot
sudo systemctl status weather-bot
🐳 Инфраструктура
На данный момент Docker и CI/CD для бота не настроены — это следующий шаг. Сейчас бот запускается локально или через systemd на сервере.

Что планируется:

Dockerfile (multi-stage, non-root пользователь).

docker-compose.yaml с сервисами bot и redis.

GitHub Actions: тесты → сборка образа → пуш в Docker Hub.

HEALTHCHECK для проверки живости бота.

🧪 Тестирование
bash
# Установить зависимости для тестов
pip install -r requirements-testing.txt

# Запустить тесты
pytest tests/ -v
Что покрыто тестами:

Файл	Что тестируется
test_networks_exceptions.py	Обработка ConnectError, TimeoutException, HTTPStatusError в APIClient.send_request
test_mock_weather_api.py	Мокирование ответов API через respx
test_weather_service.py	Парсинг HTML и форматирование данных
Структура тестов:

text
tests/
└── test_services/
    ├── test_mock/
    │   └── test_mock_weather_api.py
    ├── test_networks_exceptions.py
    └── test_weather_service.py
📝 Логирование
Логи пишутся в logs/ (корень) и app/logs/ (внутри приложения). Используется loguru с разделением на уровни:

Файл	Что пишется
app.log	Все сообщения уровня INFO и выше
error.log	Только ERROR
debug.log	Только DEBUG
critical_error.log	Только CRITICAL
Формат — JSON и текстовый. Логи содержат информацию о запросах к API, кэшировании и ошибках.

🔮 Ограничения и улучшения
⚠️ Ограничения
Ограничение	Влияние
Нет Docker	Нельзя запустить одной командой docker compose up
Нет CI/CD	Тесты не запускаются автоматически при пуше
Нет HEALTHCHECK	Нет автоматической проверки живости бота
Парсинг HTML	Зависит от структуры сайта; при изменении вёрстки может сломаться
🚀 Улучшения (по приоритету)
Улучшение	Что даст	Приоритет
Dockerfile + compose	Запуск одной командой, изоляция	Высокий
CI/CD (GitHub Actions)	Автотесты и сборка при пуше	Высокий
HEALTHCHECK	Автоматическая проверка живости	Средний
Кэширование расписания	Меньше запросов к сайту	Средний
Fallback при смене вёрстки	Бот не падает, если сайт изменился	Средний
Метрики Prometheus	Мониторинг запросов и ошибок	Низкий
👨‍💻 Автор
Alex88113

GitHub: @Alex88113

<div align="center">
⭐ Если проект был полезен — поставь звезду на GitHub!

</div> ```
