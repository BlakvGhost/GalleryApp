from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            album = Album.objects.create(
                slug=slug,
                user=request.user
            )
        
    
    return redirect('default')

