from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Licitacao, Empresa, EmpresaLicita, UserEmpresa

from funcoes.script_py.scripts import importar_licitacoes, importar_empresas


class Home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'conlicita_app/home.html')


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

    def get_success_url(self):
        bid = Licitacao.objects.get(id_conlicitacao=self.request.POST['id_conlicitacao'])
        return reverse_lazy('licita_detail', kwargs={'pk': bid.id})


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


class LicitaImport(LoginRequiredMixin, CreateView):
    model = Licitacao
    fields = [
        'id_conlicitacao',
    ]

    def post(self, request, *args, **kwargs):
        importar_licitacoes(self.request.POST['id_conlicitacao'].split())
        bid = Licitacao.objects.get(id_conlicitacao=request.POST['id_conlicitacao']).id
        return redirect(f'../detail/{bid}')


class EmpresaImport(LoginRequiredMixin, CreateView):
    model = Empresa
    fields = ['cnpj']

    def post(self, request, *args, **kwargs):
        empresa = importar_empresas(request.POST['cnpj'].split())
        return HttpResponse(empresa)


class EmpresaList(LoginRequiredMixin, ListView):
    model = Empresa


class EmpresaLicitaSelect(LoginRequiredMixin, CreateView):
    model = EmpresaLicita
    fields = [
        'licitacao', 'empresa', 'observacao','visita_tecnica', 'garantia_proposta',
        'qualificacao_tecnica', 'consorcio', 'cadastro', 'orcamento_data_base',
        'prazo_execucao', 'status',
    ]

    def get_success_url(self):
        empresa = self.request.POST['empresa']
        return reverse_lazy('minhas_licitacoes', kwargs={'pk': empresa})


class EmpresaLicitaDelete(LoginRequiredMixin, DeleteView):
    model = EmpresaLicita

    def get_success_url(self):
        empresa = self.object.empresa.id
        return reverse_lazy('minhas_licitacoes', kwargs={'pk': str(empresa)})


class EmpresaDetail(LoginRequiredMixin, DetailView):
    model = Empresa


class Minhaslicitacoes(LoginRequiredMixin, View):
    def get(self, request, pk):
        empresa = Empresa.objects.get(id=pk)
        my_bidding = empresa.licitacao_empresa.all()
        return render(request, 'conlicita_app/minhalicitacao_list.html', {'object_list': my_bidding})


class EmpresaLicitaList(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        empresa = user.user_empresa.empresa
        return HttpResponse(empresa)

    def post(self, request, *args, **kwargs):
        bidding = dict(request.POST)
        for key in bidding.keys():
            if bidding[key][0] == 'unknown':
                bidding[key] = None
            elif bidding[key][0] == 'true':
                bidding[key] = True
            elif bidding[key][0] == 'false':
                bidding[key] = False
        if not bidding['orcamento_data_base'][0]:
            bidding['orcamento_data_base'] = None
        else:
            bidding['orcamento_data_base'] = datetime.strptime(bidding['orcamento_data_base'][0], '%d/%m/%Y')
        EmpresaLicita(
            licitacao=Licitacao.objects.get(pk=bidding['licitacao'][0]),
            empresa=Empresa.objects.get(pk=bidding['empresa'][0]),
            observacao=bidding['observacao'][0],
            visita_tecnica=bidding['visita_tecnica'], # Boolean
            garantia_proposta=bidding['garantia_proposta'], # Boolean
            qualificacao_tecnica=bidding['qualificacao_tecnica'], # Boolean
            consorcio=bidding['consorcio'], # Boolean
            cadastro=bidding['cadastro'], # Boolean
            orcamento_data_base=bidding['orcamento_data_base'],
            prazo_execucao=bidding['prazo_execucao'][0],
            status=bidding['status'][0]
        ).save()

        return redirect(f"../minhas/licitacoes/{bidding['empresa'][0]}")


class LicitaSelect(LoginRequiredMixin, View):

    def get(self):
        pass

    def post(self, request):
        user = User.objects.get(username=request.user)
        empresa = user.user_empresa.empresa
        licitacao = request
        EmpresaLicita(
            licitacao=licitacao,
            empresa=empresa,
        ).save()

        return redirect('')

