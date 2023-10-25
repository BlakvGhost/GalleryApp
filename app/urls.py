from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name="default"),
    path('publish', views.publish, name="publish"),
    path('album', views.album, name="album"),
]