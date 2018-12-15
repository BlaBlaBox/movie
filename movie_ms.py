from flask import jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from movie_db import add_movie, add_genre
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
@app.route('/movie/create', methods=['POST'])
#@auth.login_required
def create():
    if not request.json:
        return abort(400)
    '''
    movie_title = request.json['movie_title']
    release_date = request.json['release_date']
    duration = request.json['duration']
    rating = request.json['rating']
    information = request.json['information']
    '''
    movie_from_json = request.get_json()

    if add_movie(**movie_from_json):
        return jsonify({'result': 'Success'}), 200

    return abort(500)

# The update action of movie
@app.route('/movie/update', methods=['POST'])
@auth.login_required
def update(movie_id):
    if not request.json:
        return abort(400)
    '''
    movie_title = request.json['movie_title']
    release_date = request.json['release_date']
    duration = request.json['duration']
    rating = request.json['rating']
    information = request.json['information']
    '''
    movie_from_json = request.get_json()

    #if update_movie(movie_title):
    #    return jsonify({'result': 'Success'}), 200
    
    return abort(500)

# The delete action of movie
@app.route('/movie/get', methods=['GET'])
@auth.login_required
def get_all():
    # TODO: Take all trasactions from the db
    all_movies = []

    # TODO: Result of the database get action
    result = True

    if result:
        return jsonify({'result': 'Success'}), 200 # TODO: Send all movies in JSON format
    else:
        return abort(500)


# Get spesific movie
@app.route('/movie/get/<int:movie_id>', methods=['GET'])
@auth.login_required
def movie_get_id(movie_id):
    # TODO: Result of the database get action by movie_id
    result = True

    if result:
        return jsonify({'result': 'Success', 'movie': movie_id}), 200 # TODO: Send send spesific user.
    else:
        return abort(500)

# Get spesific movie genre
@app.route('/movie/get/<int:movie_genre>', methods=['GET'])
@auth.login_required
def movie_get_genre(movie_genre):
    # TODO: Result of the database get action bu movie_genre
    result = True

    if result:
        return jsonify({'result': 'Success', 'movie': movie_genre}), 200 # TODO: Send send spesific user.
    else:
        return abort(500)

# The delete action of movie
@app.route('/movie/delete', methods=['POST'])
@auth.login_required
def delete():
    if not request.json:
        return abort(400)

    # TODO: Delete that id
    movie_id = request.json['movie_id']

    # TODO: Result of the database delete action
    result = True

    if result:
        return jsonify({'result': 'Success'}), 200 # Password matches
    else:
        return abort(500)


# Validate the admin signin
@auth.verify_password
def verify_password(username, password):
    # TODO: Change check if is admin in the database or not.
    return username == 'admin' and password == 'asdqwe123'


genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film, Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Superhero', 'Thriller', 'War', 'Western']


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    for genre in genres:
        add_genre(genre)

