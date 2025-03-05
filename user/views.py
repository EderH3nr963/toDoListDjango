from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    # Get the user data from the POST request
    userData = [ 
        request.POST.get('email'), 
        request.POST.get('password'), 
    ]
    
    userAuthenticate = authenticate(email=userData[0], password=userData[1])
    
    if userAuthenticate is not None:
        login(request, userAuthenticate)
        return redirect('home')
    
    return render(request, 'login.html', {'error': 'Usuário ou senha inválidos', 'userData': userData})

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    userData = [
        request.POST.get('username'), 
        request.POST.get('email'), 
        request.POST.get('password'), 
        request.POST.get('confirmPassword')
    ]
    
    # Check if username is empty
    if not userData[0]:
        return render(request, 'cadastro.html', {'error': 'Preencha o nome de usuário', 'userData': userData})
    
    # Check if email is empty
    if not userData[1]:
        return render(request, 'cadastro.html', {'error': 'Preencha o campo email', 'userData': userData})
    
    # Check if passwords match
    if userData[2] != userData[3]:
        return render(request, 'cadastro.html', {'error': 'As senhas não coincidem', 'userData': userData})
    
    # Create the user (use the manager via CustomUser.objects)
    try:
        # Create user using the CustomUserManager through the CustomUser model's manager
        user = CustomUser.objects.create_user(username=userData[0], email=userData[1], password=userData[2])
        
        # You can now log the user in or redirect to login
        return redirect('login')
    except Exception as e:
        return render(request, 'cadastro.html', {'error': f'Ocorreu um erro: {str(e)}', 'userData': userData})
