from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.paginations import ArticlePagination
from articles.models import Article, Comment, Category, Ingredient, RecipeIngredient
from articles.permissions import IsAuthenticatedOrReadOnlyExceptBookMark
from django.db.models import Count
from articles.serializers import (
    ArticleSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticlePutSerializer,
    CommentCreateSerializer,
    IngredientSerializer,
    RecipeIngredientCreateSerializer,
)
from django.conf import settings
import requests


# Create your views here.
class ArticleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnlyExceptBookMark]
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("create_at")

    def bookmarked(self):
        queryset = self.request.user.bookmarked_articles.all()
        return queryset.order_by("bookmark", "create_at")

    def liked(self):
        queryset = Article.objects.all().order_by("likes_count")
        return queryset

    def get_queryset(self):
        query_select = {
            "bookmarked": self.bookmarked,
            "liked": self.liked,
        }
        selection = self.request.GET.get("filter", None)
        return query_select.get(selection, super().get_queryset)()


# 카테고리 띄우기
class ArticleCategoryView(APIView):
    def get(self, request, category_id):
        categorizing = Category.objects.get(id=category_id)
        articles = categorizing.article_set.order_by("create_at")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 작성
class ArticleCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ArticleCreateSerializer(
            context={"request": request}, data=request.data
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 가져오기, 수정, 삭제
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(
            article,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, article_id):
        art_put = get_object_or_404(Article, id=article_id)
        if request.user == art_put.user:
            serializer = ArticlePutSerializer(
                art_put, context={"request": request}, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        art_del = get_object_or_404(Article, id=article_id)
        if request.user == art_del.user:
            art_del.delete()
            return Response("게시글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        return Response("본인이 작성한 게시글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)


class IngredientDetailView(APIView):
    def get(self, request):
        ingredient = get_object_or_404(Ingredient, id=id)
        serialize = IngredientSerializer(ingredient)
        return Response(serialize.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        ing_put = get_object_or_404(Ingredient, id=article_id)
        if request.user == ing_put.user:
            serializer = IngredientSerializer(ing_put, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        ing_del = get_object_or_404(Article, id=article_id)
        if request.user == ing_del.user:
            ing_del.delete()
            return Response("재료가 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        return Response("본인이 작성한 재료만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)


# 댓글 작성 뷰
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("본인이 작성한 댓글만 수정할수 있습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
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


# 재료 C
class RecipeIngredientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id):
        serializer = RecipeIngredientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                article_id=article_id, ingredient_id=request.data.get("ingredient")
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeIngredientDetailView(APIView):
    def put(self, request, ingredient_id):
        ing_put = get_object_or_404(RecipeIngredient, id=ingredient_id)
        if request.user == ing_put.article.author:
            serializer = RecipeIngredientCreateSerializer(ing_put, data=request.data)
            if serializer.is_valid():
                serializer.save(ingredient_id=request.data.get("ingredient"))
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("올바른 사용자가 아닙니다", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, ingredient_id):
        ing_put = get_object_or_404(RecipeIngredient, id=ingredient_id)
        if request.user != ing_put.article.author:
            return Response("올바른 사용자가 아닙니다", status=status.HTTP_401_UNAUTHORIZED)
        ing_put.delete()
        return Response("recipe ingredient가 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
