from django.db import models

from theatre_service import settings


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", related_name="plays", blank=True)
    genres = models.ManyToManyField("Genre", related_name="plays", blank=True)

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return f"{self.row} {self.seat} {self.performance}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)
