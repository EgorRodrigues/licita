from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django.urls import re_path
from django.views.static import serve


from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('list/', views.LicitaList.as_view(), name='licita_list'),
    path('create/', views.LicitaCreate.as_view(), name='licita_create'),
    path('import/', views.LicitaImport.as_view(), name='licita_import'),
    path('update/<int:pk>', views.LicitaUpdate.as_view(), name='licita_update'),
    path('detail/<int:pk>', views.LicitaDetail.as_view(), name='licita_detail'),
    path('delete/<int:pk>', views.LicitaDelete.as_view(), name='licita_delete'),
    path('empresa/import/', views.EmpresaImport.as_view(), name='empresa_import'),
    path('empresa/', views.EmpresaList.as_view(), name='empresa_list'),
    path('empresa/detail/<int:pk>', views.EmpresaList.as_view(), name='empresa_detail'),
    path('empresa/licita/delete/<int:pk>', views.EmpresaLicitaDelete.as_view(), name='empresalicita_delete'),
    path('empresa/select/', views.EmpresaLicitaSelect.as_view(), name='empresa_select'),
    path('minhas/licitacoes/<int:pk>', views.Minhaslicitacoes.as_view(), name='minhas_licitacoes'),
    path('licitacoes/list', views.EmpresaLicitaList.as_view(), name='lista_de_licitacoes'),
    path('empresa/licita/list', views.EmpresaLicitaList.as_view(), name='get_lista_de_licitacoes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^arquivos/(?P<path>.*)$', serve, {
#             'document_root':settings.MEDIA_ROOT,
#         }),
#     ]
