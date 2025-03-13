from django.db.models import F, Count
from rest_framework import viewsets

from theatre.models import Actor, Genre, TheatreHall, Play, Performance, Reservation, Ticket
from theatre.serializers import ActorSerializer, GenreSerializer, TheatreHallSerializer, PlaySerializer, \
    PerformanceSerializer, ReservationSerializer, TicketSerializer, PlayDetailSerializer, PlayListSerializer, \
    TheatreHallDetailSerializer, PerformanceListSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TheatreHallDetailSerializer
        return TheatreHallSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "list":
            return PlayListSerializer
        return PlaySerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
