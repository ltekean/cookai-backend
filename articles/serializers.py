from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Category, Article, Comment, Ingredient, RecipeIngredient
from taggit.models import Tag


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "category",
            "title",
            "update_at",
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
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    # 댓글 조회 시리얼라이저-직렬화
    class Meta:
        model = Comment
        fields = [
            "comment",
            "author",
            "created_at",
            "updated_at",
            "likes_count",
        ]  # author, created_at 등 조회에 필요한 것들

    def get_author(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.like.count()


# 레시피 재료 가져오기
class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    상세게시글에 나타낼 레시피 재료 가져오는 것입니다.
    """

    class Meta:
        model = RecipeIngredient
        fields = [
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
    comment_set = CommentSerializer(many=True)  # comment_set이라는 역참조 필드 존재
    comments_count = serializers.SerializerMethodField()
    recipeingredient_set = RecipeIngredientSerializer(
        many=True
    )  # related_name을 이용해서 변수 이름을 정하자

    class Meta:
        model = Article
        fields = "__all__"

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
            "title",
            "create_at",
            "image",
            "is_author",
            "comments_count",
            "likes_count",
        ]


class TagSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    def get_article_count(self, obj):
        return obj.taggit_taggeditem_items.count()

    class Meta:
        model = Tag
        fields = "__all__"


# 댓글 작성
class CommentCreateSerializer(ModelSerializer):
    # 댓글 생성 시리얼라이저-직렬화, 검증까지
    class Meta:
        model = Comment
        fields = [
            "comment",
        ]  # json으로 받을 데이터 필드


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
