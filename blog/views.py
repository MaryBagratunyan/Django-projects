from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test

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
    return render(request, 'blog/blog_post.html', {'post': post, 'form': form})
