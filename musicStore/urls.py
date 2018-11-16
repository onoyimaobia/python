from django.urls import path
from django.conf.urls import url

from musicStore import views
from .models import Album
app_name = 'musicStore'
urlpatterns = [

    path('', views.index, name='index'),
    path('delete_album', views.delete_album, name='delete_album'),
    path('song', views.song, name='song'),
    path('delete_song', views.delete_song, name='delete_song'),
    path('<int:album_id>/', views.detail, name='detail'),
    path('download/<int:song_id>/', views.download, name='download'),
    path('<int:album_id>/favourite/', views.favourite, name='favourite'),
    path('<int:album_id>/results/', views.results, name='result'),
    path('search/', views.search, name='search'),
    path('overview/', views.overview, name='overview'),
    path('search_song_type', views.search_song_type, name='search_song_type'),

    path('album/add/',views.CreateAlbum.as_view(), name='add-album'),
    path('album/<int:pk>/', views.UpdateAlbum.as_view(), name='update-album'),
    path('album/<int:pk>/delete/', views.DeleteAlbum.as_view(), name='delete-album'),
    path('displaydetail',views.displaydetail, name='displaydetail'),
    path('displaydetail/', views.dispdetail, name='dispdetail'),
    path('Addalbum/',views.Addalbum, name='Addalbum'),
    path('savetodb', views.savetodb, name='savetodb'),
    path('register', views.register, name='register'),
    path('permission', views.permission, name='permission'),
    path('create_group', views.create_group, name='create_group'),
    path('add_user', views.add_user, name='add_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('registers', views.registers, name='registers'),
    path('videoUpload', views.videoUpload, name='videoUpload'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('loginn', views.loginn, name='loginn'),
    path('logout', views.logout_view, name='logout'),
    path('testing', views.testing, name='testing'),
    path('txt', views.txt, name='txt')
]
