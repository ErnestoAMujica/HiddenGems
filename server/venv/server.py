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

default_image = 'https://shorturl.at/belHL'

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
    playlist_imagelinks = []
    for iter in playlists_items:
        if iter['images'] is not None and len(iter['images']) > 0:
            playlist_imagelinks.append(iter['images'][0]['url'])
        else:
            playlist_imagelinks.append(default_image)
    #playlist_imagelinks = [iter['images'][0]['url'] if len(iter['images']) > 0 
     #                    else default_image for iter in playlists_items]
    
    
    return jsonify({
        'playlist_names': playlist_names,
        'playlist_ids': playlist_ids,
        'playlist_imagelinks' : playlist_imagelinks
    })

@app.route('/api/create_playlist_from_tracks', methods=['POST'])
def create_playlist_from_tracks():

    response = request.get_json(force=True)
    track_ids = response['selected_tracks']
    playlist_name = response['playlist_name']
    if playlist_name is None or len(playlist_name) < 1:
        playlist_name = 'Recommended Playlist'
    currUser = sp.current_user()
    userID = currUser['id']
    print('in fetch')
    created_playlist = sp.user_playlist_create(userID, playlist_name, public=False, description = "Hidden Gems Playlist")
    playlist_id = (created_playlist['id'])
    # playlist_id = ('12bKze0wXhr29V1LlQSMrl')
    playlist_link = 'http://open.spotify.com/playlist/' + playlist_id
    sp.user_playlist_add_tracks(userID, playlist_id, track_ids, position=None)
    print(playlist_id)
    return jsonify({
        'playlist_id': playlist_id
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

# @app.route('/api/me/tracks/', methods=['GET'])
# def check_saved_tracks():
#     response = request.get_json()
#     liked_songs = response['selected_playlist_id']
#     playListItems = sp.playlist_items(liked_songs)['items']
#     for track in playListItems:
#         print(track['track']['name'])
#     return jsonify({
#         'liked_songs': playListItems
#     })

@app.route('/api/get_recommendations', methods=['POST'])
def get_recommendations():
    response = request.get_json()
    selected_playlist_id = response['selected_playlist_id']
    playlistItems = sp.playlist_items(selected_playlist_id)['items']
    recsList = []
    savedTracks = []
    while len(playlistItems) > 0:
        songList = []
        counter = 0
        for pl in playlistItems:
            if counter == 5:
                break
            songList.append(pl['track']['id'])
            counter+=1
        recsList += sp.recommendations(seed_tracks=songList)['tracks'][:5] #whatever this number is is how much we're taking from the 20 songs
        playlistItems = playlistItems[5:]
        # compare recsList with liked songs and remove duplicates
        # should have basic logic for removing duplicates, and this is the right method but I'm getting a 403 forbidden when I test it in postman and also here, so maybe if someone else could test. thanks
        # likedSongs = sp.current_user_saved_tracks()
        # recsList = [track for track in recsList if track['id'] not in likedSongs]
        
    
    track_names = [track['name'] for track in recsList]
    track_artists = [track['artists'][0]['name'] for track in recsList]
    track_imagelinks = [track['album']['images'][0]['url'] if len(track['album']['images']) > 0
                        else default_image for track in recsList]
    track_ids = [track['id'] for track in recsList]
    
    #print(track_names, track_artists, track_imagelinks, track_ids)
    return jsonify({
        'track_names': track_names,
        'track_artists': track_artists,
        'track_imagelinks' : track_imagelinks,
        'track_ids' : track_ids
    })
    
    
# Old recs algorithm part 2 (the one goatnesto made)
# @app.route('/api/get_recommendations', methods=['POST'])
# def get_recommendations():
#     response = request.get_json()
#     selected_playlist_id = response['selected_playlist_id']
#     playlistItems = sp.playlist_items(selected_playlist_id)['items']
#     songList = []
#     counter = 0
#     for pl in playlistItems:
#         if counter == 5:
#             break
#         songList.append(pl['track']['id'])
#         counter+=1
#     print(songList)
#     recsList = sp.recommendations(seed_tracks=songList)['tracks']
#     print(recsList)
#     track_names = [track['name'] for track in recsList]
#     track_artists = [track['artists'][0]['name'] for track in recsList]
#     track_imagelinks = [track['album']['images'][0]['url'] if len(track['album']['images']) > 0
#                         else default_image for track in recsList]
#     track_ids = [track['id'] for track in recsList]

#     print(track_names, track_artists, track_imagelinks, track_ids)
#     return jsonify({
#         'track_names': track_names,
#         'track_artists': track_artists,
#         'track_imagelinks' : track_imagelinks,
#         'track_ids' : track_ids
#     })

@app.route('/api/get_recs_old')
def get_recommendations_old():

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
    os.remove("./.cache")
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