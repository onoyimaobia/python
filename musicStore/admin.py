from django.contrib import admin

# Register your models here.
from .models import Album, Song,Videos,NewsPosts
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Videos)
admin.site.register(NewsPosts)