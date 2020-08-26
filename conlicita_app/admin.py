from django.contrib import admin
from conlicita_app.models import licitacao, empresa


class licitacaoAdmin(admin.ModelAdmin):
    list_display = ('data_validade', 'public_body', 'modality', 'edital', 'objeto', 'valor_estimado')
    fields = (
        'data_validade',
        (
            'public_body',
            'modality',
            'edital',
        ),
        'objeto',
        'valor_estimado',
        'arquivo_edital',
        'edital_site',
    )



admin.site.register(licitacao, licitacaoAdmin)
admin.site.register(empresa)