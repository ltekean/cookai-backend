from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class LoginTypeChoices(models.TextChoices):
        NORMAL = ("normal", "일반")
        KAKAO = ("kakao", "카카오")
        GOOGLE = ("google", "구글")
        NAVER = ("naver", "네이버")

    email = models.EmailField(
        max_length=255,
        default="",
        unique=False,
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
