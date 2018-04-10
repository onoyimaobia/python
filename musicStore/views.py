# from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
# from django.template import loader
from django.urls import reverse
from .models import Album
# Create your views here.


def index(request):
    all_albums = Album.objects.all()
    # template = loader.get_template('musicStore/index.html')
    # html = ''
    context = {'all_albums': all_albums}
    # for albums in all_albums:
    #     url = '/musicStore/' + str(albums.id) + '/'
    #     html += '<a href="' + url + '">' + albums.album_title + '</a><br>'
    return render(request, 'musicStore/index.html', context)

      

def detail(request, album_id):
    try:
        all_album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")
    return render(request, 'musicStore/detail.html', {'all_albums': all_album})


def results(request, album_id):
    response = "you are looking at the results of album %s."
    return HttpResponse(response % album_id)
