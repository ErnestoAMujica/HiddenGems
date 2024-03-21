import requests, os

from flask import Flask, jsonify, session, url_for, redirect, request
from flask_cors import CORS

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

#API calling things, create your Spotify app on the dev portal and copy the info here
#(Or use provided one i sent in discord)
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8080/api/callback'

#Scope permissions, add more permissions to the list as necessary when adding features
scope = 'playlist-read-private, playlist-modify-public, playlist-modify-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)
#This was in the old version idk if we're using this
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
CORS(app)

@app.route("/api/auth")
def auth():
    #If we don't have an auth token, redirect them to the auth url
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        temp = redirect(auth_url)
        print("TEMP: ",temp)
        #This was also in the old version
        #return jsonify({
         #   'link': auth_url
        #})

        return temp
    
    #If we are auth'd, display playlists
    return redirect(url_for('get_playlists'))    

@app.route('/api/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))



@app.route('/api/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    playlists = sp.current_user_playlists()
    
    dog_string = 'https://cdn.discordapp.com/attachments/1182080048178679869/1220095988879065188/poopy.jpg?ex=660db1f0&is=65fb3cf0&hm=13afc196e7f6b4bc6c123c22c6ed462d5d11e2aa41da78987285ab98a79bc90e&'
    
    playlists_info_2 = [
        [pl['name'], pl['external_urls']['spotify'],pl['images'][0]['url']] if len(pl['images']) > 0 
        else [pl['name'], pl['external_urls']['spotify'],dog_string] for pl in playlists['items']
        ]
    
    playlists_html = '<br>'.join([f'{name}: {url} <br> <img src="{image_url}" alt="lmao">' for name, url, image_url in playlists_info_2])
    return playlists_html


@app.route('/api/get_recs')
def get_recommendations():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
     #Grabs current users first playlist listed
    playlistTest = playlists['items'][0]
    songID = sp.playlist_items(playlistTest['id'])
    #Fills up songList based on the track ID of the songs in the playlist
    songList= []
    for pl in songID['items']:
        songList.append(pl['track']['id'])
    #Using the songList we got from the playlist, populates recsongList with recommendations
    recsongList = sp.recommendations(seed_tracks=songList)
    #Grabs the ID for the tracks in our new recommendation list
    track_ids = [track['id'] for track in recsongList['tracks']]
    #We need the user ID, so grabbing this now
    currUser = sp.current_user()
    userID = currUser['id']
    #Creates the initial playlist
    sp.user_playlist_create(userID,'grompula', public=False, description = "goaty schwab")
    #Updates the playlist variable to include the one 
    playlists = sp.current_user_playlists()
    #Grabs the playlist ID
    playlistEdit = (playlists['items'][0]['id'])
    #Adds the tracks to the playlist
    sp.user_playlist_add_tracks(userID, playlistEdit, track_ids, position=None)
    return
    
    

@app.route('/api/logout')
def logout():

    #Clears session id, sends them to reauth. Change landing to a login page instead eventually
    session.clear()
    return redirect(url_for('auth'))

@app.route("/api/home", methods= ['GET'])
def home():
    
    return jsonify({
        'message': "im spongebob",
        'list': ['Hidden Gem #1', 'Hidden Gem #2', 'Hidden Gem #3']
        
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
#Server run command is python3 server.py 
# http://localhost:8080/api/home