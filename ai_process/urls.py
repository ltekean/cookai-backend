from django.urls import path
from ai_process.views import TestView

urlpatterns = [
    path("", TestView.as_view()),
]
