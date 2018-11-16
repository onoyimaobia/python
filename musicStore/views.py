from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from .models import Album, Song, Videos, Profiles
from django.db.models import Q

from django.contrib.auth.models import User, Group

from django.template import  RequestContext
from django.conf import  settings
import requests
from .serializer import EmbedSerializer
from .forms import SubmitLast, VideoForm, SignUpForm
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from  django.views import  generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


def index(request):

    all_albums = Album.objects.all()

    # template = loader.get_template('musicStore/index.html')
    # html = ''
    context = {'all_albums': all_albums}
    return render(request, 'musicStore/index.html', context)


def delete_album(request):

    all_albums = Album.objects.all()

    # template = loader.get_template('musicStore/index.html')
    # html = ''
    context = {'all_albums': all_albums}
    return render(request, 'musicStore/delete_album.html', context)


def song(request):
    all_song = Song.objects.all()

    context = {'all_song': all_song}
    template = 'musicStore/song.html'
    return render(request,template,context)


def delete_song(request):
    all_song = Song.objects.all()

    context = {'all_song': all_song}
    template = 'musicStore/delete_song.html'
    return render(request,template,context)


def text(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'musicStore/text.html', context)


@login_required(login_url='/musicStore/login')
def detail(request, album_id):
    try:
        all_album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")
    return render(request, 'musicStore/detail.html', {'all_album': all_album})


@login_required(login_url='/musicStore/login')
def download(request, song_id):
    try:
        all_song = Song.objects.filter(pk=song_id)
        play = Videos.objects.filter(song_id=song_id)
    except Album.DoesNotExist:
        raise Http404("can't play or download song")
    return render(request, 'musicStore/download.html', {'all_song': all_song, 'play': play})


def favourite(request, album_id):
    all_album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = all_album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'musicStore/detail.html', {
            'all_album': all_album,
            'error_message': "you did not select a song"
        })
    else:
        selected_song.is_favourite = True
        selected_song.save()
        return render(request, 'musicStore/detail.html', {'all_album': all_album})


def results(request, album_id):
    response = "you are looking at the results of album %s."
    return HttpResponse(response % album_id)


@login_required(login_url='/musicStore/login')
def search(request):
    query = request.GET.get('q')
    convert = query.lower()
    if Album.objects.all().filter(Q(artist__iexact=query) | Q(artist__startswith=query)):
        templates = 'musicStore/search.html'

        result = Album.objects.all().filter(Q(artist__iexact=convert) | Q(artist__startswith=convert))
        identity = Album.objects.get(artist = convert)
        song = Song.objects.all().filter(album_id=identity.id)

        return render(request, templates, {'result': result, 'get': query, 'identity': identity, 'song': song})
    else:
        response = requests.get('https://itunes.apple.com/search?term='+convert)
        geodata = response.json()
        return render(request, 'musicStore/displaydetail.html',
                      {
                          'wrapperName': geodata['results']
                      })


@login_required(login_url='/musicStore/login')
def overview(request):
    allalbums = Song.objects.all()
    time = datetime.now()
    hour = time.hour
    if hour < 12:
        message = "Good Morning"
    elif 12 <= hour < 16:
        message = "Good afternoon"
    else:
        message = "Good Evening"
    template = 'musicStore/overview.html'
    context = {'allalbums': allalbums,'time': time,'message': message}
    return render(request, template, context,)


def search_song_type(request):
    template = 'musicStore/overview.html'
    if request.GET.get('song_type') == 'song_type':
        query1 = request.GET.get('s')
        allalbums = Song.objects.all().filter(Q(file_type__exact=query1))
        return render(request, template, {'allalbums':allalbums})
    elif request.GET.get('song_type') == 'song_genre':
        query1 = request.GET.get('a')
        allalbums = Song.objects.all().filter(Q(album__genere__iexact=query1))
        return render(request, template, {'allalbums': allalbums})
    elif request.GET.get('song_type') == 'multidate':

        query1 = request.GET.get('daterange')
        if ':' in query1:
            if query1.count(':') == 1:
                start_date, end_date = query1.split(" : ")
                if start_date < end_date:
                    allalbums = Song.objects.all().filter(Q(album__creation_date__gte=start_date,
                                                            album__creation_date__lte=end_date))
                    return render(request, template, {'allalbums': allalbums})
                else:
                    messages.warning(request, "start date cannot be greater than end date")
                    return redirect('musicStore:overview')
            else:
                messages.warning(request, "You can only search for two different date")
                return redirect('musicStore:overview')
        elif ':' not in query1:
            allalbums = Song.objects.all().filter(Q(album__creation_date__startswith=query1))
            return render(request, template, {'allalbums': allalbums})
        else:
            messages.warning(request, "Search does not exist")
            return redirect('musicStore:overview')
    elif request.GET.get('song_type') == 'createdate':
        query1 = request.GET.get('date')
        allalbums = Song.objects.all().filter(Q(album__creation_date__startswith=query1))

        return render(request, template, {'allalbums': allalbums})
    elif request.GET.get('song_type') == 'song_title':
        query1 = request.GET.get('t')

        allalbums = Song.objects.all().filter(Q(song_title__iexact=query1))
        return render(request, template, {'allalbums': allalbums})
    else:
        messages.warning(request, "hhhhhhh")
        return redirect('musicStore:overview')




class CreateAlbum(CreateView):
    model = Album
    fields = ['artist','album_title','genere','album_logo']


class UpdateAlbum(UpdateView):
    model = Album
    fields = ['artist','album_title','genere','album_logo']


class DeleteAlbum(DeleteView):
    model = Album
    success_url = reverse_lazy('musicStore:index')


def save_last(request):
    if request.method == 'POST':
        form = SubmitLast(request.POST)


def displaydetail(request):
    query = request.GET.get('z')
    #sting = str(query)
    convert = query.lower()
    response = requests.get('https://itunes.apple.com/search?term=' + convert)
    geodata = response.json()
    return render(request, 'musicStore/displaydetail.html',
                  {
                      'wrapperName': geodata['results']
                  })


def dispdetail(request):
    query = request.GET.get('query')
    #sting = str(query)
    convert = query.lower()
    response = requests.get('https://itunes.apple.com/search?term=' + convert)
    geodata = response.json()
    return render(request, 'musicStore/displaydetail.html',
                  {'result': geodata['resultCount'],
                      'wrapperName': geodata['results'],
                   })


def Addalbum(request):
    template = 'musicStore/Addalbum.html'
    if request.method == 'POST':
        query1 = request.POST['artistName']
        query2 = request.POST['trackName']
        query3 = request.POST['collectionName']
        query4 = request.POST['artworkUrl100']
        query5 = request.POST['primaryGenreName']
        source = "iTune"
        file_type = "mp3"
        print(query1)
        context = {'d': query1,
                   'e': query2,
                   'f': query3,
                   'g': query4,
                   'h': query5,
                   'i' : file_type,
                   'j': source
                   }
        return render(request, template, context)


def savetodb(request):
    if request.method== 'POST':
        query1 = request.POST['artistName']
        query2 = request.POST['trackName']
        query3 = request.POST['collectionName']
        query4 = request.POST['artworkUrl100']
        query5 = request.POST['primaryGenreName']
        query6 = request.POST['h']
        query7 = request.POST['i']
        if Album.objects.filter(artist= query1, album_title=query3, genere=query5,album_logo=query4).exists():
            print("good day")
        else:
            creat_album = Album.objects.create(artist=query1, album_title= query3,genere= query5,album_logo=query4)
            creat_album.save()
            creat_song = Song.objects.create(album_id=creat_album.id, file_type=query6, song_title=query2)
            creat_song.save()
            print('hiii')
            # template = loader.get_template('musicStore/index.html')
            return redirect('musicStore:index')


def register(request):
    return render(request, 'musicStore/register.html')


def registers(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        firstname1 = firstname.lower()
        lastname = request.POST['last_name']
        lastname1 = lastname.lower()
        email = request.POST['email']
        email1 = email.lower()
        contact = request.POST['contact']
        address = request.POST['address']
        username = request.POST['username']
        username1 = username.lower()
        password = request.POST['password']
        password1= password.lower()
        confirmpassword = request.POST['confirm_password']
        confirmpassword1 = confirmpassword.lower()
        if firstname == "" or lastname == "" or email == "" or contact == "" or address == "" or username == "" \
                or password == "" or confirmpassword == "":
            messages.success(request, 'All Field is Required.')
            return redirect('musicStore:register')
        else:
            user = User.objects.filter(username=username1).exists()
            if user:
                messages.success(request, 'User already exist.')
                return redirect('musicStore:register')
            elif password == confirmpassword and len(contact) == 11:
                create_user = User.objects.create_user(first_name=firstname1, last_name=lastname1, email=email1,
                                                           username=username1, password=password1)
                create_user.save()
                create_profile = Profiles.objects.create(user_id=create_user.id, contact=contact, address=address)
                create_profile.save()
                my_group = Group.objects.get(name='Viewers')
                create_user.groups.add(my_group)
                #my_group.user_set.add(create_user)
                print('Profile created')
                messages.success(request, 'User Successfully registered')
                return redirect('musicStore:login')
            else:
                messages.success(request, 'both paaword do not matche or contact not up to 11.')
                return redirect('musicStore:register')


def videoUpload(request):
    #lastvideo = Videos.objects.last()

    #videofile = lastvideo.videofile
    # (request.POST or None, request.FILES or None).
    #  request.POST or None makes the data be retained in the field after a user has submitted the form.
    # It also doesn't raise validation errors when the page is first loaded.
    #  request.FILES or None allows the files to submitted to a database in Django.
    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {#'videofile': videofile,
               'form': form,
                's': Song.objects.all()
               }
    template = 'musicStore/videoUpload.html'
    return render(request,template , context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('musicStore:index')
    else:
        form = SignUpForm()
    template = 'musicStore/signup.html'
    context = {'form': form}
    return render(request,template,context)


@login_required(login_url='/musicStore/login')
def permission(request):
    group = Group.objects.all()
    user = User.objects.all()
    viewer = User.objects.filter(groups__name='Viewers')
    staff = User.objects.filter(groups__name='Staff')

    template = 'musicStore/permission.html'
    context = {'group': group, 'user': user, 'viewer': viewer,'staff': staff}
    return render(request,template, context)


@login_required(login_url='/musicStore/login')
def create_group(request):
    if request.method == 'POST':
        group_name  = request.POST['group_name']
        if group_name == "":
            messages.success(request,'Field Required')
            return  redirect('musicStore:permission')
        else:
            creat_group, created = Group.objects.get_or_create(name= group_name)
            creat_group.save()
            messages.success(request,'Group created successfully')
            return redirect('musicStore:permission')
    else:
        messages.success(request,'only alphebets is required')
        return redirect('musicStore:permission')


def add_user(request):
    if request.method == 'POST':
        user_id = request.POST['users']
        user = User.objects.get(pk=user_id)
        if user.groups.filter(name='Staff').exists():
            messages.warning(request, 'User already exist')
            return redirect('musicStore:permission')
        else:
            Add_user = Group.objects.get(name='Staff')
            user.groups.add(Add_user)
            if user.groups.filter(name='Viewers').exists():
                remove_user = Group.objects.get(name='Viewers')
                remove_user.user_set.remove(user)
                return redirect('musicStore:permission')
            return redirect('musicStore:permission')



def delete_user(request):
    if request.method =='POST':
        user_id = request.POST['deleteuser']
        grp = request.POST['staff']

        user = User.objects.get(pk=user_id)
        if grp == 'Staff':
            if user.groups.filter(name='Staff').exists():
                deleteuser = Group.objects.get(name=grp)
                deleteuser.user_set.remove(user)
                return redirect('musicStore:permission')
            else:
                messages.warning(request, 'No such user in group')
                return redirect('musicStore:permission')
        elif grp == 'Viewers':
            if user.groups.filter(name='Viewers').exists():
                deleteuser = Group.objects.get(name=grp)
                deleteuser.user_set.remove(user)
                return redirect('musicStore:permission')
            else:
                messages.warning(request,'No such user in group')
                return redirect('musicStore:permission')

def login(request):
    return render(request, 'musicStore/login.html')


def loginn(request):
    if request.method == "POST":
        username1 = request.POST['username']
        password1 = request.POST['password']

        user = authenticate(username=username1, password=password1)
        if user is not None:
            if user.is_active:
                #log user in
                auth_login(request, user)
                return redirect('musicStore:index')
        else:
            messages.warning(request,'username or password does not match')
            return redirect('musicStore :login')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('musicStore:index')


def testing(request):
    template = 'musicStore/testing.html'
    return render(request, template)

def txt(request):
    template = 'musicStore/txt.html'
    return render(request, template)
