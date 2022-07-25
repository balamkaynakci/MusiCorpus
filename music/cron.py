from .util_spotify import getAccessToken, getRecentSongs
from .models import MusicorpusUser

def recent_songs():
    users = MusicorpusUser.objects.all()
    for user in users:
        accessToken = getAccessToken(user)
        print(accessToken)
        getRecentSongs(user,accessToken)
    






