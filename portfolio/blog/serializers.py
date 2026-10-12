from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'count']

    def get_count(self, obj: Category) -> int:
        return obj.posts.filter(is_published=True).count()


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)
    pk_id = serializers.IntegerField(source='pk', read_only=True)
    category = serializers.CharField(required=False, allow_blank=True)
    category_slug = serializers.SerializerMethodField()
    date = serializers.CharField(source='formatted_date', read_only=True)
    readTime = serializers.CharField(source='read_time', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'pk_id',
            'title',
            'slug',
            'category',
            'category_slug',
            'date',
            'readTime',
            'read_time',
            'views',
            'excerpt',
            'content',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'pk_id', 'slug', 'date', 'readTime', 'created_at', 'updated_at']

    def get_category_slug(self, obj: Post) -> str:
        return obj.category.slug if obj.category else ''

    def to_representation(self, instance: Post):
        ret = super().to_representation(instance)
        ret['category'] = instance.category.name if instance.category else 'General'
        return ret

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)
        category_obj = None
        if category_name:
            category_obj, _ = Category.objects.get_or_create(
                name=category_name.strip()
            )
        post = Post.objects.create(category=category_obj, **validated_data)
        return post

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        if category_name is not None:
            if category_name.strip():
                category_obj, _ = Category.objects.get_or_create(
                    name=category_name.strip()
                )
                instance.category = category_obj
            else:
                instance.category = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'content' in validated_data:
            instance.read_time = instance.calculate_read_time(instance.content)

        instance.save()
        return instance
