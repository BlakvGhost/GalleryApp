from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('default')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@anonymous_required
def login(request):
    
    error = False

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if password and email:
            user = authenticate(request, username=email, password=password)

            if user is not None:
                user_login(request, user)
                return redirect('default')
            error = "Mot de passe ou addresse email invalide"
        else:
            error = "Veuillez remplir tout les champs"

    context = {
        'error': error
    }

    return render(request, 'authenticate/login.html', context)


@anonymous_required
def register(request):
    
    error = False

    if request.method == 'POST':

        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')

        if password and email and firstname and lastname:

            if password == confirm_password:
                try:                    
                    user = User.objects.create_user(
                            first_name=firstname,
                            last_name=lastname,
                            email=email,
                            password=password,
                            username=email,
                        )
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        user_login(request, user)
                        return redirect('default')
                except:
                    error = "Un utilisateur existe déjà avec le même email"
            else:
                error = "Vos deux mots de passe ne sont pas identiques"            
        else:
            error = "Veuillez remplir tout les champs"

    context = {
        'error': error
    }

    return render(request, 'authenticate/register.html', context)


@login_required
def logout(request):
    user_logout(request)
    return redirect('login')