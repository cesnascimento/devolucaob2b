from django.urls import path, include
from .views import (
    CreateUserView, LoginView, UpdatePasswordView, MeView,
    UserActivitiesView, UsersView
)
from . import views
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect

router = DefaultRouter(trailing_slash=False)

router.register("create-user", CreateUserView, 'create user')
""" router.register("login", LoginView, 'login') """
router.register("update-password", UpdatePasswordView, 'update password')
router.register("me", MeView, 'me')
router.register("activities-log", UserActivitiesView, 'activities log')
router.register("users", UsersView, 'users')

urlpatterns = [
    path("", include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', lambda request: redirect('user/login/'))
]