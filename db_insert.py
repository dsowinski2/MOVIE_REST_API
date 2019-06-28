import urllib.request
from io import BytesIO

import pandas as pd
from zipfile import ZipFile
from sqlalchemy import create_engine
import re

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


def get_dataset(file_url):
    url = urllib.request.urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.read()))
    zip_names = zipfile.namelist()
    zip_names.pop(0)
    for file_name in zip_names:
        if '.csv' in file_name:
            zipfile.open(file_name) 
            data = pd.read_csv(zipfile.open(file_name), sep=',')
            if get_filename(file_name) == 'movies':
                data['year'] = get_year(data['title'])
            data.to_sql(get_filename(file_name), con=engine, if_exists='replace')




#The presented section populate the database created in a db file with data from CSV files faster, but does not work on Heroku, you can try it locally.


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
            zipfile.open(file_name) 
            data = pd.read_csv(zipfile.open(file_name), sep=',')
            destination = 'sqlite:///site.db::' + get_filename(file_name)
            if get_filename(file_name) == 'movies':
                data['year'] = get_year(data['title'])
                dshape = discover(data)
                movies = odo(data, destination, dshape=dshape)
            elif get_filename(file_name) == 'tags':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
                dshape = discover(data)
                tags = odo(data, destination, dshape=dshape)
            elif get_filename(file_name) == 'links':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
                dshape = discover(data)
                links = odo(data, destination, dshape=dshape)
            elif get_filename(file_name) == 'ratings':
                data['index'] = list(range(1,data['movieId'].shape[0]+1))
                dshape = discover(data)
                ratings = odo(data, destination, dshape=dshape) 
    return (movies,tags,links,ratings)
'''