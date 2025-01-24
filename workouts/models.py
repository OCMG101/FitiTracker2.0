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
