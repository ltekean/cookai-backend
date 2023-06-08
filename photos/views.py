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


class ArticlePhotoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, pk):
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
                ArticlePhotoSerializer(updated_article_photo).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """사진 삭제하기"""
        photo = get_object_or_404(ArticlePhoto, pk=pk)
        if photo.article and photo.article.owner != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURL(APIView):
    def post(self, request):
        """업로드용 URL 가져오기"""
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
