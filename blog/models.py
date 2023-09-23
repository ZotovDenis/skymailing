from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='image/', verbose_name='Изображение', **NULLABLE)
    created_date = models.DateField(verbose_name='Дата публикации', **NULLABLE)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
