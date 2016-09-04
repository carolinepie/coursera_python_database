# purpose: to read an XML file exported from iTunes playlist
# and produce a properly orgranized database with:
# Track, Album, Genre and Artist

# import required libraries
import xml.etree.ElementTree as ET
import sqlite3

# helper function: extract: returns string in given field
# from given xml_tree, returns None if the field being checked is not present
def extract(xml_tree, field):
    now = False
    for element in xml_tree:
        if now: return element.text
        if element.tag == 'key' and element.text == field :
            now = True
    return None

# open file and extract XML
fname = raw_input('Enter file name: ').strip()
tree = ET.parse(fname)

# set up table, remember to reset data for each run!
connection = sqlite3.connect('lib.sqlite')
cur = connection.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# print 'before loop'


songs = tree.findall('dict/dict/dict')

# for each song
for song in songs:
    # check whether is a valid song:
    track_id = extract(song, 'Track ID')
    artist = extract(song, 'Artist')
    album = extract(song, 'Album')
    genre = extract(song, 'Genre')
    if track_id is None or artist is None or album is None or genre is None: 
        continue
        
    # fill in Artists and Genre
    cur.execute('''
    INSERT OR IGNORE INTO Artist (name) VALUES (?)
    ''', (artist, ))
    
    cur.execute('''
    INSERT OR IGNORE INTO Genre (name) VALUES (?)
    ''', (genre, ))
        
    # fill in Album and Track
    cur.execute('SELECT id FROM Artist WHERE name = ? ',
    (artist, ))
        
    artist_id = cur.fetchone()[0]
        
    cur.execute('SELECT id FROM Genre WHERE name = ? ',
    (genre, ))
        
    genre_id = cur.fetchone()[0]
        
    cur.execute ('''
    INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)
    ''', (album, artist_id))
        
    cur.execute('SELECT id FROM Album WHERE title = ? ',
    (album, ))
        
    album_id = cur.fetchone()[0]        
    cur.execute ('''
    INSERT OR REPLACE INTO Track 
    (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)
    ''',
        (extract(song, 'Name'), album_id, genre_id,
        extract(song, 'Total Time'), extract(song, 'Rating'),
        extract(song, 'Track Count')))
        

# print 'after loop'        

connection.commit()
    
cur.close()   
