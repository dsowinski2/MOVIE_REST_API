import urllib.request
from io import BytesIO

import pandas as pd
from zipfile import ZipFile
from sqlalchemy import create_engine
import re
from db import db

from db import movies, links, tags, ratings

db.drop_all()
db.create_all()
engine = create_engine('sqlite:///site.db')

def get_filename(filename):
    filename = filename.split('/')
    filename = filename[1].split('.')
    return filename[0]

def get_year(data):
    date = []
    for i in data:
        year = re.findall(r"\((\d\d\d\d)\)",i)
        if year:
            date.append(int(year[0]))
        else:
            date.append(0)
    return date

def Load_Data(file_name):

    return data.tolist()


def get_dataset(file_url):
    #db.create_all()
    url = urllib.request.urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.read()))
    zip_names = zipfile.namelist()
    zip_names.pop(0)
    for file_name in zip_names:
        if '.csv' in file_name:
            print(file_name)
            zipfile.open(file_name)
            data = pd.read_csv(zipfile.open(file_name), sep=',')
            if get_filename(file_name) == 'movies':
                data['year'] = get_year(data['title'])
            data.to_sql(get_filename(file_name), con=engine, index=False, if_exists='replace')


            

    #db.session.commit()
    return 

'''
def get_dataset(file_url):
    classes = []
    for clazz in db.Model._decl_class_registry.values():
        classes.append(clazz)
    db.create_all()
    url = urllib.request.urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.read()))
    zip_names = zipfile.namelist()
    zip_names.pop(0)
    for file_name in zip_names:
        if '.csv' in file_name:
            print(file_name)


            zipfile.open(file_name) 
            data = pd.read_csv(zipfile.open(file_name), sep=',')
            if get_filename(file_name) == 'movies':
                data['year'] = get_year(data['title'])




            

    db.session.commit()
    return 

'''




#data.to_sql(get_filename(file_name), con=engine, if_exists='replace', index=False, index_label=[column.key for column in links.__table__.columns] )
#data.to_sql(get_filename(file_name), con=engine, if_exists='replace', index=False, schema='db')

'''
userId = row['userId'],
, timestamp = row['timestamp']
'''

'''
                            for index,row in data.iterrows():
                    movie = movies(movieId = row['movieId'] , title = row['title'], genres = row['genres'], year = row['year'])
                    db.session.add(movie)
            elif get_filename(file_name) == 'tags':
                for index,row in data.iterrows():
                    tag = tags( userId = row['userId'], movieId = row['movieId'], tag = row['tag'], timestamp = row['timestamp'])
                    db.session.add(tag)

            elif get_filename(file_name) == 'ratings':
                for index,row in data.iterrows():
                    rate = ratings(movieId = row['movieId'], rating = row['rating'])
                    db.session.add(rate)

            else:
                for index,row in data.iterrows():
                    link = links(movieId = row['movieId'], imdbId = row['imdbId'], tmdbId = row['tmdbId'])
                    db.session.add(link)
'''
            
