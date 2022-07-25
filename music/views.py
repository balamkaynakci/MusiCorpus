from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import (
    City,
    MusicorpusUser,
    Refresh_Token,
    Access_Token,
    Fav_Songs,
    Fav_Artists,
    User_Photo,
)
import json
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from requests import Request, post, get
from dotenv import load_dotenv, find_dotenv
import os
import random
import string
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .util_spotify import (
    getAccessToken,
    getFavSongsFromSpotify,
    getFavArtistsFromSpotify,
    getRecentSongsFromSpotify,
    getFavGenresFromSpotify,
    getPlaylistsFromSpotify,
    getTracksOfPlaylists,
)
from .util_server import (
    get_events,
    get_following,
    get_playlists,
    get_song_of_the_day,
    get_artist_of_the_day,
    get_listening_time,
    get_fav_songs_from_db,
    get_fav_artists_from_db,
    get_fav_genres_from_db,
    get_followers,
    follow,
    get_posts,
    create_post,
    get_listened_songs_number,
    get_listened_artists_number,
    get_profil_photo,
    get_listening_ratio_playlist,
    get_following_playlists,
    get_badge
)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from matplotlib import pyplot as plt


load_dotenv(find_dotenv())

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:8888/spotify/callback/"


class Index(View):
    """
    /
    Root file

    """

    def get(self, request):
        # if there is an authenticated user, lets redirect to main page.
        if request.user.id != None:
            return redirect("/main")

        return render(request, "index.html")


class AuthURL(APIView):
    """
    By using this user can reach the spotify's login page:

    Args:
        APIView (_type_): _description_
    """

    def get(self, request, format=None):
        scopes = "user-read-playback-state user-read-currently-playing user-follow-read user-read-recently-played user-read-playback-position user-top-read playlist-read-collaborative user-read-email user-read-private user-library-read"

        url = (
            Request(
                "GET",
                "https://accounts.spotify.com/authorize",
                params={
                    "scope": scopes,
                    "response_type": "code",
                    "redirect_uri": redirect_uri,
                    "client_id": client_id,
                },
            )
            .prepare()
            .url
        )

        return Response({"url": url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    """
    Spotify redirects the user this function

    Then, I sen
    """
    code = request.GET.get("code")
    error = request.GET.get("error")

    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    ).json()
    
    access_token = response.get("access_token")
    refresh_token = response.get("refresh_token")

    return redirect(
        f"/signup?access_token={access_token}&refresh_token={refresh_token}"
    )


class Profile(LoginRequiredMixin, View):
    redirect_field_name = "index"

    def get(self, request):
        user_id = request.user.id
        return redirect(f"/profile/{user_id}")


class ProfileOther(LoginRequiredMixin, View):
    redirect_field_name = "index"

    def get(self, request, pk):
        user = MusicorpusUser.objects.get(id=pk)
        # if users try to see their pages, we can redirect them to profile page.

        self_page = False
        if pk == request.user.id:
            self_page = True

        follow_status = False
        if user in get_following(request.user):
            follow_status = True

        """get_listened_songs_number(request.user)
        get_listened_artists_number(request.user)"""

        short_term_fav_songs = get_fav_songs_from_db(user, "short_term")
        medium_term_fav_songs = get_fav_songs_from_db(user, "medium_term")
        long_term_fav_songs = get_fav_songs_from_db(user, "long_term")

        short_term_fav_artists = get_fav_artists_from_db(user, "short_term")
        medium_term_fav_artists = get_fav_artists_from_db(user, "medium_term")
        long_term_fav_artists = get_fav_artists_from_db(user, "long_term")

        short_term_fav_genres = get_fav_genres_from_db(user, "short_term")
        medium_term_fav_genres = get_fav_genres_from_db(user, "medium_term")
        long_term_fav_genres = get_fav_genres_from_db(user, "long_term")
        artists_listened = get_listened_artists_number(user)

        songs_listened = get_listened_songs_number(user)
        listening_time = get_listening_time(user)
        print(listening_time)
        profil_photo_user = get_profil_photo(user)
        user_name = user.first_name
        user_playlists = get_playlists(user)
        badges = get_badge(user)

        profil_photo_request_user = get_profil_photo(request.user)
        name_request_user = request.user.first_name
        
        strFile = "./static/bar.jpg"
        if os.path.isfile(strFile):
            os.remove(strFile)   # Opt.: os.system("rm "+strFile)

        plt.bar(range(len(listening_time)), list(listening_time.values()), align='center')
        plt.savefig(strFile)

        return render(
            request,
            "profile.html",
            {
                "short_term_fav_songs": short_term_fav_songs,
                "medium_term_fav_songs": medium_term_fav_songs,
                "long_term_fav_songs": long_term_fav_songs,
                "short_term_fav_artists": short_term_fav_artists,
                "medium_term_fav_artists": medium_term_fav_artists,
                "long_term_fav_artists": long_term_fav_artists,
                "short_term_fav_genres": short_term_fav_genres,
                "medium_term_fav_genres": medium_term_fav_genres,
                "long_term_fav_genres": long_term_fav_genres,
                "listening_time": listening_time,
                "artist_listened": artists_listened,
                "songs_listened": songs_listened,
                "user_name": user_name,
                "user_photo": profil_photo_user,
                "request_user_name": name_request_user,
                "request_user_photo": profil_photo_request_user,
                "self_page": self_page,
                "follow_status": follow_status,
                'user_playlists': user_playlists,
                "badges": badges
            },
        )


@method_decorator(csrf_exempt, name="dispatch")
class signUp(View):
    def get(self, request):
        """
        After spotify, user will come here.
        """
        return render(request, "signup.html")

    def post(self, request):
        """
        Firstly, it checks the email. If it exists already, it respond with an error message.
        Then according to the given city name, it tries to find the city id from db.
            If it can not find, it respond with an error message.
        1- Adding user table
        2- Adding login_info table
        3- Adding spotify_user table
        4- Adding refresh_token table
        5- Adding access_token table
        6- Adding favorites
        7- Adding user_photo table

        Return:
            If email is already existed -> Status code is 409
            If city is not available -> Status code is 400
            If successfull -> Status code is 200.
        """
        # firstly i took the user's information that comes from the frontend
        email = request.POST["email"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]
        # currently password 2 is meaningless

        access_token = request.POST["access"]
        refresh_token = request.POST["refresh"]
        # lets take the user information from spotify.In order to that we are using the access_token.
        userInfo = get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": "Bearer " + access_token},
        ).json()
        print(userInfo)
        userIDSpotify = userInfo["id"]
        try:
            urlPhoto = userInfo["images"][0]["url"]
        except:
            #if profil photo is not exist:
            urlPhoto ="https://as2.ftcdn.net/v2/jpg/02/15/84/43/1000_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        name = userInfo["display_name"]

        # to check the email:
        # email should be unique in the db:
        if MusicorpusUser.objects.filter(email=email).exists():
            # if email exists in db:
            # status 409
            messages.info(request, "Email exists.")
            return redirect("/")

        if MusicorpusUser.objects.filter(username=userIDSpotify).exists():
            # if email exists in db:
            # status 409
            messages.info(request, "Username exists.")
            return redirect("/")

        # to find the city that user lives. This search operation should be case insensitive.
        # So, we are changing the format of the given city.
        city = city.lower()
        city = city[0].upper() + city[1:]

        # we need to check this query because city can be given as wrong.
        try:
            city_from_db = City.objects.get(name=city)
        except:
            # if this query gives an error it means that this city is not in the turkey
            # status 404
            messages.info(request, "Invalid city")
            return redirect("/")

        cityID = city_from_db.id

        # after inserting the new user, it returns the user id.
        # also the password will be hashed automatically
        user = MusicorpusUser.objects.create_user(
            username=userIDSpotify,
            first_name=name,
            city_id=cityID,
            email=email,
            password=password,
            gender=gender,
        )

        user.save()
        userID = user.id

        # to get new token we need refresh token so i added them into db:
        refreshTokenDB = Refresh_Token.objects.create(
            user=user, refresh_token=refresh_token
        )
        refreshTokenDB.save()

        # add accestoken into db:
        accessTokenDB = Access_Token.objects.create(
            user=user, access_token=access_token
        )
        accessTokenDB.save()

        # lets see the top songs:

        # short term fav songs:
        getFavSongsFromSpotify(access_token, user, "short_term")

        # medium term fav songs:
        getFavSongsFromSpotify(access_token, user, "medium_term")

        # long term fav songs:
        getFavSongsFromSpotify(access_token, user, "long_term")

        # lets see the top artists:

        # short term fav artist:
        getFavArtistsFromSpotify(access_token, user, "short_term")

        # medium term fav artist:
        getFavArtistsFromSpotify(access_token, user, "medium_term")

        # long term fav artist:
        getFavArtistsFromSpotify(access_token, user, "long_term")

        # lets see the top genres:

        # short term fav genres:
        getFavGenresFromSpotify(access_token, user, "short_term")

        # medium term fav genres:
        getFavGenresFromSpotify(access_token, user, "medium_term")

        # long term fav genres:
        getFavGenresFromSpotify(access_token, user, "long_term")

        # add url of the profil photo of the user into db:
        ppUrl = User_Photo.objects.create(user=user, photo=urlPhoto)
        ppUrl.save()

        return redirect("/main")


@method_decorator(csrf_exempt, name="dispatch")
class Login(View):
    def post(self, request):
        """
        This function is for login.

        Format for the request should be in this format:
        {
            "username":"123456",
            "password":"deneme"
        }

        Args:
            request (dict)


        If user logins, the status of the response is 200.
        If username or password is wrong, the status of the 401.
        """
        # email and passwords are retrieved from post request.
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            # does user exist?
            user = MusicorpusUser.objects.get(email=email)

        except:
            # if this query gives an error it means that this email doesn't exist in db
            # status 404
            messages.info(request, "Wrong email or password")
            return redirect("/")

        username = user.username
        userID = user.id

        userAuthenticate = auth.authenticate(username=username, password=password)
        if userAuthenticate is None:
            # if password is wrong:
            messages.info(request, "Wrong email or password")
            return redirect("/")

        # if email and password is true:
        auth.login(request, userAuthenticate)

        # to get new access token
        accessToken = getAccessToken(user)
        print(accessToken)
        # this function will add the new recent played songs:
        getRecentSongsFromSpotify(user, accessToken)

        # change short_term favs
        getFavSongsFromSpotify(accessToken, user, "short_term")
        getFavArtistsFromSpotify(accessToken, user, "short_term")
        getFavGenresFromSpotify(accessToken, user, "short_term")
        getPlaylistsFromSpotify(user, accessToken)

        return redirect("/main")


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect("/")


class Main(LoginRequiredMixin, View):
    # If user is not login the system, and s/he tries to go to main page,we will direct to index page.
    redirect_field_name = "index"

    def get(self, request):
        user = request.user

        user_playlists = get_playlists(user)
        user_photo = get_profil_photo(user)
        user_name = user.first_name
        posts = get_posts(user)
        events = get_events(user)
        song_of_day = get_song_of_the_day(user)
        artist_of_day = get_artist_of_the_day(user)
        return render(
            request,
            "main.html",
            {
                "user_playlists": user_playlists,
                "user_name": user_name,
                "user_photo": user_photo,
                "posts": posts,
                "events":events,
                "song_of_day":song_of_day,
                "artist_of_day":artist_of_day
            },
        )

@method_decorator(csrf_exempt, name="dispatch")
class UserPost(View):
    def post(self,request):
        msg = request.POST.get("user-post")
        create_post(request.user, msg)
        return redirect("/main")
    

class UserPlaylists(View):
    def get(self,request):
        user = request.user

        user_playlists = get_playlists(user)

        following_playlists = get_following_playlists(user)
        for playlist in user_playlists:
            playlist_tracks=getTracksOfPlaylists(playlist["id_spotify"], getAccessToken(user))
            playlistSongs = get_listening_ratio_playlist(user, playlist_tracks)
            playlist["ratio"]=playlistSongs["ratio"]

        for playlist in following_playlists:
            playlist_tracks=getTracksOfPlaylists(playlist["id_spotify"], getAccessToken(user))
            playlistSongs = get_listening_ratio_playlist(user, playlist_tracks)
            playlist["ratio"]=playlistSongs["ratio"]
        
        #print(following_playlist_results)
        return render(request, "playlist.html", {'user_playlists':user_playlists, 'following_playlists':following_playlists})
    
class Songs(View):
    def get(self,request,pk):
        spotify_id = pk
        user = request.user

        playlist= getTracksOfPlaylists(pk, getAccessToken(user))
        playlist = get_listening_ratio_playlist(user, playlist)
        songs = playlist["tracks"]
        print(songs)
        
        #print(following_playlist_results)
        return render(request, "songs.html", {"tracks":songs})
