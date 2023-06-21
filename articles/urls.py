from django.urls import path
from . import views


urlpatterns = [
    path("", views.ArticleCreateView.as_view()),
    path("category/", views.ArticleView.as_view()),
    path("category/<int:category_id>/", views.ArticleCategoryView.as_view()),
    path("<int:article_id>/", views.ArticleDetailView.as_view()),
    path("<int:article_id>/comment/", views.CommentView.as_view()),
    path("comment/<int:comment_id>/", views.CommentDetailView.as_view()),
    path("get-url/", views.ArticleGetUploadURLView.as_view()),
    path("tags/", views.TagSearchView.as_view()),
    path("tags/<int:tag_id>/", views.TagArticleView.as_view()),
    path("<int:article_id>/ingredient/", views.RecipeIngredientView.as_view()),
    path(
        "recipeingredient/<int:ingredient_id>/",
        views.RecipeIngredientDetailView.as_view(),
    ),  # 레시피 재료 RUD -
    path(
        "<int:article_id>/order/", views.LinkPlusView.as_view()
    ),  # 구매링크 추가 - 쿠팡이라 일단 패스
    path("like/article/<int:article_id>/", views.ArticleLikeView.as_view()),
    path("like/comment/<int:comment_id>/", views.CommentLikeView.as_view()),
    # path('<int:post_id>/like/', views.LikeSeeView.as_view(), name='likesee'),
    # path('likes/', views.CommentLikeView.as_view(), name='commentlike'),
    # path('<int:article_id>/order/', views.LinkPlusView.as_view(), name='linkplus'), # 구매링크 추가 - 쿠팡이라 일단 패스
    path("<int:article_id>/bookmark/", views.BookmarkView.as_view()),
]
