from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from movie_config import app

db = SQLAlchemy(app)

db.drop_all()


class Person(db.Model):

    person_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1))
    dob = db.Column(db.Date)


class Movie(db.Model):

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date)
    added_at = db.Column(db.DateTime, default=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    duration = db.Column(db.SmallInteger)
    rating = db.Column(db.Float)
    information = db.Column(db.Text)


class Actor(db.Model):

    actor_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))


class Director(db.Model):

    director_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))


class MovieCasting(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True)
    cast_role = db.Column(db.String(50))


class MovieDirector(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'), primary_key=True)


class Genre(db.Model):

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)


class MovieGenre(db.Model):

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)



db.create_all()


def add_person(name, surname, gender, dob):

    new_person = Person(firstname=name, surname=surname, gender=gender, dob=dob)
    db.session.add(new_person)
    db.session.commit()
    return new_person


def add_movie(movie_title, release_date, duration, rating, information):

    new_movie = Movie(movie_title=movie_title, release_date=release_date, duration=duration, rating=rating, information=information)
    db.session.add(new_movie)
    db.session.commit()

    return new_movie


def add_actor(name, surname, gender, dob):

    new_person = add_person(name, surname, gender, dob)
    new_actor = Actor(person_id=new_person.person_id)
    db.session.add(new_actor)
    db.session.commit()


def add_director(name, surname, gender, dob):

    new_person = add_person(name, surname, gender, dob)
    new_director = Director(person_id=new_person.person_id)
    db.session.add(new_director)
    db.session.commit()


def add_movie_casting(movie_id, actor_id, casting_role):

    new_m_casting = MovieCasting(movie_id, actor_id, casting_role)
    db.session.add(new_m_casting)
    db.session.commit()


def add_movie_director(movie_id, director_id):

    new_m_director = MovieDirector(movie_id, director_id)
    db.session.add(new_m_director)
    db.session.commit()


def add_genre(genre_name):

    new_genre = Genre(genre_name)
    db.session.add(new_genre)
    db.session.commit()


def add_movie_genre(movie_id, genre_id):

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


def update_person(p_id, name, surname, gender, dob):

    person_obj = Person.query.filter_by(person_id=p_id).first()
    person_obj.name = name
    person_obj.surname = surname
    person_obj.gender = gender
    person_obj.dob = dob

    db.session.commit()


def update_actor(actor_id, name, surname, gender, dob):

    actor_obj = Actor.query.filter_by(actor_id=actor_id).first()
    update_person(actor_obj.person_id, name, surname, gender, dob)


def update_director(director_id, name, surname, gender, dob):

    director_obj = Director.query.filter_by(director_id=director_id).first()
    update_person(director_obj.person_id, name, surname, gender, dob)


def update_genre(genre_id, genre_name):

    genre_obj = Genre.query.filter_by(genre_id=genre_id).first()
    genre_obj.genre_name = genre_name
    db.session.commit()


#def delete_person(person_id):
