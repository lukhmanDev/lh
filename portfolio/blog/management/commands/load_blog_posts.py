import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category, Post


class Command(BaseCommand):
    help = 'Load blog posts from posts.json into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=r'd:\projects\Lukman\blog.lhakkeem.in\server\data\posts.json',
            help='Path to posts.json file'
        )

    def handle(self, *args, **options):
        file_path = Path(options['file'])
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)

        loaded_count = 0
        for item in posts_data:
            cat_name = (item.get('category') or 'General').strip()
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )

            post_slug = item.get('id') or slugify(item['title'])
            Post.objects.update_or_create(
                slug=post_slug,
                defaults={
                    'title': item['title'].strip(),
                    'category': category,
                    'excerpt': item.get('excerpt', '').strip(),
                    'content': item.get('content', '').strip(),
                    'read_time': item.get('readTime', '').strip(),
                    'views': item.get('views', 0),
                    'is_published': True,
                }
            )
            loaded_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported/updated {loaded_count} blog posts and categories.')
        )
