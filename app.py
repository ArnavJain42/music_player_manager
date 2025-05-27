from flask import Flask, render_template, request, redirect, url_for
from models import (
    create_tables, add_song, get_all_songs, search_songs,
    get_all_playlists, create_user_if_not_exists, create_playlist
)

app = Flask(__name__)
create_tables()

@app.route('/')
def index():
    songs = get_all_songs()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        add_song(title, artist, album)
        return redirect(url_for('index'))
    return render_template('add_song.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = search_songs(query)
        return render_template('search.html', songs=results, query=query)
    return render_template('search.html', songs=[], query='')

@app.route('/playlists', methods=['GET'])
def playlists():
    data = get_all_playlists()
    return render_template('playlists.html', playlists=data)

@app.route('/create_playlist', methods=['POST'])
def create():
    username = request.form['username']
    playlist_name = request.form['playlist_name']
    create_user_if_not_exists(username)
    create_playlist(username, playlist_name)
    return redirect(url_for('playlists'))

if __name__ == '__main__':
    app.run(debug=True)