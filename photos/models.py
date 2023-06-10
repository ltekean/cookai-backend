from django.db import models


class ArticlePhoto(models.Model):
    """ArticlePhoto 모델

    article 사진 첨부할때 쓰이는 모델입니다.

    Args:
        file (text): 사진의 url
        article (foreignkey) : article 객체
    """

    file = models.URLField()
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="photos",
    )


class UserPhoto(models.Model):

    """UserPhoto 모델
    Args:
        file (text): 사진의 url
    """

    file = models.URLField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="avatars",
    )

    def __str__(self) -> str:
        return f"Photo File pk : {str(self.pk)}"
