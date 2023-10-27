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
    return f'{username}/{slugify(album_name)}/{slugify(filename)}'

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=user_directory_path, default='default.png')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.original_name

    # def save(self, *args, **kwargs):
    #     if not self.image_thumbnail:
    #         super(Photo, self).save(*args, **kwargs)

    #         image = Image.open(self.image.path)
    #         thumbnail_size = (200, 150)
    #         thumbnail = image.copy()
    #         thumbnail.thumbnail(thumbnail_size)

    #         thumbnail_dir = os.path.dirname(self.image_thumbnail.path)
    #         if not os.path.exists(thumbnail_dir):
    #             os.makedirs(thumbnail_dir)

    #         thumbnail_filename = f'thumbnails/{slugify(self.original_name)}_thumbnail.jpg'
    #         thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)

    #         with open(thumbnail_path, 'wb') as thumbnail_file:
    #             thumbnail.save(thumbnail_file, 'JPEG')

    #         self.image_thumbnail = f'thumbnails/{slugify(self.original_name)}_thumbnail.jpg'
    #         self.save(update_fields=['image_thumbnail'])

