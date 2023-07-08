from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from django.utils import timezone

GET_USER_URL = reverse("user_view")
SIGNUP_URL = reverse("user_view")
LOGIN_URL = reverse("custom_token_obtain_pair")


class UserBaseTestCase(APITestCase):
    """유저기능 테스트 준비

    유저기능 테스트를 위한 부모 클래스

    Attribute:
        user: 회원 데이터 추가됨
        user_signup_data: 회원가입을 위한 새로운 유저 데이터(유저1)
        user_edit_data: 회원정보 변경(비밀번호변경)용 데이터(유저2)
        user_login_data: 회원가입한 유저1의 로그인시도 데이터(이메일과비밀번호)
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="xptmxm111!",
        )
        cls.user.is_active = True
        cls.user.save()
        cls.user_signup_data = {
            "username": "testuser2",
            "password": "xptmxm111!",
            "password2": "xptmxm111!",
            "email": "testuser2@gmail.com",
        }
        cls.user_edit_data = {"old_password": "xptmxm111!"}
        cls.user_login_data = {"email": "testuser1@gmail.com", "password": "xptmxm111!"}

    def setUp(self) -> None:
        login_user = self.client.post(
            reverse("custom_token_obtain_pair"), self.user_login_data
        ).data
        self.access = login_user["access"]
        self.refresh = login_user["refresh"]


class UserMultiUserTestCase(UserBaseTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        user_signup_data = {
            "username": "testuser3",
            "password": "xptmxm111!",
            "email": "testuser3@gmail.com",
            # "age": 21,
            # "gender": "female",
        }
        cls.user2 = User.objects.create_user(**user_signup_data)
        cls.user2.is_active = True
        cls.user.save()


class UserSignUpTestCase(UserBaseTestCase):
    """회원가입 테스트

    회원가입을 테스트합니다.
    """

    url = reverse("user_view")

    def test_signup(self):
        """정상: 회원가입

        정상적인 회원가입입
        """
        data = self.user_signup_data
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 201)

        test_signuped_user = User.objects.get(email=data["email"])
        self.assertEqual(test_signuped_user.email, data["email"])

    def test_signup_password_not_same(self):
        """에러: 패스워드 불일치

        패스워드 불일치의 경우입니다.
        """

        data = self.user_signup_data
        data["password2"] = "qhdks222!"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_password_rule(self):
        """에러: 패스워드 규칙위반

        패스워드 규칙을 틀린 경우
        """
        data = self.user_signup_data
        data["password"], data["password2"] = "0000", "0000"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_email_rule(self):
        """에러: 유효하지 않은 email

        이메일 형식이 알맞지 않습니다
        """
        data = self.user_signup_data
        data["email"] = "naver@gmail@gmail.com"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_data(self):
        """에러: 올바르지 않은 age(생년)

        생년이 Date가 아닌경우
        """
        data = self.user_signup_data
        data["age"] = "test"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)


class UserSignOutTestCase(UserMultiUserTestCase):
    """회원탈퇴 테스트

    회원탈퇴(계정 비활성화)를 테스트합니다.
    """

    def test_signout(self):
        """정상: 회원탈퇴

        정상적인 회원탈퇴
        """
        self.url = reverse("user_detail", kwargs={"user_id": self.user.id})
        data = self.user_login_data
        response = self.client.put(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 200)

        test_signout_user = User.objects.get(email=data["email"])
        self.assertEqual(test_signout_user.is_active, False)

    def test_signout_wrong_password(self):
        """에러: 현재 패스워드 틀림

        현재 패스워드가 틀린 경우
        """
        self.url = reverse("user_detail", kwargs={"user_id": self.user.id})
        data = self.user_login_data
        del data["email"]
        data["password"] = "asdf!!1234"
        response = self.client.delete(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_signout_annon(self):
        """에러: 비로그인 접근

        비로그인한 사용자가 접근 케이스
        """
        self.url = reverse("user_detail", kwargs={"user_id": self.user.id})
        data = self.user_login_data
        response = self.client.put(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
        )
        test_signout_user = User.objects.get(email=data["email"])
        self.assertEqual(test_signout_user.is_active, True)

    def test_signout_wrong_token(self):
        """에러: 토큰 유효하지 않음

        잘못된/만료된 토큰을 보낸 케이스
        """
        self.url = reverse("user_detail", kwargs={"user_id": self.user.id})
        data = self.user_login_data
        response = self.client.put(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다")
        test_signout_user = User.objects.get(email=data["email"])
        self.assertEqual(test_signout_user.is_active, True)

    def test_wrong_user(self):
        """에러: 사용자가 같지 않음

        다른 사용자를 탈퇴시키려 할때
        """
        self.url = reverse("user_detail", kwargs={"user_id": self.user2.id})
        data = self.user_login_data
        del data["email"]
        response = self.client.put(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        test_signout_user = self.user2
        self.assertEqual(test_signout_user.is_active, True)


class UserEditTestCase(UserMultiUserTestCase):
    """회원정보수정 테스트

    회원정보 수정을 테스트
    """

    def test_useredit_no_pw(self):
        """정상: 비민감 회원정보 수정

        민감하지 않은 회원정보(성별,나이) 수정의 경우
        """
        url = reverse("user_detail", kwargs={"user_id": self.user.id})
        data = {"gender": "female", "age": "1997-10-08"}

        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_useredit_password(self):
        """정상: 패스워드 변경

        정상적인 패스워드 변경의 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        data["new_password"] = "newpassword1!"
        data["new_password2"] = "newpassword1!"
        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_useredit_nothing(self):
        """정상: 아무것도 수정안함

        아무것도 수정안한 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        old_pw = self.user.password
        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(old_pw, self.user.password)

    def test_useredit_password_wrong(self):
        """에러: 현재 패스워드 틀림

        현재 패스워드를 틀린 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        data["old_password"] = "qhdks222!"
        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)

    def test_useredit_password2_miss(self):
        """에러: 변경 패스워드2 입력 안함

        변경할 패스워드2를 입력 안한 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        data["new_password"] = "qhdks222!"
        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)

    def test_user_edit_password_not_same(self):
        """에러: 변경 패스워드 불일치

        변경할 패스워드가 불일치한 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        data["new_password"] = "qhdks111!"
        data["new_password2"] = "qhdks222!"
        response = self.client.put(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access}", data=data
        )
        self.assertEqual(response.status_code, 400)

    def test_annon(self):
        """에러: 비로그인 접근

        비로그인 접근의 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        response = self.client.put(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
        )
        response = self.client.put(
            path=url,
            data={"gender": "female", "age": 31},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
        )

    def test_wrong_token(self):
        """에러: 토큰 유효하지 않음

        잘못된 토큰을 보낸 경우입니다.
        """
        url = reverse("change_password")
        data = self.user_edit_data
        response = self.client.put(
            path=url,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다")
        response = self.client.put(
            path=url,
            data={"gender": "female", "age": 31},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
        )


class UserGetIdTestCase(UserBaseTestCase):
    """회원정보조회(ID) 테스트

    pk를 이용한 회원 정보 조회를 테스트합니다.
    """

    def test_userget_id(self):
        """정상: 정보조회

        ID를 이용한 본인정보조회입니다.
        """
        url = reverse("user_detail", kwargs={"user_id": self.user.id})
        response = self.client.get(
            path=url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_userget_id_unexist_user(self):
        """에러: 존재하지 않는 회원조회

        존재하지 않는 회원 조회입니다.
        """
        url = reverse("user_detail", kwargs={"user_id": 0})
        response = self.client.get(
            path=url,
        )
        self.assertEqual(response.status_code, 404)


class UserTokenTestCase(UserBaseTestCase):
    """토큰 로그인 및 갱신 테스트

    토큰 로그인 및 갱신을 테스트합니다.
    """

    url = reverse("custom_token_obtain_pair")

    def test_token_login(self):
        """정상: 토큰 login

        정상적인 토큰 login입니다.
        """
        data = self.user_login_data
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)

    def test_token_login_wrong_username(self):
        """에러: 유저네임 틀림

        유저네임을 틀린 경우입니다.
        """
        data = self.user_login_data
        data["email"] = "testuser0@testuser@.com"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)

    def test_token_login_wrong_password(self):
        """에러: 패스워드 틀림

        패스워트를 틀린 경우입니다.
        """
        data = self.user_login_data
        data["password"] = "qhdks222!"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)


class UserRefreshTestCase(UserBaseTestCase):
    url = reverse("token_refresh")

    def test_token_refresh(self):
        """정상: 토큰 refresh

        정상적인 토큰 refresh입니다.
        """
        data = {}
        data["refresh"] = self.refresh
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["access"])

    def test_token_refresh_wrong_token(self):
        """에러: 잘못된 refresh토큰

        잘못된 refresh토큰을 보낸 경우입니다.
        """
        data = {}
        data["refresh"] = self.refresh[:-3] + "123"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "유효하지 않거나 만료된 토큰")


class UserFollowTestCase(UserMultiUserTestCase):
    url1 = reverse("user_follow", kwargs={"user_id": 1})
    url2 = reverse("user_follow", kwargs={"user_id": 2})
    url3 = reverse("user_follow", kwargs={"user_id": 50000})

    def test_follow_normal(self):
        response = self.client.post(
            path=self.url2,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_follow_self(self):
        response = self.client.post(
            path=self.url1,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 403)

    def test_follow_non(self):
        response = self.client.post(
            path=self.url3,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 404)

    def test_follow_anon(self):
        response = self.client.post(path=self.url1)
        self.assertEqual(response.status_code, 401)

    def test_get_follow(self):
        response = self.client.get(path=self.url1)
        self.assertEqual(response.status_code, 200)

    def test_get_follow_non(self):
        response = self.client.get(path=self.url3)
        self.assertEqual(response.status_code, 404)


# class UserFridgeTestCase(UserMultiUserTestCase):
#     pass

# class UserAvatarTestCase(UserMultiUserTestCase):
#     pass
