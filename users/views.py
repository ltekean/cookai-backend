import requests
from django.contrib.auth import logout, login
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer, UserFridgeSerializer
from cookai import settings
from photos.serializers import UserPhotoSerializer
from users.models import User, Fridge
from users import serializers
from users.email_tokens import account_activation_token


class UserView(APIView):
    """유저전체보기, 주석 추가 예정"""

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """회원가입. 주석추가에정,이메일 인증 추가예정"""

    def post(self, request):
        first_password = request.data.get("first_password")
        second_password = request.data.get("second_password")
        if not first_password or not second_password:
            raise ParseError
        if first_password != second_password:
            raise ParseError
        serializer = serializers.UserSerializer(
            data=request.data,
            password=first_password,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpPermitView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                User.objects.filter(pk=uid).update(is_active=True)
                return redirect(f"{settings.FRONT_DEVELOP_URL}/login.html")
            return Response({"error": "AUTH_FAIL"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "KEY_ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLoginView(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "5c41d07be161c81979b0eb05ec72f14b",
                    "redirect_uri": f"{settings.FRONT_DEVELOP_URL}/oauth/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("id"))
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("id"),
                    username=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                    login_type="kakao",
                )
                user.set_unusable_password()
                user.save()
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://oauth2.googleapis.com/token?code={code}&client_id={settings.GC_ID}&client_secret={settings.GC_SECRET}&redirect_uri={settings.FRONT_DEVELOP_URL}/oauth/google&grant_type=authorization_code",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            try:
                user = User.objects.get(email=user_data.get("id"))
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    email=user_data.get("id"),
                    username=user_data.get("name"),
                    avatar=user_data.get("picture"),
                    login_type="google",
                )
                user.set_unusable_password()
                user.save()
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NaverLoginView(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://nid.naver.com/oauth2.0/token?code={code}&client_id={settings.NC_ID}&client_secret={settings.NC_SECRET}&grant_type=authorization_code&state=1",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            try:
                user = User.objects.get(email=user_data["response"].get("id"))
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data["response"].get("name"),
                    email=user_data["response"].get("id"),
                    avatar=user_data["response"].get("profile_image"),
                    login_type="naver",
                )
                user.set_unusable_password()
                user.save()
                refresh = RefreshToken.for_user(user)
                access_token = serializers.CustomTokenObtainPairSerializer.get_token(
                    user
                )
                return Response(
                    {"refresh": str(refresh), "access": str(access_token.access_token)},
                    status=status.HTTP_200_OK,
                )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """비밀번호 찾기. 이메일 인증하면 비밀번호 재설정할 기회를 준다. 주석추가에정,이메일 인증 추가예정"""

    def put(self, request):
        user_email = request.data.get("email")
        user = User.objects.filter(email=user_email)
        if user:
            new_first_password = request.data.get("new_first_password")
            new_second_password = request.data.get("new_second_password")
            if new_first_password == new_second_password:
                serializer = serializers.UserSerializer(
                    data=request.data,
                    password=new_first_password,
                    partial=True,
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                raise ParseError
        else:
            raise NotFound


class UserResetPasswordPermitView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                return redirect(f"{settings.FRONT_DEVELOP_URL}/login.html")
            return Response({"error": "AUTH_FAIL"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "KEY_ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, user_id):
        """유저 프로필 조회 주석 추가 예정"""
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """유저 프로필 수정"""
        user = get_object_or_404(User, id=user_id)
        # 현재유저와 수정하려는 유저가 일치한다면
        if request.user.id == user_id:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def delete(self, request, user_id):
        """유저 삭제, 주석 추가 예정"""
        user = get_object_or_404(User, id=user_id)

        # 현재유저와 삭제하려는 유저가 일치한다면
        if request.user.id == user_id:
            user = request.user
            user.is_active = False
            user.save()
            return Response("삭제되었습니다!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    """노말 로그인 회원만 비번 바꾸기. 주석추가예정"""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if user.login_type == "normal":
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")
            if not old_password or not new_password:
                raise ParseError
            if old_password == new_password:
                raise ParseError
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise ParseError
        else:
            raise ParseError


class UserDetailFridgeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_fridge = Fridge.objects.filter(user=request.user)
        serializer = UserFridgeSerializer(
            all_fridge,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserFridgeSerializer(data=request.data)
        if serializer.is_valid():
            fridge = serializer.save(
                user=request.user,
            )
            serializer = UserFridgeSerializer(fridge)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fridge_id):
        fridges = get_object_or_404(Fridge, pk=fridge_id)
        if fridges:
            fridges.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise NotFound


class UserAvatarView(APIView):
    """유저 프로필 사진 올리기, 주석 추가 예정"""

    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            raise PermissionDenied
        serializer = UserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            avatar = serializer.save()
            serializer = UserPhotoSerializer(avatar)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserFollowView(APIView):
    """팔로우한 유저 조회, 유저 팔로우 토글. 주석추가예정"""

    def get(self, request, user_id):
        """유저 팔로우한 유저들 조회"""
        follow = User.objects.filter(followings=user_id)
        serializer = UserSerializer(follow, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        """유저 팔로잉 누르기"""
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if request.user.id != user_id:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response("unfollow", status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response("follow", status=status.HTTP_200_OK)
        else:
            return Response("자신을 팔로우 할 수 없습니다!", status=status.HTTP_403_FORBIDDEN)
