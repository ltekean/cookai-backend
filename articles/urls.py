from django.urls import path
from . import views


urlpatterns = [
    path("", views.ArticleCreateView.as_view()),  # 게시글 생성 - 완료
    path("category/", views.ArticleView.as_view()),  # 전체 게시글 조회 - 완료
    path(
        "category/<int:category_id>/", views.ArticleCategoryView.as_view()
    ),  # 카테고리 별 조회 - 완료
    path("<int:article_id>/", views.ArticleDetailView.as_view()),  # 게시글 R - 완성
    path("<int:article_id>/comment/", views.CommentView.as_view()),  # 댓글 CR - 완료
    path(
        "<int:article_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view()
    ),  # 댓글 UD - 완료
    path("get-url/", views.ArticleGetUploadURLView.as_view()),  # 사진 첨부 - 완료
    path(
        "<int:article_id>/ingredient/", views.RecipeIngredientView.as_view()
    ),  # 레시피 재료 CR -
    path(
        "recipeingredient/<int:ingredient_id>/",
        views.RecipeIngredientDetailView.as_view(),
    ),  # 레시피 재료 RUD -
    path("like/<int:article_id>/", views.LikeView.as_view()),  # 좋아요 생성 - 완료
    # path('<int:post_id>/like/', views.LikeSeeView.as_view(), name='likesee'), # 이건 뭔지 감 못 잡음
    # path('likes/', views.CommentLikeView.as_view(), name='commentlike'), # 좋아요 순 댓글모음
    # path('<int:article_id>/order/', views.LinkPlusView.as_view(), name='linkplus'), # 구매링크 추가 - 쿠팡이라 일단 패스
    path("<int:article_id>/bookmark/", views.BookmarkView.as_view()),  # 북마크 - 완료
]
