from flask import jsonify, request, abort
from movie_db import insert_movie, insert_person, insert_movie_casting, insert_movie_director, insert_movie_genre, get_movie, get_movies, get_movie_cast_db, delete_movie, get_movie_from_imdb, jsonify_movie_model
from movie_config import app


@app.errorhandler(400)
def bad_request():
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@app.errorhandler(401)
def unauthorized_access():
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden():
    return jsonify({'error': 'Forbidden!'}), 403

@app.errorhandler(404)
def not_found():
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(409)
def wrong_input():
    return jsonify({'error': 'Data already exists'}), 409

@app.errorhandler(422)
def already_exists():
    return jsonify({'error': 'Prices cannot be zero or negative'}), 422

@app.errorhandler(500)
def internal_server_error():
    return jsonify({'error' : 'Internal server error'}), 500



# The create action of movie
@app.route('/movie/add', methods=['POST'])
def add_movie():
    if not request.json:
        return abort(400)

    movie_id = request.json["movie_id"]
    video_url = request.json["video_url"]
    rent = request.json["rent"]
    purchase = request.json["purchase"]

    if rent <= 0 or purchase <= 0:
        abort(422)

    movie_details = get_movie_from_imdb(movie_id)
    if movie_details == 404:
        abort(404)

    movie_det = movie_details["movie"]
    genres = movie_details["genre"]
    directors = movie_details["director"]
    casts = movie_details["cast"]

    movie_det.append(video_url)
    movie_det.append(rent)
    movie_det.append(purchase)
    mov_res = insert_movie(*movie_det)

    if mov_res != 200:
        abort(mov_res)

    for cas in casts:
        insert_person(cas[0], cas[1])
        insert_movie_casting(movie_id, cas[0])

    for direc in directors:
        insert_person(direc[0], direc[1])
        insert_movie_director(movie_id, direc[0])

    for gen in genres:
        insert_movie_genre(movie_id, gen)

    return jsonify({'result': 'Success'}), 200



# The delete action of movie
@app.route('/movie/get', methods=['GET'])
def get_all_movies():

    all_movies = get_movies()
    all_movies_json = []

    for mov in all_movies:
        all_movies_json.append(jsonify_movie_model(mov))

    if all_movies_json:
        return jsonify(result='Success', movies=all_movies_json), 200
    return jsonify(result='No film exists', movies=all_movies_json), 204


# Get spesific movie
@app.route('/movie/get/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = get_movie(movie_id)
    print(movie)
    if movie:
        return jsonify(result='Success', movie=jsonify_movie_model(movie)), 200 # TODO: Send send spesific user.
    return abort(500)


@app.route('/movie/get/<int:movie_id>/cast', methods=['GET'])
def get_movie_cast(movie_id):

    all_cast = get_movie_cast_db(movie_id)

    if all_cast:
        return jsonify({'result': 'Success', 'cast': all_cast}), 200
    return abort(500)


# The delete action of movie
@app.route('/movie/delete', methods=['POST'])
def delete_movie_by_id():
    if not request.json:
        return abort(400)

    movie_id = request.json['movie_id']

    if delete_movie(movie_id):
        return jsonify({'result': 'Success'}), 200 # Password matches
    return abort(500)



if __name__ == '__main__':
    app.run(debug=True, port=8000)
