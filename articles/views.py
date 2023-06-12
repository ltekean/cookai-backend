from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.models import Article, Comment
from articles.serializers import ArticleCreateSerializer, ArticleSerializer, ArticlePutSerializer, CommentCreateSerializer, CommentSerializer, RecipeIngredientCreateSerializer
from django.conf import settings
import requests
# Create your views here.

# 게시글 작성
class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):        
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 아티클에 이미지까지 더하기


# 게시글 가져오기, 수정, 삭제
class ArticleView(APIView):
    def get(self, request):
        article = get_object_or_404(Article,id=id)
        serialize = ArticleSerializer(article)
        return Response(serialize.data)

    def put(self, request, article_id):
        # 수정할 게시글 불러오기
        art_put = get_object_or_404(Article, id=article_id)
        # 게시글 작성자와 로그인한 유저가 같으면
        if request.user == art_put.user:
        # ArticlePutSerializer로 입력받은 데이터 직렬화, 검증
            serializer = ArticlePutSerializer(art_put, data=request.data)
            # 직렬화된 데이터가 유효하다면
            if serializer.is_valid():
            # DB에 저장
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            # 데이터 검증 실패시
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        art_del = get_object_or_404(Article, id=article_id)
        if request.user == art_del.user:
        # 게시글 삭제
            art_del.delete()
            return Response("게시글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        # 게시글 작성자 != 로그인한 유저
        return Response("본인이 작성한 게시글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment_id=comment_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    # 좋아요 순으로 댓글 가져오는 방법.. 어떻게 하지
    # 주석 처리하고 나중에 해보자
    # def get(self, request, article_id):
    #     # 게시물 id 가져오기
    #     article_get = Article.objects.get(id=article_id)
    #     # 게시물 id에 해당하는 comments들 모두 가져오기
    #     comments = article_get.comments_set.all()
    #     # CommentSerializer로 직렬화하기(불러온 comments_set)
    #     serializer = CommentSerializer(comments, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, pk):
        # 수정할 댓글 불러오기
        comment = get_object_or_404(Comment, id=pk)
        # 댓글 작성자와 로그인한 유저가 같으면
        if request.user == comment.user:
        # CommentCreateSerializer로 입력받은 데이터 직렬화, 검증
            serializer = CommentCreateSerializer(comment, data=request.data)
            # 직렬화된 데이터가 유효하다면
            if serializer.is_valid():
            # DB에 저장
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            # 데이터 검증 실패시
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # 댓글 작성자 != 로그인한 유저
        return Response("본인이 작성한 댓글만 수정할수 있습니다", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        # 삭제할 댓글 불러오기
        comment = get_object_or_404(Comment, id=pk)
        # 댓글 작성자 == 로그인한 유저
        if request.user == comment.user:
        # comment 삭제
            comment.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        # 댓글 작성자 != 로그인한 유저
        return Response("본인이 작성한 댓글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)
    

class ArticleGetUploadURLView(APIView):
    def post(self, request):
        """GetUploadURL.post

                사용자가 사진을 첨부해서 클라우드플레어에 전송하기전에 먼저 일회용 업로드 url을 요청합니다.

        Args:
            url (str): 클라우드플레어에서 미리 지정한 일회용 url 요청 링크
            one_time_url (str): post요청이 성공할 경우 클라우드플레어에서 온 response. 일회용 업로드 url을 포함하고 있습니다.
        return:
            result(str)): 일회용 url

        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response(result)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, article_id):
        """게시글 좋아요 누르기"""
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.like.all():
            article.like.remove(request.user)
            return Response("dislike", status=status.HTTP_200_OK)
        else:
            article.like.add(request.user)
            return Response("like", status=status.HTTP_200_OK)


class BookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.bookmark.all():
            article.bookmark.remove(request.user)
            return Response("unbookmark", status=status.HTTP_200_OK)
        else:
            article.bookmark.add(request.user)
            return Response("bookmark", status=status.HTTP_200_OK)
        

class IngredientView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, article_id):
        serializer = RecipeIngredientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, article_id):
        # 게시물 id 가져오기
        article_get = Article.objects.get(id=article_id)
        # 게시물 id에 해당하는 recipe 가져오기
        recipes = article_get.recipe_set.all()
        # CommentSerializer로 직렬화하기(불러온 comments_set)
        serializer = RecipeIngredientCreateSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정 중
    def put(self, request, article_id):
        # 수정할 게시글 불러오기
        ing_put = get_object_or_404(Article, id=article_id)
        # 게시글 작성자와 로그인한 유저가 같으면
        if request.user == ing_put.user:
        # ArticlePutSerializer로 입력받은 데이터 직렬화, 검증
            serializer = ArticlePutSerializer(ing_put, data=request.data)
            # 직렬화된 데이터가 유효하다면
            if serializer.is_valid():
            # DB에 저장
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            # 데이터 검증 실패시
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)