from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm


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

    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('posts:home')
    else:
        form = PostCreateForm()

    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
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


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Запись удалена')
        return redirect('posts:home')

    context = {
        'post': post
    }
    return render(request, 'posts/post_delete.html', context)


@login_required
def sent_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    return redirect('posts:detail', post.id)


@login_required
def delete_comment(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Комментарий удален')
        return redirect('posts:detail', post.parent_post.id)

    context = {
        'comment': post
    }
    return render(request, 'posts/delete_comment.html', context)


@login_required
def sent_reply(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == 'POST':
        form = ReplyCreateForm(data=request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    return redirect('posts:detail', comment.parent_post.id)


@login_required
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Ответ на комментарий удален')
        return redirect('posts:detail', reply.parent_comment.parent_post.id)

    context = {
        'reply': reply
    }
    return render(request, 'posts/delete_reply.html', context)


def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exist = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    context = {
        'post': post,
    }

    return render(request, 'snippets/likes.html', context)
