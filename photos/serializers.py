from rest_framework import serializers
from .models import ArticlePhoto, UserPhoto


class ArticlePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePhoto
        fields = (
            "pk",
            "file",
        )


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = (
            "pk",
            "file",
        )
