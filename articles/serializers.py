from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import (
    Category,
    Article,
    Comment,
    Recomment,
    Ingredient,
    IngredientLink,
    RecipeIngredient,
)
from taggit.models import Tag


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "category",
            "title",
            "updated_at",
            "like",
            "image",
            "is_author",
            "content",
            "recipe",
            "tags",
            "likes_count",
        ]

    def get_is_author(self, article):
        request = self.context["request"]
        return article.author == request.user

    def get_likes_count(self, obj):
        return obj.like.count()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    article_count = serializers.SerializerMethodField()

    def get_article_count(self, obj):
        return obj.article_set.count()

    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    # recomments = serializers.SerializerMethodField()

    # 댓글 조회 시리얼라이저-직렬화
    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "author",
            "user",
            "is_author",
            "article",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
            # "recomments",
        ]  # author, created_at 등 조회에 필요한 것들
        extra_kwargs = {
            "author": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
            "user": {
                "read_only": True,
            },
            "is_author": {
                "read_only": True,
            },
            "is_liked": {
                "read_only": True,
            },
            "likes_count": {
                "read_only": True,
            },
            "article": {
                "read_only": True,
            },
        }

    def get_user(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.like.count()

    def get_is_author(self, article):
        request = self.context["request"]
        return article.author == request.user

    def get_is_liked(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return request.user in obj.like.all() or False

    # def get_recomments(self, instance):
    #     serializer = self.__class__(instance.recomments, many=True)
    #     serializer.bind("", self)
    #     return serializer.data


class RecommentSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    # 댓글 조회 시리얼라이저-직렬화
    class Meta:
        model = Recomment
        fields = [
            "id",
            "comment",
            "recomment",
            "author",
            "user",
            "is_author",
            "article",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
        ]
        extra_kwargs = {
            "author": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
            "user": {
                "read_only": True,
            },
            "is_author": {
                "read_only": True,
            },
            "is_liked": {
                "read_only": True,
            },
            "likes_count": {
                "read_only": True,
            },
            "article": {
                "read_only": True,
            },
            "comment": {
                "read_only": True,
            },
        }

    def get_user(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.like.count()

    def get_is_author(self, article):
        request = self.context["request"]
        return article.author == request.user

    def get_is_liked(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return request.user in obj.like.all() or False


# 레시피 재료 가져오기
class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    상세게시글에 나타낼 레시피 재료 가져오는 것입니다.
    """

    class Meta:
        model = RecipeIngredient
        fields = [
            "id",
            "ingredient_id",
            "ingredient_quantity",
            "ingredient_unit",
        ]


# 상세게시글 R
class ArticleDetailSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()
    is_author = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    categoryname = serializers.SerializerMethodField()
    recipeingredient_set = RecipeIngredientSerializer(
        many=True
    )  # related_name을 이용해서 변수 이름을 정하자

    class Meta:
        model = Article
        fields = "__all__"

    def get_categoryname(self, obj):
        return str(obj.category)

    def get_user(self, obj):
        return obj.author.username

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_likes_count(self, obj):
        return obj.like.count()

    def get_is_author(self, article):
        request = self.context["request"]
        return article.author == request.user


class ArticleListSerializer(ArticleDetailSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "created_at",
            "image",
            "is_author",
            "comments_count",
            "likes_count",
            "user",
        ]
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class TagSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    def get_article_count(self, obj):
        return obj.taggit_taggeditem_items.count()

    class Meta:
        model = Tag
        fields = "__all__"


class RecipeIngredientCreateSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = [
            "ingredient_quantity",
            "ingredient_unit",
        ]

    # 없는 재료는 새로 추가해야 함

    def save(self, **kwargs):
        ingredient_name = kwargs.get("ingredient_id", None)
        if not ingredient_name:
            raise serializers.ValidationError({"ingredient_id": "재료를 입력해주세요"})
        try:
            ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
        except:
            ingredient = Ingredient.objects.create(ingredient_name=ingredient_name)
            ingredient.save()
        return super().save(**kwargs)


class IngredientLinkSerializer(ModelSerializer):
    ingredient_name = serializers.SerializerMethodField()

    class Meta:
        model = IngredientLink
        fields = ("ingredient_name", "link", "link_img", "price")

    def get_ingredient_name(self, obj):
        return obj.ingredient.ingredient_name
