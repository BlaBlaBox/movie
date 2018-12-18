from imdb import IMDb
from movie_db import parse_movie

ia = IMDb()

print('aaa')
mov2 = ia.get_movie('0094226')

print(parse_movie(mov2))

