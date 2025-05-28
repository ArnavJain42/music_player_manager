from flask import Flask, render_template, request, redirect, url_for,jsonify
from models import (
    create_tables, add_song, get_all_songs, search_songs,
    get_all_playlists, create_user_if_not_exists, create_playlist
)
from models import add_song_to_playlist
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
create_tables()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_video_url(query):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 1
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    if data.get("items"):
        video_id = data["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

# Example Flask route
@app.route('/youtube_link')
def youtube_link():
    title = request.args.get('title', '')
    artist = request.args.get('artist', '')
    query = f"{title} {artist}"
    video_url = get_youtube_video_url(query)
    if video_url:
        return jsonify({"url": video_url})
    else:
        return jsonify({"error": "No video found"}), 404

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



@app.route('/confirm_add_song', methods=['POST'])
def confirm_add_song():
    playlist_id = int(request.form['playlist_id'])
    song_id = int(request.form['song_id'])
    add_song_to_playlist(playlist_id, song_id)
    return redirect(url_for('playlists'))

@app.route('/add_song_to_playlist/<int:playlist_id>', methods=['GET', 'POST'])
def show_add_song_to_playlist(playlist_id):
    if request.method == 'POST':
        query = request.form['query']
        results = search_songs(query)
        return render_template('add_to_playlist.html', songs=results, playlist_id=playlist_id, query=query)
    return render_template('add_to_playlist.html', songs=[], playlist_id=playlist_id, query='')



if __name__ == '__main__':
    app.run(debug=True)