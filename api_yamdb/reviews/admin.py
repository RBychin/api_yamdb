from django.contrib import admin
from .models import Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'score', 'pub_date', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'review')


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)