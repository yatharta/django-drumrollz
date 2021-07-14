from django.urls import path, re_path
from . import views

app_name = 'music'
urlpatterns = [

    # registration
    #url(r'^register/$', views.register, name = "register"),

    # /login page (registration)/
    re_path(r'^register/$', views.register, name="register"),

    # login
    re_path(r'^login_user/$', views.login_user, name = "login_user"),

    # logout
    re_path(r'^logout_user/$', views.logout_user, name = "logout_user"),

    # /music/
    re_path(r'^$', views.index, name = "index"),

    # /music/album_id/
    #re_path(r'^(?P<album_id>\d+)/$', views.detail, name = "detail"),
    re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name = "detail"),

    # /music/album/add/
    re_path(r'album_create/$', views.album_create, name="album_create"),

    # /music/album/2 (updated primary key)/
    #url(r'album/(?P<pk>\d+)/$', views.AlbumUpdate.as_view(),name="album-update"),

    # /music/search
    #re_path(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name = "songs"),
    re_path(r'^songs/$', views.songs, name = "songs"),

    # /music/album/song
    re_path(r'^(?P<album_id>[0-9]+)/song_create/$', views.song_create, name = "song_create"),

    # /music/album/song/delete
    re_path(r'^(?P<album_id>[0-9]+)/song_delete/(?P<song_id>[0-9]+)/$', views.song_delete, name = "song_delete"),

    # /music/album/2/delete/
    re_path(r'album/(?P<album_id>[0-9]+)/delete/$', views.album_delete, name="album_delete"),
]