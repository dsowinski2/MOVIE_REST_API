#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from io import BytesIO
import re

from flask import Flask, render_template,request,send_file,jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from zipfile import ZipFile
from sqlalchemy import create_engine, text

import db_insert
import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
engine = create_engine('sqlite:///site.db')


GET_PRODUCTION_YEAR = '''
SELECT movies.title, movies.genres
FROM movies
WHERE movies.year == (?)
'''

ALL_MOVIES = '''
SELECT title, genres FROM movies
'''
SORT_DESC = '''
SELECT title, genres FROM movies ORDER BY year DESC
'''
SORT_ASC = '''
SELECT title, genres FROM movies ORDER BY year ASC
'''
SINGLE_MOVIE = '''

SELECT ROUND(AVG(rating),1) as rating, movies.title, movies.genres, movies.year, links.imdbId, movies.movieId
FROM movies
JOIN links ON movies.movieId == links.movieId
JOIN ratings ON movies.movieId == ratings.movieId

WHERE movies.movieId == (?)
'''
ONE_TAG = '''
SELECT movies.title, movies.genres, tags.tag
FROM movies
JOIN tags ON movies.movieId == tags.movieId
WHERE tags.tag == (?)
'''
TWO_TAGS = '''
SELECT first_tag.title, first_tag.tag as tag1, tags.tag as tag2, first_tag.year, first_tag.genres FROM(
SELECT movies.movieId, movies.title, movies.genres, tags.tag, movies.year
FROM movies
JOIN tags ON movies.movieId == tags.movieId
WHERE tags.tag == (?)) AS first_tag
JOIN tags ON first_tag.movieId == tags.movieId
WHERE tags.tag == (?)
'''


app = Flask(__name__)
@app.route('/movies', methods=['GET'])
def movies():

    sort  = request.args.get('sort')
    year  = request.args.getlist('year')
    tag = request.args.getlist('tag')

    if tag:
        if len(tag) == 1:
            data = pd.read_sql_query(ONE_TAG, engine, params=tag)
            
        else:
            data = pd.read_sql_query(TWO_TAGS, engine, params=tag)
    elif year:
        
        data = pd.read_sql_query(GET_PRODUCTION_YEAR, engine, params = year)

    elif sort:
        if sort == '-year':
            data = pd.read_sql_query(SORT_ASC, engine)
        else:
            data = pd.read_sql_query(SORT_DESC, engine)


    else:
        data = pd.read_sql_query(ALL_MOVIES,engine)

    return render_template('body.html' ,posts=data)

    
    
@app.route('/movies/<int:movieId>', methods=['GET'])
def movie(movieId):
    ID = []
    ID.append(movieId)
    data = pd.read_sql_query(SINGLE_MOVIE, engine, params = ID)
    return render_template('body.html' ,posts=data)


@app.route('/db', methods=['POST'])
def databaseb():
    try:
        url = 'http://files.grouplens.org/datasets/movielens/'
        database = request.get_json(force=True)['source']
        url = url + database + '.zip'
        db_insert.get_dataset(url)
        return "Database updated succesfully"
    except:
        return "Failed to update database"

if __name__ == '__main__':
   app.run(debug = True)