from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Album, Song

# redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .userform import UserForm, AlbumForm, SongForm

AUDIO_FILE_TYPES = ['mp3', 'ogg', 'wav']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def album_create(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1].lower()
            
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    "album": album,
                    "form": form,
                    "error_message": "Image Type Not Supported",
                }
                return render(request, 'music/form_template.html', context)
            album.save()
            
            return render(request, 'music/detail.html', {'album': album})
            context = {
                "form": form,
            } 

            return render(request, 'music/form_template.html', context)


def song_create(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)

    if form.is_valid():
        albums_songs = album.song_set.all()

        for a_song in albums_songs:
            if a_song.song_title == form.cleaned_data.get("song_title"):
                context = {
                    "album": album,
                    "form": form,
                    "error_message": "The Song Already Exists",
                }

                return render(request, 'music/form_template.html')

        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1].lower()

        if file_type not in AUDIO_FILE_TYPES:
            context = {
                "album": album,
                "form": form,
                "error_message": "Audio Type Not Supported",
            }

            return render(request, 'music/form_template.html', context)

        song.save()

        return render(request, 'music/detail.html', {"album": album})

    context = {
        "album": album,
        "form": form,
    }

    return render(request, 'music/form_template.html', context)

def album_delete(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)

    return render(request, 'music/index.html', {'albums': albums})

def song_delete(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()

    return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)

        return render(request, 'music/detail.html', {'album': album, 'user': user})

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")

        if query:
            albums = albums.filter(
                Q(album_title__icontains = query) | Q(artist__icontains = query)
            ).distinct()

            song_results = song_results.filter(
                Q(song_title__icontains = query)
            ).distinct()

            return render(request, 'music/index.html', {
                'object_list': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'object_list': albums})
 
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)

                # Here a profile/Dashboard will be included later on.
                return render(request, 'music/index.html', {'object_list': albums})
            else:
                return render(request, 'music/login.html', {'error_message': "username or password entered does not match"})
        else:
            return render(request, 'music/login.html', {'error_message': "Invalid Login"})

    return render(request, 'music/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }

    return render(request, 'music/login.html', context)


def register(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # cleaned/normalized data
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # to update user's password
        user.set_password(password)

        # now save in the database
        user.save()

        # return user object if credentials are authenticated
        user = authenticate(username=username, email=email, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    
    context = {
        "form": form,
    }
        
    return render(request, 'music/registration.html', context)

def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []

            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)

            users_songs = Song.objects.filter(pk__in = song_ids)
        except Album.DoesNotExist:
            users_songs = []

        return render(request, 'music/songs.html', {
            "song_list": users_songs,
            "filter_by": filter_by,
        })
