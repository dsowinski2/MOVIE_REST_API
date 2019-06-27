import urllib.request
from io import BytesIO

import pandas as pd
from flask import Flask, render_template,request,send_file,jsonify
from flask_sqlalchemy import SQLAlchemy
import re
from zipfile import ZipFile


app = Flask(__name__)
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class movies(db.Model):
    __tablename__ = 'movies'

    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    genres = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)



    def __repr__(self):
        return f"movies('{self.movieId}','{self.title}','{self.genres}','{self.year}')"

class links(db.Model):
    __tablename__ = 'links'
    index = db.Column(db.Integer,nullable=False, primary_key=True)
    movieId = db.Column(db.Integer, nullable=False)
    imdbId = db.Column(db.Integer, nullable=False)
    tmdbId = db.Column(db.Float)

    def __repr__(self):
        return f"links('{self.movieId}','{self.imdbId}')"


class tags(db.Model):
    __tablename__ = 'tags'
    index = db.Column(db.Integer, nullable=False, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    movieId = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"tags('{self.movieId}','{self.tag}')"
class ratings(db.Model):
    __tablename__ = 'ratings'
    index = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    movieId = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ratings('{self.movieId}','{self.rating}')"
