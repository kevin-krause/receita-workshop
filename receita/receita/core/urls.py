from django.urls import path
from .views import busca_receita

urlpatterns = [
    path('busca-receita/', busca_receita, name='busca_receita'),
]