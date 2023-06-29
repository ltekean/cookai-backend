from django.urls import path

from .views import ImageUploadView, RecommendView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="image_upload"),
    path("", RecommendView.as_view()),
]
