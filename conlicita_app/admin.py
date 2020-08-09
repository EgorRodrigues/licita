from django.contrib import admin
from conlicita_app.models import licitacao


class licitacaoAdmin(admin.ModelAdmin):
    list_display = ('data_validade', 'public_body', 'modality', 'valor_estimado')


admin.site.register(licitacao, licitacaoAdmin)