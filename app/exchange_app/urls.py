from django.urls import path
from .views import exhange

urlpatterns = [
    path('', exhange)
]