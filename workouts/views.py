from django.shortcuts import render, redirect
from .models import WorkoutDate, Workout, Exercise
from .forms import WorkoutDateForm, WorkoutForm, ExerciseFormSet, ExerciseForm

def home(request):
    return render(request, 'landing.html')

def log(request):
    if request.method == 'POST':
        # Handling the form submission
        date_form = WorkoutDateForm(request.POST)
        workout_form = WorkoutForm(request.POST)
        formset = ExerciseFormSet(request.POST)

        if date_form.is_valid() and workout_form.is_valid() and formset.is_valid():
            # Save WorkoutDate instance
            workout_date, _ = WorkoutDate.objects.get_or_create(
                date=date_form.cleaned_data['date']
            )

            # Save Workout instance
            workout = workout_form.save(commit=False)
            workout.date = workout_date
            workout.save()

            # Save Exercise instances
            formset.instance = workout
            formset.save()

            return redirect('view')  # Redirect to the view workouts page
    else:
        # Handling GET request
        date_form = WorkoutDateForm()
        workout_form = WorkoutForm()

        # Initialize formset with no exercises initially
        formset = ExerciseFormSet(queryset=Exercise.objects.none())  # Empty formset initially

        # If formset has no forms (i.e., it's empty), add one form to the formset
        if not formset.forms:  # If the formset is empty, add one form
            formset.forms.append(ExerciseForm())

    # Pass the forms to the template for rendering
    return render(request, 'log_workout.html', {
        'date_form': date_form,
        'workout_form': workout_form,
        'formset': formset,
    })


def view(request):
    workout_dates = WorkoutDate.objects.prefetch_related('workouts__exercises')
    return render(request, 'view_workouts.html', {'workout_dates': workout_dates})
