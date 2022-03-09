import telebot
import config
import dbworker
from imdb import IMDb

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
        bot.send_message(message.chat.id, "Здравствуйте! Введите название фильма/сериала: (если в какой-либо момент захотите начать диалог сначала, напишите команду /reset)")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой. Введите название фильма/сериала:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_FILM.value)
def user_entering_film(message):
    global movies
    movies = ia.search_movie(message.text)
    if len(movies) == 0:
        bot.send_message(message.chat.id, "Такого фильма/сериала нет в базе данных IMDb. Попробуйте ещё:")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)
    else:
        bot.send_message(message.chat.id, "Отлично! Теперь выберите название фильма/сериала и его год выхода (если он есть) и напишите их через символ '~&':")
        result = ''
        for movie in movies:
            try:
                output = "{0} - {1}".format(movie, movie.data['year'])
            except KeyError:
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
            bot.send_message(message.chat.id, "Фильма/сериала с таким названием и датой нет в списке! Попробуйте ещё раз:")
            dbworker.set_state(message.chat.id, config.States.S_ENTER_TRUE_FILM.value)
        else:
            result_movie = ia.get_movie(ID)
            bot.send_message(message.chat.id, "Выберите, какая информация о фильме/сериале вас интересует:")
            bot.send_message(message.chat.id, "дата выхода в России - date,")
            bot.send_message(message.chat.id, "сборы фильма - box office,")
            bot.send_message(message.chat.id, "список актёров - actors,")
            bot.send_message(message.chat.id, "список режиссёров - directors,")
            bot.send_message(message.chat.id, "список сценаристов - writers,")
            bot.send_message(message.chat.id, "список продюссеров - producers,")
            bot.send_message(message.chat.id, "список композиторов  - composers.")
            dbworker.set_state(message.chat.id, config.States.S_ENTER_COMMAND.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMMAND.value)
def user_entering_command(message):
    global result_movie
    request = message.text
    if request in ['date', 'box office', 'actors', 'directors', 'writers', 'producers', 'composers']:
        try:
            if request == 'date':
                bot.send_message(message.chat.id, result_movie.data['original air date'])
            elif request == 'box office':
                bot.send_message(message.chat.id, result_movie.data['box office']['Cumulative Worldwide Gross'])
            elif request == 'actors':
                actor_list = []
                for actor in result_movie['cast']:
                    actor_list.append(str(actor))
                bot.send_message(message.chat.id, ', '.join(actor_list).rstrip(', '))
            elif request == 'directors':
                director_list = []
                for director in result_movie.data['director']:
                    director_list.append(str(director))
                bot.send_message(message.chat.id, ', '.join(director_list).rstrip(', '))
            elif request == 'writers':
                writer_list = []
                for writer in result_movie.data['writer']:
                    writer_list.append(str(writer))
                bot.send_message(message.chat.id, ', '.join(writer_list).rstrip(', '))
            elif request == 'producers':
                producer_list = []
                for producer in result_movie.data['producer']:
                    producer_list.append(str(producer))
                bot.send_message(message.chat.id, ', '.join(producer_list).rstrip(', '))
            elif request == 'composers':
                composer_list = []
                for composer in result_movie.data['composer']:
                    composer_list.append(str(composer))
                bot.send_message(message.chat.id, ', '.join(composer_list).rstrip(', '))
        except KeyError:
            bot.send_message(message.chat.id, "Такой информации об этом фильме/сериале нет в моих базах данных.")
    else:
        bot.send_message(message.chat.id, 'Такой команды нет.')
    bot.send_message(message.chat.id, "Это последний запрос?: 'yes' или 'no' (без кавычек)")
    dbworker.set_state(message.chat.id, config.States.S_END.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_END.value)
def user_ending(message):
    if message.text == 'no':
        bot.send_message(message.chat.id, "Выберите, какая информация о фильме/сериале вас интересует:")
        bot.send_message(message.chat.id, "дата выхода в России - date,")
        bot.send_message(message.chat.id, "сборы фильма - box office,")
        bot.send_message(message.chat.id, "список актёров - actors,")
        bot.send_message(message.chat.id, "список режиссёров - directors,")
        bot.send_message(message.chat.id, "список сценаристов - writers,")
        bot.send_message(message.chat.id, "список продюссеров - producers,")
        bot.send_message(message.chat.id, "список композиторов  - composers.")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_COMMAND.value)
    elif message.text == 'yes':
        bot.send_message(message.chat.id, "Отлично! Больше от вас ничего не требуется. Если захотите пообщаться снова - отправьте команду /start.")
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю! Пожалуйста, напишите 'yes' или 'no' (без кавычек)!")
        dbworker.set_state(message.chat.id, config.States.S_END.value)


if __name__ == "__main__":
    bot.infinity_polling()
