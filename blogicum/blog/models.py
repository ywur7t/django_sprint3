from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):

    title = models.CharField(verbose_name='Заголовок',
                             max_length=256, blank=False)
    text = models.TextField(verbose_name='Текст', blank=False)
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='''Если установить дату и время
                                    в будущем — можно делать
                                    отложенные публикации.''',
                                    auto_now_add=True, blank=False)
    author = models.ForeignKey(User, verbose_name='Автор публикации',
                               on_delete=models.CASCADE,
                               related_name='posts',
                               blank=False)
    location = models.ForeignKey('Location', verbose_name='Местоположение',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='posts')
    category = models.ForeignKey('Category', verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=False,
                                 related_name='posts')
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True, blank=False)
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, verbose_name='Автор публикации',
                               on_delete=models.CASCADE,
                               related_name="comments")
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Category(models.Model):

    title = models.CharField(verbose_name='Заголовок',
                             max_length=256, blank=False)
    description = models.TextField(verbose_name='Описание', blank=False)
    slug = models.SlugField(verbose_name='Идентификатор',
                            help_text='''Идентификатор страницы для URL;
                            разрешены символы латиницы, цифры,
                            дефис и подчёркивание.''',
                            unique=True,
                            blank=False)
    is_published = models.BooleanField(
        verbose_name='Опубликовано', help_text='''Снимите галочку,
        чтобы скрыть публикацию.''',
        default=True,
        blank=False)
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    name = models.CharField(verbose_name='Название места',
                            max_length=256, blank=False)
    is_published = models.BooleanField(
        verbose_name='Опубликовано', help_text='''Снимите галочку,
        чтобы скрыть публикацию.''',
        default=True,
        blank=False)
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
