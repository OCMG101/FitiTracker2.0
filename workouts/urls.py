from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/', views.log, name='log'),
    path('view/', views.view, name='view'),
    path('get_exercises_by_category/', views.get_exercises_by_category, name='get_exercises_by_category'),
    path('get_workout_template/', views.get_workout_template, name='get_workout_template'),
]
