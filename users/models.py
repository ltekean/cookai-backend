from django.db import models
from django.contrib.auth.models import AbstractUser

"""유저 모델

    AbstractUser 유저 모델을 커스텀한 유저 모델입니다.

    Attributes:
        LoginTypeChoices(class) : 회원가입 유형(일반,카카오,구글,네이버)
        email (str): 이메일, 필수
        username (str) : 닉네임, 필수
        password (str): 패스워드
        avatar(str) : 유저의 프로필 사진을 url로 가져옵니다.
        age(date) : 나이
        updated_at (date): 수정시간
        created_at (date): 가입시간
        login_type (str): 회원가입 유형의 종류를 지정
        is_active (bool): 활성 여부
        is_admin (bool): 관리자 여부
        is_host(bool): 본인 여부
        followings(ManyToMany) : 팔로잉 목록
    """
class User(AbstractUser):
    

    class LoginTypeChoices(models.TextChoices):
        NORMAL = ("normal", "일반")
        KAKAO = ("kakao", "카카오")
        GOOGLE = ("google", "구글")
        NAVER = ("naver", "네이버")

    class GenderTypeChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        max_length=256,
    )
    avatar = models.URLField(
        blank=True,
        null=True,
    )
    age = models.DateField(
        blank=True,
        null=True,
    )
    gender = models.CharField(
        choices=GenderTypeChoices.choices,
        max_length=10,
        blank=True,
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
        default="normal",
    )
    is_active = models.BooleanField(
        default=False,
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


class Fridge(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="fridges",
    )

    # 06.09 수정 : 나중에 ingredient테이블로 FOREIGN KEY연결해야함
    # ingredient = models.TextField()

    # def __str__(self):
    #     return str(self.ingredient)
