from django.urls import path, include
from rest_framework import routers

from theatre.views import ActorViewSet, GenreViewSet, TheatreHallViewSet, PlayViewSet

app_name = "theatre"


router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("theatre-halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
