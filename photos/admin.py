from django.contrib import admin
from .models import ArticlePhoto, UserPhoto


@admin.register(ArticlePhoto)
class ArticlePhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    pass
