from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name="default"),
    path('publish/<int:album>', views.publish, name="publish"),
    path('album', views.album, name="album"),
    path('upload/<int:album>', views.upload_image, name="album.upload"),
]