from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from PIL import Image

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
    original_name = filename
    return f'{username}/{album_name}/{slugify(original_name)}'

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=user_directory_path, default='default.png')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_name

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        image = Image.open(self.image.path)

        thumbnail_size = (200, 150)

        thumbnail = image.copy()
        thumbnail.thumbnail(thumbnail_size)
        thumbnail_path = self.image.path.replace(".jpg", "_thumbnail.jpg")
        thumbnail.save(thumbnail_path)
