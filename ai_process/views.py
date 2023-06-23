from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.paginations import ArticlePagination, CommentPagination
from users.models import Fridge
from articles.models import (
    Article,
    Category,
    Ingredient,
    IngredientLink,
    RecipeIngredient,
)
from articles.permissions import IsAuthenticatedOrReadOnlyExceptBookMark
from django.db.models import Count
from articles.serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    CategorySerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    IngredientSerializer,
    RecipeIngredientCreateSerializer,
    IngredientLinkSerializer,
    TagSerializer,
)
from django.conf import settings
import requests
from django.db.models import Q, Count
from taggit.models import Tag
from articles.coupang import save_coupang_links_to_ingredient_links

from ai_process.recommend import collaborative_filtering, content_base


class TestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        func_dict = {"0": collaborative_filtering, "1": content_base}
        select = request.GET.get("recommend", "0")
        list_of_pk, dictionary = func_dict[select](request.user.id)
        articles = sorted(
            Article.objects.filter(id__in=list_of_pk),
            key=lambda x: dictionary[x.id],
            reverse=True,
        )
        serializer = ArticleListSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
