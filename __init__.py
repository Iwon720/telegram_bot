import requests
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from funcs import try_except, if_none

TOKEN = "7441878589:AAGGNwZLACaQayXgjEaUIutGv84K4Zhbz4E"

CRYPTO_TOKEN_NAMES = {
    'BTC': 'BTCUSDT',
    'ETH': 'ETHUSDT',
    'LTC': 'LTCUSDT',
}

bot = TeleBot(TOKEN)

user_states = {}
own_text = "Ввести свою крипту:"


@bot.message_handler(commands=['start', 'stop'])
def start_message(message):
    markup = ReplyKeyboardMarkup()
    command = message.text.split()[0]
    if command == "/start":
        for crypto_token_name in CRYPTO_TOKEN_NAMES.keys():
            item_button = KeyboardButton(crypto_token_name)
            markup.add(item_button)
        custom_input_button = KeyboardButton(own_text)
        markup.add(custom_input_button)
        bot.send_message(message.chat.id, "Дарова, питушара", reply_markup=markup)

    elif command == "/stop":
        bot.send_message(message.chat.id, "Прощай, скучать не буду")
        bot.stop_bot()


@bot.message_handler(func=lambda message: message.text == own_text)
def ask_for_custom_input(message):
    bot.send_message(message.chat.id, text=f'{message.chat.first_name}, введите название криптовалюты: ')
    user_states[message.chat.id] = "waiting_for_input"
    print(user_states)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_input")
def handle_custom_input(message):
    custom_text = message.text.upper()
    print(f"custom_text {custom_text}")
    text = get_info_from_binance_api(value=custom_text)
    text = if_none(text)
    bot.send_message(message.chat.id, text=text)
    user_states[message.chat.id] = None


@bot.message_handler(func=lambda message: message.text in CRYPTO_TOKEN_NAMES.keys())
def send_price_of_crypto(message):
    print(f"message.text {message.text}")
    text = get_info_from_binance_api(value=CRYPTO_TOKEN_NAMES.get(message.text))
    bot.send_message(message.chat.id, text=text)


@try_except
def get_info_from_binance_api(*, value) -> str:
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url, params={'symbol': value})
    print(response.json())
    text = str(float(response.json()['price']))
    return text


bot.infinity_polling()
