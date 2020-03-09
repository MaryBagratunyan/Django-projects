from django.urls import path

from .views import add_article, edit_article, article_history, ArticleList, ArticleDetail


urlpatterns = [
    path('', ArticleList.as_view(), name='wiki_article_list'),
    path('add/article', add_article, name='wiki_article_add'),
    path('edit/article/<str:slug>', edit_article, name='wiki_article_edit'),
    path('detail/article/<str:slug>', ArticleDetail.as_view(), name='wiki_article_detail'),
    path('history/article/<str:slug>', article_history, name='wiki_article_history')
]
