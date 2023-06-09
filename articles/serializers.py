from rest_framework.serializers import ModelSerializer
from .models import *

# 게시글 C
class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

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
        model = Comments
        fields = ['id', 'posting', 'user', 'comment', 'created_at', 'updated_at' ]


class CommentCreateSerializer(serializers.ModelSerializer):
    # 댓글 생성 시리얼라이저-직렬화, 검증까지
    class Meta:
        model = Comments
        fields = ['comment',]   # json으로 받을 데이터 필드

class PostingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    # 게시물에 작성된 댓글set과 댓글 수
    comments_set = CommentSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_comments_count(self, obj):
        return obj.comments_set.count()
        

    def get_likes_count(self, obj):
        return obj.likes.count()
        
    class Meta:
        model = Postings
        fields = ['user','id','title','content','image', 'comments_set', 'comments_count','likes_count',]

class PostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postings 
        fields = ['title','content','image']
        
class PostingPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postings 
        fields = ['title','content','image']
