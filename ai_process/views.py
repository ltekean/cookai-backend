from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageUploadSerializer
from .models import ImageUpload
from roboflow import Roboflow
from rest_framework.permissions import IsAuthenticated
import os
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.models import (
    Article,
)
from articles.serializers import ArticleListSerializer
from ai_process.recommend import collaborative_filtering, content_base
from .labels import LABELS


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        image_serializer = ImageUploadSerializer(data=request.data, partial=True)
        if image_serializer.is_valid():
            try:
                obj = ImageUpload.objects.get(pk=request.user.id)
                obj.delete()
            except:
                pass
            image_serializer.save(user=request.user)
            image_file = image_serializer.validated_data["image"]
            obj = ImageUpload.objects.get(pk=request.user.id)

            rf = Roboflow(api_key=os.environ.get("RF_API_KEY"))
            project = rf.workspace().project("cookai")
            model = project.version("3").model

            prediction = model.predict(
                "./media/" + str(obj.image), confidence=40, overlap=30
            ).json()
            results = []
            for p in prediction["predictions"]:
                results.append(LABELS[p["class"]])
            obj.image.delete(save=False)
            obj.delete()
            return Response({"results": results}, status=201)
        else:
            return Response(image_serializer.errors, status=400)


class RecommendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        func_dict = {"0": collaborative_filtering, "1": content_base}
        select = request.GET.get("recommend", "0")
        list_of_pk, dictionary = func_dict[select](request.user.id)
        articles = sorted(
            Article.objects.filter(id__in=list_of_pk),
            key=lambda x: dictionary[x.id],
            reverse=True,
        )
        serializer = ArticleListSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
