from django.urls import path
from .views import ArticlePhotoDetail, GetUploadURL

urlpatterns = [
    path("photo/<int:pk>/", ArticlePhotoDetail.as_view()),
    path("photo/get-url/", GetUploadURL.as_view()),
]
