from django.db import models


class ArticlePhoto(models.Model):
    file = models.URLField()
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="photos",
    )


class UserPhoto(models.Model):
    file = models.URLField()

    def __str__(self) -> str:
        return f"Photo File pk : {str(self.pk)}"
