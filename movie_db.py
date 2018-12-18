from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from imdb import IMDb
from movie_config import app, db

ia = IMDb()

#db.drop_all()


class Person(db.Model):

    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)


class Movie(db.Model):

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Date)
    added_at = db.Column(db.DateTime, default=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    duration = db.Column(db.SmallInteger)
    rating = db.Column(db.Float)
    information = db.Column(db.Text)
    cover_url = db.Column(db.String, nullable=True)
    rent_price = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)



class MovieCasting(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), primary_key=True)
    #cast_role = db.Column(db.String(50))


class MovieDirector(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), primary_key=True)


class Genre(db.Model):

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), unique=True)


class MovieGenre(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)



db.create_all()


GENRES = [  'Action', 'Adventure', 'Animation', 'Biography',
            'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
            'Fantasy', 'Film Noir', 'History', 'Horror', 'Music',
            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short',
            'Sport', 'Superhero', 'Thriller', 'War', 'Western'    ]



def insert_genre(genre_name):

    new_genre = Genre(genre_name=genre_name)
    db.session.add(new_genre)
    db.session.commit()


def create_genres():
    for gen in GENRES:
        insert_genre(gen)


create_genres()


def find_genre_ids(gen_list):
    result = []
    for gen in gen_list:
        for _genre, i in zip(GENRES, range(1, 50)):
            if gen == _genre:
                result.append(i)

    return result


#def parse_extra_cast(per):
#    print(vars(per.currentRole))
#    return per.currentRole


def parse_person(per):

    person_id = ia.get_imdbID(per)
    name = per["name"]
#    result = [person_id, name]     # extra_arg = is_cast=True
#    if is_cast:
#        result.append(parse_extra_cast(per))
    return [person_id, name]


def parse_movie(mov):

    temp_dur = mov["runtimes"][0]
    if ':' in temp_dur:
        temp_dur = (temp_dur.split(":"))[1]

    movie_id = ia.get_imdbID(mov)
    title = mov["title"]
    release_year = mov["year"]
    duration = temp_dur
    rating = mov["rating"]
    information = mov["plot outline"]
    cover_url = mov["cover url"]
    genres = find_genre_ids(mov["genres"])

    temp_director = mov["director"]
    temp_cast = mov["cast"]

    directors = []
    casts = []

    for direc in temp_director:
        directors.append(parse_person(direc))

    for cas in temp_cast:
        casts.append(parse_person(cas))

    return {'movie':[movie_id, title, release_year, duration, rating, information, cover_url], 'genre': genres, 'director':directors, 'cast':casts}


def get_movie_from_imdb(movie_id):
    result = ia.get_movie(movie_id)
    return parse_movie(result)




def insert_person(person_id, name):

    new_person = Person(person_id=person_id, name=name)
    db.session.add(new_person)
    db.session.commit()
    return new_person


def insert_movie(movie_id, movie_title, release_year, duration, rating, information, cover_url, rent_price, purchase_price):

    new_movie = Movie(movie_id, movie_title, release_year, duration, rating, information, cover_url, rent_price, purchase_price)
    db.session.add(new_movie)
    db.session.commit()

    return new_movie


def insert_movie_casting(movie_id, person_id):              #casting_role

    new_m_casting = MovieCasting(movie_id, person_id)       #casting_role
    db.session.add(new_m_casting)
    db.session.commit()


def insert_movie_director(movie_id, person_id):

    new_m_director = MovieDirector(movie_id, person_id)
    db.session.add(new_m_director)
    db.session.commit()


def insert_movie_genre(movie_id, genre_id):

    new_movie_genre = MovieGenre(movie_id, genre_id)
    db.session.add(new_movie_genre)
    db.session.commit()


########## UPDATE ###############


def update_movie(movie_id, movie_title, release_date, duration, rating, information):

    movie_obj = Movie.query.filter_by(movie_id=movie_id).first()
    movie_obj.movie_title = movie_title
    movie_obj.release_date = release_date
    movie_obj.duration = duration
    movie_obj.rating = rating
    movie_obj.information = information

    db.session.commit()

    return movie_obj



def get_movie(movie_id):
    return Movie.query.filter_by(movie_id=movie_id).first()


def get_movies():
    return Movie.query.all().order_by(Movie.purchase_price.desc())



def delete_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    db.session.delete(movie)
    db.session.commit()
    return True


