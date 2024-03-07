from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Post, Tag
from .forms import PostCreateForm, PostEditForm


def home(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    categories = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tag': tag
    }
    return render(request, 'posts/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:home')
    else:
        form = PostCreateForm()

    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)


def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись изменена')
            return redirect('posts:home')
    form = PostEditForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'posts/post_edit.html', context)


def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Запись удалена')
        return redirect('posts:home')

    context = {
        'post': post
    }
    return render(request, 'posts/post_delete.html', context)
