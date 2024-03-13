from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm


def home(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'posts/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    if request.htmx:
        if 'top' in request.GET:
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        context = {
            'comments': comments,
            'replyform': replyform
        }
        return render(request, 'snippets/loop_post_detail_comments.html', context)

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
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        'comment': comment,
        'post': post,
        'replyform': replyform
    }

    return render(request, 'snippets/add_comment.html', context)


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
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(data=request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'comment': comment,
        'reply': reply,
        'replyform': replyform
    }

    return render(request, 'snippets/add_reply.html', context)


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


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)

        return wrapper

    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):

    context = {
        'post': post,
    }

    return render(request, 'snippets/likes.html', context)


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    context = {
        'comment': post,
    }

    return render(request, 'snippets/likes_comment.html', context)


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    context = {
        'reply': post,
    }

    return render(request, 'snippets/likes_reply.html', context)
