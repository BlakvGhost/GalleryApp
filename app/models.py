from django.db import models
from django.contrib.auth.models import User
from slugify import slugify


class Album(models.Model):
    slug = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.slug
    
def user_directory_path(instance, filename):
    user = instance.album.user
    album_name = instance.album.slug
    username = f"{user.id}_{user.first_name}_{user.last_name}"
    return f'{username}/{album_name}/{slugify(filename)}'

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=user_directory_path, default='default.png')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.original_name