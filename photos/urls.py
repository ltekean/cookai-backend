from django.urls import path
from .views import ArticlePhotoDetailView, GetUploadURLView

urlpatterns = [
    path("photo/<int:pk>/", ArticlePhotoDetailView.as_view()),
]
