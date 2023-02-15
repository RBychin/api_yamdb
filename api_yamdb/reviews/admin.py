from django.contrib import admin

from .models import Title, Genre, Category


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'genre',
        'year',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-пусто-'
    list_editable = ('year',)
    search_fields = ('name',)
    list_filter = ('genre','category',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-пусто-'
    list_editable = ('slug',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-none-'
    list_editable = ('slug',)
    search_fields = ('name',)
