from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField(max_length=60, default='No Name')
    description = models.TextField(default='No Description Provided.')
    pic = models.ImageField(upload_to='images/', blank=True, default='images/no-pic.svg')

    def __str__(self):
        return self.name

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now=True)

    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    content = models.TextField()

    def calcComments(self):
        self.comments = Comment.objects.filter(post=self).count()
        return

    def __str__(self):
        return self.content[:15]


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:15]
