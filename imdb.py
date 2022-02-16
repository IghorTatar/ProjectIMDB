from imdb import IMDb, IMDbError
ia = IMDb()
print('Введите название фильма:')
list_ = input()
movies = ia.search_movie(list_)
print(movies)
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
    result += str(movie['title']) + ', '
print(result.rstrip(', '))
