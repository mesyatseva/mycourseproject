from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CBUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass


class Kitchen(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Кухня')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name_plural = 'Кухни'
        verbose_name = 'Кухня'

    def __str__(self):
        return self.name


""" Класс Блюда для БД """


class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Блюдо')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name_plural = 'Блюда'
        verbose_name = 'Блюдо'

    def __str__(self):
        return self.name


"""Класс 'Рецепт' """


class Recipe(models.Model):
    # Сложность
    DIFFICULTY_CHOICES = (
        ('Любая', 'любая'),
        ('Легко', 'легко'),
        ('Нормально', 'нормально'),
        ('Тяжело', 'тяжело'),
    )

    # Время приготовления рецепта
    TIME_CHOICES = (
        ('Не важно', 'не важно'),
        ('До 30 минут', 'до 30 минут'),
        ('До 1 часа', 'до 1 часа'),
        ('До 2 часов', 'до 2 часов'),
        ('До 4 часов', 'до 4 часов'),
        ('До 6 часов', 'до 6 часов'),
        ('Целый день', 'целый день'),
    )

    # favorite_recipes = models.ManyToManyField(CBUser, blank=True, verbose_name="Понравившиеся рецепты")

    # likes = models.ManyToManyField(Recipe, blank=True, verbose_name="Избранное")
    # Объявление моделей
    # likes = models.ManyToManyField(Recipe, blank=True, help_text="Приготовлю потом!", related_name="User_likes")
    name = models.CharField(max_length=200, unique=True, verbose_name='Название рецепта')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.PROTECT, verbose_name='Кухня')
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, verbose_name='Блюдо')
    description = models.CharField(max_length=100, verbose_name='Краткое описание рецепта')
    steps = models.TextField(verbose_name='Пошаговая инструкциия приготовления')
    image = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True, verbose_name='Фото')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Любая', verbose_name='Сложность')
    cooktime = models.CharField(max_length=20, choices=TIME_CHOICES, default='Не важно',
                                verbose_name='Время приготовления')
    author = models.ForeignKey(CBUser, on_delete=models.PROTECT, verbose_name='Опубликовал: ')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    # Дополнительные фотки
    image_1 = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True, verbose_name='Доп.фото')
    image_2 = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True, verbose_name='Доп.фото')

    # Вызов django-clean для удаления всех файлов, связанных с записью
    # def delete(self, *args, **kwargs):
    #     for addImage in self.additionalimage_set.all():
    #         addImage.delete()
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# def profile_liked(request):
#     liked_recipes = Recipe.objects.filter(author_id=request.user.pk)
#     context = {'liked_recipes': liked_recipes}
#     return render(request, 'CookBook/profile_liked.html', context)

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CBUser, on_delete=models.CASCADE)
    body = models.TextField(help_text="Введите комментарий", verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Комментарии от пользователей'
        verbose_name = 'Комментарий'
        ordering = ('created',)

    def __str__(self):
        return 'Комментарий от пользователя {} в посте "{}"'.format(self.user, self.recipe)


class BookLikedRecipesAndUser(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Избранный рецепт', related_name='likes')
    user = models.ForeignKey(CBUser, on_delete=models.CASCADE, verbose_name='Понравился: ')
    like = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Понравившиеся рецепты'
        verbose_name = 'Рецепт нравится:'
        unique_together = ('recipe', 'user')


        # Уникальность рецептов и пользователей
