# Generated by Django 4.1.3 on 2023-04-17 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0001_add_favorite_language_field_to_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]