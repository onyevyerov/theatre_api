from django.contrib import admin

from theatre.models import (
    Actor,
    Play,
    Genre,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
)

admin.site.register(Play)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Ticket)
admin.site.register(Reservation)
