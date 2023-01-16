from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm
from .models import Group, Post, User


# @login_required если не убрать этот декоратор, не проходят тесты:
# test_index_paginator_view
# test_index_paginator_not_in_view_context
def index(request):
    page_number = request.GET.get('page')
    posts = Post.objects.select_related('author',
                                        'group')
    paginator = Paginator(posts, settings.NUM_OF_POSTS)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author', 'group')
    page_number = request.GET.get('page')
    paginator = Paginator(posts, settings.NUM_OF_POSTS)
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    page_number = request.GET.get('page')
    posts_owner = get_object_or_404(User, username=username)
    posts = posts_owner.posts.select_related('author', 'group')
    paginator = Paginator(posts, settings.NUM_OF_POSTS)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts_owner': posts_owner
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.author = request.user
            save_form.save()
            return redirect('posts:profile', request.user.username)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id)
    if request.user != post_obj.author:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post_obj)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_obj.id)
        return render(request, 'posts/create_post.html', {'form': form,
                                                          'is_edit': True})
    form = PostForm(instance=post_obj)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': True})
