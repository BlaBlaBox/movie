from flask import jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from movie_db import insert_movie, insert_person, insert_movie_casting, insert_movie_director, insert_movie_genre, update_movie, get_movie, get_movies, delete_movie, get_movie_from_imdb
from movie_config import app

auth = HTTPBasicAuth()

@app.errorhandler(400)
def bad_request():
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@auth.error_handler
def unauthorized_access():
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden():
    return jsonify({'error': 'Forbidden!'}), 403

@app.errorhandler(404)
def not_found():
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error():
    return jsonify({'error' : 'Internal server error'}), 500



# The create action of movie
@app.route('/movie/add', methods=['POST'])
#@auth.login_required
def add_movie():
    if not request.json:
        return abort(400)
    '''
    movie_title = request.json['movie_title']
    release_date = request.json['release_date']
    duration = request.json['duration']
    rating = request.json['rating']
    information = request.json['information']
    '''

    #movie_from_json = request.get_json()
    movie_id = request.json["movie_id"]
    rent = request.json["rent"]
    purchase = request.json["purchase"]
    movie_details = get_movie_from_imdb(movie_id)

    movie_det = movie_details["movie"]
    genres = movie_details["genre"]
    directors = movie_details["director"]
    casts = movie_details["cast"]

    for cas in casts:
        insert_person(*cas)
        insert_movie_casting(movie_id, cas[0])

    for direc in directors:
        insert_person(*direc)
        insert_movie_director(movie_id, direc[0])

    movie_det.append(rent)
    movie_det.append(purchase)

    for gen in genres:
        insert_movie_genre(movie_id, gen)

    if insert_movie(*movie_det):
        return jsonify({'result': 'Success'}), 200

    return abort(500)



# The update action of movie
@app.route('/movie/update', methods=['POST'])
@auth.login_required
def update_movie_by_id():
    if not request.json:
        return abort(400)
    '''
    movie_id = request.json['movie_id']
    movie_title = request.json['movie_title']
    release_date = request.json['release_date']
    duration = request.json['duration']
    rating = request.json['rating']
    information = request.json['information']
    '''
    movie_from_json = request.get_json()

    if update_movie(**movie_from_json):
        return jsonify({'result': 'Success'}), 200

    return abort(500)



# The delete action of movie
@app.route('/movie/get', methods=['GET'])
#@auth.login_required
def get_all_movies():

    all_movies = get_movies()

    if all_movies:
        return jsonify({'result': 'Success', 'movies': all_movies}), 200
    return abort(500)



# Get spesific movie
@app.route('/movie/get/<int:movie_id>', methods=['GET'])
@auth.login_required
def get_movie_by_id(movie_id):
    movie = get_movie(movie_id)
    if movie:
        return jsonify({'result': 'Success', 'movie': movie}), 200 # TODO: Send send spesific user.
    return abort(500)



# Get spesific movie genre
@app.route('/movie/get/<int:movie_genre>', methods=['GET'])
@auth.login_required
def movie_get_genre(movie_genre):
    # TODO: Result of the database get action bu movie_genre
    result = True

    if result:
        return jsonify({'result': 'Success', 'movie': movie_genre}), 200 # TODO: Send send spesific user.
    return abort(500)



# The delete action of movie
@app.route('/movie/delete', methods=['POST'])
@auth.login_required
def delete_movie_by_id():
    if not request.json:
        return abort(400)

    movie_id = request.json['movie_id']

    if delete_movie(movie_id):
        return jsonify({'result': 'Success'}), 200 # Password matches
    return abort(500)



# Validate the admin signin#####TODO##############
@auth.verify_password
def verify_password(username, password):
    # TODO: Change check if is admin in the database or not.
    return username == 'admin' and password == 'asdqwe123'




if __name__ == '__main__':
    app.run(debug=True, port=8000)
