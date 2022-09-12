from flask import Flask, render_template
import random
import os
#Retrieves spotify data from the Spotify API as a JSON object to be used with Python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

#Turns Python into Web App
app = Flask(__name__)





@app.route("/")
def home():
    """Home Page"""
    return render_template('desktop-1.html')

@app.route("/YourRecs/")
def RenderRecommendations():
    """Renders the recommendations in HTML"""
    r1, r2, r3, r4, r5, r6, r7, r8 = getRecommendations()

    return render_template('RecommendationsPage.html', rec1=r1, rec2=r2, rec3=r3, rec4=r4, rec5=r5, rec6=r6, rec7=r7, rec8=r8)


def getRecommendations():
    os.environ['SPOTIPY_CLIENT_ID'] = "ca016b7eeaff404697381f6f9aea32a0"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "2a0f5710a11b4fe58b2f18c2e74cbe03"
    os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:9090"

    #sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    scope = "user-library-read " "user-top-read " "user-read-recently-played " "user-read-playback-state "

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    print(sp)


    """
    #used to get user data
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="56e38026bbc84e3ca3b71ff14ada6a3c",
                                                   client_secret="ec745f399faa4b09b119e51d06a18583",
                                                   redirect_uri="http://localhost:9090",
                                                   scope="user-library-read "
                                                         "user-top-read "
                                                         "user-read-recently-played "
                                                         "user-read-playback-state"))

    """

    #Gets User's saved tracks
    saved_tracks = sp.current_user_saved_tracks()
    trackList = []
    for track in saved_tracks['items']:
        trackList.append(track['track']['uri'])




    dance = 0
    energy = 0
    l = 0
    m = 0
    s = 0
    a = 0
    intr = 0
    liv = 0
    v = 0
    t = 0
    feat = sp.audio_features(tracks=trackList)
    for f in feat:
        dance += f['danceability']
        energy += f['energy']
        l += f['loudness']
        m += f['mode']
        s += f['speechiness']
        a += f['acousticness']
        intr += f['instrumentalness']
        liv += f['liveness']
        v += f['valence']
        t += f['tempo']
    danceavg = dance / len(trackList)
    energyavg = energy / len(trackList)
    loudavg = l / len(trackList)
    speechavg = s / len(trackList)
    acousticavg = a / len(trackList)
    instrumentavg = intr / len(trackList)
    liveavg = liv / len(trackList)
    valenceavg = v / len(trackList)
    tempoavg = t / len(trackList)


    topArtists = sp.current_user_top_artists()
    genres = []
    for artist in topArtists['items']:
        for art in artist['genres']:
            genres.append(art)


    firstFiveTracks = random.sample(trackList, 5)


    recommendations = sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=firstFiveTracks, limit=50,
                                         country='US',
                                         target_danceability=danceavg,
                                         target_energy=energyavg,
                                         target_loudness=loudavg,
                                         target_speechiness=speechavg,
                                         target_acousticness=acousticavg,
                                         target_instrumentalness=instrumentavg,
                                         target_liveness=liveavg,
                                         target_valence=valenceavg,
                                         target_tempo=tempoavg,
                                         max_popularity=33,
                                         target_popularity=1)

    #Filters out songs with Artist popularity above 33
    #
    #

    #prints names of tracks (testing)
    for t in recommendations['tracks']:
        #print(t['name'])
        print(t['artists'])

    #Gets spotify url's of tracks in recommendation list
    rec = []
    for item in recommendations['tracks']:
        rec.append("https://open.spotify.com/embed/track/" + item['id'])


    return random.sample(rec, 8)


if __name__ == "__main__":
    app.run(port=5000)
