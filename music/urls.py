from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Index.as_view(),name="index"),
    path('spotify/get-auth-url', views.AuthURL.as_view(), name='spotify-auth'),
    path('spotify/callback/',views.spotify_callback),
    path('signup',views.signUp.as_view()),
    path('main',views.Main.as_view()),
    path('login',views.Login.as_view()),
    path('logout',views.Logout.as_view(),name="logout"),
    path('profile',views.Profile.as_view(),name="profile"),
    path('profile/<int:pk>', views.ProfileOther.as_view()),
    path('post',views.UserPost.as_view()),
    path('playlist',views.UserPlaylists.as_view(), name="playlist"),
    path('songs/<str:pk>', views.Songs.as_view(), name='songs'),
]
