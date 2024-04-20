from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    """Класс модели категорий статей"""
    name = models.CharField("Категория", max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Article(models.Model):
    """Класс модели статьи"""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE)
    title = models.CharField("Тема", max_length=50)
    text = models.TextField("Полное содержание", max_length=10000)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    published = models.BooleanField("Опубликовать?", default=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель коментариев к новостям"""
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, verbose_name="Статья",
        related_name="comments",
        on_delete=models.CASCADE
    )
    text = models.TextField("Сообщение", default='')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.user} - {self.article}"
