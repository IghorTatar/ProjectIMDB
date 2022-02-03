import telebot
bot = telebot.TeleBot('2092560262:AAGBd8pI9jbrbFGUBxjegl1eVKNIA7XK4zc')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    else:
        bot.send_message(message.from_user.id, "Пока")
bot.polling(none_stop=True)
