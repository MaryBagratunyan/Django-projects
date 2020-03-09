from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArticleForm, EditForm
from .models import Article, Edit


@login_required
def add_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        return redirect(article)
    return render(request, 'wiki/article_form.html', {'form': form})


@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    edit_form = EditForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        if edit_form.is_valid():
            edit = edit_form.save(commit=False)
            edit.article = article
            edit.editor = request.user
            edit.save()
            return redirect(article)
    return render(request, 'wiki/article_form.html', {'form': form, 'edit_form': edit_form, 'article': article})


def article_history(request, slug):
    article = get_object_or_404(Article, slug=slug)
    queryset = Edit.objects.filter(article__slug=slug)
    return render(request, 'wiki/edit_list.html', {'article': article, 'queryset': queryset})


class ArticleList(ListView):
    template_name = 'wiki/article_list.html'

    def get_queryset(self):
        return Article.objects.all()


class ArticleDetail(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
