import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


url = os.getenv("DATABASE_URL")
if url is None:
    url = "postgres://fumlefpkuoqdsh:60ab4c7e6c2ba5bb2a2dcc4c41b0f6bd603de6ad23ac8909a423d559e0640e35@ec2-54-247-125-116.eu-west-1.compute.amazonaws.com:5432/d6gaqulqjbq654"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
