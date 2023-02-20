from django.contrib import admin

from .models import Review, Comment, Category, Title, Genre, TitleGenres


class GenreObjectsInline(admin.TabularInline):
    model = TitleGenres


@admin.register(TitleGenres)
class TitleGenresAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'genre',
    )
    list_editable = ('genre',)
    list_filter = ('genre',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-none-'
    list_editable = ('year',)
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = (GenreObjectsInline,)


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
    list_editable = ('slug',)
    list_filter = ('slug',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'score', 'pub_date', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'review')
