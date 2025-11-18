from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import CreateUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
]
