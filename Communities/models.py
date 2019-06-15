from django.db import models

class Community(models.Model):
    name = models.CharField(max_length=60, default='No Name')
    description = models.TextField(default='No Description Provided.')
    pic = models.ImageField(upload_to='images/', blank=True, default='images/no-pic.svg')

    def __str__(self):
        return self.name