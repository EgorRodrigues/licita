from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Licitacao, Empresa, EmpresaLicita

from funcoes.script_py.scripts import importar_licitacoes


class Relatorio(View):
    def get(self, request, *args, **kwargs):
        lista = Licitacao.objects.all()
        return render(request, 'budgets.html', {'Nome': lista})

    def post(self, request, *args, **kwargs):
        return HttpResponse('Deu Certo!')


class LicitaList(ListView):
    model = Licitacao


class LicitaDetail(DetailView):
    model = Licitacao


class LicitaCreate(CreateView):
    model = Licitacao
    fields = [
        'id_conlicitacao',
    ]

    def post(self, request, *args, **kwargs):
        bidding = importar_licitacoes(request.POST['id_conlicitacao'].split())
        return HttpResponse(bidding)