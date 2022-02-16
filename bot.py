import telebot
from imdb import IMDb, IMDbError
bot = telebot.TeleBot('5147701461:AAGXQC2w_h0nKIKS8r--3GEY8KsS4Rh8T64')
ia = IMDb()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text != "Привет":
        try:
            movie = str(ia.get_movie(message.text))
        except:
            movie = 'Фильма с таким ID нет'
        bot.send_message(message.from_user.id, movie)
bot.polling(none_stop=True)
