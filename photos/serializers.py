from rest_framework import serializers
from .models import ArticlePhoto, UserPhoto


class ArticlePhotoSerializer(serializers.ModelSerializer):
    """article 사진 crud용 시리얼라이저"""

    class Meta:
        model = ArticlePhoto
        fields = (
            "pk",
            "file",
        )
