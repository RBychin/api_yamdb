from django.contrib.auth import get_user_model
from rest_framework import serializers


from reviews.models import (
    Review,
    Comment,
    Title,
    Genre,
    Category
)

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user, title = (self.context.get('request').user,
                       self.context.get('title'))
        if (Review.objects.filter(title=title, author=user).exists()
                and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)


class TitlePostSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False
    )

    def to_representation(self, title):
        serializer = TitleSerializer(title)
        return serializer.data
