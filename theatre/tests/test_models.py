from datetime import datetime


from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import localtime

from theatre.models import Play, Actor, Genre, TheatreHall, Performance, Reservation, Ticket
from user.models import User


class PlayModelTest(TestCase):

    def test_play_str(self):
        play = Play.objects.create(
            title="TestTitle",
            description="TestDescription",
        )
        self.assertEqual(str(play), "TestTitle")


class ActorModelTest(TestCase):

    def test_full_name_property(self):
        actor = Actor.objects.create(
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(actor.full_name, "John Doe")
        self.assertEqual(str(actor), "John Doe")


class GenreModelTest(TestCase):

    def test_genre_str(self):
        genre = Genre.objects.create(
            name="Test"
        )
        self.assertEqual(str(genre), "Test")


class TheatreHallModelTest(TestCase):
    hall = TheatreHall.objects.create(
        name="TestHall",
        rows=3,
        seats_in_row=3
    )

    def test_capacity_property(self):
        self.assertEqual(self.hall.capacity, 9)

    def test_capacity_str(self):
        self.assertEqual(str(self.hall), "TestHall")


class PerformanceModelTest(TestCase):

    def setUp(self):
        self.hall = TheatreHall.objects.create(
            name="TestHall",
            rows=3,
            seats_in_row=3
        )
        self.play = Play.objects.create(
            title="TestTitle",
            description="TestDescription",
        )

    def test_performance_str(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 1, 1, 18, 0)
        )
        self.assertEqual(str(performance), f"TestTitle in TestHall at 2025-01-01 18:00:00")


class TicketModelTest(TestCase):

    def setUp(self):
        self.play = Play.objects.create(
            title="TestTitle",
            description="TestDescription",
        )
        self.hall = TheatreHall.objects.create(
            name="TestHall",
            rows=3,
            seats_in_row=3
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 1, 1, 18, 0)
        )
        self.user = User.objects.create_user(
            email="test@test.pl",
            password="testpass",
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
        )

    def test_ticket_clean_valid(self):
        """Test that valid Ticket instance pass validation"""
        ticket = Ticket(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation,
        )
        ticket.full_clean()

    def test_ticket_seat_invalid(self):
        """Test that Ticket instance with invalid seat number don`t pass validation"""
        ticket = Ticket(
            row=1,
            seat=5,
            performance=self.performance,
            reservation=self.reservation,
        )
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_row_invalid(self):
        """Test that Ticket instance with invalid row number don`t pass validation"""
        ticket = Ticket(
            row=5,
            seat=1,
            performance=self.performance,
            reservation=self.reservation,
        )
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_uniq_constraints(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation,
        )
        duplicate_ticket = Ticket(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation,
        )
        with self.assertRaises(ValidationError):
            duplicate_ticket.full_clean()

    def test_ticket_str(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation,
        )
        self.assertEqual(str(ticket), "TestTitle in TestHall at 2025-01-01 18:00:00 (seat: 1, row: 1)")


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.pl",
            password="<PASSWORD>",
        )

    def test_reservation_str(self):
        reservation = Reservation.objects.create(user=self.user)
        expected_str = localtime(reservation.created_at).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(str(reservation), expected_str)