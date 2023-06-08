from django.urls import path
from . import views


urlpatterns = [
    path("", views.UserView.as_view()),
    path("sign-up/", views.UserView.as_view()),
    path("log-in/", views.UserView.as_view()),
    path("oauth/kakao/", views.UserView.as_view()),
    path("oauth/google/", views.UserView.as_view()),
    path("oauth/naver/", views.UserView.as_view()),
    path("token/refresh/", views.UserView.as_view(), name="token_refresh"),
    path("change-password/", views.UserView.as_view()),
    path("search-password/", views.UserView.as_view()),
    path("<int:user_id>/", views.UserView.as_view()),
    path("<int:user_id>/fridge/", views.UserView.as_view()),
    path("<int:user_id>/avatar/", views.UserView.as_view()),
    path("<int:user_id>/follow/", views.UserView.as_view()),
]
