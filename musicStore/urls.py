from django.urls import path
from . import views
from .models import Album
urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:album_id>/',views.detail, name ='detail'),
    path('<int:album_id>/results/', views.results, name = 'result'),
]
