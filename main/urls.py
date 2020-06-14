from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('result', views.result, name='result'),
    path('describle', views.describle, name='describle'),
]
