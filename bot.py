import telebot
import config
import dbworker
from imdb import IMDb, IMDbError
ia = IMDb()
movies, result_movie = '', ''
bot = telebot.TeleBot(config.token)

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_FILM.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить название фильма, но так и не сделал этого :( Жду...")
    elif state == config.States.S_ENTER_TRUE_FILM.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал выбрать нужный фильм из списка, но так и не сделал этого :( Жду...")
    elif state == config.States.S_ENTER_COMMAND.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал выбрать нужную команду, но так и не сделал этого :( Жду...")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Здравствуйте! Введите название фильма:")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой. Введите название фильма:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_FILM.value)
def user_entering_film(message):
    global movies
    movies = ia.search_movie(message.text)
    bot.send_message(message.chat.id, "Отлично! Теперь выберите нужный фильма из предложенного списка:")
    result = ''
    for movie in movies:
        try:
            output = "{0} - {1}".format(movie, movie.data['year'])
        except:
            output = "{0}".format(movie)
        bot.send_message(message.chat.id, output)
    dbworker.set_state(message.chat.id, config.States.S_ENTER_TRUE_FILM.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_TRUE_FILM.value)
def user_entering_true_film(message):
    global movies
    global result_movie
    film = message.text
    for movie in movies:
        if str(movie) == film:
            ID = movie.movieID
            break
    result_movie = ia.get_movie(ID)
    bot.send_message(message.chat.id, "Теперь выберите, какая информация о фильме вас интересует: дата выхода в России - data, сборы фильма - box office")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_COMMAND.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMMAND.value)
def user_entering_command(message):
    global result_movie
    request = message.text
    if request in ['data', 'box office']:
        if request == 'data':
            bot.send_message(message.chat.id, result_movie.data['original air date'])
        elif request == 'box office':
            bot.send_message(message.chat.id, result_movie.data['box office']['Cumulative Worldwide Gross'])
    else:
        bot.send_message(message.chat.id, 'Такого запроса нет.')
    bot.send_message(message.chat.id, "Отлично! Больше от тебя ничего не требуется. Если захочешь пообщаться снова - "
                     "отправь команду /start.")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == "__main__":
    bot.infinity_polling()
