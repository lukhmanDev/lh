from typing import Any
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Category, Post


class BlogApiTests(APITestCase):
    client: Any

    def setUp(self):
        self.cat_dev = Category.objects.create(name='Development', slug='development')
        self.cat_design = Category.objects.create(name='Design', slug='design')

        self.post1 = Post.objects.create(
            title='First Article on Python',
            slug='first-article-on-python',
            category=self.cat_dev,
            excerpt='Short summary of python article',
            content='Full content about python and django development.',
            views=10,
            is_published=True,
        )

        self.post2 = Post.objects.create(
            title='Modern Typography in Web',
            slug='modern-typography-in-web',
            category=self.cat_design,
            excerpt='Typography rules',
            content='Full content about fonts, line height, and whitespace.',
            views=5,
            is_published=True,
        )

        self.draft_post = Post.objects.create(
            title='Draft Secret Article',
            slug='draft-secret-article',
            category=self.cat_dev,
            content='Not published yet',
            is_published=False,
        )

    def test_list_published_posts(self):
        response = self.client.get(reverse('post-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only published posts (2 out of 3)
        self.assertEqual(len(response.data), 2)
        slugs = [p['id'] for p in response.data]
        self.assertIn('first-article-on-python', slugs)
        self.assertIn('modern-typography-in-web', slugs)
        self.assertNotIn('draft-secret-article', slugs)

    def test_filter_posts_by_category(self):
        response = self.client.get(reverse('post-list-create'), {'category': 'Development'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 'first-article-on-python')

    def test_search_posts(self):
        response = self.client.get(reverse('post-list-create'), {'search': 'Typography'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 'modern-typography-in-web')

    def test_get_post_by_slug_increments_views(self):
        url = reverse('post-detail', kwargs={'lookup': self.post1.slug})
        initial_views = self.post1.views
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)
        self.assertEqual(response.data['views'], initial_views + 1)

    def test_get_post_by_numeric_pk(self):
        url = reverse('post-detail', kwargs={'lookup': str(self.post1.pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)

    def test_create_new_post(self):
        payload = {
            'title': 'New Emerging Technologies',
            'category': 'Tech News',
            'excerpt': 'Overview of upcoming tech trends.',
            'content': 'Comprehensive article describing emerging tech in 2026.',
        }
        response = self.client.post(reverse('post-list-create'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Emerging Technologies')
        self.assertEqual(response.data['category'], 'Tech News')
        self.assertTrue(Post.objects.filter(title='New Emerging Technologies').exists())
        # Category was created on the fly
        self.assertTrue(Category.objects.filter(name='Tech News').exists())

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'lookup': self.post1.slug})
        payload = {
            'title': 'Updated Python Article',
            'content': 'Updated content with even more python tips.',
        }
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Python Article')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'lookup': self.post1.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(slug=self.post1.slug).exists())

    def test_explicit_post_view_increment(self):
        url = reverse('post-view-increment', kwargs={'lookup': self.post2.slug})
        initial_views = self.post2.views
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], initial_views + 1)
        self.post2.refresh_from_db()
        self.assertEqual(self.post2.views, initial_views + 1)

    def test_list_categories_with_count(self):
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat_map = {c['name']: c['count'] for c in response.data}
        # Development has 1 published post (draft is excluded from count)
        self.assertEqual(cat_map['Development'], 1)
        # Design has 1 published post
        self.assertEqual(cat_map['Design'], 1)
