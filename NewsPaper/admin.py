from django.contrib import admin
from .models import Author, Post, PostCategory, Category, Comment


# Register your models here.

def nullify_quantity(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_quantity.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at', 'rating')
    list_filter = ('post_type', 'categories')
    search_fields = ('title', 'text', 'author__authorUser__username')
    actions = [nullify_quantity]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser__username',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)
