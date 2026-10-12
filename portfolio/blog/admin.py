from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'post_count_badge', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    @display(description='Published Articles', label='info')
    def post_count_badge(self, obj: Category) -> str:
        count = obj.posts.count()
        return f'{count} articles' if count != 1 else '1 article'


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = (
        'title',
        'category',
        'views',
        'read_time',
        'status_badge',
        'created_at',
    )
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Article Header', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Article Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Publishing & Metrics', {
            'fields': ('is_published', 'read_time', 'views')
        }),
    )

    @display(
        description='Status',
        label={
            'Published': 'success',
            'Draft': 'warning',
        }
    )
    def status_badge(self, obj: Post) -> str:
        return 'Published' if obj.is_published else 'Draft'
