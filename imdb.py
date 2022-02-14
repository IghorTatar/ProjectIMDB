from imdb import IMDb
ia = IMDb()
asd = ia.search_movie('matrix')
if len(asd) == 0:
    print('yes')
else:
    ID = asd[0].movieID
    #dsa = 'The Matrix'
    e = ia.get_movie(ID)
    print(e)
# get a movie
movie = ia.get_movie('0133093')
for key in movie:
    print(key)
