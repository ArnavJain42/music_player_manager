from db_config import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Songs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        artist VARCHAR(255),
        album VARCHAR(255)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Playlists (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PlaylistSongs (
        playlist_id INT,
        song_id INT,
        FOREIGN KEY (playlist_id) REFERENCES Playlists(id),
        FOREIGN KEY (song_id) REFERENCES Songs(id),
        PRIMARY KEY (playlist_id, song_id)
    );
    """)

    conn.commit()
    conn.close()

def add_song(title, artist, album):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Songs (title, artist, album) VALUES (%s, %s, %s)", (title, artist, album))
    conn.commit()
    conn.close()

def get_all_songs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Songs")
    results = cursor.fetchall()
    conn.close()
    return results

def search_songs(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Songs WHERE title LIKE %s OR artist LIKE %s", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_playlists():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.name, u.username FROM Playlists p
        JOIN Users u ON p.user_id = u.id
    """)
    playlists = cursor.fetchall()

    for playlist in playlists:
        cursor.execute("""
            SELECT s.title, s.artist, s.album FROM PlaylistSongs ps
            JOIN Songs s ON ps.song_id = s.id
            WHERE ps.playlist_id = %s
        """, (playlist['id'],))
        playlist['songs'] = cursor.fetchall()

    conn.close()
    return playlists

def create_user_if_not_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO Users (username) VALUES (%s)", (username,))
        conn.commit()
    conn.close()

def create_playlist(username, playlist_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        cursor.execute("INSERT INTO Playlists (user_id, name) VALUES (%s, %s)", (user_id, playlist_name))
        conn.commit()
    conn.close()