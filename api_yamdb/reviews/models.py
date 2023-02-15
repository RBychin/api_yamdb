from django.db import models

class Title(models.Model):
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name='Категория',
        related_name='Titles'
    )
    genre = models.ForeignKey(
        'Genre',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name='Жанр',
        related_name='Titles'
    )
    name = models.CharField('Название произведения', max_length=100)
    year = models.PositiveSmallIntegerField('Дата создания', blank=False, null=False)
    
    def __str__(self):
        return self.name[:30]

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
    

class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.CharField('Краткое имя жанра', max_length=50)
    
    def __str__(self):
        return self.name[:30]
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.CharField('Краткое имя категории', max_length=50)
    
    def __str__(self):
        return self.name[:30]
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
