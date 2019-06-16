from django.urls import path
from . import views

urlpatterns = [
    path('', views.communities, name='communities'),
    path('<int:pk>', views.community, name='community'),
    path('<int:community_id>/post/', views.create_post, name='post'),
    path('<int:community_id>/post/<int:post_id>/comments/', views.getComments, name='comments'),
    path('<int:community_id>/post/<int:post_id>/comment/', views.addComment, name='comment'),
    path('<int:community_id>/post/<int:post_id>/like/', views.like, name='like'),
]