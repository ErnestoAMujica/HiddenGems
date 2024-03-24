import requests, os, datetime

from flask import Flask, jsonify, session, url_for, redirect, request
from flask_cors import CORS

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

#API keys, create your Spotify app on the dev portal and copy the info here
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8080/api/callback'

#Scope permissions, add more permissions to the list as necessary when adding features
scope = 'playlist-read-private, playlist-modify-public, playlist-modify-private'

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)
CORS(app)

@app.route("/api/auth")
def auth():

    if not sp_oauth.validate_token(sp_oauth.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        print("sending auth url")
        return jsonify({
            'link': auth_url
        })
    
    #If we are auth'd, go to main page
    print("redirecting to main")
    return jsonify({
            'link': 'http://localhost:3000/pages/main'
        })

@app.route('/api/callback')
def callback():

    if not sp_oauth.validate_token(sp_oauth.get_cached_token()):
        sp_oauth.get_access_token(code=request.args['code'])

    return redirect('http://localhost:3000/pages/main')

@app.route('/api/get_playlists')
def get_playlists():
    #if not sp_oauth.validate_token(cache_handler.get_cached_token()):
    if not sp_oauth.validate_token(sp_oauth.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    playlists = sp.current_user_playlists()
    
    default_image = 'https://shorturl.at/belHL'
    #default_image = 'https://shorturl.at/fgNP0'    
    playlists_info_2 = [
        [pl['name'], pl['external_urls']['spotify'],pl['images'][0]['url']] if len(pl['images']) > 0 
        else [pl['name'], pl['external_urls']['spotify'],default_image] for pl in playlists['items']
        ]
    
    playlists_html = '<br>'.join([f'{name}: {url} <br> <img src="{image_url}" alt="lmao">' for name, url, image_url in playlists_info_2])
    playlists_html += '<br><a href="http://localhost:8080/api/get_recs"> <button>Get Recommendations</button> </a>'
    return playlists_html


@app.route('/api/get_playlists_details')
def get_playlists_details():

    playlists_items = sp.current_user_playlists()['items']

    playlist_names = [iter['name'] for iter in playlists_items]
    playlist_ids = [iter['id'] for iter in playlists_items]

    default_image = 'https://shorturl.at/belHL'
    playlist_imagelinks = [iter['images'][0]['url'] if len(iter['images']) > 0 
                           else default_image for iter in playlists_items]
    
    return jsonify({
        'playlist_names': playlist_names,
        'playlist_ids': playlist_ids,
        'playlist_imagelinks' : playlist_imagelinks
    })


    '''

    #Shortened url :)
    default_image = 'https://shorturl.at/fgNP0'
    
    playlists_info_2 = [
        [pl['name'], pl['external_urls']['spotify'],pl['images'][0]['url']] if len(pl['images']) > 0 
        else [pl['name'], pl['external_urls']['spotify'], default_image] for pl in playlists['items']
        ]
    
    playlists_html = '<br>'.join([f'{name}: {url} <br> <img src="{image_url}" alt="lmao">' for name, url, image_url in playlists_info_2])
    return playlists_html
    '''

@app.route('/api/get_recs')
def get_recommendations():

    if not sp_oauth.validate_token(sp_oauth.get_cached_token()):
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
    sp.user_playlist_create(userID,'Recommended Playlist', public=False, description = "Hidden Gems Playlist")
    #Updates the playlist variable to include the one 
    playlists = sp.current_user_playlists()
    #Grabs the playlist ID
    playlistEdit = (playlists['items'][0]['id'])
    #Adds the tracks to the playlist
    sp.user_playlist_add_tracks(userID, playlistEdit, track_ids, position=None)
    recs_html = '<bR>Playlist added to account<br>'
    return recs_html
        

@app.route('/api/logout')
def logout():

    #Clears session id, sends them to reauth. Change landing to a login page instead eventually
    session.clear()
    return redirect(url_for('home'))

@app.route("/api/home", methods= ['GET'])
def home():
    return redirect('http://localhost:3000/')
    

#All hail our great lord
@app.route("/api/spongebob", methods= ['GET'])
def spongebob():
    
    return jsonify({
        'message': "im spongebob",
        'list': ['Hidden Gem #1', 'Hidden Gem #2', 'Hidden Gem #3']
        
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)