from django.urls import path
from .views import CustomLogin

urlpatterns = [
    path('login/', CustomLogin.as_view(), name='login'),
]