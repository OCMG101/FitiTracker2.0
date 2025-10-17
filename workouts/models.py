from django.db import models

class WorkoutDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)


class Workout(models.Model):
    date = models.ForeignKey(WorkoutDate, related_name='workouts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='exercises', on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return self.exercise_name


# Memory system for reusing workout structures
class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class TemplateExercise(models.Model):
    template = models.ForeignKey(WorkoutTemplate, related_name='template_exercises', on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255)
    sets = models.PositiveIntegerField(default=0)
    reps = models.PositiveIntegerField(default=0)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.exercise_name} ({self.sets}x{self.reps})"
