"""MedicalHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 

from Profiles import views as profile_views
from Communities import views as communities_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', profile_views.loading, name='loading'),
    path('home/', profile_views.home, name='home'),
    path('login/', profile_views.login_view, name='login'),
    path('logout/', profile_views.logout_view, name='logout'),
    path('register/', profile_views.register, name='register'),
    path('communities/', communities_views.communities, name='communities'),
    path('communities/<int:pk>', communities_views.community, name='community'),
    path('communities/<int:community_id>/post/', communities_views.create_post, name='post'),
    path('communities/<int:community_id>/post/<int:post_id>/comments/', communities_views.getComments, name='comments'),
    path('communities/<int:community_id>/post/<int:post_id>/comment/', communities_views.addComment, name='comment'),
    path('communities/<int:community_id>/post/<int:post_id>/like/', communities_views.like, name='like'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

