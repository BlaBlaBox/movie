import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_jwt_extended import JWTManager


url = os.getenv("DATABASE_URL")
if url is None:
    url = os.getenv("DATABASE_URL_MOVIE")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['JWT_SECRET_KEY'] = 'blablabox-secret-pass'
db = SQLAlchemy(app)
#jwt = JWTManager(app)
