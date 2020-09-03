from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Licitacao, Empresa, EmpresaLicita


class Relatorio(View):
    def get(self, request, *args, **kwargs):
        lista = Licitacao.objects.all()
        return render(request, 'budgets.html', {'Nome': lista})

    def post(self, request, *args, **kwargs):
        return HttpResponse('Deu Certo!')


class LicitaList(ListView):
    model = Licitacao

    def post(self, request, *args, **kwargs):
        return HttpResponse('ok deu certo também')


def budgets(request):
    return render(request, 'budgets.html', {'Nome': 'Egor'})
