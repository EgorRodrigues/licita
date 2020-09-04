from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('licitacao_list/', views.LicitaList.as_view()),
    path('licita/create/', views.LicitaCreate.as_view(), name='licita_create'),
    path('licita/detail/<int:pk>', views.LicitaDetail.as_view(), name='licita_detail')
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
