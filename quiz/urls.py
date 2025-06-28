from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/<int:score>/<int:total>/', views.result, name='result'),
]
