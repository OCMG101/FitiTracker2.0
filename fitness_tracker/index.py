from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'landing.html')

def log(request):
    return render(request, 'log_workout.html')

def view(request):
    return render(request, 'view_workouts.html')