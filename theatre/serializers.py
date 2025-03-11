from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from theatre.models import Actor, Genre, TheatreHall, Play, Performance, Ticket, Reservation


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PlaySerializer(serializers.ModelSerializer):
    actors = SlugRelatedField(many=True, read_only=True, slug_field="full_name")
    genres = SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class PlayDetailSerializer(PlaySerializer):
    performances = SlugRelatedField(many=True, read_only=True, slug_field="show_time")

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields + ("performances",)


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")

