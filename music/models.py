from urllib.parse import MAX_CACHE_SIZE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=255)


class MusicorpusUser(AbstractUser):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)


class SpotifyUser(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)


class Dislike(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="user_dislike"
    )
    other_user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="dislike"
    )


class Like(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="user_like"
    )
    other_user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="like"
    )


class Follower(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="user_follow"
    )
    follower_user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE, related_name="follower"
    )
    time = models.DateTimeField(auto_now_add=True)


class Fav_Artists(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    term = models.CharField(max_length=255)
    artist1 = models.CharField(max_length=255)
    artist1_link = models.CharField(max_length=255)
    artist2 = models.CharField(max_length=255)
    artist2_link = models.CharField(max_length=255)
    artist3 = models.CharField(max_length=255)
    artist3_link = models.CharField(max_length=255)
    artist4 = models.CharField(max_length=255)
    artist4_link = models.CharField(max_length=255)
    artist5 = models.CharField(max_length=255)
    artist5_link = models.CharField(max_length=255)


class Fav_Songs(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    term = models.CharField(max_length=255)
    song1 = models.CharField(max_length=255)
    song1_link = models.CharField(max_length=255)
    song2 = models.CharField(max_length=255)
    song2_link = models.CharField(max_length=255)
    song3 = models.CharField(max_length=255)
    song3_link = models.CharField(max_length=255)
    song4 = models.CharField(max_length=255)
    song4_link = models.CharField(max_length=255)
    song5 = models.CharField(max_length=255)
    song5_link = models.CharField(max_length=255)


class Fav_Genres(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    term = models.CharField(max_length=255)
    genre1 = models.CharField(max_length=255)
    genre2 = models.CharField(max_length=255)
    genre3 = models.CharField(max_length=255)
    genre4 = models.CharField(max_length=255)
    genre5 = models.CharField(max_length=255)

class Access_Token(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    access_token = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Refresh_Token(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255)

class User_Photo(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    photo = models.TextField()

class Recent_Songs(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)
    song = models.CharField(max_length=255)
    song_link = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    artist_link = models.CharField(max_length=255)
    duration = models.IntegerField()

class Events(models.Model):
    name=models.CharField(max_length=255)
    link=models.CharField(max_length=255)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    photo= models.CharField(max_length=255, null = True)
    location = models.CharField(max_length=255, null = True)


class Posts(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)
    post = models.TextField()

class Playlists(models.Model):
    user = models.ForeignKey(
        MusicorpusUser, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    photo_url = models.CharField(max_length=255, null=True)
    id_spotify = models.CharField(max_length=255, null= True)

class Badge(models.Model):
    user = models.ForeignKey(MusicorpusUser, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=255)