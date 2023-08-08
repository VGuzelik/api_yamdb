from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from users.models import User


class AbstractModel(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Уникальный адрес',
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256, db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)],
        db_index=True
    )
    description = models.CharField(
        'Описание',
        max_length=512,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        verbose_name='Жанр'
    )

    class Meta:
        default_related_name = 'titles'
        ordering = ('year',)
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(AbstractModel):

    class Meta:
        verbose_name_plural = 'Категории'


class Genre(AbstractModel):

    class Meta:
        verbose_name_plural = 'Жанры'


# class ReviewQuerySet(models.QuerySet):
#
#     def rating(self):
#         return round(
#             sum(review.score / self.count() for review in self.all()),
#             1
#         )


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review')
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)]
    )
    # objects = ReviewQuerySet.as_manager()

    class Meta:
        ordering = ('pub_date',)
        unique_together = ('author', 'title',)


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('pub_date',)
