from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django.urls import re_path
from django.views.static import serve


from . import views

urlpatterns = [
    path('licita/relatorio/', views.Relatorio.as_view()),
    path('licita/list/', views.LicitaList.as_view(), name='licita_list'),
    path('licita/create/', views.LicitaCreate.as_view(), name='licita_create'),
    path('licita/import/', views.LicitaImport.as_view(), name='licita_import'),
    path('licita/update/<int:pk>', views.LicitaUpdate.as_view(), name='licita_update'),
    path('licita/detail/<int:pk>', views.LicitaDetail.as_view(), name='licita_detail'),
    path('licita/delete/<int:pk>', views.LicitaDelete.as_view(), name='licita_delete'),
    path('empresa/import/', views.EmpresaImport.as_view(), name='empresa_import'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^arquivos/(?P<path>.*)$', serve, {
#             'document_root':settings.MEDIA_ROOT,
#         }),
#     ]
