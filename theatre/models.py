from django.db import models


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name='performances')
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE, related_name='performances')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} in {self.theatre_hall.name} at {self.show_time}"
