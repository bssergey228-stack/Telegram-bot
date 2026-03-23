from flask import Flask, request
import requests
import json
import os

# Твой токен бота
TOKEN = "8729405998:AAFZot5rO26iCSH9NaHYelt0i2gRNwX4c_c"

# Создаем веб-приложение
app = Flask(__name__)


def send_message(chat_id, text):
    """Отправляет сообщение пользователю"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"Ошибка: {e}")


@app.route('/', methods=['GET'])
def index():
    """Главная страница для проверки"""
    return "🤖 Бот работает! Твой ноутбук может быть выключен."


@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Telegram будет отправлять сюда все сообщения"""
    try:
        # Получаем данные от Telegram
        update = request.get_json()

        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            user_name = message['chat'].get('first_name', 'Друг')

            print(f"Получено сообщение от {user_name}: {text}")

            # Обработка команд
            if text == '/start':
                send_message(chat_id,
                             f"👋 Привет, {user_name}!\n\nЯ бот, который работает в облаке!\nТвой ноутбук можешь выключить - я всё равно отвечу 😊")

            elif text == '/help':
                send_message(chat_id,
                             "📝 Команды:\n/start - приветствие\n/help - помощь\n\nПросто напиши что-нибудь - я отвечу!")

            elif text == '/info':
                send_message(chat_id,
                             f"🤖 Информация:\n- Хостинг: Render.com\n- Статус: 🟢 Работает 24/7\n- Твой ID: {chat_id}")

            else:
                # Ответ на любое сообщение
                send_message(chat_id, f"📨 Ты написал: {text}\n\nЯ работаю на сервере, а ты можешь спать 😴")

        return 'OK', 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return 'Error', 500


if __name__ == '__main__':
    # Запускаем приложение
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)