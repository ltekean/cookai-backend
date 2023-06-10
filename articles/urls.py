from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleCreate.as_view(), name='article'),
    path('<int:article_id>/', views.ArticleView.as_view(), name='articleview'),
    path('<int:article_id>/comment/', views.CommentView.as_view(), name='commentview'),
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='commentupdate'),
    path("get-url/", views.ArticleGetUploadURLView.as_view()),
    path('<int:article_id>/ingredient/<str:ingredient>/', views.IngredientView.as_view(), name='ingredient'),
    path('<int:article_id>ingredient/<ingredient>/', views.IngredientDeleteView.as_view(), name='ingredientdelete'),
    path('like/<int:comment_id>/', views.LikeView.as_view(), name='like'),
    path('likes/', views.CommentLikeView.as_view(), name='commentlike'),
]