from .models import Events, Recent_Songs, User_Photo
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils.timezone import get_current_timezone
from .models import Fav_Songs, Fav_Genres, Fav_Artists, Follower, Posts, Playlists, Badge
from django.forms.models import model_to_dict

from datetime import datetime


def get_song_of_the_day(user):
    """
    It returns the most replayed song of the day.

    Args:
        user (models.MusicorpusUser):

    Returns:
        mostPlayedSong  (dict): {'song':songname, 'song_link': link}
    """
    # get today's songs which belongs the given user
    todaySongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=1))
        & Q(user=user)
    )
    songCounter = {}
    for song in todaySongs:
        if song.song in songCounter:
            songCounter[song.song] += 1
        else:
            songCounter[song.song] = 1

    mostPlayedSongName = max(songCounter, key=songCounter.get)
    mostPlayedSong = {"song": mostPlayedSongName}
    for song in todaySongs:
        if song.song == mostPlayedSongName:
            mostPlayedSong["song_link"] = song.song_link
            break

    return mostPlayedSong


def get_artist_of_the_day(user):
    """
    It returns the most replayed artist of the day.

    Args:
        user (models.MusicorpusUser):

    Returns:
        mostPlayedArtist (dict): {'artist':artistname, 'artist_link': link}
    """
    # get today's songs which belongs the given user
    todaySongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=1))
        & Q(user=user)
    )

    artistCounter = {}
    for song in todaySongs:
        if song.artist in artistCounter:
            artistCounter[song.artist] += 1
        else:
            artistCounter[song.artist] = 1

    mostPlayedArtistName = max(artistCounter, key=artistCounter.get)

    mostPlayedArtist = {"artist": mostPlayedArtistName}
    for song in todaySongs:
        if song.artist == mostPlayedArtistName:
            mostPlayedArtist["artist_link"] = song.artist_link
            break

    return mostPlayedArtist


def get_listening_time(user):
    """
    It returns the duration of the music listened in the last 7 days.
    one refers today
    two refers yesterday
    three refers three days ago
    four refers four days ago
    five refers five days ago
    six refers six days ago
    seven refers seven days ago

    TO test you can use this query:

    INSERT INTO music_recent_songs (time,song,song_link,artist,artist_link,duration,user_id)
    VALUES
    ('2022-07-16 16:43:51.886658+03', 'song1','song1_link','artist1','artist2',60000,1);

    Args:
        user (models.MusicorpusUser):

    """
    listeningTime = {}

    # today:
    one_msec = 0
    oneSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=1))
        & Q(user=user)
    )

    for song in oneSongs:
        one_msec += song.duration

    one_min = one_msec / 60000  # to convert msec to minute

    listeningTime["1"] = one_min

    # yesterday:
    two_msec = 0
    twoSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=2))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=1))
        & Q(user=user)
    )

    for song in twoSongs:
        two_msec += song.duration

    two_min = two_msec / 60000  # to convert msec to minute

    listeningTime["2"] = two_min

    # three days ago:
    three_msec = 0
    threeSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=3))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=2))
        & Q(user=user)
    )

    for song in threeSongs:
        three_msec += song.duration

    three_min = three_msec / 60000  # to convert msec to minute

    listeningTime["3"] = three_min

    # four days ago:
    four_msec = 0
    fourSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=4))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=3))
        & Q(user=user)
    )

    for song in fourSongs:
        four_msec += song.duration

    four_min = four_msec / 60000  # to convert msec to minute

    listeningTime["4"] = four_min

    # five days ago:
    five_msec = 0
    fiveSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=5))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=4))
        & Q(user=user)
    )

    for song in fiveSongs:
        five_msec += song.duration

    five_min = five_msec / 60000  # to convert msec to minute

    listeningTime["5"] = five_min

    # six days ago:
    six_msec = 0
    sixSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=6))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=5))
        & Q(user=user)
    )

    for song in sixSongs:
        six_msec += song.duration

    six_min = six_msec / 60000  # to convert msec to minute

    listeningTime["6"] = six_min

    # seven days ago:
    seven_msec = 0
    sevenSongs = Recent_Songs.objects.filter(
        Q(time__gte=datetime.now(tz=get_current_timezone()) - timedelta(days=7))
        & Q(time__lte=datetime.now(tz=get_current_timezone()) - timedelta(days=6))
        & Q(user=user)
    )

    for song in sevenSongs:
        seven_msec += song.duration

    seven_min = seven_msec / 60000  # to convert msec to minute

    listeningTime["7"] = seven_min

    return listeningTime


def get_fav_songs_from_db(user, term):
    """
    It returns the favorite five songs of the given user according to the given term

    Args:
        user (models.MusicorpusUser):
        term (str): short_term/medium_term/long_term

    Returns:
        (dict): {'song1':song1, 'song1_link':link1, 'song2'....}
    """
    fav_songs = {}
    fav_songs_query = Fav_Songs.objects.get(user=user, term=term)

    fav_songs = model_to_dict(fav_songs_query)

    del fav_songs["id"]
    del fav_songs["user"]
    del fav_songs["term"]

    return fav_songs


def get_fav_artists_from_db(user, term):
    """
    It returns the favorite five artists of the given user according to the given term

    Args:
        user (models.MusicorpusUser):
        term (str): short_term/medium_term/long_term

    Returns:
        (dict): {'song1':song1, 'song1_link':link1, 'song2'....}
    """
    fav_artists = {}
    fav_artists_query = Fav_Artists.objects.get(user=user, term=term)

    fav_artists = model_to_dict(fav_artists_query)

    del fav_artists["id"]
    del fav_artists["user"]
    del fav_artists["term"]

    return fav_artists


def get_fav_genres_from_db(user, term):
    """
    It returns the favorite five genres of the given user according to the given term

    Args:
        user (models.MusicorpusUser):
        term (str): short_term/medium_term/long_term

    Returns:
        (dict): {'song1':song1, 'song1_link':link1, 'song2'....}
    """
    fav_genres = {}
    fav_genres_query = Fav_Genres.objects.get(user=user, term=term)

    fav_genres = model_to_dict(fav_genres_query)

    del fav_genres["id"]
    del fav_genres["user"]
    del fav_genres["term"]

    return fav_genres


def get_followers(user):
    """
    This function returns the followers of the given user:

    Args:
        user (models.MusicorpusUser):

    Returns:
        follower_list (list<models.MusicorpusUser>)
    """
    follower_list = []
    followers = Follower.objects.filter(user=user)

    for follower in followers:
        follower_list.append(follower.follower_user)

    return follower_list


def get_following(user):
    """
    This function returns the followed people by the given user:

    Args:
        user (models.MusicorpusUser):

    Returns:
        following_list (list<models.MusicorpusUser>)
    """
    following_list = []
    followings = Follower.objects.filter(follower_user=user)

    for following in followings:
        following_list.append(following.user)
    return following_list


def follow(user, follower_user):
    """
    This function adds user and the follower of the user into followers table.

    Args:
        user (models.MusicorpusUser):
        followed_user (models.MusicorpusUser):
    
    Returns:
        null:
    """

    new_follow = Follower.objects.create(user=user, follower_user = follower_user)
    new_follow.save()
    return


def get_posts(user):
    """
    This function returns the post that was shared by followed people by given user:

    Args:
        user (models.MusicorpusUser):

    Returns:
        posts (list<dict>)
    """
    response = []
    #firstly we need get the list of following:
    followings = get_following(user)
    
    if followings == []:
        print([])
        return []

    posts = Posts.objects.filter(user__in = followings).order_by("-time")
    
    for post in posts:
        post_loop = {}
        post_loop["name"]= post.user.first_name
        post_loop["post"] = post.post
        post_loop["photo"]= get_profil_photo(post.user)
        time = post.time
        post_loop["time"] = time.strftime("%B %d %Y, %H:%M")
        response.append(post_loop)

    return response

def create_post(user, text):
    """
    This function create a new post according to the given text.

    Args:
        user (models.MusicorpusUser): 
        text (str): 
    
    Returns:
        null
    """
    new_post = Posts.objects.create(user=user, post = text)
    new_post.save()
    return 

def get_playlists(user):
    """
    This function returns name and link of the user's playlists. 

    Args:
        user (_type_): _description_
    
    Return:
        playlists (list<dict>): [{'name':'n1', 'link':'l1'},{}...]
    """

    playlists =  []
    playlists_query = Playlists.objects.filter(user=user)

    for playlist in playlists_query:
        playlists.append({'name': playlist.name, 'link':playlist.link, "photo":playlist.photo_url, "id_spotify":playlist.id_spotify, "user":user.first_name})
    return playlists

def get_following_playlists(user):
    """
    This function returns name and link of the following user's playlists. 

    Args:
        user (_type_): _description_
    
    Return:
        playlists (list<dict>): [{'name':'n1', 'link':'l1'},{}...]
    """
    followings = get_following(user)
    
    if followings == []:
        print([])
        return []

    playlists =  []
    playlists_query = Playlists.objects.filter(user__in = followings)

    for playlist in playlists_query:
        playlists.append({'name': playlist.name, 'link':playlist.link, "photo":playlist.photo_url, "id_spotify":playlist.id_spotify, "user":playlist.user.first_name})
    return playlists

def get_listened_songs_number(user):
    """
    It returns the number of the listened songs of the given user.

    Args:
        user (models.MusicorpusUser): 
    
    Returns: 
        number_of_songs (int)
    """
    songs = Recent_Songs.objects.filter(user = user)
    
    number_of_songs = len(songs)
    return number_of_songs

def get_listened_artists_number(user):
    """
    It returns the number of the listened songs of the given user.

    Args:
        user (models.MusicorpusUser): 
    
    Returns: 
        number_of_artists (int)
    """
    songs = Recent_Songs.objects.filter(user = user)
    
    artists = {}

    for song in songs:
        if(song.artist in artists):
            continue
        else:
            artists[song.artist] = True
    
    number_of_artists = len(artists)
    return number_of_artists


def get_profil_photo(user):
    """
    It returns the url of the profil photo of the user

    Args:
        user (models.MusicorpusUser):
    
    Returns:
        pp (str)
    """

    photo_query = User_Photo.objects.get(user=user)

    pp = photo_query.photo
    return pp


def get_listening_ratio_playlist(user, tracks):

    listened_songs_names = []
    listened_songs = Recent_Songs.objects.filter(user=user)
    playlist = Playlists.objects.get(id_spotify = tracks["id_spotify"])

    playlist_id = tracks
    
    for song in listened_songs:
        listened_songs_names.append(song.song)
    
    song_number = len(tracks["tracks"])
    matched_song_counter = 0

    for song in tracks["tracks"]:
        if song["name"] in listened_songs_names:
            matched_song_counter += 1
            song["status"] = True
        else:
            song["status"] = False
    
    tracks["ratio"]= matched_song_counter/song_number*100

    try:
        #firstly delete old Badge
        old_badge = Badge.objects.get(user=user, playlist=playlist)
        old_badge.delete()
    except:
        pass

    badge = None
    if(tracks["ratio"] >= 70):
        badge = 'titanium'
        new_badge = Badge.objects.create(
            user=user,
            playlist=playlist,
            badge_type= 'titanium'
        )
        new_badge.save()

    elif(tracks["ratio"]>=50):
        badge = 'gold'
        new_badge = Badge.objects.create(
            user=user,
            playlist=playlist,
            badge_type= 'gold'
        )
        new_badge.save()

    elif(tracks["ratio"]>=35):
        badge = 'silver'
        new_badge = Badge.objects.create(
            user=user,
            playlist=playlist,
            badge_type= 'silver'
        )
        new_badge.save()

    elif(tracks["ratio"]>=15):
        badge = 'bronze'
        new_badge = Badge.objects.create(
            user=user,
            playlist=playlist,
            badge_type= 'bronze'
        )
        new_badge.save()
    
    tracks["badge"] = badge

    return tracks

def get_badge(user):
    badges = Badge.objects.filter(user=user)
    titanium_badge = 0
    gold_badge=0
    silver_badge=0
    bronze_badge=0
    

    for badge in badges:
        if badge.badge_type == "titanium":
            titanium_badge +=1 
        elif badge.badge_type == "gold":
            gold_badge +=1 
        elif badge.badge_type == "silver":
            silver_badge +=1 
        elif badge.badge_type == "bronze":
            bronze_badge +=1 
    response = {"titanium":titanium_badge, "gold":gold_badge, "silver":silver_badge, "bronze":bronze_badge}
    return response
    

def get_events(user):
    event_list = []
    events = Events.objects.filter(city=user.city)

    for event in events:
        new_event = model_to_dict(event)
        del new_event["id"]
        event_list.append(new_event)
    
    if(event_list== []):
        events = Events.objects.filter(city_id=34)
        for event in events:
            new_event = model_to_dict(event)
            del new_event["id"]
            event_list.append(new_event)
    return event_list