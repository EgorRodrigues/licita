from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.budgets, name='budgets'),
    path('relatorio/', views.Relatorio.as_view()),
    path('licitacao_list/', views.LicitaList.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
