import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import PlayListSerializer

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample play",
        "description": "Sample description"
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(name="Blue", rows=20, seats_in_row=20)

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def image_upload_url(play_id):
    """Return URL for recipe image upload"""
    return reverse("theatre:play-upload-image", args=[play_id])


def play_detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


def performance_detail_url(play_id):
    return reverse("theatre:performance-detail", args=[play_id])


class PlayImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.play = sample_play()
        self.genre = sample_genre()
        self.actor = sample_actor()
        self.performance = sample_performance(play=self.play)

    def tearDown(self):
        self.play.image.delete()

    def test_upload_image_to_play(self):
        """Test uploading an image to play"""
        url = image_upload_url(self.play.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.play.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.play.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.play.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_url_is_shown_on_play_detail(self):
        url = image_upload_url(self.play.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(play_detail_url(self.play.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_performance_detail(self):
        url = image_upload_url(self.play.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(performance_detail_url(self.performance.id))

        self.assertIn("image", res.data["play"])

    def test_image_url_is_shown_on_play_list(self):
        url = image_upload_url(self.play.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(PLAY_URL)

        self.assertIn('image', res.data["results"][0])


class UnauthorizedApiTests(TestCase):
    def test_authorization_required(self):
        self.client = APIClient()
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="<EMAIL>", password="<PASSWORD>"
        )
        self.client.force_authenticate(self.user)

    def test_get_play_list(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_play_detail(self):
        play = sample_play()
        res = self.client.get(play_detail_url(play.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_play_filtered_by_actors(self):
        actor_1 = Actor.objects.create(first_name="George", last_name="Clooney")
        actor_2 = Actor.objects.create(first_name="George", last_name="Clooney")

        play_without_actor = sample_play()
        play_with_actor_1 = sample_play(title="Test")
        play_with_actor_2 = sample_play(title="Test1")

        play_with_actor_1.actors.add(actor_1)
        play_with_actor_2.actors.add(actor_2)

        serializer_without_actor = PlayListSerializer(play_without_actor)
        serializer_with_actor_1 = PlayListSerializer(play_with_actor_1)
        serializer_with_actor_2 = PlayListSerializer(play_with_actor_2)

        res = self.client.get(PLAY_URL, {"actors": f"{actor_1.id},{actor_2.id}"})  # ?actors=1,2

        self.assertNotIn(serializer_without_actor.data, res.data["results"])
        self.assertIn(serializer_with_actor_1.data, res.data["results"])
        self.assertIn(serializer_with_actor_2.data, res.data["results"])

    def test_get_play_filtered_by_genres(self):
        genre_1 = Genre.objects.create(name="Drama")
        genre_2 = Genre.objects.create(name="Comedy")

        play_without_genre = sample_play()
        play_with_genre_1 = sample_play(title="Test")
        play_with_genre_2 = sample_play(title="Test1")

        play_with_genre_1.genres.add(genre_1)
        play_with_genre_2.genres.add(genre_2)

        serializer_without_genre = PlayListSerializer(play_without_genre)
        serializer_with_genre_1 = PlayListSerializer(play_with_genre_1)
        serializer_with_genre_2 = PlayListSerializer(play_with_genre_2)

        res = self.client.get(PLAY_URL, {"genres": f"{genre_1.id},{genre_2.id}"})  # ?actors=1,2

        self.assertNotIn(serializer_without_genre.data, res.data["results"])
        self.assertIn(serializer_with_genre_1.data, res.data["results"])
        self.assertIn(serializer_with_genre_2.data, res.data["results"])

    def test_get_play_filtered_by_title(self):
        play = sample_play(title="One", description="Good play")
        play_1 = sample_play(title="Two", description="Bad play")
        play_2 = sample_play(title="Three", description="Normal play")

        serializer_play = PlayListSerializer(play)
        serializer_play1 = PlayListSerializer(play_1)
        serializer_play2 = PlayListSerializer(play_2)

        res = self.client.get(PLAY_URL, {"title": play.title})

        self.assertIn(serializer_play.data, res.data["results"])
        self.assertNotIn(serializer_play1.data, res.data["results"])
        self.assertNotIn(serializer_play2.data, res.data["results"])

    def test_admin_required_for_image_upload(self):
        play = sample_play()
        url = image_upload_url(play.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_required_for_create_play(self):
        payload = {
            "title": "Test",
            "description": "Test description",
        }
        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        self.actor = Actor.objects.create(first_name="George", last_name="Clooney")
        self.genre = Genre.objects.create(name="Drama")

    def test_create_play(self):
        payload = {
            "title": "Test",
            "description": "Test description",
            "actors": self.actor.id,
            "genres": self.genre.id
        }
        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)



