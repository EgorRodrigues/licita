from django.db import models


# todo Inserir os campos multiplos
class Licitacao(models.Model):
    id_conlicitacao = models.IntegerField()
    orgao_uasg = models.CharField(max_length=6, null=True, blank=True)
    orgao_endereco = models.CharField(max_length=150, null=True, blank=True)
    orgao_cidade = models.CharField(max_length=50, null=True, blank=True)
    orgao_estado = models.CharField(max_length=2, null=True, blank=True)
    orgao_cep = models.CharField(max_length=9, null=True, blank=True)
    edital = models.CharField(max_length=20, null=True, blank=True)
    edital_site = models.URLField(max_length=255, null=True, blank=True)
    edital_homepage = models.CharField(max_length=255, null=True, blank=True)
    edital_homepage2 = models.CharField(max_length=255, null=True, blank=True)
    edital_preco = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    edital_tem = models.BooleanField()
    edital_status_id = models.DecimalField(max_digits=1, decimal_places=0, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    processo = models.CharField(max_length=50, null=True, blank=True)
    valor_estimado = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    itens = models.TextField(null=True, blank=True)
    datahora_prazo = models.DateTimeField(null=True, blank=True)
    datahora_abertura = models.DateTimeField(null=True, blank=True)
    datahora_retirada = models.DateTimeField(null=True, blank=True)
    datahora_visita = models.DateTimeField(null=True, blank=True)
    datahora_documento = models.DateTimeField(null=True, blank=True)
    data_validade = models.DateField(null=True, blank=True)
    objeto = models.TextField()
    observacao = models.TextField()
    modified = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    bidding_id = models.IntegerField()
    # edicts =
    has_electronic_trading = models.BooleanField()
    # bidding_grouping =
    # phones =
    # faxes =
    public_body = models.CharField(max_length=150, null=True, blank=True)
    modality = models.CharField(max_length=150, null=True, blank=True)
    # followups =
    arquivo_edital = models.FileField(null=True, blank=True)

    class Meta:
        unique_together = ['id_conlicitacao']
        verbose_name_plural = 'licitações'
        ordering = ['data_validade']

    def __str__(self):
        return f'{self.data_validade.strftime("%d/%m/%Y")} - {self.public_body} | {self.modality}'


# todo Inserir campos relacionados como Sócios
class Empresa(models.Model):
    razao_social = models.CharField(max_length=150)
    cnpj = models.IntegerField()
    endereco = models.CharField(max_length=150, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    situacao = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)
    natureza = models.CharField(max_length=50, null=True, blank=True)
    abertura = models.DateField(null=True, blank=True)
    capital_social = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    # sócios =
    segmento = models.TextField(null=True, blank=True)
    my_bidding = models.ManyToManyField(Licitacao, through='EmpresaLicita',
                                     related_name='licita_list', blank=True)

    class Meta:
        unique_together = ['cnpj']

    def __str__(self):
        return f'{self.cnpj} - {self.razao_social}'

class EmpresaLicita(models.Model):
    STATUS_CHOICE = (
        ('1', 'Participar'),
        ('2', 'Acompanhar'),
        ('3', 'Descartar'),
    )

    licitacao = models.ForeignKey(Licitacao, related_name='licitacao_empresa', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, related_name='licitacao_empresa', on_delete=models.CASCADE)
    observacao = models.CharField(max_length=255, null=True, blank=True)

    # Sobre a Habilitação:
    visita_tecnica = models.NullBooleanField(verbose_name='visita técnica')
    garantia_proposta = models.NullBooleanField(verbose_name='garantia de proposta')
    qualificacao_tecnica = models.NullBooleanField(verbose_name='qualificação técnica')
    consorcio = models.NullBooleanField(verbose_name='cabe consórcio?')
    cadastro = models.NullBooleanField(verbose_name='fazer cadastro?')

    # Sobre a Proposta:
    orcamento_data_base = models.DateField(verbose_name='data base da planilha', null=True, blank=True)
    prazo_execucao = models.CharField(max_length=50, verbose_name='prazo de execução da obra', null=True, blank=True)

    # Gestão das Licitações
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, blank=True, null=True)


