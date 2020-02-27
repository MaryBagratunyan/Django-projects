from django.urls import path
from .views import view_post, add_post, PostList, PostUpdate


urlpatterns = [
    path('post/<str:slug>', view_post, name='blog_post_detail'),
    path('add/post', add_post, name='blog_post_add'),
    path('posts/', PostList.as_view(), name='blog_post_list'),
    path('update/<str:slug>', PostUpdate.as_view(), name='blog_post_update')
]

