# Generated by Django 3.1.8 on 2023-02-21 09:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0002_auto_20230119_0810'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Review',
            new_name='Rating',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='review',
            new_name='avg_rating',
        ),
    ]
