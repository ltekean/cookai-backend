from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleCreate.as_view(), name='article'),
    path('<int:article_id>/', views.ArticleView.as_view(), name='articleview'),
    path('<int:article_id>/comment/', views.CommentView.as_view(), name='commentview'),
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='commentupdate'),
]