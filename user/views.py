from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

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
    
def forgotPassword(request):
    if request.method == 'GET': 
        email = request.GET.get('email')
        
        if not email:
            return render(request, 'forgotPassword.html')
        
        user = CustomUser.objects.filter(email=email).first()
        
        if not user:
            return render(request, 'forgotPassword.html', {'error': 'Usuário não encontrado'})
        
        try:
            # Verificar configurações de email
            if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == 'seu-email@gmail.com':
                raise ValueError("Configurações de email não configuradas corretamente")
            
            if not settings.EMAIL_HOST_PASSWORD or settings.EMAIL_HOST_PASSWORD == 'sua-senha-de-app':
                raise ValueError("Senha de email não configurada")
            
            # Gerar token de recuperação
            token = get_random_string(32)
            user.reset_password_token = token
            user.reset_password_token_created = timezone.now()
            user.save()
            
            # Criar link de recuperação
            reset_link = f"{request.scheme}://{request.get_host()}/user/reset-password/{token}"
            
            # Enviar email
            subject = 'Recuperação de Senha'
            message = f'Clique no link abaixo para redefinir sua senha:\n{reset_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            print(f"Tentando enviar email para: {email}")
            print(f"Usando configurações: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}")
            
            send_mail(subject, message, from_email, recipient_list)
            return render(request, 'forgotPassword.html', {'success': 'Email de recuperação enviado com sucesso!'})
        except ValueError as e:
            print(f"Erro de configuração: {str(e)}")
            return render(request, 'forgotPassword.html', {'error': 'Configuração de email não está correta. Por favor, contate o administrador.'})
        except Exception as e:
            print(f"Erro ao processar recuperação de senha: {str(e)}")
            print(f"Tipo do erro: {type(e).__name__}")
            return render(request, 'forgotPassword.html', {'error': 'Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.'})
    
    return render(request, 'forgotPassword.html')

def resetPassword(request, token):
    if request.method == 'GET':
        user = CustomUser.objects.filter(reset_password_token=token).first()
        
        if not user:
            return render(request, 'resetPassword.html', {'error': 'Token inválido ou expirado'})
        
        # Verificar se o token não expirou (24 horas)
        if timezone.now() - user.reset_password_token_created > timedelta(hours=24):
            return render(request, 'resetPassword.html', {'error': 'Token expirado'})
        
        return render(request, 'resetPassword.html', {'token': token})
    
    elif request.method == 'POST':
        user = CustomUser.objects.filter(reset_password_token=token).first()
        
        if not user:
            return render(request, 'resetPassword.html', {'error': 'Token inválido ou expirado'})
        
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not new_password or not confirm_password:
            return render(request, 'resetPassword.html', {'error': 'Preencha todos os campos'})
        
        if new_password != confirm_password:
            return render(request, 'resetPassword.html', {'error': 'As senhas não coincidem'})
        
        # Atualizar senha
        user.set_password(new_password)
        user.reset_password_token = None
        user.reset_password_token_created = None
        user.save()
        
        return redirect('login')
    
    
