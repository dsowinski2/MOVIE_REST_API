import urllib.request
from io import BytesIO

import pandas as pd
from zipfile import ZipFile
from sqlalchemy import create_engine
import re
from odo import odo

from db import db, movies, links, tags, ratings
engine = create_engine('sqlite:///site.db')
db.drop_all()
db.create_all()


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






def get_dataset(file_url):

    url = urllib.request.urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.read()))
    zip_names = zipfile.namelist()
    zip_names.pop(0)
    for file_name in zip_names:
        if '.csv' in file_name:
            zipfile.open(file_name)
            data = pd.read_csv(zipfile.open(file_name), sep=',')
            print("maka0")
            if get_filename(file_name) == 'movies':
                data['year'] = get_year(data['title'])
            if get_filename(file_name) == 'links':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
            if get_filename(file_name) == 'tags':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
            if get_filename(file_name) == 'ratings':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
            destination = 'sqlite:///site.db::' + get_filename(file_name)
            print("maka")
            odo(data, destination)
            print("maka3")

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
            
