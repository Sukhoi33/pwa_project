from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('accounts/', include('allauth.urls')),
]