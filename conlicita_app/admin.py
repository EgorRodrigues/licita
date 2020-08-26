from django.contrib import admin
from conlicita_app.models import licitacao, empresa


class licitacaoAdmin(admin.ModelAdmin):
    list_display = ('id_conlicitacao', 'data_validade', 'public_body', 'modality', 'objeto', 'valor_estimado')




admin.site.register(licitacao, licitacaoAdmin)
admin.site.register(empresa)