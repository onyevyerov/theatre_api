from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from theatre.models import (
    Actor,
    Genre,
    TheatreHall,
    Play,
    Performance,
    Ticket,
    Reservation,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlayImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("id", "image")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(read_only=True, source="play.title")
    theatre_hall = serializers.CharField(
        read_only=True,
        source="theatre_hall.name"
    )
    theatre_hall_capacity = serializers.IntegerField(
        read_only=True, source="theatre_hall.capacity"
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play_title",
            "theatre_hall",
            "theatre_hall_capacity",
            "tickets_available",
        )


class PerformanceHallSerializer(serializers.ModelSerializer):
    play = SlugRelatedField(many=False, read_only=True, slug_field="title")

    class Meta:
        model = Performance
        fields = ("id", "play", "show_time")


class TheatreHallDetailSerializer(TheatreHallSerializer):
    performances = PerformanceHallSerializer(many=True, read_only=True)

    class Meta:
        model = TheatreHall
        fields = TheatreHallSerializer.Meta.fields + ("performances",)


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres", "image")


class PlayListSerializer(serializers.ModelSerializer):
    genres = SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres", "image")


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall")


class PlayDetailSerializer(serializers.ModelSerializer):
    performances = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="show_time"
    )
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres",
            "image",
            "performances",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketListSerializer(serializers.ModelSerializer):
    performance = PerformanceHallSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")
