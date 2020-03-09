from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .models import Post
from .forms import PostForm, CommentForm


@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render(request, 'blog/add_post.html', {'form': form})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session['name'] = comment.name
        request.session['email'] = comment.email
        request.session['website'] = comment.website

    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render(request, 'blog/blog_post.html', {'post': post, 'form': form})


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'


class PostUpdate(UpdateView):
    model = Post
    fields = ['text']
    template_name = 'blog/add_post.html'
