from imdb import IMDb, IMDbError
ia = IMDb()
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
print('Какая информация о фильме вас интересует: дата выхода в России - /data, режиссеры - /directors, список всех актеров - /actors, сборы фильма - /box office')
flag = True
while flag:
    request = input()
    if request in ['/data', '/directors', '/actors', '/box office']:
        if request == '/data':
            print(result_movie.data['original air date'])
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
