# Telegram & VK DialogFlow Bots

Этот проект — это два чат-бота для Telegram и VKontakte, которые интегрированы с DialogFlow от Google. Боты умеют отвечать на заранее обученные вопросы с помощью искусственного интеллекта.

## Что умеют боты

* ✉ Отвечают на частые вопросы, например:

  * "Как устроиться к вам на работу?"
  * "Забыл пароль"
  * "Хочу удалить аккаунт"
*  Работают на базе DialogFlow: распознают намерения (intents) и подбирают релевантные ответы
*  Отправляют логи в Telegram в случае ошибок (для мониторинга работы ботов)
*  Если бот не понимает сообщение, он молчит (чтобы не мешать техподдержке)

## Что такое DialogFlow

[DialogFlow](https://dialogflow.cloud.google.com/) — это платформа от Google для создания чат-ботов, которая распознаёт естественную речь, анализирует намерения и отправляет ответные сообщения. Поддерживает множество языков, включая русский.
## Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/your_username/Bot_helper.git
cd Bot_helper
```
2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Создайте файл .env в корне проекта и добавьте переменные:
```bash
PROJECT_ID=yout_project_id # из DialogFlow
GOOGLE_APPLICATION_CREDENTIALS=your_key.json # путь до JSON-файла ключа сервисного аккаунта из Google Cloud
TELEGRAM_TOKEN=your_telegram_token
TG_CHAT_ID=your_telegram_chat_id
VK_API_TOKEN=your_vk_token
```
5. Добавьте файл с ключами DialogFlow (например, bot33331-***.json) в корень проекта.

## Структура проекта

* `telegram_bot.py` — бот для Telegram
* `vk_bot.py` — бот для ВКонтакте
* `learn_dialogflow.py` — скрипт для обучения DialogFlow новыми фразами
* `logger_config.py` — настройка логгирования ошибок в Telegram
* `questions.json` — файл с обучающими примерами (intents)
* `.env` — секреты и токены (не публикуется)
## Проверка работоспособности
```bash
python telegram_bot.py
```
Отправьте сообщение боту в Telegram — он должен ответить с помощью DialogFlow.
```bash
python vk_bot.py
```
Напишите группе ВКонтакте — бот ответит через DialogFlow.

## Ссылки на работающих ботов

* 👉 [Telegram бот](https://web.telegram.org/k/#@verbgametechhelpbot)
* 👉 [VK бот](https://vk.com/club231073553)

## 🎞️ Гифка диалога

![Демонстрация работы бота](demo.gif)

## License

MIT

---

Боты готовы к бою! Загляните в код, напишите что-то боту и получите осмысленный ответ.
