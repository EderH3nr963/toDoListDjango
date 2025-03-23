from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .forms import ForgotPasswordStep1Form, ForgotPasswordStep2Form, ForgotPasswordStep3Form
import random

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
    # Obter o step atual da sessão ou definir como 1
    current_step = request.session.get('forgot_password_step', 1)
    
    if request.method == 'POST':
        if current_step == 1:
            form = ForgotPasswordStep1Form(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = CustomUser.objects.filter(email=email).first()

                if user:
                    # Gerar código de verificação
                    verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                    user.reset_password_token = verification_code
                    user.reset_password_token_created = timezone.now()
                    user.save()

                    # Enviar email com o código
                    try:
                        send_mail(
                            'Código de Verificação',
                            f'Seu código de verificação é: {verification_code}',
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                            fail_silently=False,
                        )
                        request.session['user_email'] = email
                        request.session['forgot_password_step'] = 2
                        return redirect('forgot_password')
                    except Exception as e:
                        form.add_error(None, 'Erro ao enviar email. Tente novamente.')
                else:
                    form.add_error('email', 'Email não encontrado.')

        elif current_step == 2:
            form = ForgotPasswordStep2Form(request.POST)
            if form.is_valid():
                verification_code = form.cleaned_data['verification_code']
                email = request.session.get('user_email')

                if email:
                    user = CustomUser.objects.filter(email=email, reset_password_token=verification_code).first()
                    if user and timezone.now() - user.reset_password_token_created <= timedelta(minutes=15):
                        request.session['forgot_password_step'] = 3
                        return redirect('forgot_password')
                    else:
                        form.add_error('verification_code', 'Código inválido ou expirado.')

        elif current_step == 3:
            form = ForgotPasswordStep3Form(request.POST)
            if form.is_valid():
                email = request.session.get('user_email')
                if email:
                    user = CustomUser.objects.filter(email=email).first()
                    if user:
                        user.set_password(form.cleaned_data['new_password'])
                        user.reset_password_token = None
                        user.reset_password_token_created = None
                        user.save()

                        # Limpar a sessão
                        del request.session['forgot_password_step']
                        del request.session['user_email']
                        return redirect('login')

    # Renderizar o formulário apropriado baseado no step atual
    if request.method == 'GET':
        if current_step == 1:
            form = ForgotPasswordStep1Form()
        elif current_step == 2:
            form = ForgotPasswordStep2Form()
        else:
            form = ForgotPasswordStep3Form()

    return render(request, 'resetPassword.html', {
        'form': form,
        'current_step': current_step,
        'total_steps': 3
    })


    
