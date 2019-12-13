from django.contrib import admin
# Вызов моделей
from .models import CBUser
from .models import Kitchen, Dish, Recipe, Comment, BookLikedRecipesAndUser


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'kitchen', 'author', 'dish', 'difficulty', 'cooktime', 'created_at')
    fields = (('kitchen', 'dish'), 'name', 'author', 'description', 'steps', 'image', 'difficulty', 'cooktime', 'image_1', 'image_2')

class KitchenAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class CBUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('recipe', 'user', 'body')


@admin.register(BookLikedRecipesAndUser)
class CBBookLikedRecipesAndUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user', 'like')

# Register your models here.

admin.site.register(Kitchen, KitchenAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(CBUser, CBUserAdmin)
admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(BookLikedRecipesAndUser)
