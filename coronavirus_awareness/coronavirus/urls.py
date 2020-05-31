from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("live", views.live, name="live"),
    path("symptoms", views.symptoms, name ="symptoms"),
    path("data", views.data, name="data"),
    path("quiz", views.quiz, name="quiz"),
    path("info", views.info, name="info")
]
