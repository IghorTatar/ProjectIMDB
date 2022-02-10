from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()

# get a movie
movie = ia.get_movie('0133093')

data = input("Введите дату выхода фильма в формате '14 Oct 1999':")
if data == '14 Oct 1999':
    print(movie)
