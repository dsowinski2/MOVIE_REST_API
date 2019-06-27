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
