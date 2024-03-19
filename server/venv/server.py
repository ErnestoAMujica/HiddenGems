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
scope = 'playlist-read-private'

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

CORS(app)

@app.route("/api/auth")
def auth():
    #If we don't have an auth token, redirect them to the auth url
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        temp = redirect(auth_url)
        print("TEMP: ",temp)
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

    #Collects user playlist data and compiles them into html. Temporary and should def be changed
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url, in playlists_info])
    
    return playlists_html

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