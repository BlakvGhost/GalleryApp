# Generated by Django 4.2.3 on 2023-10-25 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='default.png', upload_to='photos/'),
        ),
    ]
