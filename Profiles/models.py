from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

GENDERS = (
    ('M', 'male'),
    ('F', 'female')
)


class Profile(models.Model):
    # Extend Django Auth's User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Start Global Attributes
    pic = models.ImageField(upload_to='images/', default='images/no-pic.svg')
    
    # Phone

    bio = models.TextField(max_length=500, blank=True)
    
    city = models.CharField(max_length=30, blank=True)
    
    address = models.CharField(max_length=120, blank=True)
    
    gender = models.CharField(max_length=1, choices=GENDERS, default='m')
    
    is_doctor = models.BooleanField(default=False)
    
    nid = models.CharField(max_length=15, blank=True)

    phone = models.CharField(max_length=12, blank=True)

    # Start Patient Attributes

    # Start Doctor Attributes
    specialization = models.CharField(max_length=120, blank=True)

    rate = models.FloatField(default=0)

    # Start Methods
    def __str__(self):
        if self.is_doctor:
            return 'Dr.%s' % self.user.username
        
        else:
            return str(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Diagnose(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now=True)

    title = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title[:15]