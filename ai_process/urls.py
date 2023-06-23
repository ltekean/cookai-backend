from django.urls import path

from .views import ImageUploadView,TestView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="image_upload"),
    path("", TestView.as_view()),

]
