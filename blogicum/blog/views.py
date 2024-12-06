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
        id=id,
        is_published=True)

    if post.pub_date > now() or not post.category.is_published:
        return render(request, 'blog/404.html', status=404)

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):

    # category = get_object_or_404(Category,
    #                              slug=category_slug,
    #                              is_published=True)

    # posts = Post.objects.filter(
    #     category=category,
    #     is_published=True,
    #     pub_date__lte=now()
    # ).order_by('-pub_date')

    # context = {
    #     'category': category,
    #     'posts': posts,
    # }
    # return render(request, 'blog/category.html', context)

    # Получаем категорию или 404, если она не опубликована
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    # Получаем опубликованные публикации этой категории,
    # чья дата публикации не позже текущего времени
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')

    # Добавляем контекст
    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'blog/category.html', context)
