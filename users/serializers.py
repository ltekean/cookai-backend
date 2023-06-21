from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.models import Ingredient
from .models import User, Fridge
from .email_tokens import account_activation_token


class UserSerializer(ModelSerializer):
    is_host = SerializerMethodField()
    total_comments = SerializerMethodField()
    total_articles = SerializerMethodField()
    total_like_articles = SerializerMethodField()
    total_like_comments = SerializerMethodField()
    total_bookmark_articles = SerializerMethodField()
    total_followings = SerializerMethodField(read_only=True)
    total_followers = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
        )
        extra_kwargs = {
            "followings": {
                "read_only": True,
            },
            "followers": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)
        to_email = user.email
        email = EmailMessage(
            "안녕하세요 Cookai입니다. 아래 링크를 클릭해 인증을 완료하세요!",
            f"http://127.0.0.1:8000/users/activate/{uidb64}/{token}",
            to=[to_email],
        )
        email.send()
        return user

    def get_is_host(self, user):
        request = self.context["request"]

        return request.user.id == user.id

    def get_total_comments(self, user):
        return user.comments.count()

    def get_total_articles(self, user):
        return user.article_set.count()

    def get_total_like_articles(self, user):
        return user.likes.count()

    def get_total_like_comments(self, user):
        return user.like_comments.count()

    def get_total_bookmark_articles(self, user):
        return user.bookmarks.count()

    def get_total_followings(self, user):
        return user.followings.count()

    def get_total_followers(self, user):
        return user.followers.count()


class PublicUserSerializer(ModelSerializer):
    is_host = SerializerMethodField()
    total_comments = SerializerMethodField()
    total_articles = SerializerMethodField()
    total_like_articles = SerializerMethodField()
    total_like_comments = SerializerMethodField()
    total_bookmark_articles = SerializerMethodField()
    total_followings = SerializerMethodField(read_only=True)
    total_followers = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "age",
            "gender",
        )
        extra_kwargs = {
            "followings": {
                "read_only": True,
            },
            "followers": {
                "read_only": True,
            },
        }

    def get_is_host(self, user):
        request = self.context["request"]

        return request.user.id == user.id

    def get_total_comments(self, user):
        return user.comments.count()

    def get_total_articles(self, user):
        return user.article_set.count()

    def get_total_like_articles(self, user):
        return user.likes.count()

    def get_total_like_comments(self, user):
        return user.like_comments.count()

    def get_total_bookmark_articles(self, user):
        return user.bookmarks.count()

    def get_total_followings(self, user):
        return user.followings.count()

    def get_total_followers(self, user):
        return user.followers.count()


class UserFridgeSerializer(ModelSerializer):
    class Meta:
        model = Fridge
        fields = ("__all__",)
        extra_kwargs = {
            "user": {
                "read_only": True,
            },
            "ingredient": {
                "read_only": True,
            },
        }

        def save(self, **kwargs):
            ingredient_name = kwargs.get("ingredient_id", None)
            if not ingredient_name:
                raise ValidationError({"ingredient_id": "재료를 입력해주세요"})
            try:
                ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
            except Ingredient.DoesNotExist:
                ingredient = Ingredient.objects.create(ingredient_name=ingredient_name)
                ingredient.save()
            return super().save(**kwargs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["login_type"] = user.login_type
        token["avatar"] = user.avatar
        return token
