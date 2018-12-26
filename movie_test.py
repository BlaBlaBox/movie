#############################
# Written for pytest module #
# BlaBlaBox Movie Unit Test #
#############################

import requests


MOVIE = "http://blablabox-movie.herokuapp.com/"

#================= ADD NEW MOVIE ===========================

def send_add_movie(imdb_id, purchase, rent, video_url, json_control):
    movie_json = {"movie_id": imdb_id, "rent": rent, "purchase": purchase, "video_url": video_url} if json_control else None
    return requests.post(MOVIE + "movie/add", json=movie_json)


def add_movie(im_id, purchase, status, json_control=True):
    imdb_id = im_id
    purchase = purchase
    rent = 7
    video_url = "http://www.google.com"     # Check for valid URLs will be done by server-side

    add_movie_resp = send_add_movie(imdb_id, purchase, rent, video_url, json_control) 

    assert add_movie_resp.status_code == status

#================= END OF ADD NEW MOVIE ====================

#================= GET ALL MOVIES ==========================

def send_get_movies():
    return requests.get(MOVIE + "movie/get")


def get_movies(status):
    get_movies_resp = send_get_movies()

    assert get_movies_resp.status_code == status

#================= END OF GET ALL MOVIES ===================

#================= GET MOVIE BY ID =========================

def send_get_movie_by_id(movie_id):
    return requests.get(MOVIE + "movie/get/" + str(movie_id))


def get_movie_by_id(movie_id, status):
    get_movie_by_id_resp = send_get_movie_by_id(movie_id)

    assert get_movie_by_id_resp.status_code == status


#================= END OF GET MOVIE BY ID ==================

#================= GET MOVIE CAST ==========================

def send_get_movie_cast(movie_id):
    return requests.get(MOVIE + "movie/get/" + str(movie_id) + "/cast")


def get_movie_cast(movie_id, status):
    get_movie_cast_resp = send_get_movie_cast(movie_id)

    assert get_movie_cast_resp.status_code == status

#================= END OF GET MOVIE CAST ===================

#================= DELETE MOVIE BY ID ======================

def send_delete_movie(movie_id, json_control):
    movie_json = {'movie_id': movie_id} if json_control else None
    return requests.post(MOVIE + "movie/delete", json=movie_json)


def delete_movie(movie_id, status, json_control=True):
    delete_movie_resp = send_delete_movie(movie_id, json_control)

    assert delete_movie_resp.status_code == status

#================= END OF DELETE MOVIE BY ID ===============

#================= END TEST ================================

def send_end_test(status=200):
    resp = requests.get(MOVIE + "endtest")
    assert resp.status_code == status

#================= END OF END TEST =========================

############################################################

#================= MAIN TEST ===============================

def test_add_movie():
    get_movie_by_id(1375666, 204)       # No movie with this ID now
    get_movie_by_id("asd", 404)         # Send unrecognized ID
    get_movie_cast(1375666, 204)        # No movie, so no cast for this ID now
    get_movie_cast("asd", 404)          # Send unrecognized ID
    get_movies(204)                     # Get all movies when there is no film (No content)
    delete_movie(1375666, 204)          # Delete movie when it is not exists
    delete_movie("asd", 500)            # Send unrecognized ID

    add_movie(1375666, 14, 200)         # Send a movie for first time
    add_movie(1375666, 14, 409)         # Send a movie for second time
    add_movie(13756666, 14, 404)        # Send an IMDB ID which is not exists in reality
    add_movie(1375666, "asd", 500)      # Send unrecognized price
    add_movie(1375666, -1, 422)         # Send a negative price

    add_movie(1375666, 14, 400, False)  # Send an invalid JSON

    get_movie_by_id(1375666, 200)       # Now, this film is exists
    get_movie_cast(1375666, 200)        # Now, this film, so cast is exists
    get_movies(200)                     # Get all movies when there is at least one movie
    delete_movie(1375666, 200)          # Delete movie when it's exists

    delete_movie(1375666, 400, False)   # Send an invalid JSON
    
    send_end_test(200)                  # Send a request to complete coverage report
