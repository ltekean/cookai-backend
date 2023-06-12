from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleCreateView.as_view(), name='article'), # 게시글 생성 - 완료
    path('<int:article_id>/', views.ArticleView.as_view(), name='articleview'), # 게시글 조회 - 완료
    path('<int:article_id>/comment/', views.CommentView.as_view(), name='commentview'), # 댓글 CR - 완료
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='commentupdate'), # 댓글 UD - 완료
    path("get-url/", views.ArticleGetUploadURLView.as_view()), # 사진 첨부 - 완료
    # path('<int:article_id>/ingredient/<str:ingredient>/', views.IngredientView.as_view(), name='ingredient'), # 레시피 재료 수정/추가
    # path('<int:article_id>ingredient/<ingredient>/', views.IngredientDeleteView.as_view(), name='ingredientdelete'), #레시피 재료 제거
    path('like/<int:comment_id>/', views.LikeView.as_view(), name='like'), # 좋아요 생성 - 완료
    # path('<int:post_id>/like/', views.LikeSeeView.as_view(), name='likesee'), # 이건 뭔지 감 못 잡음
    # path('likes/', views.CommentLikeView.as_view(), name='commentlike'), # 좋아요 순 댓글모음
    # path('<int:article_id>/order/', views.LinkPlusView.as_view(), name='linkplus'), # 구매링크 추가 - 쿠팡이라 일단 패스
    path('<int:article_id>/bookmark/', views.BookmarkView.as_view(), name='bookmark'), # 북마크 - 완료
]