from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from pathlib import Path
from .models import WorkoutDate, Workout, Exercise, WorkoutTemplate, TemplateExercise
from .forms import WorkoutDateForm, WorkoutForm, ExerciseFormSet, ExerciseForm


def home(request):
    """Landing page"""
    return render(request, 'home.html')


BASE_DIR = Path(__file__).resolve().parent
EXERCISE_FILE = BASE_DIR / "data" / "exercises.json"


def get_exercise_data():
    with open(EXERCISE_FILE, "r") as f:
        return json.load(f)


def get_exercises_by_category(request):
    category = request.GET.get("category")
    data = get_exercise_data()
    exercises = data.get(category, [])
    return JsonResponse(exercises, safe=False)


def get_workout_template(request):
    """Fetch saved exercises for a workout name"""
    name = request.GET.get("name")
    try:
        template = WorkoutTemplate.objects.get(name=name)
        exercises = list(template.template_exercises.values("exercise_name", "sets", "reps", "weight"))
        return JsonResponse(exercises, safe=False)
    except WorkoutTemplate.DoesNotExist:
        return JsonResponse([], safe=False)


def log(request):
    if request.method == 'POST':
        date_form = WorkoutDateForm(request.POST)
        workout_form = WorkoutForm(request.POST)
        formset = ExerciseFormSet(request.POST)

        if date_form.is_valid() and workout_form.is_valid() and formset.is_valid():
            workout_date, _ = WorkoutDate.objects.get_or_create(
                date=date_form.cleaned_data['date']
            )
            workout = workout_form.save(commit=False)
            workout.date = workout_date
            workout.save()
            formset.instance = workout
            formset.save()

            # Save workout as template for future use
            template, _ = WorkoutTemplate.objects.get_or_create(name=workout.name)
            template.template_exercises.all().delete()  # refresh memory
            for form in formset:
                if form.cleaned_data:
                    TemplateExercise.objects.create(
                        template=template,
                        exercise_name=form.cleaned_data.get("exercise_name"),
                        sets=form.cleaned_data.get("sets", 0),
                        reps=form.cleaned_data.get("reps", 0),
                        weight=form.cleaned_data.get("weight", 0.0)
                    )

            return redirect('view')

    else:
        date_form = WorkoutDateForm()
        workout_form = WorkoutForm()
        formset = ExerciseFormSet(queryset=Exercise.objects.none())

    categories = get_exercise_data().keys()
    return render(request, 'log_workout.html', {
        'date_form': date_form,
        'workout_form': workout_form,
        'formset': formset,
        'categories': categories,
    })


def view(request):
    workout_dates = WorkoutDate.objects.prefetch_related('workouts__exercises')
    return render(request, 'view_workouts.html', {'workout_dates': workout_dates})
