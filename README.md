# DRF-Machine_Learning-Project-cookai-Backend - <a href="https://github.com/2017250297-choi/front_cookai">Frontend 바로가기!</a>

DRF를 기반으로 Machine Learning 기능을 추가한 레시피 추천 커뮤니티 사이트

## 🖥️ 프로젝트 소개 - <a href="https://www.notion.so/woongpang/S-A-35075ce26cb641379fca5fc4dbf8d151">S.A. 바로가기!</a>

Cookai는 다양한 레시피를 공유하고, 자신에게 맞는 레시피를 추천받을 수 있는 요리관련 커뮤니티 서비스입니다.
다양한 사람들이 다양한 재료를 이용하는 레시피를 공유하며, 당신은 자신의 선호나 현재 가지고 있는 재료에 기반하여 적절한 레시피를 추천받을 수 있습니다.
<br>
<br>

## 🕰️ 개발 기간

- 23.06.05 - 23.07.10

### 🧑‍🤝‍🧑 팀원 구성 및 역할 분담

- 팀장😄 <a href="https://github.com/2017250297-choi">최창수</a><br>[BE] 댓글 좋아요, 게시글 북마크, 검색 기능, 테스트코드 <br>[FE] 메인페이지, 게시글 목록, 댓글 좋아요, 게시글 북마크
- 팀원😄 <a href="https://github.com/hyukjunkim1116">김혁준</a><br> [BE] 게시글 모델(CRUD), 이미지 CloudFlare와 연동 <br>[FE] 게시글 CRUD, 게시글 및 유저 프로필 이미지 업로드
- 팀원😄 <a href="https://github.com/woongpang/">이기웅</a><br>[BE] 유저 모델, 로그인(토큰 방식), 회원가입, 소셜 로그인 <br>[FE] 게시글 상세보기, 댓글 유튜브 iframe, Header, Footer, 소셜 로그인
- 팀원😄 <a href="https://github.com/ltekean/">이정민</a><br>[BE] 유저 프로필(RUD), 팔로잉, 유저시리얼라이저 <br>[FE] 프로필페이지, 팔로잉 리스트, 유저 정보수정
- 팀원😄 <a href="https://github.com/R40N/">임라온</a><br>[BE] 댓글 모델(CRUD), OPENAI , YOUTUBE API 연동 <br>[FE] 댓글 CRUD, 수정&삭제 버튼 권한부여
  <br>
  <br>

## ⚙️ 개발 환경 (Tech Stack)

- **Language** : `Python 3.8`
- **IDE** : `Visual Studio Code`
- **Framework** : `Django-Rest-Framework 3.14.0`
- **Database** : `postgresql DB 15.3`
- **Packaging-tool** : `Poetry 1.5.0`
- **CloudFlare** : https://www.cloudflare.com/ko-kr/
- **FRONTEND** : https://github.com/2017250297-choi/front_cookai

### <b>🦊 BE 😼</b>

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"><img src="https://img.shields.io/badge/poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white"/><img src="https://img.shields.io/badge/postgresql-4479A1?style=for-the-badge&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white"/>
<br>
<br>

### <b>😈 FE 👽</b>

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"><img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"><img src="https://img.shields.io/badge/ionicons-3880FF?style=for-the-badge&logo=ionic&logoColor=white"/><img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
<br>
<br>

### <b>🦝ETC🦄</b>

<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"><img src="https://img.shields.io/badge/cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white"/><img src="https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white"><img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white"/><img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white"/><img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"/><img src="https://img.shields.io/badge/visualstudiocode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"/>
<br>
<br>

## 🔑 프로젝트 설치 및 실행 방법

#### 깃허브 클론하기

```bash
$ git init
$ git clone <레파지토리 주소>
```

#### 패키지 밎 라이브러리 설치 | https://python-poetry.org/docs/

```bash
$ poetry shell
$ poetry install
```

#### DB 연동

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

#### 백엔드 서버 실행

```bash
$ python manage.py runserver
```

#### 프론트엔드 라이브서버 실행

```
$ vscode 확장팩 <Live Server> 설치
$ index.html에서 마우스 우클릭 후 Open with Live Server 클릭(단축키 Alt+L+O)
```

## 📌 주요 기능

#### 로그인

- DB값 검증
- 로그인 시 JWT Token 생성
- 소셜 로그인(카카오톡, 네이버, 구글)

#### 회원가입

- Email 중복방지

#### 회원탈퇴 & 휴면계정

- 회원탈퇴 시 DB에서 계정 삭제 됨
- 관리자는 회원을 휴면 계정으로 설정할 수 있음(유저의 "is_active = False" 로 변환함)

#### 마이페이지

- 프로필 정보 수정(프로필 사진, 비밀번호, 닉네임, 나이, 성별)
- 내가 쓴 글 보기, 좋아요 누른 댓글 보기, 북마크 한 게시글 보기
- 사용자 본인의 프로필만 수정 버튼이 보임
- 다른 유저의 마이페이지 접속 시 프로필 수정 버튼 자리에 팔로잉 버튼 있음
- 팔로잉, 팔로워 부분을 누르면 해당 유저의 팔로잉, 팔로워 목록을 볼 수 있음
- 존재하지 않는 user id를 url에 직접 입력하여 접속 시 404 페이지로 이동함

#### 북마크 기능

- 상세페이지를 들어 갔을때 다른 사람의 게시글이면 북마크 버튼이 보여짐
- 북마크 누른 게시글은 마이페이지에서 확인 가능함

#### 팔로우 기능

- 상세페이지를 들어갔을때 작성자가 본인이면 팔로우 버튼 x, 다른 사람일 경우 팔로우 버튼이 생김
- 팔로잉, 팔로워 부분을 클릭하면 팔로잉, 팔로워 리스트 페이지로 이동함
- 팔로잉, 팔로워 리스트에서 유저들을 클릭하면 해당 유저의 마이페이지로 이동함

#### 메인 페이지

- 검색 기능 : 게시글의 제목, 내용을 기준으로 검색할 수 있음
- 왼쪽 블럭에 9개의 댓글이 좋아요 개수 순으로 정렬되어 있음
- 보이는 이미지는 해당 댓글이 달린 게시글의 작성자가 업로드한 이미지가 보임
- 오른쪽 블럭에는 9개의 게시글이 최신순으로 정렬되어 있음

#### 게시글 목록 보기

- 전체 게시글 목록 조회
- 한 페이지에 10개씩 페이지 버튼은 5개까지 있음
- 게시글이 50개 넘어가면 5페이지 버튼 옆에 다음 페이지로 이동할 수 있는 버튼이 생김

#### 상세 페이지

- 게시글 수정, 삭제
- 게시글 북마크 기능
- 댓글 좋아요 기능
- 타인이 작성한 게시글에는 수정, 삭제 버튼 대신 북마크 버튼이 보임
- 댓글에 있는 유튜브 링크를 누르면 게시글 하단에 유튜브 영상을 바로 볼 수 있음
- 존재하지 않는 article id를 url에 직접 입력하여 접속 시 404 페이지로 이동함

#### 게시글 작성

- 제목, 내용 필수, 이미지 선택 가능
- 게시글 수정 시 원래 내용 불러오는 기능
- 수정하지 않은 내용은 그대로 다시 DB에 저장됨
- 이미지 삭제 버튼을 누르면 이미지 삭제됨
- 본인이 쓴 게시글만 수정, 삭제 가능

#### 댓글 작성

- 댓글 작성
- 작성자에게만 본인 댓글에 수정, 삭제 버튼이 보여짐
- 댓글 수정 시 기존 내용을 한번 더 확인시켜줌
- 댓글 수정 시 변경된 값이 없을 경우 백엔드로 요청 하지 않음
- 다른 유저가 작성한 댓글은 좋아요 버튼을 누를 수 있음
- 첫 번째 댓글은 AI가 추천한 댓글로, 게시글 작성자에게는 좋아요와 삭제 버튼이 보이고 다른 유저들에게는 좋아요 버튼만 보임

#### 추천알고리즘

- 게시글 작성시 내용을 분석하여 어울리는 음악을 추천함.
- 추천하는 음악이 YOUTUBE에 있는지 한번 더 검증하고 결과값을 댓글에 등록함.

#### 사물인식

- 게시글 작성시 내용을 분석하여 어울리는 음악을 추천함.
- 추천하는 음악이 YOUTUBE에 있는지 한번 더 검증하고 결과값을 댓글에 등록함.

#### COUPANG API

- 게시글 작성시 내용을 분석하여 어울리는 음악을 추천함.
- 추천하는 음악이 YOUTUBE에 있는지 한번 더 검증하고 결과값을 댓글에 등록함.

---

## 💜 ERD

![image](<https://file.notion.so/f/s/ee368f50-4bff-4fd2-a0df-d7b1c7c24290/cookai_(6).png?id=7520cb23-814a-4757-a639-c0fb69da9086&table=block&spaceId=3254a942-dc97-4efb-8eff-66cf14ebdfa9&expirationTimestamp=1688479200000&signature=d-DSnjY-w5vfNMuCru1V5C4Vw58gUkgHaxLQZcpMASc&downloadName=cookai+%286%29.png>)

## 💚 API 명세

[API 명세](https://www.notion.so/76fc707a8abf4ddca1ebdcef442b2c46?v=b62e355142c04281820a20663b9d3c29&pvs=4)
