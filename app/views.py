from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def default(request):
    
    return render(request, 'app/index.html')


@login_required
def publish(request):
    
    return render(request, 'app/publish.html')

