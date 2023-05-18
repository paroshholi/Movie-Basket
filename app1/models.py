from django.db import models


from django.db import models
category =(
    ('A','action'),
    ('C','comedy'),
    ('R','romance'),
    ('D','drama'),
    ('T','thriller'),
)

category1=(
    ('TG','TELUGU'),
    ('TL','TAMIL'),
    ('HN','HINDI'),
    ('ML','MALYALAM'),
    ('KN','KANADA'),
    ('EN','ENGLISH'),
    ('JP','JAPANESE'),
)
class smovie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    genres = models.CharField(choices=category,max_length=1)
    img = models.ImageField(upload_to='pics')
    rating=models.FloatField()
    director = models.CharField(max_length=255)
    Language = models.CharField(choices=category1,max_length=2)

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=255)
    start_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    
    def __str__(self):
        return self.title

