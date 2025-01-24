from django import forms
from django.forms import inlineformset_factory
from .models import WorkoutDate, Workout, Exercise

class WorkoutDateForm(forms.ModelForm):
    class Meta:
        model = WorkoutDate
        fields = ['date']
        widgets = {
             'date': forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY', 'type': 'text'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%d-%m-%Y']


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name']


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_name', 'sets', 'reps', 'weight']
        labels = {
            'weight': 'Weight(kg)'
        }


# Inline formset for managing exercises related to a workout
ExerciseFormSet = inlineformset_factory(
    Workout, Exercise, 
    form=ExerciseForm, 
    extra=1,
    can_delete=False
    )
