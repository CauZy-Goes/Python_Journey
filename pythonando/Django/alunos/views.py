from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Aluno

# Create your views here.

def criar_aluno(request):

    if request.method == 'GET' : 
        status = request.GET.get('status')
        alunos = Aluno.objects.all()
        return render(request,'criar_aluno.html', {'status':status, 'alunos':alunos})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        email = request.POST.get('email')

        if len(nome.strip()) == 0 or int(idade) < 0:
            return redirect ('/aluno/criar_aluno/?status=1')

        aluno = Aluno (
            nome=nome,
            idade=idade,
            email=email
        )

        aluno.save()

        return redirect('/aluno/criar_aluno/?status=0')

def listar_aluno(request):
    return HttpResponse("estou listando")

def deletar_aluno(request, id):
    aluno = Aluno.objects.get(id=id)
    aluno.delete()
    return redirect('criar_aluno')