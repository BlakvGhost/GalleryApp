from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Album, Photo

@login_required
def default(request):
    
    albums = Album.objects.all().order_by('-id')
    
    context = {
        'albums': albums,
    }
    
    return render(request, 'app/index.html', context)


@login_required
def publish(request):
    
    return render(request, 'app/publish.html')


@login_required
def album(request):
    
    slug = request.POST.get('slug')
    
    if slug:
        if request.method == 'POST':
            Album.objects.create(
                slug=slug,
                user=request.user
            )
        
    
    return redirect('default')

@login_required
@csrf_exempt
def upload_image(request, album):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            try:
                album_id = request.POST.get('album_id')
                album = Album.objects.get(pk=album_id)

                photo = Photo(image=uploaded_file, album=album)
                photo.save()

                return JsonResponse({'success': True, 'url': photo.image.url})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Aucun fichier téléchargé.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'}, status=405)


