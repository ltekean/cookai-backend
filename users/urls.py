from django.urls import path
from rest_framework_simplejwt.views import (
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
        "<int:user_id>/comments/",
        views.UserDetailCommentsView.as_view(),
        name="user_detail_comment",
    ),
    path(
        "<int:user_id>/articles/",
        views.UserDetailArticlesView.as_view(),
        name="user_detail_article",
    ),
    path(
        "<int:user_id>/articles/likes/",
        views.UserDetailLikeArticlesView.as_view(),
        name="user_detail_like_article",
    ),
    path(
        "<int:user_id>/comments/likes/",
        views.UserDetailLikeCommentsView.as_view(),
        name="user_detail_like_comment",
    ),
    path(
        "<int:user_id>/articles/bookmarks/",
        views.UserDetailArticlesBookmarksView.as_view(),
        name="user_detail_article_bookmark",
    ),
    path(
        "fridge/",
        views.UserDetailFridgeView.as_view(),
        name="user_fridge",
    ),
    path(
        "fridge/<int:fridge_id>/",
        views.UserDetailFridgeView.as_view(),
        name="user_fridge_detail",
    ),
    path(
        "<int:user_id>/following/",
        views.UserFollowView.as_view(),
        name="user_following",
    ),
    path(
        "<int:user_id>/follower/",
        views.UserFollowerView.as_view(),
        name="user_follower",
    ),
]
