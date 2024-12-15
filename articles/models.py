from django.db import models

class Article(models.Model):
    title = models.TextField()
    authors = models.TextField()
    journal = models.TextField()
    journal_url = models.URLField(null=True, blank=True)  # Add this field
    published_date = models.DateTimeField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    affiliations = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)


    class Meta:
        db_table = 'articles'  # Specify the existing table name

    def __str__(self):
        return self.title

class LastUpdated(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")