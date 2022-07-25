from http import client
from django.utils import timezone
from datetime import timedelta, datetime
from requests import Request, post, get
from .models import (
    Fav_Genres,
    Refresh_Token,
    Access_Token,
    Recent_Songs,
    Fav_Songs,
    Fav_Artists,
    Playlists,
)
from dotenv import load_dotenv
from django.db.models import Q
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:8888/spotify/callback/"


def getRefreshToken(refresh_token):
    """
    This function send a request to spotify in order to get an access token by using refresh_token.

    Args:
        refresh_token (int)

    Returns:
        access_token (int)
    """
    # request to spotify
    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    ).json()

    access_token = response.get("access_token")

    return access_token


def getAccessToken(user):
    """
    It returns a new access token for the given user
    Also, it deletes the old access token.

    Args:
        user (models.MusicorpusUser):

    Returns:
        access_token (int)
    """

    # let's delete the old accessToken if it exists:
    try:
        oldAccessToken = Access_Token.objects.filter(user=user)
        oldAccessToken.delete()
    except:
        pass
    refreshTokenQuery = Refresh_Token.objects.get(user=user)
    refreshToken = refreshTokenQuery.refresh_token

    # now we need to get a new refresh token:
    accessToken = getRefreshToken(refreshToken)

    # add new token into db:
    newAccessToken = Access_Token.objects.create(user=user, access_token=accessToken)
    newAccessToken.save()

    return accessToken


def getFavSongsFromSpotify(accessToken, user, term):
    """
    It returns the fav songs of the given users according to the given term:
    Term should be:
        'short_term' -> 4 weeks
        'medium_term' -> 6 months
        'long_term' -> ~ years

    Args:
        accessToken (string): Access token of the user
        user (models.MusicorpusUser)
        term (string):

    Returns:
        list<dict>: [{name:"..", link:".."},{}...]
    """
    favSongs = []

    favSongRequest = get(
        f"https://api.spotify.com/v1/me/top/tracks?time_range={term}&limit=5&offset=0",
        headers={"Authorization": "Bearer " + accessToken},
    ).json()

    for song in favSongRequest["items"]:
        newSong = {}
        newSong["name"] = song["name"]
        newSong["link"] = song["external_urls"]["spotify"]
        favSongs.append(newSong)

    # if this term exists in db, we need to delete it.
    try:
        oldFavSongs = Fav_Songs.objects.get(user=user, term=term)
        oldFavSongs.delete()

    except:
        pass

    topSongsDB = Fav_Songs.objects.create(
        user=user,
        term=term,
        song1=favSongs[0]["name"],
        song1_link=favSongs[0]["link"],
        song2=favSongs[1]["name"],
        song2_link=favSongs[1]["link"],
        song3=favSongs[2]["name"],
        song3_link=favSongs[2]["link"],
        song4=favSongs[3]["name"],
        song4_link=favSongs[3]["link"],
        song5=favSongs[4]["name"],
        song5_link=favSongs[4]["link"],
    )

    topSongsDB.save()

    return favSongs


def getFavArtistsFromSpotify(accessToken, user, term):
    """
    It returns the fav artists of the given users according to the given term:
    Term should be:
        'short_term' -> 4 weeks
        'medium_term' -> 6 months
        'long_term' -> ~ years

    Args:
        accessToken (string): Access token of the user
        user (models.MusicorpusUser)
        term (string):

    Returns:
        list<dict>: [{name:"..", link:".."},{}...]
    """
    favArtists = []

    favArtistRequest = get(
        f"https://api.spotify.com/v1/me/top/artists?time_range={term}&limit=5&offset=0",
        headers={"Authorization": "Bearer " + accessToken},
    ).json()

    for artist in favArtistRequest["items"]:
        newArtist = {}
        newArtist["name"] = artist["name"]
        newArtist["link"] = artist["external_urls"]["spotify"]
        favArtists.append(newArtist)

    # if this term exists in db, we need to delete it.
    try:
        oldFavArtists = Fav_Artists.objects.get(user=user, term=term)
        oldFavArtists.delete()

    except:
        pass

    topArtistDB = Fav_Artists.objects.create(
        user=user,
        term=term,
        artist1=favArtists[0]["name"],
        artist1_link=favArtists[0]["link"],
        artist2=favArtists[1]["name"],
        artist2_link=favArtists[1]["link"],
        artist3=favArtists[2]["name"],
        artist3_link=favArtists[2]["link"],
        artist4=favArtists[3]["name"],
        artist4_link=favArtists[3]["link"],
        artist5=favArtists[4]["name"],
        artist5_link=favArtists[4]["link"],
    )

    topArtistDB.save()

    return favArtists


def getFavGenresFromSpotify(accessToken, user, term):
    """
    It returns the fav genres of the given users according to the given term:
    Term should be:
        'short_term' -> 4 weeks
        'medium_term' -> 6 months
        'long_term' -> ~ years

    Args:
        accessToken (string): Access token of the user
        user (models.MusicorpusUser)
        term (string):

    Returns:
        list<dict>: [{name:"..", link:".."},{}...]
    """
    favArtistRequest = get(
        f"https://api.spotify.com/v1/me/top/artists?time_range={term}&limit=50&offset=0",
        headers={"Authorization": "Bearer " + accessToken},
    ).json()

    fav_genre = {}

    for artist in favArtistRequest["items"]:
        for genre in artist["genres"]:
            if genre in fav_genre:
                fav_genre[genre] += 1
            else:
                fav_genre[genre] = 1

    fav_genre_sort = sorted(fav_genre, key=fav_genre.get, reverse=True)

    firstFav = fav_genre_sort[0]
    secondFav = fav_genre_sort[1]
    thirdFav = fav_genre_sort[2]
    fourthFav = fav_genre_sort[3]
    fifthFav = fav_genre_sort[4]

    try:
        oldFavGenres = Fav_Genres.objects.get(user=user, term=term)
        oldFavGenres.delete()

    except:
        pass

    topGenresDB = Fav_Genres.objects.create(
        user=user,
        term=term,
        genre1=firstFav,
        genre2=secondFav,
        genre3=thirdFav,
        genre4=fourthFav,
        genre5=fifthFav,
    )
    topGenresDB.save()
    return "Ok"


def getRecentSongsFromSpotify(user, accessToken):
    """
    It checks the user's recenlty played songs.
    It checks the Recent_Songs table for the given user.
    If it can find a row, the time of this row will be used in request.
    Afterwards it will add new songs into db:

    Args:
        user (models.MusicorpusUser):
        accessToken (int):
    """

    #
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"

    try:
        # if the db do not have any row for this user it will give an error so to prevent it i am using try except block
        # also if it is the first time that we add recent songs, we will not add time limit

        # I get the rows with descending order of the time
        recentSongsDBQuery = Recent_Songs.objects.filter(user=user).order_by("-time")

        # so first element will be the newest added song:
        latestDate = recentSongsDBQuery[0].time
        latestDateMiliseconds = int(latestDate.timestamp() * 1000)

        url = url + f"&after={latestDateMiliseconds}"

    except:
        pass

    recentSongs = get(url, headers={"Authorization": "Bearer " + accessToken}).json()

    for recentSong in recentSongs["items"]:
        newSong = Recent_Songs.objects.create(
            song=recentSong["track"]["name"],
            song_link=recentSong["track"]["external_urls"]["spotify"],
            user=user,
            artist=recentSong["track"]["artists"][0]["name"],
            artist_link=recentSong["track"]["artists"][0]["external_urls"]["spotify"],
            duration=recentSong["track"]["duration_ms"],
        )
        newSong.save()

    return "Ok"


def getPlaylistsFromSpotify(user, accessToken):
    """
    It returns the four playlists of the given user:

    Args:
        user (models.MusicorpusUser)
        accessToken (string): Access token of the user

    Returns:
        null:
    """

    playlistRequest = get(
        f"https://api.spotify.com/v1/me/playlists?limit=5&offset=0",
        headers={"Authorization": "Bearer " + accessToken},
    ).json()

    # if playlists that belongs to this user exist in db, delete it
    try:
        oldPlaylists = Playlists.objects.filter(user=user)
        oldPlaylists.delete()

    except:
        pass

    for playlist in playlistRequest["items"]:
        new_playlist = Playlists.objects.create(
            user=user,
            name=playlist["name"],
            link=playlist["external_urls"]["spotify"],
            photo_url=playlist["images"][0]["url"],
            id_spotify= playlist["id"]
        )
        new_playlist.save()
    return

def getTracksOfPlaylists(playlist_id, accessToken):
    tracks = []

    trackRequest = get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name%2Cartists%2Cexternal_urls(spotify)%2Chref%2Calbum(external_urls%2Cimages)))&limit=50&offset=0",
        headers={"Authorization": "Bearer " + accessToken},
    ).json()
    for track in trackRequest["items"]:
        new_track = {}
        new_track["link"]=track["track"]["external_urls"]["spotify"]
        new_track["name"] = track["track"]["name"]
        new_track["artist_name"]=track["track"]["artists"][0]["name"]
        new_track["artist_link"]=track["track"]["artists"][0]["external_urls"]["spotify"]
        new_track["photo"]=track["track"]["album"]["images"][0]["url"]
        tracks.append(new_track)

    return {"tracks":tracks, "id_spotify":playlist_id}

