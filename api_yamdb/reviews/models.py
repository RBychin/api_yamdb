from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class CreatedModel(models.Model):
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
