from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from django.contrib.auth.decorators import login_required

# Função de login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    # Obter dados do usuário a partir do POST
    userData = [
        request.POST.get('email'),
        request.POST.get('password'),
    ]
    
    # Autenticar o usuário
    userAuthenticate = authenticate(request, username=userData[0], password=userData[1])
    
    if userAuthenticate is not None:
        # Chamar a função de login do Django com request e o usuário autenticado
        auth_login(request, userAuthenticate)
        return redirect('index')
    
    return render(request, 'login.html', {'error': 'Usuário ou senha inválidos', 'userData': userData})

# Função de cadastro
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    userData = [
        request.POST.get('username'),
        request.POST.get('email'),
        request.POST.get('password'),
        request.POST.get('confirmPassword')
    ]
    
    # Verificar se o nome de usuário está vazio
    if not userData[0]:
        return render(request, 'cadastro.html', {'error': 'Preencha o nome de usuário', 'userData': userData})
    
    # Verificar se o email está vazio
    if not userData[1]:
        return render(request, 'cadastro.html', {'error': 'Preencha o campo email', 'userData': userData})
    
    # Verificar se as senhas coincidem
    if userData[2] != userData[3]:
        return render(request, 'cadastro.html', {'error': 'As senhas não coincidem', 'userData': userData})
    
    # Criar o usuário (utilizando o manager do CustomUser)
    try:
        user = CustomUser.objects.create_user(username=userData[0], email=userData[1], password=userData[2])
        
        # Redirecionar para a página de login após criar o usuário
        return redirect('login')
    except Exception as e:
        return render(request, 'cadastro.html', {'error': f'Ocorreu um erro: {str(e)}', 'userData': userData})
