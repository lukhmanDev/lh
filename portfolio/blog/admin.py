from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    @admin.display(description='Total Posts')
    def post_count(self, obj: Category) -> int:
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'views',
        'read_time',
        'is_published',
        'created_at',
    )
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
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
