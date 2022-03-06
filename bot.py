import telebot
import config
import dbworker
from imdb import IMDb, IMDbError

ia = IMDb()
movies = ''
result_movie  = ''
bot = telebot.TeleBot(config.token)


# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_FILM.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить название фильма, но так и не сделал этого ): Жду...")
    elif state == config.States.S_ENTER_TRUE_FILM.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал выбрать нужный фильм из списка, но так и не сделал этого ): Жду...")
    elif state == config.States.S_ENTER_COMMAND.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал выбрать нужную команду, но так и не сделал этого ): Жду...")
    elif state == config.States.S_END.value:
        bot.send_message(message.chat.id, "Кажется, кто-то так и не принял решение: выбрать ещё одну характеристику фильма или нет ): Жду...")
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
    if len(movies) == 0:
        bot.send_message(message.chat.id, "Такого фильма нет в базе данных IMDb. Попробуйте ещё:")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)
    else:
        bot.send_message(message.chat.id, "Отлично! Теперь выберите название фильма и его год выхода (если он есть) и напишите их через символ '~&':")
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
    if '~&' not in film:
        bot.send_message(message.chat.id, "Я не вижу символа '~&'! Обязательно напишите его:")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_TRUE_FILM.value)
    else:
        ID = ''
        film_list = film.split('~&')
        bot.send_message(message.chat.id, film_list[0])
        bot.send_message(message.chat.id, film_list[1])
        for movie in movies:
            if str(movie) == film_list[0] and str(movie.data['year']) == film_list[1]:
                ID = movie.movieID
                break
        if ID == '':
            bot.send_message(message.chat.id, "Фильма с таким названием и датой нет в списке! Попробуйте ещё раз:")
            dbworker.set_state(message.chat.id, config.States.S_ENTER_TRUE_FILM.value)
        else:
            result_movie = ia.get_movie(ID)
            bot.send_message(message.chat.id, "Выберите, какая информация о фильме вас интересует:")
            bot.send_message(message.chat.id, "дата выхода в России - date,")
            bot.send_message(message.chat.id, "сборы фильма - box office")
            dbworker.set_state(message.chat.id, config.States.S_ENTER_COMMAND.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMMAND.value)
def user_entering_command(message):
    global result_movie
    request = message.text
    if request in ['date', 'box office']:
        try:
            if request == 'date':
                bot.send_message(message.chat.id, result_movie.data['original air date'])
            elif request == 'box office':
                bot.send_message(message.chat.id, result_movie.data['box office']['Cumulative Worldwide Gross'])
        except KeyError:
            bot.send_message(message.chat.id, "В моих базах данных нет этой информации о выбранном фильме/сериале.")
    else:
        bot.send_message(message.chat.id, 'Такой команды нет.')
    bot.send_message(message.chat.id, "Это последний запрос?: 'yes' или 'no' (без кавычек)")
    dbworker.set_state(message.chat.id, config.States.S_END.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_END.value)
def user_ending(message):
    if message.text == 'no':
        bot.send_message(message.chat.id, "Выберите, какая информация о фильме вас интересует: дата выхода в России - data, сборы фильма - box office")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_COMMAND.value)
    elif message.text == 'yes':
        bot.send_message(message.chat.id, "Отлично! Больше от вас ничего не требуется. Если захотите пообщаться снова - отправь команду /start.")
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю! Пожалуйста, напишите 'yes' или 'no' (без кавычек)!")
        dbworker.set_state(message.chat.id, config.States.S_END.value)


if __name__ == "__main__":
    bot.infinity_polling()
