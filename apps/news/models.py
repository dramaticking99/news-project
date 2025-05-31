from django.db import models
from django.utils import timezone

class Article(models.Model):
    url = models.URLField(max_lenght=500, unique=True)
    title = models.CharField(max_lenght=300)
    content = models.TextField()
    author = models.CharField(max_lenght=100, blank=True, null=True)
    published_date = models.DateTimeField()
    scraped_date = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_lenght=100, blank=True, null=True)

    def __str__(self):
        return self.title