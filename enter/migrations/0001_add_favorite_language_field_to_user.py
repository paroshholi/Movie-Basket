# Generated by Django 4.1.3 on 2023-04-17 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_language', models.CharField(blank=True, choices=[('en', 'English'), ('hi', 'Hindi'), ('te', 'Telugu'), ('ta', 'Tamil'), ('ml', 'Malayalam'), ('kn', 'Kannada'), ('ja', 'Japanese')], max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]