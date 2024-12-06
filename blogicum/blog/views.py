from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils.timezone import now


def index(request):

    posts = (
        Post.objects.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        )
        .order_by('-pub_date')[:5]
    )
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):

    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        id=id, is_published=True)
    context = {'post': post}

    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):

    category = get_object_or_404(Category.objects.filter(
        is_published=True), slug=category_slug)
    posts = Post.objects.filter(
        category=category, is_published=True).order_by('-pub_date')
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)
