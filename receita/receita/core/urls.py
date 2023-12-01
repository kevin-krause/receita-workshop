from django.urls import path
from .views import busca_receita, index, empresa_detail

urlpatterns = [
    path('busca-receita/', busca_receita, name='busca_receita'),
    path('empresa/<int:pk>/', empresa_detail, name='empresa_detail'),
    path('', index, name='index'),
]