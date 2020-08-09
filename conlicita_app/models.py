from django.db import models

# Create your models here.

class licitacao(models.Model):
    id_conlicitacao = models.IntegerField()
    orgao_uasg = models.CharField(max_length=6, null=True, blank=True)
    orgao_endereco = models.CharField(max_length=150, null=True, blank=True)
    orgao_cidade = models.CharField(max_length=50, null=True, blank=True)
    orgao_estado = models.CharField(max_length=2, null=True, blank=True)
    orgao_cep = models.CharField(max_length=9, null=True, blank=True)
    edital = models.CharField(max_length=20, null=True, blank=True)
    edital_site = models.CharField(max_length=255, null=True, blank=True)
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

    def __str__(self):
        return f'{self.data_validade} - {self.orgao_uasg}'