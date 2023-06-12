from django.db import models
from users.models import User

# Create your models here.
# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=10)
    sorts = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    sort = models.CharField(choices=sorts, max_length=10)
    info = models.TextField()

"""article 모델

    Attributes:
    title : 제목 varchar45
    content : 내용 text
    create_at : 작성시간 Datetime
    update_at : 수정시간 Datetime
    author : 작성자 int
    category : 카테고리
    recipe : 레시피 text(html)
        
    """



"""articleHistory 모델

    Attributes:
    Key :int(id)
    user : int(유저)
    article : int(글 번호)
    created_at : Datetime(조회 일자)
    """


# 아티클 모델
class Article(models.Model):
    class Meta:
        db_table = "Article"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
        default="",
        null=False,
    )
    content = models.TextField(
        max_length=500,
        default="",
        null=False,
    )
    update_at = models.DateTimeField(
        auto_now=True,
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
    )
    recipe = models.TextField(
        max_length=500,
    )
    image = models.URLField(
        blank=True,
        null=True,
    )
    likes = models.ManyToManyField(
        User,
        related_name="liked_articles",
        blank=True,
        through='likes'
    )
    bookmarks = models.ManyToManyField(
        User,
        related_name="bookmarked_articles",
        blank=True,
        through='BookMark'
    )


"""Comment 모델

    Attributes:
    comment : 내용 text
    author : 작성자 int
    article : 글 int
    """
# 댓글 모델
class Comment(models.Model):
    class meta:
        db_table = "Comment"

    author =  models.ForeignKey(
        User, on_delete=models.CASCADE,
        primary_key=True
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE
        )
    comment = models.TextField(
        max_length=300,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

class Ingredient():
    ingredient_name = models.ForeignKey(

    )
    ingredient_info = models.TextField(
        null=True,
        default=[],
        max_length=100
    )


class RecipeIngredient():
    ingredient = models.ForeignKey(
        Ingredient
    )
    article = models.ForeignKey(
        Article
    )
    ingredient_quantity = models.IntegerField(
        null=False,
        default = []
    )
    ingredient_unit = models.CharField(
        null=False,
        default= []
    )