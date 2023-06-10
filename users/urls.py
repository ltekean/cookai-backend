from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


urlpatterns = [
    path("", views.UserView.as_view()),
    path("signup/", views.SignUpView.as_view()),
    path("activate/<str:uidb64>/<str:token>/", views.UserSignUpPermitView.as_view()),
    path(
        "reset/<str:uidb64>/<str:token>/", views.UserResetPasswordPermitView.as_view()
    ),
    path("login/", TokenObtainPairView.as_view()),
    path("oauth/kakao/", views.KakaoLoginView.as_view()),
    path("oauth/google/", views.GoogleLoginView.as_view()),
    path("oauth/naver/", views.NaverLoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("reset-password/", views.ResetPasswordView.as_view()),
    path("change-password/", views.ChangePasswordView.as_view()),
    path("<int:user_id>/", views.UserDetailView.as_view()),
    path("<int:user_id>/fridge/", views.UserDetailFridgeView.as_view()),
    path("<int:user_id>/avatar/", views.UserAvatarView.as_view()),
    path("<int:user_id>/follow/", views.UserFollowView.as_view()),
]
