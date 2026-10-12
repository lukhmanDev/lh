import math
import re
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    read_time = models.CharField(max_length=50, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    @property
    def formatted_date(self) -> str:
        return self.created_at.strftime('%b %d, %Y') if self.created_at else ''

    @staticmethod
    def calculate_read_time(content_text: str) -> str:
        words = len(re.findall(r'\b\w+\b', content_text or ''))
        minutes = max(1, math.ceil(words / 180)) if words else 1
        return f'{minutes} min read'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'post'
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        if not self.read_time:
            self.read_time = self.calculate_read_time(self.content)

        if not self.excerpt and self.content:
            clean_snippet = re.sub(r'#+\s*', '', self.content)
            clean_snippet = re.sub(r'`{1,3}.*?`{1,3}', '', clean_snippet)
            clean_snippet = re.sub(r'\s+', ' ', clean_snippet).strip()
            self.excerpt = clean_snippet[:140] + ('...' if len(clean_snippet) > 140 else '')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
