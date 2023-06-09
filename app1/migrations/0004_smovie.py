# Generated by Django 4.1.3 on 2023-03-06 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_movie_genres_alter_movie_start_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='smovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('genres', models.CharField(choices=[('A', 'action'), ('C', 'comedy'), ('R', 'romance'), ('D', 'drama'), ('T', 'thriller')], max_length=1)),
                ('img', models.ImageField(upload_to='pics')),
                ('rating', models.FloatField()),
                ('director', models.CharField(max_length=255)),
                ('Language', models.CharField(choices=[('TG', 'TELUGU'), ('TL', 'TAMIL'), ('HN', 'HINDI'), ('ML', 'MALYALAM'), ('KN', 'KANADA'), ('EN', 'ENGLISH'), ('JP', 'JAPANESE')], max_length=2)),
            ],
        ),
    ]
