from imdb import IMDb, IMDbError
from datetime import *
ia = IMDb()
print('Введите film или time')
request = input()
if request == 'time':
    time = str(datetime.now()).split()[0].split('-')
    time.reverse()
    if time[1] in ['01', '03', '05', '07', '08', '10', '12']:
        if int(time[0]) + 7 > 31:
            time[0] = str(int(time[0]) + 7 - 31)
            if time[1] == '12':
                time[1] = '01'
                time[2] = str(int(time[2]) + 1)
            else:
                time[1] = str(int(time[1]) + 1)
        else:
            time[0] = str(int(time[0]) + 7)
    elif time[1] in ['04', '06', '09', '11']:
        if int(time[0]) + 7 > 30:
            time[0] = str(int(time[0]) + 7 - 30)
            time[1] = str(int(time[1]) + 1)
        else:
            time[0] = str(int(time[0]) + 7)
    elif time[1] == '02':
        if int(time[0]) + 7 > 28:
            time[0] = str(int(time[0]) + 7 - 28)
            time[1] = str(int(time[1]) + 1)
        else:
            time[0] = str(int(time[0]) + 7)
    clock = str(datetime.now()).split()[0].split('-')
    clock.reverse()
    print(clock)
    print(time)
elif request == 'film':
    print('Введите название фильма:')
    list_ = input()
    movies = ia.search_movie(list_)
    if len(movies) == 0:
        flag = True
        while flag:
            print('Нет ни одного фильма с подобным названием. Попробуй еще:')
            movies = ia.search_movie(input())
            if len(movies) != 0:
                flag = False

    print('Какой из нижеперечисленных фильмов вас интересует?')
    result = ''
    for movie in movies:
        try:
            output = "{0} - {1}".format(movie, movie.data['year'])
        except:
            output = "{0}".format(movie)
        print(output)
    film = input()
    for movie in movies:
        if str(movie) == film:
            ID = movie.movieID
            break
    result_movie = ia.get_movie(ID)
    print(result_movie.data.keys())

    print('Какая информация о фильме вас интересует: дата выхода в России - /data, режиссеры - /directors, список всех актеров - /actors, сборы фильма - /box office')
    flag = True
    while flag:
        request = input()
        if request in ['/data', '/directors', '/actors', '/box office', '/time']:
            if request == '/data':
                print(result_movie.data['original air date'])
                list_ = result_movie.data['original air date'].split()
                if list_[1] == 'Oct':
                    list_[1] == '10'
            elif request == '/directors':
                for director in result_movie.data['director']:
                    print(director)
            elif request == '/actors':
                for actor in result_movie.data['cast']:
                    print(actor)
            elif request == '/box office':
                print(result_movie.data['box office']['Cumulative Worldwide Gross'])
            print('Это последний запрос?: /да или /нет')
            if input() == '/да':
                flag = False
        else:
            print('Такого запроса нет.')
