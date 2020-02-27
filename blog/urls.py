from django.urls import path
from .views import view_post, add_post


urlpatterns = [
        path('post/<str:slug>', view_post, name='blog_post_detail'),
        path('add/post', add_post, name='blog_add_post')
]

