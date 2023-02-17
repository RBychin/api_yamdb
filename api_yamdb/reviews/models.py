from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Title(BaseModel):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField('Дата создания', blank=False,
                                            null=False)
    description = models.TextField('Описание', max_length=1000, blank=True,
                                   null=True)
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


class TitleGenres(BaseModel):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='titles'
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.DO_NOTHING,
        verbose_name='Жанр',
        related_name='genres'
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'


class Genre(BaseModel):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.CharField('Краткое имя жанра', max_length=50)

    def __str__(self):
        return self.name[:30]

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(BaseModel):
    name = models.CharField('Название категории', max_length=256)
    slug = models.CharField('Краткое имя категории', max_length=50)

    def __str__(self):
        return self.name[:30]

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CreatedModel(BaseModel):
    """Абстрактная модель. Добавляет в модель дату создания.
    Упорядочивает записи по дате создания от новой к старой."""
    text = models.TextField(
        max_length=200,
        verbose_name='Текст сообщения',
        blank=False
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ["-pub_date"]


class Review(CreatedModel):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
        blank=False
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(CreatedModel):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарии'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
