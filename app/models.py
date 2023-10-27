from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
import os

class Album(models.Model):
    slug = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

def user_directory_path(instance, filename):
    user = instance.album.user
    album_name = instance.album.slug
    username = f"{user.id} {user.first_name} {user.last_name}"
    return f'{username}/{album_name}/{slugify(filename)}'

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=user_directory_path, default='default.png')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.original_name

    def save(self, *args, **kwargs):
        if not self.image_thumbnail:
            image = Image.open(self.image.path)
            thumbnail_size = (200, 150)
            thumbnail = image.copy()
            thumbnail.thumbnail(thumbnail_size)

            thumbnail_data = BytesIO()
            thumbnail.save(thumbnail_data, 'JPEG')
            thumbnail_data.seek(0)

            thumbnail_filename = f'thumbnails/{slugify(self.original_name)}_thumbnail.jpg'
            self.image_thumbnail.save(thumbnail_filename, ContentFile(thumbnail_data), save=False)

        super(Photo, self).save(*args, **kwargs)

