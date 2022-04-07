import flask
import mysql
import spotipy
import os
from flask import Flask, session, request, url_for, redirect, render_template, flash
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy.util
import sqlite3
from mysql_connection import MySqlConnection
from random import randint
from libraries.send_email import EmailClient


minimum = 100000
maximum = 999999

send_grid_api_key = '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'

# Creates Flask web app
app = Flask(__name__)

os.environ['SPOTIPY_CLIENT_ID'] = "57cdacfda2cd4ab9ac30bac8e172e9df"
os.environ['SPOTIPY_CLIENT_SECRET'] = "a5a8f8f0c4f14715accc45326445b3aa"
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

dbconn = MySqlConnection()

def add_track_to_db(name, img, artist, album):
    query = """INSERT IGNORE INTO tracks(name, img_url, artist_name, album_name)
                VALUES(%(name)s, %(img)s, %(artist)s, %(album)s);"""

    args = {
            'name': name,
            'img': img,
            'artist': artist,
            'album': album
           }
    dbconn.query(query, args)

spotify_db = mysql.connector.connect(
            user='root',
            password='hotdog4567',
            host='localhost',
            port='3306',
            database='spotifyapp'
        )

def get_tracks_from_db():
    query = """SELECT * FROM tracks;"""
    args = {}
    tracks = dbconn.get_all(query, args)
    return tracks

# def in_database():

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        sql = "INSERT INTO loginfo (username, password, email_id, verification) VALUES (%(username)s, %(password)s, %(email_id)s, %(verification)s)"

        verification = randint(minimum, maximum)

        args = {
            'username': username,
            'password': password,
            'email_id': email,
            'verification': verification
        }
        dbconn.query(sql, args)
        EmailClient.send_email(email, 'aaron.roche4567@gmail.com', 'Sign Up Verification', 'Hi there, your code is: %s'%verification)
        return redirect(url_for('top_ten'))
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/top_ten')
def top_ten():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_tracks(limit=10, offset=0, time_range='medium_term')

    for track in top_result.get('items'):
        add_track_to_db(name=track.get('name'),
                        img=track.get('album').get('images')[0].get('url'),
                        artist=track.get('artists')[0].get('name'),
                        album=track.get('album').get('name'))


    return render_template('tracks.html', tracks=top_result.get('items'))


@app.route('/top_ten_from_db')
def top_ten_from_db():
    tracks = get_tracks_from_db()
    return render_template('tracksdb.html', tracks=tracks)


@app.route('/top_twenty')
def top_twenty():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')

    return render_template('tracks.html', tracks=top_result.get('items'))


@app.route('/top_fifty')
def top_fifty():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    print(top_result)
    return render_template('tracks.html', tracks=top_result.get('items'))


@app.route('/artists')
def artists_top_ten():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_artists(limit=10, offset=0, time_range='medium_term')
    return render_template('artists.html', artists=top_result.get('items'))


@app.route('/artists_top_five')
def artists_top_five():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_artists(limit=5, offset=0, time_range='medium_term')
    return render_template('artists.html', artists=top_result.get('items'))


@app.route('/artists_top_twenty')
def artists_top_twenty():
    scope = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_result = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
    return render_template('artists.html', artists=top_result.get('items'))


@app.route('/albums')
def my_form():
    return render_template('albums.html')


@app.route('/albums', methods=['POST'])
def my_form_post():
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    album_name = request.form['text']
    results = sp.search(q="album:" + album_name, type="album")
    album_id = results['albums']['items'][0]['uri']
    album_tracks = sp.album_tracks(album_id)

    track_names = album_tracks['items']

    album_img_url = results['albums']['items'][0]['images'][1]['url']
    list_of_tracks = []
    for i in track_names:
        list_of_tracks.append(i['name'])

    conn = sqlite3.connect('spotifyapp.db')
    c = conn.cursor()
    id_num = 'select max (album_id) + 1 from Album'
    c.execute('INSERT INTO Album VALUES (?, ?)', [c.lastrowid, album_name])
    #c.execute('INSERT INTO tracks VALUES (?, ?)', [c.lastrowid + 1, i])

    conn.commit()
    c.close()
    conn.close()

    return render_template('albums.html', list_of_tracks=list_of_tracks, album_img_url=album_img_url)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8888)
