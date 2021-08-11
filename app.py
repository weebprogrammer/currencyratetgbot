import telebot
from config import TOKEN, keys
from utils import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем порядке: \n *имя валюты* *в какую валюту надо перевести* *количество переводимой валюты*\n' \
           'Список доступных валют по команде /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def CurrencyRate(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")
        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        total_amount = float(total_base)*float(amount)
        bot.send_message(message.chat.id, f"{amount} {quote} - {total_amount} {base}")
bot.polling()