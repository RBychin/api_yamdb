from django.db import models

class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField('Дата создания', blank=False, null=False)
    description = models.TextField('Описание', max_length=1000, blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        verbose_name='Категория',
        related_name='titles'
    )

    def __str__(self):
        return self.name[:30]

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class TitleGenres(models.Model):
    title=models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='titles'
        )
    genre=models.ForeignKey(
        'Genre',
        on_delete=models.DO_NOTHING,
        verbose_name='Жанр',
        related_name='genres'
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'


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

