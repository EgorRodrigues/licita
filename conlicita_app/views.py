from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Licitacao, Empresa, EmpresaLicita

from funcoes.script_py.scripts import importar_licitacoes, importar_empresas


class Relatorio(View):
    def get(self, request, *args, **kwargs):
        lista = Licitacao.objects.all()
        return render(request, 'budgets.html', {'Nome': lista})

    def post(self, request, *args, **kwargs):
        return HttpResponse('Deu Certo!')


class LicitaList(LoginRequiredMixin, ListView):
    model = Licitacao


class LicitaDetail(LoginRequiredMixin, DetailView):
    model = Licitacao


class LicitaCreate(LoginRequiredMixin, CreateView):
    model = Licitacao
    fields = [
        'id_conlicitacao', 'orgao_uasg', 'orgao_endereco',
        'orgao_cidade', 'orgao_estado', 'orgao_cep',
        'edital', 'edital_site', 'edital_homepage',
        'edital_homepage2', 'edital_preco', 'edital_tem',
        'edital_status_id', 'email', 'processo',
        'valor_estimado', 'itens', 'datahora_prazo',
        'datahora_abertura', 'datahora_retirada', 'datahora_visita',
        'datahora_documento', 'data_validade', 'objeto',
        'observacao', 'modified', 'created', 'bidding_id',
        'has_electronic_trading', 'public_body', 'modality',
        'arquivo_edital',
    ]

    def post(self, request, *args, **kwargs):
        bidding = importar_licitacoes(request.POST['id_conlicitacao'].split())
        return HttpResponse(bidding)


class LicitaUpdate(LoginRequiredMixin, UpdateView):
    model = Licitacao
    fields = [
        'id_conlicitacao', 'orgao_uasg', 'orgao_endereco',
        'orgao_cidade', 'orgao_estado', 'orgao_cep',
        'edital', 'edital_site', 'edital_homepage',
        'edital_homepage2', 'edital_preco', 'edital_tem',
        'edital_status_id', 'email', 'processo',
        'valor_estimado', 'itens', 'datahora_prazo',
        'datahora_abertura', 'datahora_retirada', 'datahora_visita',
        'datahora_documento', 'data_validade', 'objeto',
        'observacao', 'modified', 'created', 'bidding_id',
        'has_electronic_trading', 'public_body', 'modality',
        'arquivo_edital',
    ]

    def get_success_url(self):
        return reverse_lazy('licita_detail', kwargs={'pk': self.object.id})


class LicitaDelete(LoginRequiredMixin, DeleteView):
    model = Licitacao
    success_url = reverse_lazy('licita_list')


class EmpresaImport(LoginRequiredMixin, CreateView):
    model = Empresa
    fields = ['cnpj']

    def post(self, request, *args, **kwargs):
        empresa = importar_empresas(request.POST['cnpj'].split())
        return HttpResponse(empresa)
