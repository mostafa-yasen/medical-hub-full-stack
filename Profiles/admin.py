from django.contrib import admin
from .models import Profile, Diagnose, Question

admin.site.register(Profile)

admin.site.register(Diagnose)

admin.site.register(Question)

# admin.site.register(Answer)