from datetime import datetime
from imdb import IMDb
from sqlalchemy.exc import IntegrityError
from movie_config import db

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
    video_url = db.Column(db.String, nullable=True)
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



def jsonify_movie_model(obj):
    return {'movie_id': obj.movie_id, 'movie_title': obj.movie_title, 'release_year': obj.release_year,
            'added_at': obj.added_at, 'duration': obj.duration, 'rating': obj.rating, 'information': obj.information,
            'cover_url': obj.cover_url, 'video_url': obj.video_url, 'rent_price': obj.rent_price, 'purchase_price': obj.purchase_price}

def jsonify_casting_persons(obj):
    return {'person_id': obj.person_id, 'name': obj.name}



GENRES = ['Action', 'Adventure', 'Animation', 'Biography',
          'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
          'Fantasy', 'Film Noir', 'History', 'Horror', 'Music',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short',
          'Sport', 'Superhero', 'Thriller', 'War', 'Western']



def insert_genre(genre_name):
    try:
        new_genre = Genre(genre_name=genre_name)
        db.session.add(new_genre)
        db.session.commit()
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()


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

    try:
        temp_dur = mov["runtimes"][0]
    except KeyError:
        return 404
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
    try:
        result = ia.get_movie(movie_id)
    except BaseException as err:
        print("Err: ", err)
        return 404
    return parse_movie(result)




def insert_person(person_id, name):
    try:
        new_person = Person(person_id=person_id, name=name)
        db.session.add(new_person)
        db.session.commit()
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()


def insert_movie(m_id, title, rel_year, dur, rating, info, c_url, v_url, rent, purch):
    rel = datetime.strptime(str(rel_year), "%Y")
    try:
        new_movie = Movie(movie_id=int(m_id), movie_title=title, release_year=rel, duration=int(dur), rating=rating, information=info, cover_url=c_url, video_url=v_url, rent_price=float(rent), purchase_price=float(purch))
        db.session.add(new_movie)
        db.session.commit()
        print(new_movie)
        return 200
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()
        return 409
    except Exception as err:
        db.session.rollback()
        print("Err: ", err)
        return 500


def insert_movie_casting(movie_id, person_id):              #casting_role
    try:
        new_m_casting = MovieCasting(movie_id=movie_id, person_id=person_id)       #casting_role
        db.session.add(new_m_casting)
        db.session.commit()
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()


def insert_movie_director(movie_id, person_id):
    try:
        new_m_director = MovieDirector(movie_id=movie_id, person_id=person_id)
        db.session.add(new_m_director)
        db.session.commit()
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()


def insert_movie_genre(movie_id, genre_id):
    try:
        new_movie_genre = MovieGenre(movie_id=movie_id, genre_id=genre_id)
        db.session.add(new_movie_genre)
        db.session.commit()
    except IntegrityError as err:
        print("Err: ", err)
        db.session.rollback()

########## UPDATE ###############TODO####


def update_movie(movie_id, movie_title, release_date, duration, rating, information):

    movie_obj = Movie.query.filter_by(movie_id=movie_id).first()
    movie_obj.movie_title = movie_title
    movie_obj.release_date = release_date
    movie_obj.duration = duration
    movie_obj.rating = rating
    movie_obj.information = information

    db.session.commit()

    return movie_obj

######ENDOF####TODO###########

def get_movie(movie_id):
    return Movie.query.filter_by(movie_id=movie_id).first()


def get_movies():
    return Movie.query.order_by(Movie.purchase_price.desc()).all()


def get_movie_cast_db(movie_id):
    movie_person_list = MovieCasting.query.filter_by(movie_id=movie_id).all()
    if not movie_person_list:
        return 204
    person_ids = []
    person_names = []
    for person_it in movie_person_list:
        person_ids.append(person_it.person_id)
    for person in person_ids:
        person_names.append(jsonify_casting_persons(Person.query.filter_by(person_id=person).first()))

    return person_names


def delete_movie(movie_id):

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if movie is None:
        return 204

    movie_genre_list = MovieGenre.query.filter_by(movie_id=movie_id).all()
    for mov_gen in movie_genre_list:
        db.session.delete(mov_gen)
    movie_cast_list = MovieCasting.query.filter_by(movie_id=movie_id).all()
    for mov_cast in movie_cast_list:
        db.session.delete(mov_cast)
    movie_director_list = MovieDirector.query.filter_by(movie_id=movie_id).all()
    for mov_dir in movie_director_list:
        db.session.delete(mov_dir)
    
    db.session.commit()

    db.session.delete(movie)
    db.session.commit()
    return 200
