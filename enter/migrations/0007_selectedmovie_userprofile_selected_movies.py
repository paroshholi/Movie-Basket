# Generated by Django 4.1.3 on 2023-04-18 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0006_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_movies',
            field=models.ManyToManyField(to='enter.selectedmovie'),
        ),
    ]
