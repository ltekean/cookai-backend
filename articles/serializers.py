from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

# 게시글 C
class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

#       {
#   “user_id” : 1,
#   “title” : “title”,
#   “content” : “content”,
#   “image” : [“image URL”,…],
#   “category”:”category”,
#   “tags”:[”tag1”, ”tag2”,…],
#   “recipe”:’<img src=\”\”><p></p>’,
#   “ingredients”:[{”ingredient”:”ingredient”, ingredient_quentity:float, “ingredient_unit”:”unit”},…]
#   }


# 게시글 R
class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

# 게시글 U
class ArticlePutSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category', 'tags', 'recipe']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname
    
    # 댓글 조회 시리얼라이저-직렬화
    class Meta:
        model = Comment
        fields = ['id', 'posting', 'user', 'comment', 'created_at', 'updated_at' ]


class CommentCreateSerializer(ModelSerializer):
    # 댓글 생성 시리얼라이저-직렬화, 검증까지
    class Meta:
        model = Comment
        fields = ['comment',]   # json으로 받을 데이터 필드


