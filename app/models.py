"""
Definition of models.
"""

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликовано")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.ImageField(upload_to='blog_images/')  # Добавьте это поле

    # Методы класса
    def get_absolute_url(self):
        # метод возвращает строку с URL-адресом записи
        return reverse('blogpost', args=[str(self.id)])

    def __str__(self):
        # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title

    # Метаданные - вспомогательный класс, который задает дополнительные параметры модели
    class Meta:
        db_table = 'Posts'  # имя таблицы для модели
        ordering = ['-posted']  # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога"  # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"  # тоже для всех статей блога

admin.site.register(Blog)


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к шнапсу")

    # Методы класса
    def __str__(self):
        # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return f'Комментарий id {self.id} к #{self.post.id} ({self.author})'

    # Метаданные - вспомогательный класс, который задает дополнительные параметры модели
    class Meta:
        db_table = 'Comment'
        ordering = ['-date']
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

