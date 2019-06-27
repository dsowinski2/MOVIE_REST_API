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
import SQL_queries


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
engine = create_engine('sqlite:///site.db')




app = Flask(__name__)
@app.route('/movies', methods=['GET'])
def movies():

    sort  = request.args.get('sort')
    year  = request.args.getlist('year')
    tag = request.args.getlist('tag')

    if tag:
        if len(tag) == 1:
            data = pd.read_sql_query(SQL_queries.ONE_TAG, engine, params=tag)
            
        else:
            data = pd.read_sql_query(SQL_queries.TWO_TAGS, engine, params=tag)
    elif year:
        
        data = pd.read_sql_query(SQL_queries.GET_PRODUCTION_YEAR, engine, params = year)

    elif sort:
        if sort == '-year':
            data = pd.read_sql_query(SQL_queries.SORT_ASC, engine)
        else:
            data = pd.read_sql_query(SQL_queries.SORT_DESC, engine)


    else:
        data = pd.read_sql_query(SQL_queries.ALL_MOVIES,engine)

    return render_template('body.html' ,posts=data)

    
@app.route('/movies/<int:movieId>', methods=['GET'])
def movie(movieId):
    ID = []
    ID.append(movieId)
    data = pd.read_sql_query(SQL_queries.SINGLE_MOVIE, engine, params = ID)
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
        return "Failed to updated database"
if __name__ == '__main__':
   app.run(debug = True)