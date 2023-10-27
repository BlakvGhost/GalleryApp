from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from slugify import slugify
from .models import Album, Photo

@login_required
def default(request):
    
    albums = Album.objects.filter(user=request.user).order_by('-id')
    
    context = {
        'albums': albums,
    }
    
    return render(request, 'app/index.html', context)


@login_required
def publish(request, album):
    
    return render(request, 'app/publish.html', {
        'album': Album.objects.filter(pk=album, user=request.user).first(),
        'albumID': album,
    })


@login_required
def album(request):
    
    slug = request.POST.get('slug')
    albumID = request.POST.get('slugID')
    method = request.POST.get('_method')
    
    if slug:
        if request.method == 'POST':
            if method == 'POST':
                Album.objects.create(
                    slug=slug,
                    user=request.user
                )
            elif method == 'UPDATE':
                Album.objects.filter(pk=albumID, user=request.user).update(slug=slug)
            elif method == 'DELETE':
                
                Album.objects.filter(pk=albumID, user=request.user).delete()
    
    return redirect('default')

@login_required
@csrf_exempt
def upload_image(request, albumID=None):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            try:
                album = Album.objects.filter(pk=albumID, user=request.user).first()
                if not album:                    
                    slug = f"{request.user.first_name} {request.user.last_name}"
                    album, created = Album.objects.get_or_create(user=request.user, slug=slug)

                original_name = uploaded_file.name
                photo = Photo(image=uploaded_file, album=album, original_name=original_name)
                photo.save()

                return JsonResponse({'success': True, 'url': photo.image.url})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Aucun fichier téléchargé.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'}, status=405)


