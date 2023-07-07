from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.paginations import (
    ArticlePagination,
    CommentPagination,
    ReCommentPagination,
)
from users.models import Fridge
from articles.models import (
    Article,
    Comment,
    Recomment,
    Category,
    Ingredient,
    IngredientLink,
    RecipeIngredient,
)
from django.http import JsonResponse
from articles.permissions import IsAuthenticatedOrReadOnlyExceptBookMark
from django.db.models import Count
from articles.serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    CategorySerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    RecommentSerializer,
    IngredientSerializer,
    RecipeIngredientCreateSerializer,
    IngredientLinkSerializer,
    TagSerializer,
)
from django.conf import settings
import requests
from django.db.models import Q
from taggit.models import Tag
from articles.coupang import save_coupang_links_to_ingredient_links
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.


class ArticleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnlyExceptBookMark]
    pagination_class = ArticlePagination
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all().order_by("created_at")

    def search_author(self):
        selector = self.request.GET.get("selector")
        return Q(author__username__icontains=selector)

    def search_title_content(self):
        selector = self.request.GET.get("selector")
        q = Q(title__icontains=selector)
        q.add(Q(content__icontains=selector), q.OR)
        q.add(Q(recipe__icontains=selector), q.OR)

        if self.request.GET.get("recipe"):
            q2 = Q(recipe__isnull=False)
            q2.add(Q(counts__gt=0), q2.AND)
            q.add(q2, q.AND)
        return q

    def search_ingredient(self):
        selector = self.request.GET.get("selector")
        ingredient_q = Q()
        for ingredient_ in selector.split(","):
            if ingredient_ == "":
                continue
            ingredient_q.add(Q(ingredient_name__icontains=ingredient_), ingredient_q.OR)
        ingredients = Ingredient.objects.filter(ingredient_q)
        q = Q(recipeingredient__ingredient__in=ingredients)

        return q

    def search_ingredient_title_content(self):
        q = self.search_title_content()
        q.add(self.search_ingredient(), q.OR)
        return q

    def search_tag(self):
        selector = self.request.GET.get("selector")
        return Q(tags__name__in=[selector])

    def weekly_best(self):
        q = Q(created_at__gt=timezone.now() - timedelta(weeks=1))
        q.add(Q(like__isnull=False), q.AND)
        return q

    def daily_best(self):
        q = Q(created_at__gt=timezone.now() - timedelta(days=1))
        q.add(Q(like__isnull=False), q.AND)
        return q

    def search(self, type_key):
        types = {
            "0": self.search_author,  # author 통과
            "1": self.search_title_content,  # title+con(recipeonly) 통과
            "2": self.search_ingredient,  # ingredient 통과
            "3": self.search_ingredient_title_content,  # title+con+ingredient 통과
            "4": self.search_tag,  # tag 통과
            "5": self.weekly_best,
            "6": self.daily_best,
        }
        query_filter = types.get(type_key, Q)()
        return query_filter

    def get_queryset(self):
        search_key = self.request.GET.get("search", None)
        q = Q()
        if search_key:
            q = self.search(search_key)
        category_id = self.request.GET.get("category")
        if category_id:
            try:
                category_id = int(category_id)
                q.add(Q(category_id=category_id), q.AND)
            except:
                pass
        order = self.request.GET.get("order")
        if order == "1":
            queryset = (
                Article.objects.annotate(counts=Count("recipeingredient"))
                .filter(q)
                .annotate(like_count=Count("like"))
                .order_by("-like_count")
            )
        else:
            Article.objects.annotate(counts=Count("recipeingredient"))
            queryset = (
                Article.objects.annotate(counts=Count("recipeingredient"))
                .filter(q)
                .order_by("-created_at")
            )
        return queryset

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # 카테고리 띄우기
# class ArticleCategoryView(APIView):
#     def get(self, request, category_id):
#         categorizing = Category.objects.get(id=category_id)
#         articles = categorizing.article_set.order_by("created_at")
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
class CategoryListView(APIView):
    def get(self, request):
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if request.user == art_put.author:
            serializer = ArticleSerializer(
                art_put, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        art_del = get_object_or_404(Article, id=article_id)
        if request.user == art_del.author:
            art_del.delete()
            return Response(
                {"message": "게시글이 삭제되었습니다"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "본인이 작성한 게시글만 삭제할수 있습니다"}, status=status.HTTP_403_FORBIDDEN
        )


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
            return Response(
                {"message": "재료가 삭제되었습니다"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "본인이 작성한 재료만 삭제할수 있습니다"}, status=status.HTTP_403_FORBIDDEN
        )


# 댓글 작성/조회 뷰
class CommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    queryset = None

    def get_queryset(self):
        queryset = Comment.objects.filter(article_id=self.article_id)
        order = self.request.GET.get("order", None)
        if order == "1":
            return queryset.order_by("-like_count")
        if order == "2":
            return queryset.order_by("created_at")
        return queryset.order_by("-created_at")

    def get(self, request, *args, **kwargs):
        self.article_id = kwargs.get("article_id")
        return super().get(request, *args, **kwargs)

    def post(self, request, article_id):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            serializer = CommentSerializer(
                comment, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "본인이 작성한 댓글만 수정할수 있습니다"}, status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        return Response("본인이 작성한 댓글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)


class RecommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ReCommentPagination
    serializer_class = RecommentSerializer
    queryset = None

    def get_queryset(self):
        queryset = Recomment.objects.filter(
            article_id=self.article_id, comment_id=self.comment_id
        )
        order = self.request.GET.get("order", None)
        if order == "1":
            return queryset.order_by("-like_count")
        if order == "2":
            return queryset.order_by("created_at")
        return queryset.order_by("-created_at")

    def get(self, request, *args, **kwargs):
        self.article_id = kwargs.get("article_id")
        self.comment_id = kwargs.get("comment_id")
        return super().get(request, *args, **kwargs)

    def post(self, request, article_id, comment_id):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(
                author=request.user, article_id=article_id, comment_id=comment_id
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommentDetailView(APIView):
    def put(self, request, article_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            serializer = RecommentSerializer(
                recomment, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "본인이 작성한 대댓글만 수정할수 있습니다"}, status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, article_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            recomment.delete()
            return Response(
                {"message": "대댓글이 삭제되었습니다"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "본인이 작성한 댓글만 삭제할수 있습니다"}, status=status.HTTP_403_FORBIDDEN
        )


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


class TagSearchView(APIView):
    def get(self, request):
        tag_condition = request.query_params.get("tag", None)
        tag_list = Tag.objects.filter(name__contains=tag_condition)
        serializer = TagSerializer(tag_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TagArticleView(APIView):
#     def get(self, request, tag_id):
#         try:
#             target_tag = Tag.objects.get(id=tag_id)
#             target_article = Article.objects.filter(tags__name__in=[target_tag])
#             serializer = ArticleSerializer(
#                 target_article, many=True, context={"request": request}
#             )
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(
#                 {"error": "해당 태그를 찾을 수 없습니다!"}, status=status.HTTP_404_NOT_FOUND
#             )


class ArticleLikeView(APIView):
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


class CommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        """댓글 좋아요 누르기"""
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
            return Response("dislike", status=status.HTTP_200_OK)
        else:
            comment.like.add(request.user)
            return Response("like", status=status.HTTP_200_OK)


class ReCommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, recomment_id):
        """댓글 좋아요 누르기"""
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user in recomment.like.all():
            recomment.like.remove(request.user)
            return Response("dislike", status=status.HTTP_200_OK)
        else:
            recomment.like.add(request.user)
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
            return Response(
                {"error": "올바른 사용자가 아닙니다"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, ingredient_id):
        ing_put = get_object_or_404(RecipeIngredient, id=ingredient_id)
        if request.user != ing_put.article.author:
            return Response(
                {"error": "올바른 사용자가 아닙니다"}, status=status.HTTP_401_UNAUTHORIZED
            )
        ing_put.delete()
        return Response(
            {"message": "recipe ingredient가 삭제되었습니다"}, status=status.HTTP_204_NO_CONTENT
        )


class LinkPlusView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, article_id):
        # article_id와 연결된 RecipeIngredient 조회
        recipe_ingredients = RecipeIngredient.objects.filter(
            article_id=article_id
        ).values_list("ingredient", flat=True)
        # 로그인된 사용자의 Fridge 조회
        if not request.user.is_anonymous:
            user_fridge_ingredients = Fridge.objects.filter(
                user=request.user
            ).values_list("ingredient", flat=True)
            # 사용자의 Fridge에 없는 Ingredient 찾기
            missing_ingredients = set(recipe_ingredients) - set(user_fridge_ingredients)
        else:
            missing_ingredients = set(recipe_ingredients)

        # 없는 Ingredient와 연결된 IngredientLink 조회
        # column_name+__in : 리스트 안에 지정한 문자열들 중에 하나라도 포함된 데이터를 찾을 때 사용
        ingredient_links = IngredientLink.objects.filter(
            ingredient__in=missing_ingredients
        )

        # 현재 시간과 5일 전 시간 구하기
        now = timezone.now()
        five_days_ago = now - timedelta(days=5)

        # 존재하지 않는 IngredientLink 인스턴스 생성 및 저장
        for ingredient in missing_ingredients:
            ingredient_links = IngredientLink.objects.filter(ingredient=ingredient)
            if not ingredient_links.exists():
                save_coupang_links_to_ingredient_links(ingredient)
            else:
                # link가 등록된 재료라도 `updated_at`이 5일 이상 지났다면 최신화하기
                existing_link = ingredient_links.first()
                if (
                    existing_link.ingredient.updated_at is None
                    or existing_link.ingredient.updated_at <= five_days_ago
                ):
                    save_coupang_links_to_ingredient_links(ingredient)

        # 다시 IngredientLink를 조회
        ingredient_links = IngredientLink.objects.filter(
            ingredient__in=missing_ingredients
        )

        # JSON 형태로 반환
        serialized_links = IngredientLinkSerializer(ingredient_links, many=True)
        return Response(serialized_links.data, status=status.HTTP_200_OK)
