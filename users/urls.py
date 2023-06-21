from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.UserSignUpPermitView.as_view(),
        name="user_signup_permit",
    ),
    path(
        "reset/<str:uidb64>/<str:token>/",
        views.UserResetPasswordPermitView.as_view(),
        name="user_reset_password_permit",
    ),
    path(
        "login/",
        views.CustomTokenObtainPairView.as_view(),
        name="custom_token_obtain_pair",
    ),
    path("oauth/kakao/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("oauth/google/", views.GoogleLoginView.as_view(), name="google_login"),
    path("oauth/naver/", views.NaverLoginView.as_view(), name="naver_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "get-url/",
        views.UserAvatarGetUploadURLView.as_view(),
        name="user_avatar_get_upload_url",
    ),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail"),
    path(
        "<int:user_id>/fridge/",
        views.UserDetailFridgeView.as_view(),
        name="user_detail_fridge",
    ),
    path("<int:user_id>/follow/", views.UserFollowView.as_view(), name="user_follow"),
    path(
        "<int:user_id>/follower/",
        views.UserFollowerView.as_view(),
        name="user_follower",
    ),
    # 내가 쓴 댓글
    # 내가 쓴 글
    # 내가 좋아요 누른 글
    # 내가 좋아요 누른 댓글
    # 내가 북마크 한 글
    # 남의 페이지 들어갈때 뜨는것
]
