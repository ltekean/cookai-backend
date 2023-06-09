import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from .models import ArticlePhoto
from .serializers import ArticlePhotoSerializer


class ArticlePhotoDetailView(APIView):
    """ArticlePhotoDetail

    Args:
        permission (permission): IsOwnerOrReadOnly은 요청자가 게시글의 작성자일 경우와 아닐 경우를 판단하여 권한을 부여. 기본적으로 읽기 권한만을 주어 게시글을 관리합니다.

    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, pk):
        """ArticlePhotoDetail.put

        get요청 시 제시한 pk의 사진을 가져옵니다.
        put요청 시 제시한 pk의 file을 입력받아 수정합니다.

        Args:
            pk (int): 사진의 pk를 가리킵니다.

        정상 시 200 / 원래 ArticlePhoto의 file을 변경. 수정완료.
        오류 시 400 / 사용자의 잘못된 요청
        """
        ArticlePhoto = get_object_or_404(ArticlePhoto, pk=pk)
        if ArticlePhoto.article and ArticlePhoto.article.author != request.user:
            raise PermissionDenied
        serializer = ArticlePhotoSerializer(
            ArticlePhoto,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_article_photo = serializer.save()
            return Response(
                ArticlePhotoSerializer(updated_article_photo).data, status=HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """ArticlePhoto.delete

        delete요청 시 제시한 pk의 file을 삭제합니다.

        Args:
            pk (int): 게시글의 사진의 pk를 지정합니다.

        정상일 경우 : 200 / 삭제 완료
        오류일 경우 : 401 / 권한 없음(PermissionDenied)
        """
        photo = get_object_or_404(ArticlePhoto, pk=pk)
        if photo.article and photo.article.owner != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURLView(APIView):
    def post(self, request):
        """GetUploadURL.post

        사용자가 사진을 첨부해서 클라우드플레어에 전송하기전에 먼저 일회용 업로드 url을 요청합니다.

        Args:
            url (str): 클라우드플레어에서 미리 지정한 일회용 url 요청 링크
            one_time_url (str): post요청이 성공할 경우 클라우드플레어에서 온 response. 일회용 업로드 url을 포함하고 있습니다.
        return:
            result(str)): 일회용 url

        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response(result)
