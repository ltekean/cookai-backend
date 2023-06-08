from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """유저 모델

    AbstractUser 유저 모델을 커스텀한 유저 모델입니다.

    Attributes:
        LoginTypeChoices(class) : 회원가입 유형(일반,카카오,구글,네이버)
        email (str): 이메일, 필수
        nickname (str) : 닉네임
        password (str): 패스워드
        avatar(str) : 유저의 프로필 사진을 url로 가져옵니다.
        age(int) : 나이
        updated_at (date): 수정시간
        created_at (date): 가입시간
        login_type (str): 회원가입 유형의 종류를 지정
        is_active (bool): 활성 여부
        is_admin (bool): 관리자 여부
        is_host(bool): 본인 여부
        followings(list) : 팔로잉 목록
    """

    class LoginTypeChoices(models.TextChoices):
        NORMAL = ("normal", "일반")
        KAKAO = ("kakao", "카카오")
        GOOGLE = ("google", "구글")
        NAVER = ("naver", "네이버")

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        max_length=150,
        default="",
    )
    password = models.CharField(
        max_length=256,
    )
    avatar = models.URLField(
        blank=True,
        null=True,
    )
    age = models.PositiveIntegerField(
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    login_type = models.CharField(
        max_length=15,
        choices=LoginTypeChoices.choices,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    is_host = models.BooleanField(
        default=False,
    )
    followings = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )
