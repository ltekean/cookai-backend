from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.ArticleView.as_view(),
        name="article_root",
    ),
    path(
        "category/",
        views.CategoryListView.as_view(),
        name="category",
    ),
    path(  # 게시글 RUD
        "<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "<int:article_id>/comment/",
        views.CommentView.as_view(),
        name="comment",
    ),
    path(
        "<int:article_id>/comment/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "<int:article_id>/recomment/<int:comment_id>/",
        views.RecommentView.as_view(),
        name="recomment",
    ),
    path(
        "<int:article_id>/recomment/<int:comment_id>/<int:recomment_id>/",
        views.RecommentDetailView.as_view(),
        name="recomment_detail",
    ),
    path(
        "get-url/",
        views.ArticleGetUploadURLView.as_view(),
        name="get_url",
    ),
    # path(
    #     "tags/",
    #     views.TagSearchView.as_view(),
    #     name="tags",
    # ),
    path(
        "<int:article_id>/recipeingredient/",
        views.RecipeIngredientView.as_view(),
        name="r_ingredient",
    ),
    path(
        "recipeingredient/<int:ingredient_id>/",
        views.RecipeIngredientDetailView.as_view(),
        name="r_ingredient_detail",
    ),
    path(  # 구매링크 추가
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
        "recomment/<int:recomment_id>/like/",
        views.ReCommentLikeView.as_view(),
        name="recomment_like",
    ),
    path(
        "<int:article_id>/bookmark/",
        views.BookmarkView.as_view(),
        name="article_bookmark",
    ),
]
