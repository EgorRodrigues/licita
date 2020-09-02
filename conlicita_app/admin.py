from django.contrib import admin
from conlicita_app.models import Licitacao, Empresa, EmpresaLicita


class LicitacaoAdmin(admin.ModelAdmin):
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

class LicitaEmpresaAdmin(admin.ModelAdmin):
    fields = (
        'licitacao',
        'empresa',
    )


admin.site.register(Licitacao, LicitacaoAdmin)
admin.site.register(Empresa)
admin.site.register(EmpresaLicita, LicitaEmpresaAdmin)