from django.db import models
from django.contrib.auth.models import Permission, User
import datetime
from django.urls import  reverse
from django.utils import timezone
# Create your models here.
from  ckeditor.fields import RichTextField, CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField


class Album(models.Model):

    artist = models.CharField(max_length=200)
    album_title = models.CharField(max_length=200)
    genere = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('musicStore:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=1000)
    is_favourite = models.BooleanField(default=False)
    source = models.CharField(default='iTune', max_length=200)
    song_logo = models.CharField(default='no logo', max_length=300)
    featured_artist = models.CharField(default='None', max_length=100)
    production_date = models.DateTimeField(auto_now_add=True)

    # create a string representation of song
    def __str__(self):
        return self.song_title

class last(models.Model):
    Artist =  models.CharField(max_length=30)
    wrapperType = models.CharField(max_length= 200)
    kind = models.CharField(max_length= 200)
    artistName = models.CharField(max_length=200)
    trackName = models.CharField(max_length= 200)
    releaseDate = models.CharField(max_length=20)


class test(models.Model):
    test = models.CharField(max_length=100)

class Videos(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name="")
    audio = models.FileField(upload_to='audio', blank=True, verbose_name="")
    # verbose_name "" is empty because we don't want the name of the field appearing next to the video upload button.

    #I then create a __str__ function just so that a generic Object isn't returned when calling a video object
    def __str__(self):
        return str(self.videofile)


class Profiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=100)


class Youtube(models.Model):
    song_name = models.CharField(max_length=300)
    youtube_link = models.URLField(verbose_name='Youtube Video', unique=True,max_length=300)


class NewsPosts(models.Model):
    title = RichTextField(max_length=250, config_name='special')
    description = RichTextField(max_length=200, blank=True, config_name='special')
    body = RichTextUploadingField(config_name='default',
                                  external_plugin_resources=[('Youtube',
                                                             '/myFirstSite/static/ckeditor/ckeditor/plugins/youtube/',
                                                              'plugin.js', )],
                                  )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    speaker = models.CharField(max_length=100)
    publish = models.BooleanField(default=False)
    def __str__(self):
        return str(self.title)
