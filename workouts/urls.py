from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log_workout/', views.log, name='log'),
    path('view_workouts/', views.view, name='view'),
]

