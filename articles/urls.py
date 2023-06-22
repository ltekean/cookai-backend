from django.urls import path
from . import views


urlpatterns = [
    path(  # 게시글 CR
        "",
        views.ArticleView.as_view(),
        name="article_root",
    ),
    path(  # 카테고리 리스트 (R)
        "category/",
        views.CategoryListView.as_view(),
        name="category",
    ),
    path(  # 게시글 UD
        "<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(  # 댓글 CR
        "<int:article_id>/comment/",
        views.CommentView.as_view(),
        name="comment",
    ),
    path(  # 댓글 UD
        "<int:article_id>/comment/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(  # 이미지 업로드용 가url
        "get-url/",
        views.ArticleGetUploadURLView.as_view(),
        name="get_url",
    ),
    path(  # 태그 검색(R)
        "tags/",
        views.TagSearchView.as_view(),
        name="tags",
    ),
    path(  # 레시피 재료 C
        "<int:article_id>/recipeingredient/",
        views.RecipeIngredientView.as_view(),
        name="r_ingredient",
    ),
    path(  # 레시피 재료 UD
        "recipeingredient/<int:ingredient_id>/",
        views.RecipeIngredientDetailView.as_view(),
        name="r_ingredient_detail",
    ),
    path(  # 구매링크 추가 - 쿠팡이라 일단 패스
        "<int:article_id>/order/",
        views.LinkPlusView.as_view(),
        name="order",
    ),
    path(
        "<int:article_id>/like/",
        views.ArticleLikeView.as_view(),
        name="article_like",
    ),
    path(
        "comment/<int:comment_id>/like/",
        views.CommentLikeView.as_view(),
        name="comment_like",
    ),
    path(
        "<int:article_id>/bookmark/",
        views.BookmarkView.as_view(),
        name="article_bookmark",
    ),
]
