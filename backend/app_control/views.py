from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Devolucao
from .forms import DevolucaoForm
from concurrent.futures import ThreadPoolExecutor

def update_statuses(devolucoes):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda devolucao: devolucao.update_status(), devolucoes)

def index(request):
    devolucoes = Devolucao.objects.all()
    update_statuses(devolucoes)
    if request.method == 'POST':
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        elif 'action' in request.POST and request.POST['action'] == 'Atualizar':
            update_statuses(devolucoes)
    else:
        form = DevolucaoForm()
    return render(request, 'index.html', {'form': form, 'devolucoes': devolucoes})


def atualizar_devolucoes(request):
    devolucoes = Devolucao.objects.all()
    print(devolucoes)
    update_statuses(devolucoes)
    data = []
    for devolucao in devolucoes:
        data.append({
            'codigo_sedex': devolucao.codigo_sedex,
            'data': devolucao.data.strftime('%d/%m/%Y'),
            'notas_devolucao': ', '.join(devolucao.notadevolucao_set.values_list('nota', flat=True)),
            'status': devolucao.status,
            'email': devolucao.email,
        })
    print(data)
    print(request)
    return JsonResponse(data, safe=False)