from django.shortcuts import render, redirect
from .models import Tarefa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime

# View para a página inicial, com tarefas do usuário logado
@login_required
def home(request):
    # Filtra as tarefas com o id do usuário logado
    logout(request)
    
    tarefaLista = Tarefa.objects.filter(idUser=request.user)
    return render(request, 'home.html', {'tarefaLista': tarefaLista})

# View para criar uma nova tarefa
@login_required
def create(request):
    if request.method == "GET":
        return render(request, 'create.html')

    nomeTarefa = request.POST.get('nomeTarefa')
    dataTarefa = request.POST.get('data')
    descricao = request.POST.get('descricao')

    # Verificando se os campos estão preenchidos
    if not nomeTarefa or not dataTarefa or not descricao:
        messages.error(request, 'Todos os campos devem ser preenchidos!')
        return render(request, 'create.html')

    try:
        # Tentando converter a data
        dataTarefa = datetime.strptime(dataTarefa, '%Y-%m-%d')  # ou o formato que você precisar
    except ValueError:
        messages.error(request, 'Formato de data inválido. Use AAAA-MM-DD.')
        return render(request, 'create.html')

    # Criando e salvando a tarefa
    tarefa = Tarefa.objects.create(
        nomeTarefa=nomeTarefa,
        dataTarefa=dataTarefa,
        descricao=descricao,
        idUser=request.user
    )
    tarefa.save()

    messages.success(request, 'Tarefa criada com sucesso!')
    return redirect('index')  # Redirecionando para a página inicial

@login_required
def delete(request, id):
    tarefa = Tarefa.objects.get(id=id)
    if tarefa.idUser != request.user:
        return redirect('index')  # Redirecionando para a página inicial caso a tarefa não seja do usuário logado
    tarefa.delete()
    messages.success(request, 'Tarefa excluída com sucesso!')
    return redirect('index')  # Redirecionando para a página inicial

@login_required
def update(request, id):
    # Obtém a tarefa com o ID fornecido
    tarefa = Tarefa.objects.get(id=id)

    # Verifica se a tarefa pertence ao usuário logado
    if tarefa.idUser != request.user:
        return redirect('index')  # Redireciona para a página inicial caso a tarefa não seja do usuário logado
    
    # Converte a data para o formato 'YYYY-MM-DD'
    dataTarefa = tarefa.dataTarefa.strftime('%Y-%m-%d')  # Usa o método strftime para formatar a data
    if request.method == 'GET':

        # Retorna o template com os dados da tarefa e a data formatada
        return render(request, 'update.html', {'tarefa': tarefa, 'dataTarefa': dataTarefa})
    
    tarefa.status = 1 if request.POST.get('status') == 'True' else 0
    tarefa.nomeTarefa = request.POST.get('nomeTarefa')
    tarefa.dataTarefa = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
    tarefa.descricao = request.POST.get('descricao')
    tarefa.save()
    
    return redirect('index')
