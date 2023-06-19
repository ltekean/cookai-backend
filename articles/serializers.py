from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Article, Comment, Ingredient, RecipeIngredient


# 게시글 C
class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "category",
            "recipe",
        ]


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


# 게시글 U
class ArticlePutSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "image",
            "category",
            "recipe",
        ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    # 댓글 조회 시리얼라이저-직렬화
    class Meta:
        model = Comment
        fields = [
            "comment",
            "author",
            "created_at",
            "updated_at",
        ]  # author, created_at 등 조회에 필요한 것들


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


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "category",
            "title",
            "update_at",
            "like",
            "image",
        ]


# 상세게시글 R
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)  # comment_set이라는 역참조 필드 존재
    comments_count = serializers.SerializerMethodField()
    recipeingredient_set = RecipeIngredientSerializer(
        many=True
    )  # related_name을 이용해서 변수 이름을 정하자

    def get_user(self, obj):
        return obj.author.username

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_likes_count(self, obj):
        return obj.like.count()


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
