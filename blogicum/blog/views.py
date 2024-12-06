from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils import timezone
from django.http import Http404


def index(request):

    posts = (
        Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
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

    if post.pub_date > timezone.now():
        raise Http404("Post is scheduled for the future.")

    # Если категория не опубликована, возвращаем 404
    if not post.category.is_published:
        return render(request, 'blog/404.html', status=404)

    if post.pub_date > timezone.now() or (not post.category.is_published):
        return render(request, 'blog/404.html', status=404)

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


# def category_posts(request, category_slug):

#     category = get_object_or_404(
#         Category.objects.filter(is_published=True),
#         slug=category_slug
#     )

#     posts = Post.objects.filter(
#         category=category,
#         is_published=True,
#         pub_date__lte=timezone.now()
#     ).order_by('-pub_date')
#     context = {
#         'category': category,
#         'post_list': posts,
#     }

#     return render(request, 'blog/category.html', context)


def category_posts(request, category_slug):
    # Получаем категорию, которая опубликована
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    # Получаем текущее время в UTC
    current_time_utc = timezone.now()

    # Логируем текущее время для отладки
    print(f"Current UTC time: {current_time_utc}")

    # Локализуем текущее время в локальный часовой пояс
    current_time_local = timezone.localtime(current_time_utc)
    print(f"Local time: {current_time_local}")

    # Фильтруем посты по дате публикации, исключая будущие
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time_local
        # Фильтруем только те, у которых дата <= локальное текущее время
    ).order_by('-pub_date')

    # Логируем количество отфильтрованных постов для отладки
    print(f"Filtered posts count: {posts.count()}")

    # Если нет постов, можно вернуть пустую страницу или сообщить
    if not posts:
        print("No posts available for this category.")

    context = {
        'category': category,
        'post_list': posts,  # Передаем список постов в контекст
    }

    return render(request, 'blog/category.html', context)
