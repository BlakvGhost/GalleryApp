from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from PIL import Image
import os
from pathlib import Path


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
    image_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.original_name

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        # Ouvrez l'image avec Pillow
        image = Image.open(self.image.path)

        # Définissez la taille de la miniature souhaitée
        thumbnail_size = (100, 100)

        # Créez une miniature
        thumbnail = image.copy()
        thumbnail.thumbnail(thumbnail_size)

        # Obtenez le répertoire de destination pour les miniatures
        thumbnail_dir = Path(self.image.path).parent

        # Assurez-vous que le répertoire existe, s'il n'existe pas, créez-le
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

        # Générez un nom de fichier pour la miniature
        thumbnail_filename = f'thumbnails/{slugify(self.original_name)}_thumbnail.jpg'

        # Utilisez Path pour créer le chemin complet de la miniature
        thumbnail_path = thumbnail_dir / thumbnail_filename

        # Sauvegardez la miniature
        thumbnail.save(str(thumbnail_path))

        # Stockez le chemin de la miniature dans le champ `image_thumbnail`
        self.image_thumbnail = thumbnail_filename
        self.save()
