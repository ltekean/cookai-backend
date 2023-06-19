import re
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Fridge
from .email_tokens import account_activation_token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("groups", "user_permissions")
        extra_kwargs = {
            "followings": {
                "read_only": True,
            },
            "password": {
                "write_only": True,  # 작성만 가능하도록 제한! 비밀번호 조회 불가
            },
        }

    def validate_password(self, password):
        """비밀번호 유효성 검사"""
        if len(password) < 8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
        if not re.search(r"\d", password):
            raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*()]", password):
            raise ValidationError("비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다.")
        return password

    def validate_email(self, email):
        email_regex = re.compile(
            r"^[a-zA-Z]+[!#$%&'*+-/=?^_`(){|}~]*[a-zA-Z0-9]*@[\w]+\.[a-zA-Z0-9-]+[.]*[a-zA-Z0-9]+$"
        )
        email_validation = email_regex.match(email)
        if not email_validation:
            # 알파벳 대/소문자로 시작. 특수문자로 마무리 안됨. @와 .이 포함되었는지 확인
            raise ValidationError("이메일 형식이 올바르지 않습니다!")
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        self.validate_password(password)
        self.validate_email(email)
        user = User(**validated_data, email=email)
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


class UserFridgeSerializer(ModelSerializer):
    class Meta:
        model = Fridge
        fields = ("__all__",)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        token["login_type"] = user.login_type
        token["avatar"] = user.avatar
        return token
