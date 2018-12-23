from flask import jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from movie_db import insert_movie, insert_person, insert_movie_casting, insert_movie_director, insert_movie_genre, update_movie, get_movie, get_movies, get_movie_cast_db, delete_movie, get_movie_from_imdb, jsonify_movie_model
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

    #movie_from_json = request.get_json()
    movie_id = request.json["movie_id"]
    video_url = request.json["video_url"]
    rent = request.json["rent"]
    purchase = request.json["purchase"]
    movie_details = get_movie_from_imdb(movie_id)

    movie_det = movie_details["movie"]
    genres = movie_details["genre"]
    directors = movie_details["director"]
    casts = movie_details["cast"]

    movie_det.append(video_url)
    movie_det.append(rent)
    movie_det.append(purchase)

    if insert_movie(*movie_det) is None:
        abort(500)

    for cas in casts:
        insert_person(cas[0], cas[1])
        insert_movie_casting(movie_id, cas[0])

    for direc in directors:
        insert_person(direc[0], direc[1])
        insert_movie_director(movie_id, direc[0])

    for gen in genres:
        insert_movie_genre(movie_id, gen)

    return jsonify({'result': 'Success'}), 200



# The update action of movie
@app.route('/movie/update', methods=['POST'])
@auth.login_required
def update_movie_by_id():
    if not request.json:
        return abort(400)

    movie_from_json = request.get_json()

    if update_movie(**movie_from_json):
        return jsonify({'result': 'Success'}), 200

    return abort(500)



# The delete action of movie
@app.route('/movie/get', methods=['GET'])
#@auth.login_required
def get_all_movies():

    all_movies = get_movies()
    all_movies_json = []

    for mov in all_movies:
        all_movies_json.append(jsonify_movie_model(mov))

    if all_movies_json:
        return jsonify(result='Success', movies=all_movies_json), 200
    return jsonify(result='No film exists', movies=None), 204



# Get spesific movie
@app.route('/movie/get/<int:movie_id>', methods=['GET'])
#@auth.login_required
def get_movie_by_id(movie_id):
    movie = get_movie(movie_id)
    print(movie)
    if movie:
        return jsonify(result='Success', movie=jsonify_movie_model(movie)), 200 # TODO: Send send spesific user.
    return abort(500)



# Get spesific movie genre
#@app.route('/movie/get/<int:movie_genre>', methods=['GET'])
#@auth.login_required
#def movie_get_genre(movie_genre):
#    # TODO: Result of the database get action bu movie_genre
#    result = True

#    if result:
#        return jsonify({'result': 'Success', 'movie': movie_genre}), 200 # TODO: Send send spesific user.
#    return abort(500)


@app.route('/movie/get/<int:movie_id>/cast', methods=['GET'])
#@auth.login_required
def get_movie_cast(movie_id):

    all_cast = get_movie_cast_db(movie_id)

    if all_cast:
        return jsonify({'result': 'Success', 'cast': all_cast}), 200
    return abort(500)



# The delete action of movie
@app.route('/movie/delete', methods=['POST'])
#@auth.login_required
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
