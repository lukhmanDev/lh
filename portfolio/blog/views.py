from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True).select_related('category')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(
                Q(category__name__iexact=category) | Q(category__slug__iexact=category)
            )

        if search:
            q = search.strip()
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(excerpt__icontains=q)
                | Q(content__icontains=q)
                | Q(category__name__icontains=q)
            )

        return queryset.order_by('-created_at')


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        lookup = self.kwargs.get('lookup')
        # Support lookup by integer ID or slug
        if lookup.isdigit():
            post = get_object_or_404(
                Post.objects.select_related('category'),
                pk=int(lookup)
            )
        else:
            post = get_object_or_404(
                Post.objects.select_related('category'),
                slug=lookup
            )
        return post

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment reading views on retrieve
        Post.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db(fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostViewIncrementView(APIView):
    """Explicitly increment view counter for a post."""

    def post(self, request, lookup):
        if lookup.isdigit():
            post = get_object_or_404(Post, pk=int(lookup))
        else:
            post = get_object_or_404(Post, slug=lookup)

        Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
        post.refresh_from_db(fields=['views'])
        return Response({'success': True, 'views': post.views}, status=status.HTTP_200_OK)


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
